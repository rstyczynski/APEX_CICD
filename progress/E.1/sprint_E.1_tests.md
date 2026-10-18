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

## Release verification retry and E resume — 2026-10-18

Verification manifest passes 8/0: existing C three cases; release missing-then-present, q, unexpected SQL failure; initial resume refuses published state and wrong archive. Local fresh/resume preflights and Bash syntax pass. Native E resume validates actual E1_UAT epoch 1, selected initial hash, restricted 1.0.0/root state and archived integrity plus UT-1/UT-2 (rollback fixtures). Pressing a key with no greeting reports the missing VERIFIER Hello World assertion and repeats the browser prompt. q exits 130 without publication. No new deployment attempt, migration/import/reset or greeting fixture is performed. Full successful E browser/publication remains pending.

## UAT examples with unset default — 2026-10-18

Native diagnosis: E1_UAT epoch 1/ready, complete initial archive, matching live fingerprint; one VERIFIER and one LAB_USER Hello World greeting. Hello default exists; World default is unset. This is a fixture assumption failure after successful delivery.

Corrected fixture executed natively with its insert commit replaced by rollback for this test. Explicit active selections produced the expected examples; history count and Hello/World defaults matched before/after, including the unset World default. No test examples retained. E --resume-examples natively validated ready state/archive/fingerprint and both successful receipts, reached the LAB_USER pause, then q exited 130 without preparing/capturing data. Fresh/resume local preflight and Bash syntax pass. Verification manifest passes 11/0, adding existing-baseline reuse, capture-after-success and no capture on fixture failure. Full completion of E's baseline preparation remains pending operator continuation.

## Drift outcome classification — 2026-10-18

Command: bash tests/run.sh --unit --new-only tests/manifests/protection_outcomes.manifest. Result 7/0: clean, specific drift, unexpected Oracle failure, silent failure, expected drift absent, baseline unexpectedly drifted and specific compatibility rejection. The tests invoke the production classification function with captured controller output; no Oracle/browser calls are mocked as live proof.

Native bash scripts/cicd-protection-check.sh drift exits 0 on current UAT. Patch integrity passes; output includes ALREADY DELIVERED, NO DRIFT and PASS drift protection. Before/after target/control snapshots match; archive and fingerprint remain the published patch. Protected evidence directory .local-apex/releases/protection-drift.rEEyEW. Manual editing and synthetic injection were not rerun for this increment; the existing fixture path is retained, now with explicit expected-outcome assertions. Local H preflight, Bash syntax and document checks pass.

## Native manual drift source review — 2026-10-18

Command: python3 scripts/cicd-drift-diff.py. Native exit 0, read-only final review saved under .local-apex/releases/drift-review.i0tu14iw (review.diff, raw.diff, review.json, published/live source trees and capture log). The exact successful patch archive/source/configuration matched the receipt; receipt and live fingerprint stayed unchanged across capture. Home page Title changed from APEX Delivery Laboratory to Manual drift demonstration; region Name changed from APEX Delivery Laboratory to APEX Delivery XX Laboratory. Additional SQL/export differences are retained for review. No restoration, import, source commit or runtime-data change was executed by the review tool.

Command: bash tests/run.sh --unit --new-only tests/manifests/drift_review.manifest. One wrapper passes, five underlying Python cases pass: bounded normalization/full raw retention, additions/deletions, escaped region name, unrelated source/archive receipt rejection and unchanged source. Python syntax and document links/anchors/fences/whitespace pass. The operator's restoration decision and subsequent original-fingerprint check remain pending; no rollback acceptance is claimed.

## Native drift --show entry point — 2026-10-18

Command: bash scripts/cicd-protection-check.sh drift --show. Native exit 0 on current manual UAT drift: specific rejection, source comparison, unchanged snapshots and PASS drift protection. Protection evidence .local-apex/releases/protection-drift.hoGb6P; source review .local-apex/releases/drift-review.xmnxjlwm. Live edit and published receipt remain intact; no restoration/import occurs.

Protection-outcome manifest passes 10/0, adding valid --show/expected-flag combinations and rejection of compatibility/duplicate/conflicting options. H local preflight, Bash syntax and document checks pass. The existing five source-diff tests remain applicable; comparison logic is unchanged. Clean --show's no-difference message follows the existing clean classification; a new native clean run is not claimed while the user's edit remains active.

## Handover preparation checks — 2026-10-18

[Exact checks and applicability](tests/handover_checks_20261018.txt): local A–H preflight passes; protection outcome manifest passes 10/0; drift-review wrapper passes 1/0 with five Python cases. Native drift --show returns the specific rejection and unchanged snapshots; live Home Title/region Name edits remain visible. Native preservation comparison confirms all fields of 21 prior history rows, old entries and complete configuration unchanged. Logs are retained beside the check record. No new fresh end-to-end replay, synthetic injection or restoration is claimed.

