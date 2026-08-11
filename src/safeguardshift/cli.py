from __future__ import annotations
import argparse,json
from .verify import verify
from .freeze import build
from .data import load_tasks
from .oracle import run_oracle
def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="cmd",required=True)
    sub.add_parser("verify"); sub.add_parser("freeze"); sub.add_parser("oracle")
    a=p.parse_args()
    if a.cmd=="verify": print(json.dumps(verify(),indent=2,sort_keys=True))
    elif a.cmd=="freeze": print(json.dumps(build(),indent=2,sort_keys=True))
    else:
        rows=[run_oracle(t,c) for t in load_tasks() for c in ("full","relevant_ablation","irrelevant_ablation","substitute","compound_ablation")]
        print(json.dumps({"status":"PASS","trajectories":len(rows),"substitute_success":sum(r["score"]["substitute_used"] for r in rows if r["condition"]=="substitute")},indent=2))
