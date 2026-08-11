from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from safeguardshift.data import load_tasks

CONDITIONS = ("full", "relevant_ablation", "irrelevant_ablation", "substitute", "compound_ablation")


def read_rows(root: Path):
    if not root.exists():
        return
    for path in sorted(root.rglob("*.jsonl")):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for lineno, line in enumerate(lines, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            yield path, lineno, row


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", action="append", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--report-output", required=True)
    args = ap.parse_args()

    panel = json.loads(Path("v2/configs/model_panel_v2.json").read_text(encoding="utf-8"))["backbone"]
    model = panel[2]["id"]
    tasks = load_tasks()
    task_ids = [t.task_id for t in tasks]
    task_domain = {t.task_id: t.domain for t in tasks}
    expected = {(model, t, rep, c) for t in task_ids for rep in (1, 2, 3) for c in CONDITIONS}

    accepted = {}
    provenance = {}
    source_counts = Counter()
    duplicate_count = 0
    for spec in args.source:
        name, directory = spec.split("=", 1)
        for path, lineno, row in read_rows(Path(directory)) or []:
            try:
                key = (str(row["model"]), str(row["task_id"]), int(row["replicate"]), str(row["condition"]))
            except (KeyError, TypeError, ValueError):
                continue
            if key not in expected:
                continue
            if key in accepted:
                duplicate_count += 1
                continue
            accepted[key] = row
            provenance[key] = {"source": name, "file": str(path), "line": lineno}
            source_counts[name] += 1

    task_order = {t: i for i, t in enumerate(task_ids)}
    ordered = sorted(accepted, key=lambda k: (task_order[k[1]], k[2], CONDITIONS.index(k[3])))
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        for key in ordered:
            fh.write(json.dumps(accepted[key], sort_keys=True) + "\n")

    by_domain = Counter(task_domain[key[1]] for key in accepted)
    by_replicate = Counter(key[2] for key in accepted)
    by_condition = Counter(key[3] for key in accepted)
    accepted_n = len(accepted)
    report = {
        "status": "INCOMPLETE_PROVIDER_DIAGNOSTIC" if accepted_n < 1080 else "COMPLETE",
        "model": model,
        "provider": panel[2]["provider"],
        "planned_cells": 1080,
        "accepted_cells": accepted_n,
        "missing_cells": 1080 - accepted_n,
        "coverage_rate": accepted_n / 1080,
        "accepted_by_domain": dict(sorted(by_domain.items())),
        "accepted_by_replicate": {str(k): v for k, v in sorted(by_replicate.items())},
        "accepted_by_condition": dict(sorted(by_condition.items())),
        "source_accept_counts": dict(source_counts),
        "duplicates_excluded": duplicate_count,
        "interpretation": "Provider/interface reliability diagnostic only. Behavioral endpoints are incomplete-case descriptive statistics and are not pooled into the primary estimand.",
        "known_transport_failures": [
            "HTTP-success payloads with no usable choices array",
            "HTTP-success response bodies truncated or malformed before JSON decoding"
        ],
        "amendment": "v2/amendments/005_primary_estimand_provider_attrition.md",
    }
    rp = Path(args.report_output)
    rp.parent.mkdir(parents=True, exist_ok=True)
    rp.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
