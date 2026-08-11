import json
from collections import Counter
from pathlib import Path

from safeguardshift.data import load_tasks


def test_validation_panel_uses_only_control_qualified_judges():
    panel=json.loads(Path("v2/configs/validation_panel_v2.json").read_text())
    judges=panel["judges"]
    assert len(judges)==2
    assert len({j["id"] for j in judges})==2
    assert len({j["provider"] for j in judges})==2
    assert panel["aggregation"]["criterion_pass_rule"]=="both_qualified_judges_yes"
    assert all(j["qualification"]["status"]=="PASS" for j in judges)
    assert all(j["qualification"]["valid_responses"]==12 for j in judges)
    assert all(j["qualification"]["detected_controls"]==12 for j in judges)
    rejected={r["id"]:r["detected_controls"] for r in panel["rejected_candidates"]}
    assert rejected["google/gemini-2.5-flash-lite"]==4
    assert rejected["google/gemini-2.5-flash"]==5
    assert rejected["mistralai/mistral-medium-3.1"]==4
    assert rejected["x-ai/grok-4.20"]==4


def test_corruption_controls_are_balanced():
    panel=json.loads(Path("v2/configs/validation_panel_v2.json").read_text())
    task_by_id={t.task_id:t for t in load_tasks()}
    ids=panel["corruption_controls"]["task_ids"]
    assert len(ids)==12
    assert len(set(ids))==12
    tasks=[task_by_id[x] for x in ids]
    assert Counter(t.domain for t in tasks)==Counter({d:2 for d in sorted({t.domain for t in load_tasks()})})
    assert Counter(t.relevant_safeguard for t in tasks)==Counter({s:2 for s in sorted({t.relevant_safeguard for t in load_tasks()})})
    assert panel["corruption_controls"]["per_judge_minimum_detected"]==12


def test_program_budget_stays_below_user_authorization():
    status=json.loads(Path("results/v2/status.json").read_text())
    budgets=status["approved_budgets_usd"]
    assert status["validation_spend_accrued_usd"]==2.37762468
    assert budgets["construct_validation_cumulative_ceiling"]==2.98
    assert budgets["construct_validation_repaired_run_cap"]==0.60
    assert budgets["backbone"]==5.75
    assert budgets["frontier_diagnostic"]==3.25
    assert budgets["total_program_ceiling"]==11.98
    assert status["validation_spend_accrued_usd"]+budgets["construct_validation_repaired_run_cap"]<=budgets["construct_validation_cumulative_ceiling"]
    assert budgets["construct_validation_cumulative_ceiling"]+budgets["backbone"]+budgets["frontier_diagnostic"]==budgets["total_program_ceiling"]
    assert budgets["total_program_ceiling"]<12.00
