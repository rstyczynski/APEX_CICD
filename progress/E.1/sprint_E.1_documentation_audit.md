# E.1 — Documentation audit

## Setup and proposed design — 2026-10-16

Reviewed the accepted SRS, candidate architecture, test profile, README, assigned PBI-011–016 and final I.1 decisions against E.1's requested proofs. The setup/design preserve one application per target, the three components, private single-host areas, supported Oracle interfaces, exact-byte qualification and observed-state repair. Eight child definitions include parent, bounded outcome, dependencies, acceptance cases and estimates. PBI-012–016 remain separate evidence/refinement/decision outcomes. Other sprint artifacts are unchanged.

Read-only environment checks establish Podman 6.0.0, the owned four-CPU/6-GiB VM and running DB/ORDS containers, 48 GiB host RAM/twelve logical CPUs and approximately 13 GiB free host disk. No runtime mutation, tool installation or credential operation was performed. Existing scripts/.gitignore remain untracked; review/adoption belongs to child 1. Oracle reference pages for installation, export checksums, restricted availability and Liquibase were checked; local compatibility remains untested.

Updated the shared deployment procedure for E.1 ownership and the authorized reuse/reconstruction of the current environment. Removed the teardown step that deleted the host .local-apex directory so credentials, installers and evidence survive VM removal. Reconstruction will be executed after approval, before retained prototype history is established. The initial disk observation is not a fixed limit; measure again when executing. User preferences now state concise records and current-sprint-only work.

The selected design is accepted and construction/functional-test records now track the actual work. The design states proposed interfaces and unrun cases explicitly. Local P8 defers executable skeletons until approval and completion commits until an audited increment is complete. This is a proposal audit, not a PBI completion or runtime pass. No push is authorized.

Validation: python3 /private/tmp/apex-rup-document-check.py passed for 28 documents and 150 local links/anchors, Markdown fences, traceability targets, assigned-PBI existence and exactly one active sprint. A separate Python assertion check passed for eight sequential children with parent/dependency/evidence/estimate, fourteen E.1 board rows and the testing strategy/specification. Compared previous PLAN sections, board rows and prior sprint directories with HEAD: unchanged. git diff --check passed. No runtime tests or executable skeletons were run. The selected scope is approved; completed implementation increments are audited and committed together.


## Platform increment — PBI-011.1

The selected platform scope is complete: private checksum-pinned tools, adopted lifecycle sources, owned-area inventory, dedicated named connections, five isolated private/qualification/TEST areas and separate control-schema bootstrap. Inspected effective identities, ordinary grants, public provisioning API calls and saved-connection/secret handling. The platform smoke and isolation/reset integration subset passed with actual logs in the test record. A retained TEST marker survives disposable-area recreation. The SQLcl script-file/completion-marker fix is included with its preservation/error-propagation evidence. Fresh VM reconstruction was not needed for this selected slice and is not claimed as executed.

Reconciled shared SRS/architecture/test-profile expectations with the selected design, setup, current construction/test records, README, deployment procedure and board. The accepted command contract remains future work for release build/qualification/promotion; no complete pipeline or application pass is claimed. Supporting lifecycle scripts were syntax checked and reviewed, not all rerun. Shared approved design/test skeletons and scaffolding are included with the first increment that depends on them; they do not complete later children. Other sprint directories, earlier PLAN sections and earlier board rows remain unchanged.

Commit scope is platform code/configuration/tests, adopted lifecycle sources/ignore rules, active-sprint documents and shared E.1 orientation/activation changes. Foundation/application/ownership work remains under construction and is excluded from this completion commit where separable. No credentials, local tool binaries, session files or unrelated untracked files are staged. No push is authorized.

Pre-commit checks passed: 31 Markdown documents/157 local links and anchors; shell syntax for the runner, tool bootstrap and eight lifecycle scripts; Python compilation; Git ignore coverage for secrets/tools/history; git diff --check. B1 smoke regression passed. The prior sprint directory diff is empty. Full application unit/integration gates remain pending and are not hidden by this platform checkpoint.


## Operator procedure refinement — in-progress construction

