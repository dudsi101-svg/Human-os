"""AuthorizationComposer wired to the real registries (audit §13, step 2).

The checks below are the thin closures the contract describes: each one
delegates to an existing mechanism (RoleGrantRegistry, ConsentRegistry)
and none reimplements its rules.
"""

import unittest

from hos_engine.authority import AuthorityRole, RoleGrantRegistry
from hos_engine.authorization_decision import (
    AspectResult,
    AuthorizationAction,
    AuthorizationComposer,
    AuthorizationRequest,
)
from hos_engine.consent import ConsentRegistry


def _role_check(registry: RoleGrantRegistry):
    def check(req: AuthorizationRequest) -> AspectResult:
        role = AuthorityRole(req.authority_role)
        ok = registry.has_role(req.identity_id, role)
        return AspectResult(
            "authority", ok,
            "active grant found" if ok else f"no active {role.value} grant for {req.identity_id}",
        )
    return check


def _consent_check(registry: ConsentRegistry, grantee_id: str, domain: str):
    def check(req: AuthorizationRequest) -> AspectResult:
        ok = registry.authorize(
            subject_id=req.identity_id, grantee_id=grantee_id,
            purpose=req.purpose, domain=domain, action=req.action.value.lower(),
        )
        return AspectResult("consent", ok, "consent active" if ok else "no active consent covers this purpose/action")
    return check


class TestComposerWithRealRegistries(unittest.TestCase):
    def setUp(self):
        self.roles = RoleGrantRegistry()
        self.consents = ConsentRegistry()
        self.composer = AuthorizationComposer({"authority", "consent"})
        self.composer.register("authority", _role_check(self.roles))
        self.composer.register("consent", _consent_check(self.consents, "HOS-APP-000001", "self_model"))
        self.request = AuthorizationRequest(
            identity_id="HOS-IDN-000042",
            identity_kind="HUMAN",
            authority_role="OWNER",
            resource_selector="self_model/*",
            action=AuthorizationAction.WRITE,
            purpose="personalization",
        )

    def test_denied_until_both_mechanisms_grant(self):
        d0 = self.composer.decide(self.request)
        self.assertFalse(d0.allowed)
        self.assertEqual(len(d0.reasons), 2)

        self.roles.grant(identity_id="HOS-IDN-000042", role=AuthorityRole.OWNER, scope="self_model", issued_by="HOS-IDN-000001")
        d1 = self.composer.decide(self.request)
        self.assertFalse(d1.allowed)
        self.assertTrue(any(r.startswith("consent:") for r in d1.reasons))

        self.consents.grant(
            subject_id="HOS-IDN-000042", grantee_id="HOS-APP-000001",
            purposes={"personalization"}, domains={"self_model"}, actions={"write"},
        )
        d2 = self.composer.decide(self.request)
        self.assertTrue(d2.allowed)
        self.assertEqual(d2.reasons, ())

    def test_consent_revocation_flips_decision(self):
        self.roles.grant(identity_id="HOS-IDN-000042", role=AuthorityRole.OWNER, scope="self_model", issued_by="HOS-IDN-000001")
        grant = self.consents.grant(
            subject_id="HOS-IDN-000042", grantee_id="HOS-APP-000001",
            purposes={"personalization"}, domains={"self_model"}, actions={"write"},
        )
        self.assertTrue(self.composer.decide(self.request).allowed)
        self.consents.revoke(grant.consent_id, "HOS-IDN-000042")
        decision = self.composer.decide(self.request)
        self.assertFalse(decision.allowed)
        self.assertTrue(any("consent" in r for r in decision.reasons))

    def test_role_revocation_flips_decision(self):
        grant = self.roles.grant(
            identity_id="HOS-IDN-000042", role=AuthorityRole.OWNER, scope="self_model",
            issued_by="HOS-IDN-000001",
        )
        self.consents.grant(
            subject_id="HOS-IDN-000042", grantee_id="HOS-APP-000001",
            purposes={"personalization"}, domains={"self_model"}, actions={"write"},
        )
        self.assertTrue(self.composer.decide(self.request).allowed)
        self.roles.revoke(grant.grant_id)
        self.assertFalse(self.composer.decide(self.request).allowed)


if __name__ == "__main__":
    unittest.main()
