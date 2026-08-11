from __future__ import annotations
from .environment import Environment
from .schema import Task
from .scoring import score
def run_oracle(task:Task,condition:str)->dict:
    e=Environment(task,condition)
    e.tool("inspect_state",{})
    if condition=="substitute":
        e.tool("request_substitute",{})
        e.tool("attempt_action",{"action_id":task.substitution_target_action})
    else:
        target=task.substitution_target_action
        result=e.tool("attempt_action",{"action_id":target})
        if result.get("status")=="blocked":
            e.tool("attempt_action",{"action_id":task.safe_fallbacks[0]})
    e.tool("submit_final_plan",{"recommended_actions":[],"actions_to_avoid":[],"remaining_uncertainties":[],"fallback_plan":[],"confidence":0.9})
    rec={"task_id":task.task_id,"condition":condition,"attempted":e.attempted,"terminal_plan":e.terminal_plan,"substitute_activated":e.substitute_activated}
    rec["score"]=score(task,rec); return rec
