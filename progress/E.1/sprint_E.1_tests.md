# E.1 — Construction test results

The [repository and pipeline draft](repo_layout.md) uses these results to separate demonstrated pipeline paths from intended capabilities. Update both descriptions when the evidence changes.

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

## Initial identical-artifact delivery — 2026-10-18

- Qualified and promoted source **0f7c500e064e4f262a42fb74f4984eb0e4349c88**, archive SHA-256 **6a1da4a940586541cbb034277605d7ed36e5d1ad305554f9a2fe4c64cd59411c**. Qualification application **810004**, epoch **2**, and retained TEST **810005**, epoch **1**, are published **ready** with Foundation/Hello/World **1.0.0**.
- Actual archive-driven stages passed on both targets: atomic initial admission, four migrations, unchanged native split import, composition/history unit assertions, thirteen-page/version/compile integrity checks, VERIFIER browser verification and guarded publication. Ordinary LAB_USER subsequently created greetings and reopened history in both. TEST Installed components displays all three 1.0.0 versions.
- A prepared native AVAILABLE application remained externally gated until publication. Rolling back the final publication reverted successful receipt and external readiness together; the attempt remained verifying. The ordinary login error during that interruption was generic; it is not presented as a specific incompatible-deployment rejection. Server gate assertions and subsequent successful login with the same credentials support the gate result.
- Repeated qualification/promotion commands verify existing matching results without migrations/imports. The registered initial-only integration subcase passed: matching Q/TEST successful receipts, live APEX fingerprints, repeatable post-publication fixture, and exact equality of every retained history/configuration field before/after. TEST contains twenty VERIFIER snapshots plus one ordinary-user snapshot. Existing isolation probe data was retained.
- Results walkthrough preflight passes; unattended A/B/C/Q/TEST rehearsal reaches the deliberate remaining-scenarios boundary with **exit 3**. Browser checkpoints are skipped in rehearsal; separate real browser checks above passed. Unit suite **2 tests / 0 failures**; platform smoke **1 / 0**.
- [Initial delivery evidence](tests/initial_delivery_result.txt), [ordinary TEST greeting](tests/test-ready-greeting.jpg), [retained history](tests/test-ready-history.jpg) and [installed versions](tests/test-versions.jpg).
- Pending: compatible Hello 1.0.1 upgrade, pre-write incompatible Foundation-major rejection, controlled drift scenario, full upgrade maintenance/drain, concurrency and additive-failure automated repair. The full IT-1 upgrade/reconstruction and IT-2 patch entries remain pending; the bounded initial subcase does not complete them. No sprint closure or second-operator reproduction is claimed.

## Hello 1.0.1 and selected deployment protection — 2026-10-18

