import unittest

from hos_engine.protocol_security import *


class ProtocolSecurityTests(unittest.TestCase):
    def test_signature_and_tamper(self):
        s=HMACSigner("K1",b"secret")
        e=secure_envelope(protocol="HOSP/0.2",message_type="hos.query",sender_id="A",
          recipient_id="B",subject_id="H",purpose="planning",payload={"domain":"goals"})
        x=s.sign(e);self.assertTrue(s.verify(x))
        x.envelope["payload"]["domain"]="finance";self.assertFalse(s.verify(x))
