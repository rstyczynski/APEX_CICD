# E.1 — Prototype construction

## Current increment

Status: under_construction

The approved first slice constructs the application from scratch, delivers an initial release and compatible Hello patch, then demonstrates rejection of an incompatible Foundation upgrade and unexpected live APEX drift. The [design](sprint_E.1_design.md) retains the broader concurrency/recovery work for later selection. This document is maintained during construction; pending work is not presented as delivered.

## PBI-011.1 — Tools, platform and private areas

Implemented checksum-pinned private SQLcl 25.3.0.274.1210 and Temurin Java 21.0.12.1+1 provisioning in scripts/cicd-tools.sh. Tools remain under the ignored .local-apex directory; host Java and user-level configuration are unchanged. SQLcl uses a project-local connection store, protected saved connections, disabled command history and credentials sent through standard input rather than process arguments. scripts/apex_sql.py redacts known secrets from failures and requires a server-side completion marker.

Reused the running apex-cicd VM and its existing database/APEX/ORDS installation. Observed host headroom is now approximately 63 GiB, with 18 GiB free in the VM. The shared docs/deploy.md is maintained by E.1; its runtime-removal sequence preserves host credentials/downloads/evidence. No VM teardown has been necessary for this increment. docs/deploy.md now provides separate operator commands from Podman inventory/helper/VM provisioning through network/volumes, database, APEX, ORDS, access checks, ordered stop/start and scoped reconstruction. Commands expanded from the adopted scripts are distinguished from newly executed checks. Retained-data backup/restore is not yet validated; recreation cannot be claimed to preserve that data. Rechecked both image digests/ARM64 architecture, helper 1.3.2, database health and the complete infrastructure verifier successfully.

config/areas.json declares private A/B/C schemas/workspaces/application IDs, one disposable qualification area and retained TEST. scripts/cicd-platform.py collision-checks before provisioning, records owned resources locally, creates ordinary developer/runtime identities through public APEX APIs and saves dedicated schema connections. It bootstraps E1_CTRL separately from application Foundation. Ordinary identities have no grants on another area's tables.

Executed results: all five named connections match their effective schema, FREEPDB1 and workspace association. Cross-area table reads and writes were rejected for all five areas. Recreated only E1_QUALIFY through the public workspace-removal/provisioning path; a separately committed TEST marker survived. Current isolation/preservation tests are being rerun through the registered test entry point after the SQLcl wrapper fix below. The existing platform verifier passes database/APEX registry checks, host-port authentication, ORDS/APEX HTTP routes and static asset version checks.

## PBI-011.2 — Control ownership

Implemented deploy/control.sql and scripts/cicd-task.py. The control schema stores component reservations, authenticated schema owner, task/base/generation and append-only acquisition/release events. A short NOWAIT coordination transaction acquires the complete requested scope or rolls back; committed reservation rows survive connection closure. Only registered A/B/C schemas may invoke the ownership package; they receive package execution rather than authority-table DML grants.

Executed result: A acquired Foundation for foundation-initial with ownership generation 1. A later SQLcl process verified that ownership before applying Foundation. The task remains held while the initial source baseline is completed. Parallel acquisition, reassignment and exhaustive negative ownership tests remain pending and are not claimed from this sequential run.

## PBI-011.3 — Foundation-first assembly

Implemented db/changelog.xml and immutable changeset 001-foundation. It creates component presence/version records, greeting-history snapshot storage and application/component operational states. Foundation is 1.0.0; Hello and World are explicitly not installed with no invented version. Root application state remains maintenance. No Hello/World business data was seeded.

Executed the changeset with SQLcl's bundled Liquibase 4.30.0 through deploy/foundation.sql. Liquibase validation and installation succeeded. Assertions verified Foundation's installed version, absent Hello/World and blocked application state.

Created application 810001, APEX Delivery Laboratory, from scratch through App Builder in E1_DEV_A. It currently contains the generated global, home and login pages only. Set native availability to unavailable during assembly using public APEX_APPLICATION_ADMIN. Application version is now 1.0.0, edited in App Builder. Component pages and the complete runtime guard still need construction.

## PBI-011.4 — Capture and reconstruction

Captured the Foundation shell through SQLcl split export with skipExportDate, expOriginalIds and supporting objects excluded. The captured source is in apex/f810001. Repeated capture without edits produced byte-identical contents across all 38 exported files. Oracle-generated export scripts are retained unchanged; custom code does not write APEX repository tables or invent internal APEX calls.

Private-target import mappings, cross-area capture stability, safe capture reconciliation/deletion handling and the reusable capture entry point remain pending. A successful repeated capture from A alone does not yet prove stability between A/B/C identities.

## PBI-011.5–011.8 and PBI-012–016

Hello/World authoring, integration, semantic-version patch, artifact build/qualification/promotion and the selected incompatibility/drift demonstrations remain to be implemented. The test skeletons and manifest register their selected assertions; unimplemented assertions fail explicitly. The wider parallel/failure-repair scenarios remain later work. Requirements/architecture refinement and the Lifecycle Architecture/Construction decisions depend on the resulting evidence and are not complete.

## Tests and fixes

tests/run.sh supports smoke, unit, integration, component manifests and new-only selection. Tests are grouped by domain, with the selected E.1 assertions in new_tests.manifest and the current platform subset in platform_tests.manifest. The first unit skeleton execution correctly reported two pending failures. Platform smoke has passed; the full unit/integration suites are not passing or complete yet.

The first disposable-reset preservation assertion failed because an interactive piped MERGE statement had not executed; a separately inserted and committed marker survived reset. Changed the SQLcl boundary to execute a protected temporary script file and require the database to emit its completion marker. Rechecked MERGE persistence in a second session and deliberate Oracle-error propagation successfully. See the [fold-in fix](sprint_E.1_bugs.md). No retained application history existed or was removed during this check.

Available timestamped smoke evidence includes test_run_A1_smoke_20261016_185316.log and test_run_A1_smoke_20261016_185650.log; the [test record](sprint_E.1_tests.md) maintains the verified list and results. New gate logs are recorded as they finish. No complete-sprint pass or production-readiness claim is made.

