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


def test_completed_program_status_is_self_consistent():
    status=json.loads(Path("results/v2/status.json").read_text())
    assert status["canonical_collection"]=="COMPLETE_PRIMARY3"
    assert status["analysis"]=="PASS"
    primary=status["primary_behavioral_estimand"]
    assert primary["status"]=="PASS"
    assert primary["cells"]==3240
    assert primary["tasks"]==72
    assert primary["conditions"]==5
    assert primary["replicates"]==3
    assert primary["missing_cells"]==0
    assert primary["duplicates"]==0
    assert len(primary["models"])==3
    assert status["frontier_diagnostic"]["status"]=="PASS"
    assert status["frontier_diagnostic"]["cells"]==60
    assert status["deepseek_provider_diagnostic"]["pooled_into_primary"] is False
    assert status["raw_evidence"]["status"]=="CHECKSUM_PINNED_ACTIONS_ARTIFACT_PENDING_DURABLE_MIRROR"
