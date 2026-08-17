# ADR Index

Architecture Decision Records for Human OS, grouped by family. Regenerate the table data after adding an ADR — every ADR file should carry a `## Status` section so this index can classify it.

**Status legend:**

- **Accepted** — decided and (where applicable) implemented,
- **Accepted direction** — decided as direction, not yet implemented in the engine,
- **Informational** — records context or provenance; not an implementable decision.

## Core engine (ADR-0002…0008, CORE)

Foundational engine decisions: policy engine, knowledge graph, agent runtime, simulation, protocol, execution kernel.

| ADR | Status | Title |
|---|---|---|
| [ADR-0002](ADR-0002-executable-policy-engine.md) | Accepted | Executable Policy and State Engine |
| [ADR-0003](ADR-0003-development-environment.md) | Accepted | Otwarte środowisko rozwoju |
| [ADR-0004](ADR-0004-knowledge-graph.md) | Accepted | Knowledge Graph and Provenance |
| [ADR-0005](ADR-0005-agent-runtime.md) | Accepted | Capability-bounded agent runtime |
| [ADR-0006](ADR-0006-simulation-laboratory.md) | Accepted | Simulation and Scenario Laboratory |
| [ADR-0007](ADR-0007-human-model-and-consent.md) | Accepted | Human Model and Consent-Aware Personalization |
| [ADR-0008](ADR-0008-signed-protocol-and-identity.md) | Accepted | Signed Protocol and Identity |
| [ADR-CORE-001](ADR-CORE-001-execution-kernel.md) | Accepted | HOS Core Is Established as the Executive Kernel Below the HOS Hub |
| [ADR-CORE-002](ADR-CORE-002-execution-loop-integration.md) | Accepted | A Single Execution Loop Integrates Identity, Authority, Consent, Context, Entity, Constitution, Agent, and Audit |

## Implementation order

Schema before agents before interfaces.

| ADR | Status | Title |
|---|---|---|
| [ADR-IMPL-001](ADR-IMPL-001-schema-before-agents-before-interfaces.md) | Accepted | Stabilize the Schema of Entities and Events First, Then Agents, Then Interfaces |

## Architecture

Cross-cutting architectural constraints.

| ADR | Status | Title |
|---|---|---|
| [ADR-ARCH-002](ADR-ARCH-002-new-components-preserve-layer-numbering.md) | Accepted | New Execution-Platform Components Do Not Change the Existing Domain-Layer Numbering |

## Hub

Entity-first architecture, relations as records, federation, uncertainty as valid state.

| ADR | Status | Title |
|---|---|---|
| [ADR-HUB-001](ADR-HUB-001-entity-first-architecture.md) | Accepted direction | Human OS Adopts an Entity-First Architecture |
| [ADR-HUB-002](ADR-HUB-002-document-is-representation-not-identity.md) | Accepted direction | A Document Is a Representation of an Entity, Not Its Identity |
| [ADR-HUB-003](ADR-HUB-003-relation-is-a-first-class-record.md) | Accepted direction | A Relation Is a First-Class Record With Its Own Provenance and History |
| [ADR-HUB-004](ADR-HUB-004-federated-data-not-single-store.md) | Accepted direction | The Hub Federates Data Instead of Forcing a Single Store |
| [ADR-HUB-005](ADR-HUB-005-uncertainty-and-absence-are-valid-states.md) | Accepted direction | Uncertainty, Conflict, and Absence Are Valid States of the System |
| [ADR-HUB-006](ADR-HUB-006-semantics-before-interface.md) | Accepted direction | Semantics and Contracts Precede Interface Design |

## Graph

Knowledge graph placement within the entity graph.

| ADR | Status | Title |
|---|---|---|
| [ADR-GRAPH-002](ADR-GRAPH-002-knowledge-graph-is-a-subgraph.md) | Accepted | The Knowledge Graph Is a Subgraph of the Shared Entity Graph |

## Agent network

Bounded agent roles, agent cards and autonomy levels.

| ADR | Status | Title |
|---|---|---|
| [ADR-AGENT-001](ADR-AGENT-001-bounded-agent-roles.md) | Accepted | The Agent Network Applies Bounded Roles and Least Privilege |
| [ADR-AGENT-002](ADR-AGENT-002-agent-card-and-autonomy-levels.md) | Accepted | Every Agent Has a Versioned Card, an Autonomy Level, and a Validator |

