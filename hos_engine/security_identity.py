from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Optional, Set
import uuid

class IdentityType(str,Enum):
    HUMAN="HUMAN"; AGENT="AGENT"; APPLICATION="APPLICATION"; SERVICE="SERVICE"; HUB="HUB"
class IdentityStatus(str,Enum):
    ACTIVE="ACTIVE"; SUSPENDED="SUSPENDED"; REVOKED="REVOKED"

@dataclass(frozen=True)
class KeyDescriptor:
    key_id:str; algorithm:str; public_material:str; created_at:str
    expires_at:Optional[str]=None; revoked_at:Optional[str]=None

@dataclass(frozen=True)
class ComponentIdentity:
    identity_id:str; identity_type:IdentityType; display_name:str; owner_id:str
    key_ids:Set[str]=field(default_factory=set)
    status:IdentityStatus=IdentityStatus.ACTIVE
    created_at:str=field(default_factory=lambda:datetime.now(timezone.utc).isoformat())

class IdentityRegistry:
    def __init__(self): self._ids:Dict[str,ComponentIdentity]={}; self._keys:Dict[str,KeyDescriptor]={}
    def register_identity(self,*,identity_type,display_name,owner_id,identity_id=None):
        x=ComponentIdentity(identity_id or "HOS-ID-"+uuid.uuid4().hex[:12].upper(),identity_type,display_name,owner_id)
        if x.identity_id in self._ids: raise ValueError("Identity already exists")
        self._ids[x.identity_id]=x; return x
    def attach_key(self,identity_id,key):
        x=self._ids[identity_id]
        if key.key_id in self._keys: raise ValueError("Key already exists")
        self._keys[key.key_id]=key
        self._ids[identity_id]=replace(x,key_ids=set(x.key_ids)|{key.key_id})
    def revoke(self,identity_id): self._ids[identity_id]=replace(self._ids[identity_id],status=IdentityStatus.REVOKED)
    def suspend(self,identity_id): self._ids[identity_id]=replace(self._ids[identity_id],status=IdentityStatus.SUSPENDED)
    def get_identity(self,identity_id): return self._ids[identity_id]
    def get_key(self,key_id): return self._keys[key_id]
