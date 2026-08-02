import unittest
from hos_engine.consent import ConsentRegistry
class T(unittest.TestCase):
 def test_purpose_and_revoke(self):
  c=ConsentRegistry(); g=c.grant(subject_id='H',grantee_id='A',purposes={'planning'},domains={'goals'},actions={'read'}); self.assertTrue(c.authorize(subject_id='H',grantee_id='A',purpose='planning',domain='goals',action='read')); self.assertFalse(c.authorize(subject_id='H',grantee_id='A',purpose='marketing',domain='goals',action='read')); c.revoke(g.consent_id,'H'); self.assertFalse(c.authorize(subject_id='H',grantee_id='A',purpose='planning',domain='goals',action='read'))