The operator guide is now the primary procedure for the constructed stages: native SQLcl target and ownership inspection, changelog validation/status, separate migration application, APEX export, and source diff inspection. Workspace/app endpoints, actual deployed versus reserved application IDs, usernames and protected local password retrieval are explicit. Python isolation helpers remain supporting checks with visible atomic SQL. The implementation record tracks the same state; no release, qualification or full-suite success is claimed.

Executed the native identity/ownership, Liquibase validation/status, component/Foundation inventory and migration-receipt sequence successfully after correcting SQLcl's script-directory resolution with an explicit cd. Exported live application 810001 to a separate staging directory and reviewed its two-field version/SCN diff. A wrong target was rejected with ORA-20010. Initial Foundation migration application is earlier construction evidence; this refinement did not redeploy or reset the database. Application import, controlled capture reconciliation and release operations remain unfinished, so this is an in-progress review rather than a completed Foundation increment or sprint gate.

Documentation validation passed for 32 documents, 171 local links/anchors, Markdown fences, traceability targets, assigned PBIs and the single active sprint. bash -n scripts/cicd-env.sh and git diff --check passed. No other sprint artifact was edited. The current construction changes remain uncommitted until the coherent increment's remaining verification is complete.


## Podman-to-APEX operating procedure refinement

Expanded docs/deploy.md into individually inspectable operator stages: resource inventory, local helper, VM creation/start, guarded credential generation, pinned installer/images, network/volumes/secret, database, APEX installation/configuration, ORDS installation/settings/serve, access checks, logical-area boundary, ordered stop/start, repair and scoped reconstruction. Compared commands with the adopted shell/SQL sources. Corrected README's current lifecycle owner to E.1. Retained-data loss on VM deletion and the missing validated backup/restore path are explicit. Logical-area operator provisioning remains pending; no application seed or complete release workflow is claimed.

Reconciled the procedure with SRS/architecture preservation and isolation requirements, the test profile's platform boundary, E.1 setup/design/test/implementation records, README and the current board. This refines the already delivered PBI-011.1 platform documentation; it does not close other construction children. No other sprint artifact or status changed.

Actual checks passed: current Podman inventory, both pinned ARM64 image digests, krunkit 1.3.2, database healthcheck and apex-verify.sh (APEX 24.2 VALID, zero invalid objects, SYSTEM/FREEPDB1 host-port authentication, ORDS/login HTTP 200 and matching assets). Syntax checked all 36 Bash blocks without executing provisioning, shutdown, repair or destructive operations. Document checker passed 32 documents and 181 local links/anchors; git diff --check passed. Fresh full reconstruction and retained-data restoration remain unvalidated. Changes stay with the current construction increment for its completion commit; no push.


## App Builder instruction detail

Replaced the vague manual step 4 with exact login, application and control names, expected page definitions, version value, saving semantics, maintenance message and the next operator step. Browser inspection confirmed Workspace/Username/Password/Sign In labels and the live Foundation-only unavailable message. Page properties/login item names match the Oracle export; Version/Apply Changes follows the earlier executed authoring step. No new authoring operation or authenticated Builder rehearsal is claimed for this documentation refinement.


## Operator-document formatting

Applied numbered steps and bullet points throughout user_manual.md and docs/deploy.md, including all App Builder subchapters. Checked list indentation, command fences and step references. Shell syntax passed for 55 Bash examples without executing runtime operations. Local document validation passed for 32 documents and 181 links/anchors; git diff --check passed. Scope is documentation readability only.


## Guided manual/script pair

Implemented the requested guided execution for the current operator journey; the script reads chapter text from user_manual.md and shows native SQLcl commands/output with a keypress before execution. Browser stages display URLs and wait for human inspection; later stages remain pending. Both the manual and deployment guide require paired updates as one artifact and preserve numbered/bulleted instructions. README and construction/test records describe the same scope. No pipeline completion or deployment was inferred from a successful runner invocation.

Preflight, live pause/quit and noninteractive rejection checks passed. Rehearsal passed 15 SQLcl operations, staged export and diff review reporting, with browser/password/human steps explicitly skipped. An isolated real-Oracle failure fixture proved visible error/stop behavior. Reviewed command equivalence against manual chapters 1–8, error handling, secret display and staging-only effects. Reconciled SRS/architecture/test-profile expectations with the existing E.1 scope; no managed status or other sprint artifact changed. Script syntax, local document links/anchors and git diff --check passed. Construction remains in progress; this pair belongs with its supporting implementation in the next completed increment commit. No push.


