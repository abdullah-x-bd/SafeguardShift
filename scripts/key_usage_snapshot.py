from __future__ import annotations
import json
import os
import urllib.request
from pathlib import Path


def main() -> None:
    key=os.environ["OPENROUTER_API_KEY"]
    req=urllib.request.Request("https://openrouter.ai/api/v1/key",headers={"Authorization":f"Bearer {key}"})
    with urllib.request.urlopen(req,timeout=30) as r:
        payload=json.loads(r.read())
    data=payload.get("data") or {}
    keep={k:data.get(k) for k in ("limit","limit_remaining","limit_reset","usage","usage_daily","usage_weekly","usage_monthly","is_free_tier")}
    Path("results/key_usage_snapshot.json").write_text(json.dumps(keep,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(keep,indent=2,sort_keys=True))

if __name__=="__main__": main()
