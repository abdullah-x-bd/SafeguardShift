from crisisbench.data import load_tasks
from crisisbench.environment import CrisisEnvironment
from crisisbench.scoring import score_trajectory, jaccard_distance

def test_phantom_and_recovery():
    t=load_tasks("data/base_tasks")[0]; e=CrisisEnvironment(t,"relevant_ablation"); e.action("take_high_impact_action"); e.action("inspect_evidence"); rec={"attempted":e.attempted,"terminal_plan":{"recommended_actions":[]},"substitute_activated":False}; s=score_trajectory(t,"relevant_ablation",rec); assert s["phantom_capacity_count"]>=1; assert s["safe_recovery"] is True

def test_jaccard(): assert jaccard_distance({"a"},{"a"})==0 and jaccard_distance({"a"},{"b"})==1
