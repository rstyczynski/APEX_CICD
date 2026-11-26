# E.16 native release walkthrough

The [native release workflow reference](native_release_workflow.md) documents all 33 declared Actions steps, their SQL payloads, Python checks and the [assert limitation](native_release_workflow.md#assert-limitation). This walkthrough remains the demonstration sequence and slide map.

PBI-084 promises native installation, upgrade and safe repeat with preserved data and verifiable provenance. The [checklist](sprint_E.16_checklist.md) tracks acceptance; the [manual](user_manual.md) owns prerequisites and recovery. The [presentation](sprint_E.16_increment_demo.pptx) follows the slide map below. This is a disposable table experiment on the E.15 GitHub execution boundary, not full APEX/ORDS or clean-host qualification.

## Starting state and execution boundary — slides 1–5

Start with authenticated GitHub CLI access to the private `rstyczynski/APEX_CICD_E.16` repository. The workflow declares Java 21, checksum-pinned SQLcl 25.4.1.022.0618 and two digest-pinned Oracle services. Both databases use AUTHOR16; their independent storage isolates authoring from deployment. The target starts empty. GitHub Actions sequences named lifecycle steps; each invokes native SQLcl PROJECT through a thin one-invocation shell adapter. Python performs only tool, output and provenance checks. The provenance guard rejects mismatched source, build or archive SHA-256 before invoking deployment. Generated native source and release-preparation commits are retained in a Git bundle. The workflow commit/run and reviewed-input manifest connect that history to reviewed fixture source.

The [standing project rule](../../AGENTS.md#use-core-technologies-for-their-native-responsibilities) assigns sequencing and visibility to Actions, native release behavior to SQLcl PROJECT and version history to Git. Supporting checks do not replace those tools. See [the correction design and verification](sprint_E.16_actions_refactor.md).

## SQL and native lifecycle — slides 6–9

The following is the complete significant SQL executed by the named workflow steps. Each invocation enables `whenever sqlerror exit failure rollback` and `whenever oserror exit failure rollback`. Native output is also checked for SQL errors and nonzero verification Errors counts. Service bootstrap executes the following separately in each disposable database as SYS; the credentials are disposable fixture values, never production credentials.

```sql
alter session set container=FREEPDB1;
create user AUTHOR16 identified by Disposable_Native_16 quota unlimited on users;
grant connect, resource, create view to AUTHOR16;
```

Authoring connects to port 1521, target deployment to 1522. The named “Save job-private SQLcl connections” step invokes the adapter without a preselected connection and executes:

```sql
connect -save native-author -savepwd AUTHOR16/Disposable_Native_16@//127.0.0.1:1521/FREEPDB1
connect -save native-target -savepwd AUTHOR16/Disposable_Native_16@//127.0.0.1:1522/FREEPDB1
```

SQLcl saves each job-private named connection once, then uses `connect -name`. Files live under RUNNER_TEMP and disappear with the hosted runner. The author executes:

```sql
create table preserved (id number primary key, message varchar2(80));
project init -name native16 -schemas AUTHOR16
project export -schemas AUTHOR16
project stage -branch-name baseline
project verify -compared-branch-name baseline -verbose
project release -version 1.0.0
project gen-artifact -name native16 -version 1.0.0
```

The workflow initializes a baseline Git branch, commits generated metadata, exports and commits reviewed table source, then commits the prepared release. Before deployment it verifies native metadata version 25.4.1.0, the actual qualified build, source identity and archive bytes. The target executes `project deploy -file` with that verified archive path, then:

```sql
insert into preserved values (1,'retained across upgrade');
commit;
```

For 1.1.0, the baseline branch advances to the prepared 1.0.0 commit. The author executes:

```sql
alter table preserved add (extra varchar2(80));
project export -schemas AUTHOR16
project stage -branch-name baseline
project verify -compared-branch-name baseline -verbose
project release -version 1.1.0
project gen-artifact -name native16 -version 1.1.0
```

After provenance validation the target deploys the 1.1.0 archive, then repeats precisely those bytes. After each deployment it executes:

```sql
select id,message,extra from preserved;
begin
 declare n number; begin select count(*) into n from preserved where id=1 and message='retained across upgrade'; if n<>1 then raise_application_error(-20016,'lost data');end if;end;
end;
/
```

Expected visible result is ID 1, MESSAGE `retained across upgrade`, and null EXTRA, with successful PL/SQL assertion. Repeat must preserve that row. Archive digest identity proves the repeat used identical bytes; target logs prove the observed bounded state.

## Run and inspect — slide 10

The workflow exposes the preceding operations as named steps rather than calling a lifecycle script. “Export source”, “Stage changes”, “Verify changes”, “Prepare release” and “Package release” each appear separately for 1.0.0 and 1.1.0. Installation, upgrade, repeat, target assertions and each rejection case also have separate step outcomes. Open the `native` job and expand each step to inspect the actual command and SQLcl output.

The sql.sh adapter performs one SQL payload invocation plus a preflight SQLcl version probe. It checks the measured tool/build and current native metadata, adds SQL/OS failure handling and the selected saved connection, streams output to the Actions log and a retained file, and rejects native error output even if the process returns zero. It never chooses or loops through lifecycle stages. Git commands in Actions steps commit exported source and prepared releases; jq and sha256sum write provenance receipts. The always-run private-connection cleanup precedes the always-run evidence upload. These supporting operations leave sequencing and lifecycle behavior with their native technologies. It creates fresh disposable services for each run. From the checkout root:

```bash
cd "$(git rev-parse --show-toplevel)"
gh workflow run native.yml --repo rstyczynski/APEX_CICD_E.16
gh run list --repo rstyczynski/APEX_CICD_E.16 --workflow native.yml --limit 5
```

Inspect the chosen run's terminal conclusion before accepting it. The verified refactored native run is:

```bash
gh run view 45810907563 --repo rstyczynski/APEX_CICD_E.16
code progress/E.16/tests
```

Extract the [retained raw evidence](tests/actions-refactor/README.md#read-the-retained-evidence), then read `native/receipt-1.0.0.json` and `native/receipt-1.1.0.json` alongside package, install, upgrade, repeat and assertion logs. The receipt names the source commit, actual SQLcl build, archive digest, workflow source and run. The bundle contains exported SQL and native release changesets. A successful exit alone does not establish provenance: compare archive hashes, reviewed workflow/helper hashes, history and actual SQL, as recorded in the [source review](sprint_E.16_source_review.md).

## Failures and rejection — slides 11–13

Cross-schema deployment failed with ORA-01031; separate databases with the same schema name repaired that native limitation. Repeatedly saving the same connection failed; saving once repaired initialization. [The failure record](sprint_E.16_bugs.md) retains exact runs and errors.

The negative phase alters receipt digest, selected source, actual tool build and archive bytes separately. Each must raise before deployment; the source invokes no deployment in these rejection branches. It runs the actual checksum-pinned SQLcl 25.3 executable to obtain its incompatible build. It does not attempt incompatible deployment. The unchanged target query before and after establishes the bounded row/schema observation; it is not a general database-wide mutation audit.

## Verification and decisions — slides 14–15

[Verification](sprint_E.16_tests.md) distinguishes syntax and isolated guard tests from real hosted Oracle behavior and full regression. [Handover](sprint_E.16_handover.md) records what was actually demonstrated and any remaining limits. Production multi-user authority, complete APEX/ORDS delivery and independent clean-host reproduction remain outside this table experiment. The latter is assigned to E.17. Product Owner questions and reactions are recorded only when observed.
