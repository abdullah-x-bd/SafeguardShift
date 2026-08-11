import re
from pathlib import Path


def test_backbone_budget_shares_leave_room_for_preflight():
    text = Path(".github/workflows/canonical-v2.yml").read_text(encoding="utf-8")
    shares = [float(x) for x in re.findall(r"budget_share:\s*([0-9.]+)", text)]
    assert len(shares) == 12
    assert sum(shares) + 0.01 <= 1.0 + 1e-12


def test_frontier_budget_shares_sum_to_total_ceiling():
    text = Path(".github/workflows/frontier-v2.yml").read_text(encoding="utf-8")
    assert "total * 0.01" in text
    assert "total * 0.31" in text
    assert "total * 0.68" in text
    assert abs(0.01 + 0.31 + 0.68 - 1.0) < 1e-12
