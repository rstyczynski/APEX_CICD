# E.4 — Multi-developer release and central DEV walkthrough

## Goal, starting state and delivery boundary

This walkthrough demonstrates three independent author contributions, selection of
A/C through a later announced release branch, preservation of B, a native numbered
artifact, and deliberate central DEV synchronization. It accompanies
[sprint_E.4_increment_demo.pptx](sprint_E.4_increment_demo.pptx),
[the operating manual](user_manual.md), [the implementation record](sprint_E.4_implementation.md)
and [test evidence](sprint_E.4_tests.md). Requirements belong to the
[SRS](../../docs/srs.md); the accepted experiment and counter-only recovery rule
belong to [the design](sprint_E.4_design.md).

The actual starting state for a handover today is **already delivered 1.0.7**:
central DEV 810203 is Available, A/C are installed, B remains on e4-b, temporary
central developer/proxy identities have been removed. Do not run the old sequence
blindly over that state. The numbered stages below provide a runnable inspection
route through the completed journey. Each native operation is also shown with its
complete helper SQL and the prerequisites for a newly authorized replay. The
original native sequence was executed on 2026-11-09; it is not a new live replay
merely because these evidence checks pass. A live Product Owner demonstration and
acceptance are still required.

One Codex operator simulated A/B/C and the Release Manager. Page Designer edits
were made separately; independent native capture/stage processes genuinely overlapped.
This is a prepared-host experiment, not clean-host provisioning, a three-human study,
production fencing, or arbitrary first installation. The inherited static runtime
footer remains 1.0.0; use the tagged source/archive/receipt for release identity.

## 1. Open the package and preflight — slides 1–6

Use Bash on the prepared macOS host. Git, gh, jq, unzip, Node.js, actionlint and the
VS Code `code` command must be on PATH; gh must authenticate to the existing lab.
Oracle/APEX/ORDS and the fixed author services are already prepared. Nothing in this
walkthrough creates or deletes the retained database. Do not clean .local-apex:
its narrowly excepted e1-secrets.json record remains a dependency.

Run from any directory inside the operator repository, in one named Terminal
session **E4 operator**:

```bash
ROOT=$(git rev-parse --show-toplevel)
cd "$ROOT"
E4="$ROOT/progress/E.4"
LAB="$ROOT/.local-apex/e4/lab"
REPO=rstyczynski/APEX_CICD_E3_LAB
SQLCL="$ROOT/.local-apex/tools/sqlcl-25.4.1.022.0618/sqlcl/bin/sql"
export JAVA_HOME="$ROOT/.local-apex/tools/jdk-21.0.12.1+1/Contents/Home"
"$SQLCL" -version
jq -r .sqlcl.version "$LAB/.dbtools/project.config.json"
git -C "$LAB" status --short
git -C "$LAB" rev-parse v1.0.7^{commit}
code "$E4"
```

Expect SQLcl release 25.4.1.0/build 25.4.1.022.0618, matching project metadata,
a clean application checkout and tag commit e0f60ff5efc6905c3b6a4c0e7a7a79a6b0134b0c.
If the cache is absent, stage the pinned vendor SQLcl ZIP from the declared URL and
SHA in [the existing setup action](../../examples/git-pipeline/.github/actions/setup-native/action.yml),
with Java 21, before continuing. A different SQLcl or missing qualified build stops
native processing before source/distribution/target writes. Do not change metadata
to make a newer executable pass. This is SM-1 / NFR-5.

A future native replay also requires approved author credentials and separate native
SQLcl homes outside checkout scratch. In each author's private home save the same
logical alias `lab-dev-c` pointing respectively to E4A/E4B/E4C, effective USER
E1_DEV_C. Native `connect -save lab-dev-c -savepwd` prompts/inputs belong in a private
terminal, never Git/logged shell commands. Set AUTHOR_HOME_A/B/C from those stores.
A central replay needs separate approved `e3-target` access to E3_TARGET and a newly
reserved no-user/no-author interval. The temporary E4_VERIFY/E4_SYNC used in the
recorded run no longer exists. No example assumes those removed identities still work.

## 2. Inspect independent authors and their edits — slides 7–10

The three author services contain independent copies of the accepted definitions,
not retained runtime data. They share schema/workspace/application identities to
preserve native source paths; E4I is used only later for integration.