## Audit

Provenance requirements for recommendations and actions.

| ADR | Status | Title |
|---|---|---|
| [ADR-AUDIT-001](ADR-AUDIT-001-full-provenance-trail.md) | Accepted | Every Recommendation and Action Must Have a Complete Provenance and Execution Trail |

## Proactivity

Consent and quality gates for proactive behavior.

| ADR | Status | Title |
|---|---|---|
| [ADR-PRED-001](ADR-PRED-001-proactivity-gates.md) | Accepted | Proactivity Requires Consent, a Quality Threshold, and Control of Attention Cost |

## Human Model (Layer 2)

Seven-tier ontology, life domains, anti-labeling, clinical boundary.

| ADR | Status | Title |
|---|---|---|
| [ADR-HUMAN-001](ADR-HUMAN-001-seven-tier-ontology-and-irreducible-person.md) | Accepted direction | The Human Model Is a Seven-Tier Ontology With an Irreducible Person at Tier Zero |
| [ADR-HUMAN-002](ADR-HUMAN-002-eleven-domain-map-core-vs-optional.md) | Accepted direction | Eleven Life Domains, With a Protected Core and Consent-Gated Optional Domains |
| [ADR-HUMAN-003](ADR-HUMAN-003-anti-labeling-protected-changes.md) | Accepted direction | Anti-Labeling Rules and "Protected Changes" That Require Constitutional-Level Rejection |
| [ADR-HUMAN-004](ADR-HUMAN-004-observation-hypothesis-contract-gaps-vs-code.md) | Accepted direction | The Observation/Hypothesis Data Contract Is Richer Than the Current HumanRecord |
| [ADR-HUMAN-005](ADR-HUMAN-005-three-modes-and-clinical-boundary.md) | Accepted direction | Three Operating Modes and a Hard Clinical Boundary — No Autonomous Diagnosis |

## Knowledge Map (Layer 3)

Knowledge signatures, node/edge catalog, source classes, epistemic firewall.

| ADR | Status | Title |
|---|---|---|
| [ADR-KNOWLEDGE-001](ADR-KNOWLEDGE-001-own-taxonomy-and-readiness-gate.md) | Accepted direction | The Knowledge Map Defines Its Own Signature, Readiness, and Source-Class Taxonomies |
| [ADR-KNOWLEDGE-002](ADR-KNOWLEDGE-002-no-single-number-signature.md) | Accepted direction | A Knowledge Signature Is a Vector, Never Collapsed to One Number |
| [ADR-KNOWLEDGE-003](ADR-KNOWLEDGE-003-typed-node-and-edge-catalog.md) | Accepted direction | The Knowledge Graph Has a Closed Catalog of 13 Node Types and 9 Named Relations |
| [ADR-KNOWLEDGE-004](ADR-KNOWLEDGE-004-source-class-is-a-type-not-a-rank.md) | Accepted direction | Source Classes Are Types Fit to a Question, Not One Best-to-Worst Ranking |
| [ADR-KNOWLEDGE-005](ADR-KNOWLEDGE-005-epistemic-firewall-consistent-across-layers.md) | Accepted direction | The Epistemic Firewall Around Symbolic/Traditional Knowledge Is Consistent Across Layers 3, 5, and 6 |

## User Model (Layer 4)

R0–R8 architecture, layered consent, no epistemic shortcuts, AI non-override.

| ADR | Status | Title |
|---|---|---|
| [ADR-USERMODEL-001](ADR-USERMODEL-001-r0-r8-architecture-and-own-scales.md) | Accepted direction | The User Model Is a Nine-Row R0–R8 Architecture With Its Own Four Coded Scales |
| [ADR-USERMODEL-002](ADR-USERMODEL-002-epistemic-shortcut-ban-and-right-to-be-forgotten.md) | Accepted direction | No Epistemic Shortcuts From Behavior to Label, and a Working "Right to Be Forgotten in the Model" |
| [ADR-USERMODEL-003](ADR-USERMODEL-003-layered-consent-and-ban-on-secondary-use.md) | Accepted direction | Six-Level Layered Consent, Five-Level Data Sensitivity, and an Absolute Ban on Secondary Commercial Use |
| [ADR-USERMODEL-004](ADR-USERMODEL-004-ai-role-boundaries-and-no-override.md) | Accepted direction | AI May Not Silently Infer, Label, or Override an Explicit User Correction |
| [ADR-USERMODEL-005](ADR-USERMODEL-005-not-the-same-source-as-adr-user-002.md) | Informational | This Document Is Not the Source Behind ADR-USER-002 — Two Sibling Specifications, Not One |
| [ADR-USERMODEL-006](ADR-USERMODEL-006-merge-with-adr-user-002.md) | Accepted | Merging ADR-USER-002 Into the Warstwa 4 User-Model Specification |

