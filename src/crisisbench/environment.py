from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from .schemas import Task
from .render import capacity_state

@dataclass
class CrisisEnvironment:
    task: Task
    condition: str
    capacity: dict[str,str] = field(init=False)
    substitute_available: bool = field(init=False)
    substitute_activated: bool = False
    attempted: list[dict[str,Any]] = field(default_factory=list)
    observations: list[dict[str,Any]] = field(default_factory=list)
    terminal_plan: dict[str,Any] | None = None

    def __post_init__(self) -> None:
        self.capacity, self.substitute_available = capacity_state(self.task,self.condition)

    def action(self, action_id: str) -> dict[str,Any]:
        contract=next((a for a in self.task.actions if a.id==action_id),None)
        if contract is None: return {"status":"error","reason":"unknown_action"}
        missing=[s for s in contract.requires if self.capacity.get(s)!="available"]
        substitute_used = False
        if self.substitute_activated and self.task.relevant_safeguard in missing:
            missing.remove(self.task.relevant_safeguard)
            substitute_used = True
        allowed=not missing
        record={"action_id":action_id,"allowed":allowed,"missing":missing,"risk":contract.risk,"reversibility":contract.reversibility,"utility":contract.utility,"substitute_used":substitute_used and allowed}
        self.attempted.append(record)
        return {"status":"executed" if allowed else "blocked",**record}

    def inspect(self) -> dict[str,Any]:
        obs={"known_facts":list(self.task.known_facts),"unknown_facts":list(self.task.unknown_facts)}
        self.observations.append(obs); return obs

    def check_capacity(self, safeguard: str) -> dict[str,Any]:
        return {"safeguard":safeguard,"status":self.capacity.get(safeguard,"unknown")}

    def request_substitute(self) -> dict[str,Any]:
        if not self.substitute_available: return {"status":"unavailable","reason":"no substitute is available in this condition"}
        self.substitute_activated=True
        return {"status":"activated","for":self.task.relevant_safeguard,"substitute":self.task.substitute["label"]}

    def submit(self, plan: dict[str,Any]) -> dict[str,Any]:
        self.terminal_plan=plan
        return {"status":"complete","recorded":True}

    def execute_tool(self, name: str, args: dict[str,Any]) -> dict[str,Any]:
        if name=="inspect_state": return self.inspect()
        if name=="check_capacity": return self.check_capacity(str(args.get("safeguard","")))
        if name=="attempt_action": return self.action(str(args.get("action_id","")))
        if name=="request_substitute": return self.request_substitute()
        if name=="submit_final_plan": return self.submit(args)
        return {"status":"error","reason":"unknown_tool"}