```bash
jq . "$E4/tests/parallel-contributions.json"
code "$E4/tests/author-a-source.diff"
code "$E4/tests/author-b-source.diff"
code "$E4/tests/author-c-source.diff"
```

All authors started at 5a7655ffd3e6be92bcd88e9581612be17dc3059c. A's Home header is
`E4 A: Select Hello and World values, then record the greeting.` B's page-100 region
Name is `Hello entries - deferred B`. C's page-200 region Name is
`World entries - selected C`. Only each author's own edit appears in its original
source diff. PBI-060/IT-1 requires this independence before release admission.

For a newly authorized authoring replay, open `/ords/e4a/apex`, `/ords/e4b/apex` and
`/ords/e4c/apex` at http://127.0.0.1:8080, sign into workspace E1_DEV_C with that
fixture's approved developer credentials, and select app 810003. In A select page
1 and **Header Text**; in B select page 100 then report region **Hello entries** and
**Name**; in C select page 200 then **World entries** and **Name**. Save and require
**Changes saved**. The current fixtures already retain those edits; inspect first.
Do not re-save an unchanged property as evidence of new work. Native keyboard input
must trigger the Page Designer model; a DOM-only value assignment proved insufficient
in the first attempt. The archived screenshots show the corrected saved result.

## 3. Capture, commit, independently stage and verify — slides 11–13

### What the capture helper does

It connects through the private alias, prints effective user/service, enumerates
export objects, and runs native PROJECT export. It does not merge branches or
select a release. The checked-out Git state must match its SQLcl version.

```sql
-- Run only after the shell toolchain and fixture identity checks.
-- &1: private native connection alias for this independent author fixture.
set echo off verify off define on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name &1
select user, sys_context('USERENV','SERVICE_NAME') service_name from dual;
project export -list
project export
exit success
```

In a new replay checkout based on the recorded developer start, the native command
is the following (repeat in separate author terminals/homes, after fixture identity
preflight). The recorded execution ran all three processes concurrently, not one
shared fixture repeatedly reset between authors.

```bash
cd "$ROOT/.local-apex/e4/a"
"$SQLCL" -nohistory -noupdates -home "$AUTHOR_HOME_A" -S -L /nolog   @"$E4/sql/capture.sql" lab-dev-c
```

Review the actual src diff and commit source before staging. In each new author
checkout, the concrete commit sequence is `git diff -- src`, then `git add src`
and `git commit -m "feat: capture selected author change"`. The current fixtures
and branches are already at their recorded heads: these are historical write steps,
not part of today's inspection route. The original captured
and staged SHAs are in parallel-contributions.json. Do not recommit unchanged
existing branches as a new contribution. For current handover inspection:

```bash
git -C "$LAB" show --stat e14d8b1dcc4a50ebd0a26a3ce298923bb217adc6
git -C "$LAB" show --stat 39a620024598dbb98538ab68c1b786c840c5ed27
git -C "$LAB" show --stat aaf52fa6fdf1833b7f0cd695b52a66c4666e86bd
```

### What native staging and verification do

`stage` compares committed source with the immutable comparison branch and generates
distribution metadata. It does not choose which developers enter a release. `verify`
checks the current source/snapshot/distribution against that same comparison. Native
SQLcl may exit zero despite reporting verification errors, so inspect **Errors: 0**
and explain warnings; exit code alone is insufficient.

```sql
-- &1: author connection; &2: immutable comparison branch in this checkout.
set echo off verify off define on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name &1
project stage -branch-name &2
exit success
```

```sql
-- &1: author connection; &2: reviewed comparison branch for this Git state.
set echo off verify off define on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name &1
project verify -cbn &2 -verbose
exit success
```

The per-author commands used the alias and local e4-base at the recorded start:

```bash
"$SQLCL" -nohistory -noupdates -home "$AUTHOR_HOME_A" -S -L /nolog   @"$E4/sql/stage.sql" lab-dev-c e4-base
"$SQLCL" -nohistory -noupdates -home "$AUTHOR_HOME_A" -S -L /nolog   @"$E4/sql/verify.sql" lab-dev-c e4-base
```

Review and commit generated dist only after zero-error verification: `git diff -- dist`,
`git add dist`, then `git commit -m "chore: stage native author change"`. In the recorded
run each passed with one APEX-only no-soft-object ordering warning. Inspect process
receipts and logs (they establish overlapping native processes, not three humans):

