from __future__ import annotations

import uuid
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from enum import Enum


class HubEntityType(str, Enum):
    """MVP_IMPLEMENTED_SUBSET -- the six MVP entity types from the Hub
    Entity-First spec, §9.1. This is NOT the canonical Human OS entity
    ontology: the later Formal Entity & Relation Model (found 2026-08-15,
    source integrity correction pass) describes a much broader type set
    (IDENTITY, PROFILE, PROJECT, OUTCOME, TASK, WORKFLOW, ASSET, LOCATION,
    DOCUMENT, KNOWLEDGE_ITEM, SOURCE, RISK, METRIC, EVENT, POLICY,
    PERMISSION_GRANT, CONSENT, RELATION, REPRESENTATION, VERSION, AGENT,
    AUTOMATION, INTERACTION, COMMITMENT, CAPABILITY, and more). Do not treat
    these six values as complete, and do not map them onto the formal model's
    names (e.g. PERSON -> IDENTITY) by convenience -- that mapping needs its
    own source-grounded analysis before it is made.
    """

    PERSON = "PERSON"
    GOAL = "GOAL"
    KNOWLEDGE_CLAIM = "KNOWLEDGE_CLAIM"
    DECISION = "DECISION"
    EXPERIMENT = "EXPERIMENT"
    RESOURCE = "RESOURCE"


class HubEntityStatus(str, Enum):
    """The Hub's own five-state entity lifecycle (distinct from
    hos_engine.state_machine's entity.schema.json status enum — the two
    are kept separate per the founder review of 2026-08-15, Q8)."""

    PROPOSED = "PROPOSED"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    SUPERSEDED = "SUPERSEDED"
    ARCHIVED = "ARCHIVED"


class HubRelationType(str, Enum):
    """The relation verbs named in the Hub Entity-First spec, §4.

    This is the HUB_ENTITY_FIRST_RELATION_VOCAB_v0.1. A later, more formal
    vocabulary (FORMAL_ENTITY_RELATION_VOCAB_v0.1, from the Formal Entity &
    Relation Model found 2026-08-15) uses different English verb names
    (IS_A, PART_OF, CONTAINS, OWNS, CONTROLS, DEPENDS_ON, ...) with richer
    first-class metadata (directionality, status, provenance, created_by,
    validity, constraints, schema_version). The two vocabularies are not yet
    reconciled -- see docs/RELATION_VOCABULARY_CROSSWALK.md. Do not assume
    a 1:1 mapping between them without checking that document.
    """

    JEST_TYPEM = "jest_typem"
    NALEZY_DO = "należy_do"
    DOTYCZY = "dotyczy"
    POWSTAL_Z = "powstał_z"
    REPREZENTUJE = "reprezentuje"
    WSPIERA = "wspiera"
    PRZECZY = "przeczy"
    ZALEZY_OD = "zależy_od"
    POWODUJE = "powoduje"
    POPRZEDZA = "poprzedza"
    AKTUALIZUJE = "aktualizuje"
    ZASTEPUJE = "zastępuje"
    MIERZY = "mierzy"
    REALIZUJE = "realizuje"
    ZOSTAL_ZATWIERDZONY_PRZEZ = "został_zatwierdzony_przez"
    JEST_PRZECHOWYWANY_W = "jest_przechowywany_w"
    JEST_WIDOKIEM = "jest_widokiem"


@dataclass(frozen=True)
class HubEntity:
    entity_id: str
    entity_type: HubEntityType
    working_name: str
    responsibility_owner_id: str
    provenance_source: str
    status: HubEntityStatus = HubEntityStatus.PROPOSED
    schema_version: str = "0.1"
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass(frozen=True)
class MergeRecord:
    """Provenance for a manual entity merge -- who approved it, on what
    evidence, and why. Added 2026-08-15 (source integrity correction pass)
    so that "Entity A was merged into Entity B by X at T based on evidence E"
    can always be reconstructed; the merge itself never physically erases
    the retired entity or its history (see EntityRegistry.merge)."""

    merge_id: str
    keep_entity_id: str
    retire_entity_id: str
    reason: str
    evidence: str
    approved_by: str
    occurred_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass(frozen=True)
