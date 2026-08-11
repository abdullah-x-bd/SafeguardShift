from __future__ import annotations
from dataclasses import dataclass,field
from typing import Any
from .schema import Task,SAFEGUARDS

def capacity_state(task:Task,condition:str)->tuple[dict[str,str],bool]:
    state={s:"available" for s in SAFEGUARDS}; substitute=False
    if condition=="relevant_ablation": state[task.relevant_safeguard]="unavailable"
    elif condition=="irrelevant_ablation": state[task.irrelevant_safeguard]="unavailable"
    elif condition=="substitute": state[task.relevant_safeguard]="unavailable"; substitute=True
    elif condition=="compound_ablation":
        state[task.relevant_safeguard]="unavailable"; state[task.secondary_safeguard]="unavailable"
    elif condition!="full": raise ValueError(condition)
    return state,substitute

@dataclass
class Environment:
    task:Task; condition:str
    capacity:dict[str,str]=field(init=False); substitute_available:bool=field(init=False)
    substitute_activated:bool=False; attempted:list[dict[str,Any]]=field(default_factory=list)
    terminal_plan:dict[str,Any]|None=None
    def __post_init__(self): self.capacity,self.substitute_available=capacity_state(self.task,self.condition)
    def execute(self,action_id:str)->dict[str,Any]:
        a=next((x for x in self.task.actions if x.id==action_id),None)
        if a is None:return {"status":"error","reason":"unknown_action"}
        missing=[s for s in a.requires if self.capacity.get(s)!="available"]; used=False
        if self.substitute_activated and self.task.relevant_safeguard in missing:
            missing.remove(self.task.relevant_safeguard); used=True
        allowed=not missing
        r={"action_id":a.id,"action_class":a.action_class,"allowed":allowed,"missing":missing,"risk":a.risk,
           "reversibility":a.reversibility,"utility":a.utility,"substitute_used":used and allowed}
        self.attempted.append(r); return {"status":"executed" if allowed else "blocked",**r}
    def tool(self,name:str,args:dict[str,Any])->dict[str,Any]:
        if name=="inspect_state": return {"known_facts":list(self.task.known_facts),"unknown_facts":list(self.task.unknown_facts)}
        if name=="check_capacity":
            s=str(args.get("safeguard","")); return {"safeguard":s,"status":self.capacity.get(s,"unknown")}
        if name=="attempt_action": return self.execute(str(args.get("action_id","")))
        if name=="request_substitute":
            if not self.substitute_available:return {"status":"unavailable"}
            self.substitute_activated=True; return {"status":"activated","restores":self.task.relevant_safeguard,"label":self.task.substitute["label"]}
        if name=="submit_final_plan": self.terminal_plan=args; return {"status":"complete"}
        return {"status":"error","reason":"unknown_tool"}
