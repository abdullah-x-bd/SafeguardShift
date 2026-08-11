from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from safeguardshift.agent import run
from safeguardshift.data import load_tasks
from safeguardshift.environment import Environment
from safeguardshift.ledger import CostGate
from safeguardshift.openrouter import Client, ModelSpec
from safeguardshift.scoring import score

RESERVES = {0: 0.0005, 1: 0.0002, 3: 0.0001}
RETRYABLE_HTTP_CODES = (408, 409, 429, 500, 502, 503, 504)


class RecoveryClient(Client):
    """Retry only transport-level responses that cannot constitute an agent turn."""

    def __init__(self, *args, transport_retries: int = 3, **kwargs):
        super().__init__(*args, **kwargs)
        self.transport_retries = transport_retries
        self.transport_retry_count = 0

    def chat(self, spec, messages, tools, tool_choice="auto", max_tokens=350):
        last = None
        for attempt in range(self.transport_retries + 1):
            try:
                resp = super().chat(spec, messages, tools, tool_choice=tool_choice, max_tokens=max_tokens)
            except json.JSONDecodeError as exc:
                last = exc
            else:
                choices = resp.get("choices")
                if isinstance(choices, list) and choices:
                    return resp
                last = RuntimeError("OpenRouter returned a successful response without choices")
            if attempt == self.transport_retries:
                raise last
            self.transport_retry_count += 1
            time.sleep(min(2**attempt, 4))
        raise last or RuntimeError("recovery transport retry exhausted")


def is_transport_failure(exc: Exception) -> bool:
    if isinstance(exc, json.JSONDecodeError):
        return True
    if not isinstance(exc, RuntimeError):
        return False
    text = str(exc)
    if "successful response without choices" in text:
        return True
    if text.startswith("OpenRouter HTTP "):
        try:
            code = int(text.split()[2].rstrip(":"))
        except (IndexError, ValueError):
            return False
        return code in RETRYABLE_HTTP_CODES
    return False


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cells", required=True)
    ap.add_argument("--model-index", type=int, required=True, choices=(0, 1, 3))
    ap.add_argument("--task-prefix")
    ap.add_argument("--max-cost", type=float, required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--failure-output")
    args = ap.parse_args()

    panel = json.loads(Path("v2/configs/model_panel_v2.json").read_text(encoding="utf-8"))["backbone"]
    model = panel[args.model_index]
    spec = ModelSpec(model["id"], model["provider"], model["max_token_field"], model["temperature"], RESERVES[args.model_index])
    tasks = {t.task_id: t for t in load_tasks()}
    requested = [c for c in json.loads(Path(args.cells).read_text(encoding="utf-8")) if int(c["model_index"]) == args.model_index]
    if args.task_prefix:
        requested = [c for c in requested if str(c["task_id"]).startswith(args.task_prefix)]

    gate = CostGate(args.max_cost)
    client = RecoveryClient(gate=gate, retries=4, transport_retries=3)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    failures: list[dict] = []
    completed = 0
    budget_stopped = False

    with out.open("w", encoding="utf-8") as fh:
        for position, cell in enumerate(requested):
            before = client.transport_retry_count
            task = tasks[str(cell["task_id"])]
            try:
                rec = run(client, spec, Environment(task, str(cell["condition"])), int(cell["replicate"]))
            except Exception as exc:
                if isinstance(exc, RuntimeError) and str(exc).startswith("cost gate would exceed"):
                    failures.append({
                        "cell": cell,
                        "kind": "budget_gate",
                        "error": str(exc),
                        "position": position,
                    })
                    budget_stopped = True
                    break
                if is_transport_failure(exc):
                    failures.append({
                        "cell": cell,
                        "kind": "transport",
                        "error": str(exc),
                        "position": position,
                        "transport_retries": client.transport_retry_count - before,
                    })
                    continue
                raise

            rec["score"] = score(task, rec)
            rec["exact_recovery"] = True
            rec["recovery_policy"] = "fills only absent expected cells; cell-local identical-request retry for transport-invalid responses; never outcome-contingent"
            rec["recovery_transport_retries"] = client.transport_retry_count - before
            fh.write(json.dumps(rec, sort_keys=True) + "\n")
            fh.flush()
            completed += 1

    if args.failure_output:
        fp = Path(args.failure_output)
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(json.dumps(failures, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    payload = {
        "status": "PASS" if completed == len(requested) else "PARTIAL",
        "model": spec.id,
        "task_prefix": args.task_prefix,
        "requested": len(requested),
        "completed": completed,
        "failed_or_unattempted": len(requested) - completed,
        "recorded_failures": len(failures),
        "budget_stopped": budget_stopped,
        "transport_retries": client.transport_retry_count,
        "cost_usd": gate.spent_usd,
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