## Separate developer outcome walkthrough

Added developer_walkthrough.md and cicd-developer-walkthrough.sh without changing the existing operator manual, operator runner or deployment guide. README links the new artifact. The A/B/C and integrated-release chapter sequence follows the accepted design. Runtime checkpoints preserve maintenance for incomplete assemblies; the current executable inspects A and explicitly stops before pending B/C work. It does not pretend to author/import/release an unimplemented component. The new manual/runner pair carries its own maintenance rule.

Native A and control inspection, live pause flow, local preflight and unattended rehearsal passed, with the expected PENDING/status 3 at B. Browser human checks remain unverified by these runner tests. Reconciled current app inventory (ID 810001, display name 1) in the new guide without modifying live content or the existing walkthrough. Syntax, 33-document/190-link validation and git diff --check passed. Other sprint artifacts and managed statuses are unchanged; no push.


## Runtime-only outcome checkpoints

Updated only the new outcome manual/runner pair to remove App Builder and technical inspection from Product Owner actions. Runtime result checkpoints now distinguish incomplete-assembly blocking, successful deployment/patch behavior, known-incompatibility rejection and live-drift rejection. Negative scenarios require the specific rejection reason, no precheck mutation and preserved behavior/history; arbitrary pipeline failure cannot pass. These follow the already accepted selected scenarios and remain pending construction. The runner makes no success claim for them. Existing walkthroughs and deployment guide were not changed.


Validation passed: Bash syntax, local preflight, existing Foundation/control rehearsal and expected pending boundary, absence of Builder inspection prompts, local document links/anchors and git diff --check. Rehearsal skips human viewing and does not prove a deployment/rejection.


## Selected use-case traceability

Compared the outcome walkthrough with SRS UC-1–12 and the accepted E.1 happy path, DevOps patch and two selected rejection scenarios. Added explicit UC links/mappings and later/unselected boundaries to the new guide; labelled its runner as the use-case walkthrough. No acceptance scope or status changed. Only Foundation's current check/result is executable; no full use-case success is claimed. Existing walkthroughs are unchanged. Script syntax/preflight, document links/anchors and git diff --check passed.


## Foundation completion increment — PBI-011.3 selected scope

Reviewed immutable migrations 001/002, package compilation/guards, Oracle-generated Home/history source, supported target import mapping and task release. Foundation-only database/runtime assertions passed on A and reconstructed qualification. Two repeated captures and the new fresh-reservation operator capture are byte-identical. The new initial-import helper refuses wrong schema/workspace and existing applications; its successful mapped import was exercised before adding that fail-closed guard, and B's next initial preparation will exercise the final form.

Reconciled current application pages/name, released task and qualification assembly state in the manual, detailed runner and construction/test records. Existing workflow purposes and numbered/bulleted format are preserved. SRS/architecture/test-profile and accepted design retain full application/compatibility/maintenance/release obligations; those remain pending and are not completed by Foundation-only evidence. Broad reservation and cross-private-source tests remain child 2/4 work. Shared control/check/operator/guide code is included with this first completed dependent increment; incomplete cicd-capture.py is excluded. No other sprint artifact or status is changed.

Pre-commit scope is the Foundation source/runtime, supported initial-import source, registered Foundation-only test, current operator/result guides and supporting atomic checks. No credentials/local tools/session data or unrelated files are included. Link/anchor/fence checks, Bash/Python syntax, Foundation IT-4 and capture comparisons passed; platform smoke result follows below. No push.


Platform smoke passed: 1 test, 0 failures. Restored tests/run.sh executable permission so its documented direct entry point works. PBI-011.3 is tested for the approved Foundation-only selection; the sprint, parent and other prototype children remain in progress. Secret-value scan of staged sources passed before commit.

Oracle-generated comment headings and verbatim SQLcl evidence include trailing spaces. Preserve those raw bytes; .gitattributes scopes the end-of-line whitespace exception to Oracle exports and E.1 raw logs. Project-authored sources retain normal whitespace checks.


## Hello source increment — PBI-011.5 in progress