```bash
code "$E4/tests/author-a-stage-verify.log"
code "$E4/tests/author-b-stage-verify.log"
code "$E4/tests/author-c-stage-verify.log"
jq . "$E4/tests/author-a-capture.log.process.json"
```

## 4. Announce a later release; opt in and admit separately — slides 14–16

The manager accepted harmless context PR #7 after author work began. Current main
was a018a677653935200ff32eb9982f207a72bbd162 when release-e4-candidate was created.
Issue #8 announced that branch. A/C volunteered through PRs #9/#10; B postponed
without a release PR. Admission remained a separate manager decision after checks
and source/dependency review. The original commands have already produced these
remote objects; inspect them without recreating or retargeting them:

```bash
jq . "$E4/tests/release-branch.json"
gh issue view 8 --repo "$REPO"
gh pr view 9 --repo "$REPO"
gh pr view 10 --repo "$REPO"
gh api "repos/$REPO/git/ref/heads/e4-b" --jq .object.sha
```

B must still be ed9fe37bbebe30306ce91e981da9b5565b44c5c5. For a future release,
create a new unused branch from then-current accepted main, announce its actual
name, let developers choose to submit, then independently admit or defer each PR.
Do not force all authors to wait for one another's first merge or first stage.

## 5. Reconcile actual conflicts and preserve selected intent — slides 17–19

```bash
code "$E4/tests/candidate-conflict.log"
code "$E4/tests/integration-qualified-capture.log"
code "$E4/tests/integration-restage-verify.log"
git -C "$LAB" show --stat dedbe91
git -C "$LAB" show --stat 8485f8149f30e2add49b8f5501755b3d80a13842
```

The full application, snapshot XML and application YAML conflicted. Resolution
reconstructed A's full app plus C page 200 in E4I, captured through PROJECT,
retained admitted A distribution as the comparison, and freshly staged/verified C.
A mixed current-ID/original-ID import first failed an APEX foreign key; a zero-offset
trial changed the default offset. The qualified operation uses native original-ID
exports consistently and canonical offset 3270698107083768. Generated IDs/snapshots
were not hand-patched. Review the complete source: C adds only its region label to
admitted A. B must be absent from src and dist, not merely removed from an include.

The shared APEX installer is runOnChange `INSTALL_810003`. These APEX-only feature
stage files are empty; no artificial database dependency or independent per-feature
APEX installer is claimed. A later B delivery must update against the newly announced
release branch, preserve A/C, resolve/revalidate its combined source, submit a new
PR and use a later numbered release. Its original stage is provenance, not a promise
that old generated bytes will integrate unchanged.

## 6. Promote, freeze, commit and package — slides 20–22

PR #11 promoted the validated candidate into main; generated version PR #6 selected
1.0.7 after a separately dispatched PR check. Native release then froze next and
updated metadata. Its output was reviewed and committed before tagging/packaging.

### What release and package helpers do

`project release` mutates native distribution and lastReleaseVersion; it is not
packaging. `gen-artifact` packages the clean accepted frozen Git state. Never run
release again on the existing 1.0.7 tag, move that tag, or edit historical changesets.

```sql
set echo off verify off define on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
project release -version &1
exit success
```

```sql
set echo off verify off define on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
project gen-artifact -name e3 -version &1 -format zip
exit success
```

The equivalent complete native invocations for the recorded write sequence are
below. They are a historical recipe, excluded from today's read-only rehearsal.
Run release only on the reviewed pre-freeze state for a new unused version; after
reviewing its changes, commit before packaging. The helper files are in the operator
repository, while the working directory is the application repository:

```bash
cd "$LAB"
"$SQLCL" -nohistory -noupdates -home "$AUTHOR_HOME_A" -S -L /nolog \
  @"$ROOT/examples/git-pipeline/sql/release.sql" 1.0.7
git diff -- .dbtools dist
# Stop here for review of every generated change.
git add .dbtools/project.config.json dist
git commit -m "chore(release): freeze native SQLcl release 1.0.7"
"$SQLCL" -nohistory -noupdates -home "$AUTHOR_HOME_A" -S -L /nolog \
  @"$E4/sql/verify.sql" lab-dev-c e4-release-base
# Require zero native errors and a clean checkout before packaging.
"$SQLCL" -nohistory -noupdates -home "$AUTHOR_HOME_A" -S -L /nolog \
  @"$ROOT/examples/git-pipeline/sql/package.sql" 1.0.7
```

