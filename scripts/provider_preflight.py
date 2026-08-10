from __future__ import annotations
import os
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
    if not os.getenv("OPENROUTER_API_KEY"):
        raise SystemExit("OPENROUTER_API_KEY is required")
    client = OpenRouterClient(conservative_request_usd=0.02)
    messages = [
        {"role": "system", "content": "This is a provider-compatibility preflight. Call inspect_state once."},
        {"role": "user", "content": "Call the inspection tool."},
    ]
    for spec in MODELS:
        response = client.chat(spec, messages, tool_schema(), max_tokens=100)
        calls = (response.get("choices") or [{}])[0].get("message", {}).get("tool_calls") or []
        print(spec.id, spec.provider, "PASS" if calls else "NO_TOOL_CALL", response.get("model"), response.get("provider"))


if __name__ == "__main__":
    main()
