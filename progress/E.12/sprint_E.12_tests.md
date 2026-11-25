# E.12 test execution

## Current verified results

All six PLAN gates pass: new smoke A1 2/2, unit A2 4/4 registered entries, real Oracle integration A3 1/1; unscoped regression smoke B1 11/11, unit B2 12/12 and integration B3 21/21. Every outer process exit is zero in [the final gate receipt](tests/stable-final-gates.json). The [full integration log](test_run_B3_integration_20261125_213552.log) includes the Foundation entry, not merely the earlier twenty cases. Its before/after source snapshots and all 247 canonical executable hashes match; [the final source/environment audit](tests/final-source-and-environment-audit.json) records that independent comparison. No failed attempt is accepted as a passing gate.

New gates invoke bash tests/run.sh at each selected level with --new-only progress/E.12/new_tests.manifest. Regressions invoke those levels without that filter. B3 ran the exact copied executable set in an isolated checkout, bound by [the source selection](tests/frozen-source-selection.json), without copied private settings/profiles/credentials. It used the separate owned FREEPDB1 fixture and fresh OS-private inputs. Temporary ORDS and private inputs were removed successfully. The labelled database remains available as a regression cache. Historical generated outputs were archived and their historical tracked paths restored; initial unrelated untracked files remain untouched.

## What the tests prove

PBI-048's real experiment verifies 240 separately committed workload calls from unchanged Hello/World consumers during additive expansion and interrupted recovery, identical legacy PL/SQL source, omitted-language and Polish results, specific unsupported-language rejection, exactly one 1.1.0 record, untouched original history ID 0 in both representations and language=en. IDs 1 and 2 are intentional update/delete challenges, separate from preserved ID 0.

PBI-081's actual failed child SQLPlus transaction is followed by an observed rollback before committed attributable I/U/D operations. Restarted catch-up must preserve the newer target value, remove the deleted ID, retain the inserted ID/value/language and match the complete source set in both directions under the selected source lock. Primary keys prevent duplicate identifiers. Equality applies at that boundary; later supported legacy traffic is not claimed to be continuously replicated.

The final B3 Foundation receipt names E12_RUN_80961 and driver SHA-256 7d7ef025e820e90efc774ac2084b3ee457ac199f04b41441d5d3fb4e2c2aa366; its SQL/log copies are under tests/frozen-checkout/runs/. The separate final A3 receipt and copies remain under tests/experiment.json and tests/runs/. [Observed completion gaps](tests/availability-observations.json) are bound to that A3 schema, include deliberate 0.1-second pacing, and are not a production latency SLA or direct lock-duration measurement. The subprocess budget is 180 seconds.

The repaired historical release case performs real pinned SQLcl 25.3.0.274.1210 native exports/imports, archive construction, initial and both patch-start qualifications, authenticated HTTP greeting submissions, complete retained-field comparisons, repeat admission without writes and real drift rejection/restoration. [Its evidence directory](tests/frozen-checkout/legacy-regression/run-20261125T223552-50884/) binds the accepted existing PR/source, archive bytes and runtime service separately from logical configuration. No new hosted PR or production PROJECT deployment is asserted. E.3 historical GitHub/native-release checks are explicitly evidence readers, not new hosted workflow runs. E.9 uses a local synthetic Git fixture and loopback service, not remote publication of this repository.

Smoke checks parsing/configuration. Synthetic equality cases establish corruption detection. Actual-runner cases prove final-record execution with/without newline and protection from a child draining stdin. Nine mocked private-boundary cases prove routing, redaction, cleanup and policy refusals; a separate binding case rejects unsafe descriptors before credential access and preserves pinned executable selection. Mocked checks do not prove database correctness. Real native integration establishes the bounded runtime behavior.

## Historical failures and limits

Earlier 16/20 runs failed assembly, the unfinished release stub, absent integration application and drift on an incompatible retained lineage. A later twenty-case run passed its executed functions but failed the source guard and omitted Foundation through inherited stdin. The 21:34 attempt failed fixture provisioning during overlapping access. All remain failed diagnostic runs. EOF/input ownership, native fixture identity, ORDS privileges/memory, cookies, generated-view recompilation and credential-default policy were repaired and verified in the final complete run. [The defect record](sprint_E.12_bugs.md) preserves those findings.

No production rollout, universal availability bound, fresh-host production reproduction, Foundation browser UI journey, E.13 bridge or E.14 component windows are established. Native PowerPoint and optional VS Code opening remain unverified after permission denial; all fourteen slides were rendered and visually inspected, package/layout/font/bullet/import checks pass, and raw result files were read in the terminal. These viewer conveniences are separate from the real backend demonstration in [handover](sprint_E.12_handover.md).

## Artifacts

[Final gate receipt](tests/stable-final-gates.json), [source/environment audit](tests/final-source-and-environment-audit.json), [presentation validation](tests/final-presentation-validation.json), [visual review](tests/final-presentation-visual-review.json), [walkthrough source audit](tests/final-walkthrough-source-audit.json), [link audit](tests/final-link-audit.json), [requirement checklist](sprint_E.12_remaining_work.md).

The complete physical log-path index follows. Historical logs retain their original outcomes; readable evidence may have trailing whitespace removed only after exact originals were archived.

[test_run_A1_smoke_20261125_202003.log](test_run_A1_smoke_20261125_202003.log)

[test_run_A1_smoke_20261125_202139.log](test_run_A1_smoke_20261125_202139.log)

[test_run_A1_smoke_20261125_210736.log](test_run_A1_smoke_20261125_210736.log)

[test_run_A1_smoke_20261125_211756.log](test_run_A1_smoke_20261125_211756.log)

[test_run_A1_smoke_20261125_213117.log](test_run_A1_smoke_20261125_213117.log)

[test_run_A1_smoke_20261125_213456.log](test_run_A1_smoke_20261125_213456.log)

[test_run_A1_smoke_20261125_213608.log](test_run_A1_smoke_20261125_213608.log)

[test_run_A2_unit_20261125_202004.log](test_run_A2_unit_20261125_202004.log)

[test_run_A2_unit_20261125_202139.log](test_run_A2_unit_20261125_202139.log)

[test_run_A2_unit_20261125_210736.log](test_run_A2_unit_20261125_210736.log)

[test_run_A2_unit_20261125_212159.log](test_run_A2_unit_20261125_212159.log)

[test_run_A2_unit_20261125_213117.log](test_run_A2_unit_20261125_213117.log)

[test_run_A2_unit_20261125_213456.log](test_run_A2_unit_20261125_213456.log)

