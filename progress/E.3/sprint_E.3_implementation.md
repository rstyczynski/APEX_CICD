# E.3 — Implementation record

## Current native implementation — 2026-11-04

This section describes the implemented APEX-native/GitHub Actions prototype.
The earlier adapter-based implementation is retained below as historical
engineering evidence and is superseded. The public
[APEX_CICD_E3 seed](https://github.com/rstyczynski/APEX_CICD_E3) supplies application
source and workflows; each operator creates a writable application repository.
The parent APEX_CICD repository supplies the walkthrough and local runner launcher.

Foundation, Hello and World are **project-defined logical components within one
APEX application**. Hello and World contain separate page sets plus supporting
database objects; Foundation supplies shared runtime/data and component metadata.
They are not native APEX application entities or separately deployed mini apps.
The [walkthrough introduction](sprint_E.3_increment_demo.md#application-structure-and-terminology)
and PPTX slide 2 explain the distinction. Oracle's
[mini-app guidance](https://www.oracle.com/a/tech/docs/apex-lifecycle-management-v3.pdf#page=15)
describes a pattern for larger solutions using separate APEX applications,
common components and shared authentication. That proposed PBI-044 scenario
does not change the current single-application implementation.

[Requirements](../../docs/srs.md) own the product contract;
[architecture](../../docs/architecture.md) and [accepted design](sprint_E.3_design.md)
own architectural decisions. This record explains the implementation.
The [walkthrough](sprint_E.3_increment_demo.md) owns the single manual starting
point and repeats complete SQL source before execution. The
[configuration guide](sprint_E.3_github_configuration.md) and
[operator manual](user_manual.md) own settings and operating reference details;
[tests](sprint_E.3_tests.md) and linked receipts own observed results.
[PLAN](../../PLAN.md) owns sprint assignment/status. This correction changes no
status and makes no production-readiness claim.

### PBI-053.1 — Working Copy, capture, staging and verification

A developer creates a fresh APEX Working Copy from Main 810003, changes the
Home page title, compares and merges the selected page into Main using native
APEX collaboration. The region heading remains Hello World - Git pipeline,
which the acceptance script checks. Main is the coordinated export checkpoint;
SQLcl PROJECT captures its configured definitions without a Python adapter or
exported-source rewrite. This preserves the E.2 native approach.

The application project records its SQLcl release in project.config.json.
The qualified build is 25.4.1.022.0618; another installed client is not substituted
merely because it is newer. Named, slashless branches support the qualified
PROJECT comparison path. The e3-base branch identifies pipeline.json's baseline
commit, and source is committed before staging so the comparison sees the
intended revision. A detached checkout was observed to fail PROJECT verification;
release and qualification therefore attach the selected tag to local named
branches without moving the tag.

The three author scripts use lab-dev-c. Their prologue disables echo and
substitution verification and disables ampersand substitution. SQL/OS failures
request a failing exit and rollback, but PROJECT diagnostics still require
inspection of their own result summary. SQLcl's launcher selects the saved
profile before the file runs, preventing an absent connection from silently
continuing through later statements. The workflow uses isolated job profiles;
the author's CLI uses its existing native profile.

#### Capture source

**Complete source — `sql/capture.sql`:**

```sql
set echo off verify off define off
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name lab-dev-c
project export -list
project export
exit success
```

The first PROJECT command displays the configured export scope; the second
writes captured definitions into src. This reads authoring definitions and
changes local files, not the deployment target. Review the intended page-title
diff before committing. No live DEV export occurs during release packaging.

#### Stage the committed change

**Complete source — `sql/stage.sql`:**

```sql
set echo off verify off define off
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name lab-dev-c
project stage -branch-name e3-base
exit success
```

PROJECT compares the current named branch with e3-base and generates native
Liquibase distribution files and changelog entries in dist. The developer
reviews and commits the generated distribution. Staging does not execute the
installation against the target.

#### Verify source and distribution

**Complete source — `sql/verify.sql`:**

```sql
set echo off verify off define off
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name lab-dev-c
project verify -cbn e3-base -verbose
exit success
```

PROJECT verifies the selected baseline comparison, referenced staged scripts,
APEX export completeness and agreement, changelog structure/duplicates and
project configuration. In the observed missing-file case,
stagechangelogfilesvalid reports the changelog reference and absent script;
stagechangelogcomplete can still pass. These checks establish exercised source
consistency, not business correctness or full database drift protection.
The [native positive](tests/github-native-verify.log) and
[negative](tests/github-native-rejection.log) logs preserve exact rule output.
The release gate requires Errors: 0 and rejects configured Oracle/client error
patterns before target writes; a zero process exit alone is insufficient.

### PBI-053.2 — Git review and automatic version preparation

The hosted PR checks workflow responds to PR changes and also accepts an
explicit PR number for manual checks. It reads that PR's live metadata,
validates classification with pr-policy.jq, fetches its head and checks the
native project layout, absence of Python files and actionlint workflow syntax.
Two visible checks can be separate events running the same workflow on one head;
they are not two different native database tests. The hosted job receives no
Oracle password and does not connect to the lab database.

Ordinary change PRs require exactly one classification label and matching
semantic title: patch/fix:, minor/feat:, or major/feat!:. Squash merging keeps
the reviewed semantic title in main's history. Release Please runs on main
updates, proposes the version, CHANGELOG.md, version.txt and release manifest,
and publishes the matching tag and GitHub Release notes after its release PR
is merged. Labels validate intent; accepted semantic history drives the bump.
There is no implemented manual version override.

The generated bot PR is recognized through its bot identity, release branch
prefix and pending-release label. If bot-token event suppression leaves it
without checks, an operator dispatches PR checks from main with the current
release PR number. The job then validates that PR's current head; the dispatch
summary's main branch does not identify the tested PR revision. None of these
PR, version, tag or release events dispatches deployment.

### PBI-053.3 — Local runner and selected-tag deployment

scripts/e3-runner.sh installs/registers the official pinned runner with checksum
verification and a short-lived registration token, or retains a matching
registration. Explicit repository and persistent directory arguments separate
an operator's lab from the public seed. Registration lives outside the checkout
and disposable scratch. Status queries GitHub; the default run operation checks
registration/connectivity, clears inherited operator tokens and retired tool
settings, and starts the foreground listener. It does not provision Oracle,
APEX or ORDS. Those run in the existing Podman lab; the named Podman connection
avoids accidental use of another default VM. The Mac runner reaches the exposed
Oracle/ORDS ports without accessing APEX installation files.

Only workflow_dispatch from main runs Deploy selected version on the local
macOS ARM64 e3-lab runner. It validates the published tag, accepted ancestry and
version file, checks out controller SQL from main separately from the tagged
application, and creates the e3-release-build branch. A shared concurrency group
serializes deployment and qualification jobs in this repository; it does not
provide global database ownership or fencing across other writers.

#### Private tools, profiles and target mapping

The setup-native composite action uses setup-java for Java 21, downloads the
pinned SQLcl archive on each job and verifies its SHA-256. It publishes the
executable directory through GITHUB_PATH. GitHub environment e3-lab owns eight
nonsecret variables and AUTHOR_PASSWORD/TARGET_PASSWORD secrets. Generated
SQLcl connections lab-dev-c and e3-target use a private -home under RUNNER_TEMP;
passwords arrive through standard input, not committed SQL source. A generated
native defaults file maps source APEX identity to target schema/workspace/app ID
and alias. Action outputs and GITHUB_ENV pass paths to subsequent steps.
Always-run cleanup removes private connections and snapshots; uploaded results
exclude those private files. No native.env or .local-apex configuration is used.

Repeated tool setup is an explicit prototype cost. Proposed
[PBI-055](../../BACKLOG.md#pbi-055-reduce-repeated-pipeline-toolchain-setup)
covers reducing it while retaining approved versions, integrity checks and
private per-job credentials. A cache, provisioned toolchain or custom image is
not implemented by this documentation change.

#### Package the verified tagged state

The release first runs verify.sql above with the private author connection and
requires its explicit zero-error result. Only then does it package:

**Complete source — `sql/package.sql`:**

```sql
set echo off verify off define on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
project gen-artifact -name e3 -version &1 -format zip
exit success
```

The first argument is the selected tag's numeric version. DEFINE ON permits
SQLcl positional substitution; the workflow validates the tag's syntax first.
PROJECT creates artifact/e3-<version>.zip from the selected state without
recapturing live DEV. The same archive is installed and retained with its hash.

#### Capture retained fields before and after deployment

**Complete source — `sql/snapshot.sql`:**

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

The script selects e3-target and rejects an unexpected current schema.
Argument 1 is a private output path; argument 2 is the expected schema.
Ordered JSON rows include every selected table column, while formatting settings
suppress headings/feedback that would interfere with comparison. The workflow
uses cmp on before/after files. This covers these seven tables' captured fields,
not every database object, runtime session or user preference. Full snapshots
remain private rather than being uploaded as release artifacts.

#### Restrict application access

**Complete source — `sql/restrict.sql`:**

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

Arguments 1/2/3 identify schema, workspace and application. The schema guard
precedes APEX workspace-context selection. Native APEX availability permits
VERIFIER while restricting ordinary users, then commits. This is application
availability control, not an exclusive database lock. Because import can restore
source availability, the workflow repeats this script after installation before
checking retained fields; that repetition does not make the import window atomic.

#### Install the native archive

**Complete source — `sql/deploy.sql`:**

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

Arguments 1/2/3 are archive path, generated defaults-file path and expected
schema. The guard rejects the wrong database identity before PROJECT deploy.
DEFAULTS_FILE exposes the native target mapping to the archive's installer.
PROJECT executes native installation through Liquibase. The workflow captures
its log and rejects its configured error patterns. Rollback on a SQL error does
not undo already committed Oracle DDL, so general failed-deployment recovery
remains outside this happy-path prototype.

#### Accept native behavior and publish

**Complete source — `sql/accept.sql`:**

```sql
set echo off verify off define on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name e3-target
-- Read-only behavior checks precede publication.
declare n number;
begin
  if user <> '&1' then raise_application_error(-20931,'Unexpected target'); end if;
  lab_runtime.assert_ready;
  select count(*) into n from apex_application_page_regions
   where application_id=&3 and page_id=1 and region_name='Hello World - Git pipeline';
  if n <> 1 then raise_application_error(-20932,'Expected Home heading missing'); end if;
  apex_util.set_security_group_id(apex_util.find_security_group_id('&2'));
  -- Native APEX executes the application's Initialization PL/SQL Code.
  apex_session.create_session(p_app_id=>&3,p_page_id=>1,p_username=>'VERIFIER');
  apex_session.delete_session;
end;
/
-- APEX availability is inherited from the E.2 native approach.
begin
  apex_util.set_security_group_id(apex_util.find_security_group_id('&1'));
  apex_application_admin.set_application_status(
    p_application_id => &3, p_application_status => apex_application_admin.c_app_available);
  commit;
end;
/
prompt PASS native readiness, heading and APEX publication
exit success
```

Arguments 1/2/3 identify schema, workspace and application. LAB_RUNTIME checks
readiness, the metadata query requires the expected region, and native APEX
session creation executes application initialization as VERIFIER before the
session is removed. Only after those checks does the second block publish
availability and commit. Its final workspace lookup uses argument 1; the current
lab works because schema and workspace are both E3_TARGET. Supporting different
names requires a reviewed correction rather than assuming that this code covers it.
Browser verification separately checks the new page title and retained history;
the inherited APEX footer is not automatically stamped with the pipeline version.

The release receipt binds published tag, source SHA, archive SHA-256, workflow
run and target identifiers. The job retains the archive, public native logs and
receipt, and cleans private job material on success or failure. A failed step
blocks subsequent ordinary steps; cleanup/artifact retention use always-run
conditions. Failure is not an automatic redeploy or rollback request.

### Manual rejection first, then workflow automation

The [chapter H CLI exercise](sprint_E.3_increment_demo.md#first-demonstrate-the-native-check-manually)
uses a temporary clone on e3-manual-qualification. It runs the verify.sql source
above unchanged, moves one referenced staged SQL file outside the application
while leaving the changelog intact, requires the native missing-file error,
restores the file and verifies again. The original checkout and tag remain
intact. The [manual rehearsal](tests/manual-native-rejection.log), performed on
2026-11-04 against v1.0.4 with the qualified client, records Errors: 0, then 1,
then 0 and a clean restored tree.

The qualification workflow automates the intact/missing-file comparison on its
own named branch. It uses the same private setup and verify/snapshot SQL, requires
the initial zero-error summary, removes a referenced file, requires rejection
and compares target snapshots. Its receipt records positive_native_verify,
missing_changeset_rejected and target_unchanged as true and deployment_called
as false. It contains no package, deploy, restrict or publish step. This is a
negative architecture experiment, separate from verifying a deployed application.

Review correction R1-L2 replaces the weak rule-name predicate with the shared
`.github/assert-missing-changeset.awk` assertion. It requires a positive summary
consistent with ERROR rows, the expected failing stage rule and the literal
selected file path in that rule's message. It strips ANSI/padding and joins
only exact expected-path continuation fragments. The workflow and manual use
the selected file; the fixed reference reader uses the recorded legacy path.
The shared receipt filter requires path/controller/tool-output fields in schema
2 and permits the unchanged old receipt only for its pinned v1.0.4 source/run/path.
New receipts record controller SHA separately from application SHA. The corrected
assertions have offline fixture validation, not a newly executed native run.

Parent IT-1/IT-2 remain fixed seed-evidence readers of deployment 41679427616
and qualification 41679432928; they do not validate a selected LAB replay.
Platform smoke currently probes seed-configured endpoints and needs seed
environment API access. A replay is accepted through its own actual repository,
PR/tag/source, receipt/archive/native logs and browser observations.

R1-L1 is an explicitly approved temporary prepared-host credential deferral:
read the existing E.1/E.2 record for interactive logins without creating new
scratch authority or copying/deleting private records. GitHub jobs remain
independent. The [decision record](sprint_E.3_handover_review-1-decisions.md)
owns the accommodation's ending/reconsideration trigger. The inherited startup
fallback's scratch override is outside the supported explicit-VM-start path.

### Evidence and remaining boundaries

The [configuration/run record](sprint_E.3_github_configuration.md#verification-scope)
links the native release and qualification receipts and observed checks.
The [handover](sprint_E.3_handover.md) owns the acceptance discussion. These
records do not establish independent peer review, clean-host provisioning,
complete identity/state preservation, atomic fencing, full drift detection or
general DDL recovery. The broader proofs remain registered follow-up work;
Elaboration prototype delivery and production readiness are different outcomes.

## Historical implementation — superseded

The sections below preserve the earlier 1.0.1 implementation, including its
private-repository assumption, Python source adapter and former runner defaults.
They are historical accounts, not current instructions. The current native
implementation above and GitHub configuration guide supersede them.

### PBI-053.1 — Capture and native baseline

Created the private application repository
[APEX_CICD_E3](https://github.com/rstyczynski/APEX_CICD_E3), a schema/workspace
E3_TARGET and application 810203. Retained E1_UAT and earlier sprint files remain
untouched. APEX Main is E1_DEV_C/810003. New Working Copy 100, “E3 heading patch”,
changed one Home region heading. Native browser comparison found one changed
page; it was selectively merged into Main with a target backup. Native PROJECT
export captured the result into the application Git repository.

SQLcl 25.4.1.022.0618 verifies consistent source/distribution with zero errors.
The slash-containing branch issue still appears during native source/dist
comparison; explicit slashless e3-initial/e3-heading/e3-runtime-correction branches
are used in this separate demo repository. The parent project retains its
normal branch conventions. The original failing stage output stays private.

Initial deployment exposed a mapping lookup failure because the generated
archive excludes repository-level utils. The thin installer now supplies the
absolute defaults-file path computed from its checked-out repository; the file
is committed, contains no secrets and is selected from the same source revision.
The first attempt rolled back before application installation. A retry installed
the baseline and a real greeting/history row was then added in the disposable
schema for preservation verification.

Browser validation exposed a retained E1_CTRL session hook unavailable on the
new target. A second patch PR replaces it in reviewed source with the existing
LAB_RUNTIME.assert_ready before native staging. The explicit capture adapter
performs this bounded conversion of SQL/readable source after export and before
review/stage; no post-stage archive patching occurs. Native verification passes.
The original author application/control packages and retained UAT are not changed
by that conversion. This is a documented prototype adapter, not general removal
of E.1 fencing/ownership guarantees.

### PBI-053.2 — GitHub integration and version preparation

The three workflows and thin scripts are versioned in
[examples/git-pipeline](../../examples/git-pipeline/), with a baseline Git bundle
and [preparation script](user_manual.md#configuration-ownership) preserving source provenance.
PR checks validate exactly one patch/minor/major label against the Conventional
Commit title, run source/shell checks and actionlint. Squash merge retains that
title. Release Please generates the version/changelog release PR; both that
record and GitHub Release notes use the same history. Its bot PR is explicitly
checked through manual hosted dispatch, accounting for GITHUB_TOKEN event
suppression. Deployment has no PR/push/tag/release event trigger.

Change PR 1 introduced the heading. PR 3 contains the bounded runtime adapter;
both are patch fixes accumulated into release PR 2 for 1.0.1. The sequential
review/merge roles are exercised by Codex under the Product Owner's instruction;
this is not an independent human peer-review claim.

### PBI-053.3 — Manual deployment and handover

#### Current runner installation and launch

The versioned [runner launcher](../../scripts/e3-runner.sh) implements installation separately from starting the listener. From the parent laboratory repository root, `./scripts/e3-runner.sh setup` prepares a new macOS ARM64 host: it downloads GitHub runner 2.338.2, verifies its pinned SHA-256, extracts it into `~/actions-runner-e3`, obtains a short-lived registration token through the operator's authenticated `gh` session and invokes the official `config.sh` for the private application repository with label `e3-lab`. A matching existing registration is retained; an unrelated or nonempty unregistered directory is rejected. Setup finishes by checking the GitHub-configured Oracle TCP and ORDS HTTP endpoints.

Installation and registration are required once per new runner host so GitHub can assign jobs to it. For subsequent lab sessions, `./scripts/e3-runner.sh` checks registration and endpoint access, clears inherited operator tokens and retired tool settings, then starts the official foreground `run.sh`. Wait for **Listening for Jobs** and keep the terminal open; Control-C stops it. Setup does not start a listener or provision Oracle/APEX/ORDS. Java, SQLcl and temporary job connections are prepared by the workflow. The [manual](user_manual.md#runner-infrastructure-and-workflow-setup) owns prerequisites and options; [walkthrough stage 5](sprint_E.3_increment_demo.md#5-deployer-selects-the-version) and presentation slide 4 show the operator sequence. The following initial-run account is historical.

A dedicated runner, e3-lab-mac, is registered only to the private demo repository.
The official runner archive SHA-256 was checked before extraction. Registration
required running outside the filesystem sandbox after .NET initialization failed.
No OS service was installed. PR/version jobs run on hosted runners; only the
manually dispatched lab deployment uses this local runner and private connection
configuration. [Runner entry point](user_manual.md#runner-infrastructure-and-workflow-setup) starts it for
future use. Run results, evidence and final limitations belong in the test and
handover records as they become available.

The first manual 1.0.1 run (41664285664) failed before deployment because native
PROJECT cannot verify detached HEAD. PR 4 corrects the main workflow to attach
the exact selected tag commit to a local e3-release-build branch. It does not
retag or modify application version 1.0.1. The deployment workflow is read from
accepted main while application bytes come from the selected version tag; run
history preserves both revisions. The second dispatch uses the same 1.0.1 app
version with that corrected workflow. Later Release Please proposals need not
be published or deployed for this experiment.

### Delivered verification and retention

The second manual run 41664798289 passed, binding version v1.0.1 to source
2e203ba571bbce9fd30cafc5531e36250d5594b2 and the downloaded native ZIP hash.
The deployed browser heading and existing greeting/history were inspected.
All required new-code and smoke regression gates passed. A further isolated
source-clone rehearsal ran the reusable capture.sh adapter, stage and native
verify successfully, without deployment. [Its receipt](tests/capture-rehearsal.json)
records scope. The source bundle now preserves final accepted main, both tags
and comparison history, with [identity](tests/bundle.json).

Retain the small example and scripts as a reference architecture prototype;
do not promote them to a production service without the registered additional
proofs. The [walkthrough](sprint_E.3_increment_demo.md), [manual](user_manual.md)
and [handover](sprint_E.3_handover.md) are the user-facing delivery set.

## PBI-058 — 2026-11-05 native release correction

The [correction record](sprint_E.3_release_correction.md) owns changed behavior, actual native execution and limitations. The [final gap reassessment](sprint_E.3_final_gap_analysis.md) replaces the incomplete closing mapping. Required gates use release_correction_tests.manifest: SM-1/SM-058 pass workflow and fail-closed source checks; IT-058 checks the fresh local native evidence and archive/bundle hashes. The actual native commands ran separately and are retained under tests/release-correction. The integration test function is an evidence reader, not a new remote run. Full smoke regression is required. Native release/verify/package, supported-target upgrade/repeat and APEX sessions passed; a fresh disposable-schema attempt failed the inherited seed guard and remains an explicit limitation.
