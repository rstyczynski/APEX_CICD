# E.18 experiment design

Status: self-approved in YOLO mode for corrected measured trials. Initial exploratory dispatch preceded this persisted specification and is excluded from acceptance samples.

[Architecture](../../docs/architecture.md#e18-capacity-experiment) owns native responsibilities; [test profile](../../docs/test-profile.md#e18-pipeline-capacity-experiment) owns suite invocation. [Implementation](sprint_E.18_implementation.md), [measured report](capacity_report.md) and [gallery](screenshots/index.html) provide the actual outcome and visual evidence.

## Architecture and measurement

The [setup](sprint_E.18_setup.md) owns scope interpretation; [checklist](sprint_E.18_checklist.md) owns requirement coverage. [E.17 qualified source](../E.17/sprint_E.17_source_review.md) provides the baseline. The preserved source is in [sprint-work/E.18](../../sprint-work/E.18/). GitHub Actions owns a two-replica matrix and max-parallel of one or two. Native SQLcl owns its complete export/stage/verify/release/package/install/upgrade/repeat sequence. Oracle databases and APEX/ORDS remain fresh and isolated per job. A pinned utPLSQL installation executes the existing five-case backend/API suite before native release work. The suite uses its own authenticated E5_TEST schema; no SYS inheritance grant is added. Instrumentation only observes resources and completed Actions phase timestamps.

Cold trials use unique empty download-cache keys. Warm trials require observed cache hits, with an initial population run excluded from warm counts. The cache covers checksum-verified SQLcl and APEX archives; Oracle image pulls, fresh database startup and native validation remain in every sample. It does not claim whole-machine warmth. JDK setup uses Temurin 21 as in E.17; record actual runtime from logs. Two samples per cell is an implementation choice with poor tail precision: nearest-rank p95 equals the maximum, not a service-level estimate. Serial versus concurrent means independent hosted jobs, not shared-host contention.

### Testing Strategy

Test and regression retain smoke, unit and integration without narrowed scope. New smoke checks workflow syntax and mandatory native steps. Unit checks validate percentile/queue/resource calculations on synthetic records, explicitly not workload performance. Integration downloads actual successful run receipts, checks complete mandatory step success and fresh utPLSQL results, rejects absent/wrong cache evidence and calculates measurements. Full historical smoke/unit/integration run after the new gates pass.

## Test Specification

SM-18: actionlint, Bash syntax, Python compilation and baseline step preservation. UT-18: percentile boundaries, missing/failed samples and queue calculations. IT-18: two real complete replicas in each cold/warm and serial/concurrent cell, artifacts/resources and authoritative API phase times. Traceability: SM protects unchanged validation; UT protects reporting arithmetic; IT establishes PBI-086 observations. These checks are implemented and pass in the [six-gate test record](sprint_E.18_tests.md). The specification above describes intended proof; that record distinguishes actual execution from synthetic contracts.

## Retention decision

Measurement workflows and reporting are Elaboration prototypes, retained for reproducibility. No production runner policy changes are made before evidence supports a recommendation.

## Timestamp and cold-state limits

API job creation can precede matrix admission. Report raw workflow-to-job-creation and job-creation-to-start intervals without calling either a pure infrastructure queue or admission duration. Total workflow-to-start wait includes both. Hosted JDK preinstallation and possible base-image Docker layers remain outside the archive-cache treatment; cold does not mean all tool binaries were absent. These limits preserve observable measurements rather than inventing timing attribution.

## Actor-led experiment journey

Primary actor: SRS A-03 Delivery operator; supporting actor: A-05 Git hosting service. The job's real browser test exercises A-04 application-user behavior. [SRS](../../docs/srs.md#actors) owns these actor definitions and the system boundary; Oracle and the project-owned Actions pipeline remain components. This experiment supports UC-4/UC-6 without introducing a new production functional requirement.

Preconditions are authorized workflow dispatch, pinned source/downloads and available ephemeral hosted runner slots. The operator chooses a cache/admission cell, dispatches two replicas, follows native phase outcomes, inspects backend/application/preservation/cleanup receipts, then admits only qualified samples to the four-cell comparison. Success is a source-consistent measured cohort and a bounded capacity/cache recommendation traced to PBI-086.

Alternative flows preserve failure truth: failed native installation or invoker rights excludes a trial and triggers a corrected fresh run; a warm cache miss excludes that sample until cache population and a real hit; mismatched source/artifact/tool inputs are rejected by unchanged native safety checks before target mutation. Full regression is independent of timing admission. Human review/merge lead time is not measured by this native workload experiment; the full regression retains its existing control checks.

Serial/concurrent describes each workflow matrix admission limit. Distinct cohorts, cache population and live work can overlap in wall-clock time; an account-wide quiet baseline and controlled causal hardware/cache comparison are not established.
