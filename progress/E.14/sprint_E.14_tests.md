# E.14 verification

## Proof boundaries

SM-1 parses the driver only. UT-1 uses synthetic route validation and rejects missing components/invalid contract values; it proves no Oracle outcome. IT-1 performs actual Oracle maintenance rejection, independent unaffected read/write traffic, session interruption rollback and retry, complete history/detail comparison and original greeting/settings assertions. [Live receipt](tests/run_18259/receipt.json) and [inspection](tests/run_18259/live-inspection.log) separately record demonstration. First direct run failed ORA-03405; [failed output](tests/run_16473/Hello-start.log) is retained, then statement separation fixed it. No failed assertion is waived.

## Reproduction

[Walkthrough](sprint_E.14_increment_demo.md) explains SQL, script behavior, prepared Podman/Oracle prerequisites and expected outputs. The test runner sources registered domain functions. Use Bash at the Git repository root. New gates select only this sprint's manifest; regression selects the full registered suites. Each must finish with zero failed tests. Syntax/unit are fast; real full integration reconstructs and deploys historical fixtures and can take several minutes.

```bash
cd "$(git rev-parse --show-toplevel)"
bash tests/run.sh --smoke --new-only progress/E.14/new_tests.manifest
bash tests/run.sh --unit --new-only progress/E.14/new_tests.manifest
bash tests/run.sh --integration --new-only progress/E.14/new_tests.manifest
bash tests/run.sh --smoke
bash tests/run.sh --unit
bash tests/run.sh --integration
```

## Artifacts

All six final gates pass with zero failed entries and no waiver. New smoke/unit/integration counts: 1/1/1. Full regression counts: 13/14/23. Counts describe runner entries, not individual assertions. [Final verification](tests/final-verification.json) binds the source snapshot to current files. The initial full run used the previous default registry; after correcting registration all six gates were rerun. No initial result is relabelled as the final registry run.

Historical regression freshly exercised native deployment and HTTP behavior in the owned isolated database. Recorded hosted-evidence readers remain evidence readers, not new hosted deployments. Generated historical outputs were relocated under tests/regression-generated and original historical files restored byte for byte. Raw paths retain their execution-time meaning.

## Maintenance assertion sensitivity

A separate test-only SQL substitution disabled the maintenance rejection without editing production sources. [Expected failing run](tests/maintenance-mutation-red.log) terminates specifically with ORA-20203 maintenance bypass. The legitimate driver passes independently. This proves detection of the missing gate; it does not fabricate test-first chronology or substitute for the required positive gates.

## Related design and review

[Design and test specification](sprint_E.14_design.md) owns the selected cases. [Documentation audit](sprint_E.14_documentation_audit.md) owns consistency review; [defect record](sprint_E.14_bugs.md) preserves failed attempts and corrections.

## PBI-050 verification

IT-1 and the developer live inspection verify the qualified-fixture windows, coexistence, recovery and preservation. The full regression result remains the mandatory quality disposition; individual passing observations do not close the sprint.

## PBI-080 review verification

The source-linked assessment and production follow-up inventory distinguish historical evidence, fresh registered regression, observed failures, untested product behavior, literal backlog statuses and the proposed sequence. Links and anchors are checked by the documentation audit. The separate Lifecycle Architecture decision is intentionally unmade.

## Timestamped gate logs

[test_run_A1_smoke_20261125_223046.log](tests/test_run_A1_smoke_20261125_223046.log)

[test_run_A1_smoke_20261125_224649.log](tests/test_run_A1_smoke_20261125_224649.log)

[test_run_A2_unit_20261125_223046.log](tests/test_run_A2_unit_20261125_223046.log)

[test_run_A2_unit_20261125_224649.log](tests/test_run_A2_unit_20261125_224649.log)

[test_run_A3_integration_20261125_223046.log](tests/test_run_A3_integration_20261125_223046.log)

[test_run_A3_integration_20261125_224649.log](tests/test_run_A3_integration_20261125_224649.log)

[test_run_B1_smoke_20261125_223046.log](tests/test_run_B1_smoke_20261125_223046.log)

[test_run_B1_smoke_20261125_224649.log](tests/test_run_B1_smoke_20261125_224649.log)

[test_run_B1_smoke_20261125_231149.log](tests/test_run_B1_smoke_20261125_231149.log)

[test_run_B2_unit_20261125_223046.log](tests/test_run_B2_unit_20261125_223046.log)

[test_run_B2_unit_20261125_224649.log](tests/test_run_B2_unit_20261125_224649.log)

[test_run_B2_unit_20261125_231149.log](tests/test_run_B2_unit_20261125_231149.log)

[test_run_B3_integration_20261125_223046.log](tests/test_run_B3_integration_20261125_223046.log)

[test_run_B3_integration_20261125_224649.log](tests/test_run_B3_integration_20261125_224649.log)

[test_run_B3_integration_20261125_225614.log](tests/test_run_B3_integration_20261125_225614.log)

## Recovered infrastructure interruption and final environment

The corrected-registry B3 setup attempt [failed after 300 seconds](tests/test_run_B3_integration_20261125_224649.log). [Recovery record](tests/environment-recovery.md) distinguishes observed symptoms from the unconfirmed cause. The unchanged-source [B3 retry](tests/test_run_B3_integration_20261125_225614.log) passes 23/23 entries. Full smoke and unit were rechecked after service recovery and pass 13/13 and 14/14. This is one recovered infrastructure failure, with no test deferral or percentage waiver. Prior initial-registry results remain labelled historical. The live fixture's [post-recovery preservation](tests/run_18259/post-recovery-inspection.log) also passes. Monitored oom_kill remained 33 during the retry; that does not date the earlier event or establish its cause.
