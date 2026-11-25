# E.8 test results

[Design and test specification](sprint_E.8_design.md) owns the selected gates. [Walkthrough](sprint_E.8_increment_demo.md) owns copyable operating commands. All five required gates passed; no skipped gate, failed assertion or flaky deferral. Initial expected import failure is retained in tests/test-first.log. Tests were specified before implementation.

| Gate | Result | Scope |
|---|---|---|
| A1 smoke | PASS | Python source compilation |
| A2 unit | PASS | Two policy unittest groups, many negative subcases |
| A3 integration | PASS | Three fresh Oracle cadences; five injected failure paths |
| B1 smoke | PASS | Full registered smoke, including candidate check |
| B2 unit | PASS | Full registered unit, including candidate policy |

Run `bash tests/run.sh --smoke --new-only progress/E.8/new_tests.manifest`, then the same command with `--unit` and `--integration`. Regression uses `bash tests/run.sh --smoke` and `bash tests/run.sh --unit`. Expected: zero failed tests. Oracle/host prerequisites are in the manual. B3 is not selected by PLAN, not a deferred requirement.

PBI-066: real merge after base advancement, fresh preparation/migration/compilation/state/backend, five attributable failures and stopped dependent stages. PBI-067: nonempty mandatory reports, exact identity and policy, disabled/unknown/weakened plan and non-success rejection; earliest failure retained. PBI-076: three locally executed cadences, conservative unknown fallback and contract/migration inclusion; critical disabling rejected.

Final execution receipts are in tests/executions.json. Each injected case requires its specific diagnostic; arbitrary transport errors cannot satisfy a negative case. Eight paths execute; all eight meet their expected outcome. Timings in receipts are single-host observations, not performance claims. Negative cases mutate generated targets only and cleanup succeeds. Synthetic report tests establish aggregation behavior separately from actual Oracle execution.

## Artifacts

- [test_run_A1_smoke_20261125_185755.log](test_run_A1_smoke_20261125_185755.log)
- [test_run_A1_smoke_20261125_185905.log](test_run_A1_smoke_20261125_185905.log)
- [test_run_A2_unit_20261125_185755.log](test_run_A2_unit_20261125_185755.log)
- [test_run_A2_unit_20261125_185905.log](test_run_A2_unit_20261125_185905.log)
- [test_run_A3_integration_20261125_185755.log](test_run_A3_integration_20261125_185755.log)
- [test_run_A3_integration_20261125_185905.log](test_run_A3_integration_20261125_185905.log)
- [test_run_B1_smoke_20261125_185805.log](test_run_B1_smoke_20261125_185805.log)
- [test_run_B1_smoke_20261125_185914.log](test_run_B1_smoke_20261125_185914.log)
- [test_run_B2_unit_20261125_185807.log](test_run_B2_unit_20261125_185807.log)
- [test_run_B2_unit_20261125_185917.log](test_run_B2_unit_20261125_185917.log)

- [Gate receipts](tests/gates.json)
- [Execution receipts](tests/executions.json)
- [Candidate Git bundle](tests/candidate.bundle)
- [Integrated change](tests/integrated.diff)
- [Backend regression](tests/regression-backend.log)
- [Contract regression](tests/regression-contracts.log)

Each cadence/fault directory under tests contains its stage diagnostics and result.json. Preparation and cleanup logs exist only when target creation was reached. Source rejection has neither.
