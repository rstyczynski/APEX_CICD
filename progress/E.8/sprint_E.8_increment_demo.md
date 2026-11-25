# E.8 complete candidate testing walkthrough

Goal: validate the integrated proposed greeting change rather than reusing a previously deployed release. [Plan](../../PLAN.md) and [backlog](../../BACKLOG.md) own scope; [manual](user_manual.md) owns prerequisites and recovery; [handover](sprint_E.8_handover.md) owns acceptance. [Editable deck](sprint_E.8_increment_demo.pptx) follows the stages below.

## 1. Establish the trusted validator — slides 1–4

Open a shell in /Users/rstyczynski/projects/APEX_CICD. Use the prepared host prerequisites in the manual. No network PR publication or GitHub mutation is required. Run:

```bash
python3 tests/test_candidate.py
```

Expected: two unittest groups pass. They challenge unknown/weakened policy, disabled critical coverage, empty/missing suites and reports, skipped/neutral/cancelled/failed results, identity mismatch and first-failure preservation. These are synthetic report checks, not Oracle execution. PBI-067/076.

## 2. Construct and execute the integrated candidate — slides 5–7

```bash
python3 tests/candidate_lab.py
```

Expected: PASS three real integrated candidate cadences and five fail-closed fault paths; scoped cleanup complete. The runner creates a local baseline, proposal branch adding LANGUAGE_CODE, advances main with a separate accepted contribution, then merges. It saves candidate.bundle and integrated.diff before selecting all five mandatory suites. The generated candidate has distinct base, head and merge commits; reports record the merged tree, not just the head. SQL is extracted from that merge. This simulates a PR locally; it does not publish a remote check. PBI-066.

## 3. Inspect each cadence — slides 8–9

```bash
python3 -m json.tool progress/E.8/tests/executions.json
cat progress/E.8/tests/pr-None/backend.log
cat progress/E.8/tests/scheduled-None/backend.log
cat progress/E.8/tests/prerelease-None/backend.log
```

Expected: three successful executions, each with source, migration, compilation, state and backend reports. Oracle prints Hello World in each backend log. Each target is fresh, migration adds a two-character required language column, package compiles, state passes, and the backend result is asserted. PR/scheduled/prerelease are actual locally invoked cadences, not scheduler or GitHub trigger qualification. Unknown paths and contract/migration changes conservatively retain every suite. PBI-066/076.

## 4. Inspect failure and cleanup — slides 10–12

```bash
cat progress/E.8/tests/pr-source/result.json
cat progress/E.8/tests/pr-migration/migration-failure.log
cat progress/E.8/tests/pr-compilation/compilation-failure.log
cat progress/E.8/tests/pr-state/state-failure.log
cat progress/E.8/tests/pr-backend/backend-failure.log
cat progress/E.8/tests/pr-backend/cleanup.log
```

The cheap source failure executes no target preparation. A missing-table migration stops compilation and later work. An invalid package stops state/backend. Wrong column width stops backend. Wrong greeting fails the backend assertion. Reports preserve each earliest failure and missing downstream evidence remains non-success. All created targets are dropped; failure does not modify prior sprint data. The failures are deliberate fixtures, with no hidden passing override. PBI-066/067.

## 5. Review outcomes and limits — slides 13–14

Read [test results](sprint_E.8_tests.md) and [handover](sprint_E.8_handover.md). PBI-066/067/076 are assessed individually. E.9 owns ordinary merge/review controls; E.10 owns security/concurrency/interruption boundaries; E.11 owns reproducibility/performance. They remain Planned. This experiment does not qualify native SQLcl PROJECT production deployment. Re-run only after saving a reviewed evidence snapshot. No human reaction or independent review is inferred from unattended rehearsal.