## Working commands

The [operator guide](user_manual.md) provides the application/workspace inventory, endpoints, logins, local password retrieval and stage-by-stage pipeline. Run from the repository root. Ordinary checks use the saved schema connections. Provisioning alone uses the existing platform administrator credentials.

The primary operator walkthrough now uses native SQLcl sessions and visible SQL files under deploy/operator, App Builder and Git. Executed SQLcl target identity, application inventory, component/state inventory, Foundation verification and separate control-reservation inspection successfully. Application 810001 now displays version 1.0.0; native runtime availability remains Unavailable during incomplete assembly. These operations are independently usable and do not invoke a test harness. scripts/cicd-env.sh only selects the local tools and connection store for the operator's terminal.

The isolation checks now have separate SQL files under deploy/checks and separately runnable operations. Show a statement before executing it, inspect A's identity, create each area's probe, and attempt the cross-area read/write independently:

```bash
python3 scripts/cicd-isolation.py show identity lab-dev
python3 scripts/cicd-isolation.py identity lab-dev
python3 scripts/cicd-isolation.py create-probe lab-dev
python3 scripts/cicd-isolation.py create-probe lab-dev-b
python3 scripts/cicd-isolation.py deny-read lab-dev lab-dev-b
python3 scripts/cicd-isolation.py deny-write lab-dev lab-dev-b
```

Executed this sequence successfully: E1_DEV_A / FREEPDB1 / E1_DEV_A identity, existing probe retained, read denied with ORA-00942 and write denied with ORA-00942. Output prints the actual connection/schema, SQL attempt, expected result and observed Oracle error. These operations affect only the probe tables. The combined check/isolation commands now execute these same atomic SQL operations and print the steps and observed errors.

The operator guide now separates migration identity/ownership checks, native Liquibase validation/status/application, migration-receipt inspection, native APEX export to staging and Git/directory diff review. Rehearsed the inspection and export operations through SQLcl directly. Validation succeeded, status reported the database up to date, and DATABASECHANGELOG identifies db/changelog.xml::001-foundation::apex-lab as EXECUTED. The staged export differs from the initial source only in application version and its generated version SCN. Source reconciliation remains pending.

During rehearsal, SQLcl resolved Liquibase's relative changelog against the last @script directory and stopped without applying a change. Added an explicit native SQLcl cd to the checkout root before Liquibase commands; the corrected sequence passed. The wrong-target identity check also rejected E1_DEV_B expectations while connected as E1_DEV_A with ORA-20010. These are operating instructions exercised against the real runtime, not a replacement Python simulation.

The original provisioning helper is still being separated into explicit schema/grant, workspace, user and saved-connection stages. Its reset-qualify operation destroys/recreates only the disposable qualification area. Full unit/integration suites still contain explicitly pending application implementation.

## Next construction steps

Complete the platform checks and audit its adopted sources, finish Foundation's versioned source baseline and ownership handover, then validate supported imports into the private B/C areas. Build the component pages and greeting/history flow next. Keep source commits, migrations, component versions, artifact hashes and installed fingerprints distinct throughout release construction. Commit completed increments after their audits; no remote push is authorized.


## App Builder operator instructions

Expanded manual step 4 into exact DEV_A password retrieval and workspace login, application selection, version inspection and the already performed Version/Apply Changes operation, Home/Login Page Designer inspections, expected unavailable runtime and continuation to migration/capture. Checked the current login field labels and runtime maintenance screen in the browser. Page names, titles, login item names and live version/status were reconciled with the captured Oracle export and prior authoring evidence. This walkthrough requires no new application edit.


## Operator-document readability

Reformatted every chapter of the operator manual and deployment guide into numbered actions or short bullets. App Builder instructions now separate each click, field and check; command blocks remain copyable beneath their associated action. Explanations, expected results and pending capabilities remain explicit. No runtime behavior changed.


## Guided operator execution

Implemented scripts/cicd-walkthrough.sh for the existing manual's main chapters 1–8. The runner reads chapter text from the manual, prints each native SQLcl operation, pauses for a keypress, streams actual output and stops on errors. Browser stages display their URL and manual instructions, then wait for operator continuation; they do not simulate browser success. A diff reports review required without accepting source. Live password display requires its own keypress and is skipped in rehearsal. The initial already-applied migration is not rerun, and unfinished release stages remain pending.

The manual and docs/deploy.md now require the guide and matching script to be updated/reviewed together as one operating artifact. Preflight validates local tools/files/chapter mappings; rehearsal executes current CLI operations and staging export with explicit human-step skips. A PTY check confirmed a keypress advances to sql -version, the next operation pauses, and q stops before the database command. Full rehearsal passed all 15 native SQLcl operations and the staged export; Git diff correctly reported review required. Browser/password/human checks were explicitly skipped. An isolated fixture confirmed a real Oracle error is displayed and halts the runner before later operations.


## Developer outcome walkthrough

Added developer_walkthrough.md and scripts/cicd-developer-walkthrough.sh as the second, higher-level view. The documented journey groups A/Foundation, B/Hello, C/World and exact-artifact release, with explicit Product Owner URL checkpoints after each future delivery outcome. Incomplete assemblies retain maintenance; App Builder exposes their definitions without weakening runtime guards.

The current runner groups actual A identity/inventory/assembly/control checks, streams Oracle results and pauses at A's runtime and Builder URLs. It then stops with PENDING/status 3 before B, whose application is not implemented. This inspection is not a replay of completed developer delivery and does not release A's active task. Detailed and outcome manuals/runners must be reconciled together as construction proceeds.


## Runtime results and deployment protection view

The separate outcome walkthrough now asks the Product Owner only to use runtime URLs and read operation outcomes. Removed its App Builder URL/login/definition-inspection checkpoint. The documented journey shows successful complete deployment and compatible patch behavior, then specific incompatible-contract and drift rejections with unchanged-target/history verification and a working application afterward. These deployment controls remain pending implementation. The current runner checks the existing Foundation, shows only its blocked-runtime result and stops before B; it does not claim a new deployment or protection proof. Existing operator walkthroughs remain unchanged.


