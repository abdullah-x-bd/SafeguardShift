from __future__ import annotations
import hashlib,json
from dataclasses import dataclass
def request_hash(body:dict)->str:return hashlib.sha256(json.dumps(body,sort_keys=True,separators=(",",":")).encode()).hexdigest()
@dataclass
class CostGate:
    max_usd:float; spent_usd:float=0.0
    def reserve(self,amount:float)->None:
        if self.spent_usd+amount>self.max_usd:raise RuntimeError(f"cost gate would exceed ${self.max_usd:.2f}")
    def add(self,amount:float)->None:self.spent_usd+=amount
