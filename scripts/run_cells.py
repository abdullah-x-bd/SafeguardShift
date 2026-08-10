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

MODELS={
    "gpt41":ModelSpec("openai/gpt-4.1-mini","openai",conservative_request_usd=0.003),
    "deepseek":ModelSpec("deepseek/deepseek-v3.2","deepinfra",conservative_request_usd=0.001),
}


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--model-key",choices=sorted(MODELS),required=True)
    ap.add_argument("--cells",required=True,help="comma-separated task_id:condition entries")
    ap.add_argument("--max-cost",type=float,required=True)
    ap.add_argument("--max-retries",type=int,default=3)
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    if not os.getenv("OPENROUTER_API_KEY"): raise SystemExit("OPENROUTER_API_KEY is required")
    task_map={t.task_id:t for t in load_tasks("data/base_tasks")}
    cells=[]
    for item in args.cells.split(","):
        task_id,condition=item.split(":",1)
        cells.append((task_id,condition))
    gate=CostGate(args.max_cost)
    client=OpenRouterClient(cost_gate=gate,max_retries=args.max_retries)
    spec=MODELS[args.model_key]
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    done=0
    error=None
    try:
        for task_id,condition in cells:
            env=CrisisEnvironment(task_map[task_id],condition)
            record=run_agent(client,spec,env)
            record["score"]=score_trajectory(task_map[task_id],condition,record)
            record["exact_cell_recovery"]=True
            record["cumulative_cost_usd"]=gate.spent_usd
            append_jsonl(out,record)
            done+=1
            print(f"{done}/{len(cells)} {task_id} {condition} ${gate.spent_usd:.6f}")
    except Exception as exc:
        error=f"{type(exc).__name__}: {exc}"
        print(error)
    summary={"status":"PASS" if done==len(cells) and error is None else "PARTIAL_OR_FAILED","model":spec.id,"provider":spec.provider,"expected":len(cells),"completed":done,"cost_usd":gate.spent_usd,"hard_cap_usd":args.max_cost,"max_retries":args.max_retries,"error":error}
    out.with_name(out.stem+"_cost.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2,sort_keys=True))
    if summary["status"]!="PASS": raise SystemExit(2)

if __name__=="__main__": main()