[test_run_A3_integration_20261125_202028.log](test_run_A3_integration_20261125_202028.log)

[test_run_A3_integration_20261125_202044.log](test_run_A3_integration_20261125_202044.log)

[test_run_A3_integration_20261125_202154.log](test_run_A3_integration_20261125_202154.log)

[test_run_A3_integration_20261125_210737.log](test_run_A3_integration_20261125_210737.log)

[test_run_A3_integration_20261125_213457.log](test_run_A3_integration_20261125_213457.log)

[test_run_B1_smoke_20261125_202156.log](test_run_B1_smoke_20261125_202156.log)

[test_run_B1_smoke_20261125_210751.log](test_run_B1_smoke_20261125_210751.log)

[test_run_B1_smoke_20261125_211756.log](test_run_B1_smoke_20261125_211756.log)

[test_run_B1_smoke_20261125_213118.log](test_run_B1_smoke_20261125_213118.log)

[test_run_B1_smoke_20261125_213511.log](test_run_B1_smoke_20261125_213511.log)

[test_run_B1_smoke_20261125_213608.log](test_run_B1_smoke_20261125_213608.log)

[test_run_B2_unit_20261125_202204.log](test_run_B2_unit_20261125_202204.log)

[test_run_B2_unit_20261125_210755.log](test_run_B2_unit_20261125_210755.log)

[test_run_B2_unit_20261125_212159.log](test_run_B2_unit_20261125_212159.log)

[test_run_B2_unit_20261125_213120.log](test_run_B2_unit_20261125_213120.log)

[test_run_B2_unit_20261125_213514.log](test_run_B2_unit_20261125_213514.log)

[test_run_B3_integration_20261125_202621.log](test_run_B3_integration_20261125_202621.log)

[test_run_B3_integration_20261125_211759.log](test_run_B3_integration_20261125_211759.log)

[test_run_B3_integration_20261125_213454.log](test_run_B3_integration_20261125_213454.log)

[test_run_B3_integration_20261125_213552.log](test_run_B3_integration_20261125_213552.log)

[tests/assertions.log](tests/assertions.log)

[tests/baseline.log](tests/baseline.log)

[tests/catchup.log](tests/catchup.log)

[tests/concurrent.log](tests/concurrent.log)

[tests/current-resume-independent/assertions.log](tests/current-resume-independent/assertions.log)

[tests/current-resume-independent/baseline.log](tests/current-resume-independent/baseline.log)

[tests/current-resume-independent/catchup.log](tests/current-resume-independent/catchup.log)

[tests/current-resume-independent/concurrent.log](tests/current-resume-independent/concurrent.log)

[tests/current-resume-independent/expand-backfill.log](tests/current-resume-independent/expand-backfill.log)

[tests/current-resume-independent/hello.log](tests/current-resume-independent/hello.log)

[tests/current-resume-independent/interruption.log](tests/current-resume-independent/interruption.log)

[tests/current-resume-independent/inventory.log](tests/current-resume-independent/inventory.log)

[tests/current-resume-independent/legacy-after.log](tests/current-resume-independent/legacy-after.log)

[tests/current-resume-independent/legacy-before.log](tests/current-resume-independent/legacy-before.log)

[tests/current-resume-independent/rollback-check.log](tests/current-resume-independent/rollback-check.log)

[tests/current-resume-independent/runs/E12_RUN_99171/assertions.log](tests/current-resume-independent/runs/E12_RUN_99171/assertions.log)

[tests/current-resume-independent/runs/E12_RUN_99171/baseline.log](tests/current-resume-independent/runs/E12_RUN_99171/baseline.log)

[tests/current-resume-independent/runs/E12_RUN_99171/catchup.log](tests/current-resume-independent/runs/E12_RUN_99171/catchup.log)

[tests/current-resume-independent/runs/E12_RUN_99171/concurrent.log](tests/current-resume-independent/runs/E12_RUN_99171/concurrent.log)

[tests/current-resume-independent/runs/E12_RUN_99171/expand-backfill.log](tests/current-resume-independent/runs/E12_RUN_99171/expand-backfill.log)

[tests/current-resume-independent/runs/E12_RUN_99171/hello.log](tests/current-resume-independent/runs/E12_RUN_99171/hello.log)

[tests/current-resume-independent/runs/E12_RUN_99171/interruption.log](tests/current-resume-independent/runs/E12_RUN_99171/interruption.log)

[tests/current-resume-independent/runs/E12_RUN_99171/inventory.log](tests/current-resume-independent/runs/E12_RUN_99171/inventory.log)

[tests/current-resume-independent/runs/E12_RUN_99171/legacy-after.log](tests/current-resume-independent/runs/E12_RUN_99171/legacy-after.log)

[tests/current-resume-independent/runs/E12_RUN_99171/legacy-before.log](tests/current-resume-independent/runs/E12_RUN_99171/legacy-before.log)

[tests/current-resume-independent/runs/E12_RUN_99171/rollback-check.log](tests/current-resume-independent/runs/E12_RUN_99171/rollback-check.log)

[tests/current-resume-independent/runs/E12_RUN_99171/unsupported-language.log](tests/current-resume-independent/runs/E12_RUN_99171/unsupported-language.log)

[tests/current-resume-independent/runs/E12_RUN_99171/version.log](tests/current-resume-independent/runs/E12_RUN_99171/version.log)

[tests/current-resume-independent/runs/E12_RUN_99171/world.log](tests/current-resume-independent/runs/E12_RUN_99171/world.log)

[tests/current-resume-independent/unsupported-language.log](tests/current-resume-independent/unsupported-language.log)

[tests/current-resume-independent/version.log](tests/current-resume-independent/version.log)

[tests/current-resume-independent/world.log](tests/current-resume-independent/world.log)

[tests/current-resume-ords-privileges.log](tests/current-resume-ords-privileges.log)

[tests/current-resume-unit.log](tests/current-resume-unit.log)

[tests/current-sqlcl-qualified.log](tests/current-sqlcl-qualified.log)

[tests/expand-backfill.log](tests/expand-backfill.log)

[tests/final-live-inspection.log](tests/final-live-inspection.log)

[tests/fixture-lock-preflight.log](tests/fixture-lock-preflight.log)

[tests/frozen-checkout/assertions.log](tests/frozen-checkout/assertions.log)

[tests/frozen-checkout/baseline.log](tests/frozen-checkout/baseline.log)

[tests/frozen-checkout/catchup.log](tests/frozen-checkout/catchup.log)

