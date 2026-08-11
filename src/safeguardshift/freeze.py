from __future__ import annotations
import hashlib
from pathlib import Path

FREEZE_FILES = [
    "v2/configs/protocol_v2.json",
    "v2/configs/model_panel_v2.json",
    "v2/configs/analysis_v2.json",
    "v2/configs/frontier_subset_v2.json",
    "v2/configs/validation_panel_v2.json",
    "v2/data/base_tasks_manifest.json",
    "v2/docs/HYPOTHESES.md",
    "v2/docs/SCORING.md",
    "v2/docs/CONSTRUCT_VALIDATION.md",
    "v2/docs/AMENDMENTS.md",
    "src/safeguardshift/data.py",
    "src/safeguardshift/schema.py",
    "src/safeguardshift/render.py",
    "src/safeguardshift/environment.py",
    "src/safeguardshift/tools.py",
    "src/safeguardshift/agent.py",
    "src/safeguardshift/scoring.py",
    "src/safeguardshift/analysis.py",
    "src/safeguardshift/openrouter.py",
    "scripts_v2/run_canonical.py",
    "scripts_v2/run_frontier_diagnostic.py",
    "scripts_v2/run_construct_validation.py",
    "scripts_v2/analyse_canonical.py",
]


def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def build(root: Path = Path(".")) -> dict:
    return {
        "protocol": "safeguardshift-v2.0.0",
        "frozen_on": "2026-08-11",
        "v1_parent_commit": "f4bfb19eadf68b15a3bd380992d70496df6ac258",
        "files": {f: digest(root / f) for f in FREEZE_FILES},
    }
