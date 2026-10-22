# Component dependency assessment — supporting evidence

The [operator walkthrough](cicd-walkthrough.md) states the gap finding in G.
This document contains the detailed experiments, native verification qualification
and custom-rule comparison. They support the finding; they are not required
operator steps for continuing the walkthrough.

## G. Assess native component dependency protection

**Gap: APEX does not natively support version dependencies between the
application components defined in E.1.** It does not enforce a declaration such
as “Hello 1.0.1 requires Foundation 1.0.0” or automatically block an incompatible
Foundation upgrade. SQLcl PROJECT verification also does not enforce this contract.

APEX shared-component subscriptions support reuse and propagation; they do not
provide this component-version dependency protection. E.1's explicit compatibility
check supplies a capability that the evaluated native workflow does not supply.
This is a gap identified by E.2, not a requirement to build a replacement during
the gap analysis. Placement of any supplementary enforcement is follow-up work.

**Purpose:** assess whether Oracle's native approach provides the dependency
protection exercised in E.1. The outcome is the explicit gap above. The scenario
proposes Foundation **2.0.0** while Hello **1.0.1** and World **1.0.0** still
require Foundation **1.0.0**.

The procedures below are supporting experiments. G.2 qualifies PROJECT's
verification behavior; G.3 demonstrates the retained custom rule. Neither is
native APEX component dependency protection. Repeating those experiments is not
needed merely to restate the finding. No additional deployment mechanism is
implemented by this chapter.

The proposal is **metadata only**. No Foundation 2.0.0 code, migration or archive
is created or deployed. Complex Foundation upgrades remain in E.5. The artifact
retained from F stays unchanged. This exercise establishes a dependency-admission
boundary; it does not test rollback of a breaking database migration.

The supplementary gate is project-authored. It reuses
`scripts/cicd-compatibility.py`; it does not implement another dependency rule.
The small G helper binds the artifact, source revision/worktree, declarations,
validator and exact target state before the deployment dispatch point. Native
SQLcl commands remain visible below. No manual file edits are required.

### G.1. Establish the supported state and proposed conflict

1. In **Terminal 2 (regular shell)**, prepare the assessment. `prepare` reads
   UAT, creates a separate Git comparison clone and two declaration files, and
   records the baseline. On repeat it verifies the existing baseline instead of
   replacing it:

   ```bash
   cd /Users/rstyczynski/projects/APEX_CICD
   python3 scripts/cicd-project-incompatible.py prepare
   ```

   First execution requires:

   ```text
   PASS supported Hello 1.0.1 declaration; existing compatibility validator reused
   PASS immutable artifact, source revision, declarations, validator and UAT baseline bound
   NEXT native PROJECT comparison in component-repo-g; no UAT deployment has run
   ```

   A prepared lab instead prints **PASS existing G preparation retained; exact
   artifact/source/target baseline still matches**. Both results continue at step 2.
   A **BLOCKED** result requires diagnosis; do not delete or recapture the baseline.

2. Stay in **Terminal 2**. Inspect the two declarations in VS Code:

   ```bash
   code .local-apex/e2/project-walkthrough/g-evidence/allowed.json
   code .local-apex/e2/project-walkthrough/g-evidence/incompatible.json
   code scripts/cicd-compatibility.py
   code scripts/cicd-project-incompatible.py
   ```

   The supported components are **Foundation 1.0.0 / Hello 1.0.1 / World 1.0.0**.
   Only the proposed Foundation component becomes **2.0.0** in the incompatible
   declaration. Both consumer dependencies still specify Foundation **1.0.0**.
   These files are supplied automatically; do not edit them.

3. Stay in **Terminal 2**. Run the existing validator against the supported
   declaration as a positive control:

   ```bash
   python3 scripts/cicd-compatibility.py .local-apex/e2/project-walkthrough/g-evidence/allowed.json
   ```

   Require **PASS explicit component dependencies and supported version triple**.
   This is the project's rule, not a native PROJECT result.

### G.2. Qualify native verification, then compare declarations

**Client:** this chapter uses the supplied **SQLcl 25.4.1.022.0618**, installed
alongside 25.3 using the [pinned client procedure](inputs/sqlcl-25.4.1-client.md).
Its connection store is a separate copy. The completed F repository,
archives and UAT are unchanged. SQLcl 25.3's completeness check incorrectly
expects all exported SQL sources in the current branch's stage changelog; newer
verification handles frozen releases and the separate APEX changelog.

**Comparison scope:** regenerate only the separate G comparison clone from the
current author. Preserve source/distribution consistency: do not apply F's
post-stage APEX substitutions to this clone. This makes the dependency comparison
start from a clean native project. It does not rebuild, deploy or retrospectively
certify the F archive. The clone retains Main's authoring settings and is not a
replacement deployment candidate.

