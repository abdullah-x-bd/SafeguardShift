from __future__ import annotations
import json,os
from pathlib import Path
from safeguardshift.openrouter import Client,ModelSpec
from safeguardshift.ledger import CostGate
from safeguardshift.data import load_tasks
from safeguardshift.tools import tool_schema
from safeguardshift.render import render
def main():
    if not os.getenv("OPENROUTER_API_KEY"): raise SystemExit("OPENROUTER_API_KEY is required")
    panel=json.loads(Path("v2/configs/model_panel_v2.json").read_text())["backbone"]
    task=load_tasks()[0]; gate=CostGate(0.05); client=Client(gate=gate,retries=1); results=[]
    for m in panel:
        spec=ModelSpec(m["id"],m["provider"],m["max_token_field"],m["temperature"],m["reserve_usd"])
        resp=client.chat(spec,[{"role":"user","content":render(task,"full")}],tool_schema(task),tool_choice="auto",max_tokens=64)
        results.append({"model":spec.id,"provider":spec.provider,"response_id":resp.get("id"),"pass":bool(resp.get("choices"))})
    print({"status":"PASS" if all(r["pass"] for r in results) else "FAIL","results":results,"cost_usd":gate.spent_usd})
if __name__=="__main__":main()
