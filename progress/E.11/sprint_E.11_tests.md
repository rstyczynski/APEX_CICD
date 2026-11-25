# E.11 verification

## Gates

A1 smoke 1/1, A2 unit 1/1, A3 integration 1/1, B1 full smoke 9/9 and B2 full unit 8/8 runner entries passed. These counts describe runner entries, not assertion counts. Initial unit skeleton failed with ModuleNotFoundError as expected; tests/red.log preserves it. No failed gate was waived.

Commands used bash tests/run.sh --smoke/--unit/--integration --new-only progress/E.11/new_tests.manifest for A1/A2/A3, and bash tests/run.sh --smoke and --unit for unfiltered B1/B2. The [walkthrough](sprint_E.11_increment_demo.md) gives runnable commands and required environment. Syntax smoke proves parsability only. Unit integrity/statistics cases use synthetic bytes. Integration performs six real isolated candidate executions through the controller loaded from a verified-clean full Git clone, three fresh downloads, three cache hits, runtime checks, cache-integrity challenges and scoped container/image cleanup. Credential markers were absent from reusable archives and receipt; no candidate log prints the marker. This is not a comprehensive arbitrary-host log/cache audit or proof of production isolation.

## Measurements

Three observations per mode; units seconds. Nearest-rank 95th percentile is the maximum for this sample size. Empty-cache transfer is 4,038,406 bytes per cold sample and zero per warm sample. Checkout duration is recorded separately in tests/benchmark.json and excluded from paired setup phases. Shared host and VM caches are uncontrolled.

acquire: cold median 1.4831s / p95 2.2197s; warm median 0.0001s / p95 0.0001s.

validate: cold median 0.0046s / p95 0.0047s; warm median 0.0018s / p95 0.0018s.

import: cold median 0.3905s / p95 0.4262s; warm median 0.3298s / p95 0.3515s.

execute: cold median 0.2796s / p95 0.2970s; warm median 0.2645s / p95 0.2837s.

cleanup: cold median 0.3223s / p95 0.3314s; warm median 0.3285s / p95 0.3300s.

## Decision

Keep one worker and reuse only verified public tool bytes. The acquisition savings justify archive reuse for this slice. Serial measurements do not justify another worker or establish throughput improvement. Proposed next experiment: twenty observations per mode; investigate setup above fifteen seconds or execution above five seconds before changing capacity. These are proposed budgets, not acceptance thresholds. Actual tools and exact source revision/hash are in the receipt.

## Remaining verification

PLAN's separately attributable second operator with newly supplied private service access remains unverified. These measurements used the prepared service. Full APEX/SQLcl clean-host setup, forced termination of this benchmark driver and production runner caches are outside the selected slice, not passing cases. The [blocker audit](sprint_E.11_blockers.md) explains the mandatory remaining operator criterion.

## Artifacts

[test_run_A1_smoke_20261125.log](test_run_A1_smoke_20261125.log), [test_run_A2_unit_20261125.log](test_run_A2_unit_20261125.log), [test_run_A3_integration_20261125.log](test_run_A3_integration_20261125.log), [test_run_B1_smoke_20261125.log](test_run_B1_smoke_20261125.log), [test_run_B2_unit_20261125.log](test_run_B2_unit_20261125.log), [benchmark.json](tests/benchmark.json), [red.log](tests/red.log), [presentation validation](tests/presentation-validation.json). tests/initial_probe.* and tests/controller_run.* are diagnostic intermediate executions, excluded from final acceptance. All gate logs above were captured on 2026-11-25; their filenames identify that execution date rather than second-level timestamps.
