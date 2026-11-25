# E.10 verification

## Results and interpretation

A1 smoke: 1 entry passed, syntax only. A2 unit: 1 entry containing 3 unittest cases passed. A3 integration: 1 driver passed all embedded assertions using real containers. B1 full smoke regression: 8 entries passed. B2 full unit regression: 7 entries passed. No integration regression was selected in PLAN. No mandatory failure was waived using the generic YOLO percentage threshold. Initial unit red run failed because the test target did not yet exist; it is retained as test-first evidence, not a behavioral result.

## Requirement-to-evidence checklist

PBI-072, [authoritative criterion](../../BACKLOG.md#pbi-072-validate-separation-of-proposed-code-and-privileged-validation): IT-1 verifies the unmounted trusted path/socket/token is unavailable, read-only policy cannot be changed, mount privilege is denied and the trusted policy remains unchanged. UT-1 and IT-1 serialize adversarial shell review text as JSON without executing it. Captured candidate output and report records contain no trusted marker. No cache is mounted or retained. PASS within the selected container boundary; host/kernel compromise is unverified and not claimed.

PBI-073, [authoritative criterion](../../BACKLOG.md#pbi-073-validate-concurrent-pr-isolation-and-superseded-run-cancellation): IT-1 creates A/B/release concurrently, checks each private credential file, removes superseded A, confirms B/release are still running, and exercises deduplication, stale refusal and deliberate retry. UT-1 checks exact state transitions and duplicate completion refusal. PASS for local stream/data/external filesystem effects; remote PR events are not exercised.

PBI-074, [authoritative criterion](../../BACKLOG.md#pbi-074-validate-bounded-waits-and-cleanup-after-interrupted-testing): IT-1 validates unavailable runtime failure after three bounded attempts, successful/failed commands, timeout cleanup, own-stream cancellation, actual SIGKILL orphan existence and independent recovery. An actual unavailable cleanup transport raises and recovery reaps the leftover resource; foreign session cleanup is denied and its container remains running. UT-1 verifies exactly one assertion attempt and three transport-timeout attempts. PASS. Process-call and cleanup deadlines are separate; this does not promise a single global 3-second teardown.

The [plan](../../PLAN.md#sprint-e10---validate-secure-isolated-execution-and-interrupted-cleanup) additionally requires separated validator authority and preservation of the independent release stream: both are checked in IT-1. [P8/P9](../../RUPStrikesBack.patch/RUP_patch.md#p8-reconcile-documentation-and-verify-before-each-commit) audit, presentation, demonstration and local closure are recorded separately; automated tests alone do not fulfill them.

## Reproduction and script explanation

The test runner sources each registered function from its domain script. Smoke compiles Python, unit invokes the isolated registry/retry/JSON tests, and integration invokes the real container journey explained in the [walkthrough](sprint_E.10_increment_demo.md). Expected output ends in `Tests: 1; failed: 0` for each new-code gate. Regression ends in 8 and 7 entries respectively, both with zero failures. Prerequisites are the walkthrough's running named Podman connection and pinned image.

```bash
cd "$(git rev-parse --show-toplevel)"
bash tests/run.sh --smoke --new-only progress/E.10/new_tests.manifest
bash tests/run.sh --unit --new-only progress/E.10/new_tests.manifest
bash tests/run.sh --integration --new-only progress/E.10/new_tests.manifest
bash tests/run.sh --smoke
bash tests/run.sh --unit
```

## Artifacts

[A1](test_run_A1_smoke_20261125_192728.log), [A2](test_run_A2_unit_20261125_192728.log), [A3](test_run_A3_integration_20261125_192849.log), [B1](test_run_B1_smoke_20261125_192812.log), [B2](test_run_B2_unit_20261125_192818.log), [initial red](tests/red-unit.log), [pinned pull](tests/pinned-pull.log), [presentation finalization](tests/presentation-finalization.log). The filenames identify this execution date; no earlier sprint pass is reused as fresh evidence.
