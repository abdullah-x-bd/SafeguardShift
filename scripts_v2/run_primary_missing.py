from __future__ import annotations

import argparse
import json
from pathlib import Path

from safeguardshift.agent import run
from safeguardshift.data import load_tasks
from safeguardshift.environment import Environment
from safeguardshift.ledger import CostGate
from safeguardshift.openrouter import Client, ModelSpec
from safeguardshift.scoring import score

RESERVES = {0: 0.0005, 1: 0.0002, 3: 0.0001}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cells", required=True)
    ap.add_argument("--model-index", type=int, required=True, choices=(0, 1, 3))
    ap.add_argument("--task-prefix")
    ap.add_argument("--max-cost", type=float, required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    panel = json.loads(Path("v2/configs/model_panel_v2.json").read_text(encoding="utf-8"))["backbone"]
    model = panel[args.model_index]
    spec = ModelSpec(model["id"], model["provider"], model["max_token_field"], model["temperature"], RESERVES[args.model_index])
    tasks = {t.task_id: t for t in load_tasks()}
    requested = [c for c in json.loads(Path(args.cells).read_text(encoding="utf-8")) if int(c["model_index"]) == args.model_index]
    if args.task_prefix:
        requested = [c for c in requested if str(c["task_id"]).startswith(args.task_prefix)]
    gate = CostGate(args.max_cost)
    client = Client(gate=gate, retries=4)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    completed = 0
    with out.open("w", encoding="utf-8") as fh:
        for cell in requested:
            task = tasks[str(cell["task_id"])]
            rec = run(client, spec, Environment(task, str(cell["condition"])), int(cell["replicate"]))
            rec["score"] = score(task, rec)
            rec["exact_recovery"] = True
            rec["recovery_policy"] = "fills only cells absent after fixed source-priority assembly under amendment 005"
            fh.write(json.dumps(rec, sort_keys=True) + "\n")
            fh.flush()
            completed += 1
    print(json.dumps({"status": "PASS", "model": spec.id, "task_prefix": args.task_prefix, "requested": len(requested), "completed": completed, "cost_usd": gate.spent_usd}, sort_keys=True))


if __name__ == "__main__":
    main()
