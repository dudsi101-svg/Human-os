from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from hos_engine.hub_entity_registry import (
    EntityRegistry,
    HubEntityStatus,
    HubEntityType,
    HubRelationType,
    RelationRegistry,
)
from hos_engine.hub_store import SQLiteHubStore

OWNER = "HOS-HUM-000001"


def populated_registries():
    entities = EntityRegistry()
    relations = RelationRegistry(entities)
    person = entities.register(
        entity_type=HubEntityType.PERSON, working_name="Aleks",
        responsibility_owner_id=OWNER, provenance_source="test")
    goal = entities.register(
        entity_type=HubEntityType.GOAL, working_name="Stabilna energia",
        responsibility_owner_id=OWNER, provenance_source="test")
    dup_a = entities.register(
        entity_type=HubEntityType.RESOURCE, working_name="Dysk",
        responsibility_owner_id=OWNER, provenance_source="test")
    dup_b = entities.register(
        entity_type=HubEntityType.RESOURCE, working_name="Dysk (kopia)",
        responsibility_owner_id=OWNER, provenance_source="import")
    entities.transition(goal.entity_id, HubEntityStatus.ACTIVE)
    entities.flag_possible_duplicate(dup_a.entity_id, dup_b.entity_id)
    entities.merge(
        keep_entity_id=dup_a.entity_id, retire_entity_id=dup_b.entity_id,
        reason="same drive imported twice", evidence="identical mount path",
        approved_by=OWNER)
    rel = relations.link(
        relation_type=HubRelationType.REALIZUJE,
        source_entity_id=person.entity_id, target_entity_id=goal.entity_id,
        asserted_by=OWNER, confidence=0.8)
    return entities, relations, person, goal, dup_a, dup_b, rel


class HubStoreRoundTripTests(unittest.TestCase):
    def test_snapshot_and_restore_preserve_everything_verbatim(self):
        entities, relations, person, goal, dup_a, dup_b, rel = populated_registries()
        with tempfile.TemporaryDirectory() as tmp:
            store = SQLiteHubStore(str(Path(tmp) / "hub.db"))
            store.save_snapshot(entities, relations)
            loaded_entities, loaded_relations = store.load_registries()
            store.close()

        # entities: ids, statuses and timestamps verbatim
        restored_goal = loaded_entities.get(goal.entity_id)
        self.assertEqual(restored_goal.status, HubEntityStatus.ACTIVE)
        self.assertEqual(restored_goal.created_at, goal.created_at)
        # retired entity survives with its merge provenance
        self.assertEqual(loaded_entities.get(dup_b.entity_id).status,
                         HubEntityStatus.SUPERSEDED)
        merge = loaded_entities.merge_record_for(dup_b.entity_id)
        self.assertIsNotNone(merge)
        self.assertEqual(merge.approved_by, OWNER)
        self.assertEqual(merge.evidence, "identical mount path")
        # relations: id, confidence and endpoints verbatim; indexes rebuilt
        restored_rel = loaded_relations.get(rel.relation_id)
        self.assertEqual(restored_rel.confidence, 0.8)
        self.assertEqual(
            [r.relation_id for r in loaded_relations.outgoing(person.entity_id)],
            [rel.relation_id])
        self.assertEqual(loaded_relations.orphans([dup_a.entity_id]),
                         [dup_a.entity_id])

    def test_duplicate_flags_survive_round_trip(self):
        entities = EntityRegistry()
        a = entities.register(entity_type=HubEntityType.RESOURCE, working_name="A",
                              responsibility_owner_id=OWNER, provenance_source="t")
        b = entities.register(entity_type=HubEntityType.RESOURCE, working_name="B",
                              responsibility_owner_id=OWNER, provenance_source="t")
        entities.flag_possible_duplicate(a.entity_id, b.entity_id)
        with tempfile.TemporaryDirectory() as tmp:
            store = SQLiteHubStore(str(Path(tmp) / "hub.db"))
            store.save_snapshot(entities)
            loaded, _ = store.load_registries()
            store.close()
        self.assertEqual(loaded.possible_duplicates_of(a.entity_id), {b.entity_id})
        self.assertEqual(loaded.possible_duplicates_of(b.entity_id), {a.entity_id})

    def test_resnapshot_replaces_not_duplicates(self):
        entities, relations, *_ = populated_registries()
        with tempfile.TemporaryDirectory() as tmp:
            store = SQLiteHubStore(str(Path(tmp) / "hub.db"))
            store.save_snapshot(entities, relations)
            first = store.counts()
            entities.register(entity_type=HubEntityType.DECISION,
                              working_name="Nowa decyzja",
                              responsibility_owner_id=OWNER, provenance_source="t")
            store.save_snapshot(entities, relations)
            second = store.counts()
            store.close()
        self.assertEqual(second["hub_entities"], first["hub_entities"] + 1)
        self.assertEqual(second["hub_relations"], first["hub_relations"])

    def test_restored_registry_keeps_enforcing_rules(self):
        entities, relations, person, goal, *_ = populated_registries()
        with tempfile.TemporaryDirectory() as tmp:
            store = SQLiteHubStore(str(Path(tmp) / "hub.db"))
            store.save_snapshot(entities, relations)
            loaded_entities, loaded_relations = store.load_registries()
            store.close()
        with self.assertRaises(ValueError):
            loaded_entities.merge(
                keep_entity_id=person.entity_id, retire_entity_id=person.entity_id,
                reason="x", evidence="x", approved_by=OWNER)
        with self.assertRaises(KeyError):
            loaded_relations.link(
                relation_type=HubRelationType.DOTYCZY,
                source_entity_id="HOS-ENT-NOPE", target_entity_id=goal.entity_id,
                asserted_by=OWNER)


if __name__ == "__main__":
    unittest.main()
