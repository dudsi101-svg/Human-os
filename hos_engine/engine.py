
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from .event_store import EventStore
from .flow import generative_flow_score
from .ids import IdGenerator
from .policy import ProofKernel
from .state_machine import transition


class HumanOSEngine:
    def __init__(self, event_store_path: str | None = None) -> None:
        self.ids = IdGenerator()
        self.events = EventStore(event_store_path)
        self.proof_kernel = ProofKernel()
        self.entities: dict[str, dict[str, Any]] = {}

    def register_entity(self, entity: dict[str, Any], actor_id: str) -> dict[str, Any]:
        entity_id = entity["id"]
        if entity_id in self.entities:
            raise ValueError(f"Entity already exists: {entity_id}")
        self.entities[entity_id] = dict(entity)
        self._emit("ENTITY_CREATED", actor_id, [entity_id], {"entity_type": entity.get("entity_type")})
        return self.entities[entity_id]

    def change_state(self, entity_id: str, target: str, actor_id: str) -> dict[str, Any]:
        entity = self.entities[entity_id]
        current = entity["status"]
        entity["status"] = transition(current, target)
        entity["updated_at"] = self._now()
        self._emit("ENTITY_UPDATED", actor_id, [entity_id], {"from": current, "to": target})
        return entity

    def evaluate_action(self, action: dict[str, Any], actor_id: str) -> dict[str, Any]:
        proof_id = self.ids.next("PRF")
        proof = self.proof_kernel.evaluate(action, proof_id)
        self._emit("PROOF_COMPLETED", actor_id, [action.get("id", "UNKNOWN")], proof.to_dict())
        return proof.to_dict()

    def record_flow(self, flow: dict[str, Any], actor_id: str) -> dict[str, Any]:
        flow = dict(flow)
        flow["generative_flow_score"] = generative_flow_score(flow)
        self.register_entity(flow, actor_id)
        self._emit("FLOW_RECORDED", actor_id, [flow["id"]], {"score": flow["generative_flow_score"]})
        return flow

    def disclose_limitation(self, subject_id: str, limitation: str, actor_id: str) -> None:
        self._emit("LIMITATION_DISCLOSED", actor_id, [subject_id], {"limitation": limitation})

    def _emit(self, event_type: str, actor_id: str, subject_ids: list[str], payload: dict[str, Any]) -> None:
        self.events.append({
            "id": self.ids.next("EVT"),
            "event_type": event_type,
            "occurred_at": self._now(),
            "actor_id": actor_id,
            "subject_ids": subject_ids,
            "payload": payload,
            "correlation_id": self.ids.next("COR"),
            "immutable": True,
        })

    @staticmethod
    def _now() -> str:
        return datetime.now(UTC).isoformat()