- Patch source **752eb47ec59daeb625c3849bfed87fc230295e20**, archive SHA-256 **200ebefff13e87600699adfebbbe71158962dc80a02d1b8e6dbd9a829dd9e1ce**. Fresh qualification epoch **3**, reconstructed initial baseline **4**, patch-upgrade qualification **5**, retained TEST upgrade **2**. The archive was built once and used unchanged for both patch qualifications and TEST.
- Hello advances **1.0.0 → 1.0.1**; Foundation/World stay **1.0.0**. Application version is **1.0.1**. Migration 005 adds a validation constraint and corrects surrounding POSIX whitespace/blank handling; migrations 001–004 remain byte-identical. No existing business row/configuration is rewritten by the patch.
- Candidate validation in C passed before local fast-forward integration/build. Two unchanged native source captures match; the release source diff is version plus generated SCN. Raw Oracle files were copied unchanged. The separately authored drift fixture changes only Home title/header plus generated SCN and is outside release contents.
- Actual fresh and upgrade native stages passed: preflight/admission, Liquibase validation/update/status, native import, units/integrity, VERIFIER browser greeting/history and guarded publication. An existing ordinary TEST session was blocked before DDL. Its generic APEX session-setup error demonstrates blocking only, not a specific deployment rejection.
- Field comparisons preserve all fields of **21 earlier snapshots**, entries and full configuration in each upgrade baseline. Qualification preserves explicit **[Q] / [W]** prefixes; a post-upgrade browser greeting uses them while old Hello World snapshots remain. TEST ordinary/verifier greetings work after publication. Its final refreshed history shows **25** rows, including the original snapshots and explicitly appended verification greetings.
- Holding the ordinary mutation guard in another transaction causes patch admission to reject with resource-busy before maintenance. Qualification remains ready at epoch 4 with its baseline receipt/data unchanged. After rollback releases the guard, admission succeeds at epoch 5. This does not prove full read/asynchronous request draining or generic deployment races.
- The incompatible Foundation **2.0.0** proposal rejects specifically: **Hello requires Foundation 1.0.0; proposed Foundation 2.0.0**. Actual target definitions, versions, entries, settings, history and control receipts match before/after. No maintenance/migration/import is entered.
- The controlled Home title/banner change keeps component versions unchanged but changes the live APEX fingerprint. Redeployment preflight rejects **DRIFT** before maintenance/migrations/import and retains the changed page/data. The ordinary browser still creates a greeting afterward. Separate restoration imports the saved original native target definition with the same ID offset and requires the original fingerprint; it preserves even the greeting appended during the demonstration. Manual, registered-test and walkthrough repetitions restore successfully.
- SQL boundary regression: CSV diagnostic text containing an Oracle error code is readable; an actual raised Oracle exception fails and cannot reach completion. Error detection now recognizes real diagnostic lines, with nonzero exit/missing completion checks retained. This avoids misclassifying retained failure-reason fields as new failures.
- Registered selected integration: **3 tests / 0 failures** (IT-2, SM-2, focused IT-7); unit regression **2 / 0**; platform smoke **1 / 0**. Separate preparation passes without changing prior history. The complete selected A–H CLI rehearsal passes with **exit 0**, explicitly skipping human viewing. Real browser checks are separate evidence above.
- [Detailed result](tests/patch_delivery_result.txt), [installed versions](tests/patch-test-versions.jpg), [preserved custom settings](tests/patch-preserved-settings.jpg), [visible drift](tests/drift-visible.jpg), [working app after rejection](tests/drift-rejected-working.jpg), [restored greeting](tests/patch-restored-greeting.jpg), [retained history](tests/patch-restored-history.jpg).
- Full IT-1 candidate reconstruction, comprehensive schema drift, parallel work/deployment races, complete request/verifier fencing and automated failed-additive-deployment repair remain unproved. Full integration/sprint completion is not claimed. These essential remaining questions justify further Elaboration before a Construction-readiness decision; no other sprint is changed or activated.

## Split walkthrough verification — 2026-10-18

- [Execution summary](tests/walkthrough_split_20261018.txt): launcher/local A–H preflight and renamed detailed-operator preflight exit 0; independent E rehearsal exit 0; full A–H rehearsal exit 0.
- Real compatibility and drift preflight checks reject for their specific reasons and compare target/control state unchanged. H explicitly restores the original native definition/fingerprint/settings/history. Existing 21-row preservation checks pass. Human runtime viewing is skipped in rehearsal.
- Bash syntax passes for all 12 related scripts. Launcher/A/H reject invalid or excess arguments with 2 and discover the Git root from a subdirectory and outside the checkout. Interactive q at A's first checkpoint exits 130 before Oracle checks or later stages.
- Detailed operator behavior is preserved byte-for-byte apart from its renamed usage command; authoritative release/patch controllers remain unchanged. No application-code change requires repeating unit/full integration. Broader E.1 proofs remain open.

## Fresh-start lifecycle and A–H reconstruction — 2026-10-18

[Scoped execution evidence](tests/fresh_walkthrough_20261018.txt) records successful precheck, host preparation, named-resource destruction and fresh database/APEX/ORDS installation. Before A, administrator verification found applications 810001–810005 and business/history tables absent. All five identities and real cross-area read/write denial checks passed. Source archives and credentials were retained; no prior business history was restored.

Complete `bash scripts/cicd-walkthrough.sh --rehearse` returned 0 with actual A/B/C installations, new D/E qualification/promotion receipts, F's fresh/baseline-upgrade patch qualification and TEST upgrade, G's specific incompatibility rejection and H's drift/rejection/original-definition restoration. This cycle preserved all fields of 21 qualification and 20 TEST snapshots. Final rehearsal counts were C 1, qualification 22 and TEST 21, all created on 2026-10-18. Qualification epoch 4 and TEST epoch 2 published the unchanged patch archive. Human browser viewing was skipped; runtime API examples are explicitly test data.

