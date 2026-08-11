from __future__ import annotations

import argparse
import json
from pathlib import Path

from safeguardshift.data import load_tasks
from safeguardshift.ledger import CostGate
from safeguardshift.openrouter import Client, ModelSpec
from run_construct_validation import ALIASES, corruption, prompt, task_payload, tool_schema

CANDIDATES = [
    {"id":"mistralai/mistral-medium-3.1","provider":"mistral","max_token_field":"max_tokens","temperature":0.0,"reserve_usd":0.005,"max_tokens":256},
]


def assess(client: Client, candidate: dict, payload: dict) -> dict:
    spec=ModelSpec(candidate["id"],candidate["provider"],candidate["max_token_field"],candidate["temperature"],candidate["reserve_usd"])
    response=client.chat(spec,[{"role":"user","content":prompt(payload)}],tool_schema(),tool_choice={"type":"function","function":{"name":"submit_construct_validation"}},max_tokens=int(candidate["max_tokens"]))
    choice=response.get("choices",[{}])[0]; message=choice.get("message",{}); calls=message.get("tool_calls") or []; args={}
    if calls:
        try: args=json.loads(calls[0]["function"].get("arguments") or "{}")
        except Exception: args={}
    valid=all(alias in args for alias in ALIASES) and "cf" in args
    judgments={criterion:bool(args.get(alias,False)) for alias,criterion in ALIASES.items()}
    return {"valid_response":valid,"detected_corruption":valid and not all(judgments.values()),"judgments":judgments,"confidence":args.get("cf") if valid else None,"finish_reason":choice.get("finish_reason"),"response_id":response.get("id"),"usage":response.get("usage"),"request":response.get("_safeguardshift_request")}


def main() -> None:
    ap=argparse.ArgumentParser(); ap.add_argument("--max-cost",type=float,default=0.10); ap.add_argument("--output",default="results/private/v2/validator_qualification.json"); args=ap.parse_args()
    panel=json.loads(Path("v2/configs/validation_panel_v2.json").read_text(encoding="utf-8")); task_map={t.task_id:t for t in load_tasks()}; controls=panel["corruption_controls"]["task_ids"]; modes=("irrelevant_collision","bad_substitute","bad_action_contract"); minimum=int(panel["corruption_controls"]["per_judge_minimum_detected"])
    gate=CostGate(args.max_cost); client=Client(gate=gate,retries=2); results={}
    for candidate in CANDIDATES:
        rows=[]
        for idx,task_id in enumerate(controls):
            row=assess(client,candidate,corruption(task_payload(task_map[task_id]),modes[idx%len(modes)])); row.update({"task_id":task_id,"control_mode":modes[idx%len(modes)]}); rows.append(row)
        valid=sum(bool(r["valid_response"]) for r in rows); detected=sum(bool(r["detected_corruption"]) for r in rows)
        results[candidate["id"]]={"provider":candidate["provider"],"max_tokens":candidate["max_tokens"],"valid_responses":valid,"detected_controls":detected,"required_detected":minimum,"pass":valid==12 and detected>=minimum,"rows":rows}
    payload={"status":"PASS" if all(r["pass"] for r in results.values()) else "FAIL","purpose":"validator qualification on corruption controls only; no canonical task judgments","results":results,"cost_usd":gate.spent_usd}
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":payload["status"],"cost_usd":gate.spent_usd,"results":{k:{"valid":v["valid_responses"],"detected":v["detected_controls"],"pass":v["pass"]} for k,v in results.items()}},sort_keys=True))
    raise SystemExit(0 if payload["status"]=="PASS" else 2)

if __name__=="__main__": main()
