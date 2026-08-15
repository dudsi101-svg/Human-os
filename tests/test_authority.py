import unittest

from hos_engine.authority import AuthorityRole, RoleGrantRegistry


class RoleGrantRegistryTests(unittest.TestCase):
    def setUp(self):
        self.registry = RoleGrantRegistry()

    def test_grant_assigns_id_and_is_active(self):
        grant = self.registry.grant(
            identity_id="HOS-HUM-000001",
            role=AuthorityRole.OWNER,
            scope="*",
            issued_by="HOS-HUM-000001",
        )
        self.assertTrue(grant.grant_id.startswith("HOS-ROL-"))
        self.assertTrue(self.registry.has_role("HOS-HUM-000001", AuthorityRole.OWNER))

    def test_identity_can_hold_multiple_concurrent_roles(self):
        self.registry.grant(identity_id="HOS-HUM-000001", role=AuthorityRole.OWNER, scope="*", issued_by="HOS-HUM-000001")
        self.registry.grant(identity_id="HOS-HUM-000001", role=AuthorityRole.OPERATOR, scope="project:x", issued_by="HOS-HUM-000001")

        self.assertTrue(self.registry.has_role("HOS-HUM-000001", AuthorityRole.OWNER))
        self.assertTrue(self.registry.has_role("HOS-HUM-000001", AuthorityRole.OPERATOR))
        self.assertEqual(len(self.registry.active_roles_for("HOS-HUM-000001")), 2)

    def test_revoke_removes_role_from_active_set(self):
        grant = self.registry.grant(identity_id="HOS-HUM-000001", role=AuthorityRole.OWNER, scope="*", issued_by="HOS-HUM-000001")
        self.assertTrue(self.registry.has_role("HOS-HUM-000001", AuthorityRole.OWNER))

        self.registry.revoke(grant.grant_id)
        self.assertFalse(self.registry.has_role("HOS-HUM-000001", AuthorityRole.OWNER))

    def test_double_revoke_raises(self):
        grant = self.registry.grant(identity_id="HOS-HUM-000001", role=AuthorityRole.OWNER, scope="*", issued_by="HOS-HUM-000001")
        self.registry.revoke(grant.grant_id)
        with self.assertRaises(ValueError):
            self.registry.revoke(grant.grant_id)

    def test_scope_filters_active_roles(self):
        self.registry.grant(identity_id="HOS-HUM-000001", role=AuthorityRole.OPERATOR, scope="project:x", issued_by="HOS-HUM-000001")
        self.assertTrue(self.registry.has_role("HOS-HUM-000001", AuthorityRole.OPERATOR, scope="project:x"))
        self.assertFalse(self.registry.has_role("HOS-HUM-000001", AuthorityRole.OPERATOR, scope="project:y"))

    def test_wildcard_scope_grant_matches_any_scope_query(self):
        self.registry.grant(identity_id="HOS-HUM-000001", role=AuthorityRole.OWNER, scope="*", issued_by="HOS-HUM-000001")
        self.assertTrue(self.registry.has_role("HOS-HUM-000001", AuthorityRole.OWNER, scope="project:x"))

    def test_no_roles_for_unknown_identity(self):
        self.assertEqual(self.registry.active_roles_for("HOS-HUM-999999"), [])
        self.assertFalse(self.registry.has_role("HOS-HUM-999999", AuthorityRole.OWNER))


if __name__ == "__main__":
    unittest.main()
