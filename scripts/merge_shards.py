from __future__ import annotations
import argparse
import json
from pathlib import Path
from crisisbench.analysis import analyse, load_jsonl


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--input-dir",default="results/collected_shards")
    ap.add_argument("--output",default="results/private/canonical.jsonl")
    ap.add_argument("--summary",default="results/v1/summary.json")
    ap.add_argument("--cost-summary",default="results/v1/cost_summary.json")
    args=ap.parse_args()
    root=Path(args.input_dir)
    data_files=sorted(p for p in root.rglob("*.jsonl") if p.name != Path(args.output).name)
    cost_files=sorted(root.rglob("*_cost.json"))
    rows=[]
    for path in data_files:
        rows.extend(load_jsonl(path))
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",encoding="utf-8") as f:
        for row in sorted(rows,key=lambda r:(r.get("model",""),r.get("task_id",""),r.get("condition",""))):
            f.write(json.dumps(row,ensure_ascii=False,sort_keys=True)+"\n")
    analysis=analyse(rows)
    s=Path(args.summary); s.parent.mkdir(parents=True,exist_ok=True)
    s.write_text(json.dumps(analysis,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    shard_costs=[json.loads(p.read_text(encoding="utf-8")) for p in cost_files]
    cost_summary={
        "canonical_cost_usd":sum(float(x.get("cost_usd",0.0)) for x in shard_costs),
        "canonical_hard_cap_sum_usd":sum(float(x.get("hard_cap_usd",0.0)) for x in shard_costs),
        "shards":shard_costs,
    }
    c=Path(args.cost_summary); c.parent.mkdir(parents=True,exist_ok=True)
    c.write_text(json.dumps(cost_summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"analysis":analysis,"cost":cost_summary},indent=2,sort_keys=True))
    if analysis.get("status") != "PASS" or any(x.get("status") != "PASS" for x in shard_costs) or len(shard_costs)!=14:
        raise SystemExit(2)


if __name__=="__main__":
    main()
