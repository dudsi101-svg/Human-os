from hos_engine.protocol_security import HMACSigner, secure_envelope


class SecureEnvelopeBuilder:
    def __init__(self,*,sender_id,key_id,secret):
        self.sender_id=sender_id;self.signer=HMACSigner(key_id,secret)
    def build(self,*,recipient_id,subject_id,purpose,message_type,payload,ttl_seconds=300):
        e=secure_envelope(protocol="HOSP/0.2",message_type=message_type,sender_id=self.sender_id,
          recipient_id=recipient_id,subject_id=subject_id,purpose=purpose,payload=payload,
          ttl_seconds=ttl_seconds)
        return self.signer.sign(e)