## Outcome-walkthrough use-case alignment

Added explicit SRS UC mappings for the selected A/B/C journey, configuration/greeting, exact-artifact release/patch, incompatible Foundation rejection and drift rejection. Distinguished onboarding prerequisites, UC-6 reproduction evidence, UC-5 rejection versus full repair, later concurrency/recovery cases and unselected UC-12 adoption. The guide expresses intended coverage; current executable coverage remains Foundation checks only. Existing operator walkthroughs remain unchanged.


## Foundation source handover increment

- Added immutable migration 002-foundation-runtime: compiled composition API, mutation gate and immutable snapshot guards; no component business data seeded.
- Authored Home's Create greeting action and a read-only Greeting history report (page 10) in App Builder; captured Oracle-generated source unchanged. Restored the intended application display name.
- Two unchanged native captures match byte-for-byte. Reconstructed the same Foundation source/database in E1_QUALIFY through public APEX_APPLICATION_INSTALL mapping; registry, absent-component state, compile checks and maintenance assertions passed. This is an assembly experiment, not a qualified complete release.
- Released A's foundation-initial reservation after verification. The detailed capture operation now acquires/releases its own new reservation instead of depending on that closed task's generation; the fresh capture matched source exactly.
- Registered IT-4's Foundation-only assertions passed. Complete application and release tests remain pending.


## Hello intermediate assembly

- Accepted Foundation increment committed locally as e9a490f. B reserved Hello at that base (hello-initial, generation 3) on codex/e1-hello before preparing its private area.
- Applied accepted Foundation migrations/source to E1_DEV_B/application 810002, then new migration 003-hello. Compile and blocked-assembly checks pass; no business entries seeded.
- Authored Hello pages 100/101 and configuration pages 110/111 as DEV_B. The captured form's SQL selector filters active entries; configuration creation/deletion and entry deletion are hidden. Database guards enforce those rules independently.
- Two unchanged B exports are byte-identical. Reviewed generated original-ID offsets, manifest comments, component-map cache and per-target UI identity as comparison-only metadata. Raw Oracle export files remain unmodified. Foundation page behavior is unchanged; Hello owns the added pages/LOV, with declared generated navigation/include additions.
- B remains unavailable with an accurate World-not-installed message. Its task is released after scoped verification/source review. Combined browser behavior is tested after C; this intermediate contribution does not complete child 5 or release qualification.

## World and combined database construction

- Hello source accepted as f511ab8 and integrated locally before C's task. C reserved World at that Git base (world-initial, generation 4), reconstructed Foundation/Hello into E1_DEV_C/application 810003 through the supported mappings, and passed the inherited Hello assembly checks.
- Applied immutable migration 004-world and authored World pages 200/201/210/211 as DEV_C. Root maintenance is retained while source/combined browser verification is in progress.
- UT-1 and UT-2 now run real Oracle assertions on C and pass: exact defaults/trim/prefix/Unicode composition, explicit selections, missing entry/default deactivation rejection, blank/oversize input and maximum length; unchanged original history snapshots after settings/data changes and rejected history update/delete. Fixtures roll back, including the temporary ready state; no seed entries/history remain from the unit suite.
- Capturing/reviewing C's scoped source next, before the shared composition refinement and restricted browser verification.


World source review passed against f511ab8: four World pages, its LOV and generated navigation/includes; existing Hello/Foundation behavior and original component identities are preserved. Two repeated C exports match byte-for-byte. Reviewed source copies remain raw Oracle output. World task generation 4 is released; the next shared composition change requires its own complete reservation before authoring.


## Complete development assembly — 2026-10-17

1. Reserved Foundation/Hello/World together for `compose-initial`, generation 5, from accepted World source 96f603c before shared authoring in C.
2. Authored Home's independent active Hello/World selectors in App Builder, passed their selected IDs to the existing composition API, used character-length result storage and enabled duplicate-submit prevention. Added read-only page 20, Installed components.
3. Ran separate C identity, all-three ownership and complete-assembly SQL checks. The bounded `deploy/operator/verify_development.sql` set native restricted access for VERIFIER before enabling development verification. Ordinary LAB_USER received **Development verification in progress.**
4. Through runtime pages, entered Hello/World, selected both defaults and saved **Hello World** as VERIFIER. Reopened history. These explicit verification inputs remain in C; no business data is embedded in the application export.
5. Ran `deploy/operator/publish_development.sql` after those checks. It requires the verification snapshot and publishes only C. As LAB_USER, selected Hello/World explicitly, saved another greeting and reopened/refreshed history: row 41 remains alongside the earlier verifier row 21. Installed components displays all three at 1.0.0.
6. Exported twice through native SQLcl with `apex export -applicationid 810003 -split -skipExportDate -expOriginalIds -expSupportingObjects N -dir <fresh-private-directory>`. Both complete captures match byte-for-byte. Reviewed shared Home/report/navigation edits plus native default-report layouts materialized by first runtime use. Existing component form behavior/report queries remain unchanged. Copied raw Oracle source into the canonical source directory without editing generated calls.
7. Released the complete composition reservation after source/browser verification. The verification/publication scripts intentionally reference that closed construction token; they are evidence-backed bounded operations, not reusable release installers.
8. Updated both results-runner and chapters: check preserved A/B incomplete results, then C's published development result and runtime URL, then stop at the pending release boundary. The runner does not redeploy historical developer work. The detailed operator guide retains its existing purpose and now explains current migration state and runtime use.

Evidence: [source review](tests/complete_source_review.txt), [unit assertions](tests/complete_unit.log), [smoke](tests/complete_smoke.log), [Foundation regression](tests/complete_foundation_regression.log), [results-runner rehearsal](tests/complete_results_rehearsal.log), [saved history](tests/development-history.jpg), [component versions](tests/development-versions.jpg).

