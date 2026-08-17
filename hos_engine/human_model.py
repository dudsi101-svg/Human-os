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
 # context/unit/quality/consent_scope added per ADR-HUMAN-004 (Layer 2's
 # mandatory per-record metadata, source SS19.2); optional so pre-existing
 # records and callers keep working unchanged.
 # valid_from/valid_to/last_confirmed_at/evidence_refs added per
 # ADR-SELFMODEL-001 (temporality + multi-source provenance for the
 # conversational self model); optional for the same compatibility reason.
 record_id:str; subject_id:str; domain:str; key:str; value:Any; evidence_type:EvidenceType; confidence:float; source_id:str; created_at:str; status:RecordStatus=RecordStatus.ACTIVE; supersedes:str | None=None; sensitive:bool=False; tags:set[str]=field(default_factory=set); context:str | None=None; unit:str | None=None; quality:str | None=None; consent_scope:str | None=None; valid_from:str | None=None; valid_to:str | None=None; last_confirmed_at:str | None=None; evidence_refs:tuple[str,...]=()
class HumanModel:
 def __init__(self)->None: self._records:dict[str,HumanRecord]={}
 def add(self,*,subject_id:str,domain:str,key:str,value:Any,evidence_type:EvidenceType,confidence:float,source_id:str,sensitive:bool=False,tags:set[str] | None=None,supersedes:str | None=None,context:str | None=None,unit:str | None=None,quality:str | None=None,consent_scope:str | None=None,valid_from:str | None=None,valid_to:str | None=None,last_confirmed_at:str | None=None,evidence_refs:tuple[str,...]=())->HumanRecord:
  if not 0<=confidence<=1: raise ValueError('confidence must be between 0 and 1')
  if supersedes and supersedes not in self._records: raise KeyError('superseded record does not exist')
  r=HumanRecord('HOS-HMR-'+uuid.uuid4().hex[:12].upper(),subject_id,domain,key,value,evidence_type,confidence,source_id,datetime.now(UTC).isoformat(),supersedes=supersedes,sensitive=sensitive,tags=set(tags or []),context=context,unit=unit,quality=quality,consent_scope=consent_scope,valid_from=valid_from,valid_to=valid_to,last_confirmed_at=last_confirmed_at,evidence_refs=tuple(evidence_refs)); self._records[r.record_id]=r
  if supersedes: self._records[supersedes]=replace(self._records[supersedes],status=RecordStatus.SUPERSEDED)
  return r
 def contest(self,record_id:str,*,subject_id:str)->None:
  r=self._records[record_id]
  if r.subject_id!=subject_id: raise PermissionError('Only subject may contest')
  self._records[record_id]=replace(r,status=RecordStatus.CONTESTED)
 def active_records(self,subject_id:str,domain:str | None=None)->list[HumanRecord]:
  xs=[r for r in self._records.values() if r.subject_id==subject_id and r.status==RecordStatus.ACTIVE]
  return [r for r in xs if domain is None or r.domain==domain]
 def all_records(self)->list[HumanRecord]: return list(self._records.values())
 @classmethod
 def restore(cls,records:list[HumanRecord])->HumanModel:
  m=cls()
  for r in records: m._records[r.record_id]=r
  return m
 def records_of(self,subject_id:str,status:RecordStatus | None=None)->list[HumanRecord]:
  return [r for r in self._records.values() if r.subject_id==subject_id and (status is None or r.status==status)]
 def get(self,record_id:str)->HumanRecord: return self._records[record_id]