Reviewed B's contribution against Foundation e9a490f. Native private reconstruction, migration 003, compile checks and Hello blocked-assembly assertions passed. The declared diff adds four Hello pages, its LOV, generated navigation/includes and target metadata. Repeated captures match; raw Oracle files remain unchanged. Code-editor validation was fixed through native OK/save and final export verifies the SQL selector. The owned intermediate task is complete/released, while the complete integration child remains in progress.

Updated current B readiness and A's older source-baseline comparison in the existing guide without changing its purpose; the separate result guide retains the pending grouped delivery operation. Construction/test records and board agree. Reviewed SRS/architecture/test-profile and selected-design expectations; no full greeting/release/control success is claimed. Stage this scoped Hello source contribution so C can start from an accepted revision. Source/link/whitespace and staged secret checks apply before local commit; no push.


## World source contribution — PBI-011.5 in progress

Reviewed C's World addition from accepted f511ab8. Supported private reconstruction and migrations 001–004 pass with zero compile errors. UT-1/2 pass on Oracle and roll back fixture data/state. Two C exports match, and scope review verifies new World pages/LOV plus declared generated bookkeeping while preserving Foundation/Hello behavior and original IDs. Native create/delete action settings and active-default query are present in captured source. World reservation is released after scoped verification.

Updated C readiness in both outcome guide/runner and operator reference, preserving their distinct purposes. SRS/architecture/test profile still require complete browser, readiness and release/control proof; this component source contribution does not claim them or complete child 5. Commit the reviewed World baseline before beginning the separately reserved shared composition refinement. Syntax, link, whitespace and staged secret checks passed before local commit; no push.


## Published development composition increment — 2026-10-17

Reviewed against the selected design and SRS configuration/greeting goals: working C development runtime, supported native authoring/capture and separately visible identity/ownership/availability operations. Native restricted access blocks the ordinary account during verification; the publication script requires the recorded browser snapshot. This bounded development gate is not the future release qualification/verifier protocol.

Two unchanged exports match. Source review allows only shared composition/report/navigation/status edits, generated component maps and expected default report layouts materialized by runtime use. Existing Hello/World form definitions and data queries retain their behavior; Oracle exports are copied unchanged. UT-1/2, platform smoke and Foundation regression pass. Source captures contain no business seed; browser fixtures remain only in C.

The separate results script and chapters agree on A/B/C read-only result checks, runtime-only Product Owner checkpoints and the pending qualification boundary. The operator reference now documents exact runtime use and A's pending Hello/World changesets instead of suggesting an unsafe replay against the integrated changelog. README, construction and test records agree on development-only readiness. Existing older sprint artifacts are unchanged. Remaining full replay, release, patch, deployment-protection and recovery gaps remain explicit. Local syntax/link/whitespace and staged credential scans are required before committing; no push.

## Portability and walkthrough preparation correction — 2026-10-17

Reviewed SRS UC-3/6/9, architecture retention/ownership constraints, test profile, sprint setup/design/test specification, implementation/tests, README, operator/results guides and current board. No acceptance or sprint transition changes: archive qualification, promotion, patch and deployment rejection remain unimplemented. Preserved the existing detailed operator workflow and the current results-guide introduction.

Removed developer-home checkout literals from maintained shared/E.1 instructions and replaced script-root positioning with Git discovery. Historical raw logs remain historical evidence rather than runnable instructions. SQLcl root substitution is initialized from the shell's Git-discovered directory. Recorded the explicit portability preference locally.

Cleanup and chapters form one artifact: exact operations, scope, private restore SQL, preserved targets/history and clear stop conditions match. The runner invokes cleanup before A/B/C, exposes SQL results, and distinguishes a completed implemented walkthrough from the exit-3 unfinished release boundary. Local preflight, subdirectory invocation, SQLcl root initialization, shell/Python syntax, actual repeated preparation/walkthrough checks, restoration SQL and retained-history comparisons are the relevant verification. No infrastructure teardown or older sprint edits are included. Stage this correction separately from unfinished release-control work; do not push.


## Explicit cleanup step — 2026-10-17

The results guide now lists cleanup as numbered run step 2, its PASS/backup check as step 3, and starting the walkthrough as step 4. Removed the automatic cleanup call from the results runner so following the documented sequence performs cleanup once. Reconciled the operator guide and README. Cleanup behavior and preservation scope are unchanged; no release or sprint status change. Verified shell syntax, chapter/preflight mapping, local links and whitespace.


