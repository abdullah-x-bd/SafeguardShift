from crisisbench.data import load_tasks
from crisisbench.environment import CrisisEnvironment

def test_high_impact_blocked_after_relevant_ablation():
    t=load_tasks("data/base_tasks")[0]; e=CrisisEnvironment(t,"relevant_ablation"); r=e.action("take_high_impact_action"); assert r["allowed"] is False; assert t.relevant_safeguard in r["missing"]

def test_substitute_restores_relevant_requirement():
    t=load_tasks("data/base_tasks")[0]; e=CrisisEnvironment(t,"substitute"); assert e.action("take_high_impact_action")["allowed"] is False; assert e.request_substitute()["status"]=="activated"; assert e.action("take_high_impact_action")["allowed"] is True

def test_irrelevant_ablation_does_not_block_high_impact_on_irrelevant_alone():
    t=load_tasks("data/base_tasks")[0]; e=CrisisEnvironment(t,"irrelevant_ablation"); r=e.action("take_high_impact_action"); assert t.irrelevant_safeguard not in r["missing"]
