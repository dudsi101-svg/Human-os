import unittest

from hos_engine.hub_entity_registry import (
    EntityRegistry,
    HubEntityStatus,
    HubEntityType,
    HubRelationType,
    RelationRegistry,
)

MERGE_KWARGS = {
    "reason": "duplicate founder record entered twice",
    "evidence": "same email address on both records",
    "approved_by": "HOS-HUM-000001",
}


class EntityRegistryTests(unittest.TestCase):
    def setUp(self):
        self.registry = EntityRegistry()

    def test_register_assigns_hos_ent_id_and_proposed_status(self):
        entity = self.registry.register(
            entity_type=HubEntityType.PERSON,
            working_name="Founder",
            responsibility_owner_id="HOS-HUM-000001",
            provenance_source="manual entry",
        )
        self.assertTrue(entity.entity_id.startswith("HOS-ENT-"))
        self.assertEqual(entity.status, HubEntityStatus.PROPOSED)
        self.assertEqual(self.registry.get(entity.entity_id), entity)

    def test_transition_updates_status(self):
        entity = self.registry.register(
            entity_type=HubEntityType.GOAL,
            working_name="Ship Hub MVP",
            responsibility_owner_id="HOS-HUM-000001",
            provenance_source="founder review 2026-08-15",
        )
        activated = self.registry.transition(entity.entity_id, HubEntityStatus.ACTIVE)
        self.assertEqual(activated.status, HubEntityStatus.ACTIVE)

    def test_by_type_filters_correctly(self):
        self.registry.register(entity_type=HubEntityType.PERSON, working_name="A", responsibility_owner_id="x", provenance_source="s")
        self.registry.register(entity_type=HubEntityType.GOAL, working_name="B", responsibility_owner_id="x", provenance_source="s")
        self.registry.register(entity_type=HubEntityType.GOAL, working_name="C", responsibility_owner_id="x", provenance_source="s")
        self.assertEqual(len(self.registry.by_type(HubEntityType.GOAL)), 2)
        self.assertEqual(len(self.registry.by_type(HubEntityType.PERSON)), 1)
        self.assertEqual(len(self.registry.by_type(HubEntityType.RESOURCE)), 0)

    def test_flag_and_merge_duplicates(self):
        keep = self.registry.register(entity_type=HubEntityType.PERSON, working_name="Founder", responsibility_owner_id="x", provenance_source="s")
        dupe = self.registry.register(entity_type=HubEntityType.PERSON, working_name="Founder (dup)", responsibility_owner_id="x", provenance_source="s")

        self.registry.flag_possible_duplicate(keep.entity_id, dupe.entity_id)
        self.assertIn(dupe.entity_id, self.registry.possible_duplicates_of(keep.entity_id))
        self.assertIn(keep.entity_id, self.registry.possible_duplicates_of(dupe.entity_id))

        merged = self.registry.merge(keep_entity_id=keep.entity_id, retire_entity_id=dupe.entity_id, **MERGE_KWARGS)
        self.assertEqual(merged.entity_id, keep.entity_id)
        self.assertEqual(self.registry.get(dupe.entity_id).status, HubEntityStatus.SUPERSEDED)
        self.assertEqual(self.registry.possible_duplicates_of(keep.entity_id), set())

    def test_merge_rejects_self_merge(self):
        entity = self.registry.register(entity_type=HubEntityType.PERSON, working_name="A", responsibility_owner_id="x", provenance_source="s")
        with self.assertRaises(ValueError):
            self.registry.merge(keep_entity_id=entity.entity_id, retire_entity_id=entity.entity_id, **MERGE_KWARGS)

    def test_merge_is_reconstructable_from_provenance(self):
        keep = self.registry.register(entity_type=HubEntityType.PERSON, working_name="Founder", responsibility_owner_id="x", provenance_source="s")
        dupe = self.registry.register(entity_type=HubEntityType.PERSON, working_name="Founder (dup)", responsibility_owner_id="x", provenance_source="s")

        self.assertIsNone(self.registry.merge_record_for(dupe.entity_id))
        self.registry.merge(keep_entity_id=keep.entity_id, retire_entity_id=dupe.entity_id, **MERGE_KWARGS)

        record = self.registry.merge_record_for(dupe.entity_id)
        self.assertIsNotNone(record)
        self.assertEqual(record.keep_entity_id, keep.entity_id)
        self.assertEqual(record.retire_entity_id, dupe.entity_id)
        self.assertEqual(record.reason, MERGE_KWARGS["reason"])
        self.assertEqual(record.evidence, MERGE_KWARGS["evidence"])
        self.assertEqual(record.approved_by, MERGE_KWARGS["approved_by"])
        # the retired entity itself is never erased -- it is only superseded
        self.assertEqual(self.registry.get(dupe.entity_id).status, HubEntityStatus.SUPERSEDED)


class RelationRegistryTests(unittest.TestCase):
    def setUp(self):
        self.entities = EntityRegistry()
        self.relations = RelationRegistry(self.entities)
        self.person = self.entities.register(entity_type=HubEntityType.PERSON, working_name="Founder", responsibility_owner_id="x", provenance_source="s")
        self.goal = self.entities.register(entity_type=HubEntityType.GOAL, working_name="Ship Hub MVP", responsibility_owner_id="x", provenance_source="s")

    def test_link_creates_relation_with_confidence_and_direction(self):
        relation = self.relations.link(
            relation_type=HubRelationType.REALIZUJE,
            source_entity_id=self.person.entity_id,
            target_entity_id=self.goal.entity_id,
            asserted_by=self.person.entity_id,
            confidence=0.9,
        )
        self.assertTrue(relation.relation_id.startswith("HOS-REL-"))
        self.assertEqual(relation.confidence, 0.9)
        self.assertIn(relation, self.relations.outgoing(self.person.entity_id))
        self.assertIn(relation, self.relations.incoming(self.goal.entity_id))

    def test_link_rejects_out_of_range_confidence(self):
        with self.assertRaises(ValueError):
            self.relations.link(
                relation_type=HubRelationType.REALIZUJE,
                source_entity_id=self.person.entity_id,
                target_entity_id=self.goal.entity_id,
                asserted_by=self.person.entity_id,
                confidence=1.5,
            )

    def test_link_rejects_unknown_entity(self):
        with self.assertRaises(KeyError):
            self.relations.link(
                relation_type=HubRelationType.REALIZUJE,
                source_entity_id="HOS-ENT-DOESNOTEXIST",
                target_entity_id=self.goal.entity_id,
                asserted_by=self.person.entity_id,
            )

    def test_orphans_reports_unconnected_entities(self):
        lonely = self.entities.register(entity_type=HubEntityType.RESOURCE, working_name="Unused doc", responsibility_owner_id="x", provenance_source="s")
        self.relations.link(
            relation_type=HubRelationType.REALIZUJE,
            source_entity_id=self.person.entity_id,
            target_entity_id=self.goal.entity_id,
            asserted_by=self.person.entity_id,
        )
        orphans = self.relations.orphans([self.person.entity_id, self.goal.entity_id, lonely.entity_id])
        self.assertEqual(orphans, [lonely.entity_id])


if __name__ == "__main__":
    unittest.main()
