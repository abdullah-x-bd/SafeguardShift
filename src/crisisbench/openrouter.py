from __future__ import annotations
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any
from .ledger import CostGate, request_hash

BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
GENERATION_URL = "https://openrouter.ai/api/v1/generation"

@dataclass(frozen=True)
class ModelSpec:
    id: str
    provider: str
    temperature: float | None = 0.0
    max_token_field: str = "max_tokens"
    conservative_request_usd: float = 0.003
    reasoning: dict[str, Any] | None = None

class OpenRouterClient:
    def __init__(self, api_key: str | None = None, cost_gate: CostGate | None = None, max_retries: int = 3) -> None:
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENROUTER_API_KEY is not set")
        self.cost_gate = cost_gate
        self.max_retries = max_retries

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

    def generation_cost(self, generation_id: str) -> float | None:
        query = urllib.parse.urlencode({"id": generation_id})
        req = urllib.request.Request(
            f"{GENERATION_URL}?{query}",
            headers={"Authorization": f"Bearer {self.api_key}"},
            method="GET",
        )
        for delay in (0.15, 0.35, 0.75):
            time.sleep(delay)
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    payload = json.loads(r.read())
                data = payload.get("data") or {}
                value = data.get("total_cost")
                if isinstance(value, (int, float)):
                    return float(value)
            except urllib.error.HTTPError as exc:
                if exc.code not in (404, 429, 500, 502, 503, 504):
                    return None
            except (TimeoutError, urllib.error.URLError, json.JSONDecodeError):
                pass
        return None

    def chat(
        self,
        spec: ModelSpec,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
        max_tokens: int = 500,
        tool_choice: Any = "auto",
    ) -> dict[str, Any]:
        reserve = spec.conservative_request_usd
        if self.cost_gate:
            self.cost_gate.allow(reserve)
        body: dict[str, Any] = {
            "model": spec.id,
            "messages": messages,
            "tools": tools,
            "tool_choice": tool_choice,
            "provider": {
                "order": [spec.provider],
                "allow_fallbacks": False,
                "require_parameters": True,
                "data_collection": "allow",
            },
        }
        body[spec.max_token_field] = max_tokens
        if spec.temperature is not None:
            body["temperature"] = spec.temperature
        if spec.reasoning is not None:
            body["reasoning"] = spec.reasoning
        digest = request_hash(body)
        request_bytes = json.dumps(body).encode()
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/abdullah-x-bd/crisisbench",
            "X-Title": "CrisisBench",
        }
        response: dict[str, Any] | None = None
        last_error: str | None = None
        for attempt in range(self.max_retries + 1):
            req = urllib.request.Request(BASE_URL, data=request_bytes, headers=headers, method="POST")
            try:
                with urllib.request.urlopen(req, timeout=120) as r:
                    response = json.loads(r.read())
                break
            except urllib.error.HTTPError as exc:
                detail = exc.read().decode(errors="replace")
                last_error = f"OpenRouter HTTP {exc.code}: {detail}"
                if exc.code not in (429, 500, 502, 503, 504) or attempt >= self.max_retries:
                    raise RuntimeError(last_error) from exc
                time.sleep(1.0 * (2**attempt))
            except (TimeoutError, urllib.error.URLError) as exc:
                last_error = f"OpenRouter transport error: {exc}"
                if attempt >= self.max_retries:
                    raise RuntimeError(last_error) from exc
                time.sleep(1.0 * (2**attempt))
        if response is None:
            raise RuntimeError(last_error or "OpenRouter request failed")
        cost = self.response_cost(response)
        cost_source = "response_usage"
        if cost is None and isinstance(response.get("id"), str):
            cost = self.generation_cost(response["id"])
            cost_source = "generation_audit" if cost is not None else "model_price_reserve"
        if cost is None:
            cost = reserve
            cost_source = "model_price_reserve"
        if self.cost_gate:
            self.cost_gate.add(cost)
        response["_crisisbench_request"] = {
            "sha256": digest,
            "requested_model": spec.id,
            "requested_provider": spec.provider,
            "temperature": spec.temperature,
            "max_token_field": spec.max_token_field,
            "accounted_cost_usd": cost,
            "cost_source": cost_source,
            "conservative_request_usd": reserve,
        }
        return response
