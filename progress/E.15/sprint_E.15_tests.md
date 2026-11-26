# E.15 verification record

[Design](sprint_E.15_design.md) owns mechanisms and test specification; [checklist](sprint_E.15_checklist.md) maps authoritative acceptance to evidence. All six required gates passed without a threshold exception. Earlier failed and invalidated attempts remain retained and are not counted as passes.

## Gate outcomes and what they prove

A1 smoke passed 1/1: validator/controller compilation and workflow syntax. A2 unit passed 2/2: bounded input loading and receipt-identity rejection contracts. The receipt unit case uses injected API boundaries and is explicitly not hosted acceptance evidence. A3 integration passed 1/1: a newly correlated real GitHub-hosted Oracle run, initialized private sentinel, actual greeting/schema assertions and explicit publication HTTP 403.

B1 full smoke regression passed 14/14. B2 full unit regression passed 16/16. B3 full integration regression passed 24/24, including real historical Oracle/APEX delivery, preservation, backend/contracts, candidate/review, isolated execution, reproduction and Foundation cases plus hosted Oracle. The runner's complete frozen-source check passed: all 253 executable scripts/tests still match its recorded snapshot. No mandatory case was skipped to make the gate pass.

[Quality-gates receipt](tests/quality-gates.json) records exact counts, timestamped logs, original-byte hashes and readable-view hashes. Timestamp suffixes use the original log completion modification time in UTC. Exact original bytes are preserved losslessly in tests/raw after redacting generated disposable Oracle administrator passwords; readable views normalize trailing whitespace. Fixed public fixture values are not retained production credentials.

## Corrected-boundary acceptance observations

Companion PR 1 reached ordinary protected merge after real Oracle and exact Review at 640bee9f260b52a85a212183fbc1c1938c696473. The full live replay, companion PR 3, reached ordinary protected merge at 2d5a94a55fef741f052a061ee06470439624e3e8. Neither used --admin. The controller independently verified actual candidate-specific run provenance before publication and rechecked current state before merge.

A prior green head was blocked after its source base advanced: the controller reported stale source base and native protection reported the branch was not up to date. Updating the head invalidated the saved receipt. A harmless SQL comment failed exact trusted Review and published failure. A receipt substituting another successful candidate's real run was rejected for missing candidate-specific execution evidence; native merge was refused. These are actual API/native outcomes, not injected policy results.

The candidate repository has Actions disabled, and a real candidate-owned dispatch allocated zero jobs throughout observed peer execution. Only the trusted owner has target write access in the actual configured fixture. A real read-only hosted principal attempting companion status publication received HTTP 403 in run 45787993514. Source code receives no operator credential or executable host context. This qualifies the configured candidate-code boundary, not hostile administrators, arbitrary additional repository writers or organization-wide IAM.

Both real Oracle services were observed after their assertions in Inspection interval. The operator cancelled A (45786123022); its log contains explicit owned container and network removal. B (45786126623) completed successfully, A's validation failed and native merge was refused. Fresh A validation then passed and merged. Earlier image-download cancellation verified network cleanup only and was not substituted for this active-service case. Private sentinel denial was observed after the table was actually created.

## Failed attempts and repairs

The original same-repository design allowed same-app publication spoofing and cross-run cancellation. Code-owner review mitigated merge approval but not cancellation. The explicitly authorized standalone companion with disabled Actions replaced that design. The self-fork API had returned the original repository rather than a new fork; no nonexistent fork network is claimed.

Workflow YAML parsing and report checkout defects were repaired and rerun. The first full integration attempt invalidated its result because executable test sources changed during execution. A following retry was interrupted. A later 24-entry run passed 23 entries and failed the hosted checker because it assumed exactly one job; dispatch also reports a skipped PR-only publisher. The corrected checker explicitly requires a successful Oracle job and allows only the documented job names/conclusions. The focused and complete retries passed. Despite its filename, regression-integration-final.log is a superseded failed attempt; regression-integration-qualified.log and the timestamped B3 log own the passing gate.

GitHub retained a queued zero-job dispatch record in the disabled companion. Normal cancellation, force-cancellation and deletion returned incompatible-state/permission errors. This platform metadata limit is recorded without claiming a runner was cleaned up when none was allocated. Active Oracle cleanup is proven separately.

## Source, toolchain and evidence preservation

The validator/controller/Review core is pinned at trusted tag e15-qualified, commit f98403720cd8c6fa49cba9a019590c08767db648. The later authority-probe/documentation commit leaves those core files byte-identical; the probe itself ran successfully at its recorded source. The candidate baseline and accepted history are pinned and bundled. The new workflow uses pinned Oracle image digest cebd977833411a42170777d8e9ccf616a028a2bb137ae96498354ab6c7510268 and oracledb 3.4.1.

Historical full regression uses qualified SQLcl 25.3.0.274.1210 before native target preparation. E.15 does not alter SQLcl PROJECT metadata, upgrade a toolchain or claim E.16 native release acceptance. The full runner generated private inputs outside the checkout and preserved its source/version receipts. Its 545 generated historical output paths were archived under E.15; earlier sprint evidence was restored rather than rewritten. [Archive inventory](tests/historical-regression-inventory.json), [exact archive](tests/historical-regression-evidence.tar.gz), [source verification](tests/qualified-source-verification.json).

