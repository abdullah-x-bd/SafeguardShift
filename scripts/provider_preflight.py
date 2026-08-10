from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
from crisisbench.ledger import CostGate
from crisisbench.openrouter import ModelSpec, OpenRouterClient
from crisisbench.tools import tool_schema

MODELS = [
    ModelSpec("openai/gpt-4.1-mini", "openai"),
    ModelSpec("google/gemini-2.5-flash-lite", "google-vertex"),
    ModelSpec("deepseek/deepseek-v3.2", "deepinfra"),
    ModelSpec("mistralai/mistral-small-3.2-24b-instruct", "mistral"),
    ModelSpec("openai/gpt-5", "openai"),
    ModelSpec("anthropic/claude-sonnet-5", "anthropic"),
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-cost", type=float, default=0.05)
    ap.add_argument("--output", default="results/provider_preflight.json")
    args = ap.parse_args()
    if not os.getenv("OPENROUTER_API_KEY"):
        raise SystemExit("OPENROUTER_API_KEY is required")
    gate = CostGate(args.max_cost)
    client = OpenRouterClient(cost_gate=gate, conservative_request_usd=0.01)
    inspect_tool = [t for t in tool_schema() if t["function"]["name"] == "inspect_state"]
    forced = {"type": "function", "function": {"name": "inspect_state"}}
    messages = [
        {"role": "system", "content": "Provider compatibility preflight. Call inspect_state exactly once."},
        {"role": "user", "content": "Call inspect_state."},
    ]
    results = []
    for spec in MODELS:
        before = gate.spent_usd
        row = {"model": spec.id, "requested_provider": spec.provider}
        try:
            response = client.chat(spec, messages, inspect_tool, max_tokens=80, tool_choice=forced)
            calls = (response.get("choices") or [{}])[0].get("message", {}).get("tool_calls") or []
            ok = bool(calls and calls[0].get("function", {}).get("name") == "inspect_state")
            row.update({
                "status": "PASS" if ok else "NO_EXPECTED_TOOL_CALL",
                "routed_model": response.get("model"),
                "routed_provider": response.get("provider"),
                "response_id": response.get("id"),
                "cost_usd": gate.spent_usd - before,
            })
        except Exception as exc:
            row.update({"status": "FAIL", "error": str(exc), "cost_usd": gate.spent_usd - before})
        results.append(row)
        print(json.dumps(row, sort_keys=True))
    payload = {
        "status": "PASS" if all(r["status"] == "PASS" for r in results) else "FAIL",
        "total_cost_usd": gate.spent_usd,
        "models": results,
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    if payload["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
