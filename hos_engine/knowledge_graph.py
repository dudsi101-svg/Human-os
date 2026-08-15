from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from itertools import pairwise
from typing import Any


class KnowledgeNodeType(str, Enum):
    """Layer 3's closed catalog of 13 knowledge-graph node types
    (ADR-KNOWLEDGE-003, source SS21.1). Adopting the catalog does not make
    it mandatory here: GraphNode.node_type stays a plain str for backward
    compatibility, and validate_against_catalog() below reports (never
    raises) departures, so existing untyped graphs keep working while new
    code can opt in."""

    CLAIM = "claim"
    SOURCE = "source"
    INTERVENTION = "intervention"
    PROTOCOL = "protocol"
    OUTCOME = "outcome"
    MECHANISM = "mechanism"
    RISK = "risk"
    CONTRAINDICATION = "contraindication"
    POPULATION = "population"
    METRIC = "metric"
    DOMAIN = "domain"
    USER_OR_COHORT = "user_or_cohort"
    VERSION_OR_EDITORIAL_DECISION = "version_or_editorial_decision"


class KnowledgeRelationType(str, Enum):
    """Layer 3's nine named edge relations (ADR-KNOWLEDGE-003, source
    SS21.2). Same opt-in posture as KnowledgeNodeType. Values keep the
    source's Polish verbs -- these are the canonical names, matching how
    hub_entity_registry.HubRelationType keeps the Hub spec's Polish verbs."""

    POPIERA = "popiera"
    OSLABIA = "osłabia"
    PRZECZY = "przeczy"
    WARUNKUJE = "warunkuje"
    WYJASNIA = "wyjaśnia"
    RYZYKUJE = "ryzykuje"
    WCHODZI_W_INTERAKCJE = "wchodzi_w_interakcje"
    JEST_WERSJA = "jest_wersja"
    WYNIKA_Z = "wynika_z"


@dataclass(frozen=True)
class CatalogViolation:
    """One departure from the Layer 3 catalog, reported by
    validate_against_catalog(). Reporting rather than raising follows the
    project-wide error contract (schema doc SS10): a conflict is surfaced
    explicitly, never silently corrected."""

    subject_id: str
    kind: str  # "node_type" or "relation_type"
    value: str


@dataclass(frozen=True)
class GraphNode:
    node_id: str
    node_type: str
    label: str
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GraphEdge:
    edge_id: str
    source_id: str
    target_id: str
    relation_type: str
    confidence: float = 1.0
    reversible: bool = False
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ProvenanceRecord:
    provenance_id: str
    subject_id: str
    source_type: str
    source_ref: str
    author_id: str | None
    observed_at: str
    confidence: float
    verification_status: str
    derivation_method: str
    limitations: tuple[str, ...] = ()


