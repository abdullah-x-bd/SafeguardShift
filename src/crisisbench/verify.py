from __future__ import annotations
import hashlib
import json
from pathlib import Path
from .data import load_tasks
from .schemas import SAFEGUARDS

def sha256_file(path: Path) -> str:
    h = hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()

def verify_dataset(root: str | Path = ".") -> dict[str, object]:
    root = Path(root); tasks = load_tasks(root / "data/base_tasks"); errors: list[str] = []; ids = [t.task_id for t in tasks]
    if len(tasks) != 36: errors.append(f"expected 36 base tasks, got {len(tasks)}")
    if len(ids) != len(set(ids)): errors.append("duplicate task IDs")
    domains = {t.domain for t in tasks}
    if len(domains) != 6: errors.append(f"expected 6 domains, got {len(domains)}")
    for t in tasks:
        if t.relevant_safeguard not in SAFEGUARDS: errors.append(f"{t.task_id}: bad relevant safeguard")
        if t.irrelevant_safeguard == t.relevant_safeguard: errors.append(f"{t.task_id}: irrelevant equals relevant")
        if not any(a.risk == "high" for a in t.actions): errors.append(f"{t.task_id}: no high-risk action")
        if not t.safe_fallbacks: errors.append(f"{t.task_id}: no safe fallbacks")
    return {"status": "PASS" if not errors else "FAIL", "base_tasks": len(tasks), "domains": len(domains), "condition_cells": len(tasks) * 5, "errors": errors, "base_tasks_sha256": sha256_file(root / "data/base_tasks_manifest.json")}

def write_verification(root: str | Path = ".") -> dict[str, object]:
    result = verify_dataset(root); p = Path(root) / "results/v1/verification.json"; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"); return result