The current copyable inspection route verifies the actual frozen source and archive:

```bash
gh pr view 11 --repo "$REPO"
gh release view v1.0.7 --repo "$REPO"
git -C "$LAB" show --stat e0f60ff5efc6905c3b6a4c0e7a7a79a6b0134b0c
shasum -a 256 "$E4/tests/e3-1.0.7.zip"
unzip -Z1 "$E4/tests/e3-1.0.7.zip"
code "$E4/tests/release-artifact.json"
```

Expect SHA-256 27541bed6550c9f2dcfb36aeabd5e903bfe09a475fda0b0ec1972aa8ad9a1535.
The inherited later-main context, A/C source and shared APEX installer are included;
B is absent. 1.0.7's numbered changelog is empty because the app is carried by the
shared native APEX installer, which is included by main.changelog.xml. Native
release bookkeeping is still required and verified.

## 7. Qualify a trusted initial baseline — slides 23–25

An old installed source label is not proof that today's live definitions are clean.
Verify the retained accepted archive hash, natively reconstruct its mapped app in
an isolated reference fixture, export reference and target using original IDs and
no export date, and review the entire raw diff privately. Explain each exact
mapping/instance/counter field. Unknown labels, logic, ordering or metadata block
qualification. Never overwrite central DEV to make the comparison pass.

The pre-baseline controlled title edit was rejected while remaining saved; no
baseline or deployment was created. Only the fixture property was restored.
Complete raw exports and all-field business snapshots are private; the shared
receipts/diffs expose only reviewed metadata and decisions.

```bash
code "$E4/tests/initial-reconciliation.diff"
code "$E4/tests/it3a-refusal.json"
code "$E4/tests/trusted-initial-baseline.json"
```

### What the observation helper does

It verifies effective schema, sets workspace context, reports actual availability
and calls APEX_EXPORT.GET_APPLICATION with a fixed checksum profile. It does not
change app metadata or establish trust by itself. Obtain two identical readings
only after complete source reconciliation, then preserve that approved receipt
privately between attempts.

```sql
-- &1: connection; &2: expected schema; &3: workspace; &4: application.
-- Session context only; this script does not change application state.
set echo off verify off define on serveroutput on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name &1
set serveroutput on
declare
  files apex_t_export_files;
  status varchar2(100);
begin
  if user <> '&2' then raise_application_error(-20931,'Unexpected target'); end if;
  apex_util.set_workspace(p_workspace=>'&3');
  select availability_status into status from apex_applications where application_id=&4;
  files := apex_export.get_application(
    p_application_id=>&4, p_type=>'CHECKSUM-SH256',
    p_with_date=>false, p_with_original_ids=>true,
    p_with_ir_public_reports=>true, p_with_ir_private_reports=>false,
    p_with_ir_notifications=>false, p_with_translations=>false,
    p_with_comments=>false, p_with_supporting_objects=>'N',
    p_with_acl_assignments=>false, p_with_audit_info=>null);
  dbms_output.put_line('E4_STATUS='||status);
  dbms_output.put_line('E4_CHECKSUM='||dbms_lob.substr(files(1).contents,32767,1));
end;
/
exit success
```

For a separately authorized live check, TARGET_HOME must contain approved e3-target
access; it cannot be the removed temporary E.4 proxy profile:

```bash
cd "$LAB"
"$SQLCL" -nohistory -noupdates -home "$TARGET_HOME" -S -L /nolog   @"$E4/sql/observe.sql" e3-target E3_TARGET E3_TARGET 810203
```

## 8. Refuse stale source and preserve pending edits — slides 26–28

Before deployment the operator compares the selected accepted source/archive with
the request and compares live metadata with the trusted baseline. Main advancing
alone does not silently redefine the selected release. This is a manual decision
under participant exclusion, not an autonomous stale-worker guard.

```bash
code "$E4/tests/it2-refusal.json"
code "$E4/tests/it3b-refusal.json"
code "$E4/tests/postbaseline-restoration.diff"
code "$E4/tests/trusted-recovered-baseline.json"
```

The older 1.0.5 candidate was refused after selecting 1.0.7; no deploy ran and
checksum/data/receipt remained unchanged. The saved post-baseline Home title also
caused refusal; the edit, data and prior receipt remained. Page Designer restoration
advanced p_version_scn, so the original checksum did **not** return. The Product
Owner explicitly approved the complete-source-diff, counter-only recovery. Its
new two-read baseline is linked to the prior receipt. Never silently normalize
unknown differences or convert this bounded approval into a general drift bypass.