[tests/frozen-checkout/concurrent.log](tests/frozen-checkout/concurrent.log)

[tests/frozen-checkout/expand-backfill.log](tests/frozen-checkout/expand-backfill.log)

[tests/frozen-checkout/hello.log](tests/frozen-checkout/hello.log)

[tests/frozen-checkout/interruption.log](tests/frozen-checkout/interruption.log)

[tests/frozen-checkout/inventory.log](tests/frozen-checkout/inventory.log)

[tests/frozen-checkout/legacy-after.log](tests/frozen-checkout/legacy-after.log)

[tests/frozen-checkout/legacy-before.log](tests/frozen-checkout/legacy-before.log)

[tests/frozen-checkout/legacy-regression/run-20261125T223552-50884/drift-demo.p23zm1an/capture.log](tests/frozen-checkout/legacy-regression/run-20261125T223552-50884/drift-demo.p23zm1an/capture.log)

[tests/frozen-checkout/legacy-regression/run-20261125T223552-50884/drift-demo.p23zm1an/inject.log](tests/frozen-checkout/legacy-regression/run-20261125T223552-50884/drift-demo.p23zm1an/inject.log)

[tests/frozen-checkout/legacy-regression/run-20261125T223552-50884/drift-demo.p23zm1an/restore.log](tests/frozen-checkout/legacy-regression/run-20261125T223552-50884/drift-demo.p23zm1an/restore.log)

[tests/frozen-checkout/legacy-regression/run-20261125T223552-50884/operations.log](tests/frozen-checkout/legacy-regression/run-20261125T223552-50884/operations.log)

[tests/frozen-checkout/legacy-regression/run-20261125T223552-50884/ords-install.log](tests/frozen-checkout/legacy-regression/run-20261125T223552-50884/ords-install.log)

[tests/frozen-checkout/legacy-regression/run-20261125T223552-50884/ords-uninstall.log](tests/frozen-checkout/legacy-regression/run-20261125T223552-50884/ords-uninstall.log)

[tests/frozen-checkout/legacy-regression/run-20261125T223552-50884/runtime.log](tests/frozen-checkout/legacy-regression/run-20261125T223552-50884/runtime.log)

[tests/frozen-checkout/legacy-regression/run-20261125T223552-50884/sqlcl-version.log](tests/frozen-checkout/legacy-regression/run-20261125T223552-50884/sqlcl-version.log)

[tests/frozen-checkout/live-demo.log](tests/frozen-checkout/live-demo.log)

[tests/frozen-checkout/new-integration-retry.log](tests/frozen-checkout/new-integration-retry.log)

[tests/frozen-checkout/new-integration-retry2.log](tests/frozen-checkout/new-integration-retry2.log)

[tests/frozen-checkout/regression-generated/progress/E.5/tests/mutation-detected.log](tests/frozen-checkout/regression-generated/progress/E.5/tests/mutation-detected.log)

[tests/frozen-checkout/regression-generated/progress/E.5/tests/utplsql-full.log](tests/frozen-checkout/regression-generated/progress/E.5/tests/utplsql-full.log)

[tests/frozen-checkout/regression-generated/progress/E.5/tests/utplsql-reordered.log](tests/frozen-checkout/regression-generated/progress/E.5/tests/utplsql-reordered.log)

[tests/frozen-checkout/regression-generated/progress/E.5/tests/utplsql-repeat.log](tests/frozen-checkout/regression-generated/progress/E.5/tests/utplsql-repeat.log)

[tests/frozen-checkout/regression-generated/progress/E.6/tests/compat-1.0.1.log](tests/frozen-checkout/regression-generated/progress/E.6/tests/compat-1.0.1.log)

[tests/frozen-checkout/regression-generated/progress/E.6/tests/compat-1.0.log](tests/frozen-checkout/regression-generated/progress/E.6/tests/compat-1.0.log)

[tests/frozen-checkout/regression-generated/progress/E.6/tests/compat-1.1.log](tests/frozen-checkout/regression-generated/progress/E.6/tests/compat-1.1.log)

[tests/frozen-checkout/regression-generated/progress/E.6/tests/compat-restored-consumers.log](tests/frozen-checkout/regression-generated/progress/E.6/tests/compat-restored-consumers.log)

[tests/frozen-checkout/regression-generated/progress/E.6/tests/incompatible-detected.log](tests/frozen-checkout/regression-generated/progress/E.6/tests/incompatible-detected.log)

[tests/frozen-checkout/regression-generated/progress/E.6/tests/sessions-after.log](tests/frozen-checkout/regression-generated/progress/E.6/tests/sessions-after.log)

[tests/frozen-checkout/regression-generated/progress/E.6/tests/sessions-before.log](tests/frozen-checkout/regression-generated/progress/E.6/tests/sessions-before.log)

[tests/frozen-checkout/regression-generated/progress/E.6/tests/unit.log](tests/frozen-checkout/regression-generated/progress/E.6/tests/unit.log)

[tests/frozen-checkout/regression-generated/progress/E.8/tests/pr-backend/backend-failure.log](tests/frozen-checkout/regression-generated/progress/E.8/tests/pr-backend/backend-failure.log)

[tests/frozen-checkout/regression-generated/progress/E.8/tests/pr-backend/backend.log](tests/frozen-checkout/regression-generated/progress/E.8/tests/pr-backend/backend.log)

[tests/frozen-checkout/regression-generated/progress/E.8/tests/pr-migration/migration-failure.log](tests/frozen-checkout/regression-generated/progress/E.8/tests/pr-migration/migration-failure.log)

[tests/frozen-checkout/regression-generated/progress/E.8/tests/pr-migration/migration.log](tests/frozen-checkout/regression-generated/progress/E.8/tests/pr-migration/migration.log)

[tests/frozen-checkout/regression-generated/progress/E.8/tests/pr-state/state-failure.log](tests/frozen-checkout/regression-generated/progress/E.8/tests/pr-state/state-failure.log)

[tests/frozen-checkout/regression-generated/progress/E.8/tests/pr-state/state.log](tests/frozen-checkout/regression-generated/progress/E.8/tests/pr-state/state.log)

[tests/frozen-checkout/regression-generated/progress/E.9/tests/service/direct-write.log](tests/frozen-checkout/regression-generated/progress/E.9/tests/service/direct-write.log)

[tests/frozen-checkout/regression-integration.log](tests/frozen-checkout/regression-integration.log)

[tests/frozen-checkout/regression-smoke.log](tests/frozen-checkout/regression-smoke.log)

[tests/frozen-checkout/regression-unit.log](tests/frozen-checkout/regression-unit.log)

