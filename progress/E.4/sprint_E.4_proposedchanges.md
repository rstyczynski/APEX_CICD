# E.4 Git-based feature-centric APEX development

## Decision, sources and status

This planned exercise was renumbered from E.3 to E.4 on 2026-10-19 when
the Product Owner inserted an additional Elaboration iteration. The
[E.2 gap analysis](../E.2/sprint_E.2_proposedchanges.md) now assesses E.1 and
informs later refinement; [complex upgrades](../E.5/sprint_E.5_proposedchanges.md)
are deferred to E.5 after toolchain stabilization.
References in this scope record use the new numbering; assignments and
acceptance criteria remain unchanged by the renumbering.

On 2026-10-19 the Product Owner requested splitting the Oracle-style exercise
into E.3 and E.4. E.4 is Planned in managed mode; this pre-sprint scope record
does not start execution or approve an implementation. E.3 demonstrates
APEX-native team-centric work; E.4 independently demonstrates external Git
feature integration using App Builder in private APEX environments.

The [plan](../../PLAN.md#sprint-e4---validate-git-based-feature-centric-development)
owns assignments and status, the [backlog](../../BACKLOG.md) owns item
definitions and the [board](../../PROGRESS_BOARD.md) tracks the assigned rows.
The [E.3 record](../E.3/sprint_E.3_proposedchanges.md) owns the shared native
release/test foundation and the earlier paper-to-backlog review. The
[SRS](../../docs/srs.md) owns requirements, the [architecture](../../docs/architecture.md)
owns mechanisms, and the [test profile](../../docs/test-profile.md) must define
exact approved commands before code-bearing execution. The
[README](../../README.md) and [roadmap](../../ROADMAP.md) orient the reader.
Use the supplied [Oracle lifecycle paper](../../refs/apex-lifecycle-management-v3.pdf),
especially pp. 32–39 for the feature-centric journey and pp. 40–44 for pipelines.
Preserve the [E.1 assessment](../E.1/sprint_E.1_assessment.md) as historical
evidence when comparing approaches.

## Strict acceptance requirement

The Product Owner requires exact mapping to the paper and applicable official
Oracle documentation, plus an evidence-based comparison against E.1. The
[shared strict traceability and comparison contract](../E.3/sprint_E.3_proposedchanges.md#strict-oracle-traceability-and-comparison-contract)
is mandatory for this sprint. Before implementation, map every scenario and
material failure flow to paper pages/sections and version-specific Oracle
documentation, and approve the comparison protocol. At handover, provide
the executed source/evidence map, justified deviation decisions and the
E.4-versus-E.1 comparison under PBI-046. Inherited E.3 capabilities must be
revalidated for changed versions, sources and artifacts.

The final decision package compares all three approaches: E.1 custom delivery,
E.3 APEX-native team-centric and E.4 Git-based feature-centric development.
Use matched scenario results and comparable effort/runtime/resource and
maintenance measures. Preserve historical evidence, mark missing measurements
unavailable and distinguish new Oracle scenarios from common parity tests.
Provide a supported recommendation and record the Product Owner's decision
or explicit deferral. A narrative preference, unverified documentation link
or previous E.3 pass does not satisfy these acceptance gates.

## Boundary between the two approaches

E.3 integrates developer changes in the live APEX Main application through
Working Copy comparison/refresh/merge. A coordinated team checkpoint is then
exported, reviewed and committed into Git for release history and distribution.
E.4 integrates exported definitions and migrations through a Git feature
branch, PR feedback, combined validation and merge to Git main. A native
artifact from the accepted revision updates central APEX DEV afterward.

Both use App Builder, SQLcl PROJECT and Git. Working Copies are not Git
branches, APEX Main is not Git main, and neither merge synchronizes the other.
E.4 does not require a Working Copy inside every private branch environment.
Central page locks may communicate coordination, but are not evidence of
atomic component reservations or deployment exclusivity.

## Assigned items and dependencies

[PBI-019](../../BACKLOG.md#pbi-019-prove-parallel-component-collaboration-and-integration)
owns actual independent, overlapping Hello/World work and integration.
[PBI-020](../../BACKLOG.md#pbi-020-complete-apex-capture-and-reconstruction-validation)
owns full supported private-target identity, deletion, shared-definition and
retained-user-state reconstruction checks. These extend E.3's basic native
capture/adoption foundation rather than being claimed complete by it.

[PBI-042](../../BACKLOG.md#pbi-042-synchronize-central-development-after-accepted-merges)
owns accepted-merge synchronization and unsafe-refresh rejection.
[PBI-017](../../BACKLOG.md#pbi-017-deliver-a-repository-and-pipeline-reference-guide)
owns the consolidated guide with separately navigable native-APEX and Git
paths. [PBI-046](../../BACKLOG.md#pbi-046-compare-and-independently-reproduce-the-oracle-style-laboratory)
owns independent reproduction, comparison with E.1 and E.3, and the supported
architecture recommendation. No new backlog definition or duplicate assignment
is needed for this split.

Entry requires E.3's applicable accepted toolchain, capture/staging,
release/deployment, mappings, tests, audits and pipeline baseline with exact
versions and resource constraints. If an entry dependency failed, resolve it
explicitly before dependent implementation; do not assume sprint closure
means the capability passed. E.4 needs its own activation and managed design.

## Separate use-case and acceptance exercise

For UC-8/9, provision private branch environments from the identified accepted
revision. Validate the paper's matching workspace name/ID and APEX patch-level
requirements, stable application identities and real resource budget. Distinct
workspaces within one instance are not automatically the branch-instance
pattern described on p. 34. Native inadequacy requires observed evidence
before an alternative is proposed. Preserve the stronger existing ownership
requirements until an explicit requirement decision changes them.

For UC-10, B and C make independent Hello/World changes during overlapping
work periods, author necessary migrations, test and export/stage into their
respective feature branches. Demonstrate supported page deletion and shared
definitions, stable recapture and saved-user-state preservation across the
claimed replacement/import path. Detect missing dependencies, collisions,
undeclared ownership changes and unsafe overwrite. A sequential replay of
historical commits does not pass parallel collaboration.

For UC-7, update a feature branch from newer Git main, preserve both developers'
intent, resolve a controlled same-source conflict, validate the combined
candidate and show a reviewer feedback/correction cycle before accepting the
merge. Changed branch/base revisions invalidate earlier validation. The PR
and check evidence must identify the actual source and participants; narrative
descriptions of a hosted review do not prove execution. External messaging or
publication still needs its applicable authorization.

For UC-4/11, generate/deploy the accepted native artifact into central DEV,
verify the combined behavior and show a stale or unexported-work case that
blocks unsafe synchronization. Qualify and promote the feature-integrated
release using E.3's native pipeline and record fresh results and source/artifact
identity. Re-run relevant utPLSQL, measured coverage, Cypress, audit and
preservation regression. E.3's earlier pass cannot qualify changed bytes.
This is E.4 integration/regression evidence, not a second assignment or
retrospective reopening of PBI-038/040/043/045.

For UC-5/6, retain the bounded incompatibility/drift/failed-additive-repair
behavior while independently reconstructing this workflow from a clean
checkout with new target state and credentials. Record browser evidence
separately from API fixtures. Unsupported failure/concurrency states stay
explicitly open; the broader PBI-018/022/023/024 remain unscheduled.

Compare E.3 and E.4 on the same supported change scenario: where isolation and
integration occur, review granularity, shared schema exposure, conflict
handling, source provenance, operating steps, elapsed runtime, resource use
and maintained custom code. Also compare applicable outcomes against E.1's
actual evidence. Mark absent historical measurements unavailable rather than
fabricating a numerical baseline. Explain when each approach fits and what
would be required before selecting production operation.

## Exit and delivery

All five assigned items require their own acceptance evidence. The consolidated
guide must let an operator select one complete approach without accidentally
combining APEX and Git merge semantics. Provide a runnable feature-centric
walkthrough, independent reproduction, a live review and an evidence-backed
architecture recommendation. Preserve E.3's own operating guide and evidence.
Lifecycle Architecture acceptance and sprint closure remain separate Product
Owner decisions. No duration is inferred from this planned split; estimate
resources and effort at setup without dropping committed scenarios silently.