For a new pending-edit test, reserve the target and obtain approved Builder access,
record the exact original property, save one reversible title change, observe/export,
refuse admission, prove preservation, then restore only that property. A checksum
mismatch after restoration remains blocked until a reviewed recovery is authorized.
Do not rerun this test during a read-only handover or after the reservation ends.

## 9. Admit, restrict and deploy the selected archive — slides 29–31

Re-read the selected source/tag/hash and final available-state baseline immediately
before the operation. Record all history/configuration fields privately and compare
them after import. The existing snapshot selects complete rows from all seven
retained tables in stable primary-key order; do not publish its contents.

### Complete preservation and restriction SQL

```sql
set echo off verify off define on serveroutput off
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name e3-target
begin
  if user <> '&2' then raise_application_error(-20931,'Unexpected target'); end if;
end;
/
set heading off pagesize 0 feedback off linesize 32767 long 1000000 longchunksize 32767 trimspool on
spool "&1"
select 'greeting_history|'||json_object(*) from greeting_history order by greeting_id;
select 'hello_entries|'||json_object(*) from hello_entries order by entry_id;
select 'world_entries|'||json_object(*) from world_entries order by entry_id;
select 'hello_config|'||json_object(*) from hello_config order by config_id;
select 'world_config|'||json_object(*) from world_config order by config_id;
select 'lab_components|'||json_object(*) from lab_components order by component;
select 'lab_state|'||json_object(*) from lab_state order by state_key;
spool off
exit success
```

```sql
set echo off verify off define on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name e3-target
begin
  if user <> '&1' then raise_application_error(-20931,'Unexpected target'); end if;
  apex_util.set_security_group_id(apex_util.find_security_group_id('&2'));
  apex_application_admin.set_application_status(
    p_application_id => &3, p_application_status => apex_application_admin.c_app_restricted_access,
    p_allowed_users_list => apex_t_varchar2('VERIFIER'));
  commit;
end;
/
exit success
```

The restriction uses documented APEX availability and allows VERIFIER. It does not
provide continuous exclusion: first import actually restored Available before
restriction was reapplied. Human no-user/no-author coordination covers that interval.

### Complete deployment SQL and mapping

The native installer uses the generated private defaults mapping to E3_TARGET /
workspace E3_TARGET / app 810203 / alias E3-LAB. PROJECT deploy executes the ZIP's
native installer/Liquibase graph; inherited guards and released migrations remain
unchanged. It is qualified for the retained target's upgrade path, not fresh schemas.

```sql
set echo off verify off define on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name e3-target
begin
  if user <> '&3' then raise_application_error(-20931,'Unexpected target'); end if;
end;
/
define DEFAULTS_FILE = '&2'
project deploy -file &1
exit success
```

A newly authorized repeat uses an OS-temporary private directory, approved target
home, a fresh reservation and an admitted current receipt. This is the same native
sequence used in the recorded sync/repeat, not a request to run it now:

```bash
PRIVATE=$(mktemp -d "${TMPDIR:-/tmp}/e4-replay.XXXXXX")
chmod 700 "$PRIVATE"
printf '%s\n' 'apex.810003.workspace:E3_TARGET'   'apex.810003.appId:810203' 'apex.810003.schema:E3_TARGET'   'apex.810003.alias:E3-LAB' > "$PRIVATE/target.properties"
chmod 600 "$PRIVATE/target.properties"
"$SQLCL" -nohistory -noupdates -home "$TARGET_HOME" -S -L /nolog   @"$ROOT/examples/git-pipeline/sql/snapshot.sql" "$PRIVATE/before.txt" E3_TARGET
"$SQLCL" -nohistory -noupdates -home "$TARGET_HOME" -S -L /nolog   @"$ROOT/examples/git-pipeline/sql/restrict.sql" E3_TARGET E3_TARGET 810203
"$SQLCL" -nohistory -noupdates -home "$TARGET_HOME" -S -L /nolog   @"$E4/sql/observe.sql" e3-target E3_TARGET E3_TARGET 810203
"$SQLCL" -nohistory -noupdates -home "$TARGET_HOME" -S -L /nolog   @"$ROOT/examples/git-pipeline/sql/deploy.sql"   "$E4/tests/e3-1.0.7.zip" "$PRIVATE/target.properties" E3_TARGET
"$SQLCL" -nohistory -noupdates -home "$TARGET_HOME" -S -L /nolog   @"$E4/sql/observe.sql" e3-target E3_TARGET E3_TARGET 810203
"$SQLCL" -nohistory -noupdates -home "$TARGET_HOME" -S -L /nolog   @"$ROOT/examples/git-pipeline/sql/restrict.sql" E3_TARGET E3_TARGET 810203
```

