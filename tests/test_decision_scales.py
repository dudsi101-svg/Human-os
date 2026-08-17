"""DD-006 skeleton tests.

ALL policy and measurement values in this file are SYNTHETIC TEST FIXTURES.
They exist only to exercise the mechanism and are NOT recommended,
calibrated, or founder-approved interpretations of any scale.
"""

from __future__ import annotations

import unittest

from hos_engine.decision_scales import (
    SCALE_DEFINITIONS,
    InterpretationOutcomeKind,
    InterpretationPolicy,
    ScaleInterpreter,
    ScaleKind,
    ScaleMeasurement,
)

SYNTHETIC_APPROVER = "SYNTHETIC-TEST-FIXTURE (not a real approval)"
SYNTHETIC_BASIS = "syntetyczna fixture testowa - nie jest pomiarem ani rekomendacją"


def synthetic_policy(**overrides):
    defaults = {
        "policy_id": "SYNTHETIC-POLICY-001",
        "version": "0.0.0-synthetic",
        "approved_by": SYNTHETIC_APPROVER,
        "scale": ScaleKind.INPUT_QUALITY,
        "rules": {"IQ0": "synthetic-outcome-a", "IQ5": "synthetic-outcome-b"},
    }
    defaults.update(overrides)
    return InterpretationPolicy(**defaults)


class ScaleStructureTests(unittest.TestCase):
    def test_di_has_eight_codes_iq_and_ar_have_six(self):
        self.assertEqual(
            SCALE_DEFINITIONS[ScaleKind.DECISION_INTENT].codes(),
            tuple(f"DI-{i}" for i in range(1, 9)),
        )
        self.assertEqual(
            SCALE_DEFINITIONS[ScaleKind.INPUT_QUALITY].codes(),
            tuple(f"IQ{i}" for i in range(6)),
        )
        self.assertEqual(
            SCALE_DEFINITIONS[ScaleKind.ACTION_READINESS].codes(),
            tuple(f"AR{i}" for i in range(6)),
        )

    def test_structure_carries_no_numeric_thresholds(self):
        for definition in SCALE_DEFINITIONS.values():
            for level in definition.levels:
                self.assertIsInstance(level.code, str)
            self.assertFalse(hasattr(definition, "thresholds"))

    def test_structure_is_immutable(self):
        with self.assertRaises(TypeError):
            SCALE_DEFINITIONS[ScaleKind.INPUT_QUALITY] = None  # type: ignore[index]


class MeasurementTests(unittest.TestCase):
    def test_valid_measurement(self):
        m = ScaleMeasurement(
            scale=ScaleKind.ACTION_READINESS, code="AR3",
            declared_by="HOS-HUM-000001", basis=SYNTHETIC_BASIS,
        )
        self.assertTrue(m.measurement_id.startswith("HOS-MSR-"))

    def test_code_must_belong_to_scale(self):
        with self.assertRaises(ValueError):
            ScaleMeasurement(
                scale=ScaleKind.INPUT_QUALITY, code="IQ9",
                declared_by="HOS-HUM-000001", basis=SYNTHETIC_BASIS,
            )
        with self.assertRaises(ValueError):
            ScaleMeasurement(
                scale=ScaleKind.INPUT_QUALITY, code="AR3",
                declared_by="HOS-HUM-000001", basis=SYNTHETIC_BASIS,
            )

    def test_measurement_requires_basis_and_identity(self):
        with self.assertRaises(ValueError):
            ScaleMeasurement(
                scale=ScaleKind.INPUT_QUALITY, code="IQ2",
                declared_by="HOS-HUM-000001", basis="   ",
            )
        with self.assertRaises(ValueError):
            ScaleMeasurement(
                scale=ScaleKind.INPUT_QUALITY, code="IQ2",
                declared_by="", basis=SYNTHETIC_BASIS,
            )