This is the selected sequential development prototype increment. Retain it as prototype source/operating guidance; no production suitability decision is implied. Qualification/promotion of identical release bytes, Hello 1.0.1, incompatible-major pre-write rejection and drift-stop evidence remain under construction. Full maintenance/verifier fencing, parallel reservations/races and automated additive-failure repair remain unproved broader risks; do not infer them from native restricted development access.

## Portable, repeatable results walkthrough — 2026-10-17

- Maintained commands discover the checkout through Git. Shell entry points use their script location with `git -C ... rev-parse --show-toplevel`, so they also work when invoked from a subdirectory or by absolute script filename. SQLcl receives the discovered shell root via session_root.sql; its own `cd` uses that substitution variable.
- Added a separate visible cleanup/preparation operation and invoked it before the results walkthrough. It checks idle control ownership and A/B/C identities/versions before configuration writes, backs up C defaults as private restoration SQL, reuses active Hello/World examples (creating only missing demo entries), and restores empty prefixes/defaults without deleting history or other entries.
- Before/after SHA-256 snapshots cover all fields of each retained greeting. Preparation never resets qualification, TEST, schemas, credentials, Podman resources or release records. Failed/unsupported target states require inspection instead of automatic recovery.
- The results runner no longer prints planned release instructions as though they had executed. It explicitly completes the implemented A/B/C checks and then reports an incomplete release pipeline (exit 3). Repeating cleanup cannot implement the unfinished release stages.
- The earlier release-control/archive work remains separate and under construction. This correction does not qualify/promote an artifact or change the selected design.


## Explicit cleanup step — 2026-10-17

The results guide now lists cleanup as numbered run step 2, its PASS/backup check as step 3, and starting the walkthrough as step 4. Removed the automatic cleanup call from the results runner so following the documented sequence performs cleanup once. Reconciled the operator guide and README. Cleanup behavior and preservation scope are unchanged; no release or sprint status change. Verified shell syntax, chapter/preflight mapping, local links and whitespace.


## Toolchain explanation in the results guide — 2026-10-17

Added Applied tools and techniques immediately after Deep dive. Explained Podman/logical areas, Oracle/PLSQL, APEX/ORDS, SQLcl/Java, Liquibase, Git and small operator/test helpers; source capture/review, Foundation-first assembly, versions versus archive/live fingerprints, fail-stop checks and retained-history evidence. Reconciled statements against the SRS, architecture, test profile, accepted design and actual development tests. Exact-artifact release, patch, rejection, full maintenance and recovery remain explicitly pending. The paired runner validates the new chapter reference and points readers to it without changing deployment behavior. Shell syntax, preflight, local links and whitespace checks pass; no runtime tests are needed for this explanatory change.


## Toolchain reading order — 2026-10-17

Reordered the results guide for Oracle database specialists: Database/PLSQL, SQLcl, Liquibase, APEX/ORDS, Git, shell/Python helpers, then Podman lab infrastructure. Responsibilities and readiness claims are unchanged. Reconciled the companion runner comment; syntax, chapter preflight, local links and whitespace checks pass. This editorial change requires no database operation.


Toolchain order refined: APEX/ORDS first, SQLcl second, then Database/PLSQL, Liquibase, Git, shell/Python helpers and Podman. Content and operating behavior unchanged; companion comment, syntax, chapter preflight and whitespace checked.

## Initial release artifact/controller source increment — 2026-10-17

- Reviewed two byte-identical native release captures: source imports as UNAVAILABLE; C's live development availability was restored. Only status/message/SCN and native versions-report default layout changed from the reviewed development source; raw Oracle files remain unedited.
- Added clean-Git packaging, an explicit candidate-validation receipt, complete member hashes, a retained archive SHA-256 and safe extraction. Native SQLcl/PLSQL remain the deployment interface. The one-operation controller prints every SQLcl command and executes SQL only from a newly verified archive, checks its own archived controller bytes, pins target configuration/tools and refuses any existing target for this initial path.
- Release control is outside application migrations. Initial attempts bind target schema identity, expected epoch, artifact hash, source commit and configuration digest. Missing qualification and stale epochs/tokens reject; ownership persists across installation commits/disconnects. No arbitrary-state resume or upgrade path is supplied.
- Separate initial operations are admission, migration, unavailable import, transactional unit checks, restricted verification, and final publication/receipt. Every operation must bind the same archive hash and epoch. Preliminary integrity checks exact component/migration/application versions and pages. Publication/fingerprint atomicity and native end-to-end delivery are still to be exercised in disposable qualification before TEST admission.
- Packaging fixture checks pass, including a path containing spaces, overwrite/dirty-source/changed-byte/traversal rejection. Native control compilation and specific missing-qualification/stale-token checks pass without target mutation. This source increment enables the next archive experiment; it is not a qualified or promoted release.


## Publication API boundary and external gate — 2026-10-17

Fresh reconstruction and restricted browser greeting/configuration checks passed for the first d0e4d37 archive, but the publication feasibility experiment raised ORA-01453: APEX_EXPORT starts a read-only transaction and cannot follow availability DML. Separate measurements also proved that native availability changes the application checksum. The archive remains retained and unqualified; TEST was not installed. Its inspected qualification attempt is retired as failed with a reason, retaining control history, diagnostic output and synthetic data evidence before disposable reconstruction. This is qualification-source correction, not retained-target forward-repair acceptance.

Implemented the already-approved external gate through App Builder's Database Session initialization hook, captured with native export. It reads E1_CTRL state on each application request: ordinary business access is denied while installing/verifying; only authenticated VERIFIER business requests are permitted in verification. The three named private authoring apps remain development checkpoints. Missing controlled-target state fails closed. Native availability can now be prepared/committed while the external gate stays closed, followed by read-only live fingerprint capture; final receipt and external ready state publish in one transaction. Interruption before that final commit leaves ordinary access blocked. Initial-only admission refuses existing apps, so upgrade/in-flight request drain and general stale-verifier concurrency remain later proofs.