[tests/frozen-checkout/reset-owned-fixture.log](tests/frozen-checkout/reset-owned-fixture.log)

[tests/frozen-checkout/resume-foundation-integration.log](tests/frozen-checkout/resume-foundation-integration.log)

[tests/frozen-checkout/resume-full-integration.log](tests/frozen-checkout/resume-full-integration.log)

[tests/frozen-checkout/resume-q-reconstruction.log](tests/frozen-checkout/resume-q-reconstruction.log)

[tests/frozen-checkout/resume-q-status.log](tests/frozen-checkout/resume-q-status.log)

[tests/frozen-checkout/resume-recovery-verification.log](tests/frozen-checkout/resume-recovery-verification.log)

[tests/frozen-checkout/resume-regression-smoke.log](tests/frozen-checkout/resume-regression-smoke.log)

[tests/frozen-checkout/resume-regression-unit.log](tests/frozen-checkout/resume-regression-unit.log)

[tests/frozen-checkout/resume-smoke.log](tests/frozen-checkout/resume-smoke.log)

[tests/frozen-checkout/resume-unit.log](tests/frozen-checkout/resume-unit.log)

[tests/frozen-checkout/resume-unterminated-manifest.log](tests/frozen-checkout/resume-unterminated-manifest.log)

[tests/frozen-checkout/rollback-check.log](tests/frozen-checkout/rollback-check.log)

[tests/frozen-checkout/runs/E12_RUN_80961/assertions.log](tests/frozen-checkout/runs/E12_RUN_80961/assertions.log)

[tests/frozen-checkout/runs/E12_RUN_80961/baseline.log](tests/frozen-checkout/runs/E12_RUN_80961/baseline.log)

[tests/frozen-checkout/runs/E12_RUN_80961/catchup.log](tests/frozen-checkout/runs/E12_RUN_80961/catchup.log)

[tests/frozen-checkout/runs/E12_RUN_80961/concurrent.log](tests/frozen-checkout/runs/E12_RUN_80961/concurrent.log)

[tests/frozen-checkout/runs/E12_RUN_80961/expand-backfill.log](tests/frozen-checkout/runs/E12_RUN_80961/expand-backfill.log)

[tests/frozen-checkout/runs/E12_RUN_80961/hello.log](tests/frozen-checkout/runs/E12_RUN_80961/hello.log)

[tests/frozen-checkout/runs/E12_RUN_80961/interruption.log](tests/frozen-checkout/runs/E12_RUN_80961/interruption.log)

[tests/frozen-checkout/runs/E12_RUN_80961/inventory.log](tests/frozen-checkout/runs/E12_RUN_80961/inventory.log)

[tests/frozen-checkout/runs/E12_RUN_80961/legacy-after.log](tests/frozen-checkout/runs/E12_RUN_80961/legacy-after.log)

[tests/frozen-checkout/runs/E12_RUN_80961/legacy-before.log](tests/frozen-checkout/runs/E12_RUN_80961/legacy-before.log)

[tests/frozen-checkout/runs/E12_RUN_80961/rollback-check.log](tests/frozen-checkout/runs/E12_RUN_80961/rollback-check.log)

[tests/frozen-checkout/runs/E12_RUN_80961/unsupported-language.log](tests/frozen-checkout/runs/E12_RUN_80961/unsupported-language.log)

[tests/frozen-checkout/runs/E12_RUN_80961/version.log](tests/frozen-checkout/runs/E12_RUN_80961/version.log)

[tests/frozen-checkout/runs/E12_RUN_80961/world.log](tests/frozen-checkout/runs/E12_RUN_80961/world.log)

[tests/frozen-checkout/runs/E12_RUN_91325/assertions.log](tests/frozen-checkout/runs/E12_RUN_91325/assertions.log)

[tests/frozen-checkout/runs/E12_RUN_91325/baseline.log](tests/frozen-checkout/runs/E12_RUN_91325/baseline.log)

[tests/frozen-checkout/runs/E12_RUN_91325/catchup.log](tests/frozen-checkout/runs/E12_RUN_91325/catchup.log)

[tests/frozen-checkout/runs/E12_RUN_91325/concurrent.log](tests/frozen-checkout/runs/E12_RUN_91325/concurrent.log)

[tests/frozen-checkout/runs/E12_RUN_91325/expand-backfill.log](tests/frozen-checkout/runs/E12_RUN_91325/expand-backfill.log)

[tests/frozen-checkout/runs/E12_RUN_91325/hello.log](tests/frozen-checkout/runs/E12_RUN_91325/hello.log)

[tests/frozen-checkout/runs/E12_RUN_91325/interruption.log](tests/frozen-checkout/runs/E12_RUN_91325/interruption.log)

[tests/frozen-checkout/runs/E12_RUN_91325/inventory.log](tests/frozen-checkout/runs/E12_RUN_91325/inventory.log)

[tests/frozen-checkout/runs/E12_RUN_91325/legacy-after.log](tests/frozen-checkout/runs/E12_RUN_91325/legacy-after.log)

[tests/frozen-checkout/runs/E12_RUN_91325/legacy-before.log](tests/frozen-checkout/runs/E12_RUN_91325/legacy-before.log)

[tests/frozen-checkout/runs/E12_RUN_91325/live-demo.log](tests/frozen-checkout/runs/E12_RUN_91325/live-demo.log)

[tests/frozen-checkout/runs/E12_RUN_91325/new-integration-retry.log](tests/frozen-checkout/runs/E12_RUN_91325/new-integration-retry.log)

[tests/frozen-checkout/runs/E12_RUN_91325/new-integration-retry2.log](tests/frozen-checkout/runs/E12_RUN_91325/new-integration-retry2.log)

[tests/frozen-checkout/runs/E12_RUN_91325/regression-integration.log](tests/frozen-checkout/runs/E12_RUN_91325/regression-integration.log)

[tests/frozen-checkout/runs/E12_RUN_91325/regression-smoke.log](tests/frozen-checkout/runs/E12_RUN_91325/regression-smoke.log)

[tests/frozen-checkout/runs/E12_RUN_91325/regression-unit.log](tests/frozen-checkout/runs/E12_RUN_91325/regression-unit.log)

[tests/frozen-checkout/runs/E12_RUN_91325/reset-owned-fixture.log](tests/frozen-checkout/runs/E12_RUN_91325/reset-owned-fixture.log)

[tests/frozen-checkout/runs/E12_RUN_91325/resume-foundation-integration.log](tests/frozen-checkout/runs/E12_RUN_91325/resume-foundation-integration.log)

