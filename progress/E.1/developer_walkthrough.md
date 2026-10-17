# E.1 — Use-case walkthrough: deployment results and protection

## What this walkthrough shows

- This lab simulates work of 3 developers (identified as A, B, and C) dedicated to development of APEX style Hello World application architected as composition of three components: database and two user facing ones.
- The Product Owner sees application outcomes after successful deployments and evidence that wrong deployments are blocked.
- Developer A/B/C operations run inside the guided stages. The Product Owner does not inspect App Builder, page definitions, SQL source or Git diffs in this workflow.
- Show the actual operation output and a short result: **DEPLOYED**, **REJECTED**, **ERROR** or **PENDING**.
- After a successful deployment, show its result in the running application at the printed URL.
- After an expected rejection, show the exact reason, verify the target was not overwritten, then open the application to demonstrate that its prior behavior and saved history remain intact.

## Deep dive

This business-level walkthrough, its [runner](../../scripts/cicd-developer-walkthrough.sh) and the [detailed operator guide](user_manual.md) describe one system. Maintain and review them together as **one artifact**.

## Applied tools and techniques

The deployment has two kinds of source: **APEX application definitions** and **database migrations**. Git keeps both together. Operators use small shell scripts and visible SQLcl commands to assemble and check one application in each target. The working development assembly demonstrates this approach; initial delivery and the compatible Hello upgrade execute verified archives; the selected incompatibility and page-drift rejection scenarios now have executable demonstrations.

### Toolchain and responsibilities

1. **Oracle APEX 24.2 App Builder** authors pages and shared components. **ORDS** serves their browser URLs. A save in App Builder changes the live development application; capture and Git review are separate operations.
2. **SQLcl 25.3 with Java 21** connects through private saved connections, runs explicit SQL/PLSQL and performs native APEX export/import. Capture uses split files, original component IDs, no export date and no supporting-object installation. Oracle-generated export files are executed unchanged. Public APIs such as **APEX_APPLICATION_INSTALL** map the source to a target workspace/schema/application; **APEX_APPLICATION_ADMIN** controls native availability.
3. **Oracle Database and PL/SQL** hold component data, configuration, installed versions and immutable greeting snapshots. Database constraints, packages and triggers enforce the business rules even when a caller bypasses the browser. A separate **E1_CTRL** schema keeps managed task ownership outside ordinary application migrations/imports.
4. **Liquibase through SQLcl** applies ordered database changesets and records their identities/checksums in **DATABASECHANGELOG**. An applied migration is retained unchanged; a later correction needs a new changeset. The application export and database migrations remain distinct parts of the same reviewed source revision.
5. **Git** identifies the reviewed source commit and shows the component diff. Foundation is established first; Hello and World are integrated from bounded private work. The current demonstration used sequential B/C development. Durable task reservations record owner, task, base commit and generation; they are separate from the durable initial-release ownership controls.
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
4. **Repeatability and failure reporting:** cleanup is an explicit separate step, backs up configuration and compares every existing history row before/after preparation. Scripts check Oracle errors and successful completion markers, stop on unexpected failure and show the reason. A failed connection or arbitrary error is not evidence that a bad deployment was correctly rejected.
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
- **Execution status:** this mapping describes intended coverage, not passed acceptance. A/B/C development checks and runtime checkpoints execute. Initial receipts remain verifiable after upgrade; the patch and two selected rejection stages execute. Broader use-case alternatives remain pending.

## Current readiness

- A and B retain their unavailable incomplete checkpoints.
- C, qualification 810004 and retained TEST 810005 run **Foundation 1.0.0 / Hello 1.0.1 / World 1.0.0**. The application release version is **1.0.1**.
- Initial 1.0.0 receipts remain visible as historical delivery evidence. The walkthrough does not downgrade/reinstall retained TEST to replay that earlier release.
- The runner verifies current results, demonstrates both selected rejections and restores its controlled page-drift fixture explicitly. It finishes with exit **0** when these selected stages pass.
- Full E.1 concurrency, complete maintenance fencing and failed-additive-deployment repair remain open. This walkthrough does not close the sprint.

## Run the results walkthrough

1. Open a Bash terminal in the project:

   ```bash
   cd "$(git rev-parse --show-toplevel)"
   ```

2. **Run cleanup/preparation separately before every walkthrough:**

   ```bash
   bash scripts/cicd-walkthrough-cleanup.sh
   ```

