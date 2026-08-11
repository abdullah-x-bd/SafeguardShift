from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path

def sha256(path:Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()

def main()->None:
    ap=argparse.ArgumentParser();ap.add_argument("path",nargs="?",default="results/v2/construct_validation.json");args=ap.parse_args()
    p=Path(args.path)
    if not p.exists():raise SystemExit("construct validation result missing")
    row=json.loads(p.read_text(encoding="utf-8"));errors=[]
    if row.get("protocol")!="safeguardshift-v2.0.0":errors.append("wrong protocol")
    if row.get("validation_regime")!="qualified_two_judge_synthetic_construct_validation":errors.append("wrong validation regime")
    if row.get("criterion_pass_rule")!="both_qualified_judges_yes":errors.append("wrong criterion pass rule")
    if row.get("status")!="PASS":errors.append("construct validation did not pass")
    if row.get("tasks_validated")!=72 or row.get("task_pass_count")!=72:errors.append("not all 72 tasks passed")
    if row.get("failed_tasks"):errors.append("failed task list is non-empty")
    if row.get("valid_response_count")!=168 or row.get("valid_response_expected")!=168:errors.append("expected 168 valid panel responses")
    if (row.get("corruption_controls") or {}).get("status")!="PASS":errors.append("corruption controls failed")
    detected=(row.get("corruption_controls") or {}).get("detected_by_judge") or {}
    if sorted(detected.values())!=[12,12]:errors.append("both qualified judges must detect all 12 corruption controls")
    freeze=Path("v2/FREEZE_MANIFEST.json");panel=Path("v2/configs/validation_panel_v2.json")
    if row.get("freeze_manifest_sha256")!=sha256(freeze):errors.append("validation result is stale relative to current V2 freeze manifest")
    if row.get("validation_panel_sha256")!=sha256(panel):errors.append("validation result is stale relative to validation panel")
    print(json.dumps({"status":"PASS" if not errors else "FAIL","errors":errors},indent=2));raise SystemExit(0 if not errors else 2)

if __name__=="__main__":main()
