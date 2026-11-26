# E.18 test execution results

## Verified result

All six required gates pass without waived failures. New A1 smoke, A2 unit and A3 integration pass one manifest entry each. Full B1 smoke passes 17/17, B2 unit passes 19/19 and B3 integration passes 27/27; the wrapper exits zero after source-stability and scoped-cleanup checks. These are manifest/function counts, not counts of unique native scenarios. [Checklist](sprint_E.18_checklist.md) maps acceptance, [report](capacity_report.md) owns measured results, and [handover](sprint_E.18_handover.md) records demonstration and artifact review.

## What the checks establish

A1 checks workflow/Bash/Python syntax, retention of every named E.17 native stage and byte equality with the existing backend SQL fixtures. A2 uses explicitly synthetic inputs to check statistic arithmetic, missing/failed records and warm-cache-miss refusal; it makes no performance claim. A3 reads actual successful workflow metadata/artifacts for four two-replica cells, binds source/run identity, requires complete native/backend/browser/cleanup success, verifies cold/warm admission, confirms actual serial/concurrent overlap and derives phase/resource statistics. All eight samples use aea3a771cac687fa32ac09d24faf6d2d55bd2342. Forty backend case executions represent five distinct behaviors repeated across eight samples.

The [cohort audit](tests/cohort-isolation.log) additionally checks eight distinct runner execution identities and sixteen author/target namespaces with bound source/run and private cleanup. A repeated hostname in two nonoverlapping jobs is recorded as a physical-identity/warmth limit. [Live verification](tests/live-demo-verification.log) independently checks both complete replicas at 920b1c4a15eaafb000ce73c432322efa20e247f1, including blank-login capture and actual authenticated retained-row rendering. Its timings and population run 45846157988 are excluded from the comparison.

B1/B2 re-run every existing source/platform/unit entry. B3 replays the existing complete historical integration manifest against the owned isolated local fixture and the new acceptance reader. It also dispatches a fresh real Oracle GitHub workflow in the E.18 repository: run 45855180342 at 920b1c4 passes the real greeting, private-table denial and unauthorized-publication HTTP 403 checks. The native E.16 and clean-host E.17 readers revalidate immutable qualified receipts/runs 45810907563 and 45828709006, plus their linked review controls; new downloads are not new native delivery executions. Local review/capability tests retain their documented local/synthetic boundaries.

The historical fixture deliberately uses its qualified SQLcl 25.3.0.274.1210 state; the measured native E.18 projects use qualified 25.4.1.022.0618 and metadata 25.4.1.0. No project version was edited to bypass a native check. Prepared-host regression remains separate from fresh hosted workload qualification. [Test profile](../../docs/test-profile.md#e18-pipeline-capacity-experiment) owns invocation and scope.

## Full-regression evidence preservation

The [replay index](tests/regression-replay/index.json) maps exact generated outputs to their original execution paths and hashes. Sixty-two tracked historical test outputs were restored byte for byte, and 162 new generated files were moved into E.18 after hash checks. [Restoration receipt](tests/regression-replay/restoration-receipt.txt) confirms no historical source/user changes were reverted. Raw paths/timestamps remain as recorded, including host-local timestamps in some historical filenames. These are current regression observations, not rewritten historical acceptance.

[Before-source snapshot](tests/regression-replay/progress/E.12/tests/legacy-regression/run-20261126T164709-4128/source-snapshot-before.json) and [after-source snapshot](tests/regression-replay/progress/E.12/tests/legacy-regression/run-20261126T164709-4128/source-snapshot-after.json) are equal. The full wrapper's successful exit includes that check and private fixture cleanup.

## Failure history and limits

[BUG-18.1/18.2](sprint_E.18_bugs.md) preserve real exploratory installer/privilege errors and corrected native execution; no failed/cancelled trial enters successful timing distributions. Real population cache misses are correctly refused as warm samples. Supplemental hostname QA was corrected to match the actual isolation requirement, with its original condition and evidence retained. No gate failure is deferred as flaky. UI screenshots support observations and do not replace native checks. Production tail latency, physical-host dedication, cost and shared-host packing remain unverified and outside this bounded criterion.

## Artifacts

- [test_run_A1_smoke_20261126_150322.log](test_run_A1_smoke_20261126_150322.log) records its actual command/output and result.
- [test_run_A1_smoke_20261126_150711.log](test_run_A1_smoke_20261126_150711.log) records its actual command/output and result.
- [test_run_A1_smoke_20261126_152028.log](test_run_A1_smoke_20261126_152028.log) records its actual command/output and result.
- [test_run_A1_smoke_20261126_154555.log](test_run_A1_smoke_20261126_154555.log) records its actual command/output and result.
- [test_run_A2_unit_20261126_150322.log](test_run_A2_unit_20261126_150322.log) records its actual command/output and result.
- [test_run_A2_unit_20261126_150711.log](test_run_A2_unit_20261126_150711.log) records its actual command/output and result.
- [test_run_A2_unit_20261126_152028.log](test_run_A2_unit_20261126_152028.log) records its actual command/output and result.
- [test_run_A2_unit_20261126_154556.log](test_run_A2_unit_20261126_154556.log) records its actual command/output and result.
- [test_run_A3_integration_20261126_154556.log](test_run_A3_integration_20261126_154556.log) records its actual command/output and result.
- [test_run_B1_smoke_20261126_154655.log](test_run_B1_smoke_20261126_154655.log) records its actual command/output and result.
- [test_run_B2_unit_20261126_154700.log](test_run_B2_unit_20261126_154700.log) records its actual command/output and result.
- [test_run_B3_integration_20261126_154709.log](test_run_B3_integration_20261126_154709.log) records its actual command/output and result.

[Native failures and repairs](sprint_E.18_bugs.md), [live receipts](tests/live-demo/run.json), [gallery](screenshots/index.html), [gallery browser verification](tests/gallery-verification.md) and [cohort identity diagnostic](tests/cohort-identity-diagnostic.md) provide supporting evidence.
