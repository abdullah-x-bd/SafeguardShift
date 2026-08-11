from safeguardshift.agent import SYSTEM
from safeguardshift.data import load_tasks
from safeguardshift.verify import verify


def test_balanced_design():
    v=verify(); assert v["status"]=="PASS"; assert v["tasks"]==72; assert set(v["domains"].values())=={12}; assert set(v["relevant_safeguards"].values())=={12}


def test_substitution_target_requires_only_relevant():
    for t in load_tasks():
        a=next(x for x in t.actions if x.id==t.substitution_target_action)
        assert a.requires==(t.relevant_safeguard,)


def test_irrelevant_safeguard_is_causally_irrelevant_to_all_actions():
    for t in load_tasks():
        assert all(t.irrelevant_safeguard not in a.requires for a in t.actions)


def test_only_target_and_high_impact_depend_on_manipulated_safeguards():
    for t in load_tasks():
        for a in t.actions:
            if a.action_class=="safeguard_dependent": assert a.requires==(t.relevant_safeguard,)
            elif a.action_class=="high_impact": assert set(a.requires)=={t.relevant_safeguard,t.secondary_safeguard}
            else: assert a.requires==()


def test_visible_action_labels_do_not_leak_experimental_roles():
    banned=("safeguard-dependent","relevant safeguard","irrelevant safeguard","negative control")
    for t in load_tasks():
        for a in t.actions:
            assert not any(term in a.label.lower() for term in banned)
        target=next(a for a in t.actions if a.action_class=="safeguard_dependent")
        assert target.label.startswith("Implement the prepared task response for:")


def test_system_prompt_does_not_reveal_experimental_roles_or_reconstruction_policy():
    text=SYSTEM.lower()
    for phrase in ("relevant safeguard","irrelevant safeguard","negative control","safeguard-dependent","restore it","missing capability"):
        assert phrase not in text
