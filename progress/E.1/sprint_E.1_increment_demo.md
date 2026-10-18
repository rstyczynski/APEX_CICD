# From Git to APEX — guided presentation walkthrough

Use this guide beside the [PowerPoint presentation](sprint_E.1_increment_demo.pptx). It follows the important parts of the [A–H use-case walkthrough](cicd-walkthrough.md), with slide references, commands, visible results and the next decision. The [operator manual](user_manual.md) provides the deeper SQL operations; the [handover](sprint_E.1_handover.md) records the results and review status.

## What you will see

**Slides 1–11.** Follow one Foundation/Hello/World application through private development areas, a Git-built release archive, integration_test and user_acceptance_test. Then inspect a compatible Hello patch, a rejected Foundation upgrade and a real unexpected page change.

The [draw.io model](model.drawio) supplies the lifecycle and integration-test diagrams. The slides adapt those diagrams into editable PowerPoint objects. Foundation owns composition/history/state; Hello and World each own entries/configuration and both depend on Foundation. The development team/Packager releases the reviewed source package. The Deployer installs and validates it in integration_test, then promotes those same bytes to UAT.

The selected Oracle toolchain is APEX/ORDS, SQLcl with Java, SQLcl's bundled Liquibase, E1_CTRL SQL packages, Git/archive hashes, and supporting Bash/Python scripts. The same Git repository holds application metadata and migrations. No developer database or business history is copied into a release. Native SQLcl `apex export` captures split application SQL for Git. Deployment uses `APEX_APPLICATION_INSTALL` to map the target and executes the exported `install.sql`; `APEX_EXPORT.GET_APPLICATION` supplies the live drift fingerprint. Database schema changes use separate Liquibase migrations. App Builder authors the definitions and ORDS serves runtime HTTP. APEX Working Copies and Team Development do not perform integration or promotion in this pipeline.

**Current starting state, 2026-10-18:** D/E initial delivery and F patch delivery passed in the assisted operator walkthrough. UAT runs Foundation 1.0.0 / Hello 1.0.1 / World 1.0.0. G passed. H detected the Product Owner's manual Home-page edit. Its Title and region Name still differ from published source; restoration is pending your decision. The read-only handover check confirmed preservation of all fields of 21 earlier history rows, old entries and complete configuration.

Choose how to review:

1. **Use the retained lab:** perform stage 1, inspect existing results using stages 3–7, then start stage 8 at the current drift comparison. Do not rerun A–F over completed stage directories.
2. **Reproduce from scratch:** explicitly choose stage 2, which destroys all lab database state. Then execute A–H in order. This is the previously rehearsed fresh-start path, not a second rebuild performed to prepare these slides.

## Git layout, cooperation and future pipelines