Stop on any failed identity, source/hash/checksum admission, native error or unexplained
state. On native failure observe actual availability/checksum, attempt the known
restriction, retain evidence and participant exclusion, and request reviewed recovery.
Do not assume rollback or restriction persisted; do not write a success receipt.

## 10. Verify before publication, finalize, then repeat — slides 32–34

### Complete acceptance helper

This checks native readiness, A's header, C's region, baseline Hello and absence of
B, then creates/deletes a native APEX session as permitted VERIFIER. It does not
publish. Compare every retained business field before publication.

```sql
-- &1: connection; &2: schema; &3: workspace; &4: application.
-- Read-only acceptance checks; publication is a separate explicit operation.
set echo off verify off define on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name &1
declare n number;
begin
  if user <> '&2' then raise_application_error(-20931,'Unexpected target'); end if;
  apex_util.set_workspace(p_workspace=>'&3');
  lab_runtime.assert_ready;
  select count(*) into n from apex_application_pages
   where application_id=&4 and page_id=1
     and header_text='<p>E4 A: Select Hello and World values, then record the greeting.</p>';
  if n <> 1 then raise_application_error(-20932,'Selected A header missing'); end if;
  select count(*) into n from apex_application_page_regions
   where application_id=&4 and page_id=200 and region_name='World entries - selected C';
  if n <> 1 then raise_application_error(-20933,'Selected C region missing'); end if;
  select count(*) into n from apex_application_page_regions
   where application_id=&4 and page_id=100 and region_name='Hello entries';
  if n <> 1 then raise_application_error(-20934,'Baseline Hello region missing'); end if;
  select count(*) into n from apex_application_page_regions
   where application_id=&4 and region_name='Hello entries - deferred B';
  if n <> 0 then raise_application_error(-20935,'Deferred B is present'); end if;
  apex_session.create_session(p_app_id=>&4,p_page_id=>1,p_username=>'VERIFIER');
  apex_session.delete_session;
end;
/
prompt PASS selected A/C, excluded B, native readiness and verifier session
exit success
```

For an admitted live replay continuing stage 9:

```bash
"$SQLCL" -nohistory -noupdates -home "$TARGET_HOME" -S -L /nolog   @"$E4/sql/check.sql" e3-target E3_TARGET E3_TARGET 810203
"$SQLCL" -nohistory -noupdates -home "$TARGET_HOME" -S -L /nolog   @"$ROOT/examples/git-pipeline/sql/snapshot.sql" "$PRIVATE/after.txt" E3_TARGET
cmp "$PRIVATE/before.txt" "$PRIVATE/after.txt"
```

### Complete publication helper

Only after those checks pass does the operator restore Available. The final receipt
uses two matching checksums in that final state, never the transient restricted
checksum. Native status operations can advance the version counter; status toggles
are not checksum-neutral and repeat receipts need not equal the prior checksum.

```sql
-- &1: connection; &2: expected schema; &3: workspace; &4: application.
-- Invoke only after acceptance checks and full business-field comparison pass.
set echo off verify off define on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name &1
begin
  if user <> '&2' then raise_application_error(-20931,'Unexpected target'); end if;
  apex_util.set_workspace(p_workspace=>'&3');
  apex_application_admin.set_application_status(
    p_application_id=>&4,
    p_application_status=>apex_application_admin.c_app_available);
  commit;
end;
/
exit success
```

Continue only after successful acceptance and full preservation comparison:

```bash
"$SQLCL" -nohistory -noupdates -home "$TARGET_HOME" -S -L /nolog   @"$E4/sql/publish.sql" e3-target E3_TARGET E3_TARGET 810203
"$SQLCL" -nohistory -noupdates -home "$TARGET_HOME" -S -L /nolog   @"$E4/sql/observe.sql" e3-target E3_TARGET E3_TARGET 810203
"$SQLCL" -nohistory -noupdates -home "$TARGET_HOME" -S -L /nolog   @"$E4/sql/observe.sql" e3-target E3_TARGET E3_TARGET 810203
```

