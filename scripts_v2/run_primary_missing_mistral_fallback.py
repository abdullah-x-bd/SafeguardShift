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
PROVIDER_POLICY = {
    "order": ["deepinfra", "venice"],
    "allow_fallbacks": True,
    "require_parameters": True,
    "ignore": ["mistral"],
}


class FallbackClient:
    def __init__(self, gate: CostGate, retries: int = 10):
        self.key = os.getenv("OPENROUTER_API_KEY")
        if not self.key:
            raise RuntimeError("OPENROUTER_API_KEY is not set")
        self.gate = gate
        self.retries = retries
        self.retry_count = 0
        self.events: list[dict[str, Any]] = []

    def reset_events(self) -> None:
        self.events = []

    def chat(self, spec: ModelSpec, messages: list[dict], tools: list[dict], tool_choice: Any = "auto", max_tokens: int = 350) -> dict:
        body = {
            "model": spec.id,
            "messages": messages,
            "tools": tools,
            "tool_choice": tool_choice,
            spec.max_token_field: max_tokens,
            "provider": PROVIDER_POLICY,
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
                    self.events.append({"status": "malformed_json", "attempt": attempt + 1, "request_sha256": reqhash})
                    last = exc
                else:
                    usage = payload.get("usage") or {}
                    cost = usage.get("cost")
                    charged = float(cost) if isinstance(cost, (int, float)) else spec.reserve_usd
                    self.gate.add(charged)
                    event = {
                        "attempt": attempt + 1,
                        "request_sha256": reqhash,
                        "cost_usd": charged,
                        "provider": payload.get("provider"),
                        "openrouter_metadata": payload.get("openrouter_metadata"),
                    }
                    choices = payload.get("choices")
                    if isinstance(choices, list) and choices:
                        event["status"] = "accepted_response"
                        self.events.append(event)
                        payload["_safeguardshift_request"] = {
                            "sha256": reqhash,
                            "requested_model": spec.id,
                            "routing_policy": PROVIDER_POLICY,
                        }
                        return payload
                    event["status"] = "no_choices"
                    self.events.append(event)
                    last = RuntimeError("OpenRouter returned a successful response without choices")
            except urllib.error.HTTPError as exc:
                text = exc.read().decode(errors="replace")
                try:
                    parsed = json.loads(text)
                except json.JSONDecodeError:
                    parsed = {"raw_prefix": text[:800]}
                self.events.append({
                    "status": "http_error",
                    "attempt": attempt + 1,
                    "request_sha256": reqhash,
                    "http_code": exc.code,
                    "error": parsed.get("error") if isinstance(parsed, dict) else parsed,
                    "openrouter_metadata": parsed.get("openrouter_metadata") if isinstance(parsed, dict) else None,
                })
                last = RuntimeError(f"OpenRouter HTTP {exc.code}: {text[:1200]}")
                if exc.code not in RETRY_HTTP:
                    raise last
            except (urllib.error.URLError, TimeoutError) as exc:
                self.events.append({"status": "transport_error", "attempt": attempt + 1, "request_sha256": reqhash, "error_type": type(exc).__name__})
                last = exc
            if attempt == self.retries:
                raise last or RuntimeError("fallback recovery request failed")
            self.retry_count += 1
            time.sleep(min(2**attempt, 4))
        raise last or RuntimeError("fallback recovery request failed")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cells", required=True)
    ap.add_argument("--task-prefix", required=True)
    ap.add_argument("--max-cost", type=float, required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--failure-output", required=True)
    args = ap.parse_args()

    panel = json.loads(Path("v2/configs/model_panel_v2.json").read_text(encoding="utf-8"))["backbone"]
    model = panel[3]
    spec = ModelSpec(model["id"], "fallback", model["max_token_field"], model["temperature"], 0.0003)
    tasks = {task.task_id: task for task in load_tasks()}
    requested = [
        cell for cell in json.loads(Path(args.cells).read_text(encoding="utf-8"))
        if int(cell["model_index"]) == 3 and str(cell["task_id"]).startswith(args.task_prefix)
    ]
    gate = CostGate(args.max_cost)
    client = FallbackClient(gate=gate, retries=10)
    out = Path(args.output); out.parent.mkdir(parents=True, exist_ok=True)
    failures_path = Path(args.failure_output); failures_path.parent.mkdir(parents=True, exist_ok=True)
    completed = failures = 0

    with out.open("w", encoding="utf-8") as good, failures_path.open("w", encoding="utf-8") as bad:
        for cell in requested:
            task = tasks[str(cell["task_id"])]
            before_retry = client.retry_count
            before_cost = gate.spent_usd
            client.reset_events()
            try:
                rec = run(client, spec, Environment(task, str(cell["condition"])), int(cell["replicate"]))
            except Exception as exc:
                bad.write(json.dumps({
                    "cell": cell,
                    "error_type": type(exc).__name__,
                    "error": str(exc)[:1600],
                    "routing_events": client.events,
                    "transport_retries": client.retry_count - before_retry,
                    "cost_usd": gate.spent_usd - before_cost,
                    "policy": "transport failure only; no behavioral row accepted",
                }, sort_keys=True) + "\n")
                bad.flush(); failures += 1
                text = str(exc)
                if "cost gate" in text or "OpenRouter HTTP 401" in text or "OpenRouter HTTP 402" in text:
                    raise
                continue
            rec["score"] = score(task, rec)
            rec["exact_recovery"] = True
            rec["recovery_policy"] = "fills only keys absent from the fixed amendment-009 matrix under conditional amendment 010"
            rec["original_planned_provider"] = model["provider"]
            rec["recovery_routing_policy"] = PROVIDER_POLICY
            rec["recovery_transport_retries"] = client.retry_count - before_retry
            rec["recovery_routing_events"] = client.events
            good.write(json.dumps(rec, sort_keys=True) + "\n"); good.flush(); completed += 1

    print(json.dumps({
        "status": "PASS" if failures == 0 else "PARTIAL",
        "model": spec.id,
        "task_prefix": args.task_prefix,
        "requested": len(requested),
        "completed": completed,
        "failures": failures,
        "transport_retries": client.retry_count,
        "cost_usd": gate.spent_usd,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
