from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any


def canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


class SQLiteEventStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self._migrate()

    def _migrate(self) -> None:
        self.connection.executescript(
            '''
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version INTEGER PRIMARY KEY,
                applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS events (
                sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT NOT NULL UNIQUE,
                event_type TEXT NOT NULL,
                occurred_at TEXT NOT NULL,
                actor_id TEXT NOT NULL,
                subject_ids TEXT NOT NULL,
                payload TEXT NOT NULL,
                correlation_id TEXT NOT NULL,
                causation_id TEXT,
                previous_hash TEXT,
                event_hash TEXT NOT NULL UNIQUE,
                immutable INTEGER NOT NULL CHECK (immutable = 1)
            );

            CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);
            CREATE INDEX IF NOT EXISTS idx_events_actor ON events(actor_id);
            '''
        )
        self.connection.execute(
            "INSERT OR IGNORE INTO schema_migrations(version) VALUES (1)"
        )
        self.connection.commit()

    def append(self, event: dict[str, Any]) -> str:
        if event.get("immutable") is not True:
            raise ValueError("Event must declare immutable=true.")

        previous_hash = self.latest_hash()
        material = dict(event)
        material["previous_hash"] = previous_hash
        event_hash = hashlib.sha256(canonical_json(material).encode("utf-8")).hexdigest()

        self.connection.execute(
            '''
            INSERT INTO events (
                event_id, event_type, occurred_at, actor_id, subject_ids, payload,
                correlation_id, causation_id, previous_hash, event_hash, immutable
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            ''',
            (
                event["id"],
                event["event_type"],
                event["occurred_at"],
                event["actor_id"],
                canonical_json({"values": event["subject_ids"]}),
                canonical_json(event["payload"]),
                event["correlation_id"],
                event.get("causation_id"),
                previous_hash,
                event_hash,
            ),
        )
        self.connection.commit()
        return event_hash

    def latest_hash(self) -> str | None:
        row = self.connection.execute(
            "SELECT event_hash FROM events ORDER BY sequence DESC LIMIT 1"
        ).fetchone()
        return None if row is None else str(row["event_hash"])

    def all(self) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            "SELECT * FROM events ORDER BY sequence"
        ).fetchall()
        return [self._decode(row) for row in rows]

    def verify_chain(self) -> bool:
        previous_hash: str | None = None
        for event in self.all():
            stored_hash = event.pop("event_hash")
            stored_previous = event.pop("previous_hash")
            if stored_previous != previous_hash:
                return False
            material = {
                "id": event["id"],
                "event_type": event["event_type"],
                "occurred_at": event["occurred_at"],
                "actor_id": event["actor_id"],
                "subject_ids": event["subject_ids"],
                "payload": event["payload"],
                "correlation_id": event["correlation_id"],
                "immutable": True,
                "previous_hash": previous_hash,
            }
            if event.get("causation_id") is not None:
                material["causation_id"] = event["causation_id"]
            calculated = hashlib.sha256(
                canonical_json(material).encode("utf-8")
            ).hexdigest()
            if calculated != stored_hash:
                return False
            previous_hash = stored_hash
        return True

    @staticmethod
    def _decode(row: sqlite3.Row) -> dict[str, Any]:
        subjects = json.loads(row["subject_ids"])["values"]
        return {
            "id": row["event_id"],
            "event_type": row["event_type"],
            "occurred_at": row["occurred_at"],
            "actor_id": row["actor_id"],
            "subject_ids": subjects,
            "payload": json.loads(row["payload"]),
            "correlation_id": row["correlation_id"],
            "causation_id": row["causation_id"],
            "previous_hash": row["previous_hash"],
            "event_hash": row["event_hash"],
            "immutable": True,
        }

    def close(self) -> None:
        self.connection.close()