Reviewed the new raw source diff: initialization code, explicit default public user, generated SCN/component map only. Unchanged captures match. Control package compiles and gate unit checks cover ordinary denial, verification access and missing state; packaging fixture and transactional composition/history tests pass. Native guarded-target browser/cutover checks remain required in the next disposable reconstruction before TEST. Source/schema migrations are unchanged, credentials remain private, other sprint artifacts are untouched. Syntax/link/whitespace and credential scan apply before local commit.

## Construction increment: initial identical-artifact delivery — 2026-10-18

- Qualified and promoted source **0f7c500e064e4f262a42fb74f4984eb0e4349c88**, archive SHA-256 **6a1da4a940586541cbb034277605d7ed36e5d1ad305554f9a2fe4c64cd59411c**. Qualification application **810004**, epoch **2**, and retained TEST **810005**, epoch **1**, are published **ready** with Foundation/Hello/World **1.0.0**.
- Actual archive-driven stages passed on both targets: atomic initial admission, four migrations, unchanged native split import, composition/history unit assertions, thirteen-page/version/compile integrity checks, VERIFIER browser verification and guarded publication. Ordinary LAB_USER subsequently created greetings and reopened history in both. TEST Installed components displays all three 1.0.0 versions.
- A prepared native AVAILABLE application remained externally gated until publication. Rolling back the final publication reverted successful receipt and external readiness together; the attempt remained verifying. The ordinary login error during that interruption was generic; it is not presented as a specific incompatible-deployment rejection. Server gate assertions and subsequent successful login with the same credentials support the gate result.
- Repeated qualification/promotion commands verify existing matching results without migrations/imports. The registered initial-only integration subcase passed: matching Q/TEST successful receipts, live APEX fingerprints, repeatable post-publication fixture, and exact equality of every retained history/configuration field before/after. TEST contains twenty VERIFIER snapshots plus one ordinary-user snapshot. Existing isolation probe data was retained.
- Results walkthrough preflight passes; unattended A/B/C/Q/TEST rehearsal reaches the deliberate remaining-scenarios boundary with **exit 3**. Browser checkpoints are skipped in rehearsal; separate real browser checks above passed. Unit suite **2 tests / 0 failures**; platform smoke **1 / 0**.
- [Initial delivery evidence](tests/initial_delivery_result.txt), [ordinary TEST greeting](tests/test-ready-greeting.jpg), [retained history](tests/test-ready-history.jpg) and [installed versions](tests/test-versions.jpg).
- Pending: compatible Hello 1.0.1 upgrade, pre-write incompatible Foundation-major rejection, controlled drift scenario, full upgrade maintenance/drain, concurrency and additive-failure automated repair. The full IT-1 upgrade/reconstruction and IT-2 patch entries remain pending; the bounded initial subcase does not complete them. No sprint closure or second-operator reproduction is claimed.

## Construction in progress: Hello patch and selected rejection scenarios — 2026-10-18

The authorized next increment implements Hello 1.0.1 whitespace normalization/blank rejection with an additive validation constraint, keeping Foundation/World at 1.0.0. Qualification must cover fresh reconstruction and upgrade from the accepted initial artifact before TEST receives identical bytes. Preserve all existing configuration/history fields. Expose explicit preflight/admission/migration/import/verification/publication commands, plus focused incompatible-Foundation and visible-page drift rejection demonstrations. Neither scenario may reach maintenance, migrations or import on rejection. Maintain the manual and results runner together. Full concurrency and failed-deployment repair remain outside this increment.

## Completed construction increment: Hello 1.0.1 and selected deployment protection — 2026-10-18

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

## Standalone results walkthrough chapters — 2026-10-18

Split the results runner into explicit independently executable A–H scripts named `cicd-walkthrough-A_foundation.sh` through `cicd-walkthrough-H_drift.sh`. The thin `cicd-walkthrough.sh` launcher runs those scripts in order and stops on failure/quit. Shared mechanics live in `cicd-walkthrough-common.sh`; actual SQL checks and case operations stay visible in the chapter scripts. E now independently verifies the archive/initial promotion receipt instead of relying on D's process/output. Cleanup remains a separate operator action.

Renamed the matching guide to [cicd-walkthrough.md](cicd-walkthrough.md). Preserved the detailed operator runner as `cicd-operator-walkthrough.sh`, changing only its usage command. Updated README, deployment instructions and user manual references together. Past transcript/narrative filenames remain historical; the new guide explains the naming transition. This is an operating-document/script refinement for the current PBI-011 demonstration, not a new application release or completion of other PBIs. The pinned release controllers and qualified archives are unchanged.

[Verification](tests/walkthrough_split_20261018.txt) covers local preflight, standalone E, complete real A–H rehearsal, quit/argument behavior, portable repository discovery and preservation after the controlled TEST fixture.

## Fresh infrastructure and executable construction walkthrough — 2026-10-18

Replaced settings-only cleanup with explicit complete destruction of the named lab containers, three storage volumes, network and Podman secret. The named VM/images, host credentials/tools/installers/reviewed archives and unrelated resources remain. The former defaults/history-preserving operation is retained separately as cicd-demo-defaults.sh. A read-only ownership inventory refuses unrelated consumers of lab volumes/network/secret and unexpected owned mounts/images before mutation.

Added separate prerequisite, named-host and fresh APEX initialization commands, using the existing deploy.md lifecycle and pinned inputs. Initialization installs a new database/APEX/ORDS, checks database/web/static assets, bootstraps isolated empty areas/control authority, exercises real isolation denials and verifies absent applications/business tables as administrator. Existing storage refuses installation; absent/unreachable engines are not silently treated as a successful reset.

A/B replay reviewed immutable Git snapshots; C installs the accepted complete initial source. Reservations and native SQLcl/Liquibase/APEX imports remain visible. D/E now execute new initial qualification/promotion rather than historical-result inspection. F explicitly recreates only disposable qualification for fresh and initial-baseline patch qualification, then upgrades TEST with identical patch bytes. Epochs are observed dynamically. Live verification pauses at runtime URLs; rehearsal creates announced NEW runtime examples and does not claim browser verification. A failed/attempted chapter is retained for inspection; cleanup/install is a separate deliberate demo restart.

