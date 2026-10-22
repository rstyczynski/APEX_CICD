# Live-drift assessment — supporting evidence

The [walkthrough](cicd-walkthrough.md) presents the finding in H. The detailed
procedure below is retained for inspecting and reproducing the limited experiment;
it is not required operator work and does not establish deployment protection.
Business-data assertions in the retained procedure are preservation checks only;
they provide no evidence of application or schema drift detection.
Replaying an already-applied artifact ran no pending APEX import. A pending-import
case would be needed to assess overwrite behavior and any pre-import rejection.

## H. Assess native live-drift detection and deployment protection

**Purpose:** reproduce E.1's unexpected-live-change scenario and establish what
native tools actually do. Make one visible APEX definition change outside the
release, detect it in native exports, replay the unchanged F artifact, observe
whether deployment rejects it, then explicitly restore the original attribute.

**Rehearsed outcome:** native exports reveal the live change. Native PROJECT
repeat deployment succeeds with **Run 0 / Previously run 26**, and leaves the
change in place. It does **not reject this drifted target**. This is an E.2 gap
against E.1's selected drift gate, not an instruction to expect a rejection.

The controlled edit is the application's global notification:
**H: live change outside release delivery**. It is part of the APEX definition,
not a greeting row or business configuration. Native APEX APIs apply and restore
it. No page editing, business inserts, schema DDL, artifact rebuild or custom
admission controller is used.

**Comparison policy:** native readable YAML exports contain an internal
`subscription.version-number` that advances when an attribute is changed and
restored. The file-comparison helper excludes only that revision counter and
compares every other exported YAML value. This is an explicit project comparison
policy; the helper neither changes a database nor blocks deployment. Raw native
exports remain available for inspection. Artifact hashes and live definitions
are checked separately.

The fixture below uses **UAT / E1_UAT / application 810005** and F's unchanged
**execution-r2** archive. Rehearsal used the corresponding integration application;
UAT has not been edited during preparation. Keep the same SQLcl session throughout
H so its business/history baselines remain available. Stop on an unexpected result.

### H.1. Capture the accepted target baseline

1. In **Terminal 2 (regular shell)**, check that the F archive matches its
   recorded SHA-256 and create the four local export directories for H. The helper
   performs no database operation and refuses to overwrite existing H evidence:

   ```bash
   cd /Users/rstyczynski/projects/APEX_CICD
   python3 scripts/cicd-prepare-drift.py
   ```

   Require **PASS unchanged F artifact; fresh H evidence directories created**.
   If H evidence already exists, stop and inspect it before repeating the chapter.

