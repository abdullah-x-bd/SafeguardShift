from __future__ import annotations
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

IDS = [
    "gen-1786392529-qxQjdpceBhJfmqbslCHd",
    "gen-1786392531-OyNiflq66AamNZBExYcQ",
    "gen-1786392532-YMQlFsMFxI46LJPzDVDv",
    "gen-1786392534-z5RHId3tOcS7BZG6STp0",
]


def main() -> None:
    key=os.environ["OPENROUTER_API_KEY"]
    rows=[]
    for gid in IDS:
        req=urllib.request.Request(
            "https://openrouter.ai/api/v1/generation?"+urllib.parse.urlencode({"id":gid}),
            headers={"Authorization":f"Bearer {key}"},
        )
        with urllib.request.urlopen(req,timeout=30) as r:
            data=json.loads(r.read()).get("data") or {}
        rows.append({
            "id":gid,
            "model":data.get("model"),
            "provider_name":data.get("provider_name"),
            "finish_reason":data.get("finish_reason"),
            "native_finish_reason":data.get("native_finish_reason"),
            "tokens_prompt":data.get("tokens_prompt"),
            "tokens_completion":data.get("tokens_completion"),
            "native_tokens_reasoning":data.get("native_tokens_reasoning"),
            "total_cost":data.get("total_cost"),
            "upstream_inference_cost":data.get("upstream_inference_cost"),
            "usage":data.get("usage"),
        })
    Path("results/gemini_generation_audit.json").write_text(json.dumps(rows,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(rows,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
