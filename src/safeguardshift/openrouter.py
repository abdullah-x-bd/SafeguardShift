from __future__ import annotations
import json,os,time,urllib.request,urllib.error
from dataclasses import dataclass
from typing import Any
from .ledger import CostGate,request_hash
URL="https://openrouter.ai/api/v1/chat/completions"
@dataclass(frozen=True)
class ModelSpec:
    id:str; provider:str; max_token_field:str="max_tokens"; temperature:float|None=0.0; reserve_usd:float=0.003
class Client:
    def __init__(self,key:str|None=None,gate:CostGate|None=None,retries:int=3):
        self.key=key or os.getenv("OPENROUTER_API_KEY")
        if not self.key:raise RuntimeError("OPENROUTER_API_KEY is not set")
        self.gate=gate;self.retries=retries
    def chat(self,spec:ModelSpec,messages:list[dict],tools:list[dict],tool_choice:Any="auto",max_tokens:int=350)->dict:
        if self.gate:self.gate.reserve(spec.reserve_usd)
        body={"model":spec.id,"messages":messages,"tools":tools,"tool_choice":tool_choice,spec.max_token_field:max_tokens,
              "provider":{"order":[spec.provider],"allow_fallbacks":False}}
        if spec.temperature is not None:body["temperature"]=spec.temperature
        reqhash=request_hash(body); last=None
        for attempt in range(self.retries+1):
            req=urllib.request.Request(URL,data=json.dumps(body).encode(),headers={"Authorization":f"Bearer {self.key}","Content-Type":"application/json","X-Title":"SafeguardShift"},method="POST")
            try:
                with urllib.request.urlopen(req,timeout=120) as r: resp=json.loads(r.read())
                usage=resp.get("usage") or {}; cost=usage.get("cost")
                if self.gate:self.gate.add(float(cost) if isinstance(cost,(int,float)) else spec.reserve_usd)
                resp["_safeguardshift_request"]={"sha256":reqhash,"requested_model":spec.id,"requested_provider":spec.provider}
                return resp
            except urllib.error.HTTPError as e:
                last=RuntimeError(f"OpenRouter HTTP {e.code}: {e.read().decode(errors='replace')}")
                if e.code not in (408,409,429,500,502,503,504) or attempt==self.retries:raise last
                time.sleep(min(2**attempt,8))
        raise last or RuntimeError("request failed")