## User Model — digital twin

Evolution toward a Human Digital Twin.

| ADR | Status | Title |
|---|---|---|
| [ADR-USER-002](ADR-USER-002-human-digital-twin.md) | Accepted | The User Model Evolves Into a Human Digital Twin, But Does Not Become a Definition of the Person |

## Decision Engine (Layer 5)

Decision taxonomy, hard gates, abstention, AI role boundaries.

| ADR | Status | Title |
|---|---|---|
| [ADR-DECISION-001](ADR-DECISION-001-own-taxonomy-and-nonequivalent-gate-rows.md) | Accepted direction | The Decision Engine Defines Its Own Taxonomy and a Ten-Row Non-Commutable Process Architecture |
| [ADR-DECISION-002](ADR-DECISION-002-no-verdict-objects.md) | Accepted direction | No "Verdict Objects" — Judgments About a Person Must Decompose Into Observation, Context, and Hypothesis |
| [ADR-DECISION-003](ADR-DECISION-003-abstention-is-a-first-class-outcome.md) | Accepted direction | Abstention Is a First-Class, Named Outcome — Not a Failure to Decide |
| [ADR-DECISION-004](ADR-DECISION-004-ai-role-boundaries-in-the-decision-engine.md) | Accepted direction | AI's Role in the Decision Engine — Organizes and Translates, Is Not the Source of Truth or the Final Arbiter of Risk |
| [ADR-DECISION-005](ADR-DECISION-005-high-risk-path-and-determinism-does-not-lower-safety.md) | Accepted direction | The High-Risk Decision Path — User Determination Does Not Lower the Safety Threshold |

## Experiment Engine (Layer 6)

Experiment risk taxonomy, safety/consent non-fungibility, epistemic firewall.

| ADR | Status | Title |
|---|---|---|
| [ADR-EXP-001](ADR-EXP-001-experiment-engine-own-risk-taxonomy-and-launch-gate.md) | Accepted direction | The Experiment Engine (Layer 6) Defines Its Own Risk Taxonomy and a Mandatory Pre-Launch Explainability Gate |
| [ADR-EXP-002](ADR-EXP-002-safety-baseline-consent-are-not-fungible.md) | Accepted direction | Safety, Baseline Quality, and Consent Are Not Fungible With Each Other |
| [ADR-EXP-003](ADR-EXP-003-experiment-objects-are-versioned-and-never-silently-merged.md) | Accepted direction | Experiment Objects Are Independently Versioned and Never Silently Merged |
| [ADR-EXP-004](ADR-EXP-004-ai-role-boundaries-in-the-experiment-engine.md) | Accepted direction | AI's Role in the Experiment Engine Is Bounded by a Fixed List of Forbidden Autonomous Actions |
| [ADR-EXP-005](ADR-EXP-005-reflective-symbolic-experiments-behind-an-epistemic-firewall.md) | Accepted direction | Reflective/Symbolic Experiments Sit Behind an Epistemic Firewall From Causal and Medical Claims |

## Human OS Lab

Separate environment, synthetic data, traces, promotion gates.

| ADR | Status | Title |
|---|---|---|
| [ADR-LAB-001](ADR-LAB-001-separate-environment-no-auto-digital-twin-write.md) | Accepted direction | Human OS Lab Is a Separate Environment That Never Auto-Writes to the Human Digital Twin |
| [ADR-LAB-002](ADR-LAB-002-synthetic-data-by-default.md) | Accepted direction | Human OS Lab Defaults to Synthetic Data |
| [ADR-LAB-003](ADR-LAB-003-every-session-has-trace-and-verdict.md) | Accepted direction | Every Lab Session Carries a Trace and a Tester Verdict |
| [ADR-LAB-004](ADR-LAB-004-interface-hides-complexity-not-actions.md) | Accepted direction | The Lab Interface May Hide Technical Complexity but Never System Actions |
| [ADR-LAB-005](ADR-LAB-005-promotion-requires-explicit-gate.md) | Accepted direction | Promotion from Lab to Core Requires an Explicit, Reversible Gate |
| [ADR-LAB-006](ADR-LAB-006-local-prototype-is-ux-stage.md) | Accepted direction | The Local Lab Prototype Is a UX Stage, Not a Backend |