2. Switch to **Terminal 1 (SQLcl)**. **Keep the SQLcl 25.3 session used for F**;
   no exit or restart is needed. Set and inspect its working directory:

   ```sql
   cd /Users/rstyczynski/projects/APEX_CICD/.local-apex/e2/project-walkthrough/component-repo-f2
   pwd
   ```

   Require the directory to end in **component-repo-f2/**. Continue in this
   session through H.4 so the baseline variables remain available.

   Only if Terminal 1 is at a regular shell, launch the F client there:

   ```bash
   cd /Users/rstyczynski/projects/APEX_CICD
   E2_PROJECT_ROOT="$PWD"
   cd "$E2_PROJECT_ROOT/.local-apex/e2/project-walkthrough/component-repo-f2" &&
   JAVA_HOME="$E2_PROJECT_ROOT/.local-apex/tools/jdk-21.0.12.1+1/Contents/Home" \
     "$E2_PROJECT_ROOT/.local-apex/tools/sqlcl/bin/sql" \
     -home "$E2_PROJECT_ROOT/.local-apex/tools/sqlcl-home" /nolog
   ```

   If a different SQLcl client is open, exit that client first and use this launch
   command. H uses F's original SQLcl **25.3**, rather than the separate client
   used for G's supporting experiments. Wait for **SQL>** before step 3.

3. Stay in **Terminal 1 (SQLcl)**. Select UAT and establish its accepted state.
   `h-baseline.sql 810005` checks the owned application, F versions, Available
   status and an empty notification; it records installed changeset history in
   session variables. The argument is the UAT application ID:

   ```sql
   pwd
   connect -name user_acceptance_test
   show user
   @../../../../progress/E.2/inputs/h-baseline.sql 810005
   ```

   Require **component-repo-f2 / E1_UAT** and:

   ```text
   PASS H baseline: E1_UAT / 810005 / Available / 1.0.1 / no notification
   ```

   A pre-existing notification or different release stops the exercise; it must
   not be silently overwritten or accepted as a new baseline.

4. Stay in **Terminal 1**. Capture every existing business field for the final
   preservation check. This is the read-only snapshot used in F:

   ```sql
   @../../../../progress/E.2/inputs/f2-capture-business.sql
   ```

   Require **PASS captured all business fields before deployment in E1_UAT**.
   Keep this connection/session through H.4; do not create greetings or edit
   configuration during the chapter.

5. Stay in **Terminal 1**. Capture native application SQL and readable YAML.
   `-skipExportDate` removes the export timestamp; `-expSupportingObjects N`
   excludes supporting-object execution scripts. The absolute output directory
   avoids SQLcl 25.3's failure with a parent-relative export directory:

   ```sql
   apex export -applicationid 810005 -skipExportDate -expSupportingObjects N -exptype APPLICATION_SOURCE,READABLE_YAML -dir /Users/rstyczynski/projects/APEX_CICD/.local-apex/e2/project-walkthrough/h-operator/before
   ```

   Require an export for workspace **E1_UAT / application 810005**. It creates
   `before/f810005.sql` and `before/readable/application/f810005.yaml` plus the
   page/shared-component YAML files. File existence is checked during comparison.

### H.2. Make and detect the live definition change

1. In **Terminal 1**, apply the supplied controlled change. The SQL checks the
   same owned target and empty notification before invoking native
   `APEX_APPLICATION_ADMIN.SET_GLOBAL_NOTIFICATION` and committing the one edit:

   ```sql
   @../../../../progress/E.2/inputs/h-live-change.sql
   ```

   Require **OBSERVED native APEX live change: H: live change outside release delivery**.
   No business row or component version is changed.

2. Stay in **Terminal 1**. Export the changed live application through the same
   native operation and options as the baseline:

   ```sql
   apex export -applicationid 810005 -skipExportDate -expSupportingObjects N -exptype APPLICATION_SOURCE,READABLE_YAML -dir /Users/rstyczynski/projects/APEX_CICD/.local-apex/e2/project-walkthrough/h-operator/drifted
   ```

3. Switch to **Terminal 2**. Compare the two native YAML export trees. `changed`
   requires an actual definition difference; it does not gate a deployment:

   ```bash
   python3 scripts/cicd-compare-apex-exports.py changed .local-apex/e2/project-walkthrough/h-operator/before/readable .local-apex/e2/project-walkthrough/h-operator/drifted/readable
   code --diff .local-apex/e2/project-walkthrough/h-operator/before/readable/application/f810005.yaml .local-apex/e2/project-walkthrough/h-operator/drifted/readable/application/f810005.yaml
   ```

   Require **OBSERVED changed APEX definition files: application/f810005.yaml**.
   The helper also prints its sole revision-counter exclusion. In VS Code's
   read-only comparison, find the notification text. The internal revision may
   also differ; no manual edits are needed.

4. Stay in **Terminal 2** and open the existing login card:

   ```bash
   code .local-apex/e2/project-walkthrough/access.md
   ```

5. In the **browser**, open [UAT Home](http://127.0.0.1:8080/ords/f?p=810005:1).
   1. If another account is signed in, open its account menu and choose **Sign Out**.
   2. Sign in as **LAB_USER** with the UAT password on the card.
   3. Require the working **Hello World - Working Copy** page and version **1.0.1**.
   4. Require **H: live change outside release delivery** in the page notification
      area. Scroll if necessary; its placement depends on the page template.
   5. Do not create a greeting or edit settings.

### H.3. Observe native deployment with drift present

1. Switch to **Terminal 1 (SQLcl)**. Replay the unchanged F archive using its
   existing UAT mapping. There is deliberately no custom drift gate before this
   native command: this is the behavior being assessed.

   ```sql
   set define on
   define DEFAULTS_FILE=utils/properties/uat.properties
   project deploy -file artifact/e2-1.0.1-execution-r2.zip
   ```

   Rehearsed result: **Operation completed successfully**, **Run: 0 / Previously
   run: 26**, and **Database is up to date, no changesets to execute**.
   This success is the observation: deployment did not reject the drifted target.
   Stop on any different changeset count or unexpected failure.

2. Stay in **Terminal 1**. Inspect the result and compare the retained business
   snapshot. These checks observe after deployment; they are not admission controls:

   ```sql
   @../../../../progress/E.2/inputs/h-observe-deploy.sql
   @../../../../progress/E.2/inputs/f2-check-business.sql
   ```

   Require:

   ```text
   OBSERVED live change remains after native repeat deployment
   PASS component versions, publication and changeset history unchanged
   PASS exact business fields unchanged by deployment in E1_UAT
   ```

3. Stay in **Terminal 1**. Export the actual post-deployment application:

   ```sql
   apex export -applicationid 810005 -skipExportDate -expSupportingObjects N -exptype APPLICATION_SOURCE,READABLE_YAML -dir /Users/rstyczynski/projects/APEX_CICD/.local-apex/e2/project-walkthrough/h-operator/after-deploy
   ```

4. Switch to **Terminal 2**. `same` compares the changed and post-deployment
   definitions to establish whether the live change survived:

   ```bash
   python3 scripts/cicd-compare-apex-exports.py same .local-apex/e2/project-walkthrough/h-operator/drifted/readable .local-apex/e2/project-walkthrough/h-operator/after-deploy/readable
   ```

   Require **PASS all 24 exported APEX YAML definitions match**, followed by
   the stated revision-counter policy.

5. In the **browser**, refresh the same UAT Home page as **LAB_USER**. Require
   the application to remain usable and the **H: live change outside release
   delivery** notification to remain visible.

### H.4. Explicitly restore and verify

**Decision for this walkthrough:** restore the accepted definition. The live
edit is not captured into Git or accepted as a new release baseline.

1. Switch to **Terminal 1**. Restore only the demonstration notification through
   the native APEX API. The supplied SQL refuses to overwrite a different
   notification and does not reimport the application:

   ```sql
   @../../../../progress/E.2/inputs/h-restore.sql
   @../../../../progress/E.2/inputs/f2-check-business.sql
   ```

   Require **PASS original notification restored through native APEX API** and
   **PASS exact business fields unchanged by deployment in E1_UAT**.

2. Stay in **Terminal 1**. Export the restored definition:

   ```sql
   apex export -applicationid 810005 -skipExportDate -expSupportingObjects N -exptype APPLICATION_SOURCE,READABLE_YAML -dir /Users/rstyczynski/projects/APEX_CICD/.local-apex/e2/project-walkthrough/h-operator/restored
   ```

3. Switch to **Terminal 2**. Compare every restored YAML definition with the
   original accepted export, excluding only APEX's internal revision counter:

   ```bash
   python3 scripts/cicd-compare-apex-exports.py same .local-apex/e2/project-walkthrough/h-operator/before/readable .local-apex/e2/project-walkthrough/h-operator/restored/readable
   ```

   Require **PASS all 24 exported APEX YAML definitions match**. Raw SQL exports
   and native raw checksums can differ because the APEX revision counter advanced;
   byte-identical raw output is not the restoration criterion.

4. In the **browser**, refresh [UAT Home](http://127.0.0.1:8080/ords/f?p=810005:1)
   as **LAB_USER**. Require the notification to be gone and the working page/version
   to remain. Open **Greeting history** and read the existing saved greetings.
   Do not add records until the preservation checks have passed.

### H.5. Gap finding and limits

- **Supported:** native APEX export captures the live change for comparison;
  native APIs apply and restore the selected attribute.
- **Not provided in the tested path:** native PROJECT repeat deployment does not
  automatically reject this changed target. E.1's selected drift gate provides
  additional project protection.
- **Scope:** this is a real live APEX definition edit, not an archive-hash mismatch.
  All 26 changesets were already applied, so the repeat performed no APEX import.
  It does not prove what a later changed release would overwrite, nor full schema
  drift coverage, concurrency fencing or automatic repair.
- **Project logic:** the SQL assertions and file-comparison policy are explicit
  assessment checks. They are not presented as native deployment protection.

Native references: [APEX 24.2 notification API](https://docs.oracle.com/en/database/oracle/apex/24.2/aeapi/APEX_APPLICATION_ADMIN.SET_GLOBAL_NOTIFICATION-Procedure.html)
and [APEX export API](https://docs.oracle.com/en/database/oracle/apex/24.2/aeapi/GET_APPLICATION_Function.html).
Follow-up must be reconciled with the existing drift/admission and pipeline work;
this chapter implements no replacement controller. I remains a separate chapter.
