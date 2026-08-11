from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from safeguardshift.data import load_tasks

CONDITIONS = ("full", "relevant_ablation", "irrelevant_ablation", "substitute", "compound_ablation")
PRIMARY_INDICES = (0, 1, 3)


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
    ap.add_argument("--source", action="append", required=True, help="NAME=DIR in fixed acceptance-priority order")
    ap.add_argument("--output", required=True)
    ap.add_argument("--missing-output", required=True)
    ap.add_argument("--report-output", required=True)
    args = ap.parse_args()

    panel = json.loads(Path("v2/configs/model_panel_v2.json").read_text(encoding="utf-8"))["backbone"]
    model_ids = [panel[i]["id"] for i in PRIMARY_INDICES]
    original_index = {panel[i]["id"]: i for i in PRIMARY_INDICES}
    model_order = {m: j for j, m in enumerate(model_ids)}
    tasks = load_tasks()
    task_ids = [t.task_id for t in tasks]
    task_order = {t: i for i, t in enumerate(task_ids)}
    expected = {
        (model, task_id, rep, condition)
        for model in model_ids
        for task_id in task_ids
        for rep in (1, 2, 3)
        for condition in CONDITIONS
    }

    accepted = {}
    provenance = {}
    duplicates = []
    source_counts = Counter()

    for spec in args.source:
        name, directory = spec.split("=", 1)
        root = Path(directory)
        for path, lineno, row in read_rows(root) or []:
            try:
                key = (str(row["model"]), str(row["task_id"]), int(row["replicate"]), str(row["condition"]))
            except (KeyError, TypeError, ValueError):
                continue
            if key not in expected:
                continue
            if key in accepted:
                duplicates.append({"key": list(key), "kept": provenance[key], "excluded": {"source": name, "file": str(path), "line": lineno}})
                continue
            accepted[key] = row
            provenance[key] = {"source": name, "file": str(path), "line": lineno}
            source_counts[name] += 1

    missing = sorted(expected - set(accepted), key=lambda k: (model_order[k[0]], task_order[k[1]], k[2], CONDITIONS.index(k[3])))
    ordered = sorted(accepted, key=lambda k: (model_order[k[0]], task_order[k[1]], k[2], CONDITIONS.index(k[3])))

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        for key in ordered:
            fh.write(json.dumps(accepted[key], sort_keys=True) + "\n")

    missing_rows = [
        {"model_index": original_index[m], "model": m, "task_id": t, "replicate": rep, "condition": c}
        for m, t, rep, c in missing
    ]
    mp = Path(args.missing_output)
    mp.parent.mkdir(parents=True, exist_ok=True)
    mp.write_text(json.dumps(missing_rows, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    by_model = Counter(r["model"] for r in missing_rows)
    report = {
        "status": "PASS" if not missing else "INCOMPLETE",
        "primary_models": model_ids,
        "expected_cells": 3240,
        "accepted_cells": len(accepted),
        "missing_cells": len(missing),
        "missing_by_model": dict(sorted(by_model.items())),
        "duplicates_excluded": len(duplicates),
        "source_accept_counts": dict(source_counts),
        "provenance_policy": "first valid expected cell wins in explicit source-priority order; later duplicates excluded outcome-blind",
        "amendment": "v2/amendments/005_primary_estimand_provider_attrition.md",
    }
    rp = Path(args.report_output)
    rp.parent.mkdir(parents=True, exist_ok=True)
    rp.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
