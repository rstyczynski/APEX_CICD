# E.1 — Construction test results

## Current scope

Platform/bootstrap checks are running while application construction continues. The full selected prototype suite remains incomplete. Initial unit skeletons reported two expected pending failures; this was test-harness preparation, not a passing unit gate.

## Observed results

Pinned tool checks passed for SQLcl 25.3.0.274.1210 and Java 21.0.12.1+1. All five effective schema/PDB/workspace mappings passed. Cross-area read/write rejection passed for all five areas. Platform database/HTTP/static-asset smoke passed. A committed retained TEST marker survived disposable qualification recreation. Oracle-error propagation and SQLcl MERGE persistence passed after the wrapper fix.

Foundation Liquibase validation/installation and explicit assembly assertions passed. Its unchanged repeated SQLcl capture matched all 38 source files byte-for-byte. Private-copy import stability and the complete release/browser scenarios remain pending.

## Artifacts

The platform subset passed its current new-code checks: [A1 smoke](test_run_A1_smoke_20261016_185650.log) and [A3 platform integration](test_run_A3_integration_platform_20261016_185649.log), each with one test and zero failures. [Earlier smoke](test_run_A1_smoke_20261016_185316.log) also passed before the script-file wrapper fix. The platform subset has no isolated unit assertions; application unit skeletons remain pending. These results do not establish a pass for the full selected release suite.

[B1 smoke regression](test_run_B1_smoke_20261016_185912.log) passed with one test and zero failures after the current wrapper/provisioning changes.

Earlier interactive command results support the additional Foundation/capture observations above; they are not relabeled as complete gate logs. The implementation record links the current scripts and limitations.


## Guided operator walkthrough

- Local preflight passed: tools/files and all 12 referenced chapter headings present.
- PTY verification passed: a keypress executed sql -version, the next operation paused, and q stopped before its database call (status 130).
- Noninteractive live invocation was rejected with status 2 and an explanatory error.
- Unattended rehearsal passed all 15 native SQLcl operations, exported application 810001 to staging, showed Git status/diff and ended at the pending-release boundary. The diff was reported as review required, not automatically accepted.
- Rehearsal skipped password display, five browser stages and human review explicitly. No browser acceptance is claimed.
- Error-stop verification used an isolated copy of the runner with a first-operation Oracle error (ORA-20991); it displayed the error, returned failure and did not enter later operations. Deployed sources and application data were unchanged.
- Evidence: [guided rehearsal](tests/guided_operator_rehearsal_20261016.log).
- bash -n, local link/anchor checks and git diff --check passed.


## Developer outcome view

- Added a separate A/B/C outcome manual/runner; existing walkthroughs and their scripts are unchanged by this addition.
- Preflight and Bash syntax passed.
- Real Oracle checks passed for A's identity, application/component inventory, Foundation-only assertions and control-reservation inspection.
- PTY flow reached separate runtime and App Builder URL pauses, then stopped at B with the documented PENDING/status 3. Test keypresses verified control flow; no new Product Owner/browser acceptance is claimed.
- Rehearsal reached the same pending boundary while explicitly skipping human inspection.
- The current application inventory reports saved display name 1, version 1.0.0 and Unavailable; the new outcome guide selects application 810001 by ID and does not overwrite that live edit.
- Evidence: [developer outcome rehearsal](tests/developer_walkthrough_rehearsal_20261016.log).
- B/C authoring and release operations are not implemented or tested by this runner.


## Runtime-only outcome checkpoint

- Rehearsal passed the existing Foundation/control checks and displayed only the application runtime URL, then stopped at the expected PENDING/status 3 boundary.
- Confirmed no App Builder URL or page-definition inspection prompt remains in the new runner.
- Human browser viewing was skipped; positive deployments and negative deployment protections remain unimplemented.
- Evidence: [runtime-result rehearsal](tests/developer_results_rehearsal_20261016.log).


## Foundation completion checkpoint

- SQLcl/Liquibase validate and update passed migration 002 on A; LAB_RUNTIME and both history guards compiled without USER_ERRORS.
- Native App Builder export includes Home's submit/process and page 10 history report. Repeated unchanged export and fresh reserved capture match the accepted tree byte-for-byte.
- Initial E1_QUALIFY reconstruction applied migrations 001/002 and imported mapped application 810004 successfully via APEX_APPLICATION_INSTALL. Foundation-only assertions and blocked native runtime remain valid.
- IT-4 Foundation-only function passed on A, including actual HTTP assembly-blocked message.
- A's initial reservation was released; a separate capture reservation acquired/exported/released successfully.
- Full greeting/history behavior is not yet exercised; Hello/World are absent.


