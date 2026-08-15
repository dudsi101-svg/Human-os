from __future__ import annotations

from collections.abc import Iterable
from copy import deepcopy
from typing import Any


def rebuild_entities(events: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    entities: dict[str, dict[str, Any]] = {}
    for event in events:
        event_type = event["event_type"]
        payload = event.get("payload", {})
        subjects = event.get("subject_ids", [])

        if event_type == "ENTITY_CREATED" and subjects:
            snapshot = payload.get("snapshot")
            if snapshot:
                entities[subjects[0]] = deepcopy(snapshot)

        elif event_type == "ENTITY_UPDATED" and subjects and subjects[0] in entities:
            entity = entities[subjects[0]]
            if "changes" in payload:
                entity.update(deepcopy(payload["changes"]))
            elif "to" in payload:
                entity["status"] = payload["to"]

        elif event_type == "ENTITY_ARCHIVED" and subjects and subjects[0] in entities:
            entities[subjects[0]]["status"] = "archived"

    return entities