The new [fresh-run evidence](tests/fresh_walkthrough_20261018.txt) records a successful scoped destruction/reconstruction and complete A–H execution, 20 TEST/21 qualification pre-upgrade snapshots preserved, both selected specific rejections and original-fingerprint restoration. Initial and patch archive hashes/controllers are unchanged. Runtime approximately 4.8 minutes for fresh infrastructure installation and 7.3 minutes for the A–H CLI rehearsal on the existing four-vCPU/6-GiB/30-GiB lab host; these are observed transcript durations, not guarantees. This strengthens PBI-011.1/3/4/6/7 and PBI-012 evidence without completing the broader concurrency, maintenance fencing, schema drift or repair criteria.

After recording the successful complete rehearsal, repeated the explicit scoped cleanup/fresh installation and left the lab initialized with no applications or business/history tables. Final precheck reports APEX 24.2.0 VALID; administrator checks find no old control events/attempts and fresh release targets at epoch zero. An interactive q at A's first checkpoint returns 130 before any database mutation. The unrelated default VM remains present/stopped. This is the delivered checkpoint for the Product Owner's own A–H run.

## Separate infrastructure, project control and developer onboarding — 2026-10-18

The Product Owner requires vanilla Oracle infrastructure initialization and explicit separate project/developer setup. The infrastructure runner now ends after database/APEX/ORDS validation. It contains no project provisioning, project SQL or project-specific checks. The separate infrastructure-boundary test checks zero E.1 schemas/workspaces before onboarding.

Added explicit control-only initialization, privileged provisioning of exactly one named area, developer-side configuration using only its assigned schema password, and a separate empty-state/readiness command. Control package installation no longer depends on absent area grantees. Per-area grants belong to that area's provisioning. Qualification reset provisions/grants only qualification; F no longer reinstalls global control packages. Private developer SQLcl profiles do not open administrator credential files. Roles share one OS account in this lab; this is not OS-account isolation.

README, deploy.md, the main walkthrough, user manual and test profile describe these operations together, with exact commands and actors. Application sources, accepted archives and pinned release controllers remain unchanged. This refines PBI-011.1/UC-8 setup responsibility; it does not complete concurrency, maintenance or repair work. Native checks and final delivered state are recorded in [onboarding evidence](tests/onboarding_boundaries_20261018.txt).

## Explicit APEX destruction command name — 2026-10-18

Renamed the destructive lifecycle script to `scripts/apex-destroy.sh` at the Product Owner's request. Updated current deployment/manual/walkthrough invocations and the launcher's preflight together. Usage and terminal messages now say destruction. Behavior is unchanged; no destruction was executed for this rename. Historical evidence retains the command name used at execution.

## Post-install operator verification guide — 2026-10-18

Expanded the installation chapter with numbered automated and manual verification, ADMIN/INTERNAL sign-in, local password retrieval, optional SYSTEM/SQLcl authentication, service-account responsibilities and failure logs. Deployment section 8 links the main guide and retains individual layer commands. No fixed default password is documented: existing protected generated credentials are reused. Scripts are unchanged; the existing verifier was rerun successfully. Manual sign-in is an operator step, not a new browser acceptance claim.

## Repository/pipeline reference draft and traceability — 2026-10-18

Added the Product Owner-requested repo_layout.md draft in E.1, recording the shared repository, component/change boundaries, private areas, integration/capture model, source locations, immutable artifacts, qualification/promotion, patch/rejection paths and remaining proofs. PBI-017 tracks final consolidated-document delivery as an unscheduled Proposed item; the draft does not complete that item. Added reciprocal navigation with README, SRS, architecture, test profile, deployment procedure, current design, operator manual, walkthrough and results.

Added the general document-connection requirement to the local materialization policy: descriptive links, reciprocal references, stated authority, synchronized changes and validation, while preserving historical evidence and canonical backlog format. The canonical method submodule and other sprint artifacts are unchanged. Documentation-only work; no runtime operation is implied. The [draft](repo_layout.md) identifies current implementation sources and evidence limitations.

## Resume C after leaving restricted verification — 2026-10-18

The existing stage-directory guard correctly refuses reinstalling an attempted C stage, but offered no continuation after leaving browser verification. Added C-only --resume-verification: require B completed, retained C payload and no C done marker; recover only the same owner/task/base and common generation for all three reservations; verify effective identity, complete initial assembly and exact restricted-verification status/reason. It repeats no installation or acquisition. Ownership is checked again before publication. A mismatched/completed checkpoint stops; this is not recovery from arbitrary failed import or an interruption after publication.

Updated C guidance, the operator manual and repository draft together; retained the Product Owner's grouped actor substeps. The regular fresh-run refusal now points to the bounded option. [Native continuation evidence](tests/c_resume_verification_20261018.txt) reaches the browser pause and quits with 130 without publishing. Final state remains available only to VERIFIER pending the Product Owner's checks. Full application/release controllers and immutable archives remain unchanged.

## Retry missing C runtime verification — 2026-10-18

Kept the Product Owner's exact Hello World by VERIFIER assertion. A missing snapshot is now a specific VERIFICATION NOT PASSED outcome and repeats the browser prompt instead of exiting C. Existing entries can be reused; q retains the restricted checkpoint. Unexpected Oracle/connection or malformed-result errors still stop, and the final publication transaction rechecks ownership and the original assertion. The C-only loop performs a read-only assertion query before publication; it creates no data. Rehearsal fails rather than looping indefinitely on a missing fixture. Error text names the assertion and expectation explicitly.

Updated main/operator guidance and test profile together. Focused control-flow tests cover missing-then-present, quit and unexpected SQL failure. Native read-only evidence uses an explicit missing-row condition followed by the current real snapshot; browser interaction/publication are outside that test. Release archives/controllers, other sprint artifacts and managed statuses are unchanged.

## D qualification sequence and Packager/Deployer model — 2026-10-18

