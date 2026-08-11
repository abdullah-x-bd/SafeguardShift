import json
from collections import Counter
from pathlib import Path

from safeguardshift.data import load_tasks


def test_validation_panel_keeps_two_judge_task_unanimity():
    panel=json.loads(Path("v2/configs/validation_panel_v2.json").read_text())
    judges=panel["judges"]
    assert len(judges)==2
    assert len({j["id"] for j in judges})==2
    assert len({j["provider"] for j in judges})==2
    assert panel["aggregation"]["criterion_pass_rule"]=="both_task_judges_yes"
    assert panel["aggregation"]["corruption_sentinel"]=="openai/gpt-5.4"
    assert all(j["final_repaired_run"]["real_tasks_approved"]==72 for j in judges)
    assert next(j for j in judges if j["id"]=="openai/gpt-5.4")["final_repaired_run"]["controls_detected"]==12
    assert next(j for j in judges if j["id"]=="anthropic/claude-sonnet-5")["final_repaired_run"]["controls_detected"]==7
    rejected={r["id"]:r["detected_controls"] for r in panel["rejected_candidates"]}
    assert rejected["google/gemini-2.5-flash-lite"]==4
    assert rejected["google/gemini-2.5-flash"]==5
    assert rejected["mistralai/mistral-medium-3.1"]==4
    assert rejected["x-ai/grok-4.20"]==4


def test_corruption_controls_are_balanced_and_have_one_formal_sentinel():
    panel=json.loads(Path("v2/configs/validation_panel_v2.json").read_text())
    task_by_id={t.task_id:t for t in load_tasks()}
    controls=panel["corruption_controls"]
    ids=controls["task_ids"]
    assert len(ids)==12
    assert len(set(ids))==12
    tasks=[task_by_id[x] for x in ids]
    assert Counter(t.domain for t in tasks)==Counter({d:2 for d in sorted({t.domain for t in load_tasks()})})
    assert Counter(t.relevant_safeguard for t in tasks)==Counter({s:2 for s in sorted({t.relevant_safeguard for t in load_tasks()})})
    assert controls["sentinel_judge"]=="openai/gpt-5.4"
    assert controls["sentinel_required_detected"]==12
    assert controls["final_repaired_run_detected_by_judge"]=={"openai/gpt-5.4":12,"anthropic/claude-sonnet-5":7}


def test_program_budget_stays_below_user_authorization():
    status=json.loads(Path("results/v2/status.json").read_text())
    budgets=status["approved_budgets_usd"]
    assert status["validation_spend_accrued_usd"]==3.69308468
    assert budgets["construct_validation_cumulative_ceiling"]==3.69308468
    assert budgets["backbone"]==5.90
    assert budgets["frontier_diagnostic"]==2.10
    assert budgets["total_program_ceiling"]==11.69308468
    assert budgets["construct_validation_cumulative_ceiling"]+budgets["backbone"]+budgets["frontier_diagnostic"]==budgets["total_program_ceiling"]
    assert budgets["total_program_ceiling"]<12.00