All 23 final slide PNGs were individually inspected. Package integrity, geometry/font checks and first-party reimport pass with zero findings/warnings. The [portable receipt](tests/handover_presentation_validation_20261018.json) identifies the delivered PPTX SHA and native table. Microsoft PowerPoint itself was not opened. Document links/anchors/fences, current traceability symlinks, source/slide-map consistency, staged credential/scope and whitespace checks complete the documentation audit. Broader sprint gates remain incomplete as stated in the [assessment](sprint_E.1_assessment.md).

## Presentation APEX interface clarification — 2026-10-18

Checked slide content against deploy/operator/capture.sql, import.sql, fingerprint.sql and current architecture. The revised 24-slide deck is rendered and finalized; package/layout/font and first-party reimport checks identify the current SHA in the portable receipt. The added slide and shifted table are visually inspected; other slide content is retained. Document links/anchors/fences and staged scope/credential/whitespace checks pass. No runtime tests or deployments are needed for this presentation-only explanation.

## Git presentation section — 2026-10-18

Checked actual source directories, current manifest/capture profile and the existing developer-integration contract. Oracle APEX 24.2 split-export documentation supports granular source-control review and identifies shared install/application files affected by page additions. Git text-merge capability is distinguished from application semantic validation; no actual parallel APEX merge is claimed. New slides and the shifted native version table are rendered/visually reviewed; package/layout/font/reimport checks and synchronized local links/slide references pass. Current receipt identifies the delivered revision. No runtime tests/deployments are performed for this explanatory increment.

## External review response verification — 2026-10-18

[Review answers](sprint_E.1_review-1-response.md) map each finding to actual source and bounded acceptance evidence. Focused drift-review manifest passes 1/0 with five underlying Python tests; protection outcomes pass 10/0. Native SQLPlus probe raises ORA-20224 in an anonymous block: EXIT SQL.SQLCODE returns 0, EXIT FAILURE returns 1. Both probes contain no DDL/DML and request rollback. Confirmed both historical assembly commits exist, no archive tar files are tracked and no GitHub workflows are tracked. No new migration failure/repair, replacement import, independent clone replay or saved-report preservation test is claimed. No runtime fix is made.

## Review fixes increment 1 — 2026-10-18

[Captured results](tests/review_fixes_20261018.txt): review_fixes manifest passes 1 wrapper/8 Python cases; Python discovery passes 24/0. Cases cover isolated-history archive reconstruction without retained releases, tamper/missing-source/conflicting-byte rejection, malformed config before Oracle/secret access and dirty runner/manifest/Python/shell source rejection. Native SQLPlus ORA-20224 returns 1 under EXIT FAILURE. All five native area identities and their cross-area read/write denial checks pass. Local A–H preflight, Bash/Python syntax and document checks pass. This is not an independently provisioned fresh A–H/browser replay or full unfinished integration-suite acceptance.

## BUG-6 native identity test — 2026-10-18

[Native evidence](tests/apex_identity_20261018.txt) from explicit C upgrade: wrong target ORA-20645, immutable 005 applied once then no-op on repeat, two imports with identical region IDs/private saved report fields and unchanged history/configuration. Used public APEX_SESSION/IR/EXPORT/INSTALL APIs only. Tests/manifests/apex_identity.manifest exposes the same test as an explicit integration operation. No UAT change or general saved-report/subscription coverage is claimed. Corrected artifact preparation remains outstanding.

## Corrected patch and repair-protocol preparation — 2026-10-18

Corrected patch archive SHA-256 80b51f1ed3e371d6c198dc785a7df741fd671d2ab77d8db630f7dd63bd92d583 from 0cc6c68 passes candidate development checks and both fresh/initial-upgrade integration starts with preserved 21-row baseline/settings. Full private transcript: .local-apex/qualify-corrected-patch.log; this unattended check uses explicit runtime API fixtures, not a new browser demonstration. Retained UAT is unchanged. All Python source tests pass 25/0 including Git-bound recovery artifact/tamper/unsupported-target tests. New recovery authority/observer compile with zero errors. BUG-7 native failure/repair proof remains pending, explicitly not passed by artifact/unit checks.

## BUG-7 native integration proof — 2026-10-18

[Transcript](tests/recovery_proof_20261018.txt): failed-additive artifact 713133175024c2330f40779d746a55aca3ac0ab36db6adb0ad8e6a6741453504, repair artifact 78efc057e092a79440d787846121daf6d55450b29043e0634b20b87656d51ca2, source e7ee3de. ORA-20831 is expected after BUG7-001 commits; BUG7-002 is not marked run. Ordinary runtime rejects. An additional synthetic index changes the inspected observation; controller and server ORA-20846 both reject before repair. Only that controlled negative fixture is then removed. Repair reuses 001, adds 003, retains the failed receipt and prior 21-row fields/settings, publishes a separate successful receipt and repeats with ALREADY REPAIRED/no writes. UAT untouched. Wider stale-worker/session and arbitrary partial-state coverage is not claimed.
