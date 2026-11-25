# E.7 — Test results

[The design](sprint_E.7_design.md) defines selected cases; [implementation](sprint_E.7_implementation.md) identifies their limits and outstanding work. [The test profile](../../docs/test-profile.md) remains the shared command authority.

## Executed results

A1 smoke passed 1/1. A2 unit passed its wrapper and six underlying integrity cases: valid, changed migration, changed report, changed manifest, missing report and empty report. A3 integration passed 1/1: real Oracle preservation, upgrade/repeat, selected consumers, five injected wrong states and metadata. The final rerun also verifies actual HTTP output after baseline, upgrade and repeat. B1 full smoke passed 5/5. B2 full unit passed 4/4, including retained E.1 SQL tests, E.5 utPLSQL and E.6 consumers. No integration failure was waived. The expected initial red test is retained separately.

SQLcl qualification recorded release 25.4.1.0 and build 25.4.1.022.0618 before mutation. SQLPlus executed these explicit laboratory SQL migrations; this is not native SQLcl PROJECT deployment evidence.

Native Chrome visually showed Installed release, Application release 1.1.0 | Greeting contract 1.1.0, and footer 1.1.0. Browser-tab access failed, but native Chrome controls succeeded. This observation is separate from HTTP and database metadata checks. No independent Product Owner reaction is inferred.

## Artifacts

- [test_run_A1_smoke_20261125_182356.log](test_run_A1_smoke_20261125_182356.log)
- [test_run_A1_smoke_20261125_182445.log](test_run_A1_smoke_20261125_182445.log)
- [test_run_A2_unit_20261125_182356.log](test_run_A2_unit_20261125_182356.log)
- [test_run_A2_unit_20261125_182445.log](test_run_A2_unit_20261125_182445.log)
- [test_run_A3_integration_20261125_182356.log](test_run_A3_integration_20261125_182356.log)
- [test_run_A3_integration_20261125_182445.log](test_run_A3_integration_20261125_182445.log)
- [test_run_B1_smoke_20261125_182356.log](test_run_B1_smoke_20261125_182356.log)
- [test_run_B2_unit_20261125_182356.log](test_run_B2_unit_20261125_182356.log)

[Deployment receipts](tests/deployment-receipts.json) identify archive/manifest hashes and base source commit. The tests directory contains per-state injection/detection/restoration logs, rendered HTTP responses, qualification, preservation and metadata output, source bundles and retained regression logs. [Handover](sprint_E.7_handover.md) records the unfinished acceptance gates.
