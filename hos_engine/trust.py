from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Set
class TrustLevel(str,Enum):
    UNTRUSTED="UNTRUSTED"; LIMITED="LIMITED"; TRUSTED="TRUSTED"; PRIVILEGED="PRIVILEGED"
@dataclass(frozen=True)
class TrustPolicy:
    policy_id:str; identity_id:str; trust_level:TrustLevel
    allowed_message_types:Set[str]=field(default_factory=set)
    allowed_purposes:Set[str]=field(default_factory=set)
    allowed_domains:Set[str]=field(default_factory=set)
class TrustRegistry:
    def __init__(self):self.policies:Dict[str,TrustPolicy]={}
    def set_policy(self,p):self.policies[p.identity_id]=p
    def authorize(self,*,identity_id,message_type,purpose,domain):
        p=self.policies.get(identity_id)
        if not p or p.trust_level==TrustLevel.UNTRUSTED:return False
        return ((message_type in p.allowed_message_types or "*" in p.allowed_message_types)
          and (purpose in p.allowed_purposes or "*" in p.allowed_purposes)
          and (domain in p.allowed_domains or "*" in p.allowed_domains))
