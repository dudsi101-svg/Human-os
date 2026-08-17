from __future__ import annotations

import json
import unittest
from pathlib import Path

from hos_engine.validation import SchemaRegistry

ROOT = Path(__file__).parent.parent

COMMONS_TYPES = [
    "CHALLENGE_CREATED",
    "CHALLENGE_PUBLISHED",
    "CHALLENGE_JOINED",
    "CHALLENGE_LEFT",
    "COMMITMENT_CREATED",
    "COMMITMENT_RENEGOTIATED",
    "CHECKIN_RECORDED",
    "EXPERIENCE_SHARED",
    "EXPERIENCE_RETRACTED",
    "SUPPORT_REQUESTED",
    "SUPPORT_ACCEPTED",
    "OUTCOME_RECORDED",
    "MODERATION_CASE_OPENED",
    "MODERATION_CASE_RESOLVED",
]


def dictionary() -> list[str]:
    return json.loads((ROOT / "event.types.json").read_text())["event_types"]


def schema_enum() -> list[str]:
    schema = json.loads((ROOT / "schemas" / "event.schema.json").read_text())
    return schema["properties"]["event_type"]["enum"]


class CommonsDictionaryTests(unittest.TestCase):
    """ADR-COMMONS-003 (DD-009 part 1): the fourteen new canonical types."""

    def test_all_fourteen_types_are_canonical(self):
        for name in COMMONS_TYPES:
            self.assertIn(name, dictionary())
            self.assertIn(name, schema_enum())

    def test_dictionary_and_schema_stay_in_lockstep(self):
        self.assertEqual(set(dictionary()), set(schema_enum()))

    def test_dictionary_version_bumped(self):
        version = json.loads((ROOT / "event.types.json").read_text())["version"]
        self.assertEqual(version, "0.4.0")

    def test_commons_consent_reuses_existing_types_no_duplicates(self):
        # The source's consent_granted/consent_revoked map onto the existing
        # canonical CONSENT_GRANTED/CONSENT_REVOKED (ADR-COMMONS-003 §2) --
        # no parallel COMMONS_CONSENT_* vocabulary may appear.
        self.assertIn("CONSENT_GRANTED", dictionary())
        self.assertIn("CONSENT_REVOKED", dictionary())
        for name in dictionary():
            self.assertFalse(name.startswith("COMMONS_"))

    def test_commons_event_validates_against_schema(self):
        registry = SchemaRegistry(str(ROOT / "schemas"))
        registry.validate("event.schema.json", {
            "id": "HOS-EVT-000001",
            "event_type": "CHALLENGE_JOINED",
            "occurred_at": "2026-08-17T12:00:00+00:00",
            "actor_id": "HOS-HUM-000001",
            "subject_ids": ["HOS-ENT-000001"],
            "payload": {"challenge_id": "HOS-ENT-000001"},
            "correlation_id": "HOS-COR-000001",
        })


class ChallengeRiskMappingTests(unittest.TestCase):
    """The R0-R4 mapping artifact transcribes the digest's SS7 constraints."""

    def setUp(self):
        self.mapping = json.loads(
            (ROOT / "policies" / "commons.challenge.risk.json").read_text(),
        )

    def test_all_five_constitutional_risk_classes_present(self):
        risks = [c["risk"] for c in self.mapping["classes"]]
        self.assertEqual(risks, ["R0", "R1", "R2", "R3", "R4"])

    def test_extreme_class_is_never_publishable_without_control(self):
        r4 = next(c for c in self.mapping["classes"] if c["risk"] == "R4")
        self.assertEqual(
            r4["publication"], "never_published_without_additional_control",
        )

    def test_sensitive_public_classes_require_risk_classification(self):
        for risk in ("R2", "R3"):
            entry = next(c for c in self.mapping["classes"] if c["risk"] == risk)
            self.assertIn("requires_risk_classification", entry["publication"])

    def test_mapping_references_only_canonical_event_types(self):
        canonical = set(dictionary())
        for entry in self.mapping["classes"]:
            for event_type in entry["events"]:
                self.assertIn(event_type, canonical)

    def test_mapping_is_founder_approved_and_attributed(self):
        # Signed 2026-08-17 ("Tak, róbmy to" -- class table shown verbatim);
        # an unattributed mapping must never pass again.
        self.assertIn("ZATWIERDZONE", self.mapping["status"])
        self.assertEqual(self.mapping["approved_by"], "founder (dudsi101-svg)")
        self.assertEqual(self.mapping["approved_at"], "2026-08-17")


if __name__ == "__main__":
    unittest.main()
