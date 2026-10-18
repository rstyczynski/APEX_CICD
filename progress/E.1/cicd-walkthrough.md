# E.1 — Use-case walkthrough: deployment results and protection

## Contents

Use these links to move between preparation, delivery and protection demonstrations.

- [What this walkthrough shows](#what-this-walkthrough-shows)
- [Deep dive](#deep-dive)
- [Applied tools and techniques](#applied-tools-and-techniques)
- [Alignment with selected Elaboration use cases](#alignment-with-selected-elaboration-use-cases)
- [Current readiness](#current-readiness)
- [Run the results walkthrough](#run-the-results-walkthrough)
- [Run one chapter at a time](#run-one-chapter-at-a-time)
- [Prerequisites and infrastructure precheck](#prerequisites-and-infrastructure-precheck)
- [Initialize the Podman host](#initialize-the-podman-host)
- [Prepare a repeatable walkthrough](#prepare-a-repeatable-walkthrough)
- [Install the fresh database and APEX](#install-the-fresh-database-and-apex)
- [Initialize project delivery control](#initialize-project-delivery-control)
- [Provision each assigned area](#provision-each-assigned-area)
  - [A/B/C — private development areas](#abc--private-development-areas)
  - [integration_test — disposable release validation](#integration_test--disposable-release-validation)
  - [user_acceptance_test — retained release demonstration](#user_acceptance_test--retained-release-demonstration)
- [Configure each developer environment](#configure-each-developer-environment)
- [Check project readiness before A](#check-project-readiness-before-a)
- [A. Deliver Foundation](#a-deliver-foundation)
- [B. Deliver Hello](#b-deliver-hello)
- [C. Deliver World and complete the assembly](#c-deliver-world-and-complete-the-assembly)
- [D. Qualify the initial release](#d-qualify-the-initial-release)
- [E. Promote the same initial artifact to user_acceptance_test](#e-promote-the-same-initial-artifact-to-user_acceptance_test)
- [F. Deliver the compatible Hello patch](#f-deliver-the-compatible-hello-patch)
- [G. Reject an incompatible database upgrade](#g-reject-an-incompatible-database-upgrade)
- [H. Reject deployment over unexpected live change](#h-reject-deployment-over-unexpected-live-change)
- [Destroy the lab after the walkthrough](#destroy-the-lab-after-the-walkthrough)
- [Maintain this artifact](#maintain-this-artifact)

## What this walkthrough shows

Follow one application from an empty lab to a working release, then see which incorrect deployments the pipeline blocks.

- This lab simulates work of 3 developers (identified as A, B, and C) dedicated to development of APEX style Hello World application architected as composition of three components: database and two user facing ones.
- The Product Owner sees application outcomes after successful deployments and evidence that wrong deployments are blocked.
- Developer A/B/C operations run inside the guided stages. The Product Owner does not inspect App Builder, page definitions, SQL source or Git diffs in this workflow.
- Show the actual operation output and a short result: **DEPLOYED**, **REJECTED**, **ERROR** or **PENDING**.
- After a successful deployment, show its result in the running application at the printed URL.
- After an expected rejection, show the exact reason, verify the target was not overwritten, then open the application to demonstrate that its prior behavior and saved history remain intact.

## Deep dive

For the shared repository, private branches/areas and pipeline paths behind these steps, read the [repository and pipeline draft](repo_layout.md). Keep it synchronized with this walkthrough and its linked architecture/operator sources.

This business-level walkthrough, its [launcher](../../scripts/cicd-walkthrough.sh), the A–H chapter scripts below and the [detailed operator guide](user_manual.md) describe one system. Maintain and review them together as **one artifact**.

## Applied tools and techniques

The deployment has two kinds of source: **APEX application definitions** and **database migrations**. Git keeps both together. Operators use small shell scripts and visible SQLcl commands to assemble and check one application in each target. The working development assembly demonstrates this approach; initial delivery and the compatible Hello upgrade execute verified archives; the selected incompatibility and page-drift rejection scenarios now have executable demonstrations.

### Toolchain and responsibilities

These tools cover authoring, database changes, release delivery and the supporting local lab.

1. **Oracle APEX 24.2 App Builder** authors pages and shared components. **ORDS** serves their browser URLs. A save in App Builder changes the live development application; capture and Git review are separate operations.
2. **SQLcl 25.3 with Java 21** connects through private saved connections, runs explicit SQL/PLSQL and performs native APEX export/import. Capture uses split files, original component IDs, no export date and no supporting-object installation. Oracle-generated export files are executed unchanged. Public APIs such as **APEX_APPLICATION_INSTALL** map the source to a target workspace/schema/application; **APEX_APPLICATION_ADMIN** controls native availability.
3. **Oracle Database and PL/SQL** hold component data, configuration, installed versions and immutable greeting snapshots. Database constraints, packages and triggers enforce the business rules even when a caller bypasses the browser. A separate **E1_CTRL** schema keeps managed task ownership outside ordinary application migrations/imports.
4. **Liquibase through SQLcl** applies ordered database changesets and records their identities/checksums in **DATABASECHANGELOG**. An applied migration is retained unchanged; a later correction needs a new changeset. The application export and database migrations remain distinct parts of the same reviewed source revision.
5. **Git** identifies the reviewed source commit and shows the component diff. Foundation is established first; Hello and World are integrated from bounded private work. The replay uses reviewed sequential B/C source snapshots; it does not simulate new authoring. Durable task reservations record owner, task, base commit and generation; they are separate from the durable initial-release ownership controls.
6. **Bash, small Python standard-library helpers and SQL assertions** expose operator stages, handle files/connections and check outcomes. The results script pauses at runtime URLs; the detailed operator guide explains individual commands. Credentials stay in protected local storage, outside Git and release contents. Repository positioning comes from Git discovery.
7. **Podman** runs the local Oracle Database and ORDS containers. Separate database schemas, APEX workspaces and application IDs provide A/B/C development areas, disposable integration_test and retained user_acceptance_test on the same host. This is logical isolation; it does not model independent production hosts. Infrastructure lifecycle operations follow [deploy.md](../../docs/deploy.md).

### How delivery is organized

The pipeline turns reviewed source into a verified release through these explicit stages.

1. **Prepare and identify the target.** Check the effective database user, PDB, workspace and application mapping before writes. Reserve the declared component work before managed authoring. Keep Foundation-only and incomplete assemblies unavailable.
2. **Capture and review source.** Export native APEX definitions, review the declared component changes and inherited/shared definitions, run candidate checks, then commit the accepted source. Repeated unchanged exports must match; a live development application is not itself a release artifact.
3. **Build once.** Package the accepted Git revision, migrations, deployment SQL and nonsecret manifest. Record the source commit, supported starting state, component dependencies, tool/configuration versions and the archive's **SHA-256**. Qualification and promotion must execute files from that verified archive rather than a changing checkout.
4. **Qualify, then promote the same bytes.** Reconstruct and test in the disposable area first. Retained user_acceptance_test may receive only the identical qualified artifact for its supported starting state. The selected patch must also qualify against its declared earlier baseline; successful fresh installation alone does not prove an upgrade.
5. **Verify before publishing.** Development verification already uses native restricted access for **VERIFIER**, followed by integrity/browser checks and a separate publication operation. The release design additionally requires persistent attempt ownership, maintenance fencing, final live fingerprints and a receipt before readiness. The initial release now uses persistent attempt ownership, an external runtime gate and a final fingerprint. Native availability is prepared while the external gate still restricts business requests; successful receipt and external readiness commit together. Guarded mutation admission and ordinary-request blocking passed for the patch; complete read/asynchronous request draining and stale-verifier fencing remain unproved.

### How correctness is checked

These checks establish whether the intended release is compatible, correctly installed and safe for the retained data.

1. **Isolation and identity:** actual cross-area read/write denial tests supplement configuration inspection. A correct application sent to the wrong schema still fails the target check.
2. **Dependency and version rules:** Foundation must precede its dependents, and installed components must form a supported complete combination. Semantic versions describe contracts: the compatible Hello correction advances **1.0.0 → 1.0.1**; a breaking Foundation change requires compatible dependents. Version labels alone do not establish compatibility. The Foundation 2.0.0 proposal is rejected because its dependents still require Foundation 1.0.0.
3. **Behavior and retained data:** Oracle unit assertions check exact greeting composition, defaults, explicit selections, prefixes, Unicode, limits and rejected input. Snapshot tests check that changed configuration affects new greetings while old snapshots remain unchanged, and that history update/delete is rejected. Browser checks exercise the actual runtime as verifier and ordinary user.
4. **Repeatability and failure reporting:** cleanup is an explicit separate destructive step for this disposable demonstration. During the actual patch, field-level baseline comparisons preserve this cycle's earlier rows/settings. Scripts check Oracle errors and successful completion markers, stop on unexpected failure and show the reason. A failed connection or arbitrary error is not evidence that a bad deployment was correctly rejected.
5. **Traceability and drift:** a Git commit identifies source; a semantic version describes its contract; an archive hash identifies exact packaged bytes; a recomputed live APEX fingerprint detects changed application definitions; schema checks cover the declared migrations and component versions. These serve different purposes. The selected drift scenario rejects a changed Home title/banner before maintenance, migration or import and leaves the changed page/history intact until explicit restoration. A matching hash alone does not prove functional correctness.

The [current verification evidence](sprint_E.1_tests.md) supports development, repeatable preparation, both release paths, preserved settings/history and the two selected rejection scenarios. Complete request draining/fencing, concurrency and automated failed-deployment repair remain unproved. Correctness is established by the checks actually passed for the stated scope; this chapter does not turn the [accepted design](sprint_E.1_design.md) into a completed guarantee.

## Alignment with selected Elaboration use cases

This chapter connects each demonstration to the accepted use cases and makes the remaining coverage gaps visible.

- This is an **end-to-end use-case walkthrough** of the selected E.1 slice. A/B/C stages organize the journey; the Product Owner sees application results and deployment protection.
- The [SRS use cases](../../docs/srs.md#use-cases-and-success-criteria) define actor goals and success criteria.
- The [accepted E.1 design](sprint_E.1_design.md#first-implementation--happy-path), its DevOps section and its two selected unhappy scenarios define the implementation selection.

1. **A / Foundation:** UC-9 task preparation, UC-10 source capture, UC-7 review/integration, UC-1 Foundation assembly, UC-4 controlled delivery and UC-11 verification. The first assembly remains blocked until dependents exist.
2. **B / Hello and C / World:** UC-9 → UC-10 → UC-7 → UC-4 → UC-11, executed sequentially in the first slice. Developer and reviewer decisions stay explicit even though their technical operations are grouped inside the stage.
3. **Use the completed application:** UC-2 component configuration and UC-3 greeting/history, followed by UC-11 delivery verification.
4. **Qualify/promote and compatible Hello patch:** UC-4 delivery plus UC-1's supported upgrade checks, UC-2/3 behavior/history and UC-11 verification. Qualify/promote identical bytes; preserve settings/history through Hello 1.0.0 → 1.0.1.
5. **Reject an incompatible Foundation upgrade:** the incompatible-target alternative in UC-1 and failed-check protection in UC-4. The expected outcome is rejection before writes, with the working target unchanged.
6. **Reject unexpected live drift:** UC-4's stop-before-overwrite alternative and UC-5's drift-detection entry. Demonstrating rejection does not complete UC-5's reconciliation/repair flow.

- **Prerequisites:** provisioning/onboarding from UC-8 and the separate infrastructure/operator procedures. They are not repeated as Product Owner technical inspections here.
- **Reproduction:** this guide contributes to UC-6; its full success criterion is not met by an unattended runner execution.
- **Later evidence outside this selected walkthrough:** parallel Hello/World work, the competing Hello race and other reservation alternatives in UC-9; deployment races/interruption; failed additive deployment and automated repair in UC-5. These remain in the broader design.
- **Unselected:** UC-12 adoption of an existing application. This prototype creates the application from scratch without constructing a supplied seed application.
- **Execution status:** this mapping describes intended coverage, not passed acceptance. A/B/C development checks and runtime checkpoints execute. New initial receipts remain verifiable after upgrade; the patch and two selected rejection stages execute. Broader use-case alternatives remain pending.

## Current readiness

This checkpoint describes the delivered lab state and the boundaries of what has been demonstrated.

- **Delivered checkpoint:** A/B/C development work is retained. The renamed integration_test/E1_INTEGRATION and user_acceptance_test/E1_UAT areas are empty and separately provisioned; D must start a new attempt using the newly selected archive. The old interrupted D attempt was retired and preserved; it is not qualification evidence for these new mappings. When restarting from cleanup, follow every infrastructure and onboarding chapter below before A. The earlier A–H rehearsal remains historical evidence.
- This walkthrough now starts with explicit prerequisite checking, Podman host preparation, complete lab cleanup and fresh database/APEX/ORDS installation.
- Cleanup destroys **all database state in this lab**, including A/B/C, qualification, user_acceptance_test, entries, settings, greeting history and database control receipts. Host credentials, tools, reviewed source/release archives and historical evidence remain available; unrelated Podman resources are preserved.
- Infrastructure installation ends with **only Oracle Database/APEX/ORDS**. It creates no E1_CTRL, developer/target schemas, project workspaces or developer accounts. Project control and named-area provisioning follow separately.
- A–C install the reviewed Foundation, Hello and complete World snapshots. A/B remain unavailable while incomplete; C starts at **1.0.0**.
- D/E execute real qualification and promotion of the **same initial artifact** in this cycle. F qualifies Hello **1.0.1** both fresh and over 1.0.0, then upgrades user_acceptance_test with those identical bytes, preserving only the data created during this cycle.
- G/H demonstrate the selected rejections and explicit controlled page restoration. Rehearsal uses clearly identified NEW runtime test examples and skips human browser viewing.
- Broader E.1 concurrency, complete maintenance fencing, schema-drift coverage and failed-additive-deployment repair remain open. This walkthrough does not close the sprint.

## Run the results walkthrough

Start here for the complete Product Owner journey: prepare a fresh lab, run each stage and view its application result.

1. Open a Bash terminal inside the checkout and position at its root:

   ```bash
   cd "$(git rev-parse --show-toplevel)"
   ```

2. Follow **Prerequisites and infrastructure precheck**, then **Initialize the Podman host** below.
3. Follow **Prepare a repeatable walkthrough** to destroy the current lab, then **Install the fresh database and APEX**. Complete the separate project control, named-area provisioning, developer configuration and readiness chapters. Wait for each PASS before continuing.
4. Start **A — Foundation**:

   ```bash
   bash scripts/cicd-walkthrough-A_foundation.sh
   ```

5. Read the actual operations and output. Press a key to proceed, or **q** to stop. On a failure, stop and inspect it before another operation.
6. At a verification checkpoint, use the printed URL as **VERIFIER**. After publication, use **LAB_USER** to see the result. Retrieve the account password with `python3 scripts/cicd-password.py VERIFIER` or `python3 scripts/cicd-password.py LAB_USER`.
7. After A reports PASS, run B using its chapter command. Continue through C–H the same way.

- A–F now install/deploy, rather than only display an earlier result. Repeating an already attempted construction chapter stops for inspection. C provides an explicit resume command only for its restricted-verification pause; other partial states require inspection. Start a new demonstration with the explicit infrastructure destruction/install sequence.
- **--preflight** on A–H checks local tools/files/chapter mapping without connecting to Oracle. It does not substitute for the infrastructure precheck below.
- **--rehearse** executes real installations, qualification/promotion and the user_acceptance_test page fixture without pauses. Its explicit runtime API test examples are not browser verification. It requires the fresh infrastructure preparation first.
- Normal release result inspection remains read-only through the separate operator result commands. No App Builder inspection is required in this Product Owner journey.

## Run one chapter at a time

Run each stage separately so you can pause, review the outcome and continue only after success.

1. Complete infrastructure installation, then explicit project control, named-area provisioning, developer configuration and readiness below once for this cycle.
2. Execute A–H in order. Each chapter contains its exact command, actual operation output, expected outcome and runtime URL.
3. Each script stops on errors. Do not advance after a failed or interrupted attempt; retain its transcript and inspect ownership/partial state. C can resume its documented restricted-verification pause. Full destruction is a separate deliberate restart of the demonstration, not deployment repair.

- A: `bash scripts/cicd-walkthrough-A_foundation.sh`
- B: `bash scripts/cicd-walkthrough-B_hello.sh`
- C: `bash scripts/cicd-walkthrough-C_world.sh`
- D: `bash scripts/cicd-walkthrough-D_qualification.sh`
- E: `bash scripts/cicd-walkthrough-E_promotion.sh`
- F: `bash scripts/cicd-walkthrough-F_hello_patch.sh`
- G: `bash scripts/cicd-walkthrough-G_incompatible_upgrade.sh`
- H: `bash scripts/cicd-walkthrough-H_drift.sh`

The optional launcher calls those same scripts in order **after** infrastructure and project onboarding:

```bash
bash scripts/cicd-walkthrough.sh
```

- [The common helper](../../scripts/cicd-walkthrough-common.sh) prints chapters, pauses and SQL checks, and sequences the repeated native release operations. Actual controllers remain `cicd-release-step.sh` and `cicd-patch-step.sh`; they execute SQL from verified archives.
- H's interrupted fixture is restored explicitly with `python3 scripts/cicd-drift-demo.py restore`. Ordinary result checks never silently restore it.
- [The detailed operator guide](user_manual.md) and [operator runner](../../scripts/cicd-operator-walkthrough.sh) retain the atomic commands. Historical transcripts retain the filenames/state from their original execution.

## Prerequisites and infrastructure precheck

Check that tools, installation inputs and host resources are ready before changing or destroying the lab.

Run this **before cleanup**:

```bash
bash scripts/cicd-walkthrough-prerequisites.sh
```

1. Check macOS Apple Silicon and the presence of Git, Podman, Python 3, curl, OpenSSL, unzip, shasum, tar, rg, launchctl and signing/helper tools.
2. Check the pinned local **SQLcl 25.3 / Java 21**, helper and APEX 24.2 archive; verify installer/tool archive checksums and show actual versions.
3. Verify both retained reviewed release archives and the accepted Foundation/Hello Git snapshots. These are deployment inputs, not saved business data.
4. Inspect named Podman machines, owned resource inventory and host disk space. If a named healthy database already exists, show its actual APEX registry version/status; absent/stopped/partial infrastructure is reported explicitly. Wait for **PASS prerequisites**.

- A missing prerequisite or checksum failure stops before destructive cleanup. Install missing inputs using [deploy.md sections 1–4](../../docs/deploy.md#1-open-the-operator-terminal-and-inspect-resources) and `bash scripts/cicd-tools.sh`, then rerun the check.
- This precheck does not require a running database and does not install applications or erase anything.

## Initialize the Podman host

Prepare the local container engine and Oracle images that will run the database and web gateway.

```bash
bash scripts/cicd-walkthrough-host.sh
```

1. Create **apex-cicd** only if absent; otherwise reuse it.
2. Start the named engine using the established local helper/launch procedure if stopped.
3. Inspect the engine/resources and pull the pinned native ARM database and ORDS images.
4. Wait for **PASS host**. If another VM prevents startup, stop here and follow [deploy.md](../../docs/deploy.md#3-create-and-start-the-vm--fresh-setup-only); this script does not stop/remove unrelated VMs.

## Prepare a repeatable walkthrough

Discard the previous lab installation and all its data so the next demonstration starts from an empty system.

Run the scoped **destructive cleanup** after successful precheck/host preparation:

```bash
bash scripts/apex-destroy.sh
```

1. Read the printed ownership inventory and scope. The script refuses unrelated containers sharing the lab's named volumes/network.
2. Stop/remove **apex-ords** and **apex-db** on connection **apex-cicd**.
3. Remove **apex-data**, **apex-ords-config**, **apex-images**, **apex-net** and **apex-db-password**, when present.
4. Wait for **PASS destroy**. All lab database/APEX state, including greeting history, is gone. Repeating cleanup on an already empty lab is allowed.
5. Continue to **Install the fresh database and APEX**. Do not run A yet.

- The VM, images, host credentials/tools/installers and reviewed release archives remain; unrelated containers, volumes, networks, secrets and VMs are untouched. Historical host evidence is retained separately and cannot pass fresh database receipt checks.
- This replaces the previous settings-only preparation. That optional operation is now named `bash scripts/cicd-demo-defaults.sh`; it preserves history and is not fresh-start cleanup.
- [The scoped destruction procedure](../../docs/deploy.md#12-scoped-destruction-and-fresh-reconstruction) explains the individual commands. Removing the whole VM is not needed to obtain an empty database.

## Install the fresh database and APEX

Build the Oracle Database/APEX/ORDS runtime and verify access. Project accounts, delivery control and applications are initialized in later steps.

```bash
bash scripts/cicd-walkthrough-apex-init.sh
```

1. Refuse existing database/APEX containers or volumes. This is a fresh installation, not a restart or recovery command.
2. Retain existing host credentials, or generate them only if absent. Create the named network/storage and start Oracle Database; wait for its real health check.
3. Copy and extract the verified APEX archive. Install in **FREEPDB1**, then configure the APEX administrator and REST gateway users. Full installer output is in `.local-apex/apex-install.log`; follow it from another terminal with `tail -f .local-apex/apex-install.log`.
4. Install ORDS and matching static assets. Keep `.local-apex/ords-install.log`; wait for the HTTP endpoint.
5. Verify database/APEX validity, host-port connectivity, APEX login and matching assets using `bash scripts/apex-verify.sh`.
6. Wait for **PASS APEX init**: vanilla Oracle infrastructure only, with no project-specific checks or configuration. The separate verification test confirms zero project schemas/workspaces.
7. Continue to the separate **Initialize project delivery control** chapter. Do not run A yet.

- This script cannot call project provisioning or create user-level project schemas. Only required Oracle/APEX/ORDS system accounts are installed. Application construction belongs to A–C after explicit onboarding, with qualification/promotion in D–F.
- If installation fails, inspect its log. Do not blindly rerun APEX installation over partial data. Use the separate scoped cleanup when deliberately restarting from scratch.
- Each native command is expanded in [deploy.md sections 5–9](../../docs/deploy.md#5-create-the-network-volumes-and-database--fresh-setup-only).

### Verify the installation before project setup

Confirm that the infrastructure works through both automated checks and an actual administrator sign-in before preparing project areas.

1. Rerun the automated infrastructure check at any time; it does not install project schemas or applications:

   ```bash
   bash scripts/apex-verify.sh
   ```

   Expected: **APEX 24.2 VALID**, **zero invalid APEX objects**, SYSTEM connected to **FREEPDB1** through the published database port, **ORDS landing: HTTP 200**, **APEX login: HTTP 200**, static assets **24.2**, and a final passed message. The HTTP check verifies the login page; signing in is the next manual step.

2. Retrieve only the APEX administrator password in your local terminal:

   ```bash
   python3 scripts/cicd-password.py APEX_ADMIN_PASSWORD
   ```

   There is **no fixed default password**. Installation generates random passwords on first use and retains the protected `.local-apex/credentials.env` on later destruction/reinstallation. This command deliberately displays one password; keep it out of screenshots, evidence and Git.

3. Open [APEX Administration Services](http://127.0.0.1:8080/ords/apex_admin). Sign in as **ADMIN** using that password. This is the **INTERNAL** administration workspace; if a workspace field is shown, enter **INTERNAL**. Confirm that the administration home opens, then sign out. This verifies an actual administrator login.
4. Check that the sign-in screen and administration home have normal styling/icons. [Static asset version](http://127.0.0.1:8080/i/apex_version.txt) must show **24.2**. Missing styling indicates an ORDS/static-file problem even if a page returns HTTP 200.
5. For an optional direct database login, retrieve the database password, then connect with SQLcl. SQLcl prompts for the password; do not put it in the connection command:

   ```bash
   python3 scripts/cicd-password.py ORACLE_PASSWORD
   source scripts/cicd-env.sh
   sql -nohistory -noupdates SYSTEM@//127.0.0.1:1521/FREEPDB1
   ```

   At the SQL prompt, verify the target and disconnect:

   ```sql
   select user, sys_context('USERENV','CON_NAME') as pdb from dual;
   exit
   ```

   Expected: **SYSTEM / FREEPDB1**. SYSTEM and SYS use the lab's **ORACLE_PASSWORD**; SYS connections require **AS SYSDBA**. Use these administrator accounts for infrastructure/provisioning, with assigned schema accounts for development.
6. Understand the remaining accounts before continuing:
   - **APEX_PUBLIC_USER, APEX_REST_PUBLIC_USER, APEX_LISTENER and ORDS_PUBLIC_USER** are service accounts configured by the Oracle installation. They are not browser/developer logins; leave their credentials to the installation/configuration procedure.
   - **ORDS has no separate human login account** for this verification. It serves APEX over HTTP; APEX authenticates ADMIN.
   - **DEV_A/B/C, LAB_USER, VERIFIER and E1_* schemas/workspaces** belong to later project onboarding. A vanilla installation does not create them. The delivered lab may already have them if the separate onboarding chapters were executed.
7. If a check fails, inspect `.local-apex/apex-install.log` and `.local-apex/ords-install.log`, plus the running container logs:

   ```bash
   podman --connection apex-cicd logs --tail 100 apex-db
   podman --connection apex-cicd logs --tail 100 apex-ords
   ```

   Resolve the failing layer before project setup. A failed verification is not a reason to rerun the APEX installer over an existing database.

## Initialize project delivery control

**E1_CTRL** is the project’s delivery-control schema. It holds component reservations, deployment state and release receipts, and controls runtime access during deployment. Keeping it separate from application schemas preserves coordination and deployment history across application imports. It contains no greeting business data and is created separately from vanilla Oracle infrastructure. See [delivery-control architecture](../../docs/architecture.md#delivery-control-bootstrap) for the design.

**Actor: project/platform operator**, with the lab administrator credential. This is project setup, separate from Oracle infrastructure.

```bash
bash scripts/cicd-control-init.sh
```

1. Create/check **E1_CTRL only**, with its protected operator SQLcl connection.
2. Install ownership and release-control packages. No developer or deployment-target schemas/workspaces/accounts are created. Per-area grants are deferred until the selected area is provisioned.
3. Wait for **PASS project control**, then provision the named areas below.

## Provision each assigned area

Create separate empty work areas for developers A/B/C, disposable integration_test and retained user_acceptance_test. Each area has its own database schema and APEX workspace, allowing work and validation without sharing business data. This is environment preparation under UC-8; no application is installed yet.

The intended delivery flow is:

1. Engineers author changes in their private areas.
2. Capture APEX definitions and maintain database migrations as files.
3. Review and accept those files in Git.
4. Build one release archive from the accepted Git revision.
5. Deploy and verify that archive in qualification.
6. Promote the same archive to user_acceptance_test.

We do not copy the live developer database or its business data into user_acceptance_test.

This prototype has no separate shared DEV deployment target. A/B/C are its development areas; C demonstrates the complete development assembly. Qualification is the next deployment target before user_acceptance_test. The walkthrough replays already reviewed source snapshots rather than performing new engineer authoring.

**Actor: privileged provisioning operator.** Each invocation creates/checks exactly one declared schema, workspace, workspace accounts, delivery-interface grants and central automation connection. It does not install applications or business data.

### A/B/C — private development areas

Each engineer gets a separate schema, APEX workspace and assigned application ID within the shared Oracle/APEX installation. These areas support independent development; reviewed files captured into Git become the release source. C demonstrates the complete development assembly in this walkthrough.

1. Provision A's private area:

   ```bash
   bash scripts/cicd-area-provision.sh lab-dev
   ```

2. Provision B's private area:

   ```bash
   bash scripts/cicd-area-provision.sh lab-dev-b
   ```

3. Provision C's private area:

   ```bash
   bash scripts/cicd-area-provision.sh lab-dev-c
   ```

4. Wait for each **PASS assigned area**. A command naming A never creates/changes B or C's accounts, nor qualification/user_acceptance_test.
5. Give each developer only their assigned schema password and App Builder login. The operator can retrieve a specific schema password with `python3 scripts/cicd-password.py E1_DEV_A` (or E1_DEV_B/E1_DEV_C). Do not give developers the administrator credential store. Developers configure their private profiles in the next main chapter; the central automation connections belong to the operator's lab runner.

### integration_test — disposable release validation

**DevOps role:** integration/release testing before UAT. The actual schema and workspace are **E1_INTEGRATION**, application **810004**. Qualification is the activity performed in this area.

**integration_test** is the release-validation area before user_acceptance_test. The pipeline installs the packaged archive here, checks migrations, APEX import, component compatibility and application behavior, then records qualification against the exact archive hash. A patch must pass both fresh installation and upgrade from its supported previous release. Only the same successfully qualified archive may proceed to user_acceptance_test.

1. Provision the empty integration_test area:

   ```bash
   bash scripts/cicd-area-provision.sh integration_test
   ```

2. Wait for **PASS assigned area**. Provisioning creates the area only; release qualification happens in D and F.
3. Treat qualification as disposable: its application and test data can be removed and reconstructed for a declared qualification scenario. This is where installation/upgrade failures should be discovered before changing user_acceptance_test.

### user_acceptance_test — retained release demonstration

**DevOps role:** UAT, using actual schema/workspace **E1_UAT**, application **810005**. The Product Owner decides acceptance after reviewing the delivered application; pipeline success alone does not grant acceptance.

**user_acceptance_test** receives the identical qualified archive and provides the application used to demonstrate the delivered release. Its settings and greeting history are retained across normal upgrades, allowing the Product Owner to see both the new behavior and preservation of earlier data.

1. Provision the empty user_acceptance_test area:

   ```bash
   bash scripts/cicd-area-provision.sh user_acceptance_test
   ```

2. Wait for **PASS assigned area**. Initial promotion happens in E; the compatible patch upgrade happens in F.
3. Keep user_acceptance_test data during normal deployments. Do not reset it as a qualification fixture. The separately invoked **apex-destroy.sh** is an explicit whole-lab restart and deletes user_acceptance_test along with every other lab area.


## Configure each developer environment

Configure A/B/C connections to their assigned areas. In this single-host walkthrough, the local operator supplies each schema password directly through a pipe, without displaying or typing it.

**Actor: local walkthrough operator configuring the developer profiles.** The password helper reads the protected operator credential store; developer setup receives only the selected schema password and creates no schemas or workspaces.

1. Configure A:

   ```bash
   (set -o pipefail; python3 scripts/cicd-password.py E1_DEV_A | bash scripts/cicd-developer-init.sh A --password-stdin)
   ```

2. Configure B:

   ```bash
   (set -o pipefail; python3 scripts/cicd-password.py E1_DEV_B | bash scripts/cicd-developer-init.sh B --password-stdin)
   ```

3. Configure C:

   ```bash
   (set -o pipefail; python3 scripts/cicd-password.py E1_DEV_C | bash scripts/cicd-developer-init.sh C --password-stdin)
   ```

4. Wait for each **PASS developer**. Setup verifies the effective schema/workspace and saves that developer's connection in `.local-apex/developers/A/sqlcl-home` (or B/C). The schema passwords differ from the DEV_A/B/C App Builder passwords. Passwords are not command-line arguments or environment variables.
5. In A's own Bash terminal, select that private profile and connect:

   ```bash
   source .local-apex/developers/A/environment.sh
   sql -nohistory -noupdates -home "$APEX_CICD_CONNECTIONS" -name lab-dev
   ```

- B/C use their corresponding environment file and lab-dev-b/lab-dev-c connection.
- This lab demonstrates separate roles/profiles under one host account; it does not claim OS-account isolation. Regular delivery walkthrough scripts use the operator's central automation store.

## Check project readiness before A

Confirm that the separate areas are correctly connected, isolated and empty before application construction begins.

**Actor: walkthrough operator**, after the explicit provisioning steps.

```bash
bash scripts/cicd-walkthrough-ready.sh
```

1. Check each area's actual identity and real cross-area read/write denial. Isolation probes are test objects, not business data.
2. Verify no lab applications/business tables or earlier control events/attempts exist and all release targets are new at epoch zero.
3. Initialize the fresh walkthrough cycle marker. Wait for **PASS walkthrough ready**, then run A.

## A. Deliver Foundation

Establish the shared database foundation and application shell. The application remains unavailable until Hello and World are present.

Run this chapter from the repository root:

```bash
bash scripts/cicd-walkthrough-A_foundation.sh
```

1. Acquire Foundation ownership and install the reviewed Foundation-only Git snapshot into empty A using native SQLcl/Liquibase and APEX import.
2. Verify Foundation 1.0.0, absent Hello/World, no seed entries and blocked incomplete assembly. Release the owned task.
3. Open [A](http://127.0.0.1:8080/ords/f?p=810001:1). See the unavailable incomplete application; no old greeting history exists.

## B. Deliver Hello

Add Hello on top of the accepted Foundation baseline. The application stays unavailable while World is still missing.

Run this chapter from the repository root:

```bash
bash scripts/cicd-walkthrough-B_hello.sh
```

1. After A passes, acquire Hello ownership and install the reviewed Foundation/Hello snapshot into empty B.
2. Execute its first three migrations and unchanged native APEX import. Verify Hello 1.0.0, absent World, empty business entries and blocked runtime; release the task.
3. Open [B](http://127.0.0.1:8080/ords/f?p=810002:1). See World-not-installed protection. This replays accepted sequential integration; it does not prove parallel authoring.

## C. Deliver World and complete the assembly

Add World to complete the first working application in **C’s private development area (810003)**. VERIFIER checks it there; publication opens that same development application to LAB_USER. This is not release qualification or promotion to user_acceptance_test. The archive is independently installed/verified in **qualification (810004) in D**, then the identical qualified archive is promoted to **user_acceptance_test (810005) in E**.

Run this chapter from the repository root:

```bash
bash scripts/cicd-walkthrough-C_world.sh
```

If C was already installed and the script stopped at restricted browser verification, resume that checkpoint instead of installing again:

```bash
bash scripts/cicd-walkthrough-C_world.sh --resume-verification
```

This checks the retained task owner/base/generation, complete 1.0.0 assembly and restricted-verification state. It does not repeat migrations, import or reservation acquisition. Continue at step 3 below when the verification pause appears. If you already created Hello/World entries, reuse them. A state mismatch stops for inspection; this is not general failed-deployment recovery. Do not delete the retained C_world directory or destroy the lab to resume this pause.

1. **Act as the walkthrough operator:** after B passes, start the script above and press a key when prompted. The script acquires the integration scope and installs the reviewed complete **1.0.0** source into empty C.
2. Read the migration, compilation, version and page-check results. Wait for the script's browser-verification pause. C is now restricted to **VERIFIER**; leave the script waiting while you perform the next steps.
3. **Get the VERIFIER password in a second terminal:**

   ```bash
   python3 scripts/cicd-password.py VERIFIER
   ```

4. **Act as user VERIFIER:** open [C / application 810003](http://127.0.0.1:8080/ords/f?p=810003:1) and sign in as **VERIFIER** with that password. Sign out of another application account first if necessary.

   1. Open **Hello entries**, press **Create**, enter **Entry Text = Hello** and **Active = Y**, then press **Create** to save.
   2. Open **World entries**, press **Create**, enter **Entry Text = World** and **Active = Y**, then press **Create** to save.
   3. Open **Hello configuration**, edit its existing row, select **Hello** as the default and leave the prefix empty. Press **Apply Changes**. Repeat in **World configuration**, selecting **World** and leaving the prefix empty.
   4. Open **Home** and press **Create greeting** using the configured defaults. Open **Greeting history** and refresh; confirm a saved **Hello World** row. This exact VERIFIER greeting is required before the script will publish C. If it is missing, the script reports **VERIFICATION NOT PASSED: Hello World assertion failed** and returns to the browser-verification prompt. Other greeting text is valid application data but does not satisfy this specific walkthrough assertion; create the required example and press a key to retry, or **q** to leave C restricted. No reinstall or script restart is needed for this retry.

5. **Act as the walkthrough operator again:**

   1. Return to the waiting script terminal and press a key. The script checks the greeting, publishes C for ordinary users and releases ownership.
   2. Wait for **DEPLOYED C_world** and the final browser pause.

6. **Get the LAB_USER password in the second terminal:**

   ```bash
   python3 scripts/cicd-password.py LAB_USER
   ```

7. **Act as user LAB_USER:**

   1. Sign out of VERIFIER.
   2. Reopen [C](http://127.0.0.1:8080/ords/f?p=810003:1).
   3. Sign in as **LAB_USER**.
   4. Create another greeting.
   5. Open **Greeting history**.
   6. Open **Installed components**.

   All three components must show **1.0.0**; history contains only data created during this fresh cycle.

8. Return to the script terminal and press a key to finish. Wait for **PASS result stage C_world** before starting D.

- In **--rehearse**, the script announces and creates the runtime verification examples automatically, skipping browser/password steps. Import itself supplies no business seed.

## D. Qualify the initial release

Install the packaged release in disposable qualification and test it before allowing delivery to user_acceptance_test.

**Actor: Deployer — A-03 Delivery operator**, as defined in the [SRS actors](../../docs/srs.md#actors). The development team/Packager (A-02) has already smoke-checked the development assembly and released the reviewed package. The deployer takes that package through qualification in D and user_acceptance_test promotion in E, executes the CLI steps and switches to the VERIFIER/LAB_USER runtime accounts for browser checks. These accounts are not additional system actors. This is the qualification part of [UC-4](../../docs/srs.md#uc-4--deliver-a-reviewed-change), with verification support under [UC-11](../../docs/srs.md#uc-11--verify-delivery-and-prepare-the-next-task) and runtime behavior from UC-2/3. It implements the selected [PBI-011.6 qualification/promotion slice](sprint_E.1_design.md#pbi-0116--qualify-and-promote-identical-artifacts) under [PBI-011](../../BACKLOG.md#pbi-011-build-an-executable-architectural-prototype); broader acceptance remains as recorded in the design/results.

Run this chapter from the repository root:

```bash
bash scripts/cicd-walkthrough-D_qualification.sh
```

The script executes these operations in order. Each controller operation rechecks the archive, controller revision, target mapping and tool environment; a failed command stops before the next operation. See the editable [delivery model](model.drawio), pages **lifecycle** and **D qualification**.

1. **Check prerequisites:** require C's completion marker and create a new D attempt directory. An already attempted D stage stops for inspection; C's resume option does not apply to D.
2. **Select and inspect the archive:** read `.local-apex/releases/initial-selected.txt`; verify the archive SHA-256, member checksums, manifest and candidate/source identity. D uses the retained reviewed **1.0.0** archive. It does not export C, rebuild the archive or copy business data.
3. **Read target status:** run controller **status** for `integration_test`, schema/workspace **E1_INTEGRATION**, application **810004**. Read its current epoch, which identifies the controlled deployment generation.
4. **Admit the empty target:** at the terminal prompt, press a key for **admit**. The control authority checks the expected epoch and empty initial target, records the owned attempt and advances its epoch. Ordinary runtime access remains blocked.
5. **Apply database migrations:** press a key for **migrate**. SQLcl runs Liquibase **validate → update → status** using the archive's changelog. The initial archive contains migrations 001–004; this is not the current checkout's later patch changelog.
6. **Import the APEX definition:** press a key for **import**. Import the archive's unchanged split export into application **810004**, mapped to E1_INTEGRATION. Check that ordinary access is still blocked.
7. **Run automated checks:** press a key for **units**. Check release versions, required pages and compilation, then execute greeting-composition and immutable-history tests. Their transactional fixtures are rolled back.
8. **Enable restricted verification:** press a key for **verify**. Recheck release integrity and absence of packaged business data, then allow **VERIFIER** and record the attempt as verifying. This controller operation prepares the browser test; it does not perform it.
9. **Retrieve the VERIFIER password in a second terminal:**

   ```bash
   python3 scripts/cicd-password.py VERIFIER
   ```

10. **Act as VERIFIER in integration_test:** leave the script waiting at its browser pause and open [integration_test / application 810004](http://127.0.0.1:8080/ords/f?p=810004:1). Sign out of any other account and sign in as **VERIFIER**.

    1. Create active **Hello** and **World** entries, using those exact example texts.
    2. Edit the existing Hello/World configuration rows to select those defaults with empty prefixes; save each change.
    3. On **Home**, press **Create greeting**. Open **Greeting history** and refresh to confirm **Hello World** saved by VERIFIER. These are new qualification test data, not developer data copied by the release.

11. **Publish qualification:** return to the waiting terminal and press a key. Controller **publish** requires the saved VERIFIER **Hello World** snapshot, prepares native availability, captures the final live APEX fingerprint, and commits the successful receipt with the external ready gate. A missing snapshot stops D; C's verification retry loop is specific to C.
12. **Verify the published result:** the script's result command checks ready state, component versions, matching archive hash and equality of the live fingerprint to its receipt. Only then mark D complete and report **DEPLOYED AND QUALIFIED**. This is qualification, not user_acceptance_test promotion.
13. **Retrieve LAB_USER's password in the second terminal:**

    ```bash
    python3 scripts/cicd-password.py LAB_USER
    ```

14. **Act as LAB_USER:** sign out of VERIFIER, reopen integration_test and sign in as **LAB_USER**. Create a greeting and refresh history to confirm ordinary access after publication.
15. Return to the script terminal and press a key. Wait for **PASS result stage D_qualification**. Continue to **E** to promote the same archive to user_acceptance_test.

- Initial SHA-256: `d99fe83ec3d149739a12ec0cf2f01081ae027d1ec015e16d5a971ff3c602ab45`. This cycle obtains a new database receipt; historical host evidence does not substitute for qualification.
- **--rehearse** executes real operations, substitutes explicit runtime API examples for step 10, and skips human browser/password checkpoints. It does not establish browser acceptance.

## E. Promote the same initial artifact to user_acceptance_test

Deliver the exact qualified archive to user_acceptance_test, establishing the first usable release without rebuilding its contents.

Run this chapter from the repository root:

```bash
bash scripts/cicd-walkthrough-E_promotion.sh
```

1. After D passes, select and verify the **same initial archive**; do not rebuild it.
2. Admit empty user_acceptance_test. The control authority requires this cycle's matching qualification receipt before promotion.
3. Execute **migrate → import → units → verify**, then use [user_acceptance_test](http://127.0.0.1:8080/ords/f?p=810005:1) as **VERIFIER** to create/configure Hello/World and verify the new greeting/history.
4. Continue to publish and compare the integration_test/user_acceptance_test archive hashes and new successful receipts.
5. Open user_acceptance_test as **LAB_USER**. It now runs **1.0.0** with only this cycle's data.
6. Continue to the explicitly announced twenty verification-history examples and field-level baseline capture for F. These are new test examples for preservation checks, not restored history or release seed.

- Retrieve the password with `python3 scripts/cicd-password.py LAB_USER`. Imports may require re-login.

## F. Deliver the compatible Hello patch

Demonstrate a compatible 1.0.1 upgrade: qualify the patch, promote the same bytes and preserve existing user_acceptance_test settings and greeting history.

Run this chapter from the repository root:

```bash
bash scripts/cicd-walkthrough-F_hello_patch.sh
```

1. After E passes, verify the reviewed Hello **1.0.1** archive. The initial user_acceptance_test field baseline is already captured.
2. Explicitly recreate **only disposable qualification**; install/test/publish the patch from empty using **preflight → admit → migrate → import → units → verify → publish → result**.
3. Explicitly recreate only qualification again. Reconstruct initial 1.0.0 from its archive, create new verification examples and capture the upgrade baseline.
4. Upgrade qualification with the same patch archive. Verify both required qualification starts and compare every pre-upgrade data/configuration field.
5. Upgrade retained user_acceptance_test from 1.0.0 with those **identical patch bytes**. user_acceptance_test is not reset during this upgrade.
6. At each restricted verification checkpoint, open the printed URL as **VERIFIER**, create a greeting and refresh history, then continue to publish. Read the real outputs and stop on any failure.
7. Compare user_acceptance_test's earlier rows/settings, then open [user_acceptance_test](http://127.0.0.1:8080/ords/f?p=810005:1) as **LAB_USER**. See **Foundation 1.0.0 / Hello 1.0.1 / World 1.0.0**, and greetings created before/after the upgrade in this cycle.

- Selected patch SHA-256: `4ba3abb8709f256c7a47e3e9294d3e7303f742145a95cb58d808ca6c6bcf7200`. Read it again with `shasum -a 256 "$(cat .local-apex/releases/patch-selected.txt)"`. C remains the development **1.0.0** checkpoint; F upgrades qualification and user_acceptance_test.
- Restricted verification creates current-cycle evidence. --rehearse uses explicit runtime API examples and skips browser checks. Broader request draining/fencing remains open.

## G. Reject an incompatible database upgrade

Show that the pipeline rejects a breaking Foundation proposal before changing the working database or application.

Run this chapter from the repository root:

```bash
bash scripts/cicd-walkthrough-G_incompatible_upgrade.sh
```

1. Press a key to submit the Foundation **2.0.0** proposal to the deployment compatibility gate.
2. Read **REJECTED INCOMPATIBLE: Hello requires Foundation 1.0.0; proposed Foundation 2.0.0**. World has the same declared Foundation requirement.
3. Read the unchanged-target verification: definitions, versions, entries, settings, history and control receipts match before/after rejection. Maintenance, migrations and import were not entered.
4. Open [user_acceptance_test](http://127.0.0.1:8080/ords/f?p=810005:1), create a greeting and reopen history. The current release still works.
5. Continue to the controlled page-drift demonstration.

- This is a rejected deployment proposal; no destructive Foundation 2.0.0 migration is constructed or executed.
- The accepted patch above proves the pipeline also admits a supported change.

## H. Reject deployment over unexpected live change

Introduce a controlled page change, show deployment stopping on drift, then explicitly restore the original definition while preserving data.

Run this chapter from the repository root:

```bash
bash scripts/cicd-walkthrough-H_drift.sh
```

1. Press a key for the explicit **user_acceptance_test-only page-drift fixture**. It verifies the current release, saves the actual native target export/data, then installs the separately authored Home title/banner change with the existing ID offset.
2. Open [user_acceptance_test](http://127.0.0.1:8080/ords/f?p=810005:1), re-login if needed and see **DIRECT CHANGE - deployment must stop**. Installed component versions still describe 1.0.1; the live content fingerprint has changed.
3. Continue to the attempted redeployment preflight.
4. Read **REJECTED DRIFT**, with the actual fingerprint mismatch, followed by unchanged-target/control-receipt checks. No maintenance, migration or release import occurred.
5. Reopen user_acceptance_test: the direct change remains visible and the application/history still work. Rejection has not overwritten it.
6. Press a key for the **separate explicit restoration**. It refuses another unexplained definition/release change, restores the saved native user_acceptance_test definition and requires the original successful fingerprint. All data/settings present before restoration must survive.
7. Reopen user_acceptance_test and re-login if required. The banner is gone; earlier and newly appended greetings remain.

- The fixture replacement is test setup outside release delivery. Run it with other user_acceptance_test authoring/deployment stopped.
- Restoration is controlled demonstration cleanup, not automatic deployment repair or silent acceptance of drift.
- Broader schema-drift coverage, concurrent requests, verifier fencing and failed additive deployment repair remain pending.

## Destroy the lab after the walkthrough

Optionally remove the entire lab installation and its data when the demonstration is finished.

When you deliberately want to discard this demonstration:

```bash
bash scripts/apex-destroy.sh
```

1. Read the named ownership inventory and deletion scope.
2. Wait for **PASS destroy**. All current lab applications and greeting history are removed; the VM, host inputs and unrelated resources remain.
3. To build again, follow the precheck/host/cleanup/install sequence before A. To inspect the completed applications, leave this optional destruction step until afterward.

## Maintain this artifact

Keep the editable [delivery model](model.drawio), especially its lifecycle and D qualification pages, synchronized with the actor handoff and numbered operations below.

Keep the Product Owner explanations, operator commands and actual script behavior aligned whenever this walkthrough changes.

- Start each chapter with a short explanation of its purpose and expected Product Owner outcome.
- Put the exact runnable script command after that explanation in each action chapter; keep it synchronized with that chapter script.
- Always update and review this document, its launcher, A–H chapter scripts, shared helper, cleanup instructions and detailed operator guide together as **one artifact**. Keep chapter names, script names, commands and outcomes synchronized.
- Use numbered actions, short outcome bullets and runtime URLs.
- Keep developer mechanics inside the stage; retain their real output for diagnosis.
- Add **DEPLOYED** or **REJECTED** only after the corresponding operation and verification exist.
- Keep unproved broader capabilities **PENDING** and preserve the separate detailed operator walkthroughs.
- The [accepted design](sprint_E.1_design.md) remains the source for the positive patch, incompatibility and drift acceptance criteria.
