from __future__ import annotations
import argparse,json
from pathlib import Path
from safeguardshift.agent import run
from safeguardshift.data import load_tasks
from safeguardshift.environment import Environment
from safeguardshift.ledger import CostGate
from safeguardshift.openrouter import Client,ModelSpec
from safeguardshift.scoring import score

def load_panel(): return json.loads(Path("v2/configs/model_panel_v2.json").read_text())
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--model-index",type=int,required=True); ap.add_argument("--replicate",type=int,choices=(1,2,3),required=True); ap.add_argument("--max-cost",type=float,required=True); ap.add_argument("--output",required=True); a=ap.parse_args()
    m=load_panel()["backbone"][a.model_index]; spec=ModelSpec(m["id"],m["provider"],m["max_token_field"],m["temperature"],m["reserve_usd"])
    gate=CostGate(a.max_cost); client=Client(gate=gate,retries=3); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",encoding="utf-8") as fh:
        for t in load_tasks():
            for c in ("full","relevant_ablation","irrelevant_ablation","substitute","compound_ablation"):
                rec=run(client,spec,Environment(t,c),a.replicate); rec["score"]=score(t,rec); fh.write(json.dumps(rec,sort_keys=True)+"\n"); fh.flush()
    print({"status":"PASS","model":spec.id,"replicate":a.replicate,"trajectories":360,"cost_usd":gate.spent_usd})
if __name__=="__main__":main()