class PolicyTests(unittest.TestCase):
    def test_policy_requires_version_and_approver(self):
        with self.assertRaises(ValueError):
            synthetic_policy(version=" ")
        with self.assertRaises(ValueError):
            synthetic_policy(approved_by="")

    def test_policy_rejects_codes_outside_its_scale(self):
        with self.assertRaises(ValueError):
            synthetic_policy(rules={"AR1": "x"})

    def test_policy_rules_are_immutable(self):
        policy = synthetic_policy()
        with self.assertRaises(TypeError):
            policy.rules["IQ1"] = "sneaky"  # type: ignore[index]


class InterpreterTests(unittest.TestCase):
    def measurement(self, code="IQ0"):
        return ScaleMeasurement(
            scale=ScaleKind.INPUT_QUALITY, code=code,
            declared_by="HOS-HUM-000001", basis=SYNTHETIC_BASIS,
        )

    def test_no_policy_yields_configuration_required(self):
        outcome = ScaleInterpreter().interpret(self.measurement())
        self.assertEqual(
            outcome.kind, InterpretationOutcomeKind.CONFIGURATION_REQUIRED,
        )
        self.assertIsNone(outcome.result)
        self.assertIn("DD-006", outcome.reason)

    def test_missing_rule_yields_configuration_required_not_a_guess(self):
        outcome = ScaleInterpreter(synthetic_policy()).interpret(
            self.measurement("IQ3"),
        )
        self.assertEqual(
            outcome.kind, InterpretationOutcomeKind.CONFIGURATION_REQUIRED,
        )
        self.assertIsNone(outcome.result)

    def test_wrong_scale_policy_yields_configuration_required(self):
        policy = synthetic_policy(
            scale=ScaleKind.ACTION_READINESS, rules={"AR0": "synthetic"},
        )
        outcome = ScaleInterpreter(policy).interpret(self.measurement())
        self.assertEqual(
            outcome.kind, InterpretationOutcomeKind.CONFIGURATION_REQUIRED,
        )

    def test_explicit_rule_interprets_and_carries_policy_provenance(self):
        outcome = ScaleInterpreter(synthetic_policy()).interpret(
            self.measurement("IQ0"),
        )
        self.assertEqual(outcome.kind, InterpretationOutcomeKind.INTERPRETED)
        self.assertEqual(outcome.result, "synthetic-outcome-a")
        self.assertEqual(outcome.policy_id, "SYNTHETIC-POLICY-001")
        self.assertEqual(outcome.policy_version, "0.0.0-synthetic")

    def test_outcomes_are_values_not_exceptions(self):
        interpreter = ScaleInterpreter()
        outcome = interpreter.interpret(self.measurement())
        self.assertIsNotNone(outcome.measurement_id)


if __name__ == "__main__":
    unittest.main()


