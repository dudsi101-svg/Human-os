import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True)
class ProtocolEnvelope:
 message_type:str; sender_id:str; recipient_id:str; subject_id:str; purpose:str; payload:dict; consent_refs:list[str]=field(default_factory=list); protocol:str='HOSP/0.1'; message_id:str=field(default_factory=lambda:'HOS-MSG-'+uuid.uuid4().hex[:12].upper()); created_at:str=field(default_factory=lambda:datetime.now(UTC).isoformat())
 def to_dict(self): return self.__dict__.copy()
