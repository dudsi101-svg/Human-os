# Call Authorization Contract

Public shape of `hos_engine/call_authorization.py` and its integration
point in `AgentRuntime`. Check this before changing either. Companion to
`docs/runtime-contract.md`; closes the AR-003 gap
(`docs/security-reviews/ACCEPTED_RISKS.md`).

## Inputs

- `CallRule(capability_id, ...)` — every constraint is opt-in:
  - `allowed_argument_keys: frozenset | None` — closed key set (None = any),
  - `required_argument_keys: frozenset` — keys every call must carry,
  - `allowed_argument_values: Mapping[str, tuple[str, ...]]` — per-key
    closed vocabularies (unlisted keys unconstrained),
  - `max_argument_chars: int | None` — bound on canonical-JSON size of
    the arguments,
  - `allow_via_delegation: bool` — False ⇒ direct holders only,
  - `max_delegation_depth: int | None` — longest tolerated chain.
- `CallAuthorizer(rules, *, unruled)` — one rule per capability
  (duplicate ⇒ `ValueError` at construction); `unruled` is the mandatory,
  keyword-only stance toward capabilities without a rule
  (`UnruledPolicy.ALLOW` or `DENY`) — there is no default.
- `authorize(*, capability_id, arguments, delegation_chain_length)`.

## Outputs

`CallVerdict(allowed, reason, capability_id, rule_applied)` — always a
value, never an exception. `rule_applied=False` marks verdicts produced
by the unruled stance.

## Integration

`AgentRuntime(capabilities, agents, call_authorizer=None)`:
- `call_authorizer=None` ⇒ behavior identical to before the mechanism
  existed (the runtime performs no per-call check),
- otherwise the authorizer is consulted after the capability / scope /
  approval-mode gates and **before** tool execution; a denied verdict
  becomes a `DENIED` receipt with reason `"Call refused: <verdict
  reason>"` — ExecutionLoop's no-exception contract is preserved.

## Non-goals

- Rules judge the call **as declared**; they cannot verify the honesty
  of arguments or of the chain (same epistemic boundary as the Proof
  Kernel and DecisionEngine).
- No rule persistence or distribution format is defined yet — rules are
  constructed in code by the embedding application.
- Not wired into `SecurityGateway`'s 10-step pipeline; that pipeline's
  "capability checks" step remains capability-level. Extending it is a
  separate decision.
