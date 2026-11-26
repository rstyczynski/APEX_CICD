# E.18 experiment design

Status: self-approved in YOLO mode for corrected measured trials. Initial exploratory dispatch preceded this persisted specification and is excluded from acceptance samples.

## Architecture and measurement

The [setup](sprint_E.18_setup.md) owns scope interpretation; [checklist](sprint_E.18_checklist.md) owns requirement coverage. [E.17 qualified source](../E.17/sprint_E.17_source_review.md) provides the baseline. The preserved source is in [sprint-work/E.18](../../sprint-work/E.18/). GitHub Actions owns a two-replica matrix and max-parallel of one or two. Native SQLcl owns its complete export/stage/verify/release/package/install/upgrade/repeat sequence. Oracle databases and APEX/ORDS remain fresh and isolated per job. A pinned utPLSQL installation executes a real database test before native release work. Instrumentation only observes resources and completed Actions phase timestamps.

Cold trials use unique empty download-cache keys. Warm trials require observed cache hits, with an initial population run excluded from warm counts. The cache covers checksum-verified SQLcl and APEX archives; Oracle image pulls, fresh database startup and native validation remain in every sample. It does not claim whole-machine warmth. JDK setup uses Temurin 21 as in E.17; record actual runtime from logs. Two samples per cell is an implementation choice with poor tail precision: nearest-rank p95 equals the maximum, not a service-level estimate. Serial versus concurrent means independent hosted jobs, not shared-host contention.

### Testing Strategy

Test and regression retain smoke, unit and integration without narrowed scope. New smoke checks workflow syntax and mandatory native steps. Unit checks validate percentile/queue/resource calculations on synthetic records, explicitly not workload performance. Integration downloads actual successful run receipts, checks complete mandatory step success and fresh utPLSQL results, rejects absent/wrong cache evidence and calculates measurements. Full historical smoke/unit/integration run after the new gates pass.

## Test Specification

SM-18: actionlint, Bash syntax, Python compilation and baseline step preservation. UT-18: percentile boundaries, missing/failed samples and queue calculations. IT-18: two real complete replicas in each cold/warm and serial/concurrent cell, artifacts/resources and authoritative API phase times. Traceability: SM protects unchanged validation; UT protects reporting arithmetic; IT establishes PBI-086 observations. These checks are pending implementation/execution and are not represented as passing.

## Retention decision

Measurement workflows and reporting are Elaboration prototypes, retained for reproducibility. No production runner policy changes are made before evidence supports a recommendation.
