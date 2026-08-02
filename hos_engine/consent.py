from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Iterable, Optional, Set
import uuid
class ConsentStatus(str,Enum): ACTIVE='ACTIVE'; REVOKED='REVOKED'
@dataclass(frozen=True)
class ConsentGrant:
 consent_id:str; subject_id:str; grantee_id:str; purposes:Set[str]; domains:Set[str]; actions:Set[str]; issued_at:str; expires_at:Optional[str]=None; allow_sensitive:bool=False; status:ConsentStatus=ConsentStatus.ACTIVE
class ConsentRegistry:
 def __init__(self): self._grants:Dict[str,ConsentGrant]={}
 def grant(self,*,subject_id,grantee_id,purposes,domains,actions,expires_at=None,allow_sensitive=False):
  g=ConsentGrant('HOS-CNS-'+uuid.uuid4().hex[:12].upper(),subject_id,grantee_id,set(purposes),set(domains),set(actions),datetime.now(timezone.utc).isoformat(),expires_at,allow_sensitive); self._grants[g.consent_id]=g; return g
 def revoke(self,consent_id,subject_id):
  g=self._grants[consent_id]
  if g.subject_id!=subject_id: raise PermissionError('Only subject may revoke')
  self._grants[consent_id]=ConsentGrant(**{**g.__dict__,'status':ConsentStatus.REVOKED})
 def authorize(self,*,subject_id,grantee_id,purpose,domain,action,sensitive=False,now_iso=None):
  now=now_iso or datetime.now(timezone.utc).isoformat()
  for g in self._grants.values():
   if g.status!=ConsentStatus.ACTIVE or g.subject_id!=subject_id or g.grantee_id!=grantee_id: continue
   if g.expires_at and now>=g.expires_at: continue
   if purpose not in g.purposes or (domain not in g.domains and '*' not in g.domains) or action not in g.actions: continue
   if sensitive and not g.allow_sensitive: continue
   return True
  return False
