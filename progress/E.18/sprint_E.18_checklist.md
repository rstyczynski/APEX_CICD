# E.18 requirement-to-evidence checklist

## Mandatory acceptance

All entries pending until linked execution evidence exists. Authority: [PBI-086](../../BACKLOG.md#pbi-086-measure-complete-pipeline-feedback-and-runner-capacity), [sprint plan](../../PLAN.md#sprint-e18---measure-complete-pipeline-feedback-and-runner-capacity).

- [ ] Complete JDK / qualified SQLcl / utPLSQL / Oracle workload on reproducible E.17 baseline.
- [ ] Declared sample counts, cold/warm phase timings, median/p95 feedback and queue delay.
- [ ] Resource demand and serial/concurrent comparison.
- [ ] Justified capacity/cache recommendation with measurement limits and unchanged mandatory checks/isolation.

## Delivery controls

Authority: Product Owner execution request and [local P8/P9](../../RUPStrikesBack.patch/RUP_patch.md).

- [ ] All new and full regression gates, documentation audit and scoped commits.
- [ ] Live demonstration, rendered/inspected presentation pair and handover.
- [ ] Readable contemporaneous UI captures and offline gallery with verified links/navigation.
- [ ] Recorded closure after all outcomes verified; final push to origin.

## Implementation choices

Two replicas, hosted ubuntu-24.04, concurrency limits one and two, dependency-only caching and fresh databases are design choices, not additional acceptance requirements.
