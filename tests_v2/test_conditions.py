from safeguardshift.data import load_tasks
from safeguardshift.environment import Environment,capacity_state
from safeguardshift.schema import SAFEGUARDS
def test_every_condition_renders_capacity_change():
    for t in load_tasks():
        full,_=capacity_state(t,"full"); rel,_=capacity_state(t,"relevant_ablation"); irr,_=capacity_state(t,"irrelevant_ablation"); sub,has=capacity_state(t,"substitute"); comp,_=capacity_state(t,"compound_ablation")
        assert all(full[s]=="available" for s in SAFEGUARDS); assert rel[t.relevant_safeguard]=="unavailable"; assert irr[t.irrelevant_safeguard]=="unavailable"; assert has and sub[t.relevant_safeguard]=="unavailable"; assert comp[t.relevant_safeguard]=="unavailable" and comp[t.secondary_safeguard]=="unavailable"
def test_compound_blocks_high_impact_all_tasks():
    for t in load_tasks():
        e=Environment(t,"compound_ablation"); hi=next(a for a in t.actions if a.action_class=="high_impact"); r=e.execute(hi.id); assert not r["allowed"]; assert t.relevant_safeguard in r["missing"]; assert t.secondary_safeguard in r["missing"]
def test_substitution_restores_only_primary():
    for t in load_tasks():
        e=Environment(t,"substitute"); e.tool("request_substitute",{}); target=e.execute(t.substitution_target_action); assert target["allowed"] and target["substitute_used"]
