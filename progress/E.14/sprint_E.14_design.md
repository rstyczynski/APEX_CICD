# E.14 design

Status: Accepted

The design was self-approved under YOLO before construction; this explicit status field materializes that recorded decision. This is a retained Elaboration experiment, not production rollout.

## Actors and journey

The operator upgrades the Foundation schema/API in place, then migrates Hello and World separately. The unaffected consumer continues committed reads and writes. The operator interrupts one component migration, verifies its rollback/restart, and completes the other window. The Product Owner reviews accumulated risks and separately decides Lifecycle Architecture acceptance.

## Mechanism

Reuse the E.13 bridge setup in the same experiment schema, initially routing both components through legacy API. A per-component maintenance flag rejects requests only for that component. Route switch and migration journal update share a transaction; session termination before commit must restore the old route. Independent traffic runs throughout each window and through recovery. Keep original history/settings and compare both representations. Bridge registry and maintenance flags are implementation choices, not prescribed acceptance requirements.

### Testing Strategy

Test and regression: smoke, unit, integration, full scope. Smoke parses the driver. Unit challenges route/state assertions with synthetic inputs and proves no database availability. Integration uses real Oracle sessions, deliberate uncommitted termination and committed unaffected-consumer traffic. Expected duration is seconds for the focused experiment; historical full regression may take minutes.

## Test Specification

SM-1: driver syntax. UT-1: reject missing/invalid route states. IT-1: legacy baseline, Hello maintenance with World traffic, interrupted Hello route switch and restart, mixed-version traffic, World maintenance with Hello traffic, final route/history/configuration assertions. All map to PBI-050. PBI-080 uses a source-linked assessment of targeted risks and conditional Construction sequencing. Finite traffic proves sampled availability only. Browser operation and production deployment remain unverified.

## Related authority and delivery records

[Setup](sprint_E.14_setup.md) owns the authorized scope and constraints. [SRS](../../docs/srs.md) owns product requirements; [architecture](../../docs/architecture.md) owns the existing mechanism and [test profile](../../docs/test-profile.md) owns command mapping. [Implementation](sprint_E.14_implementation.md) realizes this design and [test record](sprint_E.14_tests.md) owns observed outcomes. The [checklist](sprint_E.14_remaining_work.md) maps accepted criteria to evidence.
