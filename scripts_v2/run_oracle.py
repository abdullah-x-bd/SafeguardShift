from safeguardshift.data import load_tasks
from safeguardshift.oracle import run_oracle
def main():
    tasks=load_tasks(); rows=[run_oracle(t,c) for t in tasks for c in ("full","relevant_ablation","irrelevant_ablation","substitute","compound_ablation")]
    subs=[r for r in rows if r["condition"]=="substitute"]
    assert all(r["score"]["substitute_used"] and r["score"]["substitution_target_executed"] for r in subs)
    print({"status":"PASS","trajectories":len(rows),"substitute_oracle_success":len(subs)})
if __name__=="__main__":main()
