# Construction entry assessment

## Decision sought

[PBI-080](../../BACKLOG.md#pbi-080-assess-validation-evidence-and-the-construction-entry-decision) requires an evidence-backed recommendation, not production acceptance. Recommend conditional Construction planning for reusable delivery packaging, with explicit exit gates below. The Product Owner Lifecycle Architecture decision is separate and is not made by delegated sprint self-review. [Validation programme](../../docs/validation-programme.md) owns the targeted laboratory risks; [SRS](../../docs/srs.md) owns production requirements and [architecture](../../docs/architecture.md) owns the current mechanisms.

## Targeted risks and evidence

The [E.2 lifecycle assessment](../E.2/sprint_E.2_tests.md) and [E.3 pipeline tests](../E.3/sprint_E.3_tests.md) establish the earlier direction and native lifecycle baseline, with their recorded limits. [E.4 results](../E.4/sprint_E.4_tests.md) distinguish native processes, GitHub pull requests and browser observations in the multi-developer release journey. Its exact-checksum restoration hypothesis failed and the Product Owner explicitly amended that rule; it must not be reported as an unchanged pass. One technical operator performed the roles, so concurrent human-author usability remains unmeasured.

Backend extraction, fixture isolation and meaningful regression: [E.5 tests](../E.5/sprint_E.5_tests.md) exercised real utPLSQL, mutation detection, repeat/reorder and native artifact exclusion. Coverage is measured executable-line coverage on one package, not semantic completeness. [E.6 tests](../E.6/sprint_E.6_tests.md) cover compatibility, competing requests, transaction boundaries and separately observed browser authorization. Supplied native identities alone do not prove password authentication.

Upgrade state and identity: [E.7 tests](../E.7/sprint_E.7_tests.md) cover preserved data, repeat application, injected wrong states and HTTP identity. SQLPlus laboratory migration is not native PROJECT deployment qualification. [E.3 tests](../E.3/sprint_E.3_tests.md) retain the native pipeline baseline; current Git/tool version selection remains governed by NFR-5.

Integrated candidate selection and fail-closed aggregation: [E.8 tests](../E.8/sprint_E.8_tests.md) exercise real Oracle cadences and specific negative outcomes. [E.9 tests](../E.9/sprint_E.9_tests.md) exercise the review service and trust/freshness controls; report presence does not establish independent human endorsement. Hosted governance and organization bypass policy remain deployment decisions.

Privileged validation, concurrency and interrupted cleanup: [E.10 tests](../E.10/sprint_E.10_tests.md) establish the tested container boundary, concurrent stream independence, timeout and orphan recovery. Host/kernel compromise remains untested. [E.11 completion](../E.11/sprint_E.11_completion.md) establishes a technical second operator with fresh private access on the same kernel. Full new-host APEX/SQLcl reproduction and nested resource enforcement remain unqualified; they must not be represented as achieved.

Compatible expansion and live catch-up: [E.12 tests](../E.12/sprint_E.12_tests.md) own their finite concurrent-change experiment. [E.13 tests](../E.13/sprint_E.13_tests.md) establish paired-write rollback, rendered/structured equality, return and guarded retirement. [E.14 tests](sprint_E.14_tests.md) add separate component windows and interrupted route-switch recovery. These experiments disprove any assumption that a successful rollback of DML proves DDL rollback or that two API entry points alone prove isolated maintenance. Explicit route/fencing and recovery mechanisms are necessary.

## Conditional and untested production cases

The retained Foundation fixtures have controlled callers and finite traffic. They do not discover all real APEX sessions/jobs, fence active requests across hosts, establish zero downtime under arbitrary load, prove process/host crash recovery or qualify a production release package with both schema contracts. Browser rollout and arbitrary language/template evolution remain outside this sample. Credential-source compliance remains the explicit temporary prepared-host exception in [AGENTS](../../AGENTS.md), not resolved production NFR-4 compliance.

## Proposed Construction sequence

First reconcile reusable product boundaries and production requirements with the Product Owner, resolve the credential-source exception and select supported host/tool versions. Next package the validated backend and migration mechanisms with native release identities and pinned NFR-5 qualification, preserving existing data and repeat behavior. Then implement real caller discovery, per-component request fencing, interrupted deployment recovery and operational telemetry; validate all entry points under concurrent traffic. Next integrate the privileged validation service into the selected GitHub governance boundary and qualify cancellation, cleanup and freshness on the intended runner hosts. Finally reproduce the complete APEX/native deployment on a clean host with independently attributable operation, measure supported workload availability and perform production readiness review. These are proposed work packages, not newly registered PBIs or automatic sprint assignments.

## Acceptance boundary

No completed experiment grants production acceptance or advances the project lifecycle. Evidence supports conditional Construction planning; unresolved production risks above must be explicitly accepted, assigned or retired at the separate milestone decision. [Checklist](sprint_E.14_remaining_work.md) owns sprint acceptance mapping.

## Existing backlog and governance disposition

The [production follow-up inventory](production_follow_up.md) enumerates existing Proposed items, their exact root definitions and a proposed dependency grouping without changing Product Owner priorities or assigning sprints. The five root-backlog/PLAN status discrepancies for E.10 and E.13 were resolved on 2026-11-26 at the Product Owner’s explicit request: PBI-072, PBI-073, PBI-074, PBI-049 and PBI-082 now record Done in BACKLOG, matching their existing sprint assignments and Done board rows. The [resolution record](production_follow_up.md#recorded-lifecycle-inconsistencies) traces the correction to acceptance tests, handover decisions and closure evidence, and explains the previous interpretation. This resolves the recorded inconsistency; the separate Product Owner Lifecycle Architecture decision remains pending.

## Evidence freshness

Earlier sprint reports retain their recorded run dates, tool builds and experiment scopes. E.14's fresh full regression re-executes the registered current cases; it does not repeat every historical manual browser observation, hosted workflow or independent-operator journey. A test log or direct observation supports only its stated behavior. Prior closure prose is used to locate decisions, not to establish a successful behavior by itself. The five backlog status corrections use the retained acceptance and closure evidence under the Product Owner’s reconciliation request; no fresh runtime result or production acceptance is inferred.

## Lab interruption and recovery

The corrected-registry integration run encountered a 300-second ORDS installer timeout and unavailable Oracle instances. [Recovery evidence](tests/environment-recovery.md) records supported SQL startup, restored ORDS, preserved demonstration data and the unchanged-source retry. The lab interruption’s cause remains undiagnosed. Recovery, data-preservation checks and regression passed. This incident leaves no E.14 acceptance criterion unfinished.
