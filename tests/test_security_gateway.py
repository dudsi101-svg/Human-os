import time
import unittest
from datetime import UTC, datetime

from hos_engine.protocol_security import HMACSigner, secure_envelope
from hos_engine.replay_guard import ReplayGuard
from hos_engine.security_gateway import SecurityGateway
from hos_engine.security_identity import IdentityRegistry, IdentityType, KeyDescriptor
from hos_engine.trust import TrustLevel, TrustPolicy, TrustRegistry


class GatewayTests(unittest.TestCase):
    def setUp(self):
        self.s=HMACSigner("K1",b"secret")
        self.ids=IdentityRegistry()
        self.ids.register_identity(identity_type=IdentityType.APPLICATION,
            display_name="Planner",owner_id="H1",identity_id="APP1")
        self.ids.attach_key("APP1",KeyDescriptor("K1","HMAC-SHA256","ref",
            datetime.now(UTC).isoformat()))
        self.tr=TrustRegistry()
        self.tr.set_policy(TrustPolicy("P1","APP1",TrustLevel.TRUSTED,
            {"hos.query"},{"planning"},{"goals"}))
        self.g=SecurityGateway(self.ids,self.tr,ReplayGuard(),{"K1":self.s})

    def test_allow_and_deny(self):
        e=secure_envelope(protocol="HOSP/0.2",message_type="hos.query",
            sender_id="APP1",recipient_id="HUB",subject_id="H1",
            purpose="planning",payload={"domain":"goals"})
        self.assertTrue(self.g.evaluate(self.s.sign(e),time.time()).accepted)

        e2=secure_envelope(protocol="HOSP/0.2",message_type="hos.query",
            sender_id="APP1",recipient_id="HUB",subject_id="H1",
            purpose="planning",payload={"domain":"finance"})
        self.assertFalse(self.g.evaluate(self.s.sign(e2),time.time()).accepted)
