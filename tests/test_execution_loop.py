import tempfile
import unittest
from pathlib import Path

from hos_engine.agent_runtime import (
    AgentManifest,
    AgentRegistry,
    AgentRuntime,
    ApprovalMode,
    Capability,
    CapabilityRegistry,
    RiskLevel,
)
from hos_engine.authority import AuthorityRole, RoleGrantRegistry
from hos_engine.consent import ConsentRegistry
from hos_engine.event_store import EventStore
from hos_engine.execution_loop import ExecutionLoop, HumanIntent, IntentOutcome
from hos_engine.hos_core import ContextManager, EventEngine
from hos_engine.hub_entity_registry import (
    EntityRegistry,
    HubEntityStatus,
    HubEntityType,
    HubRelationType,
    RelationRegistry,
)
from hos_engine.policy import ProofKernel
from hos_engine.security_identity import IdentityRegistry, IdentityType
from hos_engine.sqlite_store import SQLiteEventStore

SUBJECT_ID = "HOS-HUM-000001"
AGENT_ID = "HOS-AGT-000001"
CAPABILITY_ID = "CAP-DRAFT-DOC"
PURPOSE = "drafting"
DOMAIN = "*"
ACTION = "draft_document"


class ExecutionLoopTests(unittest.TestCase):
    def setUp(self):
        self.identities = IdentityRegistry()
        self.identities.register_identity(identity_type=IdentityType.HUMAN, display_name="Founder", owner_id=SUBJECT_ID, identity_id=SUBJECT_ID)

        self.roles = RoleGrantRegistry()
        self.roles.grant(identity_id=SUBJECT_ID, role=AuthorityRole.OWNER, scope="*", issued_by=SUBJECT_ID)

        self.consents = ConsentRegistry()
        self.consents.grant(
            subject_id=SUBJECT_ID, grantee_id=AGENT_ID,
            purposes={PURPOSE}, domains={DOMAIN}, actions={ACTION},
        )

        self.contexts = ContextManager()

        self.entities = EntityRegistry()
        self.entity = self.entities.register(
            entity_type=HubEntityType.RESOURCE, working_name="Draft report",
            responsibility_owner_id=SUBJECT_ID, provenance_source="test",
        )
        self.goal = self.entities.register(
            entity_type=HubEntityType.GOAL, working_name="Ship the founder review",
            responsibility_owner_id=SUBJECT_ID, provenance_source="test",
        )
        self.relations = RelationRegistry(self.entities)

        self.capabilities = CapabilityRegistry()
        self.capabilities.register(Capability(
            capability_id=CAPABILITY_ID, action=ACTION, resource_scope="*",
            risk_level=RiskLevel.LOW, approval_mode=ApprovalMode.AUTOMATIC,
        ))
        self.agents = AgentRegistry()
        self.agents.register(AgentManifest(
            agent_id=AGENT_ID, name="Drafting Agent", purpose="drafts documents",
            owner_id=SUBJECT_ID, capabilities={CAPABILITY_ID},
        ))
        self.agent_runtime = AgentRuntime(self.capabilities, self.agents)
        self.agent_runtime.register_tool(CAPABILITY_ID, lambda args: "drafted")

        self.proof_kernel = ProofKernel()
        self.events = EventEngine()
        self.event_store = EventStore()

        self.loop = ExecutionLoop(
            identities=self.identities, roles=self.roles, consents=self.consents,
            contexts=self.contexts, entities=self.entities, proof_kernel=self.proof_kernel,
            agent_runtime=self.agent_runtime, events=self.events, event_store=self.event_store,
            relations=self.relations,
        )

    def _intent(self, **overrides):
        base = {
            "subject_id": SUBJECT_ID, "agent_id": AGENT_ID, "capability_id": CAPABILITY_ID,
            "action": ACTION, "resource_entity_id": self.entity.entity_id,
            "purpose": PURPOSE, "domain": DOMAIN, "required_role": AuthorityRole.OWNER,
            "predicted_effects": {"autonomy": 0.2, "generativity": 0.6, "extraction": 0.05},
            "reversibility": 0.9, "portability": 0.8, "exit_cost": 0.1,
        }
        base.update(overrides)
        return HumanIntent(**base)

    def test_happy_path_executes_and_produces_full_audit_trail(self):
        result = self.loop.execute(self._intent())

        self.assertEqual(result.outcome, IntentOutcome.EXECUTED)
        self.assertIsNotNone(result.context)
        self.assertIsNotNone(result.proof)
        self.assertEqual(result.receipt.status, "EXECUTED")
        self.assertTrue(len(result.audit_events) >= 3)  # PROPOSED, IN_PROGRESS, COMPLETED

        # STATE UPDATE actually happened
        self.assertEqual(self.entities.get(self.entity.entity_id).status, HubEntityStatus.ACTIVE)

        # durable domain event was recorded
        domain_events = self.event_store.by_subject(self.entity.entity_id)
        self.assertEqual(len(domain_events), 1)
        self.assertEqual(domain_events[0]["event_type"], "EXECUTION_COMPLETED")

    def test_no_relation_recorded_when_fulfills_entity_not_named(self):
        result = self.loop.execute(self._intent())
        self.assertIsNone(result.relation)
        self.assertEqual(self.relations.outgoing(self.entity.entity_id), [])

    def test_successful_execution_records_realizuje_relation_to_goal(self):
        result = self.loop.execute(self._intent(fulfills_entity_id=self.goal.entity_id))

        self.assertEqual(result.outcome, IntentOutcome.EXECUTED)
        self.assertIsNotNone(result.relation)
        self.assertEqual(result.relation.relation_type, HubRelationType.REALIZUJE)
        self.assertEqual(result.relation.source_entity_id, self.entity.entity_id)
        self.assertEqual(result.relation.target_entity_id, self.goal.entity_id)
        self.assertEqual(result.relation.asserted_by, SUBJECT_ID)

        outgoing = self.relations.outgoing(self.entity.entity_id)
        self.assertEqual(len(outgoing), 1)
        self.assertEqual(outgoing[0].relation_id, result.relation.relation_id)

    def test_refuses_unknown_fulfills_entity_before_anything_executes(self):
        result = self.loop.execute(self._intent(fulfills_entity_id="HOS-ENT-DOESNOTEXIST"))

        self.assertEqual(result.outcome, IntentOutcome.REFUSED_ENTITY_NOT_FOUND)
        # nothing downstream happened: no state change, no relation, no receipt
        self.assertEqual(self.entities.get(self.entity.entity_id).status, HubEntityStatus.PROPOSED)
        self.assertIsNone(result.receipt)
        self.assertEqual(self.relations.outgoing(self.entity.entity_id), [])

    def test_refuses_unknown_identity(self):
        result = self.loop.execute(self._intent(subject_id="HOS-HUM-999999"))
        self.assertEqual(result.outcome, IntentOutcome.REFUSED_IDENTITY)
        self.assertIsNone(result.context)

    def test_refuses_suspended_identity(self):
        self.identities.suspend(SUBJECT_ID)
        result = self.loop.execute(self._intent())
        self.assertEqual(result.outcome, IntentOutcome.REFUSED_IDENTITY)

    def test_refuses_missing_authority_role(self):
        result = self.loop.execute(self._intent(required_role=AuthorityRole.RECOVERY_CUSTODIAN))
        self.assertEqual(result.outcome, IntentOutcome.REFUSED_AUTHORITY)

    def test_refuses_missing_consent(self):
        result = self.loop.execute(self._intent(purpose="unrelated_purpose"))
        self.assertEqual(result.outcome, IntentOutcome.REFUSED_CONSENT)

    def test_refuses_unknown_entity(self):
        result = self.loop.execute(self._intent(resource_entity_id="HOS-ENT-DOESNOTEXIST"))
        self.assertEqual(result.outcome, IntentOutcome.REFUSED_ENTITY_NOT_FOUND)
        # context was still snapshotted before the entity lookup failed
        self.assertIsNotNone(result.context)

    def test_refuses_on_constitutional_violation(self):
        result = self.loop.execute(self._intent(predicted_effects={"autonomy": 0.1, "generativity": 0.5, "extraction": 0.9}))
        self.assertEqual(result.outcome, IntentOutcome.REFUSED_CONSTITUTIONAL)
        self.assertIsNotNone(result.proof)
        self.assertEqual(result.proof.final_status.value, "CONSTITUTIONAL_VIOLATION")
        # never reached agent execution -- entity was not touched
        self.assertEqual(self.entities.get(self.entity.entity_id).status, HubEntityStatus.PROPOSED)

    def test_requires_human_approval_when_capability_demands_it(self):
        self.capabilities.register(Capability(
            capability_id="CAP-HIGH-RISK", action="delete_all", resource_scope="*",
            risk_level=RiskLevel.HIGH, approval_mode=ApprovalMode.HUMAN_REQUIRED,
        ))
        self.agents.register(AgentManifest(
            agent_id="HOS-AGT-000002", name="Risky Agent", purpose="does risky things",
            owner_id=SUBJECT_ID, capabilities={"CAP-HIGH-RISK"},
        ))
        self.agent_runtime.register_tool("CAP-HIGH-RISK", lambda args: "done")
        self.consents.grant(subject_id=SUBJECT_ID, grantee_id="HOS-AGT-000002", purposes={PURPOSE}, domains={DOMAIN}, actions={"delete_all"})

        result = self.loop.execute(self._intent(agent_id="HOS-AGT-000002", capability_id="CAP-HIGH-RISK", action="delete_all"))
        self.assertEqual(result.outcome, IntentOutcome.REQUIRES_HUMAN_APPROVAL)
        # not executed, entity untouched
        self.assertEqual(self.entities.get(self.entity.entity_id).status, HubEntityStatus.PROPOSED)

    def test_agent_denial_surfaces_as_failed_with_domain_event(self):
        result = self.loop.execute(self._intent(action="draft_document", capability_id=CAPABILITY_ID, arguments={}, resource_entity_id=self.entity.entity_id))
        # sanity: happy path still works with this helper before we break it below
        self.assertEqual(result.outcome, IntentOutcome.EXECUTED)

        # now make the capability's resource scope exclude the entity to force a DENIED receipt
        self.capabilities.register(Capability(
            capability_id="CAP-SCOPED", action="draft_document", resource_scope="only-this-resource",
            risk_level=RiskLevel.LOW, approval_mode=ApprovalMode.AUTOMATIC,
        ))
        self.agents.register(AgentManifest(
            agent_id="HOS-AGT-000003", name="Scoped Agent", purpose="scoped",
            owner_id=SUBJECT_ID, capabilities={"CAP-SCOPED"},
        ))
        self.agent_runtime.register_tool("CAP-SCOPED", lambda args: "n/a")
        self.consents.grant(subject_id=SUBJECT_ID, grantee_id="HOS-AGT-000003", purposes={PURPOSE}, domains={DOMAIN}, actions={ACTION})

        denied = self.loop.execute(self._intent(agent_id="HOS-AGT-000003", capability_id="CAP-SCOPED"))
        self.assertEqual(denied.outcome, IntentOutcome.FAILED)
        self.assertEqual(denied.receipt.status, "DENIED")
        domain_events = [e for e in self.event_store.all() if e["payload"]["intent_id"] == denied.intent_id]
        self.assertEqual(len(domain_events), 1)
        self.assertEqual(domain_events[0]["event_type"], "EXECUTION_DENIED")


