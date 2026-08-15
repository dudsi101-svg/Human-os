import base64
import hashlib
import hmac
import json
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any


def canonical_json(payload:dict[str,Any])->bytes:
    return json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()

@dataclass(frozen=True)
class Signature:
    key_id:str; algorithm:str; value:str
@dataclass(frozen=True)
class SignedEnvelope:
    envelope:dict[str,Any]; signature:Signature

class HMACSigner:
    algorithm="HMAC-SHA256"
    def __init__(self,key_id,secret:bytes):
        if not secret: raise ValueError("secret cannot be empty")
        self.key_id=key_id; self.secret=secret
    def sign(self,envelope):
        d=hmac.new(self.secret,canonical_json(envelope),hashlib.sha256).digest()
        return SignedEnvelope(dict(envelope),Signature(self.key_id,self.algorithm,base64.urlsafe_b64encode(d).decode()))
    def verify(self,signed):
        if signed.signature.algorithm!=self.algorithm:return False
        expected=hmac.new(self.secret,canonical_json(signed.envelope),hashlib.sha256).digest()
        try: provided=base64.urlsafe_b64decode(signed.signature.value.encode())
        except Exception:return False  # noqa: BLE001 -- malformed signature encoding must fail verification, not raise
        return hmac.compare_digest(expected,provided)

def secure_envelope(*,protocol,message_type,sender_id,recipient_id,subject_id,purpose,payload,ttl_seconds=300,nonce:str | None=None):
    now=datetime.now(UTC)
    return {"protocol":protocol,"message_id":"HOS-MSG-"+uuid.uuid4().hex[:12].upper(),
      "message_type":message_type,"sender_id":sender_id,"recipient_id":recipient_id,
      "subject_id":subject_id,"purpose":purpose,"created_at":now.isoformat(),
      "expires_at":now.timestamp()+ttl_seconds,
      "nonce":nonce or "HOS-NONCE-"+uuid.uuid4().hex[:16].upper(),"payload":payload}
