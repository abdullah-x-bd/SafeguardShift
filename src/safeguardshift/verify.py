from __future__ import annotations
import hashlib
from collections import Counter
from pathlib import Path
from .data import load_tasks

def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(root:Path=Path("."))->dict:
    tasks=load_tasks(root/"v2/data/scenarios.json.gz");errs=[]
    if len(tasks)!=72:errs.append(f"expected 72 tasks, got {len(tasks)}")
    ids=[t.task_id for t in tasks]
    if len(set(ids))!=72:errs.append("duplicate task ids")
    domains=Counter(t.domain for t in tasks);rel=Counter(t.relevant_safeguard for t in tasks)
    if set(domains.values())!={12}:errs.append(f"domain imbalance {domains}")
    if set(rel.values())!={12}:errs.append(f"safeguard imbalance {rel}")
    for t in tasks:
        if len({t.relevant_safeguard,t.secondary_safeguard,t.irrelevant_safeguard})!=3:errs.append(f"{t.task_id}: safeguard roles overlap")
        target=next((a for a in t.actions if a.id==t.substitution_target_action),None)
        if not target or tuple(target.requires)!=(t.relevant_safeguard,):errs.append(f"{t.task_id}: substitution target must depend only on relevant safeguard")
        hi=[a for a in t.actions if a.action_class=="high_impact"]
        if len(hi)!=1 or set(hi[0].requires)!={t.relevant_safeguard,t.secondary_safeguard}:errs.append(f"{t.task_id}: high-impact action must depend exactly on relevant and secondary safeguards")
        for action in t.actions:
            if t.irrelevant_safeguard in action.requires:errs.append(f"{t.task_id}: irrelevant safeguard affects executable action {action.id}")
            if action.action_class not in ("safeguard_dependent","high_impact") and action.requires:errs.append(f"{t.task_id}: fallback action {action.id} must be safeguard-independent")
        if any(term in a.label.lower() for a in t.actions for term in ("safeguard-dependent","relevant safeguard","irrelevant safeguard","negative control")):errs.append(f"{t.task_id}: agent-visible action label leaks experimental terminology")
    return {"status":"PASS" if not errs else "FAIL","tasks":len(tasks),"domains":dict(domains),"relevant_safeguards":dict(rel),"scenario_cells":len(tasks)*5,"backbone_cells_per_replicate":len(tasks)*5*4,"backbone_trajectories_3rep":len(tasks)*5*4*3,"errors":errs,"manifest_sha256":sha(root/"v2/data/base_tasks_manifest.json")}