class HubRelation:
    relation_id: str
    relation_type: HubRelationType
    source_entity_id: str
    target_entity_id: str
    asserted_by: str
    confidence: float = 1.0
    valid_from: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    valid_to: str | None = None


class EntityRegistry:
    """Assigns identity to Byty (entities) and prevents accidental duplicates.

    First slice of HOS Hub (ADR-HUB-001, HOS Hub Model Entity-First v0.1 §5.1),
    covering the six MVP entity types. Duplicate resolution is explicit and
    manual per spec §9.1 -- this registry never auto-merges.
    """

    def __init__(self) -> None:
        self._entities: dict[str, HubEntity] = {}
        self._possible_duplicates: dict[str, set[str]] = {}
        self._merges: dict[str, MergeRecord] = {}

    def register(
        self,
        *,
        entity_type: HubEntityType,
        working_name: str,
        responsibility_owner_id: str,
        provenance_source: str,
    ) -> HubEntity:
        entity = HubEntity(
            entity_id="HOS-ENT-" + uuid.uuid4().hex[:12].upper(),
            entity_type=entity_type,
            working_name=working_name,
            responsibility_owner_id=responsibility_owner_id,
            provenance_source=provenance_source,
        )
        self._entities[entity.entity_id] = entity
        return entity

    def get(self, entity_id: str) -> HubEntity:
        return self._entities[entity_id]

    def all_entities(self) -> list[HubEntity]:
        """Every entity regardless of status -- exports must carry retired
        history too (nothing is ever physically erased)."""
        return list(self._entities.values())

    def transition(self, entity_id: str, status: HubEntityStatus) -> HubEntity:
        current = self._entities[entity_id]
        updated = replace(current, status=status, updated_at=datetime.now(UTC).isoformat())
        self._entities[entity_id] = updated
        return updated

    def flag_possible_duplicate(self, entity_id: str, other_entity_id: str) -> None:
        self._entities[entity_id]
        self._entities[other_entity_id]
        self._possible_duplicates.setdefault(entity_id, set()).add(other_entity_id)
        self._possible_duplicates.setdefault(other_entity_id, set()).add(entity_id)

    def possible_duplicates_of(self, entity_id: str) -> set[str]:
        return set(self._possible_duplicates.get(entity_id, set()))

    def merge(
        self,
        *,
        keep_entity_id: str,
        retire_entity_id: str,
        reason: str,
        evidence: str,
        approved_by: str,
    ) -> HubEntity:
        """Manually approved merge: retire_entity_id becomes SUPERSEDED by
        keep_entity_id. Requires reason/evidence/approved_by so the merge is
        always reconstructable later, per ADR-HUB-005 -- retired entities are
        never physically erased, and the merge itself is a recorded,
        attributed decision, not a silent status flip."""
        if keep_entity_id == retire_entity_id:
            raise ValueError("Cannot merge an entity into itself")
        self._entities[keep_entity_id]
        self.transition(retire_entity_id, HubEntityStatus.SUPERSEDED)
        record = MergeRecord(
            merge_id="HOS-MRG-" + uuid.uuid4().hex[:12].upper(),
            keep_entity_id=keep_entity_id,
            retire_entity_id=retire_entity_id,
            reason=reason,
            evidence=evidence,
            approved_by=approved_by,
        )
        self._merges[retire_entity_id] = record
        self._possible_duplicates.pop(retire_entity_id, None)
        for others in self._possible_duplicates.values():
            others.discard(retire_entity_id)
        return self._entities[keep_entity_id]

    def merge_record_for(self, retired_entity_id: str) -> MergeRecord | None:
        return self._merges.get(retired_entity_id)

    def merge_records(self) -> list[MergeRecord]:
        return list(self._merges.values())

    def duplicate_pairs(self) -> list[tuple[str, str]]:
        """Each flagged pair once, ordered (a < b)."""
        seen: set[tuple[str, str]] = set()
        for a, others in self._possible_duplicates.items():
            for b in others:
                seen.add((a, b) if a < b else (b, a))
        return sorted(seen)

    @classmethod
    def restore(
        cls,
        *,
        entities: list[HubEntity],
        merges: list[MergeRecord],
        duplicate_pairs: list[tuple[str, str]],
    ) -> EntityRegistry:
        """Rebuild a registry from persisted state (see hub_store). The
        explicit constructor exists so persistence layers never have to
        reach into private fields -- and so restored ids/timestamps are
        preserved verbatim instead of being re-minted by register()."""
        registry = cls()
        for entity in entities:
            registry._entities[entity.entity_id] = entity
        for record in merges:
            registry._merges[record.retire_entity_id] = record
        for a, b in duplicate_pairs:
            registry._possible_duplicates.setdefault(a, set()).add(b)
            registry._possible_duplicates.setdefault(b, set()).add(a)
        return registry

    def by_type(self, entity_type: HubEntityType) -> list[HubEntity]:
        return [e for e in self._entities.values() if e.entity_type == entity_type]


