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
