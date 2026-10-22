# E.2 — Deliver Foundation, Hello and World with SQLcl PROJECT

Repeat the E.1 application journeys using SQLcl PROJECT for capture, staging,
packaging and deployment, and APEX Working Copies for a small authoring change.
Inspect the application and retained data after each delivery.

E.2 is an independent delivery stream using the same application scenario and
acceptance outcomes. Evaluate Oracle capabilities first. Where an outcome is
unsupported or fails, record the evidence and assess the smallest necessary
supplement. The comparison does not require reproducing E.1's custom mechanisms
or treating them as prerequisites for the Oracle approach.

**Execution readiness:** A/B/C capture and D's mapped integration deployment,
restricted-verifier access, publication, ordinary-user greeting/history and
identical-artifact repeat have been exercised. SQLcl 25.3 native verification
still reports the APEX `stagechangelogcomplete` issue: D establishes a working
assessment candidate, not a clean formal release gate. E’s same-byte UAT promotion and preservation baseline are also
exercised through a small transparent wrapper prototype. The Product Owner
reported E.6 and the complete F journey completed on 2026-10-20. F covers
manual Working Copy coordination, native PROJECT patch preparation, fresh and
populated integration qualification, same-artifact UAT upgrade, preservation,
publication and repeat deployment. This is operator-reported completion; the
retained F.1 checkpoint is c79fe9d. G records the native component dependency gap; its supporting experiments are
linked separately. H presents the live-drift finding and its protection limit without a required
repeat exercise; I remains separate work.
See the [mapped deployment evidence](tests/project-integration-mapped-validation.json).

The [design](walkthrough-redesign.md) defines preparation and tool boundaries.
The [E.1 walkthrough](../E.1/cicd-walkthrough.md) defines the application journeys
being repeated. The [gap analysis](oracle-gap-analysis.md) owns the comparison
with Oracle guidance; the [operating reference](user_manual.md) describes the
previous prototype and is not the setup procedure for this replacement.

## Journey order — aligned with E.1

Follow the same application outcomes as the [E.1 walkthrough](../E.1/cicd-walkthrough.md):

1. **A — Foundation:** development area A, application 810001; incomplete assembly.
2. **B — Hello:** development area B, application 810002; World still missing.
3. **C — World:** development area C, application 810003; working greeting/history.
4. **D — Qualification:** reconstruct the initial artifact in integration_test, application 810004.
5. **E — Promotion:** deploy the identical qualified artifact to user_acceptance_test, application 810005.
6. **F — Compatible Hello patch:** qualify fresh and over 1.0.0, then upgrade the retained target and check settings/history. Working Copy authoring precedes patch capture within F.
7. **G — Incompatible upgrade:** reject before writes; retain the working application.
8. **H — Unexpected live change:** detect drift and reject before overwrite.
9. **I — Failed additive deployment:** assessment remains incomplete; no executable exercise.

A/B/C are preloaded development assemblies, matching E.1's separate areas. The
PROJECT exercises capture those real inputs; export itself is not a deployment.
D/E are the initial release qualification and promotion, not additional component
assembly stages. A/B/C capture branches have different physical schemas and
application IDs: **do not stage Hello against Foundation or World against Hello
as if they were successive revisions of one deployment target.** The World
branch supplies the complete initial-release source and subsequent patch lineage.

## What you will see

Complex Foundation upgrades remain outside this walkthrough.

## Open the demonstration

The lab contains the reviewed E.1 application checkpoints:

