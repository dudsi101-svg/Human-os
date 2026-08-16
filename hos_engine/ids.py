
from __future__ import annotations

from collections import defaultdict


class IdGenerator:
    def __init__(self) -> None:
        self._counters: defaultdict[str, int] = defaultdict(int)

    def next(self, prefix: str) -> str:
        self._counters[prefix] += 1
        return f"HOS-{prefix}-{self._counters[prefix]:06d}"
