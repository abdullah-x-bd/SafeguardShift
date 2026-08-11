from safeguardshift.data import load_tasks
from safeguardshift.scoring import score


def test_high_impact_action_does_not_inflate_safe_utility():
    task=load_tasks()[0]
    high=next(a for a in task.actions if a.risk=="high")
    rec={
        "attempted":[{
            "action_id":high.id,
            "action_class":high.action_class,
            "allowed":True,
            "missing":[],
            "risk":high.risk,
            "reversibility":high.reversibility,
            "utility":high.utility,
            "substitute_used":False,
        }],
        "terminal_plan":{},
        "substitute_activated":False,
    }
    result=score(task,rec)
    assert result["safe_executed_utility"]==0
    assert result["total_executed_utility"]==high.utility
    assert result["utility_preservation"]==0


def test_safe_action_contributes_to_safe_utility():
    task=load_tasks()[0]
    safe=next(a for a in task.actions if a.risk=="moderate")
    rec={
        "attempted":[{
            "action_id":safe.id,
            "action_class":safe.action_class,
            "allowed":True,
            "missing":[],
            "risk":safe.risk,
            "reversibility":safe.reversibility,
            "utility":safe.utility,
            "substitute_used":False,
        }],
        "terminal_plan":{},
        "substitute_activated":False,
    }
    result=score(task,rec)
    assert result["safe_executed_utility"]==safe.utility
    assert result["utility_preservation"]>0
