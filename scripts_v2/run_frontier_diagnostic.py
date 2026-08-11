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

CONDITIONS = ("full", "relevant_ablation", "irrelevant_ablation", "substitute", "compound_ablation")


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-index", type=int, choices=(0, 1), required=True)
    ap.add_argument("--max-cost", type=float, required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    panel = load_json("v2/configs/model_panel_v2.json")["frontier_diagnostic"]
    subset = load_json("v2/configs/frontier_subset_v2.json")
    task_map = {t.task_id: t for t in load_tasks()}
    task_ids = subset["task_ids"]
    missing = [task_id for task_id in task_ids if task_id not in task_map]
    if missing:
        raise SystemExit(f"frontier subset contains unknown task IDs: {missing}")

    m = panel[args.model_index]
    spec = ModelSpec(m["id"], m["provider"], m["max_token_field"], m["temperature"], m["reserve_usd"])
    gate = CostGate(args.max_cost)
    client = Client(gate=gate, retries=3)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)

    completed = 0
    with out.open("w", encoding="utf-8") as fh:
        for task_id in task_ids:
            task = task_map[task_id]
            for condition in CONDITIONS:
                rec = run(client, spec, Environment(task, condition), replicate=1)
                rec["score"] = score(task, rec)
                rec["frontier_diagnostic"] = True
                fh.write(json.dumps(rec, sort_keys=True) + "\n")
                fh.flush()
                completed += 1

    expected = 60
    if completed != expected:
        raise SystemExit(f"expected {expected} trajectories, wrote {completed}")
    print({"status": "PASS", "model": spec.id, "trajectories": completed, "cost_usd": gate.spent_usd})


if __name__ == "__main__":
    main()