[tests/frozen-checkout/runs/E12_RUN_91325/unsupported-language.log](tests/frozen-checkout/runs/E12_RUN_91325/unsupported-language.log)

[tests/frozen-checkout/runs/E12_RUN_91325/version.log](tests/frozen-checkout/runs/E12_RUN_91325/version.log)

[tests/frozen-checkout/runs/E12_RUN_91325/world.log](tests/frozen-checkout/runs/E12_RUN_91325/world.log)

[tests/frozen-checkout/runs/E12_RUN_93135/assertions.log](tests/frozen-checkout/runs/E12_RUN_93135/assertions.log)

[tests/frozen-checkout/runs/E12_RUN_93135/baseline.log](tests/frozen-checkout/runs/E12_RUN_93135/baseline.log)

[tests/frozen-checkout/runs/E12_RUN_93135/catchup.log](tests/frozen-checkout/runs/E12_RUN_93135/catchup.log)

[tests/frozen-checkout/runs/E12_RUN_93135/concurrent.log](tests/frozen-checkout/runs/E12_RUN_93135/concurrent.log)

[tests/frozen-checkout/runs/E12_RUN_93135/expand-backfill.log](tests/frozen-checkout/runs/E12_RUN_93135/expand-backfill.log)

[tests/frozen-checkout/runs/E12_RUN_93135/hello.log](tests/frozen-checkout/runs/E12_RUN_93135/hello.log)

[tests/frozen-checkout/runs/E12_RUN_93135/interruption.log](tests/frozen-checkout/runs/E12_RUN_93135/interruption.log)

[tests/frozen-checkout/runs/E12_RUN_93135/inventory.log](tests/frozen-checkout/runs/E12_RUN_93135/inventory.log)

[tests/frozen-checkout/runs/E12_RUN_93135/legacy-after.log](tests/frozen-checkout/runs/E12_RUN_93135/legacy-after.log)

[tests/frozen-checkout/runs/E12_RUN_93135/legacy-before.log](tests/frozen-checkout/runs/E12_RUN_93135/legacy-before.log)

[tests/frozen-checkout/runs/E12_RUN_93135/rollback-check.log](tests/frozen-checkout/runs/E12_RUN_93135/rollback-check.log)

[tests/frozen-checkout/runs/E12_RUN_93135/unsupported-language.log](tests/frozen-checkout/runs/E12_RUN_93135/unsupported-language.log)

[tests/frozen-checkout/runs/E12_RUN_93135/version.log](tests/frozen-checkout/runs/E12_RUN_93135/version.log)

[tests/frozen-checkout/runs/E12_RUN_93135/world.log](tests/frozen-checkout/runs/E12_RUN_93135/world.log)

[tests/frozen-checkout/runs/E12_RUN_96263/assertions.log](tests/frozen-checkout/runs/E12_RUN_96263/assertions.log)

[tests/frozen-checkout/runs/E12_RUN_96263/baseline.log](tests/frozen-checkout/runs/E12_RUN_96263/baseline.log)

[tests/frozen-checkout/runs/E12_RUN_96263/catchup.log](tests/frozen-checkout/runs/E12_RUN_96263/catchup.log)

[tests/frozen-checkout/runs/E12_RUN_96263/concurrent.log](tests/frozen-checkout/runs/E12_RUN_96263/concurrent.log)

[tests/frozen-checkout/runs/E12_RUN_96263/expand-backfill.log](tests/frozen-checkout/runs/E12_RUN_96263/expand-backfill.log)

[tests/frozen-checkout/runs/E12_RUN_96263/hello.log](tests/frozen-checkout/runs/E12_RUN_96263/hello.log)

[tests/frozen-checkout/runs/E12_RUN_96263/interruption.log](tests/frozen-checkout/runs/E12_RUN_96263/interruption.log)

[tests/frozen-checkout/runs/E12_RUN_96263/inventory.log](tests/frozen-checkout/runs/E12_RUN_96263/inventory.log)

[tests/frozen-checkout/runs/E12_RUN_96263/legacy-after.log](tests/frozen-checkout/runs/E12_RUN_96263/legacy-after.log)

[tests/frozen-checkout/runs/E12_RUN_96263/legacy-before.log](tests/frozen-checkout/runs/E12_RUN_96263/legacy-before.log)

[tests/frozen-checkout/runs/E12_RUN_96263/rollback-check.log](tests/frozen-checkout/runs/E12_RUN_96263/rollback-check.log)

[tests/frozen-checkout/runs/E12_RUN_96263/unsupported-language.log](tests/frozen-checkout/runs/E12_RUN_96263/unsupported-language.log)

[tests/frozen-checkout/runs/E12_RUN_96263/version.log](tests/frozen-checkout/runs/E12_RUN_96263/version.log)

[tests/frozen-checkout/runs/E12_RUN_96263/world.log](tests/frozen-checkout/runs/E12_RUN_96263/world.log)

[tests/frozen-checkout/unsupported-language.log](tests/frozen-checkout/unsupported-language.log)

[tests/frozen-checkout/version.log](tests/frozen-checkout/version.log)

[tests/frozen-checkout/world.log](tests/frozen-checkout/world.log)

[tests/hello.log](tests/hello.log)

[tests/interruption.log](tests/interruption.log)

[tests/inventory.log](tests/inventory.log)

[tests/isolated-db-apex-install.log](tests/isolated-db-apex-install.log)

[tests/isolated-db-memory.log](tests/isolated-db-memory.log)

[tests/isolated-legacy-attempt-1.log](tests/isolated-legacy-attempt-1.log)

[tests/isolated-legacy-attempt-2.log](tests/isolated-legacy-attempt-2.log)

[tests/isolated-legacy-attempt-3.log](tests/isolated-legacy-attempt-3.log)

[tests/isolated-legacy-attempt-4.log](tests/isolated-legacy-attempt-4.log)

[tests/isolated-legacy-attempt-5.log](tests/isolated-legacy-attempt-5.log)

[tests/isolated-legacy-attempt-6.log](tests/isolated-legacy-attempt-6.log)

[tests/isolated-regression-install.log](tests/isolated-regression-install.log)

[tests/legacy-after.log](tests/legacy-after.log)

[tests/legacy-before.log](tests/legacy-before.log)

[tests/legacy-regression/ords-install.log](tests/legacy-regression/ords-install.log)

[tests/legacy-regression/run-20261125T214617-99453/operations.log](tests/legacy-regression/run-20261125T214617-99453/operations.log)