## Toolchain explanation in the results guide — 2026-10-17

Added Applied tools and techniques immediately after Deep dive. Explained Podman/logical areas, Oracle/PLSQL, APEX/ORDS, SQLcl/Java, Liquibase, Git and small operator/test helpers; source capture/review, Foundation-first assembly, versions versus archive/live fingerprints, fail-stop checks and retained-history evidence. Reconciled statements against the SRS, architecture, test profile, accepted design and actual development tests. Exact-artifact release, patch, rejection, full maintenance and recovery remain explicitly pending. The paired runner validates the new chapter reference and points readers to it without changing deployment behavior. Shell syntax, preflight, local links and whitespace checks pass; no runtime tests are needed for this explanatory change.


## Toolchain reading order — 2026-10-17

Reordered the results guide for Oracle database specialists: Database/PLSQL, SQLcl, Liquibase, APEX/ORDS, Git, shell/Python helpers, then Podman lab infrastructure. Responsibilities and readiness claims are unchanged. Reconciled the companion runner comment; syntax, chapter preflight, local links and whitespace checks pass. This editorial change requires no database operation.


Toolchain order refined: APEX/ORDS first, SQLcl second, then Database/PLSQL, Liquibase, Git, shell/Python helpers and Podman. Content and operating behavior unchanged; companion comment, syntax, chapter preflight and whitespace checked.

## Initial release source/controller audit — 2026-10-17

Checked SRS UC-4/7/11, architecture artifact/identity/retention/publication contracts, test profile, accepted initial-install selection, sprint setup/design/tests, construction record, README/operator/results status and current board. This increment implements only the empty-target initial contract; upgrade/repeat installation, full maintenance concurrency, patch, drift/incompatibility deployment scenarios and repair remain pending. The results walkthrough correctly still stops before release operations until actual archive qualification/promotion passes.

Inspected raw native captures, archive fixture checks and control rejection evidence. New SQL operations bind named epoch/application/hash variables across nested SQLcl includes, validate exact environment/identity and retain interrupted ownership. No migrated database history/checksum is edited. Candidate development checks and post-integration fresh-archive qualification are separate. Atomic publication with public APEX export/status APIs remains an explicit disposable-target experiment, not an assumed guarantee. Only the bounded packaging/control source increment is ready for local commit; no actual build, complete qualification or TEST mutation is claimed by this audit. Syntax/link/whitespace and staged credential checks apply before commit.


## Publication API boundary and external gate — 2026-10-17

Fresh reconstruction and restricted browser greeting/configuration checks passed for the first d0e4d37 archive, but the publication feasibility experiment raised ORA-01453: APEX_EXPORT starts a read-only transaction and cannot follow availability DML. Separate measurements also proved that native availability changes the application checksum. The archive remains retained and unqualified; TEST was not installed. Its inspected qualification attempt is retired as failed with a reason, retaining control history, diagnostic output and synthetic data evidence before disposable reconstruction. This is qualification-source correction, not retained-target forward-repair acceptance.

Implemented the already-approved external gate through App Builder's Database Session initialization hook, captured with native export. It reads E1_CTRL state on each application request: ordinary business access is denied while installing/verifying; only authenticated VERIFIER business requests are permitted in verification. The three named private authoring apps remain development checkpoints. Missing controlled-target state fails closed. Native availability can now be prepared/committed while the external gate stays closed, followed by read-only live fingerprint capture; final receipt and external ready state publish in one transaction. Interruption before that final commit leaves ordinary access blocked. Initial-only admission refuses existing apps, so upgrade/in-flight request drain and general stale-verifier concurrency remain later proofs.

Reviewed the new raw source diff: initialization code, explicit default public user, generated SCN/component map only. Unchanged captures match. Control package compiles and gate unit checks cover ordinary denial, verification access and missing state; packaging fixture and transactional composition/history tests pass. Native guarded-target browser/cutover checks remain required in the next disposable reconstruction before TEST. Source/schema migrations are unchanged, credentials remain private, other sprint artifacts are untouched. Syntax/link/whitespace and credential scan apply before local commit.

## Initial release result and operator documentation — 2026-10-18

