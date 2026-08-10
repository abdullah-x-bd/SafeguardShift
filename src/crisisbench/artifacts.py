from __future__ import annotations
import hashlib
import json
from pathlib import Path

def build_manifest(root: str | Path = ".") -> dict[str, str]:
    root = Path(root); targets = [root / "configs/protocol_v1.yaml", root / "configs/model_panel_v1.yaml", root / "data/base_tasks_manifest.json", root / "data/capacity_conditions.json", root / "docs/HYPOTHESES_V1.md", root / "docs/SCORING.md"]; out: dict[str, str] = {}
    for p in targets:
        if p.exists(): out[str(p.relative_to(root))] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out

def write_freeze(root: str | Path = ".") -> dict[str, object]:
    root = Path(root); payload: dict[str, object] = {"protocol": "crisisbench-v1.0.0", "frozen_on": "2026-08-11", "files": build_manifest(root)}
    (root / "FREEZE_MANIFEST.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"); return payload
