from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path

from safeguardshift.analysis import analyse, analyse_frontier, completeness

PRIMARY_MODELS = {
    "openai/gpt-4.1-mini",
    "google/gemini-2.5-flash-lite",
    "mistralai/mistral-small-3.2-24b-instruct",
}


def load(pattern: str) -> list[dict]:
    rows = []
    for name in sorted(glob.glob(pattern)):
        for line in Path(name).read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--backbone-glob", required=True)
    ap.add_argument("--frontier-glob", required=True)
    ap.add_argument("--backbone-output", required=True)
    ap.add_argument("--frontier-output", required=True)
    args = ap.parse_args()

    backbone = load(args.backbone_glob)
    models = {str(r.get("model")) for r in backbone}
    if models != PRIMARY_MODELS:
        raise SystemExit(f"wrong primary model set: {sorted(models)}")
    check = completeness(backbone, expected_models=3, expected_tasks=72, expected_replicates={1, 2, 3})
    if check["status"] != "PASS" or check["unique_cells"] != 3240:
        raise SystemExit(f"primary matrix incomplete: {check}")

    summary = analyse(backbone)
    summary["status"] = "PASS"
    summary["completeness"] = check
    summary["estimand"] = {
        "type": "post-collection complete-case three-model primary behavioral estimand",
        "models": sorted(PRIMARY_MODELS),
        "expected_cells": 3240,
        "amendment": "v2/amendments/005_primary_estimand_provider_attrition.md",
        "deepseek_pooled": False,
    }
    Path(args.backbone_output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.backbone_output).write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    frontier = load(args.frontier_glob)
    frontier_summary = analyse_frontier(frontier)
    if frontier_summary["status"] != "PASS":
        raise SystemExit(f"frontier diagnostic incomplete: {frontier_summary['completeness']}")
    Path(args.frontier_output).write_text(json.dumps(frontier_summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"primary": check, "frontier": frontier_summary["completeness"]}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
