# E.13 verification

## Current results

All six gates PASS with zero failures and no retries: A1 smoke 1/1, A2 unit 1/1, A3 real Oracle integration 1/1; B1 full smoke 12/12, B2 full unit 13/13, B3 full integration 22/22. Counts are registered runner entries; individual entries may execute multiple assertions or experiments. [Final gate receipt](tests/final-gates.json) binds totals and confirms all 248 source files match before/after regression and current source. No threshold waiver was used.

Smoke proves the driver parses. Unit runs synthetic equality rejection checks only; it proves no database outcome. Real integration proves the observed paired-write rollback, session-interruption rollback, 160 mixed transactions, rendered/structured equality, retained historical greeting/settings, pre-retirement return, early retirement rejection and post-retirement new calls. A finite sample does not prove unbounded availability. No real browser or production deployment is claimed.

## Reproduction

The [walkthrough](sprint_E.13_increment_demo.md) explains the driver, SQL, prerequisites and expected results before invocation. The registered test runner selects the named functions from the sprint manifest and fails on any nonzero function. New gates use `bash tests/run.sh --smoke --new-only progress/E.13/new_tests.manifest`, then the same command with --unit and --integration. Full regression uses `bash tests/run.sh --smoke`, then --unit and --integration. Historical integration uses its existing isolated Oracle fixture and native toolchain checks; this is real execution, not a replayed PASS file. See [test profile](../../docs/test-profile.md).

## Artifacts

[test_run_A1_smoke_20261125_220026.log](tests/test_run_A1_smoke_20261125_220026.log)

[test_run_A2_unit_20261125_220026.log](tests/test_run_A2_unit_20261125_220026.log)

[test_run_A3_integration_20261125_220026.log](tests/test_run_A3_integration_20261125_220026.log)

[test_run_B1_smoke_20261125_220033.log](tests/test_run_B1_smoke_20261125_220033.log)

[test_run_B2_unit_20261125_220037.log](tests/test_run_B2_unit_20261125_220037.log)

[test_run_B3_integration_20261125_220045.log](tests/test_run_B3_integration_20261125_220045.log)


## Full regression and evidence preservation

Full integration freshly reconstructed and promoted the historical accepted source in the owned separate database fixture, exercised authenticated HTTP greetings, preserved UAT data through both supported patch starts and checked compatibility/drift rejection and repeat no-op. Later entries exercised backend contracts, candidate controls, review service, isolated execution, reproducibility, E.12 expansion and the current E.13 bridge. Recorded seed readers remain readers of historical hosted evidence, not a new hosted deployment or PR. The gate's output states these distinctions.

The [relocation inventory](tests/regression-evidence-relocation.json) maps fresh outputs from prior-sprint default paths into this sprint. All 59 overwritten tracked historical outputs were restored exactly to their original Git bytes; 119 new outputs were moved here. Their raw paths remain as executed. [Native regression source/tool/environment receipts](tests/regression-generated/progress/E.12/tests/legacy-regression/run-20261125T230045-92924/) support the full result. No prior sprint evidence is changed by this delivery.

[Walkthrough command verification](tests/walkthrough-command-validation.json) records successful execution of every copyable shell block. [Availability observations](tests/availability-observations.json) record about 4.786 seconds of overlapping real traffic; the largest observed completion gap was about 0.0942 seconds, including deliberate pacing. These are observations, not production guarantees. [Database](tests/database-version.log) and [SQLPlus](tests/sqlplus-version.log) record 23.26.3.0.0. Historical native PROJECT processing separately qualified SQLcl 25.3.0.274.1210 before target preparation.

[Mutation sensitivity](tests/atomicity-mutation-red.log) is an expected failing test-only variant with rollback omitted; it specifically fails ORA-20121 partial history. It is not a failed mandatory gate or a legitimate implementation run. Positive current-code runs, including full regression's tests/run_13854, pass independently. The earlier initial run retains its own older driver hash and is not used as evidence for subsequently added interruption checks.