## Commons (Wspólnie)

Opt-in collaboration module: shared challenges, circles, experience cards, federated exchange.

| ADR | Status | Title |
|---|---|---|
| [ADR-COMMONS-001](ADR-COMMONS-001-wspolnie-principles-and-structure.md) | Accepted direction | "Wspólnie" (Commons/Collaboration Module) — Principles, Structure, Rollout |
| [ADR-COMMONS-002](ADR-COMMONS-002-entities-events-privacy.md) | Accepted direction | Commons Entities, Events, Privacy and Safety Contract |
| [ADR-COMMONS-003](ADR-COMMONS-003-canonical-commons-events.md) | Accepted, implemented | Canonical `commons_*` Event Types (DD-009 part 1) |

## Applications

The user-facing app layer (`apps/user-demo`), its distribution and monetization boundaries.

| ADR | Status | Title |
|---|---|---|
| [ADR-APP-001](ADR-APP-001-store-distribution-and-freemium-boundaries.md) | Accepted | Store Distribution and the Constitutional Boundaries of a Freemium Model |
| [ADR-APP-002](ADR-APP-002-in-app-llm-guide.md) | Accepted | An In-App LLM Guide ("Przewodnik AI") Behind Constitutional Gates |
| [ADR-APP-003](ADR-APP-003-pluggable-guide-engines.md) | Accepted | The Guide Has Swappable Engines — Local by Default, Cloud by Choice |
| [ADR-APP-004](ADR-APP-004-biometric-data-boundaries.md) | Accepted | Biometric/Health Data — Local Import Only, C6 Consent, Explicit-Act Boundary |

## Living Self Model

Conversational self model with epistemic classes.

| ADR | Status | Title |
|---|---|---|
| [ADR-SELFMODEL-001](ADR-SELFMODEL-001-conversational-living-self-model.md) | Accepted | Conversational "About Me" — Living Self Model First Slice |

## Sovereign Recovery

Emergency modes, no backdoors, dual-key sovereignty, emergency event log.

| ADR | Status | Title |
|---|---|---|
| [ADR-RECOVERY-001](ADR-RECOVERY-001-seven-emergency-modes-and-control-hierarchy.md) | Accepted direction | Seven Named Emergency Modes, Ranked Above Core/Hub/Agents in an Eight-Level Control Hierarchy |
| [ADR-RECOVERY-002](ADR-RECOVERY-002-no-hidden-backdoors-no-entity-outranks-the-owner.md) | Accepted direction | No Hidden Backdoors, No Entity Outranks the Owner, No Single-Vendor Dependency |
| [ADR-RECOVERY-003](ADR-RECOVERY-003-dual-key-sovereignty-and-minimal-scope.md) | Accepted direction | Dual-Key Sovereignty and Minimal Scope Contain Coercion and Blast Radius |
| [ADR-RECOVERY-004](ADR-RECOVERY-004-emergency-event-log-and-hub-contracts.md) | Accepted direction | Every Emergency-Mode Use Is Logged in a Mandatory, Versioned, Signed 13-Field Record |
| [ADR-RECOVERY-005](ADR-RECOVERY-005-open-gaps-not-resolved-by-this-source.md) | Informational | What This Source Does Not Resolve — Recorded, Not Guessed |
| [ADR-RECOVERY-006](ADR-RECOVERY-006-founder-resolutions-for-the-four-blocking-gaps.md) | Accepted | Founder Resolutions for the Four Gaps That Blocked Recovery Implementation |

## World Model

Domain models with currency and provenance.

| ADR | Status | Title |
|---|---|---|
| [ADR-WORLD-001](ADR-WORLD-001-world-model-domain-signals.md) | Accepted | The World Model Consists of Domain Models With Currency and Uncertainty |

