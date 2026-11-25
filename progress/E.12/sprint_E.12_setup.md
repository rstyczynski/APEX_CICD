# E.12 setup

## Contract

Product Owner explicitly authorized activation and YOLO execution on 2026-11-25, overriding P5 personal field editing. No remote writes or other sprint activation. Existing CLI broker changes are unrelated and excluded. PLAN now selects only E.12; phase identifiers follow patch P0.phase. Elaboration constructs an isolated Oracle experiment, not a production rollout. No prior E.12 evidence existed.

## Analysis

Actors: delivery operator performs expansion, interruption and recovery; unchanged Hello and World consumers read/write through the legacy PL/SQL contract; migration operator backfills and reconciles. Journey: establish 1.0 history/settings, run both consumers, expand additively to 1.1, interrupt migration, accept concurrent changes, resume and compare at a selected boundary.

[Backlog](../../BACKLOG.md) PBI-048 and PBI-081 own acceptance; [PLAN](../../PLAN.md) owns scope and all three test/regression levels. [SRS](../../docs/srs.md), [architecture](../../docs/architecture.md), [test profile](../../docs/test-profile.md) and [original scenario](../E.5/sprint_E.5_proposedchanges.md) remain authoritative. Requirement evidence is tracked in the [design](sprint_E.12_design.md). Existing prepared Oracle 23.26.3 responds to local OS-authenticated SQLPlus. No credentials are copied into scratch.
