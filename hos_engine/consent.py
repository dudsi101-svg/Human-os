import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum


class ConsentStatus(str,Enum): ACTIVE='ACTIVE'; REVOKED='REVOKED'
@dataclass(frozen=True)
class ConsentGrant:
 consent_id:str; subject_id:str; grantee_id:str; purposes:set[str]; domains:set[str]; actions:set[str]; issued_at:str; expires_at:str | None=None; allow_sensitive:bool=False; status:ConsentStatus=ConsentStatus.ACTIVE
class ConsentRegistry:
 def __init__(self)->None: self._grants:dict[str,ConsentGrant]={}
 def grant(self,*,subject_id:str,grantee_id:str,purposes:set[str],domains:set[str],actions:set[str],expires_at:str | None=None,allow_sensitive:bool=False)->ConsentGrant:
  g=ConsentGrant('HOS-CNS-'+uuid.uuid4().hex[:12].upper(),subject_id,grantee_id,set(purposes),set(domains),set(actions),datetime.now(UTC).isoformat(),expires_at,allow_sensitive); self._grants[g.consent_id]=g; return g
 def revoke(self,consent_id:str,subject_id:str)->None:
  g=self._grants[consent_id]
  if g.subject_id!=subject_id: raise PermissionError('Only subject may revoke')
  self._grants[consent_id]=ConsentGrant(**{**g.__dict__,'status':ConsentStatus.REVOKED})
 def authorize(self,*,subject_id:str,grantee_id:str,purpose:str,domain:str,action:str,sensitive:bool=False,now_iso:str | None=None)->bool:
  now=now_iso or datetime.now(UTC).isoformat()
  for g in self._grants.values():
   if g.status!=ConsentStatus.ACTIVE or g.subject_id!=subject_id or g.grantee_id!=grantee_id: continue
   if g.expires_at and now>=g.expires_at: continue
   if purpose not in g.purposes or (domain not in g.domains and '*' not in g.domains) or action not in g.actions: continue
   if sensitive and not g.allow_sensitive: continue
   return True
  return False
