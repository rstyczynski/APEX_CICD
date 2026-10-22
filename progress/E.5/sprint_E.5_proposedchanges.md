# E.5 Foundation upgrades and version coexistence

## Decision, status and authoritative documents

On 2026-10-19 the Product Owner deferred the Foundation upgrade scenarios
from E.2 to E.5, the final currently planned Elaboration iteration. E.2 now
owns gap analysis and required exercises on E.1's existing technology; E.3
and E.4 retain their planned technology evaluations. E.5 is Planned in managed
mode and requires an accepted, stabilized technology/toolchain before execution.
This is a pre-sprint scope record, not an implementation approval or test result.

The [Sprint Plan](../../PLAN.md#sprint-e5---validate-foundation-upgrades-and-version-coexistence)
owns assignments and lifecycle status. The [Product Backlog](../../BACKLOG.md)
owns PBI-048–050 definitions, and the [progress board](../../PROGRESS_BOARD.md)
tracks their Planned rows. The [SRS](../../docs/srs.md) owns requirements,
the [architecture](../../docs/architecture.md) owns mechanisms, and the
[test profile](../../docs/test-profile.md) owns executable verification.
Their current application-wide maintenance baseline requires explicit
refinement before implementing this availability scenario. The
[README](../../README.md) and [roadmap](../../ROADMAP.md) link this scope to
the project direction. The closed [E.1 handover](../E.1/sprint_E.1_handover.md)
remains historical evidence, not proof of a successful Foundation upgrade.

## Assigned outcomes and semantic versioning

[PBI-048](../../BACKLOG.md#pbi-048-prove-an-available-compatible-foundation-extension)
validates Foundation 1.0.0 to 1.1.0 as a compatible extension, using optional
greeting-language support while preserving supported legacy API behavior and
database access. Both unchanged consumers must continue reading and writing
during deployment, data migration and supported recovery.

[PBI-049](../../BACKLOG.md#pbi-049-prove-an-available-breaking-foundation-transition)
retains its existing definition: a breaking Foundation 2.0.0 contract for
templates and structured parameters, coexistence with the legacy contract,
independent consumer adoption, data preservation and supported return to
legacy operation after new-contract writes. The Product Owner explicitly
requested that this backlog definition remain unchanged.

[PBI-050](../../BACKLOG.md#pbi-050-prove-an-in-place-foundation-upgrade-with-component-windows)
adds the existing-deployment scenario with separate Hello and World maintenance
windows. Each consumer stays on Foundation 1.1.0 until its own migration;
the other consumer remains operational. Its acceptance is separate from
PBI-049 and must not be inferred from the existence of two API versions.

Component release versions, supported public API contracts and physical
schema revisions are separate identities. A compatible public extension is
a minor release; a breaking public contract is a major release. The diagram's
Hello/World 2.0.0 labels describe the proposed target consumers; their final
versions must follow actual changes to their own public contracts rather
than automatically matching Foundation's version.

## Agreed breaking-transition sequence

The Product Owner supplied a five-step diagram separating Foundation's PL/SQL
API from its data schema and clarified that the extra arrow represents writes
to both schemas. Changes made through the legacy system must be reflected
in schema 2.0.0. Initial deployment of schema 2.0.0 includes migration of the
existing schema 1.0.0 data; an empty parallel deployment is insufficient.

1. Prepare Foundation 2.0.0 and schema 2.0.0 beside the working 1.0.0 system,
   including initial data migration. Hello and World still use the old path.
2. Introduce Foundation 1.1.0 as a compatible bridge for unchanged consumers.
   It accesses schema 1.0.0 and writes the corresponding changes into schema
   2.0.0. Both consumers continue through this bridge before their windows.
3. During World's maintenance window, migrate World to Foundation 2.0.0 and
   schema 2.0.0. Hello continues reading and writing through Foundation 1.1.0.
4. During Hello's separate maintenance window, migrate Hello to Foundation
   2.0.0. Retain the legacy path temporarily for the agreed recovery window.
5. Retire Foundation 1.1.0 and schema 1.0.0 after checking that no legacy
   requests, sessions or jobs remain and the agreed recovery window has ended.

The diagram's bridge version is a proposed compatible release. Its relationship
to the optional-language 1.1.0 extension must be resolved in design: either one
reviewed release contains both compatible capabilities or the bridge receives
a later compatible version. No two different artifacts may claim the same
version identity. Schema labels describe separate representations; whether
they are separate Oracle schemas or table sets remains a design decision.

## Required design decisions before implementation

Define how live changes are captured during the initial migration and the
interval before the bridge is enabled. A snapshot followed by dual writes
must not omit changes committed between those operations, and a restarted
backfill must not overwrite newer data. Define mappings for identifiers,
inserts, updates and deletes and preserve previously rendered history.

Define transaction ownership and partial-write recovery for the two writes.
The selected mechanism must expose failures and prevent silent divergence.
Whether both writes can share one database transaction depends on the chosen
topology and supported access paths; it is not approved by this scope record.

Classify shared and component-private data. In the mixed-version stage,
Foundation 2.0.0 can originate writes that Hello may need to read through the
old path. Forward propagation alone does not establish that visibility or
rollback after new-version writes. Decide whether legacy readers use a new
representation, selected changes propagate back, or feature/data restrictions
are necessary. Retaining old tables alone is not proof of safe recovery.

Select the PL/SQL binding and deployment mechanism, including treatment of
package state, direct SQL readers, scheduled jobs and existing requests.
Package naming, editions, views, triggers and synchronization tools are
candidates, not selected mechanisms. Resolve how independent maintenance
works within the existing single-application deployment topology.

Define which operations remain available in each stage, maximum permitted
request latency and lock waits, allowed unavailability within each component
window and recovery boundaries. The unaffected component must remain usable;
application-wide maintenance cannot satisfy that requirement. Reconcile
requirements, architecture and exact test commands before construction.

## Planned validation and handover

Run continuous attributable read/write traffic before, during and after each
transition, with separate results for Hello and World. Verify old and new
contracts, shared-data visibility, preserved row contents and configuration,
consistent identifiers and no missing or duplicated accepted writes.

Exercise initial-migration catch-up, concurrent updates during backfill,
failure between corresponding writes, interrupted migration, recovery and
return to legacy operation after new-version writes. Demonstrate component
maintenance enforcement and the other component's continued operation, then
validate legacy retirement only after the final caller leaves.

Specify smoke, unit and integration checks and regression against the
applicable E.1 baseline before execution. Exact commands and measured limits
remain pending managed design. Handover must demonstrate the compatible
extension and the breaking mixed-version sequence, distinguish PBI-049 and
PBI-050 evidence and state unresolved limitations. No runtime tests have been
executed by this planning change.

## Entry gate and relationship to earlier iterations

The [E.2 gap analysis](../E.2/sprint_E.2_proposedchanges.md) establishes the
source-backed direction, remaining blockers and proposed migration roadmap.
The [E.3 APEX-native exercise](../E.3/sprint_E.3_proposedchanges.md) and
[E.4 Git-based exercise](../E.4/sprint_E.4_proposedchanges.md) provide the
applicable technology evidence and supported recommendation. E.5 is the final
currently planned Elaboration step, not an assertion that every architecture
risk is already retired.

Before E.5 implementation, identify and accept the stabilized source capture,
migration, packaging, deployment and testing toolchain with pinned versions
and a reproducible baseline. Demonstrate or explicitly resolve material blockers
from the earlier analysis and exercises. If that gate is unmet, revise the
roadmap with the Product Owner rather than build these complex upgrades on an
unsettled toolchain or claim Construction readiness. Reconcile this retained
scenario with the accepted mechanisms during E.5 managed design; no E.1 custom
controller or unproved native capability is mandated by this scope.
