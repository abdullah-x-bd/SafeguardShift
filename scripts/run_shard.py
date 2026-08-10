from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
from crisisbench.agent import run_agent
from crisisbench.data import load_tasks
from crisisbench.environment import CrisisEnvironment
from crisisbench.ledger import CostGate, append_jsonl
from crisisbench.openrouter import ModelSpec, OpenRouterClient
from crisisbench.scoring import score_trajectory

CONDITIONS=("full","relevant_ablation","irrelevant_ablation","substitute","compound_ablation")
MODEL_SPECS={
    "gpt41": ModelSpec("openai/gpt-4.1-mini","openai",conservative_request_usd=0.003),
    "gemini": ModelSpec("google/gemini-2.5-flash-lite","google-vertex",conservative_request_usd=0.001,reasoning={"enabled":False}),
    "deepseek": ModelSpec("deepseek/deepseek-v3.2","deepinfra",conservative_request_usd=0.001),
    "mistral": ModelSpec("mistralai/mistral-small-3.2-24b-instruct","venice",conservative_request_usd=0.001),
    "gpt54": ModelSpec("openai/gpt-5.4","openai",temperature=None,conservative_request_usd=0.025),
    "claude": ModelSpec("anthropic/claude-sonnet-5","anthropic",temperature=None,conservative_request_usd=0.03),
}


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--shard-id",required=True)
    ap.add_argument("--model-key",choices=sorted(MODEL_SPECS),required=True)
    ap.add_argument("--domains",default="")
    ap.add_argument("--task-ids",default="")
    ap.add_argument("--max-cost",type=float,required=True)
    ap.add_argument("--output-dir",default="results/private/shards")
    args=ap.parse_args()
    if not os.getenv("OPENROUTER_API_KEY"):
        raise SystemExit("OPENROUTER_API_KEY is required")
    tasks=load_tasks("data/base_tasks")
    domains={x for x in args.domains.split(",") if x}
    task_ids={x for x in args.task_ids.split(",") if x}
    if domains:
        tasks=[t for t in tasks if t.domain in domains]
    if task_ids:
        tasks=[t for t in tasks if t.task_id in task_ids]
    tasks=sorted(tasks,key=lambda t:t.task_id)
    expected=len(tasks)*len(CONDITIONS)
    outdir=Path(args.output_dir); outdir.mkdir(parents=True,exist_ok=True)
    data_path=outdir/f"{args.shard_id}.jsonl"
    cost_path=outdir/f"{args.shard_id}_cost.json"
    gate=CostGate(args.max_cost)
    client=OpenRouterClient(cost_gate=gate)
    spec=MODEL_SPECS[args.model_key]
    completed=0
    error=None
    try:
        for task in tasks:
            for condition in CONDITIONS:
                env=CrisisEnvironment(task,condition)
                record=run_agent(client,spec,env)
                record["score"]=score_trajectory(task,condition,record)
                record["shard_id"]=args.shard_id
                record["shard_cost_usd"]=gate.spent_usd
                append_jsonl(data_path,record)
                completed+=1
                print(f"{args.shard_id} {completed}/{expected} {task.task_id} {condition} ${gate.spent_usd:.6f}")
    except Exception as exc:
        error=f"{type(exc).__name__}: {exc}"
        print(error)
    summary={
        "shard_id":args.shard_id,
        "model":spec.id,
        "provider":spec.provider,
        "expected_trajectories":expected,
        "completed_trajectories":completed,
        "status":"PASS" if completed==expected and error is None else "PARTIAL_OR_FAILED",
        "cost_usd":gate.spent_usd,
        "hard_cap_usd":args.max_cost,
        "error":error,
    }
    cost_path.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2,sort_keys=True))
    if summary["status"] != "PASS":
        raise SystemExit(2)


if __name__=="__main__":
    main()
