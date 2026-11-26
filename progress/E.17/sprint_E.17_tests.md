# E.17 test execution results

## Summary

PBI-085 acceptance is traced by the [checklist](sprint_E.17_checklist.md). All executable source matches pinned 33df904; later changes concern acceptance wording, documentation and evidence only. A1/A2/A3 pass 1/1 each; B1 passes 16/16; B2 passes 18/18. Unit tests prove refusal/receipt contracts, smoke checks source/tool setup, and integration IT-17 checks actual hosted source, archive bytes, native results, browser access and cleanup. Qualified run 45828709006 and live repeat 45831994665 both pass.

B3 full integration passes 26/26 in test_run_B3_integration_20261126_142430.log, with wrapper exit zero after source stability and scoped cleanup. All six gates pass without waived failures. The fresh hosted Oracle run is 45841076840 at 5f135bd; the historical native reader verifies accepted E.16 named-step run 45810907563 at 03f18caa. Earlier setup failures, the 26-case/7-failure diagnostic and focused 6/6 dependency retry remain preserved. The final full run verifies every case again after both local dependencies were healthy and the evidence input was corrected.

[Final receipt](tests/regression-final-receipt.json) records result/source identity. [Replay index](tests/regression-replay/index.json) maps preserved generated outputs, including identical before/after executable-source snapshots. These historical prepared-host tests remain separate from the hosted clean-host acceptance proof.

## Reproduction commands

The native test runner selects the declared manifest and delegates historical integration to its owned isolated database fixture. It creates fresh temporary private inputs and cleans its owned resources; no E.17 hosted inputs come from that fixture. Run these from the Git checkout root; historical integration requires the already prepared local tools/database and scoped credential accommodation described in the project policy.

```bash
cd "$(git rev-parse --show-toplevel)"
tests/run.sh --smoke --new-only progress/E.17/new_tests.manifest
tests/run.sh --unit --new-only progress/E.17/new_tests.manifest
E17_RUN_ID=45828709006 tests/run.sh --integration --new-only progress/E.17/new_tests.manifest
tests/run.sh --smoke
tests/run.sh --unit
HOSTED_ORACLE_REPO=rstyczynski/APEX_CICD_E.17 E16_RUN_ID=45810907563 E17_RUN_ID=45828709006 tests/run.sh --integration
```

## Artifacts

[test_run_A1_smoke_20261126_133641.log](tests/test_run_A1_smoke_20261126_133641.log) records its exact execution and outcome.

[test_run_A2_unit_20261126_133653.log](tests/test_run_A2_unit_20261126_133653.log) records its exact execution and outcome.

[test_run_A3_integration_20261126_133910.log](tests/test_run_A3_integration_20261126_133910.log) records its exact execution and outcome.

[test_run_B1_smoke_20261126_133935.log](tests/test_run_B1_smoke_20261126_133935.log) records its exact execution and outcome.

[test_run_B2_unit_20261126_133950.log](tests/test_run_B2_unit_20261126_133950.log) records its exact execution and outcome.

[test_run_B3_integration_20261126_134032.log](tests/test_run_B3_integration_20261126_134032.log) records its exact execution and outcome.

[test_run_B3_integration_20261126_140320.log](tests/test_run_B3_integration_20261126_140320.log) records its exact execution and outcome.

[test_run_B3_integration_20261126_140405.log](tests/test_run_B3_integration_20261126_140405.log) records its exact execution and outcome.

[test_run_B3_integration_20261126_140445.log](tests/test_run_B3_integration_20261126_140445.log) records its exact execution and outcome.

[test_run_B3_integration_20261126_141825.log](tests/test_run_B3_integration_20261126_141825.log) records its exact execution and outcome.

[test_run_B3_integration_20261126_142225.log](tests/test_run_B3_integration_20261126_142225.log) records its exact execution and outcome.

[test_run_B3_integration_20261126_142430.log](tests/test_run_B3_integration_20261126_142430.log) records its exact execution and outcome.

[test_run_B3_integration_resume.log](tests/test_run_B3_integration_resume.log) records its exact execution and outcome.

[Dependency retry](tests/regression-dependency-retry.log) passes 6/6; [native input retry](tests/native-regression-input-retry.log) qualifies the corrected run identity. [Live verification](tests/live-demo-verification.log), [job log](tests/live-demo-job.log) and [run metadata](tests/live-demo-run.json) retain live outcomes. [Test profile](../../docs/test-profile.md#e17-independent-host-reproduction) defines regression boundaries; [bug history](sprint_E.17_bugs.md) records failures and repairs.
