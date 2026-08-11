from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from safeguardshift.agent import run
from safeguardshift.data import load_tasks
from safeguardshift.environment import Environment
from safeguardshift.ledger import CostGate, request_hash
from safeguardshift.openrouter import ModelSpec
from safeguardshift.scoring import score

URL = "https://openrouter.ai/api/v1/chat/completions"
RETRY_HTTP = {408, 409, 429, 500, 502, 503, 504, 529}


class RoutedRecoveryClient:
    def __init__(self, gate: CostGate, retries: int = 6):
        self.key = os.getenv("OPENROUTER_API_KEY")
        if not self.key:
            raise RuntimeError("OPENROUTER_API_KEY is not set")
        self.gate = gate
        self.retries = retries
        self.transport_retry_count = 0
        self.routing_events: list[dict[str, Any]] = []

    def reset_trajectory_events(self) -> None:
        self.routing_events = []

    def chat(self, spec: ModelSpec, messages: list[dict], tools: list[dict], tool_choice: Any = "auto", max_tokens: int = 350) -> dict:
        body = {
            "model": spec.id,
            "messages": messages,
            "tools": tools,
            "tool_choice": tool_choice,
            spec.max_token_field: max_tokens,
            "provider": {
                "require_parameters": True,
                "allow_fallbacks": True,
                "ignore": ["venice", "mistral"],
            },
        }
        if spec.temperature is not None:
            body["temperature"] = spec.temperature
        reqhash = request_hash(body)
        last: Exception | None = None

        for attempt in range(self.retries + 1):
            self.gate.reserve(spec.reserve_usd)
            req = urllib.request.Request(
                URL,
                data=json.dumps(body).encode(),
                headers={
                    "Authorization": f"Bearer {self.key}",
                    "Content-Type": "application/json",
                    "X-Title": "SafeguardShift",
                    "X-OpenRouter-Metadata": "enabled",
                },
                method="POST",
            )
            try:
                with urllib.request.urlopen(req, timeout=120) as response:
                    raw = response.read()
                try:
                    payload = json.loads(raw)
                except json.JSONDecodeError as exc:
                    self.gate.add(spec.reserve_usd)
                    self.routing_events.append({"status": "malformed_json", "request_sha256": reqhash, "attempt": attempt + 1})
                    last = exc
                else:
                    usage = payload.get("usage") or {}
                    cost = usage.get("cost")
                    charged = float(cost) if isinstance(cost, (int, float)) else spec.reserve_usd
                    self.gate.add(charged)
                    metadata = payload.get("openrouter_metadata")
                    choices = payload.get("choices")
                    if isinstance(choices, list) and choices:
                        self.routing_events.append({
                            "status": "accepted_response",
                            "request_sha256": reqhash,
                            "attempt": attempt + 1,
                            "cost_usd": charged,
                            "openrouter_metadata": metadata,
                            "provider": payload.get("provider"),
                        })
                        payload["_safeguardshift_request"] = {
                            "sha256": reqhash,
                            "requested_model": spec.id,
                            "routing_policy": "require_parameters; fallbacks enabled; venice and mistral excluded",
                        }
                        return payload
                    self.routing_events.append({
                        "status": "no_choices",
                        "request_sha256": reqhash,
                        "attempt": attempt + 1,
                        "cost_usd": charged,
                        "openrouter_metadata": metadata,
                        "provider": payload.get("provider"),
                    })
                    last = RuntimeError("OpenRouter returned a successful response without choices")
            except urllib.error.HTTPError as exc:
                text = exc.read().decode(errors="replace")
                try:
                    error_payload = json.loads(text)
                except json.JSONDecodeError:
                    error_payload = {"raw_prefix": text[:800]}
                self.routing_events.append({
                    "status": "http_error",
                    "request_sha256": reqhash,
                    "attempt": attempt + 1,
                    "http_code": exc.code,
                    "openrouter_metadata": error_payload.get("openrouter_metadata") if isinstance(error_payload, dict) else None,
                    "error": error_payload.get("error") if isinstance(error_payload, dict) else error_payload,
                })
                last = RuntimeError(f"OpenRouter HTTP {exc.code}: {text[:1200]}")
                if exc.code not in RETRY_HTTP:
                    raise last
            except (urllib.error.URLError, TimeoutError) as exc:
                self.routing_events.append({"status": "transport_error", "request_sha256": reqhash, "attempt": attempt + 1, "error_type": type(exc).__name__})
                last = exc

            if attempt == self.retries:
                raise last or RuntimeError("routed recovery request failed")
            self.transport_retry_count += 1
            time.sleep(min(2**attempt, 8))

        raise last or RuntimeError("routed recovery request failed")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cells", required=True)
    ap.add_argument("--task-prefix", required=True)
    ap.add_argument("--max-cost", type=float, required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    panel = json.loads(Path("v2/configs/model_panel_v2.json").read_text(encoding="utf-8"))["backbone"]
    model = panel[3]
    spec = ModelSpec(model["id"], "routed", model["max_token_field"], model["temperature"], 0.0003)
    tasks = {task.task_id: task for task in load_tasks()}
    requested = [
        cell
        for cell in json.loads(Path(args.cells).read_text(encoding="utf-8"))
        if int(cell["model_index"]) == 3 and str(cell["task_id"]).startswith(args.task_prefix)
    ]

    gate = CostGate(args.max_cost)
    client = RoutedRecoveryClient(gate=gate, retries=6)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    completed = 0

    with out.open("w", encoding="utf-8") as fh:
        for cell in requested:
            task = tasks[str(cell["task_id"])]
            before_retries = client.transport_retry_count
            client.reset_trajectory_events()
            rec = run(client, spec, Environment(task, str(cell["condition"])), int(cell["replicate"]))
            rec["score"] = score(task, rec)
            rec["exact_recovery"] = True
            rec["recovery_policy"] = "fills only absent keys from fixed 2,972-cell primary baseline under amendment 008"
            rec["original_planned_provider"] = model["provider"]
            rec["recovery_routing_policy"] = {"require_parameters": True, "allow_fallbacks": True, "ignore": ["venice", "mistral"]}
            rec["recovery_transport_retries"] = client.transport_retry_count - before_retries
            rec["recovery_routing_events"] = client.routing_events
            fh.write(json.dumps(rec, sort_keys=True) + "\n")
            fh.flush()
            completed += 1

    print(json.dumps({
        "status": "PASS",
        "model": spec.id,
        "task_prefix": args.task_prefix,
        "requested": len(requested),
        "completed": completed,
        "transport_retries": client.transport_retry_count,
        "cost_usd": gate.spent_usd,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
