"""Tests for the unified AuthorizationDecision composition skeleton."""

import unittest

from hos_engine.authorization_decision import (
    AspectResult,
    AuthorizationAction,
    AuthorizationComposer,
    AuthorizationRequest,
)


def _request(**overrides):
    defaults = {
        "identity_id": "HOS-IDN-000001",
        "identity_kind": "HUMAN",
        "authority_role": "OWNER",
        "resource_selector": "self_model/*",
        "action": AuthorizationAction.WRITE,
        "purpose": "update confirmed value",
        "consent_refs": ("C1",),
        "policy_version": "0.2.0",
    }
    defaults.update(overrides)
    return AuthorizationRequest(**defaults)


def _pass(aspect):
    return lambda req: AspectResult(aspect, True, "ok")


def _fail(aspect, why):
    return lambda req: AspectResult(aspect, False, why)


class TestAuthorizationComposer(unittest.TestCase):
    def test_required_aspects_are_mandatory_config(self):
        with self.assertRaises(ValueError):
            AuthorizationComposer(set())
        with self.assertRaises(TypeError):
            AuthorizationComposer()  # no default exists on purpose

    def test_all_aspects_pass_allows_and_receipts_echo(self):
        composer = AuthorizationComposer({"identity", "authority", "consent"})
        for aspect in ("identity", "authority", "consent"):
            composer.register(aspect, _pass(aspect))
        decision = composer.decide(_request())
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.reasons, ())
        self.assertEqual(len(decision.aspect_results), 3)
        self.assertEqual(decision.request.purpose, "update confirmed value")
        self.assertEqual(decision.request.policy_version, "0.2.0")
        self.assertTrue(decision.decision_id.startswith("HOS-AUZ-"))

    def test_deny_first_one_failed_aspect_denies_all(self):
        composer = AuthorizationComposer({"identity", "consent"})
        composer.register("identity", _pass("identity"))
        composer.register("consent", _fail("consent", "C5 withdrawn"))
        decision = composer.decide(_request())
        self.assertFalse(decision.allowed)
        self.assertIn("consent: C5 withdrawn", decision.reasons)

    def test_missing_required_aspect_is_not_evaluated_never_silent(self):
        composer = AuthorizationComposer({"identity", "authority"})
        composer.register("identity", _pass("identity"))
        decision = composer.decide(_request())
        self.assertFalse(decision.allowed)
        self.assertIn("NOT_EVALUATED:authority", decision.reasons)

    def test_extra_registered_aspect_still_gates(self):
        composer = AuthorizationComposer({"identity"})
        composer.register("identity", _pass("identity"))
        composer.register("call_rule", _fail("call_rule", "argument too large"))
        decision = composer.decide(_request())
        self.assertFalse(decision.allowed)
        self.assertIn("call_rule: argument too large", decision.reasons)

    def test_no_silent_check_replacement(self):
        composer = AuthorizationComposer({"identity"})
        composer.register("identity", _pass("identity"))
        with self.assertRaises(ValueError):
            composer.register("identity", _fail("identity", "swapped"))

    def test_decision_is_immutable(self):
        composer = AuthorizationComposer({"identity"})
        composer.register("identity", _pass("identity"))
        decision = composer.decide(_request())
        with self.assertRaises(AttributeError):
            decision.allowed = False  # type: ignore[misc]


if __name__ == "__main__":
    unittest.main()
