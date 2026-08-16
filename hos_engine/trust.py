from dataclasses import dataclass, field
from enum import Enum


class TrustLevel(str,Enum):
    UNTRUSTED="UNTRUSTED"; LIMITED="LIMITED"; TRUSTED="TRUSTED"; PRIVILEGED="PRIVILEGED"
@dataclass(frozen=True)
class TrustPolicy:
    policy_id:str; identity_id:str; trust_level:TrustLevel
    allowed_message_types:set[str]=field(default_factory=set)
    allowed_purposes:set[str]=field(default_factory=set)
    allowed_domains:set[str]=field(default_factory=set)
class TrustRegistry:
    def __init__(self)->None:self.policies:dict[str,TrustPolicy]={}
    def set_policy(self,p:TrustPolicy)->None:self.policies[p.identity_id]=p
    def authorize(self,*,identity_id:str,message_type:str,purpose:str,domain:str)->bool:
        p=self.policies.get(identity_id)
        if not p or p.trust_level==TrustLevel.UNTRUSTED:return False
        return ((message_type in p.allowed_message_types or "*" in p.allowed_message_types)
          and (purpose in p.allowed_purposes or "*" in p.allowed_purposes)
          and (domain in p.allowed_domains or "*" in p.allowed_domains))
