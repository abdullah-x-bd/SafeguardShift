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

# Exact accepted-prefix lengths after combining the original Mistral shards and the
# six first-pass Mistral recovery artifacts. Each domain/replicate sequence is the
# frozen task order × CONDITION order, 60 cells per replicate.
ACCEPTED_PREFIX = {
    "public_health": {1: 60, 2: 40, 3: 19},
    "critical_infrastructure": {1: 48, 2: 1, 3: 26},
    "cyber_incident": {1: 60, 2: 60, 3: 17},
    "disaster_response": {1: 60, 2: 26, 3: 12},
    "public_governance": {1: 60, 2: 59, 3: 1},
    "crisis_communication": {1: 59, 2: 25, 3: 19},
}
EXPECTED_MISSING = {
    "public_health": 61,
    "critical_infrastructure": 105,
    "cyber_incident": 43,
    "disaster_response": 82,
    "public_governance": 60,
    "crisis_communication": 77,
}


def residual_cells(domain: str):
    tasks = [t for t in load_tasks() if t.domain == domain]
    sequence = [(t, c) for t in tasks for c in CONDITIONS]
    out = []
    for rep in (1, 2, 3):
        out.extend((t, rep, c) for t, c in sequence[ACCEPTED_PREFIX[domain][rep]:])
    if len(out) != EXPECTED_MISSING[domain]:
        raise RuntimeError(f"residual contract mismatch for {domain}: {len(out)}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain", required=True, choices=sorted(ACCEPTED_PREFIX))
    ap.add_argument("--max-cost", type=float, required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    model = json.loads(Path("v2/configs/model_panel_v2.json").read_text(encoding="utf-8"))["backbone"][3]
    spec = ModelSpec(model["id"], model["provider"], model["max_token_field"], model["temperature"], 0.0001)
    gate = CostGate(args.max_cost)
    client = Client(gate=gate, retries=4)
    cells = residual_cells(args.domain)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    completed = 0
    with out.open("w", encoding="utf-8") as fh:
        for task, rep, condition in cells:
            rec = run(client, spec, Environment(task, condition), rep)
            rec["score"] = score(task, rec)
            rec["exact_recovery"] = True
            rec["recovery_policy"] = "amendment 005; exact domain suffix after fixed original and first-pass recovery prefixes"
            fh.write(json.dumps(rec, sort_keys=True) + "\n")
            fh.flush()
            completed += 1
    print(json.dumps({"status": "PASS", "domain": args.domain, "requested": len(cells), "completed": completed, "cost_usd": gate.spent_usd}, sort_keys=True))


if __name__ == "__main__":
    main()