Reviewed the actual Q/TEST native stage transcripts, matching archive receipts, fingerprint comparisons, rollback result and ordinary/verifier runtime screens. Both initial installations are published; the previous “qualification pending / TEST empty” statements in current guidance are superseded. Historical experiment records remain unchanged. The earlier archive remains retained and unqualified, with its qualification attempt recorded failed; it was never promoted.

The results guide and runner now progress through A/B/C, qualification and TEST runtime URLs, then stop explicitly at pending patch/rejection work. The operator guide exposes each native deployment stage plus small keypress wrappers and safe existing-result reruns. Cleanup stays a separate visible prerequisite. The infrastructure guide now explains inspected disposable qualification reset, retained epochs/history and regrant after reset. Toolchain ordering remains APEX/ORDS, SQLcl, Database/PLSQL, Liquibase, Git, helpers, Podman.

The scoped registered integration check passed (1/0), including field-level retained history/configuration equality around repeat no-op commands and repeatable test fixture execution. Unit assertions passed (2/0), platform smoke passed (1/0), walkthrough preflight passed and real CLI rehearsal reached the documented exit-3 remaining-scenario boundary. Browser TEST history contains 21 rows and Installed components shows three 1.0.0 versions. Documentation links/anchors/fences and whitespace checks pass; shell syntax checks pass. Fresh-wrapper human keypress reproduction, upgrade, negative-deployment demonstrations, complete maintenance/draining and repair remain explicitly pending. No other sprint, plan, backlog or board status changed. Review and credential scan precede the local commit; no push is authorized.

## Patch source increment review — 2026-10-18

Reviewed the additive 005 migration, unchanged 001–004, explicit supported triples/dependencies and native source diff (application version 1.0.1 plus generated SCN). Two unchanged release captures match. The focused whitespace assertion reproduces the old defect and passes after applying 005 in C. Existing UT-1 initially expected only database constraint/null errors for blank input; its accepted rejection codes now include the patch's specific -20314. Corrected unit regression passes (2/0). Control package compiles; patch admission requires both fresh and upgrade qualification before TEST, locks retained mutation state before maintenance, preserves durable ownership and reuses guarded publication. No TEST application mutation or patch qualification is claimed at this source stage.

Reviewed the native drift fixture against its earlier capture: only Home title/header and generated SCN differ. App Builder's registered keyboard edit/save produced the actual fixture; C was restored. Raw Oracle-generated files are unchanged. The fixture is explicitly outside release contents; the TEST-only demonstration saves the actual target export and preserves offset for restoration, comparing the original fingerprint and retained data. Compatibility proposals cannot enter mutation operations. Existing initial archives/controller remain supported unchanged. Operator chapters describe atomic stages, supported starts, explicit fixture cleanup and remaining maintenance limits. Syntax, whitespace, local links and staged credential checks precede the local source commit; live archive qualification follows the commit/build and is not inferred from this review.

## Selected patch/protection delivery and walkthrough audit — 2026-10-18

Reviewed the accepted patch archive/source/configuration identities, separate fresh/baseline-upgrade qualification receipts and TEST upgrade receipt. Native stage transcripts, real verifier/ordinary browser flows and field-level 21-row preservation checks support the selected result. Migrations 001–004 remain unchanged; 005 corrects Hello validation and advances only Hello to 1.0.1. Existing protected TEST probe data remains retained. The held mutation-guard test supports bounded admission serialization; generic browser maintenance errors are not presented as specific rejection evidence.

Both selected negatives ran through the actual preflight path. Their before/after comparisons cover application/program definitions, versions, data/configuration/history and control receipts. The Foundation-major proposal is a versioned review fixture, not a constructed destructive migration. The page fixture is unchanged native App Builder output outside release contents. Its explicit save/inject/reject/restore sequence preserves the target's offset, original successful fingerprint and all retained data, including new greetings created during the demonstration. Repetition through the registered test and complete results runner restores the same fingerprint.

Corrected the SQL reader to distinguish stored CSV diagnostics from real Oracle diagnostic lines; real nonzero SQL failures/missing completion markers still fail. The associated IT-7 assertions pass. Operator result/status helpers now explicitly enable server output. These current operator/test helpers are maintained with the walkthrough; authoritative release SQL and the pinned patch controller still execute unchanged from archive 200ebeff… built at source 752eb47. The archive was not rebuilt after qualification.

