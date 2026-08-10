from __future__ import annotations
import json
from collections import defaultdict
from pathlib import Path
from typing import Any
from .scoring import action_signature, jaccard_distance

def load_jsonl(path: str|Path) -> list[dict[str,Any]]:
    if not Path(path).exists(): return []
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]

def analyse(records: list[dict[str,Any]]) -> dict[str,Any]:
    if not records: return {"status":"NO_CANONICAL_DATA","trajectories":0}
    groups=defaultdict(dict)
    for r in records: groups[(r["task_id"],r["model"])][r["condition"]]=r
    selective=[]
    for cells in groups.values():
        if all(k in cells for k in ("full","relevant_ablation","irrelevant_ablation")):
            full=action_signature(cells["full"]); rel=action_signature(cells["relevant_ablation"]); irr=action_signature(cells["irrelevant_ablation"])
            selective.append(jaccard_distance(full,rel)-jaccard_distance(full,irr))
    return {"status":"PASS","trajectories":len(records),"matched_task_model_groups":len(groups),"mean_selective_adaptation":sum(selective)/len(selective) if selective else None,"selective_adaptation_n":len(selective)}
