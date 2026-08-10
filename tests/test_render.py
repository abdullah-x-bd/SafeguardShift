from crisisbench.data import load_tasks
from crisisbench.render import capacity_state, render_scenario

def test_only_relevant_safeguard_changes():
    t=load_tasks("data/base_tasks")[0]; full,_=capacity_state(t,"full"); rel,_=capacity_state(t,"relevant_ablation")
    diff=[k for k in full if full[k]!=rel[k]]; assert diff==[t.relevant_safeguard]

def test_irrelevant_is_distinct():
    t=load_tasks("data/base_tasks")[0]; assert t.relevant_safeguard!=t.irrelevant_safeguard
    text=render_scenario(t,"irrelevant_ablation"); assert "Institutional safeguards" in text
