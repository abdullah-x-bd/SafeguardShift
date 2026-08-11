import json
from collections import Counter
from pathlib import Path

from safeguardshift.data import load_tasks


def test_validation_panel_is_three_independent_routes():
    panel=json.loads(Path("v2/configs/validation_panel_v2.json").read_text())
    judges=panel["judges"]
    assert len(judges)==3
    assert len({j["id"] for j in judges})==3
    assert len({j["provider"] for j in judges})==3
    assert panel["aggregation"]["criterion_pass_rule"]=="at_least_2_of_3_yes"


def test_corruption_controls_are_balanced():
    panel=json.loads(Path("v2/configs/validation_panel_v2.json").read_text())
    task_by_id={t.task_id:t for t in load_tasks()}
    ids=panel["corruption_controls"]["task_ids"]
    assert len(ids)==12
    assert len(set(ids))==12
    tasks=[task_by_id[x] for x in ids]
    assert Counter(t.domain for t in tasks)==Counter({d:2 for d in sorted({t.domain for t in load_tasks()})})
    assert Counter(t.relevant_safeguard for t in tasks)==Counter({s:2 for s in sorted({t.relevant_safeguard for t in load_tasks()})})


def test_construct_validation_budget_is_below_total_plan():
    status=json.loads(Path("results/v2/status.json").read_text())
    budgets=status["approved_budgets_usd"]
    assert budgets["construct_validation_cumulative_ceiling"]==1.70
    assert budgets["construct_validation_rerun_cap"]==0.80
    assert budgets["backbone"]==6.50
    assert budgets["frontier_diagnostic"]==3.50
    assert budgets["total_program_ceiling"]==11.70
    assert budgets["construct_validation_cumulative_ceiling"]+budgets["backbone"]+budgets["frontier_diagnostic"]==budgets["total_program_ceiling"]
    assert budgets["total_program_ceiling"]<12.00
