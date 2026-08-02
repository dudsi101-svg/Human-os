import unittest

from hos_engine.knowledge_graph import (
    GraphEdge,
    GraphNode,
    KnowledgeGraph,
    ProvenanceRecord,
)


class KnowledgeGraphTests(unittest.TestCase):
    def setUp(self):
        self.graph = KnowledgeGraph()
        for node in [
            GraphNode("HOS-HUM-1", "human", "Human"),
            GraphNode("HOS-INT-1", "intent", "Intent"),
            GraphNode("HOS-KNW-1", "knowledge", "Knowledge"),
        ]:
            self.graph.add_node(node)

        self.graph.add_edge(
            GraphEdge("HOS-EDG-1", "HOS-HUM-1", "HOS-INT-1", "AUTHORS", 1.0)
        )
        self.graph.add_edge(
            GraphEdge("HOS-EDG-2", "HOS-INT-1", "HOS-KNW-1", "USES", 0.8)
        )

    def test_shortest_path(self):
        self.assertEqual(
            self.graph.shortest_path("HOS-HUM-1", "HOS-KNW-1"),
            ["HOS-HUM-1", "HOS-INT-1", "HOS-KNW-1"],
        )

    def test_path_confidence(self):
        path = ["HOS-HUM-1", "HOS-INT-1", "HOS-KNW-1"]
        self.assertEqual(self.graph.confidence_of_path(path), 0.8)

    def test_provenance(self):
        record = ProvenanceRecord(
            provenance_id="HOS-PRV-1",
            subject_id="HOS-KNW-1",
            source_type="document",
            source_ref="constitution-v0.1",
            author_id="HOS-HUM-1",
            observed_at="2026-07-20T12:00:00+00:00",
            confidence=0.95,
            verification_status="VERIFIED",
            derivation_method="human-authored",
            limitations=("Not independently audited.",),
        )
        self.graph.add_provenance(record)
        self.assertEqual(len(self.graph.provenance("HOS-KNW-1")), 1)

    def test_cycle_detection(self):
        self.assertFalse(self.graph.has_directed_cycle())
        self.graph.add_edge(
            GraphEdge("HOS-EDG-3", "HOS-KNW-1", "HOS-HUM-1", "INFLUENCES", 0.5)
        )
        self.assertTrue(self.graph.has_directed_cycle())


if __name__ == "__main__":
    unittest.main()