[tests/legacy-regression/run-20261125T214617-99453/ords-install.log](tests/legacy-regression/run-20261125T214617-99453/ords-install.log)

[tests/legacy-regression/run-20261125T214617-99453/ords-uninstall.log](tests/legacy-regression/run-20261125T214617-99453/ords-uninstall.log)

[tests/legacy-regression/run-20261125T214617-99453/runtime.log](tests/legacy-regression/run-20261125T214617-99453/runtime.log)

[tests/legacy-regression/run-20261125T215611-6300/ords-uninstall.log](tests/legacy-regression/run-20261125T215611-6300/ords-uninstall.log)

[tests/legacy-regression/run-20261125T215948-8896/operations.log](tests/legacy-regression/run-20261125T215948-8896/operations.log)

[tests/legacy-regression/run-20261125T215948-8896/ords-install.log](tests/legacy-regression/run-20261125T215948-8896/ords-install.log)

[tests/legacy-regression/run-20261125T215948-8896/runtime.log](tests/legacy-regression/run-20261125T215948-8896/runtime.log)

[tests/legacy-regression/run-20261125T220404-14609/drift-demo.dptdywfy/capture.log](tests/legacy-regression/run-20261125T220404-14609/drift-demo.dptdywfy/capture.log)

[tests/legacy-regression/run-20261125T220404-14609/drift-demo.dptdywfy/inject.log](tests/legacy-regression/run-20261125T220404-14609/drift-demo.dptdywfy/inject.log)

[tests/legacy-regression/run-20261125T220404-14609/drift-demo.dptdywfy/restore.log](tests/legacy-regression/run-20261125T220404-14609/drift-demo.dptdywfy/restore.log)

[tests/legacy-regression/run-20261125T220404-14609/operations.log](tests/legacy-regression/run-20261125T220404-14609/operations.log)

[tests/legacy-regression/run-20261125T220404-14609/ords-install.log](tests/legacy-regression/run-20261125T220404-14609/ords-install.log)

[tests/legacy-regression/run-20261125T220404-14609/ords-uninstall.log](tests/legacy-regression/run-20261125T220404-14609/ords-uninstall.log)

[tests/legacy-regression/run-20261125T220404-14609/runtime.log](tests/legacy-regression/run-20261125T220404-14609/runtime.log)

[tests/legacy-regression/run-20261125T221759-30355/drift-demo.8l7hor0t/capture.log](tests/legacy-regression/run-20261125T221759-30355/drift-demo.8l7hor0t/capture.log)

[tests/legacy-regression/run-20261125T221759-30355/drift-demo.8l7hor0t/inject.log](tests/legacy-regression/run-20261125T221759-30355/drift-demo.8l7hor0t/inject.log)

[tests/legacy-regression/run-20261125T221759-30355/drift-demo.8l7hor0t/restore.log](tests/legacy-regression/run-20261125T221759-30355/drift-demo.8l7hor0t/restore.log)

[tests/legacy-regression/run-20261125T221759-30355/operations.log](tests/legacy-regression/run-20261125T221759-30355/operations.log)

[tests/legacy-regression/run-20261125T221759-30355/ords-install.log](tests/legacy-regression/run-20261125T221759-30355/ords-install.log)

[tests/legacy-regression/run-20261125T221759-30355/ords-uninstall.log](tests/legacy-regression/run-20261125T221759-30355/ords-uninstall.log)

[tests/legacy-regression/run-20261125T221759-30355/runtime.log](tests/legacy-regression/run-20261125T221759-30355/runtime.log)

[tests/legacy-regression/run-20261125T221759-30355/sqlcl-version.log](tests/legacy-regression/run-20261125T221759-30355/sqlcl-version.log)

[tests/legacy-regression/run-20261125T223454-49405/sqlcl-version.log](tests/legacy-regression/run-20261125T223454-49405/sqlcl-version.log)

[tests/live-demo.log](tests/live-demo.log)

[tests/live-handover-current.log](tests/live-handover-current.log)

[tests/live-retained-history.log](tests/live-retained-history.log)

[tests/new-integration-retry.log](tests/new-integration-retry.log)

[tests/new-integration-retry2.log](tests/new-integration-retry2.log)

[tests/owned-pdb-cleanup.log](tests/owned-pdb-cleanup.log)

[tests/private-default-author-live.log](tests/private-default-author-live.log)

[tests/private-default-routing-unit.log](tests/private-default-routing-unit.log)

[tests/private-policy-author-final.log](tests/private-policy-author-final.log)

[tests/private-policy-unit-final.log](tests/private-policy-unit-final.log)

[tests/regression-generated/progress/E.5/tests/mutation-detected.log](tests/regression-generated/progress/E.5/tests/mutation-detected.log)

[tests/regression-generated/progress/E.5/tests/utplsql-full.log](tests/regression-generated/progress/E.5/tests/utplsql-full.log)

[tests/regression-generated/progress/E.5/tests/utplsql-reordered.log](tests/regression-generated/progress/E.5/tests/utplsql-reordered.log)

[tests/regression-generated/progress/E.5/tests/utplsql-repeat.log](tests/regression-generated/progress/E.5/tests/utplsql-repeat.log)

[tests/regression-generated/progress/E.6/tests/compat-1.0.1.log](tests/regression-generated/progress/E.6/tests/compat-1.0.1.log)

[tests/regression-generated/progress/E.6/tests/compat-1.0.log](tests/regression-generated/progress/E.6/tests/compat-1.0.log)

[tests/regression-generated/progress/E.6/tests/compat-1.1.log](tests/regression-generated/progress/E.6/tests/compat-1.1.log)

[tests/regression-generated/progress/E.6/tests/compat-restored-consumers.log](tests/regression-generated/progress/E.6/tests/compat-restored-consumers.log)

[tests/regression-generated/progress/E.6/tests/incompatible-detected.log](tests/regression-generated/progress/E.6/tests/incompatible-detected.log)

[tests/regression-generated/progress/E.6/tests/sessions-after.log](tests/regression-generated/progress/E.6/tests/sessions-after.log)

[tests/regression-generated/progress/E.6/tests/sessions-before.log](tests/regression-generated/progress/E.6/tests/sessions-before.log)

[tests/regression-generated/progress/E.6/tests/unit.log](tests/regression-generated/progress/E.6/tests/unit.log)

[tests/regression-generated/progress/E.8/tests/pr-backend/backend-failure.log](tests/regression-generated/progress/E.8/tests/pr-backend/backend-failure.log)

