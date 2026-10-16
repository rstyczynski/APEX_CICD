# E.1 — Prototype construction

## Current increment

Status: under_construction

The approved first slice constructs the application from scratch, delivers an initial release and compatible Hello patch, then demonstrates rejection of an incompatible Foundation upgrade and unexpected live APEX drift. The [design](sprint_E.1_design.md) retains the broader concurrency/recovery work for later selection. This document is maintained during construction; pending work is not presented as delivered.

## PBI-011.1 — Tools, platform and private areas

Implemented checksum-pinned private SQLcl 25.3.0.274.1210 and Temurin Java 21.0.12.1+1 provisioning in scripts/cicd-tools.sh. Tools remain under the ignored .local-apex directory; host Java and user-level configuration are unchanged. SQLcl uses a project-local connection store, protected saved connections, disabled command history and credentials sent through standard input rather than process arguments. scripts/apex_sql.py redacts known secrets from failures and requires a server-side completion marker.

Reused the running apex-cicd VM and its existing database/APEX/ORDS installation. Observed host headroom is now approximately 63 GiB, with 18 GiB free in the VM. The shared docs/deploy.md is maintained by E.1; its runtime-removal sequence preserves host credentials/downloads/evidence. No VM teardown has been necessary for this increment.

config/areas.json declares private A/B/C schemas/workspaces/application IDs, one disposable qualification area and retained TEST. scripts/cicd-platform.py collision-checks before provisioning, records owned resources locally, creates ordinary developer/runtime identities through public APEX APIs and saves dedicated schema connections. It bootstraps E1_CTRL separately from application Foundation. Ordinary identities have no grants on another area's tables.

Executed results: all five named connections match their effective schema, FREEPDB1 and workspace association. Cross-area table reads and writes were rejected for all five areas. Recreated only E1_QUALIFY through the public workspace-removal/provisioning path; a separately committed TEST marker survived. Current isolation/preservation tests are being rerun through the registered test entry point after the SQLcl wrapper fix below. The existing platform verifier passes database/APEX registry checks, host-port authentication, ORDS/APEX HTTP routes and static asset version checks.

## PBI-011.2 — Control ownership

Implemented deploy/control.sql and scripts/cicd-task.py. The control schema stores component reservations, authenticated schema owner, task/base/generation and append-only acquisition/release events. A short NOWAIT coordination transaction acquires the complete requested scope or rolls back; committed reservation rows survive connection closure. Only registered A/B/C schemas may invoke the ownership package; they receive package execution rather than authority-table DML grants.

Executed result: A acquired Foundation for foundation-initial with ownership generation 1. A later SQLcl process verified that ownership before applying Foundation. The task remains held while the initial source baseline is completed. Parallel acquisition, reassignment and exhaustive negative ownership tests remain pending and are not claimed from this sequential run.

## PBI-011.3 — Foundation-first assembly

Implemented db/changelog.xml and immutable changeset 001-foundation. It creates component presence/version records, greeting-history snapshot storage and application/component operational states. Foundation is 1.0.0; Hello and World are explicitly not installed with no invented version. Root application state remains maintenance. No Hello/World business data was seeded.

Executed the changeset with SQLcl's bundled Liquibase 4.30.0 through deploy/foundation.sql. Liquibase validation and installation succeeded. Assertions verified Foundation's installed version, absent Hello/World and blocked application state.

Created application 810001, APEX Delivery Laboratory, from scratch through App Builder in E1_DEV_A. It currently contains the generated global, home and login pages only. Set native availability to unavailable during assembly using public APEX_APPLICATION_ADMIN. Application version display, component pages and the complete runtime guard still need construction.

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

Run from the repository root. The existing scoped Oracle/APEX runtime and protected .local-apex/credentials.env are prerequisites; provisioning uses its administrator credentials only for platform setup. Ordinary checks use the saved schema connections.

```bash
bash scripts/cicd-tools.sh
python3 scripts/cicd-platform.py check
python3 scripts/cicd-platform.py isolation
bash tests/run.sh --smoke --new-only progress/E.1/platform_tests.manifest
```

Expected results are the pinned SQLcl version, successful target-identity checks, denied cross-area access and a final zero-failure smoke summary. scripts/cicd-platform.py bootstrap provisions the declared owned areas; reset-qualify destroys/recreates only the disposable qualification area. Run neither against an altered mapping without inspecting the existing owned inventory. The full tests/run.sh --unit and --integration suites still contain explicitly pending implementation.

## Next construction steps

Complete the platform checks and audit its adopted sources, finish Foundation's versioned source baseline and ownership handover, then validate supported imports into the private B/C areas. Build the component pages and greeting/history flow next. Keep source commits, migrations, component versions, artifact hashes and installed fingerprints distinct throughout release construction. Commit completed increments after their audits; no remote push is authorized.
