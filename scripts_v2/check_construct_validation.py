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
    if row.get("validation_regime")!="two_judge_task_unanimity_with_gpt54_corruption_sentinel":errors.append("wrong validation regime")
    if row.get("criterion_pass_rule")!="both_task_judges_yes":errors.append("wrong criterion pass rule")
    if row.get("status")!="PASS":errors.append("construct validation did not pass")
    if row.get("tasks_validated")!=72 or row.get("task_pass_count")!=72:errors.append("not all 72 tasks passed")
    if row.get("failed_tasks"):errors.append("failed task list is non-empty")
    if row.get("valid_task_response_count")!=144 or row.get("valid_task_response_expected")!=144:errors.append("expected 144 valid real-task judgments")
    controls=row.get("corruption_controls") or {}
    if controls.get("status")!="PASS":errors.append("corruption sentinel failed")
    if controls.get("sentinel_judge")!="openai/gpt-5.4":errors.append("wrong corruption sentinel")
    detected=controls.get("detected_by_judge") or {}
    if detected.get("openai/gpt-5.4")!=12:errors.append("GPT-5.4 sentinel must detect all 12 corruption controls")
    freeze=Path("v2/FREEZE_MANIFEST.json");panel=Path("v2/configs/validation_panel_v2.json")
    if row.get("freeze_manifest_sha256")!=sha256(freeze):errors.append("validation result is stale relative to current V2 freeze manifest")
    if row.get("validation_panel_sha256")!=sha256(panel):errors.append("validation result is stale relative to validation panel")
    print(json.dumps({"status":"PASS" if not errors else "FAIL","errors":errors},indent=2));raise SystemExit(0 if not errors else 2)

if __name__=="__main__":main()
