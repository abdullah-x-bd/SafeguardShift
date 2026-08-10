from crisisbench.data import load_tasks
from crisisbench.environment import CrisisEnvironment
from crisisbench.scoring import score_trajectory, jaccard_distance

def test_phantom_and_recovery():
    t=load_tasks("data/base_tasks")[0]; e=CrisisEnvironment(t,"relevant_ablation"); e.action("take_high_impact_action"); e.action("inspect_evidence"); rec={"attempted":e.attempted,"terminal_plan":{"recommended_actions":[]},"substitute_activated":False}; s=score_trajectory(t,"relevant_ablation",rec); assert s["phantom_capacity_count"]>=1; assert s["safe_recovery"] is True

def test_jaccard(): assert jaccard_distance({"a"},{"a"})==0 and jaccard_distance({"a"},{"b"})==1

def test_repeated_action_does_not_inflate_utility():
    t=load_tasks("data/base_tasks")[0]
    once=CrisisEnvironment(t,"full"); once.action("inspect_evidence")
    twice=CrisisEnvironment(t,"full"); twice.action("inspect_evidence"); twice.action("inspect_evidence")
    a=score_trajectory(t,"full",{"attempted":once.attempted,"terminal_plan":{},"substitute_activated":False})
    b=score_trajectory(t,"full",{"attempted":twice.attempted,"terminal_plan":{},"substitute_activated":False})
    assert a["utility_preservation"] == b["utility_preservation"]

def test_substitute_must_be_used():
    t=load_tasks("data/base_tasks")[0]; e=CrisisEnvironment(t,"substitute"); e.request_substitute()
    s=score_trajectory(t,"substitute",{"attempted":e.attempted,"terminal_plan":{},"substitute_activated":True})
    assert s["substitute_activated"] is True
    assert s["substitute_used"] is False
