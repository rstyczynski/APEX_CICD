# E.15 verification record — acceptance remains open

[Design](sprint_E.15_design.md) owns the test specification; [checklist](sprint_E.15_checklist.md) owns mandatory outcomes. [Remaining-requirement audit](sprint_E.15_blockers.md) separates the unresolved authority failure from recoverable implementation/test issues.

## New-code gates

SM-15: `bash tests/run.sh --smoke --new-only progress/E.15/new_tests.manifest` passed 1/1. It compiles the trusted validator and validates workflow YAML with actionlint. It does not prove hosted behavior.

UT-15: `bash tests/run.sh --unit --new-only progress/E.15/new_tests.manifest` passed 1/1. It proves empty/oversized/wrong-path inputs are rejected and valid fixture text is loaded. It does not execute Oracle or prove merge authority.

IT-15: `bash tests/run.sh --integration --new-only progress/E.15/new_tests.manifest` passed 1/1. It dispatched a newly correlated GitHub-hosted run, waited for its terminal result, and required actual Oracle success, the initialized private sentinel and explicit publication HTTP 403. Run 45780060548 at adda0100ccd4e4f8a3adbe7d381c9da2d9af0a5a passed; this is fresh execution, not replay of a receipt. It does not establish the full integrated negative acceptance set.

## Regression

`bash tests/run.sh --smoke` passed 14/14 and `bash tests/run.sh --unit` passed 15/15, including the registered hosted-domain checks. The complete integration suite uses the existing isolated historical regression database with generated temporary private inputs and the qualified SQLcl 25.3.0.274.1210 native APEX client. It checks the actual client before preparing its disposable target. It does not change SQLcl PROJECT metadata or qualify a release upgrade.

The first full integration result was invalidated by its source-stability assertion: new hosted-domain test sources and manifest entries changed during execution. Its case passes do not constitute a passing full gate. The following retry was interrupted before completion. `bash tests/run.sh --integration` is now executing against frozen sources; its final result is pending in regression-integration-final.log. No source-stability check will be skipped.

## Real GitHub/Oracle observations

PR 4: real Oracle greeting/schema and private-sentinel checks, trusted exact-byte Review, separate code-owner approval and ordinary merge all verified. Run 45781363137 attempt 1 was cancelled by the cross-candidate authority test; attempt 2 passed, and PR 4 merged without --admin at 8ee003ad9f45ae62d5fe0d1a0bb389e311c1b27a. The rerun proves recovery of that path, not prevention of interference.

PR 3: Oracle refused the actual private sentinel read with ORA-00942 after the table was initialized. This is a real negative schema-access result. A missing table before initialization would not prove the same claim; initial baseline evidence is labelled accordingly.

A read-only trusted job token received explicit HTTP 403 on publication. A branch-owned workflow requesting checks:write nevertheless published an Integrated check under the same GitHub Actions app. Strict expected-app identity alone therefore failed the intended authority boundary. Native required code-owner review was added and an invalid ordinary merge was refused. Code-owner syntax was checked by the GitHub API with zero errors.

The same-repository candidate workflow subsequently requested actions:write and cancelled another candidate run. This unresolved hosted failure prevents overall acceptance. Current safeguards are respected; no new exploit escalation is required to preserve that conclusion.

A harmless comment-only fixture now exercises stale native review dismissal and trusted report-byte mismatch. Record the terminal current run and refreshed review state before claiming that case complete. No successful positive merge substitutes for freshness or corrected isolation.

## Artifacts

All completed readable log views have lossless original bytes in tests/raw when whitespace normalization was needed. Logs redact generated disposable SYS/SYSTEM passwords; fixed fixture passwords are public nonsecret test inputs. GitHub token values remain masked.

New gates: [smoke](tests/new-smoke.log), [unit](tests/new-unit.log), [integration](tests/new-integration.log).

Regression: [smoke](tests/regression-smoke.log), [unit](tests/regression-unit.log), [invalidated integration](tests/regression-integration.log), [interrupted retry](tests/regression-integration-retry.log), [current final retry](tests/regression-integration-final.log).

Hosted evidence: [baseline](tests/hosted-baseline.log), [candidate B](tests/hosted-candidate-b.log), [private-read rejection](tests/hosted-unauthorized-read.log), [report checkout failure](tests/review-initial-failure.log), [cross-candidate authority](tests/cross-candidate-attack.log), [ordinary merge](tests/ordinary-merge.json), [owner review](tests/owner-review.json), [protection](tests/current-protection.json), [invalid merge refusal](tests/codeowner-invalid-merge-refusal.txt), [freshness before](tests/freshness-before.json), [freshness after](tests/freshness-after.json), [freshness merge refusal](tests/freshness-merge-refusal.txt).

Additional API receipts, interrupted-run details, presentation validation and exact reviewed diffs are retained in the same tests directory. The complete inventory is generated during final reconciliation; pending artifacts are not declared passed.
