from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum

"""Per-call authorization for agent tool invocations (closes AR-003's gap).

Capability grants answer "may this agent ever use this tool?". They do not
answer "should *this* call, with *these* arguments, arriving through *this*
delegation chain, be allowed?" — the gap recorded as AR-003 in
`docs/security-reviews/ACCEPTED_RISKS.md` and in `security/THREAT_MODEL.md`
("per-call authorization bound to delegation-chain context").

This module supplies that second answer as declarative, per-capability
rules evaluated by `AgentRuntime` on every invocation, after the existing
capability/scope/approval gates and before the tool executes.

Design constraints, matching the project's founder resolutions:

- **No defaults.** A `CallAuthorizer` must declare its stance toward
  capabilities that have no rule (`UnruledPolicy.ALLOW` or `DENY`) — there
  is no built-in assumption, so a deployment cannot drift into an
  unconsidered posture.
- **Refusal is a first-class verdict**, never an exception: the runtime
  turns a denied verdict into a DENIED receipt, keeping ExecutionLoop's
  no-exception contract intact.
- **Declared inputs only.** Rules constrain the call as declared
  (arguments, chain shape). They cannot verify honesty of the declaration
  — same epistemic boundary as the Proof Kernel and DecisionEngine.
"""


class UnruledPolicy(str, Enum):
    """Stance toward a capability that has no CallRule. Must be chosen
    explicitly when constructing an authorizer — never assumed."""

    ALLOW = "ALLOW"
    DENY = "DENY"


@dataclass(frozen=True)
class CallRule:
    """Declarative constraints for calls on one capability.

    Every field is opt-in: an unset field constrains nothing, so a rule
    states exactly what it means and nothing more.
    """

    capability_id: str
    # Closed set of argument keys the call may carry. None = any keys.
    allowed_argument_keys: frozenset[str] | None = None
    # Keys every call must carry.
    required_argument_keys: frozenset[str] = frozenset()
    # Per-key closed vocabularies; a listed key's value must be one of the
    # given strings. Unlisted keys are unconstrained by this field.
    allowed_argument_values: Mapping[str, tuple[str, ...]] = field(default_factory=dict)
    # Upper bound on the canonical-JSON size of the arguments, guarding
    # against payload smuggling through an otherwise-legitimate call.
    max_argument_chars: int | None = None
    # False → only a direct holder of the capability may call; any
    # delegation chain is refused.
    allow_via_delegation: bool = True
    # Longest delegation chain this rule tolerates (None = registry's own
    # depth limits are the only bound).
    max_delegation_depth: int | None = None


@dataclass(frozen=True)
class CallVerdict:
    """The authorizer's answer for one invocation."""

    allowed: bool
    reason: str
    capability_id: str
    rule_applied: bool


class CallAuthorizer:
    """Evaluates CallRules against a concrete invocation.

    Stateless with respect to calls; all state is the rule table given at
    construction. One rule per capability — a second rule for the same
    capability is a configuration error, refused loudly.
    """

    def __init__(self, rules: list[CallRule], *, unruled: UnruledPolicy) -> None:
        self._rules: dict[str, CallRule] = {}
        for rule in rules:
            if rule.capability_id in self._rules:
                raise ValueError(
                    f"duplicate CallRule for capability {rule.capability_id!r}"
                )
            self._rules[rule.capability_id] = rule
        self._unruled = unruled

    def authorize(
        self,
        *,
        capability_id: str,
        arguments: Mapping[str, object],
        delegation_chain_length: int,
    ) -> CallVerdict:
        rule = self._rules.get(capability_id)
        if rule is None:
            allowed = self._unruled is UnruledPolicy.ALLOW
            return CallVerdict(
                allowed=allowed,
                reason=(
                    f"no call rule for {capability_id}; declared unruled"
                    f" policy is {self._unruled.value}"
                ),
                capability_id=capability_id,
                rule_applied=False,
            )

        def deny(reason: str) -> CallVerdict:
            return CallVerdict(
                allowed=False, reason=reason,
                capability_id=capability_id, rule_applied=True,
            )

        if rule.allowed_argument_keys is not None:
            unexpected = sorted(set(arguments) - rule.allowed_argument_keys)
            if unexpected:
                return deny(
                    f"arguments outside the allowed set: {', '.join(unexpected)}"
                )
        missing = sorted(rule.required_argument_keys - set(arguments))
        if missing:
            return deny(f"required arguments missing: {', '.join(missing)}")
        for key, vocabulary in rule.allowed_argument_values.items():
            if key in arguments and str(arguments[key]) not in vocabulary:
                return deny(
                    f"argument {key!r} value outside its closed vocabulary"
                )
        if rule.max_argument_chars is not None:
            size = len(json.dumps(dict(arguments), sort_keys=True, default=str))
            if size > rule.max_argument_chars:
                return deny(
                    f"arguments exceed {rule.max_argument_chars} chars ({size})"
                )
        if delegation_chain_length > 0 and not rule.allow_via_delegation:
            return deny("capability may only be called by a direct holder")
        if (
            rule.max_delegation_depth is not None
            and delegation_chain_length > rule.max_delegation_depth
        ):
            return deny(
                f"delegation chain length {delegation_chain_length} exceeds"
                f" the rule's limit of {rule.max_delegation_depth}"
            )
        return CallVerdict(
            allowed=True,
            reason="call satisfies its capability's rule",
            capability_id=capability_id,
            rule_applied=True,
        )
