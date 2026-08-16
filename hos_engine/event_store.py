
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class EventStore:
    def __init__(self, path: str | Path | None = None) -> None:
        self.path = Path(path) if path else None
        self._events: list[dict[str, Any]] = []
        if self.path and self.path.exists():
            self._load()

    def append(self, event: dict[str, Any]) -> None:
        if not event.get("immutable", False):
            raise ValueError("Event must be immutable.")
        self._events.append(event)
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")

    def all(self) -> list[dict[str, Any]]:
        return list(self._events)

    def by_subject(self, subject_id: str) -> list[dict[str, Any]]:
        return [e for e in self._events if subject_id in e.get("subject_ids", [])]

    def _load(self) -> None:
        if self.path is None:
            return
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    self._events.append(json.loads(line))