**Slides 8–11.** The Git repository is this actual APEX_CICD checkout. Foundation, Hello and World share its complete `apex/f810001/` source tree, with database migrations in `db/changes/`, release contracts in `release/`, deployment SQL in `deploy/` and target mappings in `config/areas.json`. The [repository and pipeline draft](repo_layout.md#repository-contents) gives the complete layout. Private A/B/C workspaces are runtime areas, not separate source repositories.

The intended cooperation path is scope reservation → independent task branch/private area → native export and migration changes → review and combined-candidate validation → accepted source → immutable release. The current walkthrough replays reviewed sequential revisions. Real parallel Hello/World capture/merge and a hosted pull-request runner remain future validation/automation work.

APEX split SQL exports are text and can be diffed/merged by Git. Different pages reduce overlap, while shared definitions, import lists, internal identities and dependencies need joint review. A clean Git merge does not establish semantic correctness: import the complete merged tree in a disposable area and verify it. Keep applied database migrations immutable; review added migrations for ordering/compatibility separately. See the [merge guidance](repo_layout.md#merging-apex-export-files) and [future pipeline proposal](repo_layout.md#future-pipeline-automation).

## 1. Prepare the review session

**Slides 1–11.** Open a Bash terminal inside the checkout. Keep the following CLI commands in this **Terminal A**:

```bash
cd "$(git rev-parse --show-toplevel)"
bash scripts/cicd-walkthrough.sh --preflight
```

1. Look for the A–H chapter/tool/file checks. This is local preflight, not a fresh database acceptance test.
2. Keep a browser open for runtime results and a **Terminal B** at the same Git repository root for password retrieval. Passwords are generated locally; none is printed in this handover or stored in Git.
3. For ordinary application viewing, run in Terminal B:

   ```bash
   python3 scripts/cicd-password.py LAB_USER
   ```

4. Open [UAT application 810005](http://127.0.0.1:8080/ords/f?p=810005:1) and sign in as **LAB_USER**. Use **Installed components** to see the current version triple and **Greeting history** to inspect saved snapshots. The current manual drift changes display text, not these component versions.

Expected result: you can inspect the retained release and follow the presentation without deleting anything. The requirement/actor definitions remain in the [SRS](../../docs/srs.md); assigned outcome evidence is summarized in the [assessment](sprint_E.1_assessment.md).

## 2. Optional fresh infrastructure and onboarding

**Slides 12–13. Fresh replay only.** Skip this stage during retained-lab review. The destruction command removes every lab application, project schema and greeting-history row, including UAT. It preserves host credentials, tools, retained archives/evidence and unrelated Podman resources.

Run each operation separately in Terminal A and wait for success:

```bash
bash scripts/cicd-walkthrough-prerequisites.sh
bash scripts/cicd-walkthrough-host.sh
bash scripts/apex-destroy.sh
bash scripts/cicd-walkthrough-apex-init.sh
```

1. Precheck validates the required host tools and verified installers before destruction.
2. Host preparation initializes the owned Podman environment.
3. Destruction removes only the owned lab resources.
4. Initialization installs and verifies **Oracle Database/APEX/ORDS only**. It must not create project schemas or accounts. Follow installer output with `tail -f .local-apex/apex-install.log` if needed. Wait for **PASS APEX init**.
5. Inspect [Administration Services](http://127.0.0.1:8080/ords/apex_admin) as **ADMIN / INTERNAL** if you want to verify administrative access. Retrieve its password in Terminal B with `python3 scripts/cicd-password.py APEX_ADMIN_PASSWORD`. Runtime accounts do not yet exist at this infrastructure-only checkpoint.
6. Create the separate delivery authority:

   ```bash
   bash scripts/cicd-control-init.sh
   ```

   E1_CTRL stores task reservations, deployment epochs and receipts. It holds no greeting data.

7. Provision each assigned area explicitly:

   ```bash
   bash scripts/cicd-area-provision.sh lab-dev
   bash scripts/cicd-area-provision.sh lab-dev-b
   bash scripts/cicd-area-provision.sh lab-dev-c
   bash scripts/cicd-area-provision.sh integration_test
   bash scripts/cicd-area-provision.sh user_acceptance_test
   ```

8. Configure the three private developer profiles:

   ```bash
   (set -o pipefail; python3 scripts/cicd-password.py E1_DEV_A | bash scripts/cicd-developer-init.sh A --password-stdin)
   (set -o pipefail; python3 scripts/cicd-password.py E1_DEV_B | bash scripts/cicd-developer-init.sh B --password-stdin)
   (set -o pipefail; python3 scripts/cicd-password.py E1_DEV_C | bash scripts/cicd-developer-init.sh C --password-stdin)
   ```

9. Verify effective identities, isolation and the empty starting state:

   ```bash
   bash scripts/cicd-walkthrough-ready.sh
   ```

Expected result: **PASS walkthrough ready**, with empty A/B/C, integration_test and UAT. The maintained native provisioning/destruction procedure and troubleshooting are in [deploy.md](../../docs/deploy.md#fresh-walkthrough-infrastructure-sequence). No new installer version or rebuild is claimed by this handover preparation. This stage supplies the PBI-011.1 / UC-8 prerequisite for the later journey.

## 3. A–C: assemble the development application

**Slide 14.** For fresh replay, run these stages in order in Terminal A, following the keypress pauses:

```bash
bash scripts/cicd-walkthrough-A_foundation.sh
bash scripts/cicd-walkthrough-B_hello.sh
bash scripts/cicd-walkthrough-C_world.sh
```

1. **A / 810001:** Foundation only. Open [A](http://127.0.0.1:8080/ords/f?p=810001:1). Ordinary runtime remains unavailable while dependent components are absent.
2. **B / 810002:** accepted Foundation plus Hello. Open [B](http://127.0.0.1:8080/ords/f?p=810002:1). World is still missing, so the complete application remains unavailable.
3. **C / 810003:** complete Foundation/Hello/World 1.0.0 assembly. The script enables restricted verification. Leave Terminal A waiting.
4. In Terminal B, retrieve the runtime verifier password:

   ```bash
   python3 scripts/cicd-password.py VERIFIER
   ```

5. Open [C](http://127.0.0.1:8080/ords/f?p=810003:1), sign out of another runtime account if needed, and sign in as **VERIFIER**.
   1. Under **Hello entries**, create active **Hello** if missing.
   2. Under **World entries**, create active **World** if missing.
   3. Edit the existing Hello/World configuration rows, select those defaults, leave prefixes empty and save.
   4. On **Home**, press **Create greeting**. Refresh **Greeting history** and confirm exactly **Hello World** by VERIFIER.
6. Return to Terminal A and press a key. A missing example repeats the prompt; unexpected SQL errors stop. Publication retains the ownership and runtime assertion checks.
7. Sign out of VERIFIER, retrieve LAB_USER's password, reopen C as **LAB_USER** and create a greeting. **Installed components** shows three 1.0.0 components. Finish the script's final viewing pause and require **PASS result stage C_world**.

For the retained lab, inspect those existing URLs and their expected availability/version states; do not reinstall them. This is the selected sequential assembly/capture slice of PBI-011.3/.4/.5. It does not prove genuinely parallel development.

## 4. D: integration_test of the initial archive

**Slides 15–16. Fresh replay only:**

```bash
bash scripts/cicd-walkthrough-D_integration_test.sh
```

1. Require completed C. The script selects the initial archive through `.local-apex/releases/initial-selected.txt` and verifies its hash, members and accepted source identity.
2. Read the target identity and current epoch: **E1_INTEGRATION / application 810004**.
3. Admit the empty target. The control authority records the owned attempt and advances its epoch.
4. Step through **migrate → import → units → verify**. SQLcl/Liquibase applies the archive's migrations; the native import maps its unchanged APEX source to this target. Integrity and rollback unit checks must pass. Ordinary runtime remains blocked.
5. At the browser pause, retrieve the VERIFIER password in Terminal B and open [integration_test](http://127.0.0.1:8080/ords/f?p=810004:1) as **VERIFIER**.
6. Create active Hello/World entries, configure their defaults with empty prefixes, create **Hello World**, and refresh history. Use the same controls as in stage 3.
7. Return to Terminal A. The pre-publication assertion repeats if the example is missing. Guarded publication prepares native availability, captures the final live fingerprint and commits successful receipt/ready state.
8. Inspect the application as **LAB_USER**. Finish the script and require **PASS result stage D_integration_test**.

Expected result: a complete 1.0.0 release in integration_test, with the archive/source/configuration and live fingerprint in its receipt. D does not export C or copy C's business data. This is the selected PBI-011.6 / UC-4/11 integration gate.

## 5. E: promote the same archive to UAT

**Slide 17. Fresh replay only:**

```bash
bash scripts/cicd-walkthrough-E_promotion.sh
```

1. Select and inspect the same initial archive; do not rebuild it.
2. Admit **E1_UAT / application 810005**. Missing matching integration_test evidence must block admission.
3. Follow migrate/import/unit/verify prompts. Use [UAT](http://127.0.0.1:8080/ords/f?p=810005:1) as **VERIFIER**, create/configure Hello/World, and save **Hello World**.
4. Continue to guarded publication and the matching successful integration/UAT receipts.
5. Sign in as **LAB_USER**, create a greeting and refresh history. Return to Terminal A.
6. Continue to the explicitly announced upgrade-test examples. These are new runtime fixtures outside the release package. The script creates enough explicit VERIFIER Hello/World snapshots and captures a field-level baseline. Existing configuration and history remain intact.
7. Require **PASS result stage E_promotion** before F.

**Retained-lab review:** initial 1.0.0 receipts are historical after F. Inspect them without reinstalling:

```bash
python3 scripts/apex_sql.py lab-control deploy/operator/show_release_receipts.sql
python3 scripts/cicd-artifact.py inspect "$(cat .local-apex/releases/initial-selected.txt)"
```

Look for successful initial integration/UAT records with the same artifact hash. Current runtime has since advanced to the patch. The field-baseline file is `.local-apex/releases/test-initial-preservation.json`; do not overwrite it. Successful UAT deployment is separate from the Product Owner's acceptance decision.

## 6. F: deliver the compatible Hello patch

**Slide 18. Fresh replay, after E:**

```bash
bash scripts/cicd-walkthrough-F_hello_patch.sh
```

1. The patch archive comes from `.local-apex/releases/patch-selected.txt`. Hello changes to **1.0.1**, while Foundation and World remain **1.0.0**.
2. Explicitly recreate only integration_test and install the patch from empty. Follow its VERIFIER prompts before publication.
3. Recreate only integration_test again, reconstruct initial 1.0.0, prepare explicit verification examples and capture its upgrade baseline.
4. Upgrade that baseline using the same patch archive; complete verification and field-preservation checks.
5. Only after both integration starts pass, upgrade retained UAT using those **identical patch bytes**. Do not reset UAT.
6. At each verification pause, use the printed application's URL as **VERIFIER**, create the required greeting, refresh history and return to the terminal. On an existing baseline, keep existing entries/defaults/settings.
7. Compare old rows/configuration. Open UAT as **LAB_USER**, view Installed components and Greeting history, then finish the script. Require **PASS result stage F_hello_patch**.

**Retained-lab review:** verify the archive and preserved fields without repeating F:

```bash
python3 scripts/cicd-artifact.py inspect "$(cat .local-apex/releases/patch-selected.txt)"
python3 scripts/cicd-preservation.py compare user_acceptance_test .local-apex/releases/test-initial-preservation.json
```

The handover check reports **21 prior history rows** with all fields unchanged, plus preserved old entries and complete configuration. This count describes the retained run; a fresh replay can create a different total if the operator adds more greetings. New rows may append. A text/version change without these receipts and comparisons would not establish this result.

## 7. G: reject an incompatible Foundation upgrade

**Slide 19.** Run:

```bash
bash scripts/cicd-walkthrough-G_incompatible_upgrade.sh
```

1. Submit the Foundation 2.0.0 proposal at the prompt.
2. Read **REJECTED INCOMPATIBLE: Hello requires Foundation 1.0.0; proposed Foundation 2.0.0**. World declares the same requirement.
3. Read the unchanged-target/control check. The expected rejection happens before maintenance, migration or APEX import; an arbitrary execution error is not a pass.
4. Open UAT as **LAB_USER** and confirm the working application/history remain. Complete the viewing pause and require **PASS result stage G_incompatible_upgrade**.

The [shared release manifest](../../release/manifest.json) contains component versions and dependency descriptors. The [proposal](../../release/proposals/foundation-major.json) introduces the mismatch. The archived [compatibility checker](../../scripts/cicd-compatibility.py) validates explicit exact dependencies and supported triples, not the semantic meaning of SQL. This is the selected PBI-011.7 incompatible-change protection, not an executed destructive migration.

## 8. H: detect, inspect and decide on manual drift

**Slides 20–22.** The regular command supports both states:

```bash
bash scripts/cicd-protection-check.sh drift
```

1. Before any edit, require **NO DRIFT** and unchanged snapshots. In the current retained session, this earlier clean result has already been observed; the manual edit is now active, so expect **DETECTED DRIFT** instead.
2. For a new manual example, sign in to workspace **E1_UAT** using an authorized developer account, such as the temporary **DRIFT_EDITOR**. LAB_USER/VERIFIER do not have App Builder access. To reach workspace sign-in, open [ORDS](http://127.0.0.1:8080/ords/) and click **Go** under **Oracle APEX**.
3. If temporary access must be created, retrieve ADMIN's password with `python3 scripts/cicd-password.py APEX_ADMIN_PASSWORD`, open [Administration Services](http://127.0.0.1:8080/ords/apex_admin) as ADMIN/INTERNAL, then select **Manage Workspaces → Manage Developers and Users → Create User**. Create DRIFT_EDITOR in workspace/default schema E1_UAT, enter and confirm an operator-chosen password, allow developer/App Builder access, keep the account unlocked and leave administrator/SQL Workshop/Team Development access off. Sign out before using workspace sign-in.
4. Open **App Builder → application 810005 → 1 — Home**. **Rendering** is the first icon above the left-hand tree. Click the green **Page 1: Home** node above Pre-Rendering/Components/Post-Rendering. In the right-hand Property Editor, copy the original **Identification → Title**, change it to **Manual drift demonstration**, and Save. Leave component versions unchanged. View the changed page/browser title as LAB_USER.
5. Run the drift command again. Require **REJECTED DRIFT**, **DETECTED DRIFT** and **PASS drift protection**. The edited page and business data must remain after rejection.
6. Inspect the unexpected source through the same command:

   ```bash
   bash scripts/cicd-protection-check.sh drift --show
   ```

   Read published versus live values and the SQL diff. Minus lines are published source; plus lines are live source. Open the paths printed after **REVIEW** and **COMPLETE RAW DIFF**. Both source trees remain saved. The shorter diff omits only target offset lines and generated Manifest comments; target alias, availability and other metadata differences remain visible for separate interpretation.
7. **Current observed example:** Home Title changed from `APEX Delivery Laboratory` to `Manual drift demonstration`; the region Name changed from `APEX Delivery Laboratory` to `APEX Delivery XX Laboratory`. The report retains additional SQL/export differences rather than hiding them. No restoration was performed during handover preparation.
8. **Choose keep or undo.** To keep it, stop here, preserve the live export and reconcile through reviewed Git source/new release. Deployment remains blocked while drift remains. To undo, restore the published page Title and every other property you changed. For the observed region change, expand Components, select that region and restore **Identification → Name**; also restore its Title if you changed it. Save.
9. Run the same drift check again. Restoration passes only with **NO DRIFT** against the original successful receipt, plus retained history. If drift remains, use --show to inspect remaining differences. Do not replace the accepted baseline to clear the error.
10. Remove DRIFT_EDITOR through Administration Services only if you created that temporary account for this demonstration. Keep existing accounts unchanged.

The supported source-review profile and controls are in the [operator manual](user_manual.md#inspect-manual-drift-before-deciding-restoration). This is the selected PBI-011.7/PBI-012, UC-5/FR-10 page-drift slice. It does not complete general reconciliation, schema drift or failure repair.

## 9. Optional scripted drift replay

**Slides 20–22.** Run only after the manual edit is restored and no other UAT authoring/deployment is active:

```bash
bash scripts/cicd-walkthrough-H_drift.sh
```

1. The script requires a clean baseline.
2. It saves the current UAT definition and data snapshot, then imports the prepared native Home title/banner fixture outside release delivery. The release/component versions stay unchanged.
3. View **DIRECT CHANGE - deployment must stop** in UAT.
4. Continue to the same protection check with --show. The automated replay explicitly expects drift; a clean observation cannot pass that phase.
5. Inspect the rejection/differences and unchanged target/control results.
6. Choose the script's explicit restoration operation. It refuses an unexplained intervening edit, imports the saved definition, and requires the original fingerprint and preserved data.
7. View the restored runtime and require **PASS result stage H_drift**.

This synthetic setup is useful for repeatable testing of the detection routine. It is separate from the real Page Designer edit and must not overwrite an active manual example. Quitting can deliberately leave its fixture active. Only for that synthetic fixture, `python3 scripts/cicd-drift-demo.py restore` is the separate explicit cleanup command; it is not the restoration command for arbitrary edits.

## 10. Verification continuations and remaining limits

**Slide 23.** A missing required browser greeting is an assertion failure, not a successful release. A post-publication fixture error is different: the release can already be ready while example preparation remains incomplete. The observed fixture bug used an unset World default; it now selects active entries explicitly and preserves configuration.

Use only the command matching the retained checkpoint:

```bash
bash scripts/cicd-walkthrough-C_world.sh --resume-verification
bash scripts/cicd-walkthrough-E_promotion.sh --resume-verification
bash scripts/cicd-walkthrough-E_promotion.sh --resume-examples
```

These are alternatives, not a sequence to run now. The first two require their exact restricted verification states. The last requires the published initial UAT release and resumes only the examples/baseline step. They do not reinstall, skip publication guards or recover arbitrary partial migrations. In the current completed/patch run, rerunning them should be rejected as the wrong checkpoint.

Fresh-only unattended rehearsal uses `bash scripts/cicd-walkthrough.sh --rehearse` **after fresh infrastructure/onboarding**, and performs actual installs, upgrades and synthetic fixtures. It announces skipped browser checks; it is not a substitute for the operator's live acceptance.

## 11. Evidence, conclusions and next decisions

**Slides 24–28.** The [completion assessment](sprint_E.1_assessment.md) lists each assigned PBI/child, official status, demonstrated subset and remaining acceptance work. The [test record](sprint_E.1_tests.md) and [handover checks](tests/handover_checks_20261018.txt) distinguish current native checks from reused earlier evidence.

1. The selected assembly/release/patch/protection slice works and has been exercised with the Product Owner.
2. The full E.1 acceptance scope is not complete. Genuine concurrent ownership/integration, full maintenance/verifier fencing, schema drift and failed additive deployment with automated repair remain open.
3. Recommend focused further Elaboration before full Lifecycle Architecture acceptance. The proposed next work reuses existing children; no new sprint is activated or Construction plan accepted by preparing this package.
4. Review the handover outcome, choose what to do with the active manual edit, and select the remaining proofs to prioritize. Record the decision in the [handover](sprint_E.1_handover.md). The Product Owner's earlier stage PASS observations do not automatically close E.1.