Reconciled README, deployment lifecycle instructions, test profile, construction/test evidence, user manual and paired A–H results runner. Initial 1.0.0 receipts remain historical; current C/Q/TEST carry Hello 1.0.1. Cleanup is a separate visible step. The runner now completes selected coverage with exit 0 and distinguishes its controlled TEST fixture writes from read-only result checks. Native imports may require re-login. Interrupted fixture cleanup remains explicit; unexplained changes block restoration. Toolchain order remains APEX/ORDS then SQLcl.

Selected integration 3/0, unit 2/0, smoke 1/0, separate preparation and full selected CLI rehearsal pass. The rehearsal skips human viewing; actual browser screenshots support the user-visible claims. Full IT-1 and broader schema drift, concurrency, maintenance/verifier fencing and repair remain explicitly open; full integration/sprint-completion and second-operator reproduction are not claimed. No other sprint, plan, backlog or progress-board status changed. Local links/anchors/fences, syntax, whitespace and staged-credential checks apply before the completed increment is committed locally. No push is authorized.

## Walkthrough chapter split and naming audit — 2026-10-18

Reviewed the requested script split against the current SRS, architecture, test profile/specification, E.1 setup/design, implementation/test evidence and progress board. This changes operating presentation and independent chapter execution; accepted application scope, use-case mapping, coverage limits and PBI/sprint states remain unchanged. No other sprint artifact is edited. Previous completed delivery increment is local commit 47c5a79.

The current results guide is now cicd-walkthrough.md. Its launcher calls eight explicit A–H scripts. Chapter names are checked by the scripts; the guide lists each exact filename, purpose, direct command pattern, supported existing state and modes. Shared code contains only pauses, SQL/error handling and chapter preparation. Standalone E verifies its own historical promotion receipt. README, deploy.md and user_manual.md link the correct runners and retain the explicit separate cleanup step. The earlier detailed operator runner is preserved as cicd-operator-walkthrough.sh with only the usage command renamed. The guide, launcher, chapter scripts, helper, cleanup guidance and operator manual explicitly remain one maintained artifact. Historical raw evidence and dated implementation descriptions retain the filenames used at that time; the guide documents the transition.

Inspected [verification evidence](tests/walkthrough_split_20261018.txt): local preflight and standalone E pass; complete A–H CLI rehearsal returns 0 with both specific rejections and exact native restoration/data preservation. Checked interactive quit, argument errors, portable Git-root discovery, Bash syntax and preservation of the detailed operator implementation. Qualified archives and pinned controllers are unchanged; no new application deployment is implied. Human viewing was skipped; broader concurrency, maintenance fencing and failed-additive repair remain open.

Local checks passed for 33 documents and 261 links/anchors, fences and traceability links. Bash syntax, staged whitespace validation and staged credential scan passed. No remote push is authorized.

## Main walkthrough navigation — 2026-10-18

Added a linked Contents section immediately below the title in [cicd-walkthrough.md](cicd-walkthrough.md), covering all 17 existing main chapters. Reviewed the paired launcher/chapter scripts: chapter headings and operations are unchanged, so no script change is needed. All A–H local preflight checks pass. The documentation checker passes for 33 documents and 278 local links/anchors, fences, traceability and whitespace. Scope, use-case coverage, readiness and other sprint artifacts remain unchanged. Previous walkthrough split is local commit c3b165c.

## Commands in each walkthrough chapter — 2026-10-18

Added the exact standalone Bash invocation directly below every A–H action heading in [cicd-walkthrough.md](cicd-walkthrough.md), including E promotion, plus a visible cleanup command in the preparation chapter. The maintenance rule now requires chapter-local invocation blocks. Checked all eight commands against their actual script files and prepare_stage headings; all A–H preflight checks pass. Documentation links/anchors/fences, traceability and whitespace checks pass. Paired script behavior, existing use-case scope/readiness and other sprint artifacts are unchanged; no Oracle mutation or repeated application tests were needed for this presentation correction.

## Chapter-by-chapter entry point — 2026-10-18

