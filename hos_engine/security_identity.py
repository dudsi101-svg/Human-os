import uuid
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from enum import Enum


class IdentityType(str,Enum):
    HUMAN="HUMAN"; AGENT="AGENT"; APPLICATION="APPLICATION"; SERVICE="SERVICE"; HUB="HUB"
class IdentityStatus(str,Enum):
    ACTIVE="ACTIVE"; SUSPENDED="SUSPENDED"; REVOKED="REVOKED"

@dataclass(frozen=True)
class KeyDescriptor:
    key_id:str; algorithm:str; public_material:str; created_at:str
    expires_at:str | None=None; revoked_at:str | None=None

@dataclass(frozen=True)
class ComponentIdentity:
    identity_id:str; identity_type:IdentityType; display_name:str; owner_id:str
    key_ids:set[str]=field(default_factory=set)
    status:IdentityStatus=IdentityStatus.ACTIVE
    created_at:str=field(default_factory=lambda:datetime.now(UTC).isoformat())

class IdentityRegistry:
    def __init__(self)->None: self._ids:dict[str,ComponentIdentity]={}; self._keys:dict[str,KeyDescriptor]={}
    def register_identity(self,*,identity_type:IdentityType,display_name:str,owner_id:str,identity_id:str | None=None)->ComponentIdentity:
        x=ComponentIdentity(identity_id or "HOS-ID-"+uuid.uuid4().hex[:12].upper(),identity_type,display_name,owner_id)
        if x.identity_id in self._ids: raise ValueError("Identity already exists")
        self._ids[x.identity_id]=x; return x
    def attach_key(self,identity_id:str,key:KeyDescriptor)->None:
        x=self._ids[identity_id]
        if key.key_id in self._keys: raise ValueError("Key already exists")
        self._keys[key.key_id]=key
        self._ids[identity_id]=replace(x,key_ids=set(x.key_ids)|{key.key_id})
    def revoke(self,identity_id:str)->None: self._ids[identity_id]=replace(self._ids[identity_id],status=IdentityStatus.REVOKED)
    def suspend(self,identity_id:str)->None: self._ids[identity_id]=replace(self._ids[identity_id],status=IdentityStatus.SUSPENDED)
    def get_identity(self,identity_id:str)->ComponentIdentity: return self._ids[identity_id]
    def get_key(self,key_id:str)->KeyDescriptor: return self._keys[key_id]
