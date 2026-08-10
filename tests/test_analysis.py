from crisisbench.analysis import analyse, BACKBONE_MODELS, FRONTIER_MODELS, FRONTIER_TASK_IDS, CONDITIONS
from crisisbench.data import load_tasks


def record(task_id: str, model: str, condition: str) -> dict:
    attempted = [{"action_id": "inspect_evidence", "allowed": True, "missing": [], "risk": "low", "reversibility": "high", "utility": 1.0}]
    return {
        "task_id": task_id,
        "model": model,
        "condition": condition,
        "attempted": attempted,
        "terminal_plan": {"recommended_actions": ["inspect_evidence"]},
        "score": {
            "phantom_capacity_count": 0,
            "irreversible_error_intent_count": 0,
            "safe_recovery": False,
            "task_completed": True,
            "substitute_activated": condition == "substitute",
            "substitute_used": condition == "substitute",
            "utility_preservation": 0.5,
        },
    }


def test_full_matrix_analysis_contract():
    tasks = load_tasks("data/base_tasks")
    rows = [record(t.task_id, model, condition) for model in BACKBONE_MODELS for t in tasks for condition in CONDITIONS]
    rows += [record(task_id, model, condition) for model in FRONTIER_MODELS for task_id in FRONTIER_TASK_IDS for condition in CONDITIONS]
    out = analyse(rows)
    assert out["status"] == "PASS"
    assert out["trajectories"] == 780
    assert out["expected_cells"] == 780
    assert out["primary"]["task_completion_rate"] == 1.0
    assert out["primary"]["feasible_substitution_rate"] == 1.0
