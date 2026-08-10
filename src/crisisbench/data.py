from __future__ import annotations
import json
from pathlib import Path
from .schemas import Task

def load_tasks(path: str | Path) -> list[Task]:
    p=Path(path); files=sorted(p.glob("*.jsonl")) if p.is_dir() else [p]; rows=[]
    for file in files:
        with file.open(encoding="utf-8") as f:
            for line in f:
                if line.strip(): rows.append(Task.from_dict(json.loads(line)))
    return rows

def load_conditions(path: str | Path) -> dict[str, dict[str, object]]:
    return json.loads(Path(path).read_text(encoding="utf-8"))