[tests/regression-generated/progress/E.8/tests/pr-backend/backend.log](tests/regression-generated/progress/E.8/tests/pr-backend/backend.log)

[tests/regression-generated/progress/E.8/tests/pr-migration/migration-failure.log](tests/regression-generated/progress/E.8/tests/pr-migration/migration-failure.log)

[tests/regression-generated/progress/E.8/tests/pr-migration/migration.log](tests/regression-generated/progress/E.8/tests/pr-migration/migration.log)

[tests/regression-generated/progress/E.8/tests/pr-state/state-failure.log](tests/regression-generated/progress/E.8/tests/pr-state/state-failure.log)

[tests/regression-generated/progress/E.8/tests/pr-state/state.log](tests/regression-generated/progress/E.8/tests/pr-state/state.log)

[tests/regression-generated/progress/E.9/tests/service/direct-write.log](tests/regression-generated/progress/E.9/tests/service/direct-write.log)

[tests/regression-integration.log](tests/regression-integration.log)

[tests/regression-smoke.log](tests/regression-smoke.log)

[tests/regression-unit.log](tests/regression-unit.log)

[tests/reset-owned-fixture.log](tests/reset-owned-fixture.log)

[tests/resume-current-full-integration.log](tests/resume-current-full-integration.log)

[tests/resume-foundation-integration.log](tests/resume-foundation-integration.log)

[tests/resume-full-integration.log](tests/resume-full-integration.log)

[tests/resume-q-reconstruction.log](tests/resume-q-reconstruction.log)

[tests/resume-q-status.log](tests/resume-q-status.log)

[tests/resume-recovery-verification.log](tests/resume-recovery-verification.log)

[tests/resume-regression-smoke.log](tests/resume-regression-smoke.log)

[tests/resume-regression-unit.log](tests/resume-regression-unit.log)

[tests/resume-smoke.log](tests/resume-smoke.log)

[tests/resume-unit.log](tests/resume-unit.log)

[tests/resume-unterminated-manifest.log](tests/resume-unterminated-manifest.log)

[tests/rollback-check.log](tests/rollback-check.log)

[tests/runner-stdin-defect.log](tests/runner-stdin-defect.log)

[tests/runs/E12_RUN_18254/assertions.log](tests/runs/E12_RUN_18254/assertions.log)

[tests/runs/E12_RUN_18254/baseline.log](tests/runs/E12_RUN_18254/baseline.log)

[tests/runs/E12_RUN_18254/catchup.log](tests/runs/E12_RUN_18254/catchup.log)

[tests/runs/E12_RUN_18254/concurrent.log](tests/runs/E12_RUN_18254/concurrent.log)

[tests/runs/E12_RUN_18254/expand-backfill.log](tests/runs/E12_RUN_18254/expand-backfill.log)

[tests/runs/E12_RUN_18254/hello.log](tests/runs/E12_RUN_18254/hello.log)

[tests/runs/E12_RUN_18254/interruption.log](tests/runs/E12_RUN_18254/interruption.log)

[tests/runs/E12_RUN_18254/inventory.log](tests/runs/E12_RUN_18254/inventory.log)

[tests/runs/E12_RUN_18254/legacy-after.log](tests/runs/E12_RUN_18254/legacy-after.log)

[tests/runs/E12_RUN_18254/legacy-before.log](tests/runs/E12_RUN_18254/legacy-before.log)

[tests/runs/E12_RUN_18254/rollback-check.log](tests/runs/E12_RUN_18254/rollback-check.log)

[tests/runs/E12_RUN_18254/unsupported-language.log](tests/runs/E12_RUN_18254/unsupported-language.log)

[tests/runs/E12_RUN_18254/version.log](tests/runs/E12_RUN_18254/version.log)

[tests/runs/E12_RUN_18254/world.log](tests/runs/E12_RUN_18254/world.log)

[tests/runs/E12_RUN_3568/assertions.log](tests/runs/E12_RUN_3568/assertions.log)

[tests/runs/E12_RUN_3568/baseline.log](tests/runs/E12_RUN_3568/baseline.log)

[tests/runs/E12_RUN_3568/catchup.log](tests/runs/E12_RUN_3568/catchup.log)

[tests/runs/E12_RUN_3568/concurrent.log](tests/runs/E12_RUN_3568/concurrent.log)

[tests/runs/E12_RUN_3568/expand-backfill.log](tests/runs/E12_RUN_3568/expand-backfill.log)

[tests/runs/E12_RUN_3568/hello.log](tests/runs/E12_RUN_3568/hello.log)

[tests/runs/E12_RUN_3568/interruption.log](tests/runs/E12_RUN_3568/interruption.log)

[tests/runs/E12_RUN_3568/inventory.log](tests/runs/E12_RUN_3568/inventory.log)

[tests/runs/E12_RUN_3568/legacy-after.log](tests/runs/E12_RUN_3568/legacy-after.log)

[tests/runs/E12_RUN_3568/legacy-before.log](tests/runs/E12_RUN_3568/legacy-before.log)

[tests/runs/E12_RUN_3568/rollback-check.log](tests/runs/E12_RUN_3568/rollback-check.log)

[tests/runs/E12_RUN_3568/unsupported-language.log](tests/runs/E12_RUN_3568/unsupported-language.log)

[tests/runs/E12_RUN_3568/version.log](tests/runs/E12_RUN_3568/version.log)

[tests/runs/E12_RUN_3568/world.log](tests/runs/E12_RUN_3568/world.log)

[tests/runs/E12_RUN_49496/assertions.log](tests/runs/E12_RUN_49496/assertions.log)

[tests/runs/E12_RUN_49496/baseline.log](tests/runs/E12_RUN_49496/baseline.log)

[tests/runs/E12_RUN_49496/catchup.log](tests/runs/E12_RUN_49496/catchup.log)

[tests/runs/E12_RUN_49496/concurrent.log](tests/runs/E12_RUN_49496/concurrent.log)

[tests/runs/E12_RUN_49496/expand-backfill.log](tests/runs/E12_RUN_49496/expand-backfill.log)

[tests/runs/E12_RUN_49496/hello.log](tests/runs/E12_RUN_49496/hello.log)

[tests/runs/E12_RUN_49496/interruption.log](tests/runs/E12_RUN_49496/interruption.log)

[tests/runs/E12_RUN_49496/inventory.log](tests/runs/E12_RUN_49496/inventory.log)

[tests/runs/E12_RUN_49496/legacy-after.log](tests/runs/E12_RUN_49496/legacy-after.log)

[tests/runs/E12_RUN_49496/legacy-before.log](tests/runs/E12_RUN_49496/legacy-before.log)

