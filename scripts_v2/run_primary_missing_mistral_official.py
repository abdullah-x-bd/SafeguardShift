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


class RecoveryClient(Client):
    def __init__(self, *args, transport_retries: int = 5, **kwargs):
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
                last = RuntimeError(f"OpenRouter successful response without choices: {json.dumps(resp, sort_keys=True)[:1200]}")
            if attempt == self.transport_retries:
                raise last
            self.transport_retry_count += 1
            time.sleep(min(2**attempt, 8))
        raise last or RuntimeError("recovery transport retry exhausted")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cells", required=True)
    ap.add_argument("--task-prefix", required=True)
    ap.add_argument("--max-cost", type=float, required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    panel = json.loads(Path("v2/configs/model_panel_v2.json").read_text(encoding="utf-8"))["backbone"]
    model = panel[3]
    spec = ModelSpec(model["id"], "mistral", model["max_token_field"], model["temperature"], 0.0002)
    tasks = {t.task_id: t for t in load_tasks()}
    requested = [c for c in json.loads(Path(args.cells).read_text(encoding="utf-8")) if int(c["model_index"]) == 3 and str(c["task_id"]).startswith(args.task_prefix)]
    gate = CostGate(args.max_cost)
    client = RecoveryClient(gate=gate, retries=4, transport_retries=5)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    completed = 0
    with out.open("w", encoding="utf-8") as fh:
        for cell in requested:
            before = client.transport_retry_count
            task = tasks[str(cell["task_id"])]
            rec = run(client, spec, Environment(task, str(cell["condition"])), int(cell["replicate"]))
            rec["score"] = score(task, rec)
            rec["exact_recovery"] = True
            rec["recovery_policy"] = "fills only cells absent from the fixed 2,972-cell primary baseline under amendment 007"
            rec["recovery_transport_retries"] = client.transport_retry_count - before
            rec["recovery_provider_override"] = "mistral"
            rec["original_planned_provider"] = model["provider"]
            fh.write(json.dumps(rec, sort_keys=True) + "\n")
            fh.flush()
            completed += 1
    print(json.dumps({"status": "PASS", "model": spec.id, "provider": spec.provider, "task_prefix": args.task_prefix, "requested": len(requested), "completed": completed, "transport_retries": client.transport_retry_count, "cost_usd": gate.spent_usd}, sort_keys=True))


if __name__ == "__main__":
    main()
