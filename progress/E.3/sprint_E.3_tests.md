# E.3 — Test execution and experiment results

## Added validation LC-1 — accepted

The Product Owner accepted the lifecycle mapping on 2026-11-05 and explicitly
removed the separate pending-acceptance/report requirement. The
[accepted mapping and gap dispositions](sprint_E.3_pipeline_scope.md#lc-1--oracle-apex-lifecycle-alignment-validation)
record the paper references, retained evidence and backlog owners. Slides
19–21 present the mapping; identified follow-up is tracked by existing items
and new PBI-056/057. LC-1 is accepted for the demonstrated E.3 slice. This is
an accepted documentary assessment using retained evidence, not a new runtime
test or proof that deferred capabilities have been delivered.

Configuration update: the [GitHub-owned setup](sprint_E.3_github_configuration.md) supersedes every retained-local-file/tool-path assumption below. Earlier run results remain historical evidence for their original revisions.

Current correction — 2026-11-03: the Product Owner required native APEX/SQLcl
and GitHub Actions control, with all E.3 Python removed. The
[native correction record](sprint_E.3_native_correction.md) supersedes the earlier
1.0.1 implementation described below. Historical evidence is retained.

2026-11-03. Test: smoke, integration. Regression: smoke. The
[accepted design](sprint_E.3_design.md) defines SM-1/IT-1/IT-2;
[implementation](sprint_E.3_implementation.md) explains fixes. The
[walkthrough](sprint_E.3_increment_demo.md) connects commands, screens and results.
[Handover](sprint_E.3_handover.md) owns the delivery boundary. This is prototype
validation, not production qualification or full E.1 regression acceptance.

## Current command behavior — reference evidence, not a new LAB journey

The copyable parent commands below run static/reference checks. Integration
IT-1/IT-2 read the fixed seed journey from github-environment-journey.json,
deployment 41679427616 and qualification 41679432928, v1.0.4. They download old
run artifacts and inspect their logs/receipts; they do not create a new native
defect or qualification run and need no private preservation snapshot. Current
platform smoke probes the seed-configured login form and needs seed environment
API permission. These commands do not accept the operator's selected LAB replay.
The [test profile](../../docs/test-profile.md#e3-implemented-pipeline-checks)
and [manual](user_manual.md) identify access requirements and new-run acceptance.
The older accounts below remain historical and are not fresh execution claims.

## Review correction checks — 2026-11-04

`bash tests/unit/test_missing_changeset.sh` passed 21/21 offline diagnostic and
receipt cases. It runs the actual shared AWK/jq assertions on retained logs and
synthetic fixtures, including unrelated errors, wrong paths, incomplete output,
ANSI/padding/wrapping and legacy/new receipt constraints. `bash tests/run.sh
--smoke --new-only progress/E.3/new_tests.manifest` passed 1/1 static smoke.
These are proportionate offline review regressions, not a new native workflow
or a rerun of the reference integrations/platform smoke. The
[diagnostic log](tests/review-1-offline-diagnostics.log),
[static smoke log](tests/review-1-static-smoke.log) and
[correction receipt](tests/review-1-correction-checks.json) record the results.
Slides 4/10 were inspected before/after; package/import/layout and source/link
checks passed. No database, deployment or qualification was dispatched.

## Historical quality-gate execution

A1 new smoke passed: 1/1 registered test, including actionlint, script checks,
workflow deployment separation and nine label/title classification examples.
A3 new integration passed: 2/2 tests, checking live GitHub/Oracle evidence and a
real native verification rejection. B1 full smoke regression passed: 2/2 tests,
including the existing Oracle SQL/ORDS/APEX baseline and the new pipeline smoke.
No unit or broader regression suites were requested; A2/B2/B3 were not run.
No flaky failure was deferred and no retry threshold was exhausted. A further
isolated [capture helper rehearsal](tests/capture-rehearsal.json) ran capture.sh,
the pre-stage adapter, native stage and zero-error verify against the same live
Main without deployment. It closes the reusable-command verification question,
not an independent full environment reproduction claim.

Reproduce from the parent Git root with the prepared lab and gh access:

```bash
cd "$(git rev-parse --show-toplevel)"
bash tests/run.sh --smoke --new-only progress/E.3/new_tests.manifest
bash tests/run.sh --integration --new-only progress/E.3/new_tests.manifest
bash tests/run.sh --smoke
```

Expected registered totals are 1/0, 2/0 and 2/0 tests/failed respectively.
These commands now fetch fixed seed evidence; they do not create/delete a
native experiment clone, inject a defect or read a private preservation snapshot.
The older clone-based integration execution described elsewhere is historical.
Artifact availability and seed environment API access can limit repetition.

## Native and hosted observations

Working Copy 100 saved the Home heading; native comparison reported one changed
page. The selected Main merge completed successfully. New native exports/stages
verified with Errors 0, Warnings 0, Info 15 using the pinned 25.4.1 client.
The source-level runtime adapter was reviewed and staged before verification.
No E.2 verification waiver was reused.

[PR 1](https://github.com/rstyczynski/APEX_CICD_E3/pull/1) and
[PR 3](https://github.com/rstyczynski/APEX_CICD_E3/pull/3) passed hosted checks,
were squash merged and accumulated into
[release PR 2](https://github.com/rstyczynski/APEX_CICD_E3/pull/2).
Its final head was manually checked in
[run 41664109570](https://github.com/rstyczynski/APEX_CICD_E3/actions/runs/41664109570).
The generated CHANGELOG.md and
[GitHub v1.0.1 notes](https://github.com/rstyczynski/APEX_CICD_E3/releases/tag/v1.0.1)
contain the same two fixes. The tag resolves to release-PR commit
2e203ba571bbce9fd30cafc5531e36250d5594b2.

The [pre-dispatch observation](tests/pre-dispatch.json) records the original
heading and unchanged prior fields after integration. The first manual
[run 41664285664](https://github.com/rstyczynski/APEX_CICD_E3/actions/runs/41664285664)
failed before target mutation because PROJECT expected a named branch rather
than detached HEAD. [PR 4](https://github.com/rstyczynski/APEX_CICD_E3/pull/4)
corrected only the main workflow's build branch; it passed hosted checks.
The tag was not moved. Retrying that version in
[run 41664798289](https://github.com/rstyczynski/APEX_CICD_E3/actions/runs/41664798289)
succeeded: native verification, one native archive, deployment and preservation.
That deployed **application 810203 / E3_TARGET**, not retained UAT.

The [receipt](tests/release-receipt.json) binds tag, exact source SHA and archive
SHA-256 3553480967f5aa4492e90192e508221e9630ecee0c10ccdbbb2a8a7bea3ffb22.
IT-1 re-queries merged PRs, tag and successful manual run, verifies actual downloaded
archive bytes against that hash, compares release notes with the committed
changelog and checks current Oracle data against the private pre-release baseline.
The comparison covers every field in the seven business tables, including the
one existing Hello World history row. It does not equate data equality with
schema/application drift protection.

Browser verification after deployment signed in as LAB_USER and showed the
new heading and retained Hello World history. The [observation](tests/browser.json)
and Home/history PNGs retain those results. The APEX display-version footer is
still 1.0.0, while the repository release/tag and receipt are v1.0.1. Automatic
APEX display-version stamping was not qualified; component versions and release
versions must not be conflated.

IT-2 removed one included SQL changeset in a throwaway clone and ran real PROJECT
verify. The native missing-file failure was required, no deploy was called, and
the target snapshot remained identical. This is a pre-deployment rejection,
not proof of rollback, repair or fencing after committed DDL.

## Material failures and corrections

Slash-containing native stage paths reproduced the source/dist verification
problem: use explicit slashless demo branches. A repository-relative mapping
file was absent from the archive search path: supply the committed file by its
computed absolute checkout path. The inherited E1_CTRL session hook blocked the
native target's login: replace it in reviewed pre-stage source with the existing
application readiness assertion. Detached HEAD failed native verification on
the first remote run: attach the selected tag to a named local build branch.
All are deterministic failures; their correction/evidence remain visible.

Release Please has now prepared [PR 5 for 1.0.2](https://github.com/rstyczynski/APEX_CICD_E3/pull/5)
for the workflow correction. It is intentionally unmerged and undeployed: a
prepared newer version does not change the deployer's explicit choice of 1.0.1.
This is normal release batching/selection, not unfinished application deployment.

## Artifacts

[A1 smoke](tests/test_run_A1_smoke_20261103_153419.log),
[A3 integration](tests/test_run_A3_integration_20261103_153419.log) and
[B1 smoke regression](tests/test_run_B1_smoke_20261103_153419.log) are the final
timestamped gate logs. [Earlier integration](tests/integration.log) and
[earlier smoke regression](tests/regression-smoke.log) record exploratory checks.
[Readable native rejection output](tests/native-verification-rejection.log) and
[rejection receipt](tests/rejection.json) support IT-2.

[Journey identities](tests/journey.json), [release receipt](tests/release-receipt.json),
[pre-dispatch target](tests/pre-dispatch.json), [browser observation](tests/browser.json),
[bundle identity](tests/bundle.json) and
[remaining version proposal](tests/remaining-release-proposals.json) bind the
retained source and remote execution. [Working Copy edit](tests/working-copy-heading.png),
[native diff](tests/working-copy-diff.png), [merge observation](tests/working-copy-merge.json),
[later readable Working Copy inspection](tests/working-copy-inspection.png), [deployed Home](tests/deployed-home.png)
and [history](tests/deployed-history.png) are actual browser captures.

The design-stage red logs and check receipt are historical design evidence,
not current failures: [smoke](tests/design_red_smoke_20261103_121830.log),
[integration](tests/design_red_integration_20261103_121830.log) and
[receipt](tests/design_checks_20261103_121830.json). Detailed private native
capture/stage/bootstrap logs and business snapshots stay under .local-apex/e3;
credentials and runtime rows are not published as CI artifacts.

The readable rejection log removes SQLcl's trailing table-padding spaces only.
Raw output is retained in the original completion commit and privately under
.local-apex/e3/logs/native-verification-rejection-raw.log; no test facts changed.