## Artifacts

- [test_run_A1_smoke_20261126_085433.log](test_run_A1_smoke_20261126_085433.log)
- [test_run_A2_unit_20261126_085433.log](test_run_A2_unit_20261126_085433.log)
- [test_run_A3_integration_20261126_085607.log](test_run_A3_integration_20261126_085607.log)
- [test_run_B1_smoke_20261126_090232.log](test_run_B1_smoke_20261126_090232.log)
- [test_run_B2_unit_20261126_090241.log](test_run_B2_unit_20261126_090241.log)
- [test_run_B3_integration_20261126_085730.log](test_run_B3_integration_20261126_085730.log)
- [tests/accepted-oracle.log](tests/accepted-oracle.log)
- [tests/accepted-publisher.log](tests/accepted-publisher.log)
- [tests/all-workflow-syntax.log](tests/all-workflow-syntax.log)
- [tests/clean-validator-clone.log](tests/clean-validator-clone.log)
- [tests/companion-accepted-controller.log](tests/companion-accepted-controller.log)
- [tests/companion-accepted-receipt.log](tests/companion-accepted-receipt.log)
- [tests/companion-active-cancel-controller.log](tests/companion-active-cancel-controller.log)
- [tests/companion-base-maintenance.log](tests/companion-base-maintenance.log)
- [tests/companion-cancelled-cleanup.log](tests/companion-cancelled-cleanup.log)
- [tests/companion-cleanup-final-a-controller.log](tests/companion-cleanup-final-a-controller.log)
- [tests/companion-cleanup-final-b-controller.log](tests/companion-cleanup-final-b-controller.log)
- [tests/companion-cleanup-final-b.log](tests/companion-cleanup-final-b.log)
- [tests/companion-cleanup-peer-controller.log](tests/companion-cleanup-peer-controller.log)
- [tests/companion-cleanup-peer-receipt.log](tests/companion-cleanup-peer-receipt.log)
- [tests/companion-first-controller.log](tests/companion-first-controller.log)
- [tests/companion-independent-controller.log](tests/companion-independent-controller.log)
- [tests/companion-independent-receipt.log](tests/companion-independent-receipt.log)
- [tests/companion-live-oracle-cleanup.log](tests/companion-live-oracle-cleanup.log)
- [tests/companion-peer-current-controller.log](tests/companion-peer-current-controller.log)
- [tests/companion-peer-current-receipt.log](tests/companion-peer-current-receipt.log)
- [tests/companion-publication-authority.log](tests/companion-publication-authority.log)
- [tests/cross-candidate-attack.log](tests/cross-candidate-attack.log)
- [tests/document-links.log](tests/document-links.log)
- [tests/freshness-publisher.log](tests/freshness-publisher.log)
- [tests/freshness-validator.log](tests/freshness-validator.log)
- [tests/hosted-baseline.log](tests/hosted-baseline.log)
- [tests/hosted-candidate-b.log](tests/hosted-candidate-b.log)
- [tests/hosted-unauthorized-read.log](tests/hosted-unauthorized-read.log)
- [tests/live-companion-controller.log](tests/live-companion-controller.log)
- [tests/live-companion-receipt.log](tests/live-companion-receipt.log)
- [tests/live-oracle.log](tests/live-oracle.log)
- [tests/new-integration-qualified.log](tests/new-integration-qualified.log)
- [tests/new-integration-retry.log](tests/new-integration-retry.log)
- [tests/new-integration.log](tests/new-integration.log)
- [tests/new-smoke-current.log](tests/new-smoke-current.log)
- [tests/new-smoke-qualified.log](tests/new-smoke-qualified.log)
- [tests/new-smoke.log](tests/new-smoke.log)
- [tests/new-unit-current.log](tests/new-unit-current.log)
- [tests/new-unit-qualified.log](tests/new-unit-qualified.log)
- [tests/new-unit.log](tests/new-unit.log)
- [tests/qualified-core-source-diff.log](tests/qualified-core-source-diff.log)
- [tests/regression-integration-final.log](tests/regression-integration-final.log)
- [tests/regression-integration-qualified.log](tests/regression-integration-qualified.log)
- [tests/regression-integration-retry.log](tests/regression-integration-retry.log)
- [tests/regression-integration.log](tests/regression-integration.log)
- [tests/regression-smoke-current.log](tests/regression-smoke-current.log)
- [tests/regression-smoke-qualified.log](tests/regression-smoke-qualified.log)
- [tests/regression-smoke.log](tests/regression-smoke.log)
- [tests/regression-unit-current.log](tests/regression-unit-current.log)
- [tests/regression-unit-qualified.log](tests/regression-unit-qualified.log)
- [tests/regression-unit.log](tests/regression-unit.log)
- [tests/rehearsal-baseline-preparation.log](tests/rehearsal-baseline-preparation.log)
- [tests/review-initial-failure.log](tests/review-initial-failure.log)
- [tests/walkthrough-shell-syntax.log](tests/walkthrough-shell-syntax.log)
