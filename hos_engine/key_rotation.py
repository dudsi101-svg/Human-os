from dataclasses import dataclass
from datetime import datetime,timezone
from typing import Optional
import uuid
@dataclass(frozen=True)
class KeyRotation:
    rotation_id:str; identity_id:str; previous_key_id:str; new_key_id:str
    effective_at:str; overlap_until:Optional[str]; approved_by:str
def create_rotation(*,identity_id,previous_key_id,new_key_id,approved_by,overlap_until=None):
    return KeyRotation("HOS-KRT-"+uuid.uuid4().hex[:12].upper(),identity_id,previous_key_id,
      new_key_id,datetime.now(timezone.utc).isoformat(),overlap_until,approved_by)
