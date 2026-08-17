"""SQLite persistence for the Hub Entity/Relation registries.

Follows graph_store.py's pattern (one store class, explicit schema,
row_factory=Row). The registries themselves stay in-memory and unaware of
persistence; this store snapshots their full state and rebuilds them via
the registries' explicit ``restore`` constructors, so ids, timestamps,
merge provenance, and duplicate flags survive verbatim.

Snapshot semantics (not an event log): ``save_snapshot`` rewrites the
tables atomically with the registries' current state. Durable *history*
belongs to the event stores and the merge records -- which are part of the
snapshot -- not to this file.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from .hub_entity_registry import (
    EntityRegistry,
    HubEntity,
    HubEntityStatus,
    HubEntityType,
    HubRelation,
    HubRelationType,
    MergeRecord,
    RelationRegistry,
)


class SQLiteHubStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self._migrate()

    def _migrate(self) -> None:
        self.connection.executescript(
            '''
            CREATE TABLE IF NOT EXISTS hub_entities (
                entity_id TEXT PRIMARY KEY,
                entity_type TEXT NOT NULL,
                working_name TEXT NOT NULL,
                responsibility_owner_id TEXT NOT NULL,
                provenance_source TEXT NOT NULL,
                status TEXT NOT NULL,
                schema_version TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS hub_relations (
                relation_id TEXT PRIMARY KEY,
                relation_type TEXT NOT NULL,
                source_entity_id TEXT NOT NULL REFERENCES hub_entities(entity_id),
                target_entity_id TEXT NOT NULL REFERENCES hub_entities(entity_id),
                asserted_by TEXT NOT NULL,
                confidence REAL NOT NULL CHECK(confidence >= 0 AND confidence <= 1),
                valid_from TEXT NOT NULL,
                valid_to TEXT
            );

            CREATE INDEX IF NOT EXISTS idx_hub_relations_source
            ON hub_relations(source_entity_id);

            CREATE INDEX IF NOT EXISTS idx_hub_relations_target
            ON hub_relations(target_entity_id);

            CREATE TABLE IF NOT EXISTS hub_merges (
                merge_id TEXT PRIMARY KEY,
                keep_entity_id TEXT NOT NULL,
                retire_entity_id TEXT NOT NULL,
                reason TEXT NOT NULL,
                evidence TEXT NOT NULL,
                approved_by TEXT NOT NULL,
                occurred_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS hub_duplicate_flags (
                entity_a TEXT NOT NULL,
                entity_b TEXT NOT NULL,
                PRIMARY KEY (entity_a, entity_b)
            );
            '''
        )
        self.connection.commit()

    # -- write -----------------------------------------------------------

    def save_snapshot(
        self, entities: EntityRegistry, relations: RelationRegistry | None = None,
    ) -> None:
        """Atomically replace the persisted state with the registries'
        current state (merge records and duplicate flags included)."""
        with self.connection:
            self.connection.execute("DELETE FROM hub_relations")
            self.connection.execute("DELETE FROM hub_entities")
            self.connection.execute("DELETE FROM hub_merges")
            self.connection.execute("DELETE FROM hub_duplicate_flags")
            for e in entities.all_entities():
                self.connection.execute(
                    '''INSERT INTO hub_entities VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (e.entity_id, e.entity_type.value, e.working_name,
                     e.responsibility_owner_id, e.provenance_source,
                     e.status.value, e.schema_version, e.created_at, e.updated_at),
                )
            for m in entities.merge_records():
                self.connection.execute(
                    '''INSERT INTO hub_merges VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (m.merge_id, m.keep_entity_id, m.retire_entity_id,
                     m.reason, m.evidence, m.approved_by, m.occurred_at),
                )
            for a, b in entities.duplicate_pairs():
                self.connection.execute(
                    "INSERT INTO hub_duplicate_flags VALUES (?, ?)", (a, b),
                )
            if relations is not None:
                for r in relations.all_relations():
                    self.connection.execute(
                        '''INSERT INTO hub_relations VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                        (r.relation_id, r.relation_type.value,
                         r.source_entity_id, r.target_entity_id, r.asserted_by,
                         r.confidence, r.valid_from, r.valid_to),
                    )

    # -- read ------------------------------------------------------------

    def load_registries(self) -> tuple[EntityRegistry, RelationRegistry]:
        entities = [
            HubEntity(
                entity_id=row["entity_id"],
                entity_type=HubEntityType(row["entity_type"]),
                working_name=row["working_name"],
                responsibility_owner_id=row["responsibility_owner_id"],
                provenance_source=row["provenance_source"],
                status=HubEntityStatus(row["status"]),
                schema_version=row["schema_version"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
            for row in self.connection.execute("SELECT * FROM hub_entities")
        ]
        merges = [
            MergeRecord(
                merge_id=row["merge_id"],
                keep_entity_id=row["keep_entity_id"],
                retire_entity_id=row["retire_entity_id"],
                reason=row["reason"],
                evidence=row["evidence"],
                approved_by=row["approved_by"],
                occurred_at=row["occurred_at"],
            )
            for row in self.connection.execute("SELECT * FROM hub_merges")
        ]
        pairs = [
            (row["entity_a"], row["entity_b"])
            for row in self.connection.execute("SELECT * FROM hub_duplicate_flags")
        ]
        entity_registry = EntityRegistry.restore(
            entities=entities, merges=merges, duplicate_pairs=pairs,
        )
        relations = [
            HubRelation(
                relation_id=row["relation_id"],
                relation_type=HubRelationType(row["relation_type"]),
                source_entity_id=row["source_entity_id"],
                target_entity_id=row["target_entity_id"],
                asserted_by=row["asserted_by"],
                confidence=row["confidence"],
                valid_from=row["valid_from"],
                valid_to=row["valid_to"],
            )
            for row in self.connection.execute("SELECT * FROM hub_relations")
        ]
        relation_registry = RelationRegistry.restore(entity_registry, relations)
        return entity_registry, relation_registry

    def counts(self) -> dict[str, int]:
        result = {}
        for table in ["hub_entities", "hub_relations", "hub_merges", "hub_duplicate_flags"]:
            row = self.connection.execute(f"SELECT COUNT(*) AS total FROM {table}").fetchone()
            result[table] = int(row["total"])
        return result

    def close(self) -> None:
        self.connection.close()
