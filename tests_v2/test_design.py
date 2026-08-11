from safeguardshift.data import load_tasks
from safeguardshift.verify import verify
def test_balanced_design():
    v=verify(); assert v["status"]=="PASS"; assert v["tasks"]==72; assert set(v["domains"].values())=={12}; assert set(v["relevant_safeguards"].values())=={12}
def test_substitution_target_requires_relevant():
    for t in load_tasks():
        a=next(x for x in t.actions if x.id==t.substitution_target_action); assert t.relevant_safeguard in a.requires
