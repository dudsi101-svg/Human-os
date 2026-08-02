
from __future__ import annotations
from typing import Dict, Set


ALLOWED_TRANSITIONS: Dict[str, Set[str]] = {
    "draft": {"active", "archived", "revoked"},
    "active": {"paused", "completed", "archived", "revoked"},
    "paused": {"active", "completed", "archived", "revoked"},
    "completed": {"archived"},
    "archived": set(),
    "revoked": set(),
}


def transition(current: str, target: str) -> str:
    allowed = ALLOWED_TRANSITIONS.get(current)
    if allowed is None:
        raise ValueError(f"Unknown state: {current}")
    if target not in allowed:
        raise ValueError(f"Invalid transition: {current} -> {target}")
    return target
