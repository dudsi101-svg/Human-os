import unittest

from hos_engine.consent import ConsentRegistry


class T(unittest.TestCase):
 def test_purpose_and_revoke(self):
  c=ConsentRegistry(); g=c.grant(subject_id='H',grantee_id='A',purposes={'planning'},domains={'goals'},actions={'read'}); self.assertTrue(c.authorize(subject_id='H',grantee_id='A',purpose='planning',domain='goals',action='read')); self.assertFalse(c.authorize(subject_id='H',grantee_id='A',purpose='marketing',domain='goals',action='read')); c.revoke(g.consent_id,'H'); self.assertFalse(c.authorize(subject_id='H',grantee_id='A',purpose='planning',domain='goals',action='read'))


class WildcardConsentTests(unittest.TestCase):
    """Regression: the 2026-08-17 simulation found '*' was honoured only for
    domain, so a wildcard purpose/action grant silently failed to authorise,
    inconsistent with the TrustPolicy convention."""

    def setUp(self):
        self.reg = ConsentRegistry()

    def test_wildcard_purpose_and_action_authorise(self):
        self.reg.grant(subject_id="S", grantee_id="G",
                       purposes={"*"}, domains={"*"}, actions={"*"})
        self.assertTrue(self.reg.authorize(
            subject_id="S", grantee_id="G",
            purpose="anything", domain="health", action="write"))

    def test_specific_grant_still_scoped(self):
        self.reg.grant(subject_id="S", grantee_id="G",
                       purposes={"read"}, domains={"health"}, actions={"read"})
        self.assertTrue(self.reg.authorize(
            subject_id="S", grantee_id="G",
            purpose="read", domain="health", action="read"))
        self.assertFalse(self.reg.authorize(
            subject_id="S", grantee_id="G",
            purpose="write", domain="health", action="read"))