class ExecutionLoopSQLiteProvenanceTests(unittest.TestCase):
    """Same loop, but backed by SQLiteEventStore instead of the plain
    EventStore -- proves ExecutionLoop's event_store port works with the
    project's actual tamper-evidence mechanism (hash chain), not just an
    in-memory list. Closes the "event persistence" and "provenance" items
    from the founder continuation directive's Phase 3 progressive-
    integration list."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.event_store = SQLiteEventStore(Path(self.tmpdir.name) / "events.db")

        self.identities = IdentityRegistry()
        self.identities.register_identity(identity_type=IdentityType.HUMAN, display_name="Founder", owner_id=SUBJECT_ID, identity_id=SUBJECT_ID)
        self.roles = RoleGrantRegistry()
        self.roles.grant(identity_id=SUBJECT_ID, role=AuthorityRole.OWNER, scope="*", issued_by=SUBJECT_ID)
        self.consents = ConsentRegistry()
        self.consents.grant(subject_id=SUBJECT_ID, grantee_id=AGENT_ID, purposes={PURPOSE}, domains={DOMAIN}, actions={ACTION})
        self.contexts = ContextManager()
        self.entities = EntityRegistry()
        self.entity_a = self.entities.register(entity_type=HubEntityType.RESOURCE, working_name="Draft A", responsibility_owner_id=SUBJECT_ID, provenance_source="test")
        self.entity_b = self.entities.register(entity_type=HubEntityType.RESOURCE, working_name="Draft B", responsibility_owner_id=SUBJECT_ID, provenance_source="test")
        self.capabilities = CapabilityRegistry()
        self.capabilities.register(Capability(capability_id=CAPABILITY_ID, action=ACTION, resource_scope="*", risk_level=RiskLevel.LOW, approval_mode=ApprovalMode.AUTOMATIC))
        self.agents = AgentRegistry()
        self.agents.register(AgentManifest(agent_id=AGENT_ID, name="Drafting Agent", purpose="drafts documents", owner_id=SUBJECT_ID, capabilities={CAPABILITY_ID}))
        self.agent_runtime = AgentRuntime(self.capabilities, self.agents)
        self.agent_runtime.register_tool(CAPABILITY_ID, lambda args: "drafted")
        self.proof_kernel = ProofKernel()
        self.events = EventEngine()

        self.loop = ExecutionLoop(
            identities=self.identities, roles=self.roles, consents=self.consents,
            contexts=self.contexts, entities=self.entities, proof_kernel=self.proof_kernel,
            agent_runtime=self.agent_runtime, events=self.events, event_store=self.event_store,
        )

    def tearDown(self):
        self.event_store.close()
        self.tmpdir.cleanup()

    def _intent(self, resource_entity_id):
        return HumanIntent(
            subject_id=SUBJECT_ID, agent_id=AGENT_ID, capability_id=CAPABILITY_ID,
            action=ACTION, resource_entity_id=resource_entity_id,
            purpose=PURPOSE, domain=DOMAIN, required_role=AuthorityRole.OWNER,
            predicted_effects={"autonomy": 0.2, "generativity": 0.6, "extraction": 0.05},
            reversibility=0.9, portability=0.8, exit_cost=0.1,
        )

    def test_executions_persist_to_sqlite_with_a_verifiable_hash_chain(self):
        first = self.loop.execute(self._intent(self.entity_a.entity_id))
        second = self.loop.execute(self._intent(self.entity_b.entity_id))

        self.assertEqual(first.outcome, IntentOutcome.EXECUTED)
        self.assertEqual(second.outcome, IntentOutcome.EXECUTED)

        stored = self.event_store.all()
        self.assertEqual(len(stored), 2)
        self.assertTrue(self.event_store.verify_chain())

        # each event's previous_hash correctly links to the one before it
        self.assertIsNone(stored[0]["previous_hash"])
        self.assertEqual(stored[1]["previous_hash"], stored[0]["event_hash"])

    def test_refused_intents_never_reach_the_hash_chain(self):
        self.loop.execute(self._intent("HOS-ENT-DOESNOTEXIST"))  # REFUSED_ENTITY_NOT_FOUND
        self.assertEqual(self.event_store.all(), [])
        self.assertTrue(self.event_store.verify_chain())


if __name__ == "__main__":
    unittest.main()
