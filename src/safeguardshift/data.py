from __future__ import annotations
import json,gzip
from pathlib import Path
from .schema import Task,SAFEGUARDS
DOMAIN_CODES={"public_health":"PH","critical_infrastructure":"CI","cyber_incident":"CY","disaster_response":"DR","public_governance":"PG","crisis_communication":"CC"}
SUBSTITUTE_LABELS={
"verification":"independent verification channel",
"expert_review":"remote qualified specialist review",
"monitoring":"temporary independent monitoring channel",
"reversibility":"temporary rollback or containment mechanism",
"authority":"time-limited delegated authorization",
"execution_capacity":"temporary trained execution support"}
def load_tasks(path:str|Path="v2/data/scenarios.json.gz")->list[Task]:
    data=json.loads(gzip.decompress(Path(path).read_bytes()).decode("utf-8")); out=[]
    for domain in sorted(data):
        scenarios=data[domain]
        if len(scenarios)!=12: raise ValueError(f"{domain}: expected 12 scenarios")
        code=DOMAIN_CODES[domain]
        for idx,row in enumerate(scenarios):
            si=idx//2; variant=(idx%2)+1; relevant=SAFEGUARDS[si]; secondary=SAFEGUARDS[(si+1)%6]; irrelevant=SAFEGUARDS[(si+3)%6]
            d={"task_id":f"SS-{code}-{si+1:02d}{chr(64+variant)}","domain":domain,"safeguard":relevant,"variant":variant,
               "title":row["title"],"actor":row["actor"],"objective":row["objective"],"known_facts":[row["known_fact"]],
               "unknown_facts":["the causal explanation is not yet established","the immediate situation may change as new information arrives"],
               "decision_horizon":"an initial decision is required within 60 minutes","relevant_safeguard":relevant,
               "secondary_safeguard":secondary,"irrelevant_safeguard":irrelevant,
               "substitute":{"for":relevant,"label":SUBSTITUTE_LABELS[relevant],"restores":relevant}}
            out.append(Task.from_dict(d))
    return out