[tests/runs/E12_RUN_49496/rollback-check.log](tests/runs/E12_RUN_49496/rollback-check.log)

[tests/runs/E12_RUN_49496/unsupported-language.log](tests/runs/E12_RUN_49496/unsupported-language.log)

[tests/runs/E12_RUN_49496/version.log](tests/runs/E12_RUN_49496/version.log)

[tests/runs/E12_RUN_49496/world.log](tests/runs/E12_RUN_49496/world.log)

[tests/runs/E12_RUN_91325/assertions.log](tests/runs/E12_RUN_91325/assertions.log)

[tests/runs/E12_RUN_91325/baseline.log](tests/runs/E12_RUN_91325/baseline.log)

[tests/runs/E12_RUN_91325/catchup.log](tests/runs/E12_RUN_91325/catchup.log)

[tests/runs/E12_RUN_91325/concurrent.log](tests/runs/E12_RUN_91325/concurrent.log)

[tests/runs/E12_RUN_91325/expand-backfill.log](tests/runs/E12_RUN_91325/expand-backfill.log)

[tests/runs/E12_RUN_91325/hello.log](tests/runs/E12_RUN_91325/hello.log)

[tests/runs/E12_RUN_91325/interruption.log](tests/runs/E12_RUN_91325/interruption.log)

[tests/runs/E12_RUN_91325/inventory.log](tests/runs/E12_RUN_91325/inventory.log)

[tests/runs/E12_RUN_91325/legacy-after.log](tests/runs/E12_RUN_91325/legacy-after.log)

[tests/runs/E12_RUN_91325/legacy-before.log](tests/runs/E12_RUN_91325/legacy-before.log)

[tests/runs/E12_RUN_91325/live-demo.log](tests/runs/E12_RUN_91325/live-demo.log)

[tests/runs/E12_RUN_91325/new-integration-retry.log](tests/runs/E12_RUN_91325/new-integration-retry.log)

[tests/runs/E12_RUN_91325/new-integration-retry2.log](tests/runs/E12_RUN_91325/new-integration-retry2.log)

[tests/runs/E12_RUN_91325/regression-integration.log](tests/runs/E12_RUN_91325/regression-integration.log)

[tests/runs/E12_RUN_91325/regression-smoke.log](tests/runs/E12_RUN_91325/regression-smoke.log)

[tests/runs/E12_RUN_91325/regression-unit.log](tests/runs/E12_RUN_91325/regression-unit.log)

[tests/runs/E12_RUN_91325/reset-owned-fixture.log](tests/runs/E12_RUN_91325/reset-owned-fixture.log)

[tests/runs/E12_RUN_91325/resume-foundation-integration.log](tests/runs/E12_RUN_91325/resume-foundation-integration.log)

[tests/runs/E12_RUN_91325/unsupported-language.log](tests/runs/E12_RUN_91325/unsupported-language.log)

[tests/runs/E12_RUN_91325/version.log](tests/runs/E12_RUN_91325/version.log)

[tests/runs/E12_RUN_91325/world.log](tests/runs/E12_RUN_91325/world.log)

[tests/runs/E12_RUN_93135/assertions.log](tests/runs/E12_RUN_93135/assertions.log)

[tests/runs/E12_RUN_93135/baseline.log](tests/runs/E12_RUN_93135/baseline.log)

[tests/runs/E12_RUN_93135/catchup.log](tests/runs/E12_RUN_93135/catchup.log)

[tests/runs/E12_RUN_93135/concurrent.log](tests/runs/E12_RUN_93135/concurrent.log)

[tests/runs/E12_RUN_93135/expand-backfill.log](tests/runs/E12_RUN_93135/expand-backfill.log)

[tests/runs/E12_RUN_93135/hello.log](tests/runs/E12_RUN_93135/hello.log)

[tests/runs/E12_RUN_93135/interruption.log](tests/runs/E12_RUN_93135/interruption.log)

[tests/runs/E12_RUN_93135/inventory.log](tests/runs/E12_RUN_93135/inventory.log)

[tests/runs/E12_RUN_93135/legacy-after.log](tests/runs/E12_RUN_93135/legacy-after.log)

[tests/runs/E12_RUN_93135/legacy-before.log](tests/runs/E12_RUN_93135/legacy-before.log)

[tests/runs/E12_RUN_93135/rollback-check.log](tests/runs/E12_RUN_93135/rollback-check.log)

[tests/runs/E12_RUN_93135/unsupported-language.log](tests/runs/E12_RUN_93135/unsupported-language.log)

[tests/runs/E12_RUN_93135/version.log](tests/runs/E12_RUN_93135/version.log)

[tests/runs/E12_RUN_93135/world.log](tests/runs/E12_RUN_93135/world.log)

[tests/runs/E12_RUN_96263/assertions.log](tests/runs/E12_RUN_96263/assertions.log)

[tests/runs/E12_RUN_96263/baseline.log](tests/runs/E12_RUN_96263/baseline.log)

[tests/runs/E12_RUN_96263/catchup.log](tests/runs/E12_RUN_96263/catchup.log)

[tests/runs/E12_RUN_96263/concurrent.log](tests/runs/E12_RUN_96263/concurrent.log)

[tests/runs/E12_RUN_96263/expand-backfill.log](tests/runs/E12_RUN_96263/expand-backfill.log)

[tests/runs/E12_RUN_96263/hello.log](tests/runs/E12_RUN_96263/hello.log)

[tests/runs/E12_RUN_96263/interruption.log](tests/runs/E12_RUN_96263/interruption.log)

[tests/runs/E12_RUN_96263/inventory.log](tests/runs/E12_RUN_96263/inventory.log)

[tests/runs/E12_RUN_96263/legacy-after.log](tests/runs/E12_RUN_96263/legacy-after.log)

[tests/runs/E12_RUN_96263/legacy-before.log](tests/runs/E12_RUN_96263/legacy-before.log)

[tests/runs/E12_RUN_96263/rollback-check.log](tests/runs/E12_RUN_96263/rollback-check.log)

[tests/runs/E12_RUN_96263/unsupported-language.log](tests/runs/E12_RUN_96263/unsupported-language.log)

[tests/runs/E12_RUN_96263/version.log](tests/runs/E12_RUN_96263/version.log)

[tests/runs/E12_RUN_96263/world.log](tests/runs/E12_RUN_96263/world.log)

[tests/unsupported-language.log](tests/unsupported-language.log)

[tests/version.log](tests/version.log)

[tests/world.log](tests/world.log)
