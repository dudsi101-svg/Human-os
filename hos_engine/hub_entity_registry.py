from __future__ import annotations

import uuid
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from enum import Enum


class HubEntityType(str, Enum):
    """The six MVP entity types from the Hub Entity-First spec, §9.1."""

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
    """The relation verbs named in the Hub Entity-First spec, §4."""

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

    def merge(self, *, keep_entity_id: str, retire_entity_id: str) -> HubEntity:
        """Manually approved merge: retire_entity_id becomes SUPERSEDED by keep_entity_id."""
        if keep_entity_id == retire_entity_id:
            raise ValueError("Cannot merge an entity into itself")
        self._entities[keep_entity_id]
        self.transition(retire_entity_id, HubEntityStatus.SUPERSEDED)
        self._possible_duplicates.pop(retire_entity_id, None)
        for others in self._possible_duplicates.values():
            others.discard(retire_entity_id)
        return self._entities[keep_entity_id]

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
