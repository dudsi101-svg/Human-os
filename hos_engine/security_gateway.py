from dataclasses import dataclass

from .protocol_security import HMACSigner, SignedEnvelope
from .replay_guard import ReplayGuard
from .security_identity import IdentityRegistry, IdentityStatus
from .trust import TrustRegistry


@dataclass(frozen=True)
class SecurityDecision: accepted:bool; status:str; reason:str
class SecurityGateway:
    def __init__(self,identities:IdentityRegistry,trust:TrustRegistry,replay_guard:ReplayGuard,verifiers:dict[str,HMACSigner])->None:
        self.identities=identities;self.trust=trust;self.replay_guard=replay_guard;self.verifiers=verifiers
    def evaluate(self,signed:SignedEnvelope,now_epoch:float | None=None)->SecurityDecision:
        e=signed.envelope; sender=str(e.get("sender_id","")); key=signed.signature.key_id
        try:i=self.identities.get_identity(sender)
        except KeyError:return SecurityDecision(False,"DENIED","Unknown sender")
        if i.status!=IdentityStatus.ACTIVE:return SecurityDecision(False,"DENIED","Inactive identity")
        if key not in i.key_ids:return SecurityDecision(False,"DENIED","Key not bound to sender")
        v=self.verifiers.get(key)
        if not v or not v.verify(signed):return SecurityDecision(False,"DENIED","Invalid signature")
        r=self.replay_guard.check(e,now_epoch)
        if not r.accepted:return SecurityDecision(False,"DENIED",r.reason)
        payload=e.get("payload") or {}; domain=str(payload.get("domain","*"))
        if not self.trust.authorize(identity_id=sender,message_type=str(e.get("message_type","")),
            purpose=str(e.get("purpose","")),domain=domain):
            return SecurityDecision(False,"DENIED","Trust policy rejected request")
        return SecurityDecision(True,"ACCEPTED","Security checks passed")