class RelationRegistry:
    """Records typed, evidenced, temporal relations between entities.

    First slice of HOS Hub (ADR-HUB-001, HOS Hub Model Entity-First v0.1 §5.2).
    Relations are first-class records, not tags: every relation carries its
    own confidence, validity window, and asserting author.
    """

    def __init__(self, entities: EntityRegistry) -> None:
        self._entities = entities
        self._relations: dict[str, HubRelation] = {}
        self._outgoing: dict[str, set[str]] = {}
        self._incoming: dict[str, set[str]] = {}

    def link(
        self,
        *,
        relation_type: HubRelationType,
        source_entity_id: str,
        target_entity_id: str,
        asserted_by: str,
        confidence: float = 1.0,
    ) -> HubRelation:
        self._entities.get(source_entity_id)
        self._entities.get(target_entity_id)
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        relation = HubRelation(
            relation_id="HOS-REL-" + uuid.uuid4().hex[:12].upper(),
            relation_type=relation_type,
            source_entity_id=source_entity_id,
            target_entity_id=target_entity_id,
            asserted_by=asserted_by,
            confidence=confidence,
        )
        self._relations[relation.relation_id] = relation
        self._outgoing.setdefault(source_entity_id, set()).add(relation.relation_id)
        self._incoming.setdefault(target_entity_id, set()).add(relation.relation_id)
        return relation

    def get(self, relation_id: str) -> HubRelation:
        return self._relations[relation_id]

    def outgoing(self, entity_id: str) -> list[HubRelation]:
        return [self._relations[rid] for rid in self._outgoing.get(entity_id, set())]

    def incoming(self, entity_id: str) -> list[HubRelation]:
        return [self._relations[rid] for rid in self._incoming.get(entity_id, set())]

    def orphans(self, entity_ids: list[str]) -> list[str]:
        """Entities with neither outgoing nor incoming relations -- flagged for review per §5.2."""
        return [
            eid for eid in entity_ids
            if not self._outgoing.get(eid) and not self._incoming.get(eid)
        ]

    def all_relations(self) -> list[HubRelation]:
        return list(self._relations.values())

    @classmethod
    def restore(
        cls, entities: EntityRegistry, relations: list[HubRelation],
    ) -> RelationRegistry:
        """Rebuild from persisted state; same rationale as
        EntityRegistry.restore (ids and validity windows kept verbatim)."""
        registry = cls(entities)
        for relation in relations:
            registry._relations[relation.relation_id] = relation
            registry._outgoing.setdefault(relation.source_entity_id, set()).add(relation.relation_id)
            registry._incoming.setdefault(relation.target_entity_id, set()).add(relation.relation_id)
        return registry
