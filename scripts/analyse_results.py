from __future__ import annotations
import argparse
import json
from pathlib import Path
from crisisbench.analysis import analyse, load_jsonl


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="results/private/canonical.jsonl")
    ap.add_argument("--output", default="results/v1/summary.json")
    args = ap.parse_args()
    summary = analyse(load_jsonl(args.input))
    Path(args.output).write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
