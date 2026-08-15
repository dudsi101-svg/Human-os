from dataclasses import dataclass
from typing import Any

from .human_model import HumanRecord


@dataclass(frozen=True)
class PersonalizationContext:
 subject_id:str; grantee_id:str; purpose:str; records:list[HumanRecord]; projection:dict[str,Any]
class ConsentAwarePersonalizer:
 def __init__(self,model,consents): self.model=model; self.consents=consents
 def build_context(self,*,subject_id,grantee_id,purpose,domain):
  if not self.consents.authorize(subject_id=subject_id,grantee_id=grantee_id,purpose=purpose,domain=domain,action='read'): raise PermissionError('No active consent')
  records=[r for r in self.model.active_records(subject_id,domain) if not r.sensitive or self.consents.authorize(subject_id=subject_id,grantee_id=grantee_id,purpose=purpose,domain=domain,action='read',sensitive=True)]
  projection={r.key:{'value':r.value,'evidence_type':r.evidence_type.value,'confidence':r.confidence} for r in records}
  return PersonalizationContext(subject_id,grantee_id,purpose,records,projection)
