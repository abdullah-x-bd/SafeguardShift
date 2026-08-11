from __future__ import annotations
import argparse,json
from pathlib import Path
from safeguardshift.agent import run
from safeguardshift.data import load_tasks
from safeguardshift.environment import Environment
from safeguardshift.ledger import CostGate
from safeguardshift.openrouter import Client,ModelSpec
from safeguardshift.scoring import score

CONDITION_ORDER=("full","relevant_ablation","irrelevant_ablation","substitute","compound_ablation")
CONDITIONS=set(CONDITION_ORDER)
RESERVES={0:0.0005,1:0.0002,2:0.0002,3:0.0001}
GEMINI_ACCEPTED_PER_DOMAIN={"public_health":20,"critical_infrastructure":36,"cyber_incident":45,"disaster_response":16,"public_governance":24,"crisis_communication":19}
DEEPSEEK_FINALIZED_PREFIXES={
 "public_health":{1:23,2:19},
 "critical_infrastructure":{1:24,2:19,3:0},
 "cyber_incident":{1:21,2:0,3:0},
 "disaster_response":{1:24,2:0,3:0},
 "public_governance":{1:21,2:0,3:0},
 "crisis_communication":{1:21,2:0},
}

def ordered_rep_cells(model_index:int,domain:str,rep:int)->list[dict]:
    ordered=[t for t in load_tasks() if t.domain==domain]
    return [{"model_index":model_index,"task_id":t.task_id,"replicate":rep,"condition":condition} for t in ordered for condition in CONDITION_ORDER]

def gemini_suffix(domain:str)->list[dict]:
    n=GEMINI_ACCEPTED_PER_DOMAIN[domain];out=[]
    for rep in (1,2,3):out.extend(ordered_rep_cells(1,domain,rep)[n:])
    return out

def deepseek_finalized_suffix(domain:str)->list[dict]:
    out=[]
    for rep,n in sorted(DEEPSEEK_FINALIZED_PREFIXES[domain].items()):out.extend(ordered_rep_cells(2,domain,rep)[n:])
    return out

def main()->None:
    ap=argparse.ArgumentParser();ap.add_argument("--cells");ap.add_argument("--gemini-domain",choices=sorted(GEMINI_ACCEPTED_PER_DOMAIN));ap.add_argument("--deepseek-finalized-domain",choices=sorted(DEEPSEEK_FINALIZED_PREFIXES));ap.add_argument("--max-cost",type=float,required=True);ap.add_argument("--output",required=True);a=ap.parse_args()
    panel=json.loads(Path("v2/configs/model_panel_v2.json").read_text(encoding="utf-8"))["backbone"];tasks={t.task_id:t for t in load_tasks()}
    modes=sum(bool(x) for x in (a.cells,a.gemini_domain,a.deepseek_finalized_domain))
    if modes!=1:raise SystemExit("provide exactly one recovery selector")
    if a.cells:cells=json.loads(Path(a.cells).read_text(encoding="utf-8"))
    elif a.gemini_domain:cells=gemini_suffix(a.gemini_domain)
    else:cells=deepseek_finalized_suffix(a.deepseek_finalized_domain)
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
