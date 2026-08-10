from __future__ import annotations
import argparse, json
from .artifacts import write_freeze
from .data import load_tasks
from .render import render_scenario
from .verify import write_verification

def main() -> None:
    p=argparse.ArgumentParser(prog="crisisbench"); sub=p.add_subparsers(dest="cmd",required=True)
    sub.add_parser("verify"); sub.add_parser("freeze")
    r=sub.add_parser("render"); r.add_argument("task_id"); r.add_argument("condition")
    args=p.parse_args()
    if args.cmd=="verify": print(json.dumps(write_verification("."),indent=2))
    elif args.cmd=="freeze": print(json.dumps(write_freeze("."),indent=2))
    elif args.cmd=="render":
        task=next(t for t in load_tasks("data/base_tasks") if t.task_id==args.task_id); print(render_scenario(task,args.condition))

if __name__ == "__main__":
    main()
