from __future__ import annotations
import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any
from .ledger import CostGate, request_hash

BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

@dataclass(frozen=True)
class ModelSpec:
    id: str
    provider: str

class OpenRouterClient:
    def __init__(self, api_key: str | None = None, cost_gate: CostGate | None = None, conservative_request_usd: float = 0.01) -> None:
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENROUTER_API_KEY is not set")
        self.cost_gate = cost_gate
        self.conservative_request_usd = conservative_request_usd

    @staticmethod
    def response_cost(response: dict[str, Any]) -> float | None:
        usage = response.get("usage") or {}
        for key in ("cost", "total_cost"):
            value = usage.get(key)
            if isinstance(value, (int, float)):
                return float(value)
        value = response.get("cost")
        if isinstance(value, (int, float)):
            return float(value)
        return None

    def chat(self, spec: ModelSpec, messages: list[dict[str, Any]], tools: list[dict[str, Any]], temperature: float = 0.0, max_tokens: int = 500) -> dict[str, Any]:
        if self.cost_gate:
            self.cost_gate.allow(self.conservative_request_usd)
        body: dict[str, Any] = {
            "model": spec.id,
            "messages": messages,
            "tools": tools,
            "tool_choice": "auto",
            "parallel_tool_calls": False,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "provider": {
                "order": [spec.provider],
                "allow_fallbacks": False,
                "require_parameters": True,
                "data_collection": "deny",
            },
        }
        digest = request_hash(body)
        req = urllib.request.Request(
            BASE_URL,
            data=json.dumps(body).encode(),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/abdullah-x-bd/crisisbench",
                "X-Title": "CrisisBench",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                response: dict[str, Any] = json.loads(r.read())
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")
            raise RuntimeError(f"OpenRouter HTTP {e.code}: {detail}") from e
        if self.cost_gate:
            cost = self.response_cost(response)
            self.cost_gate.add(cost if cost is not None else self.conservative_request_usd)
        response["_crisisbench_request"] = {
            "sha256": digest,
            "requested_model": spec.id,
            "requested_provider": spec.provider,
        }
        return response