## Hello intermediate-source verification

- Native Foundation reconstruction in B and immutable migration 003 passed; USER_ERRORS is empty.
- Hello assembly checks passed: Foundation/Hello 1.0.0, World absent, no seeded entries, incomplete runtime rejects mutation.
- Repeated B exports are byte-identical. [Scope review](tests/hello_source_review.txt) identifies generated identity metadata and preserves Foundation behavior; the final form source contains active-entry lookup and disabled configuration creation/deletion.
- Hello task generation 3 was released after verification. Combined runtime behavior remains pending C.


## World contribution and combined database

- C reconstructed accepted Foundation/Hello f511ab8 and passed inherited Hello assembly checks before migration 004.
- World migration 004 compiled cleanly; all components report 1.0.0 while root remains maintenance.
- Registered unit suite passed 2 tests, 0 failures, on real Oracle with rolled-back fixtures.
- [World source review](tests/world_source_review.txt) passed repeated byte-identical export, original-ID preservation, untouched Hello/Foundation behavior and final form controls.
- World generation 4 released. Complete browser result/publication remains pending shared-composition verification.


## Complete development increment — 2026-10-17

- UT-1/UT-2: real Oracle composition/history assertions pass (2 tests, 0 failures); fixture changes roll back. CLI SQL-file execution now preserves native nested include resolution.
- Platform smoke: 1 test, 0 failures. Foundation IT-4 regression passes against preserved A, including blocked HTTP runtime.
- C complete/published development checks pass: zero compile errors, three 1.0.0 components, thirteen required pages, application ready and native available status.
- Browser: VERIFIER greeting/default/history flow passes; ordinary LAB_USER is blocked while restricted, then creates a greeting after publication. Re-login and refresh show both saved history rows. Installed components shows Foundation/Hello/World 1.0.0.
- Repeated complete native captures are byte-identical. Scoped source review accounts for shared composition, read-only versions and native default report layouts; no source deletion or manual rewrite of Oracle output.
- Results runner preflight passes. Unattended rehearsal checks A/B/C successfully and deliberately exits 3 at pending qualification; human URL viewing is skipped and is not an automated browser result.
- Full integration/release suite remains incomplete. No exact-artifact promotion, patch, drift/incompatibility deployment rejection, concurrency or additive-failure repair acceptance is claimed.

## Walkthrough portability and repeatability — 2026-10-17

- [Verification record](tests/walkthrough_repeatability.txt): two unattended A/B/C rehearsals reach the same exit-3 unfinished release boundary after successful preparation/results checks.
- An active Hello task produces the specific ORA-20701 refusal before cleanup writes. The test reservation is released afterward.
- Configuration restore SQL executes in C. A further cleanup leaves Hello/World entry counts at 1/2 and preserves all fields of the seven existing history rows. No duplicate demo entries or history deletion occurs.
- Git-root discovery/preflight passes from a repository subdirectory and invocation outside the checkout. SQLcl receives the discovered root. Shell/Python syntax, unit tests (2/0), smoke (1/0), local links and whitespace checks pass.
- Browser pauses are skipped during rehearsal. Qualification, TEST promotion, patch and deployment-rejection scenarios remain pending; cleanup does not provide that acceptance.

## Initial release preparation checks — 2026-10-17

- [Archive checks](tests/initial_artifact_checks.txt): clean Git fixture build/unpack preserves raw source; dirty source, overwrite, altered bytes and path traversal reject. No Oracle qualification is implied.
- [Control checks](tests/initial_control_checks.txt): package compiles; missing qualification, stale expected epoch and stale ownership token reject specifically. Both controlled targets remain at initial epoch zero.
- [Source review](tests/initial_release_source_review.txt): repeated captures match; only controlled unavailable status and the native versions-report layout differ from the reviewed development source.
- Fresh Oracle qualification, publication atomicity, ordinary/verifier browser checks and identical-byte TEST promotion are the next pending IT-1 initial-install experiment. Broader IT-1 repeat/upgrade acceptance remains pending.