Finalize source/archive/target/options/status/checksum only after equality of these
last two reads and full acceptance. Repeat admission must start from that finalized
receipt. The recorded first deployment ran 1 changeset, 22 previously applied; the
repeat ran 0, 23 previously applied. The repeat stayed Restricted after deploy because
no app import ran. Both preserved every retained business field. Inspect:

```bash
code "$E4/tests/sync-lifecycle.json"
code "$E4/tests/repeat-lifecycle.json"
code "$E4/tests/sync-receipt.json"
code "$E4/tests/repeat-receipt.json"
code "$E4/tests/final-source-reconciliation.diff"
```

## 11. Verify in the browser and remove temporary access — slides 35–37

Open the retained central application at
[central DEV](http://127.0.0.1:8080/ords/r/e3_target/e3-lab/home), using the existing
runtime account through its authorized credential source. Do not press Create greeting
in a preservation demonstration. Home shows A's explanatory sentence. World entries
has the selected C region name in accessibility/Builder; Hello entries retains its
baseline region name. Region names are not necessarily rendered as visible report
headings because the theme hides those headers. Builder confirms exact Name values.
The provided screenshots use the actual desktop view; no business history is shared.

```bash
code "$E4/tests/central-final-home-desktop.png"
code "$E4/tests/central-final-c-designer.png"
code "$E4/tests/central-final-b-absent.png"
code "$E4/tests/browser-final.json"
```

### Complete temporary central-access removal SQL

This narrowly scoped SYS script removes only the approved E.4 identities and verifies
zero counts plus Available status. It has already been executed and is not idempotent;
do not rerun it against absent users. The current handover route reads its receipt.

```sql
-- Prepared host only: SYS in the existing apex-db CDB, after final validation.
-- Removes only the explicitly authorized E.4 temporary identities.
set echo off verify off serveroutput on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
alter session set container=FREEPDB1;
begin
  apex_util.set_workspace(p_workspace=>'E3_TARGET');
  apex_util.remove_user(p_user_name=>'E4_VERIFY');
  commit;
end;
/
alter user E3_TARGET revoke connect through E4_SYNC;
drop user E4_SYNC;
select count(*) temporary_database_users from dba_users where username='E4_SYNC';
select count(*) temporary_builder_users from apex_workspace_apex_users
 where workspace_name='E3_TARGET' and user_name='E4_VERIFY';
select application_id,availability_status from apex_applications
 where application_id=810203;
exit
```

```bash
code "$E4/tests/temporary-access-cleanup.log"
code "$E4/tests/cleanup.json"
```

Temporary private connection/password files are session material, not reusable
settings. Keep private diagnostics only as required for the reviewed evidence;
never copy the retained e1-secrets.json record or clean retained B's work. A future
live write demo requires a new explicit target reservation and approved access.

## 12. Gates, limits and Product Owner decision — slides 38–41

The existing runner sources manifest-listed functions. E.4 checks bind archive bytes,
real overlapping process receipts, GitHub admission and negative/positive receipts;
they explicitly identify themselves as evidence readers, not fresh Oracle replays.
The selected regression is the existing native pipeline smoke slice.

```bash
cd "$ROOT"
bash tests/run.sh --smoke --new-only progress/E.4/new_tests.manifest
bash tests/run.sh --integration --new-only progress/E.4/new_tests.manifest
bash tests/run.sh --smoke --new-only progress/E.4/regression_tests.manifest
code "$E4/sprint_E.4_handover.md"
```

Expect 1/1 smoke, 3/3 integration evidence checks and 2/2 regression smoke checks.
Runtime SM-1/IT-1/IT-2/IT-3/IT-4 evidence is described separately in the test report.
The controlled restoration failed its original checksum-equality hypothesis and
passed only the explicitly approved reviewed recovery procedure. Broader schema
fingerprinting, production races/fencing, general fresh installation, clean-host
reproduction and automatic release admission remain outside this prototype.

The independent Astra handover review must be read before acceptance. During the
live meeting, the Product Owner inspects the branch/PR journey, native artifact,
refusals, actual status transitions, final browser result and B continuation; then
accepts the handover or requests corrections. Passing gates and a rehearsal do not
constitute that decision or close Sprint E.4.
