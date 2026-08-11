from __future__ import annotations
import argparse,json
from pathlib import Path
from safeguardshift.agent import run
from safeguardshift.data import load_tasks
from safeguardshift.environment import Environment
from safeguardshift.ledger import CostGate
from safeguardshift.openrouter import Client,ModelSpec
from safeguardshift.scoring import score

CONDITIONS={"full","relevant_ablation","irrelevant_ablation","substitute","compound_ablation"}
RESERVES={0:0.0005,1:0.0002,2:0.0002,3:0.0001}

def main()->None:
    ap=argparse.ArgumentParser();ap.add_argument("--cells",required=True);ap.add_argument("--domain");ap.add_argument("--max-cost",type=float,required=True);ap.add_argument("--output",required=True);a=ap.parse_args()
    all_cells=json.loads(Path(a.cells).read_text(encoding="utf-8"));panel=json.loads(Path("v2/configs/model_panel_v2.json").read_text(encoding="utf-8"))["backbone"];tasks={t.task_id:t for t in load_tasks()}
    cells=[c for c in all_cells if not a.domain or tasks[str(c["task_id"])].domain==a.domain]
    gate=CostGate(a.max_cost);out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);written=[]
    with out.open("w",encoding="utf-8") as fh:
        for cell in cells:
            mi=int(cell["model_index"]);task_id=str(cell["task_id"]);rep=int(cell["replicate"]);condition=str(cell["condition"])
            if mi not in range(4) or task_id not in tasks or rep not in (1,2,3) or condition not in CONDITIONS:raise SystemExit(f"invalid recovery cell {cell}")
            m=panel[mi];spec=ModelSpec(m["id"],m["provider"],m["max_token_field"],m["temperature"],RESERVES[mi]);client=Client(gate=gate,retries=8 if mi==2 else 4)
            rec=run(client,spec,Environment(tasks[task_id],condition),rep);rec["score"]=score(tasks[task_id],rec);rec["exact_recovery"]=True
            fh.write(json.dumps(rec,sort_keys=True)+"\n");fh.flush();written.append((m["id"],task_id,rep,condition))
    print({"status":"PASS","cells":len(written),"cost_usd":gate.spent_usd})

if __name__=="__main__":main()
