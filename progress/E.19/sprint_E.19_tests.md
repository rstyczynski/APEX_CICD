# E.19 verified test results

## Six required gates

A1 smoke passes 1/1 manifest entry, A2 unit passes 1/1 (five Node contract groups), A3 integration passes 1/1. B1 full smoke passes 18/18, B2 full unit passes 20/20, B3 full integration passes 28/28. The full integration wrapper exits zero after equal executable-source snapshots and private fixture cleanup. No failed gate or waived failure remains. These are manifest-entry counts, not unique functional scenario counts.

New smoke checks Node/Bash/Actions syntax and no Python reference in the native/acceptance workflow. Unit tests exercise the five guard contracts with valid and missing/malformed/mismatched files. New integration revalidates final matrix 45876173032, actual native run 45874462191 and accepted paired timing run 45875517420, including source/run bindings, archive hashes and exact target observations.

## Real behavior and controlled checks

The final matrix invokes 24 actual catalogued actions: five valid and nineteen expected refusals. Each refusal has an outcome assertion and skipped mutation sentinel. Fixtures are synthetic JSON/log/archive inputs in a real GitHub workflow without Python; their filesystem sentinel does not establish Oracle target preservation. Actual native run 45874462191 independently executes SQLcl PROJECT export/stage/verify/release/package, install/additive upgrade/repeat, wrong artifact/source/actual incompatible tool/substituted-byte refusal, equal real target observations, authenticated APEX retained-row rendering and private cleanup. The adapters remain byte-identical and the workflow differs only by one trailing-blank cleanup to the accepted native trial; the native guard implementation prefix is unchanged by later candidate/Review additions. [Applicability audit](tests/source-applicability.log) records that comparison.

Actual PR trial 45875727042 exercises candidate metadata and trusted Review actions against PR 1, then real Oracle greeting, authenticated schema identity, private-table denial and unauthorized-publication HTTP 403. Its initial missing PR-read permission failed in 45875288879 and was repaired; [bug record](sprint_E.19_bugs.md) preserves both observations. The separate Oracle application test intentionally uses Python and remains outside support-check migration.

[Optimization regression](tests/optimization-check.log) actually shows the historical baseline rejects invalid provenance normally, accepts it under Python -O, and the JavaScript action explicitly rejects the same bytes. No target operation is performed in that controlled test.

The [accepted comparison](comparison_report.md) uses paired run 45875517420, five helper processes per batch, two hosts and reversed language order. First invocation n=2 and repeats n=20 per runtime; no installation occurred. Earlier three-helper and unequal-image cohorts remain historical and are excluded from the accepted performance conclusion.

## Full regression scope and limits

Full integration runs the complete unfiltered aggregate. Earlier local-controller/capability/Oracle experiments retain their documented scope and synthetic boundaries. It revalidates immutable native E.16, clean-host E.17 and E.18 capacity receipts and dispatches a fresh actual Oracle validation in this sprint repository, run 45877085121. Receipt revalidation is not a fresh execution of those earlier native experiments. The full gate's E.19 reader used the earlier action matrix and initial three-helper timing receipts as reader-regression inputs; final A3 separately qualifies the final matrix and accepted five-helper paired measurements. The comparison report excludes those earlier timing samples.

Historical regression uses its accepted SQLcl 25.3.0.274.1210 state and the owned isolated fixture; native E.19 uses release 25.4.1.0/build 25.4.1.022.0618 and matching generated metadata. This does not edit a project's required version to bypass compatibility. [Preservation receipt](tests/regression-replay/restoration-receipt.txt) records 162 new outputs retained in E.19 and 59 historical tracked outputs restored byte-for-byte. Original paths remain in raw evidence. No earlier sprint source or unrelated user edits were reverted.

## Demonstration and artifact checks

The developer directly operated the actual guard entrypoint with valid evidence, substituted bytes and restored input; [repeated demo log](tests/live-guard-demo.log) records validation, explicit artifact mismatch, absent mutation and successful recovery. The first attempted shell path was wrong and was corrected before the observed demonstration. The final matrix was inspected in real Chrome; the offline gallery rendered, next/previous navigation worked and a full-resolution image opened. [Gallery verification](tests/gallery-verification.md) distinguishes actual UI checks from static links. The presentation package/render review and final documentation audit are separate retained controls.

## Artifacts

All `test_run_*.log` files below this sprint directory are retained. Timestamped A1/A2/A3/B3 files are explicitly marked snapshots of the original execution logs, with exact commands. Original direct logs remain under their original names. B1/B2 final execution logs include the six-gate manifest counts. Additional exact records are [full integration output](tests/full-integration.log), [initial Node contracts](tests/initial-unit.log), [native execution](tests/native-success.log), [final action matrix](tests/action-matrix-success.log), [candidate failure](tests/candidate-first-failure.log), [candidate success](tests/real-candidate-success.log), [candidate metadata](tests/real-candidate-success.json), [paired timing API metadata](tests/timing-paired-run.json), [measurement data](tests/comparison-summary.json), [local links](tests/handover-links.log) and [slide verification](tests/slide-verification.md). Native archives, receipts, screenshots and run metadata are retained under tests/qualified; historical generated artifacts are indexed under tests/regression-replay.

[test_run_A1_smoke.log](test_run_A1_smoke.log)

[test_run_A1_smoke_20261126_183918.log](test_run_A1_smoke_20261126_183918.log)

[test_run_A2_unit.log](test_run_A2_unit.log)

[test_run_A2_unit_20261126_183918.log](test_run_A2_unit_20261126_183918.log)

[test_run_A3_integration.log](test_run_A3_integration.log)

[test_run_A3_integration_20261126_183918.log](test_run_A3_integration_20261126_183918.log)

[test_run_B1_smoke_20261126_183537.log](test_run_B1_smoke_20261126_183537.log)

[test_run_B2_unit_20261126_183541.log](test_run_B2_unit_20261126_183541.log)

[test_run_B3_integration_20261126_183918.log](test_run_B3_integration_20261126_183918.log)

[Whitespace correction A1](tests/whitespace-A1-smoke.log) passes 1/1 and [full smoke rerun](tests/whitespace-B1-smoke.log) passes 18/18 after the final behavior-neutral YAML cleanup. Full increment git diff --check passes with the existing raw-evidence whitespace policy extended to E.19.
