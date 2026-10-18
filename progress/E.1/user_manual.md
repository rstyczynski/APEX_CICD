# E.1 — Operator guide

The [repository and pipeline draft](repo_layout.md) explains the source directories, private development areas, integration and artifact flow behind these operations. Maintain these descriptions together.

## What you can use now

- Run commands from the project checkout:

  ```bash
  cd "$(git rev-parse --show-toplevel)"
  ```

- The existing apex-cicd Podman VM hosts Oracle Database, APEX 24.2 and ORDS.
- The database endpoint is 127.0.0.1:1521/FREEPDB1.
- The [ORDS landing page](http://127.0.0.1:8080/ords/) and [App Builder sign-in](http://127.0.0.1:8080/ords/f?p=4550:1) are on loopback.
- Infrastructure start/stop/recreation belongs to the shared [deployment procedure](../../docs/deploy.md).

- The application pipeline is under construction.
- A/B retain incomplete assembly checkpoints; C has the working Foundation/Hello/World development application. Qualification and retained TEST are published at application release 1.0.1: Foundation/World 1.0.0, Hello 1.0.1.
- Use the areas below to inspect the actual current state.
- This guide is updated as construction makes each operation usable.

## Guided execution — this manual and its script

1. Open a terminal in the project checkout.
2. Start the guided walkthrough:

   ```bash
   bash scripts/cicd-operator-walkthrough.sh
   ```

3. Read the displayed manual chapter and the next command or browser action.
4. Press any key to execute that operation; press **q** to stop.
5. Inspect the command's actual output and **OK**, **REVIEW REQUIRED** or **ERROR** result.
6. When prompted for a browser step, open the displayed URL and follow that chapter's numbered instructions.
7. Press a key after completing the browser inspection to continue.

- The script displays the corresponding chapter directly from this manual.
- It covers the currently implemented main walkthrough, chapters **1–8**, including **4.1–4.5**.
- It uses native SQLcl for the same visible Oracle operations. Each SQLcl operation uses a fresh saved-connection session; commands needing a shared workspace context execute together.
- It stops on a command failure and displays the error; it does not retry writes or continue into later stages.
- A diff containing changes is **REVIEW REQUIRED**, not an automatic failure or approval.
- Browser inspection remains a human operation. A keypress records continuation, not an automated browser pass.
- The script prints DEV_A's password only after an explicit live-mode keypress. It does not save a walkthrough transcript; avoid terminal recording or redirecting live output to a shared log.
- The historical initial **lb update** is not rerun: the current walkthrough inspects the already installed Foundation.
- Capture writes only its staging directory. The script does not replace source, commit, reset infrastructure or run the unfinished release stages.

### Local preflight

1. Check that tools, required local files and manual chapter mappings exist:

   ```bash
   bash scripts/cicd-operator-walkthrough.sh --preflight
   ```

- This is a local file/tool check. Database access is checked in walkthrough chapter 2.

### Unattended rehearsal

1. Execute the current CLI operations without keypress pauses:

   ```bash
   bash scripts/cicd-operator-walkthrough.sh --rehearse
   ```

- Rehearsal still connects to Oracle and exports the live application into staging.
- It skips password display, browser interactions and human review, and labels those skips explicitly.
- A successful rehearsal does not establish browser acceptance or acceptance of a source diff.

### Maintain the pair as one artifact

- **This manual and [cicd-operator-walkthrough.sh](../../scripts/cicd-operator-walkthrough.sh) are one operating artifact. Always update and review them together with the [results guide](cicd-walkthrough.md), its launcher, A–H chapter scripts and cleanup instructions.**
- Keep the numbered/bulleted format for actions, fields, expected results and stop conditions.
- When a chapter, command, URL, prerequisite or expected outcome changes, reconcile the matching script stage and manual chapter in the same increment.
- Browser instructions are read from this file; executable commands are explicit in the script and must remain equivalent to the documented operator operations.
- Keep pending chapters labelled pending in both. Do not add a script stage that silently bypasses a manual check.
- Validate chapter mapping and script syntax, rehearse changed CLI operations, and inspect changed browser instructions before calling the pair ready.

## Operator walkthrough — current working operations

- This is the atomic operator reference; the [main A–H guide](cicd-walkthrough.md) is the fresh Product Owner walkthrough.
- Use App Builder for authoring, Git for source/review and SQLcl for Oracle operations.
- The Python isolation suite is a supporting test.
- Construction and rehearsal use these same operator steps; automated tests subsequently check their outcomes.
- Each release use case must leave the intermediate state visible so the operator can inspect it and decide whether to proceed.
- A small script may implement one bounded operation, such as checking compatibility, but must expose its inputs, target, result and failure reason.
- The guided script advances through the same visible operations with operator pauses; supporting tests remain separate.

### 1. Select the local tools and connection store

```bash
source scripts/cicd-env.sh
sql -version
```

- The sourced file only sets this terminal's Java, PATH and APEX_CICD_CONNECTIONS.
- It performs no provisioning or deployment.
- Expected SQLcl version: 25.3.0.274.1210.
- Keep this named terminal for the following commands.

### 2. Connect to A and identify the target

```bash
sql -nohistory -noupdates -home "$APEX_CICD_CONNECTIONS" -name lab-dev @deploy/operator/session_root.sql "$PWD"
```

- You are now at the SQLcl prompt. Run these operations one at a time:

  ```sql
  @deploy/operator/identity.sql E1_DEV_A E1_DEV_A
  @deploy/operator/application_inventory.sql
  @deploy/operator/component_inventory.sql
  @deploy/operator/foundation_verify.sql
  ```

- The first operation returns E1_DEV_A and FREEPDB1, checks its E1_DEV_A workspace mapping and refuses a mismatch.
- The next operation shows application 810001, APEX Delivery Laboratory, version 1.0.0 and Unavailable.
- The component inventory shows Foundation 1.0.0 installed, Hello/World absent, the maintenance root and zero saved greetings.
- The final operation checks this declared Foundation-only assembly.
- These commands have been executed successfully through native SQLcl.

- Their readable SQL files are [identity](../../deploy/operator/identity.sql), [application inventory](../../deploy/operator/application_inventory.sql), [component/state inventory](../../deploy/operator/component_inventory.sql) and [Foundation verification](../../deploy/operator/foundation_verify.sql).
- They do not call the Python test runner.
- Press Ctrl+D to leave SQLcl when finished.

### 3. Inspect the ownership authority separately

- From the same terminal after leaving the previous session:

  ```bash
  sql -nohistory -noupdates -home "$APEX_CICD_CONNECTIONS" -name lab-control
  ```

- At its SQLcl prompt:

  ```sql
  @deploy/operator/show_reservations.sql
  ```

- Foundation’s initial task is complete and released. The reservation inventory should show no current owner unless a new developer/capture task is active.
- Hello and World have no owner at this checkpoint.
- This authority is in E1_CTRL, outside the application Foundation schema.
- This inspection does not release or change any reservation.
- Leave with Ctrl+D.

### 4. Open Foundation in App Builder and inspect its definition

- This step opens the existing Foundation application.
- It does not ask you to create Hello/World pages or invent a change.
- The version authoring operation described below has already been performed during construction; the current inspection should find 1.0.0.

#### 4.1 Sign in as Developer A

1. In your terminal, retrieve A's Builder password:

   ```bash
   python3 scripts/cicd-password.py DEV_A
   ```

2. Open [App Builder sign-in](http://127.0.0.1:8080/ords/f?p=4550:1).
3. Fill **Workspace** with **E1_DEV_A**.
4. Fill **Username** with **DEV_A**.
5. Fill **Password** with the value printed in step 1.
6. Click **Sign In**.

- Use the developer account here; INTERNAL/ADMIN and LAB_USER have different roles.
- If another workspace is signed in, sign out of that Builder session first.
- If login fails, check the workspace/username and retrieve DEV_A's password again. Do not reset instance credentials.

#### 4.2 Open application 810001

1. On the workspace home, click **App Builder**.
2. Open **APEX Delivery Laboratory**, application **810001**, from the application list.
3. Confirm the application number before editing.
4. Locate the page list on the **application home**.

- If the screen heading says **Edit Application Definition**, click **Cancel** to leave without saving.
- If needed, click **Application 810001** in the upper-left breadcrumb to reach the application home.
- The expected page list contains:
  - **0 — Global Page**: shared page components.
  - **1 — Home**: initial application shell with its guarded Create greeting action.
  - **10 — Greeting history**: immutable snapshot report.
  - **9999 — Login Page**: generated runtime login page.
- Hello, World and history pages are not implemented yet.
- If the page list is empty or the application number differs, return to workspace/application selection. Do not create a replacement application.

#### 4.3 Inspect the application version

1. On the application home, click **Edit Application Definition**.
2. Locate **Version** and check that its value is **1.0.0**.
3. Leave the value unchanged and click **Cancel**.
4. If needed, click **Application 810001** in the upper-left breadcrumb to return to the page list.

- If you accidentally change **Name**, **Version** or another field, use **Cancel** to discard the unsaved edit.
- The earlier construction operation was:
  1. Open the same application-definition form.
  2. Replace **Release 1.0** in **Version** with **1.0.0**.
  3. Click **Apply Changes** to save to the live APEX repository.
- That change has already been saved; do not repeat it for this inspection.
- The display version and database component version are separate metadata. Editing this field alone does not migrate the database or release a component.

#### 4.4 Inspect the Home and Login definitions

1. Leave **Edit Application Definition** with **Cancel**.
2. If needed, click **Application 810001** in the upper-left breadcrumb.
3. On the application home, open **1 — Home** from the page list. Page Designer opens.
4. In the **Rendering** tree, select the page node.
5. Check **Name = Home** and **Title = APEX Delivery Laboratory**.
6. Locate the **APEX Delivery Laboratory** region. No greeting interaction is available yet.
7. Use the application breadcrumb to return to the page list.
8. Open **9999 — Login Page**.
9. In its **Rendering** tree, inspect the login region and its existing controls:
   - **P9999_USERNAME**
   - **P9999_PASSWORD**
   - **P9999_REMEMBER**
   - **LOGIN** button, displayed as **Sign In**.
10. Leave these definitions unchanged; do not create duplicate items.

- **Save** in Page Designer saves page edits to the live APEX application.
- **Apply Changes** in the application-definition form saves application-level edits.
- Neither action exports source or creates a Git commit.
- Use the later capture/review steps to bring an authorized edit into source control.

#### 4.5 Check runtime availability, then continue to SQLcl

1. Open the [application runtime](http://127.0.0.1:8080/ords/f?p=810001:1) in another tab.
2. Check that the page heading is **Application Not Available**.
3. Check that it displays **Foundation assembly: Hello and World are not installed.**
4. Leave availability set to **Unavailable** while Hello/World and their guards are unfinished.
5. Continue to **step 5** below for database migration inspection.
6. Continue to **step 6** for application source capture.

- App Builder can inspect page definitions while runtime access is blocked.
- No artificial page edit is needed before capture.

### 5. Inspect migration state before applying anything

- Connect to lab-dev as in step 2. At the SQLcl prompt, execute each command separately:

  ```sql
  @deploy/operator/identity.sql E1_DEV_A E1_DEV_A
  cd "&REPO_ROOT"
  lb validate -changelog-file db/changelog.xml
  lb status -changelog-file db/changelog.xml
  ```

- Target identity must pass before proceeding. These migration inspections are read-only; the historical Foundation construction task is already released.
- SQLcl can change its script search directory after an @file operation. Chapter 2 passes the Git-discovered shell root into `session_root.sql`; SQLcl `cd "&REPO_ROOT"` restores that location. `git rev-parse` belongs in the shell, not at the SQLcl prompt.
- Validation checks the changelog; status reports unapplied changesets.
- A has 001-foundation and 002-foundation-runtime installed. The current integrated changelog also contains Hello/World: status on A therefore reports 003/004 pending. This is expected for its preserved Foundation-only checkpoint.
- This is the inspection part of the same migration procedure used during construction.

- On the initial empty A area, the next distinct operation was:

  ```sql
  lb update -changelog-file db/changelog.xml
  ```

- First run the SQLcl cd command above again if you have executed another @file since validation.
- The update applies the database migration and records its checksum in DATABASECHANGELOG.
- It has already been performed on A.
- Do not run this historical update command on A against the newer integrated changelog: it would install Hello/World and change the walkthrough checkpoint. C has all four changesets; qualification/release uses its own controlled procedure.
- Never change an already applied migration to force an upgrade: add a new migration for the next version.
- On any validation or migration error, stop and inspect the output before another write.
- Follow the update with these separate inspections:

  ```sql
  @deploy/operator/component_inventory.sql
  @deploy/operator/foundation_verify.sql
  select id, author, filename, exectype from databasechangelog order by orderexecuted;
  ```

- Expected: Foundation 1.0.0, Hello/World absent, maintenance state and the executed 001/002 Foundation migrations.
- This is a prototype Foundation procedure; the general release preflight and promotion procedure is still being built.

### 6. Capture APEX source as an operator

1. Leave SQLcl with **Ctrl+D**.
2. Create the staging directory and identify the current Git base in the same terminal:

   ```bash
   mkdir -p .local-apex/captures/foundation-operator-review
   APEX_CAPTURE_BASE="$(git rev-parse HEAD)"
   APEX_CAPTURE_TASK="foundation-capture-$(date +%s)"
   ```

3. Read the bounded capture operation before running it:

   ```bash
   cat deploy/operator/capture_current_foundation.sql
   ```

4. Execute that native SQLcl operation:

   ```bash
   sql -nohistory -noupdates -home "$APEX_CICD_CONNECTIONS" -name lab-dev \
     @deploy/operator/capture_current_foundation.sql "$APEX_CAPTURE_BASE" \
     "$PWD/.local-apex/captures/foundation-operator-review" "$APEX_CAPTURE_TASK"
   ```

5. Check the actual export output for application **810001 / E1_DEV_A**, f810001/install.sql and **Foundation capture task released.**
6. Leave SQLcl with **Ctrl+D**, then continue to source review.

- The operation acquires a fresh Foundation capture reservation, selects A's workspace, exports with the documented native profile and releases that reservation. It does not reuse the completed construction task's generation.
- The export uses **-split -skipExportDate -expOriginalIds -expSupportingObjects N**; database changes remain separately managed migrations.
- A conflicting reservation or Oracle error stops the operation. If interrupted after acquisition, inspect the authority before any retry; do not assume a timeout releases ownership.
- Capture affects staging only. A source diff still requires review before acceptance.

### 7. Review the captured changes before accepting source

- In the terminal:

  ```bash
  git status --short
  diff -ru apex/f810001 .local-apex/captures/foundation-operator-review/f810001
  ```

- For diff, status 0 means identical; status 1 means differences to review.
- A retains the accepted Foundation-only checkpoint e9a490f. The current integrated source may additionally contain Hello/World work; compare A against its recorded Foundation baseline and do not accept apparent component removals from an older private area. Any live edits require review.
- Review every additional difference rather than assuming it belongs to this task.
- Do not copy the staging tree over the source until its component scope and deletions have been checked.
- The controlled source reconciliation and cross-area import steps are still under construction.

- This sequence uses the native Oracle export operation.
- The bounded capture.sql convenience script combines its preconditions and export, but it is not required to understand or perform these steps.

### 8. Continue through the remaining delivery stages

- The operator journey now includes task reservation, private-area preparation/capture, source acceptance, immutable build, initial/patch qualification, TEST promotion and post-deployment verification. Broader alternatives remain unproved.
- Each will state its target, required input, command, visible result and stop condition.
- The pipeline-stage list at the end tracks what works and what remains under construction.

- For another area's inventory, connect with lab-dev-b, lab-dev-c, lab-qualify or lab-test and run the same application_inventory.sql.
- After infrastructure installation there are no project schemas/workspaces. Explicit project/area onboarding follows; after readiness, all five lab applications remain absent. After B, B contains Foundation plus Hello; after C, C contains the published complete 1.0.0 development assembly; after F, qualification and TEST contain Hello 1.0.1 over Foundation/World 1.0.0.
- Foundation is installed in A/B/C, qualification and TEST.

## Developer A — Foundation

- Open [App Builder](http://127.0.0.1:8080/ords/f?p=4550:1), enter workspace E1_DEV_A and username DEV_A. Retrieve that password locally:

  ```bash
  python3 scripts/cicd-password.py DEV_A
  ```

- The deployed application is **APEX Delivery Laboratory**, ID 810001.
- It contains global, Home and Login pages.
- Its [runtime endpoint](http://127.0.0.1:8080/ords/f?p=810001:1) currently displays “Foundation assembly: Hello and World are not installed.” This is the intended blocked state during assembly.
- Use App Builder to inspect the application; a working greeting is not available yet.

- The database schema is E1_DEV_A and its saved SQLcl connection is lab-dev. Foundation's installed component version is 1.0.0. Check the actual application metadata:

  ```bash
  sql -nohistory -noupdates -home "$APEX_CICD_CONNECTIONS" -name lab-dev
  ```

- Then at the SQLcl prompt:

  ```sql
  @deploy/operator/application_inventory.sql
  ```

- The query shows the application ID, name, alias, current application version and availability.
- The current application and Foundation versions are both 1.0.0; Hello and World remain explicitly absent.

## Developer B — Hello

- Use the same [App Builder sign-in](http://127.0.0.1:8080/ords/f?p=4550:1), workspace E1_DEV_B and username DEV_B:

  ```bash
  python3 scripts/cicd-password.py DEV_B
  sql -nohistory -noupdates -home "$APEX_CICD_CONNECTIONS" -name lab-dev-b
  ```

- At the SQLcl prompt, run @deploy/operator/application_inventory.sql and leave with Ctrl+D.
- The schema is E1_DEV_B and the saved connection is lab-dev-b.
- Application 810002 now contains Foundation plus Hello pages 100/101 and 110/111. Its runtime is blocked while World is absent.
- Open http://127.0.0.1:8080/ords/f?p=810002:1 to see the Hello assembly message. This is not a complete release.

## Developer C — World

For an interrupted results walkthrough already at C's restricted-verification checkpoint, use `bash scripts/cicd-walkthrough-C_world.sh --resume-verification` and follow [C's runtime verification steps](cicd-walkthrough.md#c-deliver-world-and-complete-the-assembly). This checks retained ownership/state and repeats no migration/import; other partial states are not repaired by this command.

- Use [App Builder](http://127.0.0.1:8080/ords/f?p=4550:1), workspace E1_DEV_C and username DEV_C:

  ```bash
  python3 scripts/cicd-password.py DEV_C
  sql -nohistory -noupdates -home "$APEX_CICD_CONNECTIONS" -name lab-dev-c
  ```

- At the SQLcl prompt, run @deploy/operator/application_inventory.sql and leave with Ctrl+D.
- The schema is E1_DEV_C and the saved connection is lab-dev-c.
- Application 810003 now contains Foundation, Hello and World, including World pages 200/201 and 210/211. It is published after restricted browser verification; ordinary LAB_USER can now create greetings and view saved history.

## Qualification and TEST

- Qualification uses workspace/schema E1_QUALIFY, connection lab-qualify and reserved application ID 810004.
- This area is disposable.
- TEST uses workspace/schema E1_TEST, connection lab-test and reserved application ID 810005; it is retained.
- Qualification application 810004 and TEST application 810005 contain the qualified/promoted 1.0.1 application release: Foundation/World 1.0.0, Hello 1.0.1.
- Both runtimes are published for LAB_USER: [qualification](http://127.0.0.1:8080/ords/f?p=810004:1) and [TEST](http://127.0.0.1:8080/ords/f?p=810005:1).

```bash
sql -nohistory -noupdates -home "$APEX_CICD_CONNECTIONS" -name lab-qualify
```

- At the SQLcl prompt, run @deploy/operator/application_inventory.sql and leave with Ctrl+D. Repeat with -name lab-test to inspect TEST separately.

- LAB_USER is the ordinary runtime account and VERIFIER is the controlled verification account, already created within each workspace.
- Retrieve their passwords when the corresponding application is ready:

  ```bash
  python3 scripts/cicd-password.py LAB_USER
  python3 scripts/cicd-password.py VERIFIER
  ```

- These accounts are not App Builder developers.
- Use DEV_A/B/C for authoring in their own workspaces.
- The instance administrator uses [APEX Administration Services](http://127.0.0.1:8080/ords/apex_admin), workspace INTERNAL and username ADMIN; its local password is available with python3 scripts/cicd-password.py APEX_ADMIN_PASSWORD.
- Passwords remain in the protected, ignored local credential files rather than this guide.

## Supporting tests — inspect one target

- Check A's actual connected database identity and workspace association:

  ```bash
  python3 scripts/cicd-isolation.py identity lab-dev
  ```

- It executes SELECT USER and SYS_CONTEXT for the PDB, queries APEX_WORKSPACE_SCHEMAS, then asserts E1_DEV_A / FREEPDB1 / E1_DEV_A.
- Expected output includes the returned values and PASS identity.
- It does not install or provision anything.
- Replace lab-dev with another named connection above to inspect that area.

- Show the complete SQL without executing it:

  ```bash
  python3 scripts/cicd-isolation.py show identity lab-dev
  ```

- The source is [identity.sql](../../deploy/checks/identity.sql).
- Each operation has a visible SQL file; the helper selects the configured identity, executes that one operation and reports the actual result.

## Supporting tests — atomic isolation operations

- First create or retain the probe table in each schema. These are separate operations using each area's own credentials:

  ```bash
  python3 scripts/cicd-isolation.py create-probe lab-dev
  python3 scripts/cicd-isolation.py create-probe lab-dev-b
  ```

- [create_probe.sql](../../deploy/checks/create_probe.sql) checks USER_TABLES and creates E1_PRIVATE_PROBE only when absent.
- It neither clears existing rows nor modifies application tables.
- The table has one numeric primary-key column.

- Next attempt the read as A:

  ```bash
  python3 scripts/cicd-isolation.py deny-read lab-dev lab-dev-b
  ```

- [deny_read.sql](../../deploy/checks/deny_read.sql) attempts SELECT COUNT(*) FROM E1_DEV_B.E1_PRIVATE_PROBE.
- Output shows the connected schema, statement, expected rejection and actual Oracle error.
- PASS means Oracle denied the read with ORA-00942 or ORA-01031.
- An accessible table is a failed isolation test.

- Attempt the write separately:

  ```bash
  python3 scripts/cicd-isolation.py deny-write lab-dev lab-dev-b
  ```

- [deny_write.sql](../../deploy/checks/deny_write.sql) attempts INSERT INTO E1_DEV_B.E1_PRIVATE_PROBE VALUES (1).
- An unexpectedly successful insert is rolled back and the test fails.
- The expected Oracle rejection is printed explicitly.
- Show either full SQL body before running it with the show command, for example:

  ```bash
  python3 scripts/cicd-isolation.py show deny-write lab-dev lab-dev-b
  ```

- The combined isolation test is a convenience that performs probe creation and five read/write pairs: A→B, B→C, C→qualification, qualification→TEST and TEST→A.
- It does not prove every possible pair or browser access control.
- The individual commands above let you perform and inspect each operation yourself.

## How the pipeline is being built

- The selected pipeline consists of the following distinct stages.
- Only the operations marked working have been executed successfully so far; later commands are added here when implemented rather than presented as working examples prematurely.

1. **Prepare and identify the area — working.** Provision its schema/grants, workspace association, developer/runtime users and saved connection; inspect actual identity before writes. The [onboarding chapters](cicd-walkthrough.md#provision-each-assigned-area) separate privileged one-area provisioning from developer-side private connection setup.
2. **Reserve the component — working for Foundation.** The control package records owner, task, Git base and generation before managed work. It lives in E1_CTRL outside application migrations. A's initial reservation is released; inspection does not acquire ownership. General acquisition/release examples will accompany the completed task handover.
3. **Author Foundation — working initial assembly.** Liquibase validates db/changelog.xml, applies 001-foundation, then assertions check Foundation 1.0.0, absent Hello/World and root maintenance. deploy/foundation.sql records the bounded initial construction operation with its ownership token. That task is now closed: do not replay it as a general release installer.
4. **Capture and review — initial capture working.** SQLcl exports the application to staging; source is reviewed in Git. Repeated unchanged capture matches all 38 files. The reusable ownership/scope-aware capture command and private-copy normalization are still being completed.
5. **Author Hello and World — working development assembly.** B and C worked sequentially in private copies, captured native source and integrated reviewed contributions. No completed component application is supplied as a seed.
6. **Validate candidate, then accept source.** Validate the combined revision before local integration. Preserve its review/check evidence. Remote PR publication is outside the current local execution.
7. **Build once.** Package the accepted revision, migrations and component/compatibility metadata into an immutable archive. Record its hash and source revision.
8. **Qualify initial exact bytes.** Import that archive into the disposable area and verify versions and greeting/history. The patch qualifies from both empty and initial 1.0.0 starts.
9. **Preflight supported TEST upgrade.** Verify compatibility, expected installed revision and live fingerprints before mutation. Reject the incompatible Foundation upgrade or unexpected APEX drift with a clear reason and unchanged working target.
10. **Promote initial release and verify.** Install the same qualified archive under controlled availability, check behavior/history and installed metadata, then publish readiness. A successful database step alone cannot publish application success.
11. **Demonstrate the patch.** Upgrade Hello from 1.0.0 to 1.0.1 while Foundation and World remain 1.0.0. Show preserved configuration/history and source/artifact/deployment receipts.

- The [construction document](sprint_E.1_implementation.md) records code changes, tests and remaining work.
- The [design](sprint_E.1_design.md) retains acceptance criteria and later experiments.
- Initial commands are retained below for historical reproduction. The later patch and selected protection chapters describe the current live release.


## Use the complete development application

1. Open [C / application 810003](http://127.0.0.1:8080/ords/f?p=810003:1).
2. Sign in as **LAB_USER**. Retrieve only its password locally:

   ```bash
   python3 scripts/cicd-password.py LAB_USER
   ```

3. On **Home**, choose **Hello** and **World**, or leave the configured-default options selected. Press **Create greeting** and see the saved-greeting success message.
4. Open **Greeting history** using the navigation menu. Refresh to verify the new snapshot remains. Earlier snapshots retain the text/prefixes used when saved.
5. Open **Installed components**. Fresh chapter C shows all three at **1.0.0**. After F, qualification and TEST show Foundation **1.0.0**, Hello **1.0.1**, World **1.0.0**.
6. To add a value, open **Hello entries** or **World entries**, press **Create**, enter **Entry Text** and **Active = Y**, then save with **Create**.
7. To change a default or prefix, open the corresponding **Hello configuration** or **World configuration** report. Open its row using the edit icon, select an active default, enter an optional prefix and press **Apply Changes**.
8. Return **Home**, generate another greeting and reopen history. The new settings affect new snapshots; earlier rows remain unchanged.
9. Sign out when finished.

- Expand the menu with **Main Navigation**. Direct entry URLs (a new login may be required): [Hello](http://127.0.0.1:8080/ords/f?p=810003:100), [Hello configuration](http://127.0.0.1:8080/ords/f?p=810003:110), [World](http://127.0.0.1:8080/ords/f?p=810003:200), [World configuration](http://127.0.0.1:8080/ords/f?p=810003:210), [history](http://127.0.0.1:8080/ords/f?p=810003:10), [versions](http://127.0.0.1:8080/ords/f?p=810003:20).
- Blank/oversize entries, deactivating a configured default and editing/deleting history are rejected by database guards.
- The development example values and verification history were entered through the browser; no seed application/business data is distributed.
- Publication used separate identity, ownership, compilation/page/version checks, restricted browser verification and `deploy/operator/publish_development.sql`. These bounded scripts name C and the completed construction task; do not replay them as generic release scripts or reuse closed ownership tokens.
- Initial and patch qualification/TEST publication and the selected incompatible/page-drift rejections are complete. Broader concurrency, maintenance and repair remain open.
- Maintain this chapter with its companion results runner and guide; the existing Foundation operator walkthrough remains a separate detailed view.


## Prepare a repeatable walkthrough

1. For the requested **fresh-start walkthrough**, follow [the explicit infrastructure lifecycle](../../docs/deploy.md#fresh-walkthrough-infrastructure-sequence): prerequisites precheck, named Podman host preparation, complete lab cleanup and database/APEX/ORDS installation.
2. Run these as separate operations, waiting for each PASS:

   ```bash
   bash scripts/cicd-walkthrough-prerequisites.sh
   ```

   ```bash
   bash scripts/cicd-walkthrough-host.sh
   ```

   ```bash
   bash scripts/apex-destroy.sh
   ```

   ```bash
   bash scripts/cicd-walkthrough-apex-init.sh
   ```

3. Cleanup **destroys all lab applications, entries, configuration, greeting history and control receipts**, including TEST. It keeps the named VM, host credentials/tools/source archives and unrelated Podman resources. This deliberate fresh-demo reset is separate from normal data-preserving deployments.
4. After **PASS APEX init**, complete [project control, per-area provisioning, developer configuration and readiness](cicd-walkthrough.md#initialize-project-delivery-control), then start `bash scripts/cicd-walkthrough-A_foundation.sh`. Follow B–H using their own commands in [the main guide](cicd-walkthrough.md). Those stages install/deploy new applications and qualify/promote artifacts in this cycle.
5. If you only want to restore defaults in an existing C application **without deleting history**, use the separately named `bash scripts/cicd-demo-defaults.sh`. Its private evidence retains restore-defaults.sql and before/after history hashes. It is not fresh-start cleanup.

- Do not run A–H after cleanup alone: complete database/APEX installation first.
- A failed installation or application stage stops. Inspect logs/ownership before retry; full cleanup is an explicit restart of the demonstration, not deployment repair.
- Ordinary release result inspection below remains read-only. Broader maintenance/concurrency/repair proofs remain open.

## Initial release: build, qualify and promote

### Inspect or repeat the existing result

1. Position inside the checkout and select the retained archive:

   ```bash
   cd "$(git rev-parse --show-toplevel)"
   archive="$(cat .local-apex/releases/initial-selected.txt)"
   python3 scripts/cicd-artifact.py inspect "$archive"
   ```

2. Verify qualification and TEST without redeploying:

   ```bash
   bash scripts/cicd-qualify.sh "$archive"
   bash scripts/cicd-promote.sh "$archive" lab-test
   ```

3. These initial-only commands apply while the live targets still contain 1.0.0. After the patch, use `bash scripts/cicd-patch-result.sh lab-test` instead; initial-only verification correctly refuses a newer live release. For a matching initial installation, expect **ALREADY DELIVERED** after actual version, readiness and live APEX fingerprint checks. A mismatch fails without overwriting. These commands preserve configuration/history and do not repeat migration/import.
4. Open [TEST](http://127.0.0.1:8080/ords/f?p=810005:1) as **LAB_USER**. Follow the entry/configuration/greeting/history operations in [the runtime chapter](#use-the-complete-development-application), using TEST instead of C.
5. Keep fresh-demo cleanup separate: it destroys the entire lab, including TEST. Do not use it for ordinary result inspection or data-preserving release work. Optional `cicd-demo-defaults.sh` changes only C defaults and preserves history.

### First installation on an empty target

1. Validate the clean candidate with `bash scripts/cicd-candidate-check.sh`, integrate the accepted commit locally and build once with `python3 scripts/cicd-artifact.py build`. Preserve the archive/sidecar; never overwrite or rebuild it for promotion. The builder records the selected archive path above.
2. Follow [the infrastructure procedure](../../docs/deploy.md#disposable-qualification-lifecycle) for any required disposable qualification reset and control bootstrap. Inspect active ownership first. Never reset TEST. Normal reruns use existing-result verification. An explicitly requested disposable initial reconstruction is supported for patch-baseline qualification, with a new attempt epoch and the first qualification receipt retained.
3. Run `bash scripts/cicd-qualify.sh "$archive"`. On an empty target the wrapper pauses before each operation and prints native SQLcl output. It refuses active/interrupted attempts and never resets a target automatically.
4. For individual operations, execute `bash scripts/cicd-release-step.sh "$archive" lab-qualify status 0`, inspect its current epoch and use that value for **admit**. Admission increments it; all following operations require the resulting epoch. Our completed run used expected epoch 1 → actual 2 for qualification, and expected 0 → actual 1 for TEST. These are historical values, not repeat-run instructions.
5. Run each atomic operation separately with `bash scripts/cicd-release-step.sh "$archive" lab-qualify OPERATION EPOCH`, substituting **admit**, then **migrate**, **import**, **units**, **verify**. Use the pre-admission epoch only for admit. Migrate exposes SQLcl `lb validate/update/status`; import executes unchanged native split APEX source mapped through public APIs.
6. At verify, open qualification as **VERIFIER**. Using the runtime chapter, create active Hello/World entries, configure both defaults, create **Hello World**, then reopen and refresh its saved history. Retrieve only that account's password with `python3 scripts/cicd-password.py VERIFIER`.
7. Run the **publish** operation with the admitted epoch, then `bash scripts/cicd-release-result.sh "$archive" lab-qualify`. Verify ordinary LAB_USER access afterward.
8. Run `bash scripts/cicd-promote.sh "$archive" lab-test` against empty TEST. It uses the identical archive, requires its qualification receipt and repeats the visible migration/import/unit/integrity/VERIFIER/publication stages. Do not rebuild between targets.

- These primitive stages and both browser flows passed. The fresh-install wrapper's human keypress journey is not a separate second-operator reproduction acceptance.
- Admission supports **empty application targets only**, retaining the isolation probe. An existing application/schema requires the future supported upgrade path.
- SQL is extracted from the verified archive on every operation; archive membership/content/configuration and controller identity are checked before execution. Private transcripts remain under `.local-apex/releases/`.
- Native availability changes the APEX checksum, and APEX_EXPORT starts a read-only transaction. Publication therefore prepares native AVAILABLE while the external session-initialization gate still restricts business requests, computes the final checksum in a fresh transaction, then commits successful receipt and external ready state together. Login page access remains available; VERIFIER alone can exercise business pages during verification.
- This initial-install proof does not establish full upgrade request draining, schema-drift detection, repair or concurrent deployment safety.
- Twenty VERIFIER greeting snapshots were explicitly created **after** TEST publication with `tests/sql/prepare_history_sentinels.sql` for later upgrade comparisons. The repeatable fixture appends only missing verification snapshots; it never distributes seed data or deletes existing history.

### Recorded initial result before the fresh reset

These are historical observations from the earlier database. Fresh D/E obtain new receipts; discover epochs from current status rather than copying these values.

- Source commit: `0f7c500e064e4f262a42fb74f4984eb0e4349c88`.
- Qualified/promoted archive SHA-256: `6a1da4a940586541cbb034277605d7ed36e5d1ad305554f9a2fe4c64cd59411c`.
- Qualification 810004 epoch 2 and TEST 810005 epoch 1 are **ready**; Foundation/Hello/World are all **1.0.0**.
- The earlier qualification publication experiment failed before promotion. Its archive and failed attempt remain retained; no failed-release repair acceptance is inferred.
- Maintain this chapter, the release wrappers and the results walkthrough together as one operator artifact.

## Hello 1.0.1 operator stages

1. The correction normalizes all surrounding whitespace in Hello entries and rejects whitespace-only text. Existing entry text, settings and immutable greeting snapshots are retained. Foundation/World remain 1.0.0; migration **005-hello-1.0.1** adds validation without editing migrations 001–004.
2. Select the new archive after candidate validation/local integration/build: `archive="$(cat .local-apex/releases/patch-selected.txt)"`. The current source manifest is `release/manifest.json`; retained initial archives keep their original manifest filename.
3. Execute **one operation at a time** with `bash scripts/cicd-patch-step.sh "$archive" TARGET OPERATION EPOCH START`. TARGET is lab-qualify or lab-test; START is empty (qualification only) or 1.0.0. Use the currently observed epoch for preflight/admit; admission increments it, and subsequent operations use the new epoch.
4. Operations are **preflight**, **admit**, **migrate**, **import**, **units**, **verify**, **publish** and **result**. Preflight is read-only: compatibility, identity, supported initial artifact and live fingerprint. Admission locks the application state row before maintenance and commits durable attempt ownership; existing guarded mutations must finish first. Migration exposes native SQLcl/Liquibase commands; import maps the existing target and executes unchanged native source.
5. At **verify**, open the printed target URL as VERIFIER, create a greeting and refresh history. After **publish**, open it as LAB_USER and repeat. **result** verifies matching versions/artifact/fingerprint without reinstalling; use START **1.0.0** for this existing-result check, including after fresh qualification. A failed operation retains ownership/partial state; no automatic reset or success is performed.
6. Qualification requires two successful executions of the **same archive**: an empty reconstruction, then an upgrade over the accepted initial release reconstructed in the disposable area. Follow [the scoped qualification lifecycle](../../docs/deploy.md#disposable-qualification-lifecycle); never reset TEST. The initial qualification receipt is retained if its archive is reconstructed again; each new attempt keeps its own epoch/history.
7. Only after both qualification starts pass may TEST admit the patch over its unchanged initial baseline. Capture retained data first with `python3 scripts/cicd-preservation.py capture lab-test FILE`, using a new private evidence filename; compare afterward with `python3 scripts/cicd-preservation.py compare lab-test FILE`. New history/entries may append; every old field and complete configuration must match.

- Fresh and initial-baseline upgrade qualification, TEST promotion and both selected rejection demonstrations passed. Native stage logs, field comparisons and runtime screenshots are linked in the construction/test evidence.
- The mutation-state lock does not establish complete read-request draining, asynchronous request fencing or stale verifier exclusion. Those broader maintenance tests remain pending.

## Selected deployment protection operations

1. After patch publication, run `bash scripts/cicd-protection-check.sh compatibility`. It submits `release/proposals/foundation-major.json` to the actual patch preflight compatibility gate. Hello/World still require Foundation 1.0.0; the proposed 2.0.0 contract must reject before a target connection or deployment write.
2. For the drift demonstration, run `python3 scripts/cicd-drift-demo.py inject`. This is an explicit, TEST-only test-fixture operation, outside release delivery. It first verifies the current patch receipt/fingerprint, saves a native TEST export and data snapshot, then imports the separately authored native Home-page drift fixture using TEST's existing ID offset. The component version remains unchanged. The fixture is not a release artifact or business seed.
3. Open TEST to see **DIRECT CHANGE - deployment must stop**. Then run `bash scripts/cicd-protection-check.sh drift`. The actual preflight must reject its live-fingerprint mismatch before maintenance, migrations or release import. The check compares versions, definitions, data/settings and control receipts before/after rejection. An arbitrary error does not pass.
4. Open TEST again to see that rejection did not overwrite the changed page or history.
5. Restore explicitly with `python3 scripts/cicd-drift-demo.py restore`. It refuses an unexplained additional definition/release change, imports the saved original native TEST definition with the same offset and requires the **original successful fingerprint**. All data/settings present immediately before restoration must survive. This is controlled test cleanup, not failed-deployment repair or silent drift adoption.
6. Reopen TEST and confirm the banner is gone and history remains. An interrupted fixture operation remains recorded privately for inspection; do not reset retained TEST.

- Run this controlled fixture sequence with other TEST authoring/deployment stopped. It replaces only APEX definitions; concurrent application-definition authoring is unsupported during the demonstration.
- The Product Owner results walkthrough calls these operations and pauses at runtime URLs. No App Builder inspection is needed for that walkthrough.

### Read the current patch result

1. Run `bash scripts/cicd-patch-result.sh lab-qualify` or `bash scripts/cicd-patch-result.sh lab-test`. The helper discovers the current epoch and invokes the verified archive's result check. It never reinstalls.
2. After upgrading the live targets, initial 1.0.0 receipts remain historical evidence. The initial-release result helper appropriately rejects a live 1.0.1 target; do not interpret that as an initial deployment failure.
3. The optional `tests/sql/prepare_qualification_fixture.sql` creates twenty verification snapshots only in a freshly reconstructed disposable baseline, after restricted verification is enabled. It is separate test preparation, not release seeding. It refuses a nonempty baseline; the browser verification still follows.

### Current patch result and repeatable demonstration

1. Patch source is `752eb47ec59daeb625c3849bfed87fc230295e20`; qualified/promoted SHA-256 is `200ebefff13e87600699adfebbbe71158962dc80a02d1b8e6dbd9a829dd9e1ce`.
2. Before the fresh reset, patch qualification used epochs **3/5** and TEST **2**. These are historical values. Fresh D–F discover and use the new database epochs through the native status/admission operations; do not copy an old epoch into a new command.
3. Current results: `bash scripts/cicd-patch-result.sh lab-qualify`, then `bash scripts/cicd-patch-result.sh lab-test`. Normal repeat commands verify without reinstalling.
4. Current-cycle pre-upgrade baselines are `.local-apex/releases/test-initial-preservation.json` and `.local-apex/releases/qualification-initial-preservation.json`. E/F capture newly created rows/settings there and print their actual counts. Cleanup moves earlier baselines out of the active cycle. The earlier 21-row and **[Q] / [W]** evidence remains historical; it is not restored into this fresh demonstration.
5. For a new demonstration, follow the [fresh infrastructure sequence](../../docs/deploy.md#fresh-walkthrough-infrastructure-sequence), then the [A–H walkthrough](cicd-walkthrough.md#run-one-chapter-at-a-time). It constructs the reviewed source, qualifies/promotes initial and patch archives in the new database and demonstrates both protections. For read-only inspection of an already delivered patch, use the result commands in step 3 instead. Imports may require re-login.
6. To run the selected registered assertions without human checkpoints, use `bash tests/run.sh --integration --new-only tests/manifests/patch_protections.manifest`. This includes controlled TEST page-fixture replacement/restoration; stop other TEST authoring/deployment first. Expected result: **3 tests, 0 failures**.
7. Historical initial-only evidence remains valid for that release. Current targets are newer; do not reinstall/downgrade them to make an old result check pass.

- This is the selected patch/protection slice. Full IT-1 candidate reconstruction, broader schema drift, concurrency, complete request/verifier fencing and failed additive deployment repair remain open.

- If a walkthrough is stopped while its drift fixture is active, run `python3 scripts/cicd-drift-demo.py restore` explicitly before restarting. Settings-only C preparation never overwrites TEST drift or repairs an interrupted deployment. Fresh-demo cleanup instead deliberately discards the entire lab. If restoration reports an unexplained additional change, inspect the retained journal/logs instead of resetting TEST.
