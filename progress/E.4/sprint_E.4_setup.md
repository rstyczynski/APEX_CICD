# E.4 — Contract and analysis

## Contract

The Product Owner selected only [PBI-042 and PBI-060](../../BACKLOG.md), excluded
PBI-056 and classified the other suggested additions as Construction work.
On 2026-11-09 the Product Owner accepted and closed E.3 and authorized E.4.
[PLAN](../../PLAN.md) owns assignment/status; [the board](../../PROGRESS_BOARD.md)
owns execution tracking. Managed mode, Test: smoke, integration; Regression:
smoke. This is an Elaboration experiment. Setup/design and an external review
in the existing local Astra chat are authorized; implementation awaits explicit
Product Owner approval after that review. The direct request authorizes local
reviewer contact in place of the skill's normal user-relay procedure.

The manager, contractor, analyst, designer and test-architecture procedures are
applied with the local patch and Product Owner preferences. The manager's combined
setup record replaces separate contract/analysis summaries. Native SQLcl and
APEX perform capture, staging, release and installation; GitHub provides source
review and visible run evidence. No independent reservation service, private
branch provisioning, production hardening or new test framework is selected.
No code or test skeleton is created before approval, following local P8 and the
explicit stop-after-design instruction. Token usage is not available per phase.

Use GitHub variables/secrets for workflow configuration; generate connections
in RUNNER_TEMP and clean them. Do not create authoritative scratch settings or
expand the prepared-host credential exception. Preserve unrelated working edits.
The review checkpoint may include the existing PBI-060 definition as necessary
review context, without claiming completion or changing its acceptance criterion.

## Analysis

### System boundary and actors

A-01 developers A/B/C author three independently attributable changes. A-02
integrator reviews their Git contributions and assembles a release. A-03 operator
synchronizes central DEV explicitly. A-04 application user inspects combined
behavior and retained history. A-05 GitHub hosts branches/PRs and run evidence.
The [SRS](../../docs/srs.md) owns actor and use-case definitions; this experiment
covers bounded UC-10/7/4/11 paths, not complete UC-8/9 onboarding or FR-8's atomic
reservation contract. Existing requirements remain requirements after this sprint.

### PBI-060 analysis

The acceptance signal is three separately staged contributions integrated and
validated in one numbered native release. It does not require new isolated
branch environments or a simultaneous conflicting-write proof. Use the prepared
shared authoring application and coordinated capture windows. Each developer
owns a separate checkout and branch, records its actual base and exports/stages
only a reviewed delta. A/B/C may develop ideas concurrently, but capture into
shared author Main is deliberately serialized. Do not present this as PBI-019.

The risk is that accumulated source or generated changelog includes hide or
lose a contribution. Retain before/after source and distribution diffs for each
window, the native comparison base, dependency order and final include graph.
A same-file collision must be explained by actual observed native output; if
no textual conflict occurs, do not fabricate one or claim conflict testing.

### PBI-042 analysis

Central DEV is the separate prepared release target, not the authoring Main
application. An accepted revision must update that target while preserving
uncaptured target edits and refusing an older candidate after a newer revision
is selected/applied. Native PROJECT verify checks project structure; it does not
establish absence of target drift. Use native APEX checksum observations and an
explicit operator admission decision under a coordinated no-edit interval.
This validates the safe procedure, not an unattended race-proof enforcement service.

### Compatibility and feasibility

Reuse E.3's corrected local bundle and qualified native lifecycle. Its historical
remote seed can differ. The [E.3 correction](../E.3/sprint_E.3_release_correction.md)
records SQLcl 25.4.1.022.0618 / project 25.4.1.0 / Java 21 and APEX 24.2.
Before native writes compare the actual selected checkout metadata and executable
release/build. Never change the metadata to bypass the native version check.

The retained E3_TARGET upgrade/repeat path is qualified; independent initial
installation failed ORA-20860 and is excluded. Existing author/target mappings,
permissions and current baselines must be checked before execution. Do not
promise successful reuse based solely on old receipts. Design feasibility is
supported by documented interfaces and E.3 evidence; E.4 runtime results remain
pending. The [design](sprint_E.4_design.md) specifies the experiment and stop rules.

## Readiness

Analysis is complete for design. No additional product-scope question is pending.
Design is Proposed, subject to independent local Astra review and Product Owner
approval. No E.4 database operation, workflow dispatch or implementation has run.
