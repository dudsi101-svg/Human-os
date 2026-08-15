from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from .knowledge_graph import GraphEdge, GraphNode, ProvenanceRecord


class SQLiteGraphStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self._migrate()

    def _migrate(self) -> None:
        self.connection.executescript(
            '''
            CREATE TABLE IF NOT EXISTS graph_nodes (
                node_id TEXT PRIMARY KEY,
                node_type TEXT NOT NULL,
                label TEXT NOT NULL,
                properties_json TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS graph_edges (
                edge_id TEXT PRIMARY KEY,
                source_id TEXT NOT NULL REFERENCES graph_nodes(node_id),
                target_id TEXT NOT NULL REFERENCES graph_nodes(node_id),
                relation_type TEXT NOT NULL,
                confidence REAL NOT NULL CHECK(confidence >= 0 AND confidence <= 1),
                reversible INTEGER NOT NULL,
                properties_json TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_graph_edges_source
            ON graph_edges(source_id);

            CREATE INDEX IF NOT EXISTS idx_graph_edges_target
            ON graph_edges(target_id);

            CREATE TABLE IF NOT EXISTS provenance_records (
                provenance_id TEXT PRIMARY KEY,
                subject_id TEXT NOT NULL,
                source_type TEXT NOT NULL,
                source_ref TEXT NOT NULL,
                author_id TEXT,
                observed_at TEXT NOT NULL,
                confidence REAL NOT NULL CHECK(confidence >= 0 AND confidence <= 1),
                verification_status TEXT NOT NULL,
                derivation_method TEXT NOT NULL,
                limitations_json TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_provenance_subject
            ON provenance_records(subject_id);
            '''
        )
        self.connection.commit()

    def save_node(self, node: GraphNode) -> None:
        self.connection.execute(
            '''
            INSERT INTO graph_nodes(node_id, node_type, label, properties_json)
            VALUES (?, ?, ?, ?)
            ''',
            (node.node_id, node.node_type, node.label, json.dumps(node.properties, ensure_ascii=False)),
        )
        self.connection.commit()

    def save_edge(self, edge: GraphEdge) -> None:
        self.connection.execute(
            '''
            INSERT INTO graph_edges(
                edge_id, source_id, target_id, relation_type,
                confidence, reversible, properties_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                edge.edge_id, edge.source_id, edge.target_id, edge.relation_type,
                edge.confidence, int(edge.reversible),
                json.dumps(edge.properties, ensure_ascii=False),
            ),
        )
        self.connection.commit()

    def save_provenance(self, record: ProvenanceRecord) -> None:
        self.connection.execute(
            '''
            INSERT INTO provenance_records(
                provenance_id, subject_id, source_type, source_ref, author_id,
                observed_at, confidence, verification_status,
                derivation_method, limitations_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                record.provenance_id, record.subject_id, record.source_type,
                record.source_ref, record.author_id, record.observed_at,
                record.confidence, record.verification_status,
                record.derivation_method,
                json.dumps(list(record.limitations), ensure_ascii=False),
            ),
        )
        self.connection.commit()

    def counts(self) -> dict[str, int]:
        result = {}
        for table in ["graph_nodes", "graph_edges", "provenance_records"]:
            row = self.connection.execute(f"SELECT COUNT(*) AS total FROM {table}").fetchone()
            result[table] = int(row["total"])
        return result

    def close(self) -> None:
        self.connection.close()
