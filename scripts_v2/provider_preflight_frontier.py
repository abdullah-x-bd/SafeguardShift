from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
from safeguardshift.data import load_tasks
from safeguardshift.ledger import CostGate
from safeguardshift.openrouter import Client, ModelSpec
from safeguardshift.render import render
from safeguardshift.tools import tool_schema


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-cost", type=float, required=True)
    args = ap.parse_args()
    if not os.getenv("OPENROUTER_API_KEY"):
        raise SystemExit("OPENROUTER_API_KEY is required")

    panel = json.loads(Path("v2/configs/model_panel_v2.json").read_text(encoding="utf-8"))["frontier_diagnostic"]
    subset = json.loads(Path("v2/configs/frontier_subset_v2.json").read_text(encoding="utf-8"))
    task_map = {t.task_id: t for t in load_tasks()}
    task = task_map[subset["task_ids"][0]]
    gate = CostGate(args.max_cost)
    client = Client(gate=gate, retries=1)
    results = []
    for m in panel:
        spec = ModelSpec(m["id"], m["provider"], m["max_token_field"], m["temperature"], m["reserve_usd"])
        resp = client.chat(
            spec,
            [{"role": "user", "content": render(task, "full")}],
            tool_schema(task),
            tool_choice="auto",
            max_tokens=64,
        )
        results.append({
            "model": spec.id,
            "provider": spec.provider,
            "response_id": resp.get("id"),
            "pass": bool(resp.get("choices")),
        })
    status = "PASS" if all(r["pass"] for r in results) else "FAIL"
    print({"status": status, "results": results, "cost_usd": gate.spent_usd})
    if status != "PASS":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