3. Wait for **PASS preparation**. Keep the printed configuration backup/restore path. Cleanup preserves greeting history.
4. **Start the results walkthrough:**

   ```bash
   bash scripts/cicd-developer-walkthrough.sh
   ```

5. Read the next developer operation's purpose.
6. Press any key to run it, or **q** to stop.
7. Read the displayed pipeline outcome and any error or rejection reason.
8. When prompted, open the printed **runtime URL** and use the application as described.
9. Press a key to proceed to the next implemented stage.

- No App Builder login or technical inspection is requested.
- An unexpected error stops the workflow.
- An expected negative scenario counts as protected only when the specific rejection and unchanged-target checks pass. A connection error or arbitrary failure is not a successful protection demonstration.
- Browser continuation is not reported as an automated browser test.
- Run with **--preflight** for local tool/file/chapter checks without Oracle access.
- Run with **--rehearse** for the implemented CLI checks without pauses; human viewing is explicitly skipped.
- **--rehearse** executes the CLI stages, including the controlled TEST page fixture/rejection/restoration, without human viewing. It is not read-only. Successful selected coverage ends with status 0; broader E.1 work remains open.

## Prepare a repeatable walkthrough

1. Run `bash scripts/cicd-walkthrough-cleanup.sh` as the separate preparation step above.
2. Cleanup checks that no managed authoring/deployment is active and that A/B/C still match the supported development checkpoints.
3. It backs up C's configuration, restores active **Hello** / **World** defaults and empty prefixes, then checks that all existing history snapshots are unchanged. Existing matching demo entries are reused.
4. Keep the printed private evidence/restore path if you want to restore your previous settings after the demonstration.
5. Start `bash scripts/cicd-developer-walkthrough.sh` to continue to A's runtime result. The results script does not run cleanup automatically.

