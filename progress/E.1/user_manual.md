# E.1 — Operator guide

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
- A/B retain incomplete assembly checkpoints; C has the working Foundation/Hello/World development application. The retained TEST release remains under construction.
- Use the areas below to inspect the actual current state.
- This guide is updated as construction makes each operation usable.

## Guided execution — this manual and its script

1. Open a terminal in the project checkout.
2. Start the guided walkthrough:

   ```bash
   bash scripts/cicd-walkthrough.sh
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
   bash scripts/cicd-walkthrough.sh --preflight
   ```

- This is a local file/tool check. Database access is checked in walkthrough chapter 2.

### Unattended rehearsal

1. Execute the current CLI operations without keypress pauses:

   ```bash
   bash scripts/cicd-walkthrough.sh --rehearse
   ```

- Rehearsal still connects to Oracle and exports the live application into staging.
- It skips password display, browser interactions and human review, and labels those skips explicitly.
- A successful rehearsal does not establish browser acceptance or acceptance of a source diff.

### Maintain the pair as one artifact

- **This manual and [cicd-walkthrough.sh](../../scripts/cicd-walkthrough.sh) are one operating artifact. Always update and review both together.**
- Keep the numbered/bulleted format for actions, fields, expected results and stop conditions.
- When a chapter, command, URL, prerequisite or expected outcome changes, reconcile the matching script stage and manual chapter in the same increment.
- Browser instructions are read from this file; executable commands are explicit in the script and must remain equivalent to the documented operator operations.
- Keep pending chapters labelled pending in both. Do not add a script stage that silently bypasses a manual check.
- Validate chapter mapping and script syntax, rehearse changed CLI operations, and inspect changed browser instructions before calling the pair ready.

## Operator walkthrough — current working operations

- This is the primary operating path.
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

- The remaining operator journey will provide distinct task reservation, Git branch, private-area preparation, source acceptance, immutable build, qualification, TEST preflight/promotion and post-deployment verification operations.
- Each will state its target, required input, command, visible result and stop condition.
- The pipeline-stage list at the end tracks what works and what remains under construction.

- For another area's inventory, connect with lab-dev-b, lab-dev-c, lab-qualify or lab-test and run the same application_inventory.sql.
- B contains Foundation plus Hello; C contains the published complete development assembly; TEST has no application. Qualification contains Foundation only.
- Foundation is installed in A, B, C and the Foundation-only qualification experiment.

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
- Qualification currently contains the reconstructed Foundation-only application 810004 for the initial import experiment. TEST still has no application.
- Qualification’s current runtime remains blocked for incomplete assembly; this is not a qualified complete release. TEST has no deployed runtime yet.

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

1. **Prepare and identify the area — working.** Provision its schema/grants, workspace association, developer/runtime users and saved connection; inspect actual identity before writes. The command/API breakdown for provisioning is being separated from the original combined helper.
2. **Reserve the component — working for Foundation.** The control package records owner, task, Git base and generation before managed work. It lives in E1_CTRL outside application migrations. A's initial reservation is released; inspection does not acquire ownership. General acquisition/release examples will accompany the completed task handover.
3. **Author Foundation — working initial assembly.** Liquibase validates db/changelog.xml, applies 001-foundation, then assertions check Foundation 1.0.0, absent Hello/World and root maintenance. deploy/foundation.sql records the bounded initial construction operation with its ownership token. That task is now closed: do not replay it as a general release installer.
4. **Capture and review — initial capture working.** SQLcl exports the application to staging; source is reviewed in Git. Repeated unchanged capture matches all 38 files. The reusable ownership/scope-aware capture command and private-copy normalization are still being completed.
5. **Author Hello and World — working development assembly.** B and C worked sequentially in private copies, captured native source and integrated reviewed contributions. No completed component application is supplied as a seed.
6. **Validate candidate, then accept source — pending.** Validate the combined revision before local integration. Preserve its review/check evidence. Remote PR publication is outside the current local execution.
7. **Build once — pending.** Package the accepted revision, migrations and component/compatibility metadata into an immutable archive. Record its hash and source revision.
8. **Qualify exact bytes — pending.** Import that archive into the disposable area and verify versions and greeting/history. The patch release must also qualify from its declared earlier baseline.
9. **Preflight TEST — pending.** Verify compatibility, expected installed revision and live fingerprints before mutation. Reject the incompatible Foundation upgrade or unexpected APEX drift with a clear reason and unchanged working target.
10. **Promote and verify — pending.** Install the same qualified archive under controlled availability, check behavior/history and installed metadata, then publish readiness. A successful database step alone cannot publish application success.
11. **Demonstrate the patch — pending.** Upgrade Hello from 1.0.0 to 1.0.1 while Foundation and World remain 1.0.0. Show preserved configuration/history and source/artifact/deployment receipts.

