import re
from pathlib import Path


def test_backbone_budget_shares_leave_room_for_preflight():
    text = Path(".github/workflows/canonical-v2.yml").read_text(encoding="utf-8")
    match = re.search(r"shares=\{0:([0-9.]+),1:([0-9.]+),2:([0-9.]+),3:([0-9.]+)\}", text)
    assert match is not None
    per_replicate_model_shares = [float(x) for x in match.groups()]
    assert "/6.0" in text
    assert "replicate: [1, 2, 3]" in text
    assert "domain: [public_health, critical_infrastructure, cyber_incident, disaster_response, public_governance, crisis_communication]" in text
    assert 3 * sum(per_replicate_model_shares) + 0.01 <= 1.0 + 1e-12


def test_frontier_budget_shares_sum_to_total_ceiling():
    text = Path(".github/workflows/frontier-v2.yml").read_text(encoding="utf-8")
    assert "total * 0.01" in text
    assert "total * 0.31" in text
    assert "total * 0.68" in text
    assert abs(0.01 + 0.31 + 0.68 - 1.0) < 1e-12