1. In **Terminal 2 (regular shell)**, select the supported declaration and check
   the supplied replacement client. The explicit Java path avoids selecting a
   different Java installation from PATH:

   ```bash
   cd /Users/rstyczynski/projects/APEX_CICD
   cp .local-apex/e2/project-walkthrough/g-evidence/allowed.json .local-apex/e2/project-walkthrough/component-repo-g/dist/component-contract.json
   JAVA_HOME="$PWD/.local-apex/tools/jdk-21.0.12.1+1/Contents/Home" \
     .local-apex/tools/sqlcl-25.4.1.022.0618/sqlcl/bin/sql -version
   ```

   Require **Release 25.4.1.0 / Build 25.4.1.022.0618**. The download is pinned
   to the [official Oracle release](https://www.oracle.com/tools/sqlcl/sqlcl-downloads.html);
   its ZIP SHA1 was checked against **1ce64ff5778c0fb739f7d9724eebfcc9c1aacfeb**.

2. Switch to **Terminal 1**. At the old `SQL>` prompt, run:

   ```sql
   exit
   ```

   Terminal 1 is now a **regular shell**. Launch the supplied client directly
   in the G comparison clone:

   ```bash
   cd /Users/rstyczynski/projects/APEX_CICD
   E2_PROJECT_ROOT="$PWD"
   cd "$E2_PROJECT_ROOT/.local-apex/e2/project-walkthrough/component-repo-g" &&
   JAVA_HOME="$E2_PROJECT_ROOT/.local-apex/tools/jdk-21.0.12.1+1/Contents/Home" \
     "$E2_PROJECT_ROOT/.local-apex/tools/sqlcl-25.4.1.022.0618/sqlcl/bin/sql" \
     -home "$E2_PROJECT_ROOT/.local-apex/tools/sqlcl-home-25.4.1-qualification" /nolog
   ```

   Wait for the new **SQLcl 25.4.1 / SQL>** prompt. Continue here for the SQL
   steps below. Do not run them in the old 25.3 session.

3. Stay in **Terminal 1 (SQLcl)**. Configure this clone for the new client and
   capture the author using current APEX identities:

   ```sql
   pwd
   connect -name lab-dev-c
   show user
   project config set -name sqlcl.version -value 25.4.1.0
   project config set -name sqlcl.autoConnect -value false
   project config set -name export.apex.expOriginalIds -value false
   project export -list
   project export
   ```

   Require **component-repo-g / E1_DEV_C**, only **application_id=810003** in
   the APEX selection, and **Exported 22 objects**. The last setting exports
   current application/schema identities: **810003 / E1_DEV_C**, rather than
   the inherited **810001 / E1_DEV_A** identities. It changes exported identifiers,
   not the live author application. Working Copies remain excluded by the filter.
   The configuration operations and export can be repeated safely in this clone.

4. Switch to **Terminal 2**. Review and commit the configuration and source
   capture before staging. The conditional commit permits a repeated capture
   that matches the retained source exactly:

   ```bash
   git -C .local-apex/e2/project-walkthrough/component-repo-g diff -- .dbtools/project.config.json src
   git -C .local-apex/e2/project-walkthrough/component-repo-g add .dbtools/project.config.json src
   if ! git -C .local-apex/e2/project-walkthrough/component-repo-g diff --cached --quiet; then
     git -C .local-apex/e2/project-walkthrough/component-repo-g commit -m "Qualify SQLcl 25.4.1 and current APEX identities for G"
   fi
   ```

   Require only the reviewed configuration and native APEX identity/source
   changes in this capture. No database migration is executed.

5. Switch to **Terminal 1 (SQLcl)**. Regenerate the comparison distribution
   from that committed source, then record native verification:

   ```sql
   project stage -branch-name e2-world -verbose
   spool ../g-evidence/native-25.4.1-allowed.txt
   project verify -compared-branch-name e2-world -verbose
   spool off
   ```

   Require **Errors: 0 / Warnings: 0 / Info: 15**. Both
   **stagechangelogcomplete** and **apexinsrcmatchesdist** must report no issues.
   Stop on any error. The earlier completeness error is not an accepted result
   in this corrected procedure. Do not manually modify the generated APEX SQL.

6. Switch to **Terminal 2**. Replace only the comparison clone's declaration
   with the supplied incompatible proposal:

   ```bash
   cp .local-apex/e2/project-walkthrough/g-evidence/incompatible.json .local-apex/e2/project-walkthrough/component-repo-g/dist/component-contract.json
   git -C .local-apex/e2/project-walkthrough/component-repo-g diff -- dist/component-contract.json
   ```

   Require only Foundation's declared version to change **1.0.0 → 2.0.0**.
   Do not stage, package or deploy this proposal.

7. Switch to **Terminal 1 (SQLcl)**. Repeat the same native verification:

   ```sql
   spool ../g-evidence/native-25.4.1-incompatible.txt
   project verify -compared-branch-name e2-world -verbose
   spool off
   ```

   Require **Errors: 0 / Warnings: 0 / Info: 15**, with no Foundation/consumer
   dependency diagnostic. Now both comparisons have a clean structural baseline:
   the test establishes that native verification does not interpret our explicit
   JSON dependency contract. It does not establish that custom Oracle/Liquibase
   checks are impossible. [SQLcl 25.4 PROJECT reference](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.4/sqcug/project.html).

### G.3. Reject before the deployment dispatch point

1. Switch to **Terminal 2**. Submit the bound incompatible proposal to the
   supplementary gate. `reject` first checks artifact/source/declaration identity
   and the retained live UAT baseline. It then invokes the existing compatibility
   validator before the native deployment call. Rejection must leave that call
   unexecuted:

   ```bash
   python3 scripts/cicd-project-incompatible.py reject
   ```

   Require these exact results:

   ```text
   REJECTED INCOMPATIBLE: Hello requires Foundation 1.0.0; proposed Foundation 2.0.0
   PASS PROJECT deploy invocations: 0
   PASS UAT business rows, installed versions, migration history, schema DDL and APEX export unchanged
   ```

   The helper treats this expected rejection as a successful exercise. A missing
   receipt, changed binding or unexpected rejection is **BLOCKED**, not a pass.
   The target snapshot uses read-only SQL, native DBMS_METADATA and an APEX export
   without export date. It compares business rows, installed state, changeset
   history, schema definitions, application definition and availability.

2. Stay in **Terminal 2**. Inspect the resulting receipt:

   ```bash
   code .local-apex/e2/project-walkthrough/g-evidence/rejection.json
   ```

   Require **result = REJECTED**, **deploy_invocations = 0** and
   **target_unchanged = true**. The receipt identifies the bound F artifact and
   source, proposed declaration and target. No version row is edited to force a
   pass. The proposed metadata is not represented as a packaged Foundation 2.0.0
   implementation.

### G.4. Inspect the retained application and check again

1. Switch to **Terminal 1 (SQLcl)**. Return to the F repository, connect to UAT,
   and inspect the retained installed versions:

   ```sql
   cd ../component-repo-f2
   pwd
   connect -name user_acceptance_test
   show user
   select component, installed, version from lab_components order by component;
   select application_id, availability_status from apex_applications
     where application_id=810005;
   ```

   Require **component-repo-f2 / E1_UAT**, components **1.0.0 / 1.0.1 / 1.0.0**
   and application **810005 / Available**. Foundation must remain **1.0.0**.

2. Stay in **Terminal 1**. Read the preserved configuration and greetings:

   ```sql
   select * from hello_config;
   select greeting_id, greeting_text, actor from greeting_history order by greeting_id;
   ```

   Require the existing **UAT:** prefix and retained greeting rows. Read these
   values; do not add or edit records during this unchanged-state exercise.

3. Switch to **Terminal 2** and open the existing login card:

   ```bash
   code .local-apex/e2/project-walkthrough/access.md
   ```

4. In the **browser**, open the UAT URL:
   [UAT Home](http://127.0.0.1:8080/ords/f?p=810005:1).
   1. If another account is signed in, open its account menu and choose **Sign Out**.
   2. Sign in as **LAB_USER** with the UAT password on the login card.
   3. Require the working Home page with **Hello World - Working Copy** and
      assembly version **1.0.1**.
   4. Open **Greeting history**. Require the previously saved greetings.
   5. Open **Installed components**. Require Foundation **1.0.0**, Hello
      **1.0.1**, World **1.0.0**.
   6. Do not create a greeting or edit settings; this chapter checks preservation.

5. Return to **Terminal 2**. `check` verifies the retained rejection receipt,
   artifact/source bindings and exact live target snapshot again after inspection:

   ```bash
   python3 scripts/cicd-project-incompatible.py check
   ```

   Require:

   ```text
   PASS retained rejection receipt; PROJECT deploy invocations: 0
   PASS exact UAT baseline unchanged; application remains Available
   ```

**Completion:** the supported declaration passes the existing rule; the conflicting
proposal is rejected before native deployment; UAT remains unchanged and usable.
Native verification and supplementary dependency admission are recorded separately.
The native comparison project passes structural verification, but this does not
retroactively qualify the preserved F archive as a formal release. It is not a
Foundation upgrade implementation or automatic dependency enforcement by PROJECT.
H remains a separate chapter.
