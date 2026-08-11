from __future__ import annotations
import hashlib
from pathlib import Path
FREEZE_FILES=["v2/configs/protocol_v2.json","v2/configs/model_panel_v2.json","v2/configs/analysis_v2.json","v2/data/base_tasks_manifest.json","v2/docs/HYPOTHESES.md","v2/docs/SCORING.md"]
def digest(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def build(root:Path=Path("."))->dict:
    return {"protocol":"safeguardshift-v2.0.0","frozen_on":"2026-08-11","v1_parent_commit":"f4bfb19eadf68b15a3bd380992d70496df6ac258","files":{f:digest(root/f) for f in FREEZE_FILES}}
