import time
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ReplayDecision: accepted:bool; reason:str
class ReplayGuard:
    def __init__(self)->None: self.ids:set[str]=set(); self.nonces:set[str]=set()
    def check(self,envelope:dict[str,Any],now_epoch:float | None=None)->ReplayDecision:
        now=time.time() if now_epoch is None else now_epoch
        mid=str(envelope.get("message_id","")); nonce=str(envelope.get("nonce",""))
        if not mid or not nonce:return ReplayDecision(False,"Missing identifier")
        if float(envelope.get("expires_at",0))<=now:return ReplayDecision(False,"Envelope expired")
        if mid in self.ids:return ReplayDecision(False,"Message already processed")
        if nonce in self.nonces:return ReplayDecision(False,"Nonce already used")
        self.ids.add(mid); self.nonces.add(nonce)
        return ReplayDecision(True,"Envelope accepted")
