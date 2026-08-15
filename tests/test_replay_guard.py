import time
import unittest

from hos_engine.protocol_security import secure_envelope
from hos_engine.replay_guard import ReplayGuard


class ReplayTests(unittest.TestCase):
    def test_replay_and_expiry(self):
        g=ReplayGuard()
        e=secure_envelope(protocol="HOSP/0.2",message_type="q",sender_id="A",recipient_id="B",
          subject_id="H",purpose="p",payload={},ttl_seconds=300)
        now=time.time();self.assertTrue(g.check(e,now).accepted);self.assertFalse(g.check(e,now).accepted)
        e2=secure_envelope(protocol="HOSP/0.2",message_type="q",sender_id="A",recipient_id="B",
          subject_id="H",purpose="p",payload={},ttl_seconds=1)
        self.assertFalse(g.check(e2,time.time()+10).accepted)
