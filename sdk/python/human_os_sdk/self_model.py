"""Thin SDK exposure of the engine's conversational self model.

Deliberately a re-export, not a wrapper: the epistemic rules (declaration
vs hypothesis, user-only confirmation, tensions as signal, consent gating)
are engine guarantees and must not be reimplemented or softened at the SDK
layer. See docs/self-model-contract.md for the I/O contract.
"""

from hos_engine.self_model import (
    Interaction,
    InteractionLog,
    InteractionMessage,
    InteractionMode,
    MessageAuthor,
    SelfModelService,
    Tension,
    TensionStatus,
    confidence_band,
)

__all__ = [
    "Interaction",
    "InteractionLog",
    "InteractionMessage",
    "InteractionMode",
    "MessageAuthor",
    "SelfModelService",
    "Tension",
    "TensionStatus",
    "confidence_band",
]