- **Foundation:** [application 810001](http://127.0.0.1:8080/ords/f?p=810001:1), schema/workspace E1_DEV_A.
- **Hello:** [application 810002](http://127.0.0.1:8080/ords/f?p=810002:1), schema/workspace E1_DEV_B.
- **World:** [application 810003](http://127.0.0.1:8080/ords/f?p=810003:1), schema/workspace E1_DEV_C.

1. Open the [local login card](../../.local-apex/e2/project-walkthrough/access.md).
2. Open [the complete application](http://127.0.0.1:8080/ords/f?p=810003:1).
3. Sign in as **LAB_USER** with the password on the card.
4. On Home, leave **Hello** and **World** set to their configured defaults.
5. Click **Create greeting**.
6. Check the success message: **Hello World — saved to history.**
7. Open **Greeting history** from the navigation menu and find the saved row.
8. Open **Installed components** and inspect the three `1.0.0` versions.

Accounts, schema objects and application pages are already loaded. The current
preloaded fixture also retains an E1_CTRL runtime dependency from its source;
that is a fixture constraint to assess, not a requirement that E.2 adopt that
delivery controller. Application creation and environment provisioning are not
operator steps in this walkthrough.

### Start the two terminals

File and directory viewing commands use VS Code through `code`, on macOS and
Windows. Install VS Code and make its `code` command available on your terminal
PATH before starting; `code --version` should print its version.

Use Terminal 1 for SQLcl and Terminal 2 for Git. Initialize each terminal
explicitly; shell variables are not shared between them. Start inside the main
APEX_CICD checkout. The application repository below is separate from that checkout.

**Terminal 2 — initialize a fresh application repository:**

```bash
cd /Users/rstyczynski/projects/APEX_CICD
mkdir .local-apex/e2/project-walkthrough/component-repo
git -C .local-apex/e2/project-walkthrough/component-repo init -b e2-base
git -C .local-apex/e2/project-walkthrough/component-repo commit --allow-empty -m "Establish empty E.2 capture baseline"
```

Expected: branch `e2-base` has one empty commit. If `mkdir` reports that the
directory exists, stop and inspect it; do not repeat initialization, delete its
contents or reuse the earlier `repo`/`rehearsal-repo` directories. This guide
uses `component-repo` throughout. Keep Terminal 2 at the main checkout root.

**Terminal 1 — launch the pinned SQLcl client:**

```bash
cd /Users/rstyczynski/projects/APEX_CICD
E2_PROJECT_ROOT="$PWD"
cd "$E2_PROJECT_ROOT/.local-apex/e2/project-walkthrough/component-repo" &&
JAVA_HOME="$E2_PROJECT_ROOT/.local-apex/tools/jdk-21.0.12.1+1/Contents/Home" \
  "$E2_PROJECT_ROOT/.local-apex/tools/sqlcl/bin/sql" \
  -home "$E2_PROJECT_ROOT/.local-apex/tools/sqlcl-home" /nolog
```

Wait for `SQL>`. All `sql` blocks below belong at that prompt; all `bash`
blocks belong in Terminal 2. SQLcl starts in the application repository, so no
host-specific absolute directory or unexplained directory substitution is needed.

Saved connections are `lab-dev` (E1_DEV_A), `lab-dev-b` (E1_DEV_B), `lab-dev-c`
(E1_DEV_C), `integration_test` (E1_INTEGRATION) and `user_acceptance_test` (E1_UAT).
A connection changes the database session; PROJECT's schema, connection and
filters are configured separately on each capture branch below.

## A. Deliver Foundation

**Purpose:** inspect E.1's preloaded Foundation-only development outcome and
capture that exact assembly with SQLcl PROJECT. Application creation is already
complete; the operator does not construct its pages.

### A.1. Select and check development area A

1. In Terminal 2, create the Foundation capture branch from the empty baseline:

   ```bash
   git -C .local-apex/e2/project-walkthrough/component-repo switch -c e2-foundation e2-base
   ```

2. In Terminal 1, enter:

   ```sql
   connect -name lab-dev
   show user
   select component, installed, version from lab_components order by component;
   select application_id, application_name, owner from apex_applications where application_id=810001;
   ```

3. Require schema **E1_DEV_A**, application **810001**, Foundation installed at
   **1.0.0**, and Hello/World not installed. A missing application or another
   schema is a stop condition.
4. Open [Foundation / 810001](http://127.0.0.1:8080/ords/f?p=810001:1).
   Confirm incomplete-assembly protection. This is the preloaded development
   result; it is not evidence that PROJECT has deployed a candidate.

### A.2. Initialize PROJECT for Foundation

1. In Terminal 1:

   ```sql
   project init -name e2 -schemas E1_DEV_A -connection-name lab-dev
   project config set -name export.setTransform.emitSchema -value false
   project config set -name export.apex.expOriginalIds -value true
   project config set -name export.apex.skipExportDate -value true
   project config set -name git.defaultBranch -value e2-foundation-base
   ```

2. In Terminal 2, install the Foundation capture filter and retain the configured
   empty source baseline:

   ```bash
   cp progress/E.2/inputs/project-foundation.filters .local-apex/e2/project-walkthrough/component-repo/.dbtools/filters/project.filters
   git -C .local-apex/e2/project-walkthrough/component-repo add .dbtools .gitignore README.md
   git -C .local-apex/e2/project-walkthrough/component-repo commit -m "Configure Foundation capture in E1_DEV_A"
   git -C .local-apex/e2/project-walkthrough/component-repo branch e2-foundation-base
   ```

3. The filter includes Main application **810001** and excludes ORDS, private
   Working Copies and existing Liquibase bookkeeping. Target schema names are
   excluded from emitted schema DDL by `emitSchema=false`.

### A.3. Capture and review Foundation

1. In Terminal 1:

   ```sql
   project export -list
   project export
   ```

2. Inspect the list: it must capture Foundation's schema objects and Main
   **810001**, not application 810003 or Hello/World tables.
3. In Terminal 2:

   ```bash
   git -C .local-apex/e2/project-walkthrough/component-repo status --short
   git -C .local-apex/e2/project-walkthrough/component-repo diff
   git -C .local-apex/e2/project-walkthrough/component-repo add src
   git -C .local-apex/e2/project-walkthrough/component-repo diff --cached --stat
   git -C .local-apex/e2/project-walkthrough/component-repo diff --cached
   ```

4. Review the actual source before accepting it. Newly exported files are
   untracked until added, so `git diff` alone does not display their contents.
5. Commit the reviewed capture:

   ```bash
   git -C .local-apex/e2/project-walkthrough/component-repo commit -m "Capture Foundation 1.0.0"
   ```

**Result:** Foundation source is retained on `e2-foundation`. No target release
or migration has been executed by these export commands.

## B. Deliver Hello

**Purpose:** inspect E.1's Foundation-plus-Hello development assembly in B and
capture it explicitly. Do not look for a checkpoint selector in SQLcl or Builder.

### B.1. Select and check development area B

1. In Terminal 2:

   ```bash
   git -C .local-apex/e2/project-walkthrough/component-repo switch -c e2-hello e2-base
   ```

2. In Terminal 1:

   ```sql
   connect -name lab-dev-b
   show user
   select component, installed, version from lab_components order by component;
   select application_id, application_name, owner from apex_applications where application_id=810002;
   ```

3. Require **E1_DEV_B**, application **810002**, Foundation/Hello **1.0.0**, and
   World not installed.
4. Open [Hello / 810002](http://127.0.0.1:8080/ords/f?p=810002:1). Confirm the
   application remains incomplete while World is missing.

### B.2. Initialize and capture Hello

1. In Terminal 1:

   ```sql
   project init -name e2 -schemas E1_DEV_B -connection-name lab-dev-b
   project config set -name export.setTransform.emitSchema -value false
   project config set -name export.apex.expOriginalIds -value true
   project config set -name export.apex.skipExportDate -value true
   project config set -name git.defaultBranch -value e2-hello-base
   ```

2. In Terminal 2:

   ```bash
   cp progress/E.2/inputs/project-hello.filters .local-apex/e2/project-walkthrough/component-repo/.dbtools/filters/project.filters
   git -C .local-apex/e2/project-walkthrough/component-repo add .dbtools .gitignore README.md
   git -C .local-apex/e2/project-walkthrough/component-repo commit -m "Configure Hello capture in E1_DEV_B"
   git -C .local-apex/e2/project-walkthrough/component-repo branch e2-hello-base
   ```

3. In Terminal 1:

   ```sql
   project export -list
   project export
   ```

4. Require Main **810002**, Foundation objects and Hello objects; no World tables.
5. In Terminal 2, review and retain the exported source:

   ```bash
   git -C .local-apex/e2/project-walkthrough/component-repo add src
   git -C .local-apex/e2/project-walkthrough/component-repo diff --cached --stat
   git -C .local-apex/e2/project-walkthrough/component-repo diff --cached
   ```

6. After review:

   ```bash
   git -C .local-apex/e2/project-walkthrough/component-repo commit -m "Capture Foundation and Hello 1.0.0"
   ```

**Result:** the B development assembly is captured on `e2-hello`. This is not
an upgrade of physical schema E1_DEV_A. Its own configured empty baseline is
`e2-hello-base`; the Foundation branch remains intact for inspection.

## C. Deliver World and complete the assembly

**Purpose:** capture the complete C development assembly, then exercise the
working greeting/history application as in E.1. This branch becomes the source
for initial qualification, promotion and the compatible Hello patch.

### C.1. Select and check development area C

1. In Terminal 2:

   ```bash
   git -C .local-apex/e2/project-walkthrough/component-repo switch -c e2-world e2-base
   ```

2. In Terminal 1:

   ```sql
   connect -name lab-dev-c
   show user
   select component, installed, version from lab_components order by component;
   select application_id, application_name, owner from apex_applications where application_id=810003;
   ```

3. Require **E1_DEV_C**, application **810003** and all three components installed
   at **1.0.0**.

### C.2. Initialize and capture the complete assembly

1. In Terminal 1:

   ```sql
   project init -name e2 -schemas E1_DEV_C -connection-name lab-dev-c
   project config set -name export.setTransform.emitSchema -value false
   project config set -name export.apex.expOriginalIds -value true
   project config set -name export.apex.skipExportDate -value true
   project config set -name git.defaultBranch -value e2-world-base
   ```

2. In Terminal 2:

   ```bash
   cp progress/E.2/inputs/project-world.filters .local-apex/e2/project-walkthrough/component-repo/.dbtools/filters/project.filters
   git -C .local-apex/e2/project-walkthrough/component-repo add .dbtools .gitignore README.md
   git -C .local-apex/e2/project-walkthrough/component-repo commit -m "Configure complete World capture in E1_DEV_C"
   git -C .local-apex/e2/project-walkthrough/component-repo branch e2-world-base
   ```

3. In Terminal 1:

   ```sql
   project export -list
   project export
   ```

4. Require Main **810003** and all seven business tables. Private Working Copies,
   ORDS and existing Liquibase bookkeeping must not be captured.

5. In Terminal 2, review the new source files:

   ```bash
   git -C .local-apex/e2/project-walkthrough/component-repo add src
   git -C .local-apex/e2/project-walkthrough/component-repo diff --cached --stat
   git -C .local-apex/e2/project-walkthrough/component-repo diff --cached
   ```

6. After review:

   ```bash
   git -C .local-apex/e2/project-walkthrough/component-repo commit -m "Capture complete Foundation Hello World 1.0.0"
   ```

### C.3. Check the working application

1. Open [C / application 810003](http://127.0.0.1:8080/ords/f?p=810003:1).
2. Sign in as **LAB_USER** using the [local login card](../../.local-apex/e2/project-walkthrough/access.md).
3. Open **Hello entries** and **World entries**. The prepared Hello/World examples
   already exist; no page creation is required.
4. Open **Hello configuration** and **World configuration**. Inspect the prepared
   defaults and empty prefixes.
5. On **Home**, click **Create greeting**.
6. Check **Hello World — saved to history.**
7. Open **Greeting history** and find the new row.
8. Open **Installed components**; require three **1.0.0** versions.

**Result:** C's complete source and functioning development assembly are visible.
Export captures definitions, not this greeting history or configured business data.
No integration_test qualification or UAT promotion is implied by C's success.

## D. Qualify the initial release

**Purpose:** reconstruct and verify the complete initial candidate in
integration_test (E1_INTEGRATION / application 810004), before any UAT promotion.
Use branch `e2-world` and its configured empty source baseline `e2-world-base`.
Keep A/B captures as comparison evidence, outside this release's lineage.

**Demonstrated scope:** D's native mapped installation and application checks
passed. Native verification retains one reported APEX completeness error; its
assessment status is explained in D.2. Promotion and later journeys are separate
from this observed integration result.

### D.1. Inspect source, migrations and release data

Use the World branch in the same application Git repository throughout D–H.
A/B are independent development captures, not migration predecessors of C.

1. In **Terminal 2 — the regular shell, not the SQLcl prompt**, start inside
   the main APEX_CICD checkout and check the application repository:

   ```bash
   cd /Users/rstyczynski/projects/APEX_CICD
   git -C .local-apex/e2/project-walkthrough/component-repo status --short --branch
   git -C .local-apex/e2/project-walkthrough/component-repo branch --list
   ```

   Require a clean working tree and branches `e2-world` and `e2-world-base`.
   If changes remain, stop and review them before switching; do not discard them.
2. Still in **Terminal 2**, switch to the World branch and confirm it:

   ```bash
   git -C .local-apex/e2/project-walkthrough/component-repo switch e2-world
   git -C .local-apex/e2/project-walkthrough/component-repo branch --show-current
   ```

   Expected: `e2-world`. Leave Terminal 2 at the main checkout root.
3. In **Terminal 2**, list the captured source files and inspect their changes
   against the configured empty source baseline:

   ```bash
   git -C .local-apex/e2/project-walkthrough/component-repo ls-tree -r --name-only HEAD src
   git -C .local-apex/e2/project-walkthrough/component-repo diff --stat e2-world-base HEAD -- src
   git -C .local-apex/e2/project-walkthrough/component-repo diff e2-world-base HEAD -- src
   ```

   The paths printed by Git are relative to **component-repo**, not the main
   APEX_CICD checkout. In **Terminal 2**, view application `810003` in VS Code:

   ```bash
   code .local-apex/e2/project-walkthrough/component-repo/src/database/e1_dev_c/apex_apps/f810003/
   ```

   Inspect its application SQL and `readable/` files. To inspect the business
   schema definitions, open their parent source directory in VS Code:

   ```bash
   code .local-apex/e2/project-walkthrough/component-repo/src/database/e1_dev_c/
   ```

4. Return to **Terminal 1 — the SQLcl session** opened earlier in the same
   application repository. Confirm the source connection. On the first pass,
   stage the source with the command below. If the distribution already exists
   from this exercise, retain it and continue at step 5; do not regenerate an
   already reviewed/adapted distribution during inspection:

   ```sql
   connect -name lab-dev-c
   show user
   project stage -branch-name e2-world-base
   ```

   Require user **E1_DEV_C**. Git selected the source branch; the connection
   selects the database session. Both must identify the intended source.

5. In **Terminal 2**, open the generated distribution and locate its installer
   and changelogs:

   ```bash
   code .local-apex/e2/project-walkthrough/component-repo/dist/
   ```

6. Inspect the **actual execution order**, rather than the alphabetical order
   of files in the file explorer. In **Terminal 2**, open these generated files in VS Code:

   ```bash
   code .local-apex/e2/project-walkthrough/component-repo/dist/install.sql
   code .local-apex/e2/project-walkthrough/component-repo/dist/releases/main.changelog.xml
   code .local-apex/e2/project-walkthrough/component-repo/dist/releases/next/release.changelog.xml
   code .local-apex/e2/project-walkthrough/component-repo/dist/releases/next/changes/e2-world/stage.changelog.xml
   code .local-apex/e2/project-walkthrough/component-repo/dist/releases/apex/apex.changelog.xml
   ```

   1. In `install.sql`, find `lb update` and its entry point,
      `releases/main.changelog.xml`. You are reading the installer, not executing it.
   2. In `main.changelog.xml`, read the `<include>` elements from top to bottom.
      The generated order is **`next/release.changelog.xml` first**, then
      **`apex/apex.changelog.xml`**: schema migrations precede application import.
   3. In `next/release.changelog.xml`, follow the include to
      `changes/e2-world/stage.changelog.xml`. Paths with
      `relativeToChangelogFile="true"` are relative to the containing XML file.
   4. In `stage.changelog.xml`, read the includes in order. The inspected output
      contains the `lab_runtime` package specification, the seven
      business tables, the package body, triggers, and finally the two foreign
      keys. It does **not** group every file into Foundation → Hello → World
      component releases; this is a full initial schema capture.
   5. Check the concrete dependencies: `lab_runtime` specification precedes its
      body; all business tables precede that body and their triggers;
      `hello_config` and `hello_entries` both precede
      `ref_constraints/hello_config.hello_entries.sql`; `world_config` and
      `world_entries` both precede their equivalent foreign-key file. The config
      tables can appear before the entries tables because these foreign keys
      are added separately at the end.
   6. In `apex/apex.changelog.xml`, follow `f810003/f810003.xml`. Its application
      import runs after the schema changelog. Import order alone does not prove
      that initialization data, target mapping or runtime publication is ready.
   7. Older captures also include two E1_CTRL grants to the source grantee
      E1_DEV_C. D.1.10 removes their replay from the candidate; the current World
      capture filter excludes that external grant category. They are not
      application-schema migrations and are not needed by the approved native
      runtime controls.

   **Expected observation:** the generated order places the listed schema
   objects before their dependents and imports APEX afterward. This is a file
   inspection. D.1.10 prepares the explicit runtime/mapping adjustments, and D.2
   tests the resulting fresh installation rather than assuming staging proves it.

   > **Native ordering and component contracts:** SQLcl PROJECT
   > generates the Liquibase changelog hierarchy; we did not manually declare
   > this execution order in `project.config.json`. The generated includes make
   > the order explicit. This is native [PROJECT staging/deployment behavior](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/project.html),
   > observed here for this capture. It does not mean PROJECT understands our
   > Foundation/Hello/World contracts. Requirements such as “Hello requires
   > Foundation 1.x,” compatible component versions, initialization data and
   > external E1_CTRL access are not declared or enforced by our current PROJECT
   > configuration. Those require separate contract/admission checks and target
   > validation; generated object ordering alone does not prove compatibility.

7. Create the initialization changeset in **Terminal 1**. If
   `_custom/e2_release_data.sql` already exists from this step, keep it and
   continue at step 8; do not generate it again:

   ```sql
   project stage add-custom -file-name e2_release_data.sql
   ```

8. In **Terminal 2**, inspect the supplied initialization input:

   ```bash
   code progress/E.2/inputs/initial-release-data.sql
   ```

   This input explicitly creates three `1.0.0` component declarations, four
   internal assembly-state rows, new literal **Hello**/**World** examples and two
   default configuration rows with empty prefixes. It creates **no greeting
   history**. It first refuses any schema except E1_INTEGRATION/E1_UAT and any
   existing row in the seven application tables. It therefore cannot initialize
   a populated upgrade target by replacing its settings or history.

   This is a candidate release input, not evidence of a successful installation.
   The old private `.local-apex/.../initial-release-data.sql` is not used here.

9. Append that input to the generated custom changeset **once**, preserving
   PROJECT's existing Liquibase header. Run in **Terminal 2**:

   ```bash
   E2_CUSTOM=.local-apex/e2/project-walkthrough/component-repo/dist/releases/next/changes/e2-world/_custom/e2_release_data.sql
   if test -f "$E2_CUSTOM"; then
     if rg -q 'E2_INITIAL_RELEASE_DATA_1_0_0' "$E2_CUSTOM"; then
       printf '%s\n' 'Initialization input is already present; inspect it below.'
     else
       cat progress/E.2/inputs/initial-release-data.sql >> "$E2_CUSTOM"
     fi
     code "$E2_CUSTOM"
   else
     printf '%s\n' 'Custom changeset is missing. Complete step 7 in SQLcl first.'
   fi
   ```

   1. Require the generated `-- liquibase formatted sql`, `-- changeset` and
      `-- sqlcl_snapshot` header lines, followed by one initialization block.
   2. Read that block: every inserted business value is a literal demonstration
      value or a newly returned local entry ID. There is no developer-schema
      query, existing-setting update or history insert/delete.
   3. Inspect `stage.changelog.xml` again. Its
      `_custom/e2_release_data.sql` include must occur once, after the schema
      objects/triggers. In the block, component and state rows are inserted
      before entry inserts invoke `lab_runtime.assert_ready`; the entries are
      inserted before configuration guards validate their default IDs.
   4. The internal assembly `ready` rows do not grant public access through the
      native APEX restricted-access setting. The candidate replaces its inherited
      E1_CTRL initialization call as described in D.1.10; verifier access and
      publication remain explicit native APEX operations.

10. In **Terminal 2**, prepare the target mappings and the approved native
    runtime controls. Review the supplied patches in VS Code first:

    ```bash
    code progress/E.2/inputs/mapped-initial.patch
    code progress/E.2/inputs/exclude-source-grants.patch
    code progress/E.2/inputs/integration.properties
    code progress/E.2/inputs/uat.properties
    ```

    The mapping patch adds the [Oracle paper's page-30 defaults-file hook](../../refs/apex-lifecycle-management-v3.pdf)
    to `dist/install.sql` and enables SQLcl substitution for `DEFAULTS_FILE`.
    It also makes the candidate start with native **Restricted Access / VERIFIER**
    and removes its inherited E1_CTRL initialization call. This candidate-only
    fixture adaptation was approved; it does not change authoring application
    810003 or claim equivalent custom-controller fencing/concurrency behavior.

    > **Native APEX access controls:** this candidate uses APEX's own application
    > availability gate instead of calling the custom E1_CTRL release controller
    > (a separate schema with packages/tables, not an application component).
    > [`APEX_APPLICATION_ADMIN.SET_APPLICATION_STATUS`](https://docs.oracle.com/en/database/oracle/apex/24.2/aeapi/APEX_APPLICATION_ADMIN.SET_APPLICATION_STATUS-Procedure.html)
    > sets **Restricted Access** with an allowed-user list containing VERIFIER,
    > **Available** after verification, or **Unavailable** to block application
    > access. The application's **APEX Accounts authentication scheme** still
    > authenticates VERIFIER and LAB_USER; availability determines whether they
    > may enter. Component versions remain in `lab_components`, and PROJECT's
    > Liquibase history records executed migrations. APEX availability does not
    > replace those records or establish artifact qualification, dependency
    > compatibility or concurrent-deployment fencing.

    Run the following in **Terminal 2**, at the main checkout root:

    ```bash
    E2_ROOT=/Users/rstyczynski/projects/APEX_CICD
    E2_REPO="$E2_ROOT/.local-apex/e2/project-walkthrough/component-repo"
    cp progress/E.2/inputs/project-world.filters "$E2_REPO/.dbtools/filters/project.filters"
    git -C "$E2_REPO" rm --ignore-unmatch -- 'src/database/e1_ctrl/object_grants/*.sql'
    if rg -q '<include file="e1_ctrl/object_grants/' "$E2_REPO/dist/releases/next/changes/e2-world/stage.changelog.xml"; then
      git -C "$E2_REPO" apply --check "$E2_ROOT/progress/E.2/inputs/exclude-source-grants.patch" &&
      git -C "$E2_REPO" apply "$E2_ROOT/progress/E.2/inputs/exclude-source-grants.patch"
    fi
    if git -C "$E2_REPO" apply --reverse --check "$E2_ROOT/progress/E.2/inputs/mapped-initial.patch"; then
      printf '%s\n' 'Mapping hook and native runtime settings are already present.'
    else
      git -C "$E2_REPO" apply --check "$E2_ROOT/progress/E.2/inputs/mapped-initial.patch" &&
      git -C "$E2_REPO" apply "$E2_ROOT/progress/E.2/inputs/mapped-initial.patch"
    fi
    mkdir -p "$E2_REPO/dist/utils/properties"
    cp progress/E.2/inputs/integration.properties "$E2_REPO/dist/utils/properties/integration.properties"
    cp progress/E.2/inputs/uat.properties "$E2_REPO/dist/utils/properties/uat.properties"
    ```

    Any patch mismatch stops preparation: inspect its actual diff rather than
    forcing it. The reverse check only detects an already applied patch; it
    does not undo it. The target properties map source key `apex.810003` to
    workspace/schema **E1_INTEGRATION**, application **810004**, alias
    **E2-INTEGRATION**. UAT has its separate mapping for the same artifact.

11. In **Terminal 2**, review the exact source/configuration/distribution changes
    and commit the accepted assessment candidate:

    ```bash
    git -C .local-apex/e2/project-walkthrough/component-repo add .dbtools src dist
    git -C .local-apex/e2/project-walkthrough/component-repo diff --cached --stat
    git -C .local-apex/e2/project-walkthrough/component-repo diff --cached
    ```

    After inspecting the changes:

    ```bash
    git -C .local-apex/e2/project-walkthrough/component-repo commit -m "Prepare mapped initial Oracle assessment candidate"
    ```

    If already committed with a clean tree, retain that commit. Existing
    historical archives are retained; D.2 generates a new mapped candidate name.

**Migration lifecycle:** PROJECT generates the migrations for this independent
delivery stream. Each target records the changesets it actually executes in
its own Liquibase history. The initial artifact contains schema definitions and
explicit initialization changesets; an upgrade adds changesets while preserving
applied history and retained application data. The exercise validates whether
this native lifecycle satisfies the scenario's installation, upgrade and
preservation requirements.

### D.2. Package and qualify the initial application

**Purpose:** deploy the mapped PROJECT artifact into integration_test and
observe working greetings/history through native restricted verification and
publication. All SQL blocks below run in **Terminal 1**. Terminal 1 remains in
`.local-apex/e2/project-walkthrough/component-repo` from its launch step.

1. Connect to the source and run native verification:

   ```sql
   connect -name lab-dev-c
   project verify -compared-branch-name e2-world-base -verbose
   ```

   The observed SQLcl 25.3 result is **Errors: 1**, for
   `stagechangelogcomplete`: the APEX SQL file is reported missing from the stage
   changelog, although `main.changelog.xml` includes it through the separate
   APEX changelog. The other seven verification results pass/report INFO.
   Retain that finding. The following explicitly labeled **assessment candidate**
   exercises deployment; it does not convert this failed gate into a formal
   release pass. Any additional/unexpected error requires diagnosis first.

2. Generate the mapped assessment candidate on its first pass. If
   `artifact/e2-1.0.0-mapped-r1.zip` already exists, skip this command and inspect
   that retained archive at step 3:

   ```sql
   project gen-artifact -name e2 -version 1.0.0-mapped-r1 -format zip
   ```

   Expected file: `artifact/e2-1.0.0-mapped-r1.zip`. If it already exists, retain
   it; do not overwrite it. The earlier unmapped candidate is not used for D.

3. In **Terminal 2**, record the actual archive hash:

   ```bash
   python3 -c 'from pathlib import Path; import hashlib; p=Path(".local-apex/e2/project-walkthrough/component-repo/artifact/e2-1.0.0-mapped-r1.zip"); print(hashlib.sha256(p.read_bytes()).hexdigest(), p)'
   ```

   The exercised archive has SHA-256
   `0377604203edf3674ae5a2b3735da11f108de6f576c879266ea1325d4bf6e0d0`.
   A newly generated archive may have different bytes; qualify that actual file
   rather than transferring the old receipt to it.

4. In **Terminal 1**, inspect the target identity and starting state:

   ```sql
   connect -name integration_test
   show user
   select application_id, owner, availability_status
     from apex_applications where application_id=810004;
   select table_name from user_tables
     where table_name in ('LAB_COMPONENTS','LAB_STATE','HELLO_ENTRIES',
       'WORLD_ENTRIES','HELLO_CONFIG','WORLD_CONFIG','GREETING_HISTORY')
     order by table_name;
   ```

   Require **E1_INTEGRATION**. A fresh target has no application 810004 and no
   business tables. The completed demonstration already has that application;
   the identical-artifact repeat below is supported and preserves its data.
   Another archive or unexplained partial installation requires inspection.

5. In **Terminal 1**, select the packaged mapping and deploy the exact candidate:

   ```sql
   set define on
   define DEFAULTS_FILE=utils/properties/integration.properties
   project deploy -file artifact/e2-1.0.0-mapped-r1.zip
   ```

   Expected first installation: **23 changesets**, successful Liquibase update
   and **Operation completed successfully**. The tested identical-artifact repeat
   executes **0 changesets**, preserving existing history/configuration. It is
   not a reset or a new fresh-install qualification.

6. In **Terminal 1**, inspect the result and enable restricted verification:

   ```sql
   select application_id, application_name, owner, availability_status
     from apex_applications where application_id=810004;
   select component, installed, version from lab_components order by component;
   select object_name, object_type from user_objects
     where status='INVALID' and object_type in ('PACKAGE','PACKAGE BODY','TRIGGER');
   begin
     apex_util.set_workspace('E1_INTEGRATION');
     apex_application_admin.set_application_status(
       810004, apex_application_admin.c_app_restricted_access,
       p_allowed_users_list=>apex_t_varchar2('VERIFIER'),
       p_message=>'Initial release verification in progress.');
     commit;
   end;
   /
   ```

   Require target **810004 / E1_INTEGRATION**, all three components installed at
   **1.0.0**, and no invalid application packages/triggers. The source identifier
   printed inside an exported script is not the target identity; the metadata
   query above verifies the actual mapping. Native Liquibase's generated
   `DATABASECHANGELOG_DETAILS` view was invalid in this client run; it is not a
   business package and is recorded separately from application validity.

7. Open the integration application and verify it in the browser:

   1. In **Terminal 2**, open the private login card:

      ```bash
      code .local-apex/e2/project-walkthrough/access.md
      ```

   2. Open [integration_test / application 810004](http://127.0.0.1:8080/ords/f?p=810004:1).
   3. Sign in as **VERIFIER** with the password on that card.
   4. On **Home**, leave the configured Hello/World defaults selected and click
      **Create greeting**. Require **Hello World — saved to history.**
   5. Open **Greeting history**. Require a new **Hello World** row with actor
      **VERIFIER**. Open **Installed components** and check all three **1.0.0** versions.
   6. Sign out using the account menu, then sign in as **LAB_USER**. Require
      **Access to this application is restricted, please try again later.**
      This demonstrates native APEX restriction before publication.

8. Return to **Terminal 1** and publish after the verifier check:

   ```sql
   declare n number;
   begin
     if user <> 'E1_INTEGRATION' then
       raise_application_error(-20870,'Wrong target');
     end if;
     select count(*) into n from lab_components
       where installed=1 and version='1.0.0'
         and component in ('Foundation','Hello','World');
     if n<>3 then raise_application_error(-20871,'Component mismatch'); end if;
     select count(*) into n from greeting_history
       where actor='VERIFIER' and greeting_text='Hello World';
     if n<1 then raise_application_error(-20872,'Verifier greeting missing'); end if;
     apex_util.set_workspace('E1_INTEGRATION');
     apex_application_admin.set_application_status(
       810004, apex_application_admin.c_app_available);
     commit;
   end;
   /
   select application_id, owner, availability_status
     from apex_applications where application_id=810004;
   ```

   Expected: **Available**. This uses the [native APEX 24.2 status API](https://docs.oracle.com/en/database/oracle/apex/24.2/aeapi/APEX_APPLICATION_ADMIN.SET_APPLICATION_STATUS-Procedure.html),
   not the E1_CTRL delivery controller. It does not claim complete request draining or
   concurrent-deployment fencing.

9. In the browser, check ordinary-user access after publication:

   1. Open [integration_test / application 810004](http://127.0.0.1:8080/ords/f?p=810004:1).
      This is the **same integration URL used in step 7**.
   2. Sign out of **VERIFIER**, or whichever account is currently signed in:
      open the username menu at the top right and choose **Sign Out**.
      If the login screen is already displayed, continue to the next step.
   3. Sign in as **LAB_USER** using the LAB_USER password on the
      [local login card](../../.local-apex/e2/project-walkthrough/access.md).
   4. Require the working **Home** page and **lab_user** in the account menu.
   5. Click **Create greeting**. Require **Hello World — saved to history.**
   6. Open **Greeting history**. Require the earlier VERIFIER row and the new
      LAB_USER row, both **Hello World**.
   7. In **Terminal 1**, inspect the saved greetings:

      ```sql
      select greeting_id as "Greeting ID",
             greeting_text as "Saved greeting",
             actor as "Created by",
             to_char(created_at, 'YYYY-MM-DD HH24:MI:SS TZH:TZM') as "Saved at"
        from greeting_history order by greeting_id;
      ```

      **Read this as application data:** **Saved greeting** is the
      actual text saved by the application, **Created by** identifies VERIFIER
      or LAB_USER, and **Saved at** gives its creation time. Find the earlier
      VERIFIER **Hello World** row and your new LAB_USER **Hello World** row.
      Repeated browser greeting actions add more rows; do not require exactly
      two or fixed greeting IDs.

   8. In **Terminal 1**, inspect the installation log:

      ```sql
      select orderexecuted as "Execution order",
             replace(filename, 'e2-world/', '') as "Migration file",
             exectype as "Result",
             to_char(dateexecuted, 'YYYY-MM-DD HH24:MI:SS') as "Applied at"
        from databasechangelog order by orderexecuted;
      ```

      **Read this as deployment history:** **Execution order** and
      **Migration file** show which changes Liquibase applied and in what order;
      **EXECUTED** means the changeset ran, and **Applied at** records when.
      Locate the table/package/trigger changes, `_custom/e2_release_data.sql`
      initialization and `releases/apex/f810003/f810003.xml` application import.
      The first installation recorded 23 changesets. The tested identical-archive
      repeat added none. This history records migrations, not greetings,
      component compatibility or a complete release-qualification decision.

**Observed result:** mapped native installation, restricted verifier access,
ordinary-user restriction, native publication, greeting/history and unchanged
business data on identical-artifact repeat passed. The
[receipt](tests/project-integration-mapped-validation.json) records the exact
archive and limits. Native verification remains a reported tool/configuration
blocker to formal release; runtime success is a separate observed result.

## E. Promote the same initial artifact to user_acceptance_test

**Purpose:** deliver the identical D-tested archive to **E1_UAT / application
810005**, verify native access/publication, and retain a real setting/history
baseline for the compatible upgrade. This is an assessment promotion; D's
reported native verification error still prevents a clean formal release claim.

The small [promotion prototype](../../scripts/cicd-project-promote.py) automates
repetitive SQLcl calls and checks. It prints its named connection, SQLcl commands,
archive hash and results. It does not recapture source, rebuild the ZIP, provision
infrastructure or perform browser acceptance for you. The browser checkpoints
remain separate actions. Use the shell commands below in **Terminal 2**; the SQL
blocks show the native operations that the prototype runs, rather than a second
sequence to execute alongside it.

### E.1. Inspect the candidate and actual target

1. In **Terminal 2**, at the main checkout root, run `inspect` to check the
   retained artifact identity, packaged UAT mapping and actual database/application
   identities before deployment. This action reads the current state without
   deploying or publishing the application:

   ```bash
   cd /Users/rstyczynski/projects/APEX_CICD
   python3 scripts/cicd-project-promote.py inspect
   ```

2. Read **ARCHIVE** and **SHA256**. Require D's retained
   `e2-1.0.0-mapped-r1.zip`, SHA-256
   `0377604203edf3674ae5a2b3735da11f108de6f576c879266ea1325d4bf6e0d0`.
   The prototype compares the actual ZIP against D's recorded evidence, inspects
   its packaged UAT mapping and native runtime settings, checks live integration
   identity/component versions, and checks the effective UAT schema.

3. Read **TARGET**. The first promotion requires schema **E1_UAT**, zero business
   tables and no application 810005. A completed promotion shows seven business
   tables and application **810005 / E1_UAT**. An unexpected partial target or
   an existing target without this prototype's deployment receipt stops writes.

4. To inspect the prototype itself:

   ```bash
   code scripts/cicd-project-promote.py
   ```

### E.2. Deploy the same bytes to UAT

1. In **Terminal 2**, run `deploy` to install the same D-tested archive into
   UAT through SQLcl PROJECT, using its packaged target mapping. On a repeat,
   it checks that deployment preserves the existing business data. `--assessment`
   selects this documented prerelease exercise despite the unresolved native
   verification finding; it does not declare a formal release pass:

   ```bash
   python3 scripts/cicd-project-promote.py deploy --assessment
   ```

2. Read the native command printed by the prototype:

   ```sql
   connect -name user_acceptance_test
   set define on
   define DEFAULTS_FILE=utils/properties/uat.properties
   project deploy -file artifact/e2-1.0.0-mapped-r1.zip
   ```

   It runs in the application repository and uses the UAT properties packaged
   inside that same archive: workspace/schema **E1_UAT**, application **810005**,
   alias **E2-UAT**. No integration application ID is reused as the target.

3. Require **Operation completed successfully** and **PASS same-byte UAT
   deployment**. The first installation executes **23 changesets**. The
   prototype checks all three **1.0.0** component versions, target ownership and
   application package/trigger validity, then writes its local deployment receipt.

4. On first installation, require **Restricted Access**. Continue at E.3 for the
   human browser checks. If the same archive was already published, the tested
   repeat executes **0 changesets**, compares every business field before/after
   and retains **Available** status. To repeat the browser restriction/publication
   exercise, continue at E.3: its first step explicitly restores restricted access.

`--assessment` explicitly labels this runtime exercise with its known native
verification finding. Omitting it blocks deployment/publication through the
prototype; it is not a formal-release verification waiver.

### E.3. Verify the UAT application before publication

1. In **Terminal 1**, explicitly put UAT into verifier-only access. Do this
   before the browser checks, including on a repeat: deployment of an already
   applied artifact preserves its current status, which may be **Available**.

   ```sql
   connect -name user_acceptance_test
   begin
     if user<>'E1_UAT' then raise_application_error(-20870,'Wrong target'); end if;
     apex_util.set_workspace('E1_UAT');
     apex_application_admin.set_application_status(
       810005, apex_application_admin.c_app_restricted_access,
       p_allowed_users_list=>apex_t_varchar2('VERIFIER'),
       p_message=>'Initial release verification in progress.');
     commit;
   end;
   /
   select application_id, owner, availability_status
     from apex_applications where application_id=810005;
   ```

   Require **810005 / E1_UAT / Restricted Access** before continuing. This
   temporarily restricts application access; it does not reinstall the application
   or reset its greetings, settings or migration history. E.4 restores **Available**.

2. In **Terminal 2**, open the prepared account details:

   ```bash
   code .local-apex/e2/project-walkthrough/access.md
   ```

3. Open [user_acceptance_test / application 810005](http://127.0.0.1:8080/ords/f?p=810005:1).
   This is the **UAT URL**, not integration application 810004.

4. If an account is already signed in, use its top-right username menu →
   **Sign Out**. Sign in as **VERIFIER** with the password on the login card.

5. On **Home**, leave the configured Hello/World defaults selected and click
   **Create greeting**. Require **Hello World — saved to history.**

6. Open **Greeting history** and find the new **Hello World** row with actor
   **VERIFIER**. Open **Installed components** and require three **1.0.0** versions.

7. Open the VERIFIER menu → **Sign Out**. Sign in at the same UAT URL as
   **LAB_USER** with its password on the card. Require **Initial release verification in progress.**

If LAB_USER can use the application, this check has **failed**. Check the
status using step 1's query, confirm the URL contains application **810005**, and
repeat step 1 followed by sign-out/login. Do not count a successful login as
restricted verification or proceed to E.4 with an unexplained result.

### E.4. Publish through the native APEX API

1. In **Terminal 2**, run `publish` to check the deployment receipt, initial
   component versions and saved VERIFIER greeting, then make UAT **Available**
   through the native APEX API. It compares business data before and after the
   operation. `--assessment` keeps this publication within the prerelease
   exercise; it does not resolve the native verification finding:

   ```bash
   python3 scripts/cicd-project-promote.py publish --assessment
   ```

   Require **PASS native UAT publication; business data unchanged**. The prototype
   verifies the resulting **Available** status and compares all business data
   before/after publication. This is native APEX availability with local prototype
   checks; it is not the E1_CTRL release controller.

2. The prototype checks its artifact/target receipt, initial component versions
   and the saved VERIFIER **Hello World** row. The following SQL shows what the
   wrapper executes; it is an explanation, not a second action to run:

   ```sql
   connect -name user_acceptance_test
   begin
     if user<>'E1_UAT' then raise_application_error(-20870,'Wrong target'); end if;
     apex_util.set_workspace('E1_UAT');
     apex_application_admin.set_application_status(
       810005, apex_application_admin.c_app_available);
     commit;
   end;
   /
   ```

### E.5. Use UAT as LAB_USER and inspect the retained setting

**Purpose:** confirm ordinary-user access after E.4 and demonstrate that the
prepared UAT configuration affects new greetings while earlier history stays
unchanged. The UAT application already has **Prefix = UAT:** and
**Default Entry Id = Hello**. No configuration edit is required in this chapter.

1. Open the **same UAT URL**, [application 810005](http://127.0.0.1:8080/ords/f?p=810005:1).

2. Sign out of **VERIFIER**, or whichever account is currently signed in, using
   the top-right username menu → **Sign Out**. If the login screen is already
   displayed, continue. Sign in as **LAB_USER** using the login-card password.

3. Require **Home** and **lab_user** in the account menu. If the restriction
   message still appears, complete E.4 before continuing.

4. Open **Greeting history**. Inspect the existing greetings and note their
   text, actor and timestamp so you can recognize them after creating a new one.
   Retain all existing rows, including the **UAT:Hello World** rows.

5. In the navigation menu, open **Hello configuration**. Confirm the existing
   row shows **Prefix = UAT:** and **Default Entry Id = Hello**. Leave the row
   unchanged. If these values differ, stop and investigate the preparation
   mismatch before continuing.

6. Open **Home** → **Create greeting**. Require
   **UAT:Hello World — saved to history.** There is no space after the colon.

7. Open **Greeting history**. Find the new LAB_USER row by its timestamp:
   **UAT:Hello World**, with Hello prefix **UAT:**. Confirm that the rows
   inspected in step 4 retain their original values. Earlier **Hello World**
   rows keep their original text and empty prefixes. A setting affects new
   greetings, not saved snapshots.

Continue at E.6 to check the preservation baseline. Keep the existing
configuration and history. Greeting IDs need not be consecutive; identify rows
by their text, actor and timestamp.

### E.6. Capture and check the preservation baseline

**Purpose:** prepare the preservation check for F, matching E.1 chapter E's
field-level baseline. Steps 1–4 establish that common scenario outcome.

Step 5 is an **additional Oracle-toolchain assessment**, not an E.1 scenario
requirement or a capability advantage established over E.1. It asks whether an
operator can repeat the same PROJECT deployment after publication without
rerunning initialization, resetting access or changing business data. This is
useful when designing pipeline retries after uncertain delivery acknowledgements.
It tests a completed deployment repeated normally; it does not prove safe retry
of a partially failed deployment or concurrent deployment.

**Native capability and prototype responsibility:** `project deploy` runs the
packaged installer, whose `lb update` uses Liquibase's applied-changeset history.
The [observed repeat](tests/project-uat-prototype-repeat.txt) reports **Run: 0**
and **Previously run: 23**. Skipping applied changesets is native SQLcl/Liquibase
behavior in this PROJECT artifact. The Python helper adds artifact-identity,
APEX-status and business-data checks; its baseline comparison is custom prototype
logic, not an APEX or PROJECT preservation guarantee. E.1 also uses Liquibase;
this result supports the sufficiency of the Oracle approach for this particular
repeat, rather than demonstrating a feature absent from E.1.

1. In **Terminal 2**, run `baseline` to record the UAT business data that later
   upgrades must preserve: existing greetings, entries and configuration values,
   together with component versions and artifact identity. On first use it saves
   a private baseline file. If that file already exists, it checks the live data
   against it and retains the original file. It does not modify application data:

   ```bash
   python3 scripts/cicd-project-promote.py baseline
   ```

2. Read the results in order:
   1. **PASS initial component versions** confirms Foundation, Hello and World
      are installed at **1.0.0**. Each `[1, "1.0.0"]` means installed flag **1**
      and version **1.0.0**.
   2. With the prepared baseline already present, require
      **PASS existing immutable baseline retained; prior fields match**.
      The original file is unchanged and its recorded business fields still
      match UAT. On a first capture instead, expect **PASS saved immutable
      baseline** followed by the file path.
   3. **BASELINE counts** reports the **current live UAT row counts**, even
      when the saved baseline is retained. For example, `"history": 5` means
      five greetings currently exist; it does not mean the saved baseline was
      replaced with five rows. Creating more greetings increases this count.
      Additional rows are allowed provided every previously recorded field
      remains unchanged. No fixed greeting count is required.

   The private file is
   `.local-apex/e2/project-walkthrough/uat-promotion/baseline.json`. It contains
   every column of each greeting, entry and configuration row present at first
   capture, plus the initial component declarations and artifact identity.

3. Inspect the actual baseline in VS Code:

   ```bash
   code .local-apex/e2/project-walkthrough/uat-promotion/baseline.json
   ```

4. Run `check-baseline` in **Terminal 2** to compare the live UAT data with
   the saved baseline. This read-only action detects changes to or loss of
   previously recorded business fields; it does not capture a replacement baseline:

   ```bash
   python3 scripts/cicd-project-promote.py check-baseline
   ```

   Require **PASS every prior business field preserved**. The check compares
   each saved row by its primary key and every saved field, including text,
   prefixes, defaults, timestamps and actor. Additional rows/columns are
   permitted; deleting a saved row/field or changing a saved value fails.
   Schema/component compatibility is a separate check. Repeating `baseline`
   retains the existing file and checks it instead of replacing it.

5. **Additional assessment — repeat a completed PROJECT deployment.** In
   **Terminal 2**, repeat `deploy --assessment` to apply the identical
   archive again as a prerelease assessment. Then run `check-baseline` to verify
   that the original retained data survived the repeat. These two commands
   demonstrate repeat deployment and preservation as separate checks:

   ```bash
   python3 scripts/cicd-project-promote.py deploy --assessment
   python3 scripts/cicd-project-promote.py check-baseline
   ```

   Read the two results separately:
   1. From `deploy --assessment`, require **0 changesets executed**, target
      status **Available**, and **PASS same-byte UAT deployment; inspect the
      printed native changeset results**. This repeats the installed initial
      artifact; it does not apply the future Hello patch.
   2. The helper also prints **NEXT browser: VERIFIER greeting/history;
      LAB_USER must be blocked while Restricted Access. If already Available,
      this was a preserved repeat.** For this E.6 repeat, the target remains
      **Available**. That generic prompt does not require another E.3/E.4 cycle
      or another restriction check. Continue with `check-baseline` above.
   3. From `check-baseline`, require **PASS every prior business field
      preserved; new rows/columns are permitted**. This confirms the saved
      business fields survived the repeat; additional greetings are allowed.

   With these results, E.6 is complete. Keep the original baseline for F;
   any later upgrade must check its saved fields as well as the new component
   version and behavior.

**Observed result:** same-byte UAT promotion, restricted verifier access, native
publication, ordinary-user greeting/history, retained `UAT:` configuration,
immutable full-field baseline and same-artifact repeat passed. The
[UAT receipt](tests/project-uat-promotion-validation.json) records evidence.
The helper is an Elaboration automation prototype: local receipts are not a
production trust/provenance service, it does not serialize competing deployers,
and it does not automate browser acceptance or infer component compatibility.
Existing pipeline/provenance/recovery work remains separate; formal native
verification still has the recorded APEX issue.

## F. Deliver the compatible Hello patch

**Goal:** demonstrate that developers can make independent changes in APEX
Working Copies, combine their reviewed changes in Main without losing either
edit, and use SQLcl PROJECT and Git to deliver a compatible Hello upgrade while
preserving existing UAT data and configuration.

The journey has two distinct outcomes:

1. **F.1 — Authoring and team checkpoint.** One Working Copy changes Home;
   a second Working Copy changes Greeting history. Merge the second copy into
   Main, refresh that accepted change into the first copy, then merge the first
   copy. Main receives edits through these reviewed merges. Export the agreed
   Main with native `project export`, review the files and commit them in Git.
2. **F.2 — Release and upgrade.** Use native SQLcl PROJECT commands to stage,
   verify, package and deploy the compatible Hello **1.0.1** release. Qualify
   both fresh installation and upgrade from **1.0.0**, then deliver the same
   qualified artifact to retained UAT and check its saved business fields.

The two-copy exercise demonstrates coordination of disjoint page changes; it
is not a text merge of competing edits to the same page. The visible heading
changes in F.1 establish the authoring/capture path. They do not themselves
implement or prove the Hello **1.0.1** component upgrade. F.2 must supply that
separate release evidence. Builder handles authoring; SQLcl PROJECT handles
capture and delivery; Git records the reviewed checkpoints.

**Execution boundary:** F.1 and F.2 have detailed operator instructions. F.2
integration qualification is rehearsed; UAT promotion remains for your execution.
Completing F.1 alone does not complete F.

### F.1. Make a small Working Copy change

**Purpose:** combine independent edits from two Working Copies through reviewed
merges into Main, then capture the agreed Main state through native SQLcl
PROJECT and Git.
The result is an authoring checkpoint. Component versions remain **1.0.0** here;
F.2 must separately build and qualify the compatible Hello **1.0.1** release.
No integration or UAT deployment takes place in F.1.

Use **Main application 810003**, **APEX Delivery Laboratory**, in workspace and
parsing schema **E1_DEV_C**. Applications **810004** and **810005** are delivery
targets; leave them unchanged. Application **810103 / E2 F1 rehearsal** and its
copy are retained rehearsal evidence, not the Main application for your steps.

#### F.1.1. Prepare the Git branch and authoring connection

1. In **Terminal 2**, the regular shell at the main checkout root, inspect the
   application repository before creating the patch branch:

   ```bash
   cd /Users/rstyczynski/projects/APEX_CICD
   git -C .local-apex/e2/project-walkthrough/component-repo status --short --branch
   git -C .local-apex/e2/project-walkthrough/component-repo log -1 --oneline
   ```

   Require a clean **e2-world** branch at the mapped initial candidate commit
   **87fa1dc**. If changes are present, inspect them before proceeding; do not
   discard them to satisfy this check.

2. Create a development branch from that retained initial checkpoint. These
   commands affect Git, not a database schema:

   ```bash
   git -C .local-apex/e2/project-walkthrough/component-repo switch e2-world
   git -C .local-apex/e2/project-walkthrough/component-repo switch -c e2-hello-patch
   ```

   For a resumed F.1 with this branch already created, use `switch e2-hello-patch`
   instead of `switch -c`. Keep its existing work. The remaining steps describe
   the first execution; inspect existing edits rather than create duplicate copies.

3. In **Terminal 1**, the SQLcl session launched in the application repository,
   check the authoring connection and Main's initial state one result at a time.

   1. Connect to the authoring schema and display the current user:

      ```sql
      connect -name lab-dev-c
      show user
      ```

      Require **E1_DEV_C** before continuing.

   2. Identify Main and check its availability:

      ```sql
      select application_id, application_name, owner, availability_status
        from apex_applications where application_id=810003;
      ```

      Require one row: **810003 / APEX Delivery Laboratory / E1_DEV_C / Available**.

   3. Inspect the two pages used by this exercise:

      ```sql
      select page_id, page_name, page_title
        from apex_application_pages
        where application_id=810003 and page_id in (1,10) order by page_id;
      ```

      Require these two rows:
      - **Page 1:** Name **Home**, Title **APEX Delivery Laboratory**.
      - **Page 10:** Name **Greeting history**, Title **Greeting history**.

      Page 10's Title is the starting value for the independent Main edit.

   4. Inspect Home's region heading:

      ```sql
      select page_id, region_name
        from apex_application_page_regions
        where application_id=810003 and page_id=1;
      ```

      Require page **1**, region **APEX Delivery Laboratory**. This region Name
      is the starting value for the Working Copy edit.

   5. Inspect installed component versions:

      ```sql
      select component, installed, version from lab_components order by component;
      ```

      Require **Foundation**, **Hello** and **World**, each with **Installed = 1**
      and **Version = 1.0.0**. If any check differs, inspect the mismatch before
      continuing with the edits.

4. In **Terminal 2**, open the same private Markdown login card used in D/E.
   It already contains the Builder workspace, developer username and password:

   ```bash
   code .local-apex/e2/project-walkthrough/access.md
   ```

   Find **Builder**, **Workspace**, **Developer** and **Developer password**.

5. Open [APEX Builder](http://127.0.0.1:8080/ords/apex). If another workspace is
   signed in, use the top-right account menu → **Sign Out**. Enter
   **Workspace = E1_DEV_C**, **Username = DEV_C**, and the **Developer password**
   from the Markdown login card.
   Click **Sign In**, then **App Builder** → **APEX Delivery Laboratory 810003**.
   Confirm **Application 810003** in the breadcrumb before editing.

#### F.1.2. Make the isolated Home-heading change

1. On application 810003's home page, find **Working Copy Tasks** on the right
   and click **Create Working Copy**.
   1. Require **Main Application ID = 810003**.
   2. Set **Working Copy Name = E2 Hello patch**.
   3. Set **Working Copy Description = Home heading change for PROJECT capture**.
   4. Click **Create Working Copy** and wait for its application home to open.
   5. Record the assigned **Application** number from the breadcrumb. It is a
      separate APEX application ID, not a new schema. Do not assume the rehearsal
      copy's ID **101** will be assigned to your copy.

2. In that Working Copy, click **1 - Home**. Wait for Page Designer to load.
   1. Confirm the toolbar shows **Working Copy: E2 Hello patch**.
   2. In the left **Rendering** tree, expand **Components → Breadcrumb Bar**
      if necessary and click the **APEX Delivery Laboratory** region.
   3. On the right, require the property-editor tab **Region**, not **Page**.
   4. Under **Identification**, change **Name** to exactly
      **Hello World - Working Copy**. This is the visible Hero-region heading;
      changing only the page Name or browser Title would not change that heading.
   5. Press **Tab** to finish editing the field, then click **Save**. Wait for
      saving to finish and confirm the region's new name in the Rendering tree.

#### F.1.3. Merge the second developer's independent change

Use a second Working Copy to represent the other developer's task. Both tasks
use the prepared **DEV_C** account in this lab; this is a coordination exercise,
not a test of access separation between developer identities.

**Continuing the earlier instructions:** if you already saved page 10's Title
as **Greeting history - Main checkpoint** directly in Main, retain that edit.
Use step 5 below to return to **E2 Hello patch**, then continue at F.1.4. Do not
undo or repeat your saved work. That execution used the earlier direct-Main
shortcut; it does not demonstrate the second-copy merge described here.

1. From Page Designer in **E2 Hello patch**, click its Working Copy dropdown
   near **Save**, then **Switch to Main**. Require **Application 810003** and
   **Main** in the toolbar. Navigate here to create the second copy; do not
   edit Main's page properties.

2. Click the **Application 810003** breadcrumb to open its application home.
   Under **Working Copy Tasks**, click **Create Working Copy**.
   1. Require **Main Application ID = 810003**.
   2. Set **Working Copy Name = E2 History update**.
   3. Set **Working Copy Description = Independent history heading change**.
   4. Click **Create Working Copy** and wait for its home page to open.
   5. Record its assigned application ID. Confirm this is **E2 History update**,
      distinct from Main and **E2 Hello patch**.

3. In **E2 History update**, click **10 - Greeting history** and wait for Page
   Designer to load.
   1. Confirm the toolbar shows **Working Copy: E2 History update**.
   2. In the left Rendering tree, click the top **Page 10: Greeting history** node.
   3. On the right, require the **Page** property-editor tab.
   4. Under **Identification**, change **Title** to exactly
      **Greeting history - Main checkpoint**. Keep **Name = Greeting history**
      and its alias unchanged.
   5. Press **Tab**, click **Save**, and wait for saving to finish.

4. Bring that reviewed page into Main through a native merge:
   1. Open **Working Copy: E2 History update → Merge into Main**.
   2. Wait for comparison to finish. Require only
      **1 Changed: Greeting history / PAGE:10**. The other copy's Home edit is
      still private and must not appear as a Main change here.
   3. Keep only **Greeting history / PAGE:10** checked and click **Next**.
   4. Require exactly that page in **Selected Components**.
   5. Keep **Backup target app first** checked and
      **Delete Working Copy after merge** unchecked.
   6. Click **Confirm Merge**. Require
      **Your changes have been successfully merged!** and **Application 810003 / Main**.

5. Switch from Main back to the first Working Copy:
   1. Find the **Main** button with a branch icon and down arrow near **Save**
      in the top toolbar. Its tooltip is **Working Copy: Main**.
   2. Open the dropdown, then **Working Copies**. Wait for the submenu.
   3. Click **E2 Hello patch - <number>**, not **E2 History update**. The number
      is displayed in the submenu; you do not type or substitute an ID.
   4. Wait for the page to reload. Require **E2 Hello patch** in the toolbar
      and its private application number rather than **810003**. This copy
      still has its Home edit and now needs the accepted page 10 change.

#### F.1.4. Compare and refresh only Main's page 10

1. Open **Working Copy: E2 Hello patch → Compare Working Copy with Main**.
   Wait until the background comparison finishes and the progress indicator
   disappears. Require **2 Changed**, with **Home / PAGE:1** and
   **Greeting history / PAGE:10**. An initial **0 Changed** while processing is
   not the completed comparison result.

   Comparison uses APEX background jobs. The prepared lab has
   **JOB_QUEUE_PROCESSES = 10** in both CDB and PDB. If comparison remains queued,
   stop for scheduler inspection; do not interpret a busy screen as no changes.

2. Switch from the comparison report to the refresh operation:
   1. In the top-right toolbar, click **E2 Hello patch ▾** (the Working Copy
      dropdown), then choose **Refresh Working Copy**.
   2. Wait for the comparison to finish. Require the page heading
      **Refresh E2 Hello patch from Main**. If it still says
      **Compare E2 Hello patch with Main**, you are in the read-only comparison
      report; open the dropdown again and choose **Refresh Working Copy**.
   3. In the refresh report, find the checkbox column at the far left of the
      differences table. It is present in **Refresh**, not in **Compare**.
   4. **Uncheck** the checkbox beside **Home / PAGE:1**. “Uncheck” means remove
      its selection, not delete or clear the page.
   5. Leave only **Greeting history / PAGE:10** checked. The initial refresh UI
      checks both rows; accepting that default would replace your copy's Home edit.
   6. Click **Next**. Require exactly **1 Changed**, **Greeting history / PAGE:10**.
   7. Keep **Backup target app first** checked. Here the target is the copy.
   8. Click **Confirm Refresh** and wait for
      **Your changes have been successfully refreshed!**

3. On the copy's application home, click **10 - Greeting history** and check
   the Page **Title** is **Greeting history - Main checkpoint**. Open page **1**
   and confirm its region **Hello World - Working Copy** remains. No additional
   edit is needed.

#### F.1.5. Merge only the copy's Home page into Main

1. In the copy, open **Working Copy: E2 Hello patch → Merge into Main**.
   Wait for comparison to finish. Require only **1 Changed: Home / PAGE:1**.
   Page 10 should now match Main because of the refresh.

2. Keep only **Home / PAGE:1** checked and click **Next**.
   1. Require **1 Changed: Home / PAGE:1** in Selected Components.
   2. Keep **Backup target app first** checked. Here the target is Main.
   3. Leave **Delete Working Copy after merge** unchecked, retaining the copy
      for inspection.
   4. Click **Confirm Merge** and wait for
      **Your changes have been successfully merged!**
   5. Require **Application 810003 / Working Copy: Main** after completion.
      Under **Backups → Manage backups**, inspect the retained Main backup.

3. Open [Main's Home page](http://127.0.0.1:8080/ords/f?p=810003:1) in a runtime
   browser tab. Sign in as **LAB_USER** using the existing login-card password
   if prompted. Refresh an already open page.
   1. Require the visible heading **Hello World - Working Copy**.
   2. Click **Greeting history**. Require the page heading/browser title
      **Greeting history - Main checkpoint**. The navigation entry may remain
      **Greeting history**, because its label was not changed.
   3. Existing greeting rows remain unchanged; these edits change application
      presentation, not greetings, prefixes or component versions.

#### F.1.6. Capture the agreed Main checkpoint with SQLcl PROJECT

1. In **Terminal 1**, read Main's saved metadata using the same queries as F.1.1, step 3.
   Require the new page 1 region name and page 10 title, with three component
   versions still **1.0.0**.

2. Still in **Terminal 1**, list the objects selected by PROJECT before writing
   source files. `-list` previews the configured export selection:

   ```sql
   project export -list
   ```

   Under **APEX_APPLICATIONS**, require **application_id=810003** only. The
   filter also selects this schema's application database objects. Your private
   Working Copy and rehearsal application **810103** must not be listed.

3. Export that agreed Main state into the existing application repository:

   ```sql
   project export
   ```

   Require **Exporting Workspace E1_DEV_C - application 810003** and the export
   completion summary. This captures source SQL and readable YAML; it does not
   stage a release, build an archive or deploy to UAT.

4. In **Terminal 2**, inspect the captured changes and open the readable files
   in VS Code. These commands target the application repository, not the main
   toolchain repository:

   ```bash
   git -C .local-apex/e2/project-walkthrough/component-repo status --short --branch
   git -C .local-apex/e2/project-walkthrough/component-repo diff --stat
   git -C .local-apex/e2/project-walkthrough/component-repo diff -- src/database/e1_dev_c/apex_apps/f810003
   code .local-apex/e2/project-walkthrough/component-repo/src/database/e1_dev_c/apex_apps/f810003/readable/application/pages/p00001.yaml
   code .local-apex/e2/project-walkthrough/component-repo/src/database/e1_dev_c/apex_apps/f810003/readable/application/pages/p00010.yaml
   ```

   Find **Hello World - Working Copy** in page 1's region definition and
   **Greeting history - Main checkpoint** in page 10's title. Review the matching
   SQL export changes. Investigate unrelated differences before committing.
   In VS Code's Explorer, confirm no new application folder for the private copy
   was introduced. The export list is the authoritative selection check; retained
   files from earlier exports alone do not prove that they were exported now.

5. Commit only the reviewed Main application capture to the patch branch:

   ```bash
   git -C .local-apex/e2/project-walkthrough/component-repo add src/database/e1_dev_c/apex_apps/f810003
   git -C .local-apex/e2/project-walkthrough/component-repo diff --cached --stat
   git -C .local-apex/e2/project-walkthrough/component-repo commit -m "Capture Main checkpoint after Working Copy refresh and merge"
   git -C .local-apex/e2/project-walkthrough/component-repo log -1 --oneline
   git -C .local-apex/e2/project-walkthrough/component-repo status --short --branch
   ```

   Require branch **e2-hello-patch** and a commit containing both intended edits.
   Keep the initial `dist/` and its already qualified archive unchanged in F.1.
   Any remaining unstaged changes need review before F.2.

**Check:** this commit is the agreed Main team checkpoint. Native refresh/merge
selected whole pages; Git records the exported result. A Working Copy shares its
Main parsing schema, so it does not isolate schema or business-data edits.
See Oracle's [APEX 24.2 Working Copy guidance](https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/about-working-copies.html).
The [F.1 rehearsal record](tests/project-f1-working-copy-validation.json) identifies
the separate rehearsal applications and the actual checks performed.

### F.2. Capture, qualify and deliver the compatible Hello upgrade

**Purpose:** deliver the real Hello **1.0.1** correction using native SQLcl
PROJECT, demonstrate both fresh installation and upgrade from **1.0.0**, then
promote the identical assessment archive to UAT while preserving its settings
and greeting history. Foundation and World remain **1.0.0**.

The correction trims surrounding spaces, tabs and line breaks from new Hello
entries and rejects whitespace-only entries. It does not rewrite existing
entries or greetings. The new constraint requires existing Hello entries to
contain a non-whitespace character; the upgrade preflight below checks that
condition. This is a qualified data starting state, not automatic SemVer inference.

**Starting point:** your completed F.1 checkpoint **c79fe9d** is retained.
Use a separate execution clone at that checkpoint so the release operations below
have not already run. The existing `component-repo` and its assessment archives
remain reference evidence. The author schema already contains the Hello 1.0.1
correction; you will capture it yourself and build a new candidate.

Integration is disposable qualification space. UAT retains its existing settings
and history. F.2 tests installation from empty, upgrade over populated 1.0.0 and
promotion of the identical qualified archive. These are operator-run SQLcl
operations with explicit SQL assertions; they are not an automated pipeline.

#### F.2.1. Start from the F.1 checkpoint and inspect the change

1. In **Terminal 2**, at the main APEX_CICD checkout root, create a separate
   application repository for your execution. The clone preserves the original
   repository and makes the initial comparison branch available locally:

   ```bash
   git clone --no-hardlinks --branch e2-world .local-apex/e2/project-walkthrough/component-repo .local-apex/e2/project-walkthrough/component-repo-f2
   git -C .local-apex/e2/project-walkthrough/component-repo-f2 switch -c e2-hello-patch c79fe9d
   git -C .local-apex/e2/project-walkthrough/component-repo-f2 status --short --branch
   git -C .local-apex/e2/project-walkthrough/component-repo-f2 log -1 --oneline
   ```

   Require a clean **e2-hello-patch** branch at **c79fe9d**. If the destination
   already exists, stop and inspect its state: this initialization runs once.
   Do not repeat it over a partially completed execution.

2. Copy only the unchanged initial archive needed for the later upgrade test.
   This does not copy the prepared patch distribution:

   ```bash
   mkdir .local-apex/e2/project-walkthrough/component-repo-f2/artifact
   cp .local-apex/e2/project-walkthrough/component-repo/artifact/e2-1.0.0-mapped-r1.zip .local-apex/e2/project-walkthrough/component-repo-f2/artifact/
   code progress/E.2/inputs/hello-1.0.1-patch.sql
   ```

   The SQL implements the business correction: trim surrounding whitespace,
   reject whitespace-only Hello entries, and declare Hello 1.0.1. Existing
   business rows are not rewritten. Working Copies isolate APEX metadata;
   this schema correction is shared by them.

3. In **Terminal 1**, exit the old SQLcl session with `exit`. In that terminal's
   regular shell, launch SQLcl in the new application repository. Use the
   explicit APEX_CICD path: `git rev-parse --show-toplevel` inside an application
   repository returns that nested repository, not the main project. The `&&`
   prevents launching SQLcl if changing directory fails:

   ```bash
   cd /Users/rstyczynski/projects/APEX_CICD
   E2_PROJECT_ROOT="$PWD"
   cd "$E2_PROJECT_ROOT/.local-apex/e2/project-walkthrough/component-repo-f2" &&
   JAVA_HOME="$E2_PROJECT_ROOT/.local-apex/tools/jdk-21.0.12.1+1/Contents/Home" \
     "$E2_PROJECT_ROOT/.local-apex/tools/sqlcl/bin/sql" \
     -home "$E2_PROJECT_ROOT/.local-apex/tools/sqlcl-home" /nolog
   ```

   At `SQL>`, connect to the author and check the directory:

   ```sql
   pwd
   connect -name lab-dev-c
   show user
   ```

   Require **component-repo-f2** and **E1_DEV_C**. All subsequent SQL blocks in
   F.2 run in this session. Terminal 2 stays at the main checkout root.

4. Execute the reviewed correction. In the current lab it reports that the
   correction is already applied, then prints its definitions:

   ```sql
   @../../../../progress/E.2/inputs/hello-1.0.1-patch.sql
   ```

   Require Foundation **1.0.0**, Hello **1.0.1**, World **1.0.0**, and
   **HELLO_TEXT_NONBLANK / ENABLED / VALIDATED**. This does not edit Main's pages.

5. Verify normalization and rejection with inserts that are rolled back:

   ```sql
   @../../../../progress/E.2/inputs/f2-verify-hello.sql
   ```

   Require **PASS whitespace-only Hello rejected with ORA-20314** and
   **PASS Hello 1.0.1 normalization; verification inserts rolled back**.
   Sequence values may have gaps; existing business rows remain unchanged.

**Captured F.1 detail:** page 1's visible region is **Hello World - Working Copy**.
Page 10's committed Name is **Greeting history - Main checkpoint**; its Title
remains **Greeting history**. Preserve this checkpoint without additional UI edits.

#### F.2.2. Freeze the initial history, capture the patch and build your candidate

**Purpose:** execute the native PROJECT preparation yourself. The existing
migration history is **1.0.0**; the new application candidate is **1.0.1**.
Run each preparation operation once, in order. Stop on an unexpected error.

1. In **Terminal 1**, freeze the initial migrations before staging the patch:

   ```sql
   project release -version 1.0.0 -verbose
   ```

   Require successful creation of `dist/releases/1.0.0`. This preserves the
   initial changeset identities. It does not deploy or publish version 1.0.0.
   An “already exists” error means this preparation step has already run in the
   selected repository; do not continue as if a fresh execution had succeeded.

2. In **Terminal 1 (SQLcl)**, capture the corrected schema and agreed Main application:

   ```sql
   project export -list
   project export
   ```

   Require only application **810003** in the APEX selection. Private Working
   Copies are excluded.

3. Switch to **Terminal 2 (regular shell)**. Inspect the source capture before
   committing it. Terminal 2 must be at the main APEX_CICD checkout root:

   ```bash
   cd /Users/rstyczynski/projects/APEX_CICD
   git -C .local-apex/e2/project-walkthrough/component-repo-f2 diff -- src
   git -C .local-apex/e2/project-walkthrough/component-repo-f2 diff --stat -- dist
   git -C .local-apex/e2/project-walkthrough/component-repo-f2 add src dist
   git -C .local-apex/e2/project-walkthrough/component-repo-f2 commit -m "Freeze initial history and capture Hello 1.0.1"
   ```

   Review the Hello constraint/trigger correction and frozen migration paths.
   Commit IDs will differ from the reference preparation.

4. In **Terminal 1**, generate the migrations against the initial source branch:

   ```sql
   project stage -branch-name e2-world -verbose
   project stage add-custom -file-name hello_1_0_1_version.sql
   ```

   Require successful staging and creation of the custom SQL file under
   `dist/releases/next/changes/e2-hello-patch/_custom/`. The native custom file
   contains a generated Liquibase changeset header; keep that header intact.

5. In **Terminal 2 (regular shell)**, populate the generated custom changeset
   from the reviewed SQL input. This retains PROJECT's header and appends the
   version update once. A repeated execution verifies the existing content:

   ```bash
   cd /Users/rstyczynski/projects/APEX_CICD
   F2_CUSTOM=.local-apex/e2/project-walkthrough/component-repo-f2/dist/releases/next/changes/e2-hello-patch/_custom/hello_1_0_1_version.sql
   if ! rg -q "update lab_components set version='1.0.1'" "$F2_CUSTOM"; then
     sed '$r progress/E.2/inputs/hello-1.0.1-release-data.sql' "$F2_CUSTOM" > "$F2_CUSTOM.tmp" &&
     mv "$F2_CUSTOM.tmp" "$F2_CUSTOM"
   fi
   python3 -c 'from pathlib import Path; p=Path(".local-apex/e2/project-walkthrough/component-repo-f2/dist/releases/next/changes/e2-hello-patch/_custom/hello_1_0_1_version.sql"); s=p.read_text(); body=Path("progress/E.2/inputs/hello-1.0.1-release-data.sql").read_text(); assert s.endswith(body), "STOP: custom SQL does not match reviewed input"; assert s.count("-- changeset ")==1, "STOP: generated header missing or duplicated"; print("PASS custom changeset contains reviewed Hello version update")'
   ```

   Require **PASS custom changeset contains reviewed Hello version update**.
   The SQL checks the initial component versions and applied correction, then
   updates only Hello's version. It does not copy author business data.

6. Review the generated dependency order in **Terminal 2**:

   ```bash
   code .local-apex/e2/project-walkthrough/component-repo-f2/dist/releases/main.changelog.xml
   code .local-apex/e2/project-walkthrough/component-repo-f2/dist/releases/next/changes/e2-hello-patch/stage.changelog.xml
   ```

   Require the main chain to include **1.0.0 → APEX → next**. Require the patch
   stage to include **hello_entries constraint → hello_entries_guard trigger →
   custom Hello version SQL**. Inspect the included SQL files, not only names.
   Initial release-data SQL remains unchanged and retains its changeset identity.

7. In **Terminal 2 (regular shell)**, apply the candidate's APEX settings
   with `sed`. This replaces existing arguments and also removes any four settings
   accidentally pasted before `p_id`. It leaves the source export unchanged.
   A temporary file avoids macOS/Windows differences in `sed -i` syntax:

   ```bash
   cd /Users/rstyczynski/projects/APEX_CICD
   F2_APEX_FILE=.local-apex/e2/project-walkthrough/component-repo-f2/dist/releases/apex/f810003/f810003.sql
   sed \
     -e '/wwv_imp_workspace\.create_flow(/,/^[[:space:]]*p_id=>/ {
   /p_flow_version=>/d
   /p_flow_status=>/d
   /p_restrict_to_user_list=>/d
   /p_vpd=>/d
   }' \
     -e "s/^[[:space:]]*,p_flow_version=>.*/,p_flow_version=>'1.0.1'/" \
     -e "s/^[[:space:]]*,p_flow_status=>.*/,p_flow_status=>'RESTRICTED_ACCESS'/" \
     -e "s/^[[:space:]]*,p_restrict_to_user_list=>.*/,p_restrict_to_user_list=>'VERIFIER'/" \
     -e 's/^[[:space:]]*,p_vpd=>.*/,p_vpd=>null/' \
     "$F2_APEX_FILE" > "$F2_APEX_FILE.tmp" &&
   mv "$F2_APEX_FILE.tmp" "$F2_APEX_FILE"
   rg -n '^,p_(flow_version|flow_status|restrict_to_user_list|vpd)=>' "$F2_APEX_FILE"
   ```

   Require exactly four matching lines with these values:

   ```text
   ,p_flow_version=>'1.0.1'
   ,p_flow_status=>'RESTRICTED_ACCESS'
   ,p_restrict_to_user_list=>'VERIFIER'
   ,p_vpd=>null
   ```

   This sets the assembly footer and native restricted verification, and removes
   the inherited E1_CTRL runtime hook from this candidate. Component versions
   remain separately declared. Do not run `project stage` again after this edit:
   it regenerates the APEX distribution from Main's original settings.

8. Retain the reviewed mapping and explicit component declaration. In
   **Terminal 2**, copy the reference declaration, then inspect the mapping:

   ```bash
   cp .local-apex/e2/project-walkthrough/component-repo/dist/component-contract.json .local-apex/e2/project-walkthrough/component-repo-f2/dist/component-contract.json
   code .local-apex/e2/project-walkthrough/component-repo-f2/dist/component-contract.json
   code .local-apex/e2/project-walkthrough/component-repo-f2/dist/install.sql
   code .local-apex/e2/project-walkthrough/component-repo-f2/dist/utils/properties/integration.properties
   code .local-apex/e2/project-walkthrough/component-repo-f2/dist/utils/properties/uat.properties
   ```

   Require Foundation/Hello/World **1.0.0/1.0.1/1.0.0** in the declaration;
   PROJECT does not infer or enforce semantic compatibility from it. Require
   `-defaults-file &DEFAULTS_FILE` in the installer and source key `apex.810003`
   mapped to integration **810004 / E1_INTEGRATION / E2-INTEGRATION** and UAT
   **810005 / E1_UAT / E2-UAT**. These mappings are inherited from checkpoint D.

9. In **Terminal 1**, run native verification before packaging:

   ```sql
   project verify -compared-branch-name e2-world -verbose
   ```

   The reference preparation reported **Errors: 1 / Warnings: 0 / Info: 7**:
   **stagechangelogcomplete** lists frozen initial-source files and the separately
   included APEX source. Compare the finding with
   [the retained output](tests/project-f2-operator-verify-build.txt). Stop and
   diagnose any additional error. This known finding blocks a **formal release
   pass**; the following candidate is an explicit prerelease runtime assessment.

10. In **Terminal 2**, review and commit your complete distribution:

   ```bash
   git -C .local-apex/e2/project-walkthrough/component-repo-f2 diff -- dist
   git -C .local-apex/e2/project-walkthrough/component-repo-f2 add dist
   git -C .local-apex/e2/project-walkthrough/component-repo-f2 commit -m "Prepare mapped Hello 1.0.1 execution candidate"
   ```

11. Switch to **Terminal 1 (SQLcl)**. Generate your new assessment archive:

   ```sql
   project gen-artifact -name e2 -version 1.0.1-execution-r2 -format zip
   ```

   Require **artifact/e2-1.0.1-execution-r2.zip**. This archive is new; do not
   substitute the reference archive or overwrite it on a retry. A changed build
   requires a new candidate name and qualification.

12. In **Terminal 2**, record your archive's hash before qualification. This
    records identity; it is not evidence that runtime qualification has passed:

    ```bash
    python3 -c 'from pathlib import Path; import hashlib; p=Path(".local-apex/e2/project-walkthrough/component-repo-f2/artifact/e2-1.0.1-execution-r2.zip"); h=hashlib.sha256(p.read_bytes()).hexdigest(); p.with_suffix(".sha256").write_text(h+"\n"); print(h)'
    ```

    Keep that hash and use the exact same archive throughout F.2.3–F.2.7.
    Its hash will differ from the reference archive because the native generated
    changeset metadata is new. The [reference qualification receipt](tests/project-f2-upgrade-validation.json)
    establishes previous observations, not qualification of your new bytes.
    The copied initial archive must retain SHA-256
    **0377604203edf3674ae5a2b3735da11f108de6f576c879266ea1325d4bf6e0d0**.

#### F.2.3. Qualify the patch from an empty integration target

**Purpose:** show the cumulative patch archive can reconstruct the complete
application from empty. This deliberately deletes only disposable integration
application **810004** and its test tables/data. It retains its workspace/accounts.
UAT is not reset anywhere in F.2.

1. In **Terminal 1**, select and confirm the disposable target:

   ```sql
   connect -name integration_test
   show user
   ```

   Require **E1_INTEGRATION** before the reset.

2. Execute the explicitly guarded integration reset:

   ```sql
   @../../../../progress/E.2/inputs/f2-reset-integration.sql RESET_E1_INTEGRATION
   ```

   Require **PASS disposable integration application and tables removed; UAT
   not touched**, **REMAINING_TABLES = 0**, and **REMAINING_APPLICATION = 0**.
   The SQL refuses another schema, an unexpected application or unrelated tables.

3. Select the candidate's packaged integration mapping and deploy it:

   ```sql
   set define on
   define DEFAULTS_FILE=utils/properties/integration.properties
   project deploy -file artifact/e2-1.0.1-execution-r2.zip
   ```

   Require **Operation completed successfully**, **Run: 26 / Previously run: 0**.
   These counts cover initial schema/data, the updated APEX application, and the
   three Hello patch changesets. No separate initial-archive deployment is needed
   for this fresh-install test.

4. Verify the actual mapped application:

   ```sql
   select application_id, owner, availability_status
     from apex_applications where application_id=810004;
   ```

   Require **810004 / E1_INTEGRATION / Restricted Access**.

5. Run the reviewed component and rolled-back behavior checks on this target:

   ```sql
   @../../../../progress/E.2/inputs/f2-verify-hello.sql
   ```

   Require both PASS messages from F.2.1 step 5 and component versions
   **Foundation 1.0.0 / Hello 1.0.1 / World 1.0.0**.

6. Set an explicit native verification message and allowed account:

   ```sql
   begin
     if user<>'E1_INTEGRATION' then raise_application_error(-20870,'Wrong target'); end if;
     apex_util.set_workspace('E1_INTEGRATION');
     apex_application_admin.set_application_status(
       810004, apex_application_admin.c_app_restricted_access,
       p_allowed_users_list=>apex_t_varchar2('VERIFIER'),
       p_message=>'Hello patch verification in progress.');
     commit;
   end;
   /
   ```

   Require **PL/SQL procedure successfully completed**.

7. Verify the browser path on [integration / application 810004](http://127.0.0.1:8080/ords/f?p=810004:1):

   1. Reload after reconstruction; an old application session may require login.

   2. Sign out of any current account and sign in as **VERIFIER**, using the
      password in `.local-apex/e2/project-walkthrough/access.md`.

   3. On Home, require **Hello World - Working Copy** and click **Create greeting**.
      Require **Hello World — saved to history.**

   4. Open **Greeting history** and find that VERIFIER row. Open **Installed
      components** and require **1.0.0 / 1.0.1 / 1.0.0** for Foundation/Hello/World.

   5. Use the VERIFIER menu → **Sign Out**. At the same integration URL, sign
      in as **LAB_USER**. Require **Hello patch verification in progress.**

8. In **Terminal 1**, publish through the native APEX API:

   ```sql
   begin
     if user<>'E1_INTEGRATION' then raise_application_error(-20870,'Wrong target'); end if;
     apex_util.set_workspace('E1_INTEGRATION');
     apex_application_admin.set_application_status(810004,apex_application_admin.c_app_available);
     commit;
   end;
   /
   ```

   Require **PL/SQL procedure successfully completed**. Refresh the blocked
   browser page as LAB_USER; require Home, then create a **Hello World** greeting.
   Fresh-install qualification is complete. Its test data will be replaced by
   the separate integration reconstruction in F.2.4.

#### F.2.4. Qualify an upgrade over populated 1.0.0

**Purpose:** test the same patch bytes against an existing application, including
retained settings and history. Fresh installation alone does not establish this.

1. In **Terminal 1**, remain connected as **E1_INTEGRATION**. Reset only the
   disposable integration fixture again:

   ```sql
   show user
   @../../../../progress/E.2/inputs/f2-reset-integration.sql RESET_E1_INTEGRATION
   ```

   Require **E1_INTEGRATION**, the reset PASS and both zero counts.

2. Reconstruct the original initial archive using its integration mapping:

   ```sql
   set define on
   define DEFAULTS_FILE=utils/properties/integration.properties
   project deploy -file artifact/e2-1.0.0-mapped-r1.zip
   ```

   Require **Run: 23 / Previously run: 0** and **Operation completed successfully**.

3. Add the reviewed new test fixtures. This SQL sets the integration-only prefix
   to `QUAL:` and saves a `QUAL:Hello World` snapshot through an APEX VERIFIER
   session. These are literal qualification examples, not imported UAT data:

   ```sql
   @../../../../progress/E.2/inputs/f2-seed-integration-baseline.sql
   ```

   Require **PASS new qualification fixture: QUAL: prefix and retained
   QUAL:Hello World greeting**. Inspect the printed greeting fields and config
   row: the prefix is **QUAL:**, and the default entry ID still selects Hello.
   This fixture refuses existing history or a nonempty prefix.

4. Check the supported data precondition before changing the application:

   ```sql
   select count(*) as incompatible_hello_rows
     from hello_entries where not regexp_like(entry_text,'[^[:space:]]');
   ```

   Require **0**. Whitespace-only legacy entries would violate the new constraint;
   stop for a data/contract decision rather than silently rewriting them.

5. Capture every current business field into a native SQLcl CLOB bind variable:

   ```sql
   @../../../../progress/E.2/inputs/f2-capture-business.sql
   ```

   Require **PASS captured all business fields before deployment in E1_INTEGRATION**.
   This captures all columns of greetings, entries and both configuration tables.
   Component versions are checked separately because Hello must change.
   Keep this SQLcl session connected through steps 6–7; do not recapture the
   baseline after deployment or create greetings before comparing it.

6. Deploy the **same patch archive** used for the fresh test:

   ```sql
   set define on
   define DEFAULTS_FILE=utils/properties/integration.properties
   project deploy -file artifact/e2-1.0.1-execution-r2.zip
   ```

   Require **Operation completed successfully**, **Run: 4 / Previously run: 22**.
   The four executions are the changed APEX import (`runOnChange`), new Hello
   constraint, corrected Hello trigger and explicit installed-version update.
   Initial data is not rerun. The original APEX changeset runs again, so it is
   not counted among the 22 skipped executions.

7. Compare every business field before any browser write:

   ```sql
   @../../../../progress/E.2/inputs/f2-check-business.sql
   ```

   Require **PASS exact business fields unchanged by deployment in E1_INTEGRATION**.
   This uses Oracle `JSON_EQUAL` over all captured rows/columns, in primary-key
   order. It checks exact equality, so run it before adding post-upgrade examples.
   These SQL assertions are project-authored checks using native database
   capabilities; PROJECT does not perform this business comparison automatically.

8. Verify new behavior and installed versions:

   ```sql
   @../../../../progress/E.2/inputs/f2-verify-hello.sql
   ```

   Require both behavior PASS messages and **Foundation 1.0.0 / Hello 1.0.1 /
   World 1.0.0**. The verification inserts roll back.

9. Repeat **F.2.3 steps 6–8** on **integration application 810004**: explicitly
   set restricted verification, sign in as VERIFIER, check a new greeting/history,
   require LAB_USER denial, and publish. This time, expected greeting text is
   **QUAL:Hello World**, because the retained prefix must survive. Earlier saved
   greeting fields remain unchanged. After publication, LAB_USER must also create
   **QUAL:Hello World**. Both supported qualification starting states have now passed.

#### F.2.5. Promote the identical qualified archive to retained UAT

**Purpose:** upgrade UAT with the artifact exercised in both integration starts.
Keep UAT's `UAT:` configuration and all existing business rows.

1. In **Terminal 2**, compare the archive with the hash recorded before
   qualification. This checks identity without replacing the recorded hash:

   ```bash
   python3 -c 'from pathlib import Path; import hashlib; p=Path(".local-apex/e2/project-walkthrough/component-repo-f2/artifact/e2-1.0.1-execution-r2.zip"); h=hashlib.sha256(p.read_bytes()).hexdigest(); assert h==p.with_suffix(".sha256").read_text().strip(), "STOP: candidate bytes changed"; print("PASS identical qualified candidate",h)'
   ```

   Require **PASS identical qualified candidate**. Keep this archive for UAT;
   no recapture or rebuild occurs between qualification and promotion.

2. In **Terminal 1**, select UAT and inspect the starting components:

   ```sql
   connect -name user_acceptance_test
   show user
   select component, installed, version from lab_components order by component;
   ```

   Require **E1_UAT**, with Foundation, Hello and World installed at **1.0.0**.
   If Hello is already **1.0.1** from a completed execution, retain UAT and
   continue at F.2.7 for a repeat; do not reset UAT to replay an initial upgrade.

3. Inspect the retained configuration and supported data precondition:

   ```sql
   select config_id, prefix, default_entry_id from hello_config;
   select count(*) as incompatible_hello_rows
     from hello_entries where not regexp_like(entry_text,'[^[:space:]]');
   ```

   Require prefix **UAT:**, the existing default ID, and **0** incompatible rows.
   Keep existing settings unchanged. Use the next snapshot to compare every
   field, rather than assuming a fixed history-row count.

4. Capture the complete current UAT business state before deployment:

   ```sql
   @../../../../progress/E.2/inputs/f2-capture-business.sql
   ```

   Require **PASS captured all business fields before deployment in E1_UAT**.
   Stay in this same connected SQLcl session through steps 5–6. This captures
   even greetings added after E.6's durable baseline.

5. Select the **UAT** mapping packaged in the identical archive and deploy:

   ```sql
   set define on
   define DEFAULTS_FILE=utils/properties/uat.properties
   project deploy -file artifact/e2-1.0.1-execution-r2.zip
   ```

   Require **Run: 4 / Previously run: 22** and **Operation completed successfully**.
   The packaged mapping selects **E1_UAT / application 810005 / alias E2-UAT**.
   No integration application ID is reused here.

6. Compare the retained UAT business fields immediately, before browser writes:

   ```sql
   @../../../../progress/E.2/inputs/f2-check-business.sql
   ```

   Require **PASS exact business fields unchanged by deployment in E1_UAT**.
   If it fails, stop for inspection; do not overwrite either baseline to obtain a pass.

7. Verify the installed correction and mapped application:

   ```sql
   @../../../../progress/E.2/inputs/f2-verify-hello.sql
   select application_id, owner, availability_status
     from apex_applications where application_id=810005;
   ```

   Require the two behavior PASS messages, **Foundation 1.0.0 / Hello 1.0.1 /
   World 1.0.0**, and **810005 / E1_UAT / Restricted Access**.

#### F.2.6. Verify and publish the upgraded UAT application

1. In **Terminal 1**, explicitly configure the UAT verification account/message:

   ```sql
   begin
     if user<>'E1_UAT' then raise_application_error(-20870,'Wrong target'); end if;
     apex_util.set_workspace('E1_UAT');
     apex_application_admin.set_application_status(
       810005, apex_application_admin.c_app_restricted_access,
       p_allowed_users_list=>apex_t_varchar2('VERIFIER'),
       p_message=>'Hello patch verification in progress.');
     commit;
   end;
   /
   ```

   Require **PL/SQL procedure successfully completed**.

2. Open the [UAT URL / application 810005](http://127.0.0.1:8080/ords/f?p=810005:1).

   1. Reload after import. Sign out of any current account; sign in as
      **VERIFIER** using the Markdown login card.

   2. Require Home's **Hello World - Working Copy** heading and footer **1.0.1**.

   3. Open **Installed components**. Require **Foundation 1.0.0 / Hello 1.0.1 /
      World 1.0.0**; this page identifies the component versions separately from
      the APEX assembly version in the footer.

   4. Open **Hello configuration**. Require the existing **UAT:** prefix and
      **Hello** default; leave them unchanged.

   5. Open **Home → Create greeting**. Require
      **UAT:Hello World — saved to history.**

   6. Open **Greeting history**. Find the new VERIFIER row and inspect earlier
      rows separately. Earlier **Hello World** and **UAT:Hello World** snapshots
      retain their original prefixes, text, actor and timestamps.

   7. Use **VERIFIER → Sign Out**, then log in as **LAB_USER** at the same UAT
      URL. Require **Hello patch verification in progress.**

3. In **Terminal 1**, publish UAT through the native API:

   ```sql
   begin
     if user<>'E1_UAT' then raise_application_error(-20870,'Wrong target'); end if;
     apex_util.set_workspace('E1_UAT');
     apex_application_admin.set_application_status(810005,apex_application_admin.c_app_available);
     commit;
   end;
   /
   ```

   Require **PL/SQL procedure successfully completed**. This command sets
   application availability; it is not a PROJECT qualification receipt.

4. Refresh the blocked UAT page as **LAB_USER**. If login is requested, use
   LAB_USER again. Require Home, create another **UAT:Hello World** greeting,
   then find the new LAB_USER row in **Greeting history**. Earlier history stays intact.

5. In **Terminal 2**, check E.6's original durable baseline against the upgraded
   UAT. This existing read-only comparator permits the new greeting rows while
   requiring every earlier recorded business field to remain unchanged:

   ```bash
   python3 scripts/cicd-project-promote.py check-baseline
   ```

   Require **PASS every prior business field preserved; new rows/columns are permitted**.
   Deployment and publication above were native SQLcl/APEX operations; this
   existing prototype supplies the separate durable business-preservation check.

#### F.2.7. Repeat the patch without rebuilding or resetting UAT

**Purpose:** assess a repeat of the completed patch deployment. As in E.6, this
is an additional repeatability observation, not recovery from partial failure.

1. In **Terminal 1**, connect to UAT and capture its current state, including
   the new verification greetings. These commands start a new same-session comparison:

   ```sql
   connect -name user_acceptance_test
   @../../../../progress/E.2/inputs/f2-capture-business.sql
   ```

   Require **PASS captured all business fields before deployment in E1_UAT**.

2. Deploy the exact same archive again:

   ```sql
   set define on
   define DEFAULTS_FILE=utils/properties/uat.properties
   project deploy -file artifact/e2-1.0.1-execution-r2.zip
   ```

   Require **Run: 0 / Previously run: 26**, **Operation completed successfully**.
   All changesets are already applied; APEX should remain **Available**.

3. Check the business state and availability:

   ```sql
   @../../../../progress/E.2/inputs/f2-check-business.sql
   select application_id, owner, availability_status
     from apex_applications where application_id=810005;
   ```

   Require **PASS exact business fields unchanged by deployment in E1_UAT** and
   **810005 / E1_UAT / Available**. No new restriction/publication cycle is needed
   for this successful repeat.

**Completion:** both integration starts passed; the same patch bytes upgraded
UAT to **Foundation 1.0.0 / Hello 1.0.1 / World 1.0.0**; existing UAT settings
and history survived; ordinary-user behavior passed after publication. Keep the
original E.6 baseline and both immutable archives. Record your observed results
before continuing to G, which remains separate work.

**Evidence boundary:** preparation evidence records the reference candidate's
fresh/populated integration qualification. The Product Owner reported the complete
F journey completed on 2026-10-20, including the operator-built candidate's UAT
upgrade and repeat. This report is distinct from independently captured execution
transcripts. The unresolved native verification finding continues to prevent a
clean formal release verdict.

## G. Component version dependency protection — not supported by native tools

### G.1. Gap finding

**Native support: not supported in the evaluated APEX/SQLcl PROJECT workflow.**

**APEX does not natively enforce version dependencies between the application
components defined in E.1. It does not automatically block an incompatible
Foundation upgrade.**

For example, Hello **1.0.1** requires Foundation **1.0.0**. APEX does not interpret
that requirement and reject proposed Foundation **2.0.0**. SQLcl PROJECT also
does not enforce our component dependency declaration.

APEX shared-component subscriptions support reuse and propagation, but do not
provide this application-component version protection.

### G.2. Evidence and comparison with E.1

- Native PROJECT verification passed both supported and conflicting declarations
  in the corrected SQLcl 25.4.1 comparison.
- E.1's explicit compatibility validator rejected the conflicting declaration.
  That rejection was custom project logic, not native APEX or PROJECT behavior.
- No breaking Foundation upgrade was deployed. The existing UAT application,
  installed versions and business data remained unchanged.

The [supporting experiments](g-component-dependency-evidence.md) retain commands,
client qualification and evidence links. **No additional command execution is
required in this chapter.**

### G.3. Consequence for the toolchain

E.1 supplies component dependency protection that the evaluated native approach
lacks. Retain an explicit component contract and plan how its compatibility rules
will be enforced during delivery. The enforcement mechanism is follow-up work;
E.2 does not need to implement another deployment controller to establish this gap.

Reconcile follow-up with existing **PBI-021/038/045** and **PBI-052**. Complex
Foundation upgrades remain assigned to **E.5**.

Continue to H for the separate drift-protection assessment.

## H. Automatic live-drift deployment protection — not supported by native tools

**Native support: not supported as an automatic deployment gate in the evaluated
APEX/SQLcl PROJECT workflow.** The retained experiment does not establish a
product-wide absence of drift-comparison capabilities.

**Required outcome:** before deployment, automatically detect unexpected changes
in the target's APEX application, database schema and stored code against its
last accepted deployment baseline; stop deployment and report the differences.

**Finding:** the evaluated native APEX/SQLcl PROJECT workflow has not demonstrated
this protection. E.2 cannot claim equivalence to E.1's explicit drift gate.

Native exports provide material for comparison. A manual file diff is not a
deployment gate. The earlier artifact replay ran no pending import and therefore
did not test protection against overwriting drift. Business-data preservation
checks do not test application/schema drift either.

**Decision:** retain this as a gap in the evaluated delivery approach. Qualify a
native capability or provide a supplementary automated pre-deployment check under
existing PBI-023/PBI-045. Any supplementary implementation must be identified as
project logic, with its baseline, scope and rejection behavior defined.

**No operator exercise is required in H.** The [supporting evidence](h-live-drift-evidence.md)
records the limited experiments; they do not establish automatic drift protection.

## I. Automatic failed-deployment repair — not supported by native tools

**Automatic diagnosis and repair of a partially failed deployment: not supported
by the evaluated PROJECT workflow.** A developer must inspect the partial state
and prepare a reviewed repair.

SQLcl/Liquibase supports delivering that reviewed repair through changesets;
this is not automatic repair. E.2 has not exercised this supported manual
forward-repair path. No operator exercise is supplied here.

## Compare the approaches

1. Evaluate native PROJECT/APEX/Git behavior against the shared scenario's
   outcomes. Identify any supplementary mechanism separately, with the evidence
   that makes it necessary.
2. Keep the Working Copy team checkpoint with F's authoring/capture steps.
3. Review the [gap analysis and dependency-ordered roadmap](oracle-gap-analysis.md).
4. Keep complex Foundation upgrades in E.5.

The Oracle-based checks, exact input paths, bounded recovery and expected output
must be completed and rehearsed before the corresponding chapters are executable.
Native PROJECT dependency/SemVer inference is a validation question, not an
assumption in either direction.

## Completion criteria

- The operator executes SQLcl commands directly, with prepared connections and inputs.
- Foundation, Hello, World and the compatible upgrade produce understandable application results.
- Working Copies require only small authoring edits.
- Source, native migrations, artifacts, mappings and external controls are distinguishable.
- A fresh delivery and populated upgrade use qualified, identified artifacts.
- Settings/history preservation and selected rejection paths are actually observed.
- Every chapter has exact inputs, expected output and a verified continuation path.

## Maintain alignment with E.1

Keep A–I names, actor goals, component versions, application results and
protection/preservation criteria aligned with the corresponding E.1 chapters.
E.2 changes the evaluated capture/delivery tools and adds Working Copy authoring;
it must not replace the business journey with a smaller unrelated fixture.

Check both walkthroughs when changing either journey. Update E.2's commands,
prepared inputs and implementation evidence together; leave E.1's historical
artifacts intact. Preloaded development state, captured source, generated
migrations, qualified artifacts and target deployment are distinct outcomes.
Never report an unexecuted later outcome as complete because an earlier one passed.
