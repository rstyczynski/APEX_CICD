# E.12 test execution

## Current results

New smoke and unit passed 1/1 runner entries each. Real Oracle integration passed after correcting SQLPlus settings and transaction granularity. The latest direct run additionally compared unchanged legacy PL/SQL source and rejected unsupported language with ORA-20002. Source/target equality is checked under a shared source lock; no continuous replication after that boundary is claimed. Each consumer accepted 120 separate transactions without error. Raw server timestamps show actual requests across the expansion and catch-up interval. Preserved configuration is language=en; history identity 1 is intentionally updated, 2 intentionally deleted, 3 intentionally inserted. These changes are journal-attributed to E12_CONCURRENT.

Full smoke and unit regression passed 10/10 and 9/9 entries. One full integration execution recorded 16/20 with four failures. The timestamped B3 gate also completed at 16/20 with the same four failures. The method's 80% integration threshold does not resolve the Product Owner's instruction to repair failures. No sprint completion is claimed.

## Failure diagnosis

Assembly's HTTP assertion expected public Foundation text; current application redirects to authenticated login. A current cookie-enabled HTTP probe confirms P9999_USERNAME/P9999_PASSWORD. Its SQL checks passed. Full release test is a deliberate return-1 stub reporting full upgrade/reconstruction acceptance pending. Patch result fails ORA-20987 because APEX application 810004 is absent for E1_INTEGRATION. Drift injection requires ready retained E1_UAT; it rejects the current state before injection. These are unresolved regression work, not proven external blockers. Restoring old targets without understanding their retained state would be unsafe; isolated replay and current supported repair need investigation.

## Commands and proof boundaries

The [walkthrough](sprint_E.12_increment_demo.md) explains the SQL and exact runnable integration command. New gates use bash tests/run.sh --smoke, --unit and --integration with --new-only progress/E.12/new_tests.manifest; regressions use the same levels without that filter. Smoke proves Python syntax only. Unit cases use synthetic tuples and prove the equality assertion detects stale, missing and duplicate rows. Integration actually invokes Oracle through separate SQLPlus sessions; it does not prove an APEX browser journey or native SQLcl PROJECT packaging. No source/distribution export or deployment was performed.

## Artifacts

[test_run_A1_smoke_20261125_202003.log](test_run_A1_smoke_20261125_202003.log)

[test_run_A1_smoke_20261125_202139.log](test_run_A1_smoke_20261125_202139.log)

[test_run_A2_unit_20261125_202004.log](test_run_A2_unit_20261125_202004.log)

[test_run_A2_unit_20261125_202139.log](test_run_A2_unit_20261125_202139.log)

[test_run_A3_integration_20261125_202028.log](test_run_A3_integration_20261125_202028.log)

[test_run_A3_integration_20261125_202044.log](test_run_A3_integration_20261125_202044.log)

[test_run_A3_integration_20261125_202154.log](test_run_A3_integration_20261125_202154.log)

[test_run_B1_smoke_20261125_202156.log](test_run_B1_smoke_20261125_202156.log)

[test_run_B2_unit_20261125_202204.log](test_run_B2_unit_20261125_202204.log)

[test_run_B3_integration_20261125_202621.log](test_run_B3_integration_20261125_202621.log)

[Real experiment receipt](tests/experiment.json), [expansion](tests/expand-backfill.log), [catch-up](tests/catchup.log), [assertions](tests/assertions.log), [Hello](tests/hello.log), [World](tests/world.log), [unsupported language](tests/unsupported-language.log), [presentation validation](tests/presentation-validation.json), [slide montage](tests/presentation-montage.png). tests/regression-integration.log records the separately observed 16/20 run; it is not substituted for the in-progress timestamped gate.


Final full integration gate: [B3](test_run_B3_integration_20261125_202621.log). Both full runs observed the same failures. Historical tracked test outputs changed by regression were copied under tests/regression-generated/ and restored to their Git baseline, preserving other sprint evidence.
