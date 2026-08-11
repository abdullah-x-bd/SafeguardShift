from safeguardshift.verify import verify
from safeguardshift.oracle import run_oracle
from safeguardshift.data import load_tasks
v=verify(); assert v["status"]=="PASS",v
subs=[run_oracle(t,"substitute") for t in load_tasks()]
assert all(r["score"]["substitute_used"] and r["score"]["substitution_target_executed"] for r in subs)
print({"status":"PASS","dataset":v,"oracle_substitute_success":len(subs),"expert_validation":"SEPARATE_EXTERNAL_GATE"})
