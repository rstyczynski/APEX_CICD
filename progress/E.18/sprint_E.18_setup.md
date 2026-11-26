# E.18 setup

## Contract

The Product Owner explicitly authorizes activation, YOLO execution, companion repositories and final origin push. Only E.18 and necessary shared documents change. SQLcl PROJECT and Actions retain native responsibilities. No credentials are stored in scratch. No prior completion assertion counts as fresh evidence. Token accounting is unavailable.

## Analysis

[PBI-086](../../BACKLOG.md#pbi-086-measure-complete-pipeline-feedback-and-runner-capacity) and [PLAN](../../PLAN.md#sprint-e18---measure-complete-pipeline-feedback-and-runner-capacity) require complete workload timing on the E.17 baseline. E.17 source has JDK, pinned SQLcl, Oracle, APEX, ORDS and native release checks; utPLSQL must be added to the measured workload. Fresh hosted jobs preserve candidate isolation. The primary actor is SRS A-03 Delivery operator, supported by A-05 Git hosting service; browser validation exercises A-04 application-user behavior. Actions, Oracle and the project-owned pipeline remain internal components under the [SRS actor model](../../docs/srs.md#actors). The operator dispatches a declared experiment, inspects phase/resource/queue receipts, compares distributions and chooses capacity without dropping validation.

## Decisions

Use an Elaboration executable measurement prototype, retaining all E.17 native checks. Use two replicas per serial/concurrent trial and explicitly describe small-sample percentile limits. Cold means a unique empty per-run dependency-cache key; warm means a verified cache hit, not a reused database. Database state remains job-private. No ten-minute process cutoff supersedes the user instruction to persist.
