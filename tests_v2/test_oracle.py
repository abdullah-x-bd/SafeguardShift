from safeguardshift.data import load_tasks
from safeguardshift.oracle import run_oracle
def test_oracle_substitute_all_tasks():
    for t in load_tasks():
        r=run_oracle(t,"substitute"); assert r["score"]["substitute_used"]; assert r["score"]["substitution_target_executed"]
def test_irrelevant_ablation_does_not_block_target():
    from safeguardshift.environment import Environment
    for t in load_tasks():
        e=Environment(t,"irrelevant_ablation"); r=e.execute(t.substitution_target_action); assert r["allowed"]
