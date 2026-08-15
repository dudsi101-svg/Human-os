from __future__ import annotations

import uuid
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from enum import Enum


class AuthorityRole(str, Enum):
    """AXIS B: what authority a subject holds -- distinct from
    hos_engine.security_identity.IdentityType (AXIS A: what kind of subject
    it technically is). See founder review Q9 correction, 2026-08-15
    (docs/FOUNDER_REVIEW_2026-08-15.md): a subject can be identity kind
    HUMAN while holding role OWNER or OPERATOR; a SERVICE can be a subject
    kind and separately receive an authority role. The two axes are kept in
    two separate modules on purpose -- this one never touches
    security_identity.py.

    From Identity, Authority & Permissions v0.1, §1.
    """

    OWNER = "OWNER"
    OPERATOR = "OPERATOR"
    TRUSTED_DELEGATE = "TRUSTED_DELEGATE"
    # Holder of the independent recovery key in Sovereign Recovery's dual-key
    # sovereignty scheme (docs/adr/ADR-RECOVERY-003) -- never the OWNER
    # themself, since the second key exists specifically to guard against an
    # irreversible action taken by the owner under coercion or by mistake.
    # The role name appears in this enum with no justification in its own
    # source document; founder decision 2026-08-15 maps it onto the
    # Constitution's Security Team governance role (constitution/README.md
    # Ch.13, "Zespol bezpieczenstwa") rather than inventing a new governance
    # role -- see docs/FOUNDER_REVIEW_2026-08-15.md, "Piata tura".
    RECOVERY_CUSTODIAN = "RECOVERY_CUSTODIAN"
    AGENT = "AGENT"
    SERVICE = "SERVICE"
    GUEST = "GUEST"
    SYSTEM_PROCESS = "SYSTEM_PROCESS"


@dataclass(frozen=True)
class RoleGrant:
    grant_id: str
    identity_id: str
    role: AuthorityRole
    scope: str
    issued_by: str
    valid_from: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    valid_to: str | None = None
    revoked_at: str | None = None


class RoleGrantRegistry:
    """Assigns and revokes AuthorityRole grants against an identity_id.

    Cardinality: one identity may hold multiple concurrent grants -- e.g. a
    HUMAN identity holding both OWNER and OPERATOR at once, each
    independently scoped, time-bounded, and revocable. This registry does
    not create, validate, or own identities itself; it only records grants
    against an identity_id supplied by the caller (typically
    hos_engine.security_identity.IdentityRegistry), which is exactly the
    separation Q9's correction called for.

    Revocation is explicit and permanent for that grant (a revoked grant is
    never un-revoked; issue a new one instead) -- consistent with the
    project-wide rule that consent/authority revocation is a first-class,
    auditable event, not a silent state flip.
    """

    def __init__(self) -> None:
        self._grants: dict[str, RoleGrant] = {}

    def grant(
        self,
        *,
        identity_id: str,
        role: AuthorityRole,
        scope: str,
        issued_by: str,
        valid_to: str | None = None,
    ) -> RoleGrant:
        role_grant = RoleGrant(
            grant_id="HOS-ROL-" + uuid.uuid4().hex[:12].upper(),
            identity_id=identity_id,
            role=role,
            scope=scope,
            issued_by=issued_by,
            valid_to=valid_to,
        )
        self._grants[role_grant.grant_id] = role_grant
        return role_grant

    def revoke(self, grant_id: str) -> RoleGrant:
        current = self._grants[grant_id]
        if current.revoked_at is not None:
            raise ValueError(f"Grant {grant_id} is already revoked")
        updated = replace(current, revoked_at=datetime.now(UTC).isoformat())
        self._grants[grant_id] = updated
        return updated

    def get(self, grant_id: str) -> RoleGrant:
        return self._grants[grant_id]

    def active_roles_for(self, identity_id: str, *, scope: str | None = None) -> list[RoleGrant]:
        now = datetime.now(UTC).isoformat()
        return [
            g for g in self._grants.values()
            if g.identity_id == identity_id
            and g.revoked_at is None
            and (g.valid_to is None or g.valid_to > now)
            and (scope is None or g.scope == scope or g.scope == "*")
        ]

    def has_role(self, identity_id: str, role: AuthorityRole, *, scope: str | None = None) -> bool:
        return any(g.role == role for g in self.active_roles_for(identity_id, scope=scope))