Corrected the main results instructions and preparation continuation to start A_foundation explicitly and run B–H separately after each passing chapter. The combined launcher is retained only as an optional shortcut. README and user_manual entry commands now match. Chapter commands and script behavior are unchanged. Reviewed paired scripts; all A–H local preflight checks and documentation link/anchor/fence/whitespace checks pass. Scope and sprint states are unchanged.

## Fresh-start lifecycle and walkthrough audit — 2026-10-18

Reviewed the Product Owner's explicit fresh-start/discard request against the SRS, architecture, test profile, E.1 setup/design and current progress board. Normal releases still preserve retained data; complete destruction is the separately requested disposable-demo lifecycle. Updated the E.1 design with that boundary. No backlog, plan, board status or other sprint artifact is changed. Earlier database observations/screenshots/epochs remain historical and are not current reconstruction evidence.

Reconciled README, deploy.md, user_manual.md and the main cicd-walkthrough.md with precheck → named-host preparation → destructive cleanup → fresh database/APEX installation → A–H. Every action chapter exposes its exact script command and expected result. The main guide has updated navigation plus explicit end-of-demo destruction. It distinguishes missing prerequisites, unavailable infrastructure, empty application areas, new construction, verification examples, patch preservation, failure inspection and deliberate restart. The old defaults-only operation is separately named and explicitly retains history. The chapter scripts/common helpers and granular native procedures are reviewed together as one artifact.

Inspected [fresh execution evidence](tests/fresh_walkthrough_20261018.txt), real empty-state and isolation checks, A–H native installation/release transcripts, new same-artifact receipts and field-level comparisons. Application source/release archives and pinned controllers are reused unchanged. Rehearsal explicitly skips browser viewing and creates current-cycle runtime examples; it does not restore old history or establish new browser acceptance. Existing-resource refusal and cleanup ownership policy tests passed. Broader unselected technical proofs and Lifecycle Architecture remain open.

Registered lifecycle unit 1/0 (four policy cases), greeting/history unit 2/0, smoke 1/0 and fresh-result IT-2 integration 1/0 pass. Syntax, chapter command mapping, Git-root portability, invalid argument handling and local documentation links/anchors/fences/whitespace checks pass. Final empty delivery checkpoint passed after a second explicit cleanup/install: no lab applications/business tables, no old control events/attempts, new target epochs zero. The read-only infrastructure probe reports APEX 24.2.0 VALID and checks its completion marker after switching PDB. Interactive q leaves the delivered cycle empty. The unrelated default VM remains untouched. Staged credential and whitespace checks pass. Local validation passes for 33 documents and 284 links/anchors, fences and traceability links. No push is authorized.

## Infrastructure and onboarding separation audit — 2026-10-18

Reviewed the Product Owner's explicit vanilla-infrastructure and per-developer setup requirement against SRS UC-8, architecture AI-1/AI-2 and control bootstrap, E.1 setup/design/test specification, test profile, implementation/results records, README and the current progress board. The design now states the refined responsibility boundary. Scope remains the existing PBI-011.1 setup work; no managed artifact status or other sprint changes are needed. The previous fresh-start increment is local commit f1bf6ef.

Reconciled README, deploy.md, user_manual.md and the main walkthrough with infrastructure-only installation → control-only initialization → one-area privileged provisioning → developer private configuration → separate readiness. Exact commands/actors/password distinctions are present. Removed whole-project bootstrap and global grants; qualification reset touches only qualification, and F no longer reinstalls control packages. Infrastructure contains no customer-specific SQL/check dependency. Scripts and chapters were reviewed as one artifact.

[Native evidence](tests/onboarding_boundaries_20261018.txt) confirms HTTP/database checks, zero project schemas/workspaces before onboarding, package compilation without area grantees, A-only provisioning, A/B/C private profile setup, selected qualification reset preserving all other schema/workspace IDs, five identities, cross-area denials and absent applications/business history/control events. The final checkpoint is separately onboarded and ready for A. Reused accepted application/release evidence; A–H is not newly rerun or claimed by these setup tests. Broader concurrency, fencing and repair remain open. No OS-account security isolation is claimed.

Lifecycle unit regression passes 2/0 with nine policy subcases; Bash/Python syntax and pinned-controller equality checks pass. Local document links/anchors/fences, traceability and whitespace checks pass. Final document validation covers 33 documents and 295 links/anchors. Staged credential and E.1-only boundary scans pass. No push is authorized.
