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

[test_run_A1_smoke_20261125_193917.log](test_run_A1_smoke_20261125_193917.log), [test_run_A2_unit_20261125_193918.log](test_run_A2_unit_20261125_193918.log), [test_run_A3_integration_20261125_193751.log](test_run_A3_integration_20261125_193751.log), [test_run_B1_smoke_20261125_193920.log](test_run_B1_smoke_20261125_193920.log), [test_run_B2_unit_20261125_193926.log](test_run_B2_unit_20261125_193926.log), [benchmark.json](tests/benchmark.json), [red.log](tests/red.log), [presentation validation](tests/presentation-validation.json). tests/initial_probe.* and tests/controller_run.* are diagnostic intermediate executions, excluded from final acceptance. All gate logs above were captured on 2026-11-25; their filenames record UTC completion timestamps.

## Resume verification — 2026-11-25

At source e528e42, reran A1/A2/A3 and full B1/B2 in order. All passed: 1/1, 1/1, 1/1, 9/9 and 8/8 runner entries respectively. Exact commands were `bash tests/run.sh --smoke --new-only progress/E.11/new_tests.manifest`, the same with `--unit` and `--integration`, followed by `bash tests/run.sh --smoke` and `bash tests/run.sh --unit`. Integration again performed six real executions, three empty-cache downloads, three warm hits, integrity rejection and cleanup. This proves repeatability on the prepared service, not second-operator access. Preserved the historical benchmark and prior tracked regression outputs after the run; the new gate logs retain the observed fresh results. Slide measurements remain the original baseline.

[test_run_A1_smoke_resume_20261125_194958.log](test_run_A1_smoke_resume_20261125_194958.log)

[test_run_A2_unit_resume_20261125_194958.log](test_run_A2_unit_resume_20261125_194958.log)

[test_run_A3_integration_resume_20261125_194958.log](test_run_A3_integration_resume_20261125_194958.log)

[test_run_B1_smoke_resume_20261125_194958.log](test_run_B1_smoke_resume_20261125_194958.log)

[test_run_B2_unit_resume_20261125_194958.log](test_run_B2_unit_resume_20261125_194958.log)


## Technical-operator completion gates

Latest A1 1/1, A2 1/1, A3 2/2 (primary and real technical second operator), full B1 9/9 and B2 8/8 passed. Exact commands remain the standard manifest-filtered new gates and unfiltered regressions. Logs: [A1](test_run_A1_smoke_operator_20261125_200144.log), [A2](test_run_A2_unit_operator_20261125_200144.log), [A3](test_run_A3_integration_operator_20261125_200144.log), [B1](test_run_B1_smoke_operator_20261125_200144.log), [B2](test_run_B2_unit_operator_20261125_200144.log). New connection selection first failed as specified; [red evidence](tests/connection-red.log). The final live repeat additionally retained the exact selected-source Git bundle, without changing workload assertions.

The [second-operator receipt](tests/second-operator/receipt.json) records uid, fresh certificate fingerprint, source hashes/snapshot, pinned image and cleanup. [Execution log](tests/second-operator/execution.log) records all six sample successes. [Unauthenticated rejection](tests/second-operator/denied-without-certificate.log) proves the endpoint requires newly supplied client access; it does not prove general network security. [Engine information](tests/second-operator/engine-info.json) records actual nested runtime configuration. [Source bundle](tests/second-operator/source.bundle) retains the exact clean selected-source snapshot.

Historical failed attempts are preserved in tests/second-operator/cgroup-failure.log, empty-log-failure.log and failure-before-diagnostic-fix.log. Synthetic candidate tokens in failure diagnostics are redacted; no TLS private material is retained. The final successful receipt supersedes intermediate failure.log. The cgroup failure specifically showed missing memory.max; supported nested mode disables cgroups. CPU/memory/PID enforcement is not qualified. Empty remote logs were repaired by explicit k8s-file logging in the shared controller; all prior smoke/unit regression passed with that change. Host provisioning SSH requests were rejected before execution; no host-account mutation occurred.

The second-operator timing receipt is a separate environment measurement and is not substituted for baseline slides or treated as an isolated caching speedup across different runtimes. Full APEX/SQLcl/new-kernel/human-operator reproduction remains outside this selected slice. All assigned mandatory criteria are now evidenced within the stated scope.


Baseline preservation: tests/benchmark.json is restored to its original 5866c23 measured bytes, which own the slide comparison. tests/benchmark-resume-baseline.json preserves the subsequent resume snapshot. The latest primary A3 execution receipt is tests/primary-operator-rerun.json; the technical operator has its separate receipt. No measurements were recalculated or substituted across runtime contexts.