- This prepares an existing development demonstration. It does not erase history or rebuild the application from scratch.
- A/B, qualification, TEST, credentials, deployment records and Podman resources are retained.
- For exact SQL and restoration details, see [the operator chapter](user_manual.md#prepare-a-repeatable-walkthrough).

## A. Deliver Foundation

### Developer operations inside the stage

1. Establish Foundation from its accepted source and database changes.
2. Verify installed Foundation version, absent Hello/World and blocked incomplete assembly.
3. Show the real operation result.

- The current implementation performs only checks of the already existing Foundation, not steps to redeploy it.
- Internal checks use lab-dev and lab-control; their output is visible but does not require Product Owner technical inspection.

### Product Owner result

1. Open [A's runtime](http://127.0.0.1:8080/ords/f?p=810001:1).
2. See **Application Not Available** and **Foundation assembly: Hello and World are not installed.**
3. Continue in the terminal.

- The useful result at this stage is protection from using an incomplete application.
- This maintenance screen does not prove protection against an incompatible or drifted deployment. Those scenarios require the later real rejection checks.

## B. Deliver Hello

### Developer operations inside the stage

1. Reserve Hello and prepare B's private area from accepted Foundation source.
2. Apply the reviewed Hello change and its database migration.
3. Capture/validate/integrate the scoped source and verify the resulting assembly.
4. Show the operation result and resulting runtime URL.

### Product Owner result

1. Open [B's runtime](http://127.0.0.1:8080/ords/f?p=810002:1).
2. See that complete-application access remains blocked while World is missing.
3. Continue to World delivery.

- No page-definition review is required.
- Hello's usable behavior is demonstrated in the completed application after World is integrated.
- B is verified as an existing blocked assembly. Replaying its source preparation, authoring and integration remains a separate operator operation.

## C. Deliver World and complete the assembly

### Developer operations inside the stage

1. Prepare C from the accepted Foundation-plus-Hello baseline.
2. Apply and integrate the reviewed World change and migration.
3. Verify the complete Foundation/Hello/World assembly before publishing readiness.
4. Show the resulting application URL and installed versions.

### Product Owner result

1. Open [C's working application](http://127.0.0.1:8080/ords/f?p=810003:1) and sign in as **LAB_USER**.
2. Retrieve its local password with `python3 scripts/cicd-password.py LAB_USER` if needed.
3. Select **Hello** and **World**, then press **Create greeting**. See **Hello World — saved to history.**
4. Open **Greeting history** in the navigation menu. Refresh and confirm the new row and earlier snapshots remain.
5. Open **Installed components** and see Foundation **1.0.0**, Hello **1.0.1** and World **1.0.0**.
6. To try your own data, follow the [runtime instructions](user_manual.md#use-the-complete-development-application) for entry/configuration pages.
7. Continue in the terminal to qualification and TEST results.

- The terminal shows the current versions **1.0.0 / 1.0.1 / 1.0.0** and actual successful verification output.
- The first slice runs B/C sequentially; it does not claim concurrent-development proof.
- C is a development result, not a qualified release or retained TEST promotion. Browser-created verification examples remain in its history; application exports contain no business seed.

## D. Qualify the initial release

1. Read the initial archive verification and historical qualification receipt in the terminal.
2. Open [qualification](http://127.0.0.1:8080/ords/f?p=810004:1) as **LAB_USER**. The live area now contains the later patch; initial delivery is shown through its retained receipts.
3. Continue to the initial TEST receipt.

- Initial source: `0f7c500e064e4f262a42fb74f4984eb0e4349c88`; initial archive SHA-256: `6a1da4a940586541cbb034277605d7ed36e5d1ad305554f9a2fe4c64cd59411c`.
- The first initial qualification used epoch 2. A later disposable reconstruction at epoch 4 supplied the baseline for patch-upgrade qualification. Both successful attempts remain retained.

## E. Promote the same initial artifact to TEST

1. Read the successful historical TEST epoch-1 receipt for the **same initial archive hash**.
2. Open [TEST](http://127.0.0.1:8080/ords/f?p=810005:1) as **LAB_USER**. It now runs 1.0.1; this stage does not reinstall or downgrade it.
3. Continue to the current patch result and preservation checks.

- The initial archive and receipts are retained unchanged. Qualification/TEST runtime data is not packaged business seed.
- Retrieve the local password with `python3 scripts/cicd-password.py LAB_USER` if needed. Native imports may require re-login.

## F. Deliver the compatible Hello patch

1. The terminal verifies the current qualification and TEST artifact, installed versions and live APEX fingerprints.
2. Read the passing field-level comparison: every earlier greeting snapshot, entry and setting remains unchanged. New greetings may append.
3. Read the correction check: tab/newline-padded text normalizes; whitespace-only Hello text rejects. Its test changes roll back.
4. Open [TEST](http://127.0.0.1:8080/ords/f?p=810005:1), sign in as **LAB_USER**, select **Hello/World** and **Create greeting**.
5. Reopen **Greeting history**, refresh and see the new greeting alongside earlier snapshots.
6. Open **Installed components**: **Foundation 1.0.0 / Hello 1.0.1 / World 1.0.0**. The footer shows application release **1.0.1**.
7. Continue to the incompatible deployment proposal.

- Patch source: `752eb47ec59daeb625c3849bfed87fc230295e20`.
- Patch SHA-256: `200ebefff13e87600699adfebbbe71158962dc80a02d1b8e6dbd9a829dd9e1ce`.
- Identical bytes passed fresh qualification (epoch 3), baseline-upgrade qualification (epoch 5), then TEST upgrade (epoch 2). Qualification also preserves explicit **[Q] / [W]** prefixes; TEST retains its own settings.
- Repeating this result stage verifies the installed release without migration/import. Detailed fresh/upgrade operations are in the [operator guide](user_manual.md#hello-101-operator-stages).

## G. Reject an incompatible database upgrade

1. Press a key to submit the Foundation **2.0.0** proposal to the deployment compatibility gate.
2. Read **REJECTED INCOMPATIBLE: Hello requires Foundation 1.0.0; proposed Foundation 2.0.0**. World has the same declared Foundation requirement.
3. Read the unchanged-target verification: definitions, versions, entries, settings, history and control receipts match before/after rejection. Maintenance, migrations and import were not entered.
4. Open [TEST](http://127.0.0.1:8080/ords/f?p=810005:1), create a greeting and reopen history. The current release still works.
5. Continue to the controlled page-drift demonstration.

- This is a rejected deployment proposal; no destructive Foundation 2.0.0 migration is constructed or executed.
- The accepted patch above proves the pipeline also admits a supported change.

## H. Reject deployment over unexpected live change

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

## Maintain this artifact

- Always change this document and its own runner together.
- Use numbered actions, short outcome bullets and runtime URLs.
- Keep developer mechanics inside the stage; retain their real output for diagnosis.
- Add **DEPLOYED** or **REJECTED** only after the corresponding operation and verification exist.
- Keep unproved broader capabilities **PENDING** and preserve the separate detailed operator walkthroughs.
- The [accepted design](sprint_E.1_design.md) remains the source for the positive patch, incompatibility and drift acceptance criteria.
