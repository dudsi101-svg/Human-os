"""SQLite persistence for the Living Self Model.

Same snapshot semantics as hub_store.py: ``save_snapshot`` atomically
rewrites the persisted state of a ``SelfModelService`` (HumanModel records,
InteractionLog conversations and messages, tensions); ``load_service``
rebuilds a service via the explicit ``restore`` constructors, so record
ids, the supersedes chain, message quotes behind ``why()``, and tension
history all survive a process restart verbatim.

Division of labor: the *audit trail* of lifecycle transitions already goes
to an event store (hash chain) when one is wired into the service; this
store carries the *current state* so it does not have to be replayed.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .consent import ConsentRegistry
from .human_model import EvidenceType, HumanModel, HumanRecord, RecordStatus
from .self_model import (
    Interaction,
    InteractionLog,
    InteractionMessage,
    InteractionMode,
    MessageAuthor,
    SelfModelService,
    Tension,
    TensionStatus,
)


class SQLiteSelfModelStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self._migrate()

    def _migrate(self) -> None:
        self.connection.executescript(
            '''
            CREATE TABLE IF NOT EXISTS human_records (
                record_id TEXT PRIMARY KEY,
                subject_id TEXT NOT NULL,
                domain TEXT NOT NULL,
                key TEXT NOT NULL,
                value_json TEXT NOT NULL,
                evidence_type TEXT NOT NULL,
                confidence REAL NOT NULL CHECK(confidence >= 0 AND confidence <= 1),
                source_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                status TEXT NOT NULL,
                supersedes TEXT,
                sensitive INTEGER NOT NULL,
                tags_json TEXT NOT NULL,
                context TEXT, unit TEXT, quality TEXT, consent_scope TEXT,
                valid_from TEXT, valid_to TEXT, last_confirmed_at TEXT,
                evidence_refs_json TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_human_records_subject
            ON human_records(subject_id);

            CREATE TABLE IF NOT EXISTS interactions (
                interaction_id TEXT PRIMARY KEY,
                subject_id TEXT NOT NULL,
                mode TEXT NOT NULL,
                started_at TEXT NOT NULL,
                purpose TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS interaction_messages (
                message_id TEXT PRIMARY KEY,
                interaction_id TEXT NOT NULL REFERENCES interactions(interaction_id),
                author TEXT NOT NULL,
                text TEXT NOT NULL,
                at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_messages_interaction
            ON interaction_messages(interaction_id);

            CREATE TABLE IF NOT EXISTS tensions (
                tension_id TEXT PRIMARY KEY,
                subject_id TEXT NOT NULL,
                record_a TEXT NOT NULL,
                record_b TEXT NOT NULL,
                note TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                resolution TEXT
            );
            '''
        )
        self.connection.commit()

    def save_snapshot(self, service: SelfModelService) -> None:
        with self.connection:
            for table in ("interaction_messages", "interactions",
                          "human_records", "tensions"):
                self.connection.execute(f"DELETE FROM {table}")
            for r in service.model.all_records():
                self.connection.execute(
                    "INSERT INTO human_records VALUES "
                    "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (r.record_id, r.subject_id, r.domain, r.key,
                     json.dumps(r.value, ensure_ascii=False),
                     r.evidence_type.value, r.confidence, r.source_id,
                     r.created_at, r.status.value, r.supersedes,
                     int(r.sensitive),
                     json.dumps(sorted(r.tags), ensure_ascii=False),
                     r.context, r.unit, r.quality, r.consent_scope,
                     r.valid_from, r.valid_to, r.last_confirmed_at,
                     json.dumps(list(r.evidence_refs), ensure_ascii=False)),
                )
            for it in service.interactions.all_interactions():
                self.connection.execute(
                    "INSERT INTO interactions VALUES (?, ?, ?, ?, ?)",
                    (it.interaction_id, it.subject_id, it.mode.value,
                     it.started_at, it.purpose),
                )
            for m in service.interactions.all_messages():
                self.connection.execute(
                    "INSERT INTO interaction_messages VALUES (?, ?, ?, ?, ?)",
                    (m.message_id, m.interaction_id, m.author.value, m.text, m.at),
                )
            for t in service.all_tensions():
                self.connection.execute(
                    "INSERT INTO tensions VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (t.tension_id, t.subject_id, t.record_a, t.record_b,
                     t.note, t.status.value, t.created_at, t.resolution),
                )

    def load_service(
        self,
        *,
        consent: ConsentRegistry | None = None,
        grantee_id: str | None = None,
        event_store: Any = None,
    ) -> SelfModelService:
        records = [
            HumanRecord(
                record_id=row["record_id"], subject_id=row["subject_id"],
                domain=row["domain"], key=row["key"],
                value=json.loads(row["value_json"]),
                evidence_type=EvidenceType(row["evidence_type"]),
                confidence=row["confidence"], source_id=row["source_id"],
                created_at=row["created_at"],
                status=RecordStatus(row["status"]),
                supersedes=row["supersedes"], sensitive=bool(row["sensitive"]),
                tags=set(json.loads(row["tags_json"])),
                context=row["context"], unit=row["unit"], quality=row["quality"],
                consent_scope=row["consent_scope"], valid_from=row["valid_from"],
                valid_to=row["valid_to"], last_confirmed_at=row["last_confirmed_at"],
                evidence_refs=tuple(json.loads(row["evidence_refs_json"])),
            )
            for row in self.connection.execute("SELECT * FROM human_records")
        ]
        interactions = [
            Interaction(
                interaction_id=row["interaction_id"], subject_id=row["subject_id"],
                mode=InteractionMode(row["mode"]), started_at=row["started_at"],
                purpose=row["purpose"],
            )
            for row in self.connection.execute("SELECT * FROM interactions")
        ]
        messages = [
            InteractionMessage(
                message_id=row["message_id"], interaction_id=row["interaction_id"],
                author=MessageAuthor(row["author"]), text=row["text"], at=row["at"],
            )
            for row in self.connection.execute("SELECT * FROM interaction_messages")
        ]
        service = SelfModelService(
            model=HumanModel.restore(records),
            interactions=InteractionLog.restore(interactions, messages),
            consent=consent, grantee_id=grantee_id, event_store=event_store,
        )
        for row in self.connection.execute("SELECT * FROM tensions"):
            service.restore_tension(Tension(
                tension_id=row["tension_id"], subject_id=row["subject_id"],
                record_a=row["record_a"], record_b=row["record_b"],
                note=row["note"], status=TensionStatus(row["status"]),
                created_at=row["created_at"], resolution=row["resolution"],
            ))
        return service

    def counts(self) -> dict[str, int]:
        result = {}
        for table in ["human_records", "interactions", "interaction_messages", "tensions"]:
            row = self.connection.execute(f"SELECT COUNT(*) AS total FROM {table}").fetchone()
            result[table] = int(row["total"])
        return result

    def close(self) -> None:
        self.connection.close()
