from pathlib import Path
import os, json
from crisisbench.verify import verify_dataset

result=verify_dataset(Path(__file__).resolve().parents[1])
result["openrouter_key_present"]=bool(os.getenv("OPENROUTER_API_KEY"))
print(json.dumps(result,indent=2,sort_keys=True))
if result["status"]!="PASS": raise SystemExit(1)
