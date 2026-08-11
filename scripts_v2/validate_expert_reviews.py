from __future__ import annotations
import csv,sys
from collections import defaultdict
from pathlib import Path
path=Path(sys.argv[1] if len(sys.argv)>1 else "v2/validation/expert_reviews.csv")
if not path.exists(): raise SystemExit("expert review file missing")
rows=list(csv.DictReader(path.open(encoding="utf-8")))
by=defaultdict(list)
for r in rows:
    if r.get("reviewer_id"): by[r["task_id"]].append(r)
errors=[]
required=("relevant_safeguard_valid","irrelevant_safeguard_valid","substitute_plausible","actions_plausible","pair_equivalence_valid","utility_order_valid")
for task,rs in by.items():
    if len({r["reviewer_id"] for r in rs})<2: errors.append(f"{task}: fewer than two independent reviewers")
    for r in rs:
        for k in required:
            if r.get(k,"").strip().lower() not in ("yes","true","1"): errors.append(f"{task}/{r.get('reviewer_id')}: {k} not approved")
if len(by)!=72: errors.append(f"expected reviews for 72 tasks, got {len(by)}")
print({"status":"PASS" if not errors else "FAIL","tasks_reviewed":len(by),"errors":errors})
raise SystemExit(0 if not errors else 2)