- The [construction document](sprint_E.1_implementation.md) records code changes, tests and remaining work.
- The [design](sprint_E.1_design.md) retains acceptance criteria and later experiments.
- The operator guide will gain the exact runnable release commands and deployed TEST URL as those stages are built.


## Use the complete development application

1. Open [C / application 810003](http://127.0.0.1:8080/ords/f?p=810003:1).
2. Sign in as **LAB_USER**. Retrieve only its password locally:

   ```bash
   python3 scripts/cicd-password.py LAB_USER
   ```

3. On **Home**, choose **Hello** and **World**, or leave the configured-default options selected. Press **Create greeting** and see the saved-greeting success message.
4. Open **Greeting history** using the navigation menu. Refresh to verify the new snapshot remains. Earlier snapshots retain the text/prefixes used when saved.
5. Open **Installed components** to see Foundation, Hello and World at **1.0.0**.
6. To add a value, open **Hello entries** or **World entries**, press **Create**, enter **Entry Text** and **Active = Y**, then save with **Create**.
7. To change a default or prefix, open the corresponding **Hello configuration** or **World configuration** report. Open its row using the edit icon, select an active default, enter an optional prefix and press **Apply Changes**.
8. Return **Home**, generate another greeting and reopen history. The new settings affect new snapshots; earlier rows remain unchanged.
9. Sign out when finished.

- Expand the menu with **Main Navigation**. Direct entry URLs (a new login may be required): [Hello](http://127.0.0.1:8080/ords/f?p=810003:100), [Hello configuration](http://127.0.0.1:8080/ords/f?p=810003:110), [World](http://127.0.0.1:8080/ords/f?p=810003:200), [World configuration](http://127.0.0.1:8080/ords/f?p=810003:210), [history](http://127.0.0.1:8080/ords/f?p=810003:10), [versions](http://127.0.0.1:8080/ords/f?p=810003:20).
- Blank/oversize entries, deactivating a configured default and editing/deleting history are rejected by database guards.
- The development example values and verification history were entered through the browser; no seed application/business data is distributed.
- Publication used separate identity, ownership, compilation/page/version checks, restricted browser verification and `deploy/operator/publish_development.sql`. These bounded scripts name C and the completed construction task; do not replay them as generic release scripts or reuse closed ownership tokens.
- Qualification and retained TEST publication, patch and incompatible/drift deployment rejection remain under construction.
- Maintain this chapter with its companion results runner and guide; the existing Foundation operator walkthrough remains a separate detailed view.


## Prepare a repeatable walkthrough

1. Open a terminal anywhere inside the checkout and select its root using Git:

   ```bash
   cd "$(git rev-parse --show-toplevel)"
   ```

2. Run the bounded cleanup/preparation operation before another results demonstration:

   ```bash
   bash scripts/cicd-walkthrough-cleanup.sh
   ```

3. Read each printed SQL operation and its actual result. Preparation refuses active authoring/deployment ownership, incorrect target identities, unsupported component versions or a non-ready C application. It does not repair a failed deployment.
4. Note the private `.local-apex/operator/walkthrough-prepare.*` evidence directory. It holds **restore-defaults.sql**, containing the original Hello/World configuration, plus before/after hashes of every existing history row.
5. C's defaults become active **Hello** / **World**, with empty prefixes. Existing matching entries are reused; only a missing demo entry is created. Other entries and every greeting snapshot remain. Repeating preparation does not add duplicate demo entries.
6. If you want the previous settings back, connect to **lab-dev-c**, verify its identity and run the recorded private restore SQL. It only restores configuration; current default-entry guards still apply.
7. After cleanup reports **PASS preparation**, start the results walkthrough as a separate command. It does not repeat cleanup automatically:

   ```bash
   bash scripts/cicd-developer-walkthrough.sh
   ```

- Neither operation drops/recreates applications, schemas, credentials or Podman resources. Qualification, retained TEST and release/audit history remain untouched. Destructive disposable-area lifecycle operations remain separate in [deploy.md](../../docs/deploy.md).
- `--preflight` on cleanup checks local tools/files only. The walkthrough's `--rehearse` performs CLI checks without browser pauses; run cleanup separately first.
- The implemented A/B/C walkthrough ends with **exit 3** because later release stages are unimplemented. This is an explicit incomplete-pipeline outcome, not failure caused by rerunning a configured system.
- Maintain this chapter, the results chapters and their scripts together.