Expanded D into fifteen numbered operations, distinguishing archive inspection, target status/admission, database migration, APEX import, automated checks, restricted verification preparation, actual browser checks, guarded publication, receipt/live fingerprint and ordinary-account checks. The D script prints the chapter and its final password/account steps; comments map its helper call to the numbered operations. No release-controller or qualification behavior changes.

Adopted the Product Owner's editable model.drawio, corrected the World/Hello dependency and direct export-to-TEST implication, and added lifecycle and detailed D qualification pages. Retained the user's original backup drawing as a historical page. Development team/Packager performs C smoke testing and releases the reviewed package; Deployer takes the same bytes through qualification and TEST promotion. VERIFIER/LAB_USER remain runtime accounts. Updated SRS A-02/A-03 role labels and UC-4 handoff, current PBI-011.6 design, repository draft, main guide and operator manual consistently. Existing PBI-011/012 and UC-4/11 traceability are explicit; no new backlog scope or sprint assignment.

Native draw.io export and visual inspection passed for the lifecycle and D qualification pages after layout corrections. XML cell/edge/link checks, D local preflight, Bash syntax and documentation checks pass. This is model/operator-guidance refinement, not another D deployment or new browser/release acceptance. Current qualification failure/continuation limitations remain documented.

## Rename release areas to integration_test and user_acceptance_test — 2026-10-18

By Product Owner direction, renamed the public environment/connection keys to integration_test and user_acceptance_test, and the actual workspace/schema identities to E1_INTEGRATION and E1_UAT. Application IDs remain 810004/810005. Old script target tokens are normalized as compatibility aliases; direct SQLcl uses the new saved profiles. Updated configuration, provisioning/reset/isolation, controller/operator checks, fixtures, manuals, model and SRS/architecture terminology. Qualification remains the validation activity; successful UAT deployment is not Product Owner acceptance.

The Product Owner explicitly chose to stop the paused old D attempt and rebuild these areas. Preserved its native export, table rows, old configuration and control rows in protected local evidence; retired epoch 1 through the old public API with a reason. Recreated only the two areas, keeping A/B/C and control attempt history. The old E1_QUALIFY attempt is failed; the new integration target retains epoch 1/new and UAT remains epoch 0/new. No integration/UAT application is currently installed. D's old host attempt directory is archived so D can start anew.

Kept the old immutable 1.0.0/1.0.1 archives. Built new mapping archives from local source revisions 08a5cf27e8a31ff7b77b6fd694f673847726eda1 and ee8f1af8e35f81bb3b75051243df2ab9c6e4c0e5, with hashes d99fe83ec3d149739a12ec0cf2f01081ae027d1ec015e16d5a971ff3c602ab45 and 4ba3abb8709f256c7a47e3e9294d3e7303f742145a95cb58d808ca6c6bcf7200. Initial candidate reran native composition/history tests on retained C. Patch APEX/db are byte-identical to the previous accepted patch; its candidate explicitly reuses that immutable functional evidence plus new identity/control checks rather than pretending C was upgraded. Both new archives remain unqualified: D and F must obtain new receipts before UAT promotion. The incompatible proposal now names the selected new patch as its base.

[Rename evidence](tests/environment_rename_20261018.txt) covers exact identity checks, retained history, missing-qualification UAT rejection, candidate/build checks and scope limits. The artifact/controller source revisions changed deliberately; the original archives were never edited. No full new delivery or acceptance is claimed.

## Complete current integration_test naming — 2026-10-18

Renamed the D runner to scripts/cicd-walkthrough-D_integration_test.sh and its stage token to D_integration_test; renamed the integration-test wrapper and fixture too. Updated current scripts, operator chapters, model and related product documents together. Carried the completed local D marker forward to the new token so E can proceed without reinstallation. Immutable archives/controllers and historical evidence retain their original identifiers.

The existing selected initial archive passes the read-only integration_test result check: complete 1.0.0, ready state and live APEX fingerprint match. Current readiness now reflects completed D and pending E. No deployment or data fixture was rerun.

## Initial UAT verification continuation and release prompt retry — 2026-10-18

E now accepts --resume-verification only for an incomplete retained stage with matching initial archive, owned epoch, restricted 1.0.0 application and exact initial root verification state. It reruns archived integrity/rollback unit checks and returns to the browser prompt. No new admission, migration, import or reset is performed. Final publication remains the original archived controller/SQL; archive bytes are unchanged.

D/E/F now check the exact VERIFIER Hello World assertion before publication and repeat only for missing browser data. Unexpected SQL errors stop. The existing C behavior is retained. Operator guide, manual, repository draft and test profile describe the same boundary. UAT remains restricted awaiting the user's browser example, not successfully promoted.

## Preserve settings during post-publication upgrade examples — 2026-10-18

Corrected the UAT history fixture to select existing active Hello/World entries explicitly instead of relying on saved defaults. A valid manually selected greeting does not require both defaults. The fixture preserves configuration and prior history; missing active entries or incompatible prefixes give a fixture-specific error. No application source, migration or immutable release archive changes.

Added E --resume-examples for an incomplete stage after successful initial publication. It validates the ready archive/live fingerprint, returns to the LAB_USER result pause, and completes examples/baseline capture without republishing or reinstalling. An existing baseline is compared rather than overwritten. The script now explains this continuation if example preparation fails. Main guide/readiness, operator manual, repository draft and test profile are synchronized. UAT is published; example preparation remains for the operator to finish.

## One drift command for clean, manual and synthetic cases — 2026-10-18

The operator's drift check now reports NO DRIFT for a specific successful preflight, or DETECTED DRIFT for the specific nonzero fingerprint rejection. Both recognized outcomes require unchanged target/control snapshots. Unexpected SQL/tool errors or missing expected output still fail. The underlying immutable archive/controller and deployment guards are unchanged. Compatibility continues to require its exact rejection.

