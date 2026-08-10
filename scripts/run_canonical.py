from __future__ import annotations
import argparse
import os
from crisisbench.agent import run_agent
from crisisbench.data import load_tasks
from crisisbench.environment import CrisisEnvironment
from crisisbench.ledger import CostGate, append_jsonl
from crisisbench.openrouter import ModelSpec, OpenRouterClient
from crisisbench.scoring import score_trajectory

BACKBONE = [
    ModelSpec("openai/gpt-4.1-mini", "openai"),
    ModelSpec("google/gemini-2.5-flash-lite", "google-vertex"),
    ModelSpec("deepseek/deepseek-v3.2", "deepinfra"),
    ModelSpec("mistralai/mistral-small-3.2-24b-instruct", "deepinfra"),
]
FRONTIER = [
    ModelSpec("openai/gpt-5", "openai", temperature=None, max_token_field="max_completion_tokens"),
    ModelSpec("anthropic/claude-sonnet-5", "anthropic", temperature=None),
]
CONDITIONS = ["full", "relevant_ablation", "irrelevant_ablation", "substitute", "compound_ablation"]
FRONTIER_TASK_IDS = {
    "CB-PH-001", "CB-CY-001", "CB-CI-001", "CB-DR-001", "CB-CC-001", "CB-PG-001",
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="results/private/canonical.jsonl")
    ap.add_argument("--max-cost", type=float, default=5.10)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--include-frontier", action="store_true")
    args = ap.parse_args()
    if not os.getenv("OPENROUTER_API_KEY"):
        raise SystemExit("OPENROUTER_API_KEY is required")
    gate = CostGate(args.max_cost)
    client = OpenRouterClient(cost_gate=gate, conservative_request_usd=0.02)
    tasks = load_tasks("data/base_tasks")
    n = 0
    panels = [(BACKBONE, tasks)]
    if args.include_frontier:
        panels.append((FRONTIER, [t for t in tasks if t.task_id in FRONTIER_TASK_IDS]))
    for models, selected_tasks in panels:
        for spec in models:
            for task in selected_tasks:
                for condition in CONDITIONS:
                    if args.limit and n >= args.limit:
                        print(f"stopped after {n} trajectories; provider-reported/conservative spend ${gate.spent_usd:.4f}")
                        return
                    env = CrisisEnvironment(task, condition)
                    record = run_agent(client, spec, env)
                    record["score"] = score_trajectory(task, condition, record)
                    record["cumulative_cost_usd"] = gate.spent_usd
                    append_jsonl(args.output, record)
                    n += 1
                    print(f"{n}: {spec.id} {task.task_id} {condition} cumulative=${gate.spent_usd:.4f}")
    print(f"complete: {n} trajectories; cumulative=${gate.spent_usd:.4f}")


if __name__ == "__main__":
    main()
