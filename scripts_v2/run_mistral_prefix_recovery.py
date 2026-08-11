from __future__ import annotations
import argparse,json
from pathlib import Path
from safeguardshift.agent import run
from safeguardshift.data import load_tasks
from safeguardshift.environment import Environment
from safeguardshift.ledger import CostGate
from safeguardshift.openrouter import Client,ModelSpec
from safeguardshift.scoring import score

CONDITIONS=("full","relevant_ablation","irrelevant_ablation","substitute","compound_ablation")
PREFIXES={
 "public_health":{1:29,2:15},
 "critical_infrastructure":{1:23,2:1},
 "cyber_incident":{1:38,2:15},
 "disaster_response":{1:27,2:17},
 "public_governance":{1:44,2:3},
 "crisis_communication":{1:29},
}

def cells(domain:str)->list[dict]:
    tasks=[t for t in load_tasks() if t.domain==domain];out=[]
    for rep,n in sorted(PREFIXES[domain].items()):
        seq=[(t,c) for t in tasks for c in CONDITIONS]
        out.extend({"task":t,"replicate":rep,"condition":c} for t,c in seq[n:])
    return out

def main()->None:
    ap=argparse.ArgumentParser();ap.add_argument("--domain",required=True,choices=sorted(PREFIXES));ap.add_argument("--max-cost",type=float,required=True);ap.add_argument("--output",required=True);a=ap.parse_args()
    m=json.loads(Path("v2/configs/model_panel_v2.json").read_text())["backbone"][3];spec=ModelSpec(m["id"],m["provider"],m["max_token_field"],m["temperature"],0.0001);gate=CostGate(a.max_cost);client=Client(gate=gate,retries=4);out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);n=0
    with out.open("w",encoding="utf-8") as f:
        for cell in cells(a.domain):
            t=cell["task"];rec=run(client,spec,Environment(t,cell["condition"]),cell["replicate"]);rec["score"]=score(t,rec);rec["exact_recovery"]=True;f.write(json.dumps(rec,sort_keys=True)+"\n");f.flush();n+=1
    print({"status":"PASS","cells":n,"cost_usd":gate.spent_usd})
if __name__=="__main__":main()