H's automated replay asserts --expect-clean before injection, --expect-drift after injection and --expect-clean after restoration; a failed fixture cannot pass as a clean observation. The main guide presents the same command before editing, after a real Page Designer change and after synthetic change, with restoration between cases. Updated operator manual, test profile and design notes. Refreshed current readiness using completed F and native clean-patch evidence. Broader drift/concurrency/repair scope is unchanged.

## Inspect manual drift and choose restoration — 2026-10-18

Added cicd-drift-diff.py as a read-only UAT/APEX review tool. It verifies selected archive/member/source/configuration identities against the successful receipt, saves the unchanged archived source and a native split live export, checks stable receipt/fingerprint during capture, prints page Title/region Name differences and writes full review/raw diffs. The shorter report omits only target import-offset lines and generated Manifest comment blocks; other differences remain visible. It changes neither target nor Git and has no restoration action.

H.1 now follows detection with source review, explicit keep/undo decision and manual restoration of all edited published property values, including a changed region Name. The original published fingerprint remains the restoration acceptance gate. Keeping an edit instead requires reviewed Git reconciliation/new release; no silent baseline adoption. Guide/readiness, operator manual, test profile and design notes are synchronized. This remains the selected page-drift slice, not a general SQL comparison or repair platform.

## Show source differences through the regular drift command — 2026-10-18

Added --show to cicd-protection-check.sh drift. After a recognized drift rejection and unchanged target/control snapshots, it calls the internal read-only source review; a clean target reports no unexpected changes to display. Review errors propagate and never restore content. Existing expected-outcome flags can be combined with --show, while invalid/duplicate/conflicting options reject before Oracle operations. H.2 uses --expect-drift --show and preflights the helper's presence. Main guide, operator manual, design and test profile use the regular shell entry point; immutable controller/archive bytes are unchanged.

## Product Owner handover materials — 2026-10-18

Prepared the canonical [23-slide presentation](sprint_E.1_increment_demo.pptx), [guided presentation walkthrough](sprint_E.1_increment_demo.md), [handover](sprint_E.1_handover.md) and [completion assessment](sprint_E.1_assessment.md). The deck uses editable adaptations of existing draw.io lifecycle/integration diagrams and a native semantic-version comparison table. Frozen figure data and the builder preserve its source baseline without editing the working model.

The package follows infrastructure/onboarding, A–C assembly, Git-built archive integration/promotion, compatible Hello patch and preservation, incompatible proposal rejection, manual drift/source review and restoration choice. It explicitly identifies incomplete concurrency/fencing/schema-drift/repair proofs and recommends focused further Elaboration. PBI-011–016 traceability links and maintained document backlinks connect the materials without changing managed statuses or claiming parent completion. No application deployment or restoration is performed by this documentation increment.

## APEX interface explanation in the presentation — 2026-10-18

Added slide 7 explaining the actual application-definition interfaces: SQLcl apex export, supported APEX_APPLICATION_INSTALL target mapping, native exported install.sql and APEX_EXPORT.GET_APPLICATION fingerprinting. Separate Liquibase migrations own schema changes; App Builder authors definitions and ORDS serves HTTP. Working Copies/Team Development are not the release integration/promotion mechanism. The presentation now has 24 slides; guided slide references and handover are synchronized. No runtime or architecture decision changes.

## Git layout, cooperation and future pipeline section — 2026-10-18

Added four presentation slides covering the actual shared repository layout, proposed task-branch cooperation, text-based APEX export merging and a future CI/PR pipeline around existing gates. The 28-slide deck distinguishes current sequential snapshot replay from unproved parallel capture/integration and hosted automation. Expanded the linked repository draft with merge review/validation and future pipeline guidance; synchronized guided slide references and handover. No Git merge behavior, source attributes, live pipeline or runtime is changed.

## Review fixes increment 1 — 2026-10-18

[BUG-2–5](sprint_E.1_bugs.md) fix release-input acquisition, infrastructure error status, pre-SQL configuration validation and complete test-source cleanliness. Added exact historical recipe reconstruction from Git/original evidence with member/final hashes, conflict protection and explicit operator documentation. Input replay never claims a new test. Configuration is validated before secret access/connection and bounded to the implemented controller mappings. SQLPlus infrastructure failures now use EXIT FAILURE. Candidate/package scope includes the complete tests tree. Existing archives, retained UAT and other Podman resources remain unchanged.

[Evidence](tests/review_fixes_20261018.txt): eight focused Python cases, 24 Python regressions, local preflight, native SQLPlus failure probe and all five native identity/cross-area isolation checks. Stable replacement identity and bounded additive repair remain BUG-6/7, not completed by these changes. [Selected review decisions](sprint_E.1_review-1-decisions.md) keep work within existing E.1 scope.

## BUG-6 importer identity correction — 2026-10-18

Replacement imports verify application/workspace ownership and read the existing offset via public APEX export before SET_OFFSET. Fresh imports retain GENERATE_OFFSET. Native C experiment migrated Hello to 1.0.1, preserved business fields and a private saved report across two imports, compared region/report IDs and rejected a wrong-workspace app before import. C's ordinary availability/reservation was restored; UAT untouched. [Evidence](tests/apex_identity_20261018.txt). A new corrected patch archive remains required before closing BUG-6; historical archives retain their old code.

## BUG-6 corrected delivery input and BUG-7 construction — 2026-10-18

Candidate checks at 0cc6c68 pass against C and the corrected stable-offset patch archive 80b51f1e…d92d583 is built. Native disposable integration testing passes fresh and from the retained initial artifact, preserving all fields of 21 baseline rows/settings. The new versioned patch recipe makes that archive reproducible from a full checkout. The existing UAT artifact/pointer and manual drift are retained; no claim of new-byte UAT promotion.

Added bounded integration-only recovery authority, two immutable Git-source artifact kinds, atomic operator steps and negative/tamper test specifications under existing PBI-011.8. The authority/observer compile natively and archive integrity tests pass; actual committed-DDL failure/repair qualification still follows. PBI-011.8 moves to under_construction following the Product Owner's selection, not tested or completed. This is prototype construction evidence, not closure of BUG-7.
