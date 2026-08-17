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
   # '*' is a wildcard for purpose, domain and action alike -- matching the
   # TrustPolicy convention. Previously only domain honoured it, so a
   # wildcard purpose/action grant silently failed to authorise.
   if not self._covers(purpose,g.purposes) or not self._covers(domain,g.domains) or not self._covers(action,g.actions): continue
   if sensitive and not g.allow_sensitive: continue
   return True
  return False
 @staticmethod
 def _covers(value:str,allowed:set[str])->bool: return value in allowed or '*' in allowed
