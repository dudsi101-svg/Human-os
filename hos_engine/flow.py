
from __future__ import annotations


def generative_flow_score(flow: dict[str, object]) -> float:
    def num(key: str) -> float:
        value = flow.get(key, 0.0)
        return float(value) if isinstance(value, (int, float)) else 0.0

    def ext(key: str) -> float:
        externalities = flow.get("externalities", {})
        if not isinstance(externalities, dict):
            return 0.0
        value = externalities.get(key, 0.0)
        return float(value) if isinstance(value, (int, float)) else 0.0

    positive = (
        num("gain") * num("reciprocity") * num("consent")
        * num("durability") * num("generativity")
    )
    penalties = num("extraction") + max(num("dependency_effect"), 0.0) + ext("negative")
    bonus = (max(-num("dependency_effect"), 0.0) + ext("positive")) * 0.25
    raw = positive + bonus - penalties
    return round(max(-1.0, min(1.0, raw)), 4)
