from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

@dataclass
class CostGate:
    maximum_usd: float
    spent_usd: float = 0.0
    def allow(self, projected_request_usd: float) -> None:
        projected = self.spent_usd + projected_request_usd
        if projected > self.maximum_usd:
            raise RuntimeError(f"cost gate: projected ${projected:.4f} exceeds ${self.maximum_usd:.4f}")
    def add(self, cost: float) -> None:
        self.spent_usd += max(0.0, float(cost))

def request_hash(payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(canonical).hexdigest()

def append_jsonl(path: str | Path, row: dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
