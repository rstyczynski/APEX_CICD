# E.1 — Use-case walkthrough: deployment results and protection

## Contents

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
- [Configure each developer environment](#configure-each-developer-environment)
- [Check project readiness before A](#check-project-readiness-before-a)
- [A. Deliver Foundation](#a-deliver-foundation)
- [B. Deliver Hello](#b-deliver-hello)
- [C. Deliver World and complete the assembly](#c-deliver-world-and-complete-the-assembly)
- [D. Qualify the initial release](#d-qualify-the-initial-release)
- [E. Promote the same initial artifact to TEST](#e-promote-the-same-initial-artifact-to-test)
- [F. Deliver the compatible Hello patch](#f-deliver-the-compatible-hello-patch)
- [G. Reject an incompatible database upgrade](#g-reject-an-incompatible-database-upgrade)
- [H. Reject deployment over unexpected live change](#h-reject-deployment-over-unexpected-live-change)
- [Destroy the lab after the walkthrough](#destroy-the-lab-after-the-walkthrough)
- [Maintain this artifact](#maintain-this-artifact)

## What this walkthrough shows

- This lab simulates work of 3 developers (identified as A, B, and C) dedicated to development of APEX style Hello World application architected as composition of three components: database and two user facing ones.
- The Product Owner sees application outcomes after successful deployments and evidence that wrong deployments are blocked.
- Developer A/B/C operations run inside the guided stages. The Product Owner does not inspect App Builder, page definitions, SQL source or Git diffs in this workflow.
- Show the actual operation output and a short result: **DEPLOYED**, **REJECTED**, **ERROR** or **PENDING**.
- After a successful deployment, show its result in the running application at the printed URL.
- After an expected rejection, show the exact reason, verify the target was not overwritten, then open the application to demonstrate that its prior behavior and saved history remain intact.

## Deep dive

This business-level walkthrough, its [launcher](../../scripts/cicd-walkthrough.sh), the A–H chapter scripts below and the [detailed operator guide](user_manual.md) describe one system. Maintain and review them together as **one artifact**.

## Applied tools and techniques

The deployment has two kinds of source: **APEX application definitions** and **database migrations**. Git keeps both together. Operators use small shell scripts and visible SQLcl commands to assemble and check one application in each target. The working development assembly demonstrates this approach; initial delivery and the compatible Hello upgrade execute verified archives; the selected incompatibility and page-drift rejection scenarios now have executable demonstrations.

### Toolchain and responsibilities

1. **Oracle APEX 24.2 App Builder** authors pages and shared components. **ORDS** serves their browser URLs. A save in App Builder changes the live development application; capture and Git review are separate operations.
2. **SQLcl 25.3 with Java 21** connects through private saved connections, runs explicit SQL/PLSQL and performs native APEX export/import. Capture uses split files, original component IDs, no export date and no supporting-object installation. Oracle-generated export files are executed unchanged. Public APIs such as **APEX_APPLICATION_INSTALL** map the source to a target workspace/schema/application; **APEX_APPLICATION_ADMIN** controls native availability.
3. **Oracle Database and PL/SQL** hold component data, configuration, installed versions and immutable greeting snapshots. Database constraints, packages and triggers enforce the business rules even when a caller bypasses the browser. A separate **E1_CTRL** schema keeps managed task ownership outside ordinary application migrations/imports.
4. **Liquibase through SQLcl** applies ordered database changesets and records their identities/checksums in **DATABASECHANGELOG**. An applied migration is retained unchanged; a later correction needs a new changeset. The application export and database migrations remain distinct parts of the same reviewed source revision.
5. **Git** identifies the reviewed source commit and shows the component diff. Foundation is established first; Hello and World are integrated from bounded private work. The replay uses reviewed sequential B/C source snapshots; it does not simulate new authoring. Durable task reservations record owner, task, base commit and generation; they are separate from the durable initial-release ownership controls.
6. **Bash, small Python standard-library helpers and SQL assertions** expose operator stages, handle files/connections and check outcomes. The results script pauses at runtime URLs; the detailed operator guide explains individual commands. Credentials stay in protected local storage, outside Git and release contents. Repository positioning comes from Git discovery.
7. **Podman** runs the local Oracle Database and ORDS containers. Separate database schemas, APEX workspaces and application IDs provide A/B/C development areas, disposable qualification and retained TEST on the same host. This is logical isolation; it does not model independent production hosts. Infrastructure lifecycle operations follow [deploy.md](../../docs/deploy.md).

### How delivery is organized

1. **Prepare and identify the target.** Check the effective database user, PDB, workspace and application mapping before writes. Reserve the declared component work before managed authoring. Keep Foundation-only and incomplete assemblies unavailable.
2. **Capture and review source.** Export native APEX definitions, review the declared component changes and inherited/shared definitions, run candidate checks, then commit the accepted source. Repeated unchanged exports must match; a live development application is not itself a release artifact.
3. **Build once.** Package the accepted Git revision, migrations, deployment SQL and nonsecret manifest. Record the source commit, supported starting state, component dependencies, tool/configuration versions and the archive's **SHA-256**. Qualification and promotion must execute files from that verified archive rather than a changing checkout.
4. **Qualify, then promote the same bytes.** Reconstruct and test in the disposable area first. Retained TEST may receive only the identical qualified artifact for its supported starting state. The selected patch must also qualify against its declared earlier baseline; successful fresh installation alone does not prove an upgrade.
5. **Verify before publishing.** Development verification already uses native restricted access for **VERIFIER**, followed by integrity/browser checks and a separate publication operation. The release design additionally requires persistent attempt ownership, maintenance fencing, final live fingerprints and a receipt before readiness. The initial release now uses persistent attempt ownership, an external runtime gate and a final fingerprint. Native availability is prepared while the external gate still restricts business requests; successful receipt and external readiness commit together. Guarded mutation admission and ordinary-request blocking passed for the patch; complete read/asynchronous request draining and stale-verifier fencing remain unproved.

### How correctness is checked

1. **Isolation and identity:** actual cross-area read/write denial tests supplement configuration inspection. A correct application sent to the wrong schema still fails the target check.
2. **Dependency and version rules:** Foundation must precede its dependents, and installed components must form a supported complete combination. Semantic versions describe contracts: the compatible Hello correction advances **1.0.0 → 1.0.1**; a breaking Foundation change requires compatible dependents. Version labels alone do not establish compatibility. The Foundation 2.0.0 proposal is rejected because its dependents still require Foundation 1.0.0.
3. **Behavior and retained data:** Oracle unit assertions check exact greeting composition, defaults, explicit selections, prefixes, Unicode, limits and rejected input. Snapshot tests check that changed configuration affects new greetings while old snapshots remain unchanged, and that history update/delete is rejected. Browser checks exercise the actual runtime as verifier and ordinary user.
4. **Repeatability and failure reporting:** cleanup is an explicit separate destructive step for this disposable demonstration. During the actual patch, field-level baseline comparisons preserve this cycle's earlier rows/settings. Scripts check Oracle errors and successful completion markers, stop on unexpected failure and show the reason. A failed connection or arbitrary error is not evidence that a bad deployment was correctly rejected.
5. **Traceability and drift:** a Git commit identifies source; a semantic version describes its contract; an archive hash identifies exact packaged bytes; a recomputed live APEX fingerprint detects changed application definitions; schema checks cover the declared migrations and component versions. These serve different purposes. The selected drift scenario rejects a changed Home title/banner before maintenance, migration or import and leaves the changed page/history intact until explicit restoration. A matching hash alone does not prove functional correctness.

The [current verification evidence](sprint_E.1_tests.md) supports development, repeatable preparation, both release paths, preserved settings/history and the two selected rejection scenarios. Complete request draining/fencing, concurrency and automated failed-deployment repair remain unproved. Correctness is established by the checks actually passed for the stated scope; this chapter does not turn the [accepted design](sprint_E.1_design.md) into a completed guarantee.

## Alignment with selected Elaboration use cases

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

- **Delivered checkpoint:** infrastructure and the separate onboarding steps have been verified; the five lab applications and their business/history tables are absent. The lab is ready for A. When restarting from cleanup, follow every infrastructure and onboarding chapter below before A. The earlier A–H rehearsal remains historical evidence.
- This walkthrough now starts with explicit prerequisite checking, Podman host preparation, complete lab cleanup and fresh database/APEX/ORDS installation.
- Cleanup destroys **all database state in this lab**, including A/B/C, qualification, TEST, entries, settings, greeting history and database control receipts. Host credentials, tools, reviewed source/release archives and historical evidence remain available; unrelated Podman resources are preserved.
- Infrastructure installation ends with **only Oracle Database/APEX/ORDS**. It creates no E1_CTRL, developer/target schemas, project workspaces or developer accounts. Project control and named-area provisioning follow separately.
- A–C install the reviewed Foundation, Hello and complete World snapshots. A/B remain unavailable while incomplete; C starts at **1.0.0**.
- D/E execute real qualification and promotion of the **same initial artifact** in this cycle. F qualifies Hello **1.0.1** both fresh and over 1.0.0, then upgrades TEST with those identical bytes, preserving only the data created during this cycle.
- G/H demonstrate the selected rejections and explicit controlled page restoration. Rehearsal uses clearly identified NEW runtime test examples and skips human browser viewing.
- Broader E.1 concurrency, complete maintenance fencing, schema-drift coverage and failed-additive-deployment repair remain open. This walkthrough does not close the sprint.

## Run the results walkthrough

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

- A–F now install/deploy, rather than only display an earlier result. Repeating an already attempted construction chapter stops for inspection; start a new demonstration with the explicit infrastructure cleanup/install sequence.
- **--preflight** on A–H checks local tools/files/chapter mapping without connecting to Oracle. It does not substitute for the infrastructure precheck below.
- **--rehearse** executes real installations, qualification/promotion and the TEST page fixture without pauses. Its explicit runtime API test examples are not browser verification. It requires the fresh infrastructure preparation first.
- Normal release result inspection remains read-only through the separate operator result commands. No App Builder inspection is required in this Product Owner journey.

## Run one chapter at a time

1. Complete infrastructure installation, then explicit project control, named-area provisioning, developer configuration and readiness below once for this cycle.
2. Execute A–H in order. Each chapter contains its exact command, actual operation output, expected outcome and runtime URL.
3. Each script stops on errors. Do not advance after a failed or interrupted attempt; retain its transcript and inspect ownership/partial state. Full cleanup is a separate deliberate restart of the demonstration, not deployment repair.

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

```bash
bash scripts/cicd-walkthrough-host.sh
```

1. Create **apex-cicd** only if absent; otherwise reuse it.
2. Start the named engine using the established local helper/launch procedure if stopped.
3. Inspect the engine/resources and pull the pinned native ARM database and ORDS images.
4. Wait for **PASS host**. If another VM prevents startup, stop here and follow [deploy.md](../../docs/deploy.md#3-create-and-start-the-vm--fresh-setup-only); this script does not stop/remove unrelated VMs.

## Prepare a repeatable walkthrough

Run the scoped **destructive cleanup** after successful precheck/host preparation:

```bash
bash scripts/cicd-walkthrough-cleanup.sh
```

1. Read the printed ownership inventory and scope. The script refuses unrelated containers sharing the lab's named volumes/network.
2. Stop/remove **apex-ords** and **apex-db** on connection **apex-cicd**.
3. Remove **apex-data**, **apex-ords-config**, **apex-images**, **apex-net** and **apex-db-password**, when present.
4. Wait for **PASS cleanup**. All lab database/APEX state, including greeting history, is gone. Repeating cleanup on an already empty lab is allowed.
5. Continue to **Install the fresh database and APEX**. Do not run A yet.

- The VM, images, host credentials/tools/installers and reviewed release archives remain; unrelated containers, volumes, networks, secrets and VMs are untouched. Historical host evidence is retained separately and cannot pass fresh database receipt checks.
- This replaces the previous settings-only preparation. That optional operation is now named `bash scripts/cicd-demo-defaults.sh`; it preserves history and is not fresh-start cleanup.
- [The scoped destruction procedure](../../docs/deploy.md#12-scoped-destruction-and-fresh-reconstruction) explains the individual commands. Removing the whole VM is not needed to obtain an empty database.

## Install the fresh database and APEX

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

## Initialize project delivery control

**Actor: project/platform operator**, with the lab administrator credential. This is project setup, separate from Oracle infrastructure.

```bash
bash scripts/cicd-control-init.sh
```

1. Create/check **E1_CTRL only**, with its protected operator SQLcl connection.
2. Install ownership and release-control packages. No developer or deployment-target schemas/workspaces/accounts are created. Per-area grants are deferred until the selected area is provisioned.
3. Wait for **PASS project control**, then provision the named areas below.

## Provision each assigned area

**Actor: privileged provisioning operator.** Each invocation creates/checks exactly one declared schema, workspace, workspace accounts, delivery-interface grants and central automation connection. It does not install applications or business data.

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

4. Provision disposable qualification:

   ```bash
   bash scripts/cicd-area-provision.sh lab-qualify
   ```

5. Provision retained TEST:

   ```bash
   bash scripts/cicd-area-provision.sh lab-test
   ```

- Wait for each **PASS assigned area**. A command naming A never creates/changes B or C's accounts, nor qualification/TEST.
- Give each developer only their assigned schema password and App Builder login. The operator can retrieve a specific schema password with `python3 scripts/cicd-password.py E1_DEV_A` (or E1_DEV_B/E1_DEV_C). Do not give developers the administrator credential store.
- The shared central automation connections belong to the operator's lab runner. Developers configure their own profiles in the next chapter.

## Configure each developer environment

**Actor: the assigned developer.** These commands perform no schema/workspace creation and never open the administrator credential files.

1. Developer A runs:

   ```bash
   bash scripts/cicd-developer-init.sh A
   ```

2. Developer B runs:

   ```bash
   bash scripts/cicd-developer-init.sh B
   ```

3. Developer C runs:

   ```bash
   bash scripts/cicd-developer-init.sh C
   ```

4. Enter only the assigned **schema password**, hidden at the prompt. For A this is E1_DEV_A's password; DEV_A is the separate App Builder account.
5. The command verifies the effective schema/workspace and saves only that developer's connection in `.local-apex/developers/A/sqlcl-home` (or B/C). It prints **PASS developer** and the exact environment command.
6. In A's own Bash terminal, select that private profile and connect:

   ```bash
   source .local-apex/developers/A/environment.sh
   sql -nohistory -noupdates -home "$APEX_CICD_CONNECTIONS" -name lab-dev
   ```

- B/C use their corresponding environment file and lab-dev-b/lab-dev-c connection. The setup needs no SYS connection or privileged files. `--password-stdin` is available for controlled automated verification; passwords are never command-line arguments.
- This lab demonstrates separate roles/profiles under one host account; it does not claim OS-account isolation. Regular delivery walkthrough scripts use the operator's central automation store.

## Check project readiness before A

**Actor: walkthrough operator**, after the explicit provisioning steps.

```bash
bash scripts/cicd-walkthrough-ready.sh
```

1. Check each area's actual identity and real cross-area read/write denial. Isolation probes are test objects, not business data.
2. Verify no lab applications/business tables or earlier control events/attempts exist and all release targets are new at epoch zero.
3. Initialize the fresh walkthrough cycle marker. Wait for **PASS walkthrough ready**, then run A.

## A. Deliver Foundation

Run this chapter from the repository root:

```bash
bash scripts/cicd-walkthrough-A_foundation.sh
```

1. Acquire Foundation ownership and install the reviewed Foundation-only Git snapshot into empty A using native SQLcl/Liquibase and APEX import.
2. Verify Foundation 1.0.0, absent Hello/World, no seed entries and blocked incomplete assembly. Release the owned task.
3. Open [A](http://127.0.0.1:8080/ords/f?p=810001:1). See the unavailable incomplete application; no old greeting history exists.

## B. Deliver Hello

Run this chapter from the repository root:

```bash
bash scripts/cicd-walkthrough-B_hello.sh
```

1. After A passes, acquire Hello ownership and install the reviewed Foundation/Hello snapshot into empty B.
2. Execute its first three migrations and unchanged native APEX import. Verify Hello 1.0.0, absent World, empty business entries and blocked runtime; release the task.
3. Open [B](http://127.0.0.1:8080/ords/f?p=810002:1). See World-not-installed protection. This replays accepted sequential integration; it does not prove parallel authoring.

## C. Deliver World and complete the assembly

Run this chapter from the repository root:

```bash
bash scripts/cicd-walkthrough-C_world.sh
```

1. After B passes, acquire the complete integration scope and install the reviewed complete 1.0.0 source into empty C.
2. Check migrations, compilation, component versions and required pages. Enable restricted verification.
3. Open [C](http://127.0.0.1:8080/ords/f?p=810003:1) as **VERIFIER**. Create **Hello** and **World**, configure defaults, create **Hello World** and refresh its new history.
4. Continue in the terminal to publish and release ownership.
5. Open C as **LAB_USER**. Use the application and see only data created in this fresh cycle. All three components are **1.0.0**.

- In --rehearse, the explicitly announced runtime API fixture performs step 3; browser viewing is skipped. Import itself supplies no business seed.

## D. Qualify the initial release

Run this chapter from the repository root:

```bash
bash scripts/cicd-walkthrough-D_qualification.sh
```

1. After C passes, verify the retained reviewed initial archive and its SHA-256. This archive contains source and deployment SQL, not prior business data.
2. Admit the empty qualification application target using its observed epoch. Run **migrate → import → units → verify** as visible separate controller operations from that archive.
3. Open [qualification](http://127.0.0.1:8080/ords/f?p=810004:1) as **VERIFIER**, create/configure Hello and World, create Hello World and refresh history.
4. Continue to **publish**, verify the new qualification receipt/fingerprint, then open the application as **LAB_USER**.

- Initial SHA-256: `6a1da4a940586541cbb034277605d7ed36e5d1ad305554f9a2fe4c64cd59411c`. This cycle obtains a new database receipt; historical host evidence does not substitute for qualification.

## E. Promote the same initial artifact to TEST

Run this chapter from the repository root:

```bash
bash scripts/cicd-walkthrough-E_promotion.sh
```

1. After D passes, select and verify the **same initial archive**; do not rebuild it.
2. Admit empty TEST. The control authority requires this cycle's matching qualification receipt before promotion.
3. Execute **migrate → import → units → verify**, then use [TEST](http://127.0.0.1:8080/ords/f?p=810005:1) as **VERIFIER** to create/configure Hello/World and verify the new greeting/history.
4. Continue to publish and compare the qualification/TEST archive hashes and new successful receipts.
5. Open TEST as **LAB_USER**. It now runs **1.0.0** with only this cycle's data.
6. Continue to the explicitly announced twenty verification-history examples and field-level baseline capture for F. These are new test examples for preservation checks, not restored history or release seed.

- Retrieve the password with `python3 scripts/cicd-password.py LAB_USER`. Imports may require re-login.

## F. Deliver the compatible Hello patch

Run this chapter from the repository root:

```bash
bash scripts/cicd-walkthrough-F_hello_patch.sh
```

1. After E passes, verify the reviewed Hello **1.0.1** archive. The initial TEST field baseline is already captured.
2. Explicitly recreate **only disposable qualification**; install/test/publish the patch from empty using **preflight → admit → migrate → import → units → verify → publish → result**.
3. Explicitly recreate only qualification again. Reconstruct initial 1.0.0 from its archive, create new verification examples and capture the upgrade baseline.
4. Upgrade qualification with the same patch archive. Verify both required qualification starts and compare every pre-upgrade data/configuration field.
5. Upgrade retained TEST from 1.0.0 with those **identical patch bytes**. TEST is not reset during this upgrade.
6. At each restricted verification checkpoint, open the printed URL as **VERIFIER**, create a greeting and refresh history, then continue to publish. Read the real outputs and stop on any failure.
7. Compare TEST's earlier rows/settings, then open [TEST](http://127.0.0.1:8080/ords/f?p=810005:1) as **LAB_USER**. See **Foundation 1.0.0 / Hello 1.0.1 / World 1.0.0**, and greetings created before/after the upgrade in this cycle.

- Patch SHA-256: `200ebefff13e87600699adfebbbe71158962dc80a02d1b8e6dbd9a829dd9e1ce`. C remains the development **1.0.0** checkpoint; F upgrades qualification and TEST.
- Restricted verification creates current-cycle evidence. --rehearse uses explicit runtime API examples and skips browser checks. Broader request draining/fencing remains open.

## G. Reject an incompatible database upgrade

Run this chapter from the repository root:

```bash
bash scripts/cicd-walkthrough-G_incompatible_upgrade.sh
```

1. Press a key to submit the Foundation **2.0.0** proposal to the deployment compatibility gate.
2. Read **REJECTED INCOMPATIBLE: Hello requires Foundation 1.0.0; proposed Foundation 2.0.0**. World has the same declared Foundation requirement.
3. Read the unchanged-target verification: definitions, versions, entries, settings, history and control receipts match before/after rejection. Maintenance, migrations and import were not entered.
4. Open [TEST](http://127.0.0.1:8080/ords/f?p=810005:1), create a greeting and reopen history. The current release still works.
5. Continue to the controlled page-drift demonstration.

- This is a rejected deployment proposal; no destructive Foundation 2.0.0 migration is constructed or executed.
- The accepted patch above proves the pipeline also admits a supported change.

## H. Reject deployment over unexpected live change

Run this chapter from the repository root:

```bash
bash scripts/cicd-walkthrough-H_drift.sh
```

1. Press a key for the explicit **TEST-only page-drift fixture**. It verifies the current release, saves the actual native target export/data, then installs the separately authored Home title/banner change with the existing ID offset.
2. Open [TEST](http://127.0.0.1:8080/ords/f?p=810005:1), re-login if needed and see **DIRECT CHANGE - deployment must stop**. Installed component versions still describe 1.0.1; the live content fingerprint has changed.
3. Continue to the attempted redeployment preflight.
4. Read **REJECTED DRIFT**, with the actual fingerprint mismatch, followed by unchanged-target/control-receipt checks. No maintenance, migration or release import occurred.
5. Reopen TEST: the direct change remains visible and the application/history still work. Rejection has not overwritten it.
6. Press a key for the **separate explicit restoration**. It refuses another unexplained definition/release change, restores the saved native TEST definition and requires the original successful fingerprint. All data/settings present before restoration must survive.
7. Reopen TEST and re-login if required. The banner is gone; earlier and newly appended greetings remain.

- The fixture replacement is test setup outside release delivery. Run it with other TEST authoring/deployment stopped.
- Restoration is controlled demonstration cleanup, not automatic deployment repair or silent acceptance of drift.
- Broader schema-drift coverage, concurrent requests, verifier fencing and failed additive deployment repair remain pending.

## Destroy the lab after the walkthrough

When you deliberately want to discard this demonstration:

```bash
bash scripts/cicd-walkthrough-cleanup.sh
```

1. Read the named ownership inventory and deletion scope.
2. Wait for **PASS cleanup**. All current lab applications and greeting history are removed; the VM, host inputs and unrelated resources remain.
3. To build again, follow the precheck/host/cleanup/install sequence before A. To inspect the completed applications, leave this optional destruction step until afterward.

## Maintain this artifact

- Put the exact runnable script command directly below each action chapter heading; keep it synchronized with that chapter script.
- Always update and review this document, its launcher, A–H chapter scripts, shared helper, cleanup instructions and detailed operator guide together as **one artifact**. Keep chapter names, script names, commands and outcomes synchronized.
- Use numbered actions, short outcome bullets and runtime URLs.
- Keep developer mechanics inside the stage; retain their real output for diagnosis.
- Add **DEPLOYED** or **REJECTED** only after the corresponding operation and verification exist.
- Keep unproved broader capabilities **PENDING** and preserve the separate detailed operator walkthroughs.
- The [accepted design](sprint_E.1_design.md) remains the source for the positive patch, incompatibility and drift acceptance criteria.