class ApprovedShadowPolicyTests(unittest.TestCase):
    """The founder-signed v0.2.0 shadow policies (2026-08-17, rules taken
    verbatim from the Layer 5 source DOCX sections 5.2/6.1/8.2) must load
    into the engine's types and interpret every code of all three scales.
    The v0.1.0 interpolations stay recorded as superseded history."""

    @classmethod
    def setUpClass(cls):
        import json
        from pathlib import Path
        raw = json.loads(
            (Path(__file__).parent.parent
             / "policies" / "scale.interpretation.policies.json").read_text()
        )
        cls.raw = raw
        cls.policies = {
            entry["scale"]: InterpretationPolicy(
                policy_id=entry["policy_id"],
                version=entry["version"],
                approved_by=raw["approved_by"],
                scale=ScaleKind(entry["scale"]),
                rules=entry["rules"],
            )
            for entry in raw["policies"]
        }

    def test_config_is_shadow_mode_and_attributed(self):
        self.assertEqual(self.raw["mode"], "SHADOW")
        self.assertTrue(self.raw["approved_by"].strip())
        self.assertTrue(self.raw["approved_at"].strip())

    def test_all_three_scales_have_a_signed_policy(self):
        self.assertEqual(set(self.policies), {"IQ", "AR", "DI"})
        for policy in self.policies.values():
            self.assertEqual(policy.version, "0.2.0")

    def test_policies_cover_every_code_of_their_scale(self):
        for scale_name, policy in self.policies.items():
            definition = SCALE_DEFINITIONS[ScaleKind(scale_name)]
            self.assertEqual(set(policy.rules), set(definition.codes()))

    def test_signed_policy_interprets_with_source_wording(self):
        m = ScaleMeasurement(
            scale=ScaleKind.INPUT_QUALITY, code="IQ0",
            declared_by="HOS-HUM-000001", basis=SYNTHETIC_BASIS,
        )
        outcome = ScaleInterpreter(self.policies["IQ"]).interpret(m)
        self.assertEqual(outcome.kind, InterpretationOutcomeKind.INTERPRETED)
        self.assertEqual(outcome.result, "tylko-pytania-bezpieczenstwo-eskalacja")
        self.assertEqual(outcome.policy_version, "0.2.0")

    def test_di_interprets_via_signed_source_policy(self):
        m = ScaleMeasurement(
            scale=ScaleKind.DECISION_INTENT, code="DI-8",
            declared_by="HOS-HUM-000001", basis=SYNTHETIC_BASIS,
        )
        outcome = ScaleInterpreter(self.policies["DI"]).interpret(m)
        self.assertEqual(outcome.kind, InterpretationOutcomeKind.INTERPRETED)
        self.assertEqual(
            outcome.result, "priorytet-bezpieczenstwa-i-kontakt-z-pomoca",
        )

    def test_no_policy_still_means_configuration_required(self):
        # the safe-refusal mechanism is untouched by the sign-off
        m = ScaleMeasurement(
            scale=ScaleKind.DECISION_INTENT, code="DI-1",
            declared_by="HOS-HUM-000001", basis=SYNTHETIC_BASIS,
        )
        outcome = ScaleInterpreter().interpret(m)
        self.assertEqual(
            outcome.kind, InterpretationOutcomeKind.CONFIGURATION_REQUIRED,
        )

    def test_superseded_v010_is_preserved_as_history(self):
        superseded = self.raw.get("superseded", [])
        versions = {(e["policy_id"], e["version"]) for e in superseded}
        self.assertIn(("HOS-POL-IQ-001", "0.1.0"), versions)
        self.assertIn(("HOS-POL-AR-001", "0.1.0"), versions)
        for entry in superseded:
            self.assertEqual(entry["superseded_by"], "0.2.0")


class PolicyLoaderTests(unittest.TestCase):
    """load_policies_json turns the signed policy file into runtime
    policies -- active section only, approver required."""

    PATH = "policies/scale.interpretation.policies.json"

    def test_loads_all_three_active_policies(self):
        from hos_engine.decision_scales import load_policies_json
        loaded = load_policies_json(self.PATH)
        self.assertEqual(
            {k.value for k in loaded}, {"IQ", "AR", "DI"},
        )
        for kind, policy in loaded.items():
            self.assertIs(policy.scale, kind)
            self.assertEqual(policy.version, "0.2.0")
            self.assertTrue(policy.approved_by.strip())

    def test_superseded_versions_are_never_loaded(self):
        from hos_engine.decision_scales import load_policies_json
        loaded = load_policies_json(self.PATH)
        for policy in loaded.values():
            self.assertNotEqual(policy.version, "0.1.0")

    def test_unattributed_file_refuses_to_load(self):
        import json
        import tempfile

        from hos_engine.decision_scales import load_policies_json
        with tempfile.NamedTemporaryFile(
            "w", suffix=".json", delete=False, encoding="utf-8",
        ) as handle:
            json.dump({"policies": []}, handle)
            path = handle.name
        with self.assertRaises(ValueError):
            load_policies_json(path)
