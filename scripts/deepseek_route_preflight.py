from __future__ import annotations
import json
import os
from crisisbench.ledger import CostGate
from crisisbench.openrouter import ModelSpec, OpenRouterClient
from crisisbench.tools import tool_schema


def main() -> None:
    if not os.getenv("OPENROUTER_API_KEY"):
        raise SystemExit("OPENROUTER_API_KEY is required")
    gate=CostGate(0.02)
    client=OpenRouterClient(cost_gate=gate)
    tools=[t for t in tool_schema() if t["function"]["name"]=="inspect_state"]
    forced={"type":"function","function":{"name":"inspect_state"}}
    rows=[]
    for provider in ("atlas-cloud","baidu-qianfan"):
        spec=ModelSpec("deepseek/deepseek-v3.2",provider,conservative_request_usd=0.001)
        try:
            response=client.chat(spec,[{"role":"system","content":"Call inspect_state exactly once."},{"role":"user","content":"Call inspect_state."}],tools,max_tokens=80,tool_choice=forced)
            calls=(response.get("choices") or [{}])[0].get("message",{}).get("tool_calls") or []
            rows.append({"status":"PASS" if calls and calls[0].get("function",{}).get("name")=="inspect_state" else "FAIL","requested_provider":provider,"routed_provider":response.get("provider"),"response_id":response.get("id")})
        except Exception as exc:
            rows.append({"status":"FAIL","requested_provider":provider,"error":str(exc)})
    print(json.dumps({"cost_usd":gate.spent_usd,"routes":rows},sort_keys=True))
    if not any(r["status"]=="PASS" for r in rows): raise SystemExit(1)

if __name__=="__main__": main()
