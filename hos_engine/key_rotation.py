import uuid
from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True)
class KeyRotation:
    rotation_id:str; identity_id:str; previous_key_id:str; new_key_id:str
    effective_at:str; overlap_until:str | None; approved_by:str
def create_rotation(*,identity_id:str,previous_key_id:str,new_key_id:str,approved_by:str,overlap_until:str | None=None)->KeyRotation:
    return KeyRotation("HOS-KRT-"+uuid.uuid4().hex[:12].upper(),identity_id,previous_key_id,
      new_key_id,datetime.now(UTC).isoformat(),overlap_until,approved_by)