class KnowledgeGraph:
    def __init__(self) -> None:
        self._nodes: dict[str, GraphNode] = {}
        self._edges: dict[str, GraphEdge] = {}
        self._outgoing: dict[str, set[str]] = {}
        self._incoming: dict[str, set[str]] = {}
        self._provenance: dict[str, list[ProvenanceRecord]] = {}

    def add_node(self, node: GraphNode) -> None:
        if node.node_id in self._nodes:
            raise ValueError(f"Node already exists: {node.node_id}")
        self._nodes[node.node_id] = node
        self._outgoing[node.node_id] = set()
        self._incoming[node.node_id] = set()

    def add_edge(self, edge: GraphEdge) -> None:
        if edge.edge_id in self._edges:
            raise ValueError(f"Edge already exists: {edge.edge_id}")
        if edge.source_id not in self._nodes or edge.target_id not in self._nodes:
            raise ValueError("Both edge endpoints must exist.")
        if not 0.0 <= edge.confidence <= 1.0:
            raise ValueError("Edge confidence must be between 0 and 1.")
        self._edges[edge.edge_id] = edge
        self._outgoing[edge.source_id].add(edge.edge_id)
        self._incoming[edge.target_id].add(edge.edge_id)

    def add_provenance(self, record: ProvenanceRecord) -> None:
        if record.subject_id not in self._nodes and record.subject_id not in self._edges:
            raise ValueError(f"Unknown provenance subject: {record.subject_id}")
        if not 0.0 <= record.confidence <= 1.0:
            raise ValueError("Provenance confidence must be between 0 and 1.")
        self._provenance.setdefault(record.subject_id, []).append(record)

    def node(self, node_id: str) -> GraphNode:
        return self._nodes[node_id]

    def edge(self, edge_id: str) -> GraphEdge:
        return self._edges[edge_id]

    def neighbours(
        self,
        node_id: str,
        relation_type: str | None = None,
        direction: str = "outgoing",
    ) -> list[GraphNode]:
        if direction not in {"outgoing", "incoming", "both"}:
            raise ValueError("direction must be outgoing, incoming or both.")

        edge_ids: set[str] = set()
        if direction in {"outgoing", "both"}:
            edge_ids |= self._outgoing[node_id]
        if direction in {"incoming", "both"}:
            edge_ids |= self._incoming[node_id]

        result: dict[str, GraphNode] = {}
        for edge_id in edge_ids:
            edge = self._edges[edge_id]
            if relation_type and edge.relation_type != relation_type:
                continue
            other_id = edge.target_id if edge.source_id == node_id else edge.source_id
            result[other_id] = self._nodes[other_id]
        return list(result.values())

    def shortest_path(
        self,
        start_id: str,
        end_id: str,
        relation_types: set[str] | None = None,
    ) -> list[str] | None:
        if start_id == end_id:
            return [start_id]

        queue: list[tuple[str, list[str]]] = [(start_id, [start_id])]
        visited = {start_id}

        while queue:
            current, path = queue.pop(0)
            for edge_id in self._outgoing[current]:
                edge = self._edges[edge_id]
                if relation_types and edge.relation_type not in relation_types:
                    continue
                nxt = edge.target_id
                if nxt == end_id:
                    return path + [nxt]
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append((nxt, path + [nxt]))
        return None

    def confidence_of_path(self, node_path: list[str]) -> float:
        if len(node_path) < 2:
            return 1.0

        confidence = 1.0
        for source, target in pairwise(node_path):
            candidates = [
                self._edges[eid]
                for eid in self._outgoing[source]
                if self._edges[eid].target_id == target
            ]
            if not candidates:
                raise ValueError(f"No edge: {source} -> {target}")
            confidence *= max(edge.confidence for edge in candidates)
        return round(confidence, 6)

    def orphan_nodes(self) -> list[GraphNode]:
        return [
            node for node_id, node in self._nodes.items()
            if not self._incoming[node_id] and not self._outgoing[node_id]
        ]

    def has_directed_cycle(self) -> bool:
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(node_id: str) -> bool:
            if node_id in visiting:
                return True
            if node_id in visited:
                return False
            visiting.add(node_id)
            for edge_id in self._outgoing[node_id]:
                if visit(self._edges[edge_id].target_id):
                    return True
            visiting.remove(node_id)
            visited.add(node_id)
            return False

        return any(visit(node_id) for node_id in self._nodes if node_id not in visited)

    def provenance(self, subject_id: str) -> list[ProvenanceRecord]:
        return list(self._provenance.get(subject_id, []))

    def validate_against_catalog(self) -> list[CatalogViolation]:
        """Report every node/edge whose type is outside Layer 3's closed
        catalog (ADR-KNOWLEDGE-003). Purely diagnostic -- an empty list means
        the graph is catalog-conformant; a non-empty list is information for
        the caller, not an error."""
        node_types = {t.value for t in KnowledgeNodeType}
        relation_types = {t.value for t in KnowledgeRelationType}
        violations: list[CatalogViolation] = []
        for node in self._nodes.values():
            if node.node_type not in node_types:
                violations.append(CatalogViolation(node.node_id, "node_type", node.node_type))
        for edge in self._edges.values():
            if edge.relation_type not in relation_types:
                violations.append(CatalogViolation(edge.edge_id, "relation_type", edge.relation_type))
        return violations

    def export(self) -> dict[str, Any]:
        return {
            "nodes": [
                {
                    "id": n.node_id,
                    "type": n.node_type,
                    "label": n.label,
                    "properties": n.properties,
                }
                for n in self._nodes.values()
            ],
            "edges": [
                {
                    "id": e.edge_id,
                    "source_id": e.source_id,
                    "target_id": e.target_id,
                    "relation_type": e.relation_type,
                    "confidence": e.confidence,
                    "reversible": e.reversible,
                    "properties": e.properties,
                }
                for e in self._edges.values()
            ],
            "provenance": {
                subject_id: [
                    {
                        "id": p.provenance_id,
                        "source_type": p.source_type,
                        "source_ref": p.source_ref,
                        "author_id": p.author_id,
                        "observed_at": p.observed_at,
                        "confidence": p.confidence,
                        "verification_status": p.verification_status,
                        "derivation_method": p.derivation_method,
                        "limitations": list(p.limitations),
                    }
                    for p in records
                ]
                for subject_id, records in self._provenance.items()
            },
        }


def now_utc() -> str:
    return datetime.now(UTC).isoformat()
