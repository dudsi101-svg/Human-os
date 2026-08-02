
from __future__ import annotations
from typing import Dict


def generative_flow_score(flow: Dict[str, float]) -> float:
    positive = (
        flow.get("gain", 0.0)
        * flow.get("reciprocity", 0.0)
        * flow.get("consent", 0.0)
        * flow.get("durability", 0.0)
        * flow.get("generativity", 0.0)
    )
    penalties = (
        flow.get("extraction", 0.0)
        + max(flow.get("dependency_effect", 0.0), 0.0)
        + flow.get("externalities", {}).get("negative", 0.0)
    )
    bonus = (
        max(-flow.get("dependency_effect", 0.0), 0.0)
        + flow.get("externalities", {}).get("positive", 0.0)
    ) * 0.25
    raw = positive + bonus - penalties
    return round(max(-1.0, min(1.0, raw)), 4)
