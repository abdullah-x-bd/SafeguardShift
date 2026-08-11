import json
from collections import Counter
from pathlib import Path
from safeguardshift.data import load_tasks


def test_frontier_subset_is_balanced_and_complete():
    subset = json.loads(Path("v2/configs/frontier_subset_v2.json").read_text(encoding="utf-8"))
    task_map = {t.task_id: t for t in load_tasks()}
    ids = subset["task_ids"]
    assert len(ids) == 12
    assert len(set(ids)) == 12
    assert all(task_id in task_map for task_id in ids)
    tasks = [task_map[task_id] for task_id in ids]
    assert set(Counter(t.domain for t in tasks).values()) == {2}
    assert set(Counter(t.relevant_safeguard for t in tasks).values()) == {2}
    assert subset["expected_trajectories"] == 120
