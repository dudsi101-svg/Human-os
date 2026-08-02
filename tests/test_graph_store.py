import tempfile
import unittest
from pathlib import Path

from hos_engine.graph_store import SQLiteGraphStore
from hos_engine.knowledge_graph import GraphEdge, GraphNode, ProvenanceRecord


class GraphStoreTests(unittest.TestCase):
    def test_persistence_counts(self):
        with tempfile.TemporaryDirectory() as directory:
            store = SQLiteGraphStore(Path(directory) / "graph.db")
            store.save_node(GraphNode("N1", "human", "Human"))
            store.save_node(GraphNode("N2", "knowledge", "Knowledge"))
            store.save_edge(GraphEdge("E1", "N1", "N2", "AUTHORS", 1.0))
            store.save_provenance(
                ProvenanceRecord(
                    "P1", "N2", "document", "doc-1", "N1",
                    "2026-07-20T12:00:00+00:00", 1.0,
                    "VERIFIED", "human-authored"
                )
            )
            self.assertEqual(
                store.counts(),
                {"graph_nodes": 2, "graph_edges": 1, "provenance_records": 1},
            )
            store.close()


if __name__ == "__main__":
    unittest.main()
