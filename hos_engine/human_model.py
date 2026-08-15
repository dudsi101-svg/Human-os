from __future__ import annotations

import uuid
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from enum import Enum
from typing import Any


class EvidenceType(str,Enum):
 USER_DECLARATION='USER_DECLARATION'; OBSERVATION='OBSERVATION'; VERIFIED_FACT='VERIFIED_FACT'; AI_INFERENCE='AI_INFERENCE'; HYPOTHESIS='HYPOTHESIS'
class RecordStatus(str,Enum):
 ACTIVE='ACTIVE'; CONTESTED='CONTESTED'; SUPERSEDED='SUPERSEDED'; DELETED='DELETED'
@dataclass(frozen=True)
class HumanRecord:
 record_id:str; subject_id:str; domain:str; key:str; value:Any; evidence_type:EvidenceType; confidence:float; source_id:str; created_at:str; status:RecordStatus=RecordStatus.ACTIVE; supersedes:str | None=None; sensitive:bool=False; tags:set[str]=field(default_factory=set)
class HumanModel:
 def __init__(self): self._records:dict[str,HumanRecord]={}
 def add(self,*,subject_id,domain,key,value,evidence_type,confidence,source_id,sensitive=False,tags=None,supersedes=None):
  if not 0<=confidence<=1: raise ValueError('confidence must be between 0 and 1')
  if supersedes and supersedes not in self._records: raise KeyError('superseded record does not exist')
  r=HumanRecord('HOS-HMR-'+uuid.uuid4().hex[:12].upper(),subject_id,domain,key,value,evidence_type,confidence,source_id,datetime.now(UTC).isoformat(),supersedes=supersedes,sensitive=sensitive,tags=set(tags or [])); self._records[r.record_id]=r
  if supersedes: self._records[supersedes]=replace(self._records[supersedes],status=RecordStatus.SUPERSEDED)
  return r
 def contest(self,record_id,*,subject_id):
  r=self._records[record_id]
  if r.subject_id!=subject_id: raise PermissionError('Only subject may contest')
  self._records[record_id]=replace(r,status=RecordStatus.CONTESTED)
 def active_records(self,subject_id,domain=None):
  xs=[r for r in self._records.values() if r.subject_id==subject_id and r.status==RecordStatus.ACTIVE]
  return [r for r in xs if domain is None or r.domain==domain]
 def get(self,record_id): return self._records[record_id]
