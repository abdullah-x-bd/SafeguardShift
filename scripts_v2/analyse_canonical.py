from __future__ import annotations
import argparse,glob,json
from pathlib import Path
from safeguardshift.analysis import analyse,analyse_frontier


def load(pattern:str)->list[dict]:
    files=sorted(glob.glob(pattern))
    rows=[]
    for name in files:
        for line in Path(name).read_text(encoding="utf-8").splitlines():
            if line.strip():rows.append(json.loads(line))
    return rows


def write(path:str,payload:dict)->None:
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")


def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--backbone-glob",default="results/private/v2/model*-rep*-*.jsonl")
    ap.add_argument("--frontier-glob",default="results/private/v2/frontier-*.jsonl")
    ap.add_argument("--backbone-output",default="results/v2/backbone_summary.json")
    ap.add_argument("--frontier-output",default="results/v2/frontier_summary.json")
    args=ap.parse_args()
    backbone=load(args.backbone_glob); frontier=load(args.frontier_glob)
    b=analyse(backbone); f=analyse_frontier(frontier) if frontier else {"status":"NOT_RUN","rows":0}
    write(args.backbone_output,b);write(args.frontier_output,f)
    print(json.dumps({"backbone_status":b["status"],"backbone_rows":len(backbone),"frontier_status":f["status"],"frontier_rows":len(frontier)},sort_keys=True))
    raise SystemExit(0 if b["status"]=="PASS" and (not frontier or f["status"]=="PASS") else 2)

if __name__=="__main__":main()
