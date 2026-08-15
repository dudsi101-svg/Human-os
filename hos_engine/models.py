
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Decision(str, Enum):
    APPROVED = "APPROVED"
    APPROVED_WITH_LIMITS = "APPROVED_WITH_LIMITS"
    REQUIRES_CONSENT = "REQUIRES_CONSENT"
    REQUIRES_HUMAN_DECISION = "REQUIRES_HUMAN_DECISION"
    REQUIRES_REDESIGN = "REQUIRES_REDESIGN"
    CONSTITUTIONAL_VIOLATION = "CONSTITUTIONAL_VIOLATION"


class TestResult(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"


@dataclass
class ProofTest:
    test_id: str
    name: str
    result: TestResult
    evidence: list[str] = field(default_factory=list)
    confidence: float = 1.0


@dataclass
class Proof:
    proof_id: str
    subject_id: str
    tests: list[ProofTest]
    final_status: Decision
    human_review_required: bool
    limitations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.proof_id,
            "subject_id": self.subject_id,
            "tests": [
                {
                    "test_id": t.test_id,
                    "name": t.name,
                    "result": t.result.value,
                    "evidence": t.evidence,
                    "confidence": t.confidence,
                }
                for t in self.tests
            ],
            "final_status": self.final_status.value,
            "human_review_required": self.human_review_required,
            "limitations": self.limitations,
        }
