
from __future__ import annotations

from typing import Any

from .models import Decision, Proof, ProofTest, TestResult

SEVERITY = {
    Decision.APPROVED: 0,
    Decision.APPROVED_WITH_LIMITS: 1,
    Decision.REQUIRES_CONSENT: 2,
    Decision.REQUIRES_HUMAN_DECISION: 3,
    Decision.REQUIRES_REDESIGN: 4,
    Decision.CONSTITUTIONAL_VIOLATION: 5,
}


class ProofKernel:
    def evaluate(self, subject: dict[str, Any], proof_id: str) -> Proof:
        tests: list[ProofTest] = []

        author_id = subject.get("responsibility_owner_id") or subject.get("author_id")
        if author_id:
            tests.append(ProofTest("PROOF-001", "Test autorstwa", TestResult.PASS, ["Human author/responsibility owner is explicit."]))
        else:
            tests.append(ProofTest("PROOF-001", "Test autorstwa", TestResult.FAIL, ["No explicit human author or responsibility owner."]))

        autonomy = subject.get("predicted_effects", {}).get("autonomy", 0.0)
        if autonomy < -0.2:
            tests.append(ProofTest("PROOF-002", "Test autonomii", TestResult.FAIL, [f"Predicted autonomy impact: {autonomy}"]))
        elif autonomy < 0:
            tests.append(ProofTest("PROOF-002", "Test autonomii", TestResult.WARN, [f"Predicted autonomy impact: {autonomy}"]))
        else:
            tests.append(ProofTest("PROOF-002", "Test autonomii", TestResult.PASS, [f"Predicted autonomy impact: {autonomy}"]))

        generativity = subject.get("predicted_effects", {}).get("generativity")
        if generativity is None:
            tests.append(ProofTest("PROOF-003", "Test generatywności", TestResult.UNKNOWN, ["No generativity estimate."]))
        elif generativity < 0.2:
            tests.append(ProofTest("PROOF-003", "Test generatywności", TestResult.WARN, [f"Generativity: {generativity}"]))
        else:
            tests.append(ProofTest("PROOF-003", "Test generatywności", TestResult.PASS, [f"Generativity: {generativity}"]))

        extraction = subject.get("predicted_effects", {}).get("extraction", 0.0)
        if extraction > 0.5:
            tests.append(ProofTest("PROOF-004", "Test ekstrakcji", TestResult.FAIL, [f"Extraction risk: {extraction}"]))
        elif extraction > 0.2:
            tests.append(ProofTest("PROOF-004", "Test ekstrakcji", TestResult.WARN, [f"Extraction risk: {extraction}"]))
        else:
            tests.append(ProofTest("PROOF-004", "Test ekstrakcji", TestResult.PASS, [f"Extraction risk: {extraction}"]))

        consent = subject.get("consent")
        if consent is True:
            tests.append(ProofTest("PROOF-005", "Test zgody", TestResult.PASS, ["Consent confirmed."]))
        elif consent is False:
            tests.append(ProofTest("PROOF-005", "Test zgody", TestResult.FAIL, ["Consent denied."]))
        else:
            tests.append(ProofTest("PROOF-005", "Test zgody", TestResult.UNKNOWN, ["Consent not recorded."]))

        reversibility = subject.get("reversibility", 0.0)
        if reversibility < 0.2:
            tests.append(ProofTest("PROOF-006", "Test odwracalności", TestResult.FAIL, [f"Reversibility: {reversibility}"]))
        elif reversibility < 0.5:
            tests.append(ProofTest("PROOF-006", "Test odwracalności", TestResult.WARN, [f"Reversibility: {reversibility}"]))
        else:
            tests.append(ProofTest("PROOF-006", "Test odwracalności", TestResult.PASS, [f"Reversibility: {reversibility}"]))

        dependency = subject.get("predicted_effects", {}).get("degrading_system_dependency", 0.0)
        if dependency > 0.4:
            tests.append(ProofTest("PROOF-007", "Test zależności od systemów degradujących", TestResult.FAIL, [f"Dependency increase: {dependency}"]))
        elif dependency > 0:
            tests.append(ProofTest("PROOF-007", "Test zależności od systemów degradujących", TestResult.WARN, [f"Dependency increase: {dependency}"]))
        else:
            tests.append(ProofTest("PROOF-007", "Test zależności od systemów degradujących", TestResult.PASS, [f"Dependency impact: {dependency}"]))

        portability = subject.get("portability", 0.0)
        exit_cost = subject.get("exit_cost", 0.0)
        if portability < 0.3 or exit_cost > 0.7:
            tests.append(ProofTest("PROOF-008", "Test przenośności i wyjścia", TestResult.FAIL, [f"Portability: {portability}; exit cost: {exit_cost}"]))
        elif portability < 0.6 or exit_cost > 0.4:
            tests.append(ProofTest("PROOF-008", "Test przenośności i wyjścia", TestResult.WARN, [f"Portability: {portability}; exit cost: {exit_cost}"]))
        else:
            tests.append(ProofTest("PROOF-008", "Test przenośności i wyjścia", TestResult.PASS, [f"Portability: {portability}; exit cost: {exit_cost}"]))

        limitations = subject.get("limitations")
        if limitations:
            tests.append(ProofTest("PROOF-009", "Test transparentności ograniczeń", TestResult.PASS, ["Limitations disclosed."]))
        else:
            tests.append(ProofTest("PROOF-009", "Test transparentności ograniczeń", TestResult.WARN, ["No limitations disclosed."]))

        decision = self._aggregate(tests)
        human_review_required = decision in {
            Decision.REQUIRES_HUMAN_DECISION,
            Decision.REQUIRES_REDESIGN,
            Decision.CONSTITUTIONAL_VIOLATION,
        }
        return Proof(
            proof_id=proof_id,
            subject_id=subject.get("id", "UNKNOWN"),
            tests=tests,
            final_status=decision,
            human_review_required=human_review_required,
            limitations=[
                "Rule thresholds are normative design assumptions, not empirical truth.",
                "Runtime evaluates declared inputs; it cannot verify whether declarations are honest."
            ],
        )

    def _aggregate(self, tests: list[ProofTest]) -> Decision:
        by_id = {t.test_id: t for t in tests}

        if by_id["PROOF-004"].result == TestResult.FAIL:
            return Decision.CONSTITUTIONAL_VIOLATION
        if by_id["PROOF-005"].result == TestResult.FAIL:
            return Decision.REQUIRES_CONSENT
        if by_id["PROOF-001"].result == TestResult.FAIL:
            return Decision.REQUIRES_HUMAN_DECISION
        if any(by_id[x].result == TestResult.FAIL for x in ["PROOF-002", "PROOF-006", "PROOF-008"]):
            return Decision.REQUIRES_REDESIGN
        if by_id["PROOF-007"].result == TestResult.FAIL:
            return Decision.APPROVED_WITH_LIMITS
        if any(t.result in {TestResult.WARN, TestResult.UNKNOWN} for t in tests):
            return Decision.APPROVED_WITH_LIMITS
        return Decision.APPROVED