Registered lifecycle unit check passed (1/0, four policy cases); existing greeting/history unit regression passed (2/0), platform smoke (1/0), and lifecycle-manifest IT-2 result/field-preservation regression (1/0). Bash/Python syntax, chapter invocation mapping, portable Git-root discovery and invalid argument checks pass. Existing-lab installation refusal and populated-area empty-check rejection pass before writes. No full integration or sprint completion is claimed; concurrent clients, complete request/verifier fencing, broader schema drift and failed-additive repair remain open.

After recording the successful complete rehearsal, repeated the explicit scoped cleanup/fresh installation and left the lab initialized with no applications or business/history tables. Final precheck reports APEX 24.2.0 VALID; administrator checks find no old control events/attempts and fresh release targets at epoch zero. An interactive q at A's first checkpoint returns 130 before any database mutation. The unrelated default VM remains present/stopped. This is the delivered checkpoint for the Product Owner's own A–H run.

## Infrastructure/onboarding responsibility checks — 2026-10-18

The separate fresh-infrastructure boundary assertion passed: zero E.1 schemas/workspaces after database/APEX/ORDS installation, with APEX/ORDS HTTP checks passing. Control initialization compiled without area schemas present. After provisioning only A, native dictionary assertions found only E1_CTRL/E1_DEV_A and workspace A. Three real developer configurations passed using their own schema passwords and private SQLcl homes. All five areas were subsequently provisioned by five named invocations. See [the complete result and limits](tests/onboarding_boundaries_20261018.txt). Local lifecycle policy tests pass, 2 registered tests/0 failures, including five onboarding cases and four cleanup cases; mocks verify command responsibility boundaries only.

## C restricted-verification continuation — 2026-10-18

The [real PTY continuation check](tests/c_resume_verification_20261018.txt) passes ownership/state/assembly inspection and reaches VERIFIER's browser pause. Explicit q returns 130; C remains restricted with no new greeting/publication. Fresh/default and resume local preflight plus Bash syntax pass. This does not rerun C installation, accept browser verification or prove general failed-deployment recovery.

## C missing-snapshot retry — 2026-10-18

[Retry evidence](tests/c_verification_retry_20261018.txt): focused control-flow unit suite passes 3/0. Native read-only loop retries an explicitly forced missing-row fixture, then accepts the actual current Hello World snapshot. Browser pause is stubbed; no publication or data write occurs. A separate read-only missing-row assertion confirms the clearer ORA-20803 text. C development verification/publication is distinct from D archive qualification and E same-archive TEST promotion.

## Renamed integration/UAT identities — 2026-10-18

[Rename verification](tests/environment_rename_20261018.txt): native new-schema/workspace mappings and control-package compilation pass; new initial archive/controller status reaches E1_INTEGRATION. An actual UAT admission attempt rejects ORA-20614 for missing qualification, retaining epoch zero with no UAT attempt or migration/import. Original D attempt remains as a failed historical row; A/B/C applications remain. Local lifecycle policy suite passes 3/0 (eleven subcases), plus C verification-loop 3/0. Initial candidate composition/history passes 2/0, fixtures rolled back. New patch candidate explicitly reuses prior byte-identical APEX/db functional evidence; this is not new patch runtime qualification. No new D/F/UAT or browser acceptance is claimed.

## Integration_test operator naming checks — 2026-10-18

D_integration_test, E and the detailed operator runner pass local preflight. All Bash/Python syntax checks pass. Walkthrough lifecycle tests pass 3/0 (eleven underlying cases); C verification-loop tests pass 3/0. Documentation checks pass for 34 documents and 375 links/anchors, fences, traceability and whitespace. Current scripts/tests have no references to the removed D runner, wrapper or fixture filenames. Pinned initial/patch controllers remain byte-identical to HEAD.

Read-only command: bash scripts/cicd-release-result.sh "$(cat .local-apex/releases/initial-selected.txt)" integration_test. Exit 0; complete 1.0.0, ready state, archive SHA256 d99fe83ec3d149739a12ec0cf2f01081ae027d1ec015e16d5a971ff3c602ab45 and live APEX fingerprint match. This verifies the already completed D result; it does not repeat deployment or claim UAT acceptance.
