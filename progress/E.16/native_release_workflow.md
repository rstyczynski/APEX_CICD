# E.16 native release workflow reference

This document explains the current [native.yml](../../sprint-work/E.16/.github/workflows/native.yml) and its supporting checks. The YAML and linked source files own executable behavior; this guide owns the technical explanation and must be reconciled when those sources change. The [user manual](user_manual.md) owns prerequisites, invocation and recovery, while the [walkthrough](sprint_E.16_increment_demo.md) owns the demonstration journey and slide map. The [implementation record](sprint_E.16_implementation.md) and [Actions correction record](sprint_E.16_actions_refactor.md) own design history, qualification and evidence. [Architecture responsibilities](../../docs/architecture.md#native-technology-responsibilities) and the [standing project rule](../../AGENTS.md#use-core-technologies-for-their-native-responsibilities) govern technology ownership.

## Responsibility and execution boundary

GitHub Actions owns sequencing, conditions, failure propagation and the visible execution timeline. SQLcl PROJECT owns init, export, stage, verify, release, gen-artifact and deploy. Native Git owns commits, branches and history; Oracle owns SQL execution and constraints. Shell glue invokes those tools and generates receipts using jq/sha256sum. Python only validates measured tools/metadata, native output and provenance. There is no Python lifecycle controller; lifecycle.py was removed.

The native job runs on ubuntu-24.04 with a 25-minute timeout and read-only contents permission. Two digest-pinned Oracle services expose independent FREEPDB1 databases on host loopback ports 1521 and 1522. Both use AUTHOR16 to preserve native schema qualification without archive rewriting. Java 21 and checksum-pinned SQLcl 25.4.1.022.0618 process the generated native project with sqlcl.version 25.4.1.0. SQLcl 25.3.0.274.1210 is only an incompatible-input fixture. This is a bounded disposable table experiment, not complete APEX/ORDS or independent-host qualification.

There are 33 declared workflow steps below. The retained successful job reports 39 steps because GitHub also records runner/service setup, post-action cleanup and job completion. Ordinary run steps use the default Actions failure behavior; shell failures stop later normal steps. Cleanup and artifact upload explicitly use always(). Exact source action/image/download pins remain in the YAML rather than a duplicated configuration specification here.

## SQLcl invocation adapter

Before the step catalog, [sql.sh](../../sprint-work/E.16/sql.sh) must be understood: every call first runs SQL_EXE -version and checks the captured output against the qualified release/build and any existing native metadata. It then creates a job-private input, prepends SQL/OS error handling and an optional saved connection, appends the caller's SQL and terminates that SQLcl session. One payload invocation runs with a 240-second timeout, the private SQLcl home, history/update checks disabled, and output streamed through tee to the named result log. pipefail propagates SQLcl/tee failures. check_output.py also rejects native errors when the process returns zero. The EXIT trap deletes the temporary input. No phase loop or next-stage decision exists in this adapter.

The generated SQL prelude is shown here. CONNECTION is explanatory notation for the selected saved alias; the workflow passes native-author or native-target. With selector "-", the connect line is omitted and the complete caller payload supplies connection creation. These are hosted-job reference snippets, not a standalone local deployment recipe. Unquoted YAML shell heredocs expand GITHUB_WORKSPACE before SQLcl receives deployment paths.

```sql
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name CONNECTION
```

The adapter appends a SQLcl session exit after the payload. That terminates the SQLcl child process, not an operator's parent shell. tool.txt records the measured tool output; each label records its own payload output. The Python checker details and the optimization limitation are below.

## Declared Actions steps in execution order

The SQL blocks below reproduce the complete workflow heredoc payloads. SQLcl PROJECT commands are native commands without SQL semicolons. SQL/PLSQL bodies retain their own terminators. They execute through the already explained adapter except bootstrap, which uses SQL*Plus directly inside each service.

### 1. actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683

Checks out the trusted companion revision using the pinned checkout action. persist-credentials is false; the fixture Git history created later is separate from this checkout. No SQLcl or Python check runs here.

### 2. actions/setup-java@cf277c60eb25467037889841efdb72551f06f6c3

Installs Temurin Java 21 through the pinned setup-java action. This supplies the SQLcl runtime; it does not execute a release phase.

### 3. Install qualified SQLcl

Downloads SQLcl 25.4.1.022.0618, verifies its pinned SHA-256, unpacks it under RUNNER_TEMP and publishes SQL_EXE through GITHUB_ENV. Separately downloads/checksums 25.3.0.274.1210 for the later refusal case and publishes INCOMPATIBLE_SQL_EXE. A failed download/checksum stops subsequent normal steps. The exact URLs/checksums remain owned by the YAML.

### 4. Initialize isolated native schemas

Runs the following bootstrap SQL as SYS inside each of the two disposable Oracle services using docker exec and SQL*Plus. Both independent databases get AUTHOR16. This is fixture provisioning, not PROJECT release deployment. The password shown is the disposable fixture value from source, not a production credential. SQL errors fail bootstrap.

```sql
whenever sqlerror exit failure
alter session set container=FREEPDB1;
create user AUTHOR16 identified by Disposable_Native_16 quota unlimited on users;
grant connect, resource, create view to AUTHOR16;
```

### 5. Initialize job-private workspace

Creates RUNNER_TEMP/native and the checkout result directory. sha256sum records the workflow, sql.sh and all three Python check files in result/reviewed-inputs.sha256. This manifest binds the reviewed executable inputs; no database operation occurs.

### 6. Save job-private SQLcl connections

Invokes sql.sh with connection selector "-", so the payload itself creates the two saved connections. Author uses host port 1521; target uses 1522. SQLcl stores both beneath RUNNER_TEMP/private-sqlcl. Subsequent calls select native-author or native-target by name; no Python state tracks saved connections. The adapter arguments are `-` and `connections`; payload output is retained as `result/connections.log`.

```sql
connect -save native-author -savepwd AUTHOR16/Disposable_Native_16@//127.0.0.1:1521/FREEPDB1
connect -save native-target -savepwd AUTHOR16/Disposable_Native_16@//127.0.0.1:1522/FREEPDB1
```

### 7. Create author fixture

Connects as native-author through sql.sh and creates the initial source table. The target still has no application table. Native errors fail the step. The adapter arguments are `native-author` and `author-initial`; payload output is retained as `result/author-initial.log`.

```sql
create table preserved (id number primary key, message varchar2(80));
```

### 8. Initialize native SQLcl project

Runs native PROJECT init as native-author. jq first requires the generated sqlcl.version to equal 25.4.1.0, then changes only sqlcl.connectionName to native-author. It does not rewrite the tool version. Creates the expected dist/releases/apex directory, initializes a native Git repository on baseline, commits generated metadata and switches to release. This working repository supplies the source/preparation history captured in receipts and the final Git bundle. The adapter arguments are `native-author` and `init`; payload output is retained as `result/init.log`.

```sql
project init -name native16 -schemas AUTHOR16
```

### 9. Export source 1.0.0

Connects as native-author and uses native PROJECT export for 1.0.0. Native Git adds and commits the exported source on release; the commit is the source input for subsequent staging. The adapter arguments are `native-author` and `export-1`; payload output is retained as `result/export-1.log`.

```sql
project export -schemas AUTHOR16
```

### 10. Stage changes 1.0.0

Connects as native-author and asks PROJECT to stage 1.0.0 changes against baseline. SQLcl generates the staged changesets; the shell/Python checks do not calculate migrations. The adapter arguments are `native-author` and `stage-1`; payload output is retained as `result/stage-1.log`.

```sql
project stage -branch-name baseline
```

### 11. Verify changes 1.0.0

Connects as native-author and runs native PROJECT verification of 1.0.0 against baseline. SQLcl owns its native project verification checks. check_output.py only detects reported errors, including a nonzero Errors count. The adapter arguments are `native-author` and `verify-1`; payload output is retained as `result/verify-1.log`.

```sql
project verify -compared-branch-name baseline -verbose
```

### 12. Prepare release 1.0.0

Connects as native-author and asks PROJECT to prepare release 1.0.0. Git then commits the generated release preparation. No Python code manufactures changelogs. The adapter arguments are `native-author` and `release-1`; payload output is retained as `result/release-1.log`.

```sql
project release -version 1.0.0
```

### 13. Package release 1.0.0

Connects as native-author and asks PROJECT to generate the 1.0.0 artifact. Shell find/test require the expected native16-1.0.0.zip file, then copy its exact bytes into result/. jq writes receipt-1.0.0.json with current native Git HEAD, approved build, ZIP SHA-256, version, workflow SHA/run ID and reviewed-input manifest digest. The adapter separately measures/enforces the actual approved build; the receipt build field itself is a declared constant, not a measurement. The adapter arguments are `native-author` and `package-1.0.0`; payload output is retained as `result/package-1.0.0.log`.

```sql
project gen-artifact -name native16 -version 1.0.0
```

### 14. Install verified release 1.0.0

First calls provenance.py with the 1.0.0 archive/receipt, native Git HEAD and approved build. Only a successful guard allows the adapter to connect as native-target and invoke PROJECT deploy. The adapter performs its own measured tool/metadata preflight before executing the payload. The adapter arguments are `native-target` and `install`; payload output is retained as `result/install.log`.

```sql
project deploy -file $GITHUB_WORKSPACE/result/native16-1.0.0.zip
```

### 15. Seed retained target data

Connects as native-target, inserts ID 1 with the known message and commits. This is the business-data preservation fixture for upgrade and repeat assertions. The adapter arguments are `native-target` and `seed`; payload output is retained as `result/seed.log`.

```sql
insert into preserved values (1,'retained across upgrade');
commit;
```

### 16. Apply additive author change

Moves baseline to the prepared 1.0.0 commit with native Git, then connects as native-author and adds nullable EXTRA. The target is not changed in this step. The adapter arguments are `native-author` and `author-upgrade`; payload output is retained as `result/author-upgrade.log`.

```sql
alter table preserved add (extra varchar2(80));
```

### 17. Export source 1.1.0

Connects as native-author and uses native PROJECT export for 1.1.0. Native Git adds and commits the exported source on release; the commit is the source input for subsequent staging. The adapter arguments are `native-author` and `export-2`; payload output is retained as `result/export-2.log`.

```sql
project export -schemas AUTHOR16
```

### 18. Stage changes 1.1.0

Connects as native-author and asks PROJECT to stage 1.1.0 changes against baseline. SQLcl generates the staged changesets; the shell/Python checks do not calculate migrations. The adapter arguments are `native-author` and `stage-2`; payload output is retained as `result/stage-2.log`.

```sql
project stage -branch-name baseline
```

### 19. Verify changes 1.1.0

Connects as native-author and runs native PROJECT verification of 1.1.0 against baseline. SQLcl owns its native project verification checks. check_output.py only detects reported errors, including a nonzero Errors count. The adapter arguments are `native-author` and `verify-2`; payload output is retained as `result/verify-2.log`.

```sql
project verify -compared-branch-name baseline -verbose
```

### 20. Prepare release 1.1.0

Connects as native-author and asks PROJECT to prepare release 1.1.0. Git then commits the generated release preparation. No Python code manufactures changelogs. The adapter arguments are `native-author` and `release-2`; payload output is retained as `result/release-2.log`.

```sql
project release -version 1.1.0
```

### 21. Package release 1.1.0

Connects as native-author and asks PROJECT to generate the 1.1.0 artifact. Shell find/test require the expected native16-1.1.0.zip file, then copy its exact bytes into result/. jq writes receipt-1.1.0.json with current native Git HEAD, approved build, ZIP SHA-256, version, workflow SHA/run ID and reviewed-input manifest digest. The adapter separately measures/enforces the actual approved build; the receipt build field itself is a declared constant, not a measurement. The adapter arguments are `native-author` and `package-1.1.0`; payload output is retained as `result/package-1.1.0.log`.

```sql
project gen-artifact -name native16 -version 1.1.0
```

### 22. Upgrade with verified release 1.1.0

First checks the 1.1.0 archive/receipt against native Git HEAD and approved build, then connects as native-target through the measured-tool adapter and invokes PROJECT deploy. SQLcl/Liquibase performs the additive upgrade. The adapter arguments are `native-target` and `upgrade`; payload output is retained as `result/upgrade.log`.

```sql
project deploy -file $GITHUB_WORKSPACE/result/native16-1.1.0.zip
```

### 23. Assert retained data after upgrade

Connects as native-target, prints ID/MESSAGE/EXTRA and raises ORA-20016 if the original ID/message row is missing. The visible expected row is ID 1, MESSAGE retained across upgrade and null EXTRA. The adapter arguments are `native-target` and `assert-upgrade`; payload output is retained as `result/assert-upgrade.log`.

```sql
select id,message,extra from preserved;
begin
 declare n number; begin select count(*) into n from preserved where id=1 and message='retained across upgrade'; if n<>1 then raise_application_error(-20016,'lost data');end if;end;
end;
/
```

### 24. Repeat identical verified release 1.1.0

Repeats the same provenance guard and native-target PROJECT deploy against the same qualified 1.1.0 ZIP. No new package is generated. The qualified run reports zero new changesets and two previously run; the next step checks retained data. The adapter arguments are `native-target` and `repeat`; payload output is retained as `result/repeat.log`.

```sql
project deploy -file $GITHUB_WORKSPACE/result/native16-1.1.0.zip
```

### 25. Assert retained data after repeat

Repeats the same native-target query and PL/SQL preservation assertion after the identical archive has been deployed again. This checks the fixture row; it does not claim database-wide or full-application preservation. The adapter arguments are `native-target` and `assert-repeat`; payload output is retained as `result/assert-repeat.log`.

```sql
select id,message,extra from preserved;
begin
 declare n number; begin select count(*) into n from preserved where id=1 and message='retained across upgrade'; if n<>1 then raise_application_error(-20016,'lost data');end if;end;
end;
/
```

### 26. Observe target before refusal checks

Connects as native-target and captures the known table state in negative-before.log. It establishes the bounded comparison state for the four following refusal cases. The adapter arguments are `native-target` and `negative-before`; payload output is retained as `result/negative-before.log`.

```sql
select id,message,extra from preserved;
```

### 27. Reject mismatched artifact evidence

Uses jq to replace the receipt SHA-256 with zeros in RUNNER_TEMP/wrong-receipt.json. Calls provenance.py against the unchanged 1.1.0 archive, actual Git HEAD and approved build. The shell requires nonzero status and the exact message artifact mismatch. No deploy or SQL payload is called by this refusal step.

### 28. Reject mismatched source evidence

Uses jq to replace the receipt source with zeros, then checks it against actual Git HEAD. Requires nonzero provenance.py status and source mismatch. No deploy or SQL payload is called.

### 29. Reject actual incompatible SQLcl build

Executes the checksum-pinned older SQLcl with -version only, retains incompatible-tool.txt and extracts actual build 25.3.0.274.1210. Passes that measured wrong build to provenance.py with the valid archive/receipt/source. Requires nonzero status and tool mismatch. It never uses the older executable to deploy or connect to the target.

### 30. Reject substituted archive bytes

Copies the qualified 1.1.0 ZIP to substituted.zip and appends altered bytes. The original ZIP and receipt stay unchanged. provenance.py must return nonzero with artifact mismatch before any deployment is invoked.

### 31. Assert refusal cases preserved target

Connects as native-target and captures negative-after.log, then cmp requires byte-identical before/after query output. Native Git creates native-history.bundle with all fixture refs. jq writes success.json only after the comparisons succeed, recording install/upgrade/repeat/preservation and all four refusal cases. This is a bounded observed-row comparison plus inspection of refusal control flow, not a general mutation audit. The adapter arguments are `native-target` and `negative-after`; payload output is retained as `result/negative-after.log`.

```sql
select id,message,extra from preserved;
```

### 32. Clean job-private connection material

Uses if: always() to remove RUNNER_TEMP/private-sqlcl and the temporary wrong receipt on success or failure. Each sql.sh call separately removes its temporary input through an EXIT trap. Hosted runner/service disposal removes the experiment environment; evidence contains outputs rather than saved private profiles.

### 33. Preserve experiment evidence

Uses the pinned upload-artifact action with if: always(). Uploads result/ as native-${{ github.run_id }}, including diagnostics after a failed run when files exist. Uploading an artifact does not make a failed lifecycle pass.

## Python checks and invocation contracts

These are the three runtime Python files in the E.16 companion. None imports subprocess, invokes Git/SQLcl, selects a lifecycle phase or schedules work. Nonzero check status stops its caller's normal Actions step. The command arguments below describe the workflow contract; they are not instructions to run against a retained target.

### check_tool.py

[Source](../../sprint-work/E.16/check_tool.py). Takes one argument: the captured SQLcl version-output file. Requires the measured text to contain release 25.4.1.0 and build 25.4.1.022.0618. If .dbtools/project.config.json exists in the current project directory, also requires sqlcl.version 25.4.1.0. If the file is absent, the metadata comparison is skipped; this permits native init, but the checker itself does not distinguish init from later phases. Native PROJECT commands retain their own project-context checks. It only reads metadata and never upgrades or rewrites it. Failures exit with tool mismatch or metadata version mismatch. These are explicit if/SystemExit checks and remain active with Python optimization.

```python
"""Validate measured SQLcl identity and native metadata without invoking tools."""
import json,sys
from pathlib import Path
text=Path(sys.argv[1]).read_text()
if 'Release 25.4.1.0 Production Build: 25.4.1.022.0618' not in text:
    raise SystemExit('tool mismatch')
config=Path('.dbtools/project.config.json')
if config.exists() and json.loads(config.read_text())['sqlcl']['version']!='25.4.1.0':
    raise SystemExit('metadata version mismatch')
```

### check_output.py

[Source](../../sprint-work/E.16/check_output.py). Takes one argument: the saved native output file. Removes matched ANSI SGR styling for inspection, then rejects nonzero verification Errors counts, leading ORA-/PLS-/SP2-/ERROR/Error starting/Unknown Command messages and Expected a subcommand. It detects reported native failures rather than implementing PROJECT verification. A match exits with native output contains errors. The explicit if/SystemExit check remains active with optimization.

```python
"""Reject native errors even when SQLcl returns zero."""
import re,sys
from pathlib import Path
text=re.sub(r'\x1b\[[0-9;]*m','',Path(sys.argv[1]).read_text())
if re.search(r'Errors:\s*[1-9]|(?im:^\s*(?:ORA-|PLS-|SP2-|ERROR\b|Error starting|Unknown Command))|Expected a subcommand',text):
    raise SystemExit('native output contains errors')
```

### provenance.py

[Source](../../sprint-work/E.16/provenance.py). Takes archive path, receipt JSON path, selected native source commit and supplied tool-build string. Compares receipt source to the supplied commit, receipt/supplied build to the approved build, and receipt SHA-256 to the actual archive bytes. In deployment steps the supplied build is the approved constant; sql.sh independently measures and enforces the actual executable before the payload. In the tool-negative step the supplied build is extracted from the actual older executable's version output. AssertionError is converted into a nonzero CLI exit with the mismatch text. Other errors, such as unreadable JSON, also fail the process. It does not deploy, inspect a target or provide an independent signing authority.

```python
"""Fail-closed archive/source/tool identity check before native deployment."""
import hashlib
BUILD='25.4.1.022.0618'
def guard(archive,receipt,source,tool):
    assert receipt['source']==source,'source mismatch'
    assert receipt['build']==tool==BUILD,'tool mismatch'
    assert receipt['sha256']==hashlib.sha256(archive.read_bytes()).hexdigest(),'artifact mismatch'

if __name__=='__main__':
    import json,sys
    from pathlib import Path
    try:guard(Path(sys.argv[1]),json.loads(Path(sys.argv[2]).read_text()),sys.argv[3],sys.argv[4])
    except AssertionError as error:raise SystemExit(str(error))
```

## Assert limitation

provenance.py implements its three required comparisons with Python assert. Python -O, -OO, or an effective PYTHONOPTIMIZE setting can remove those assertions. The CLI then loads the receipt and calls guard, but the source/build/archive comparisons are omitted; mismatched evidence can return success. Remaining file/JSON/argument errors may still fail. This is a limitation of the current helper implementation, not optimization-resistant enforcement.

The workflow invokes plain python3 and does not explicitly enforce or clear PYTHONOPTIMIZE. A plain invocation alone is therefore not a general protection against optimization inherited through the environment. The qualified native run exercised all four expected refusal cases successfully, establishing their behavior in that observed execution. It does not prove refusal with optimized Python. check_tool.py and check_output.py use explicit branches and do not have this assertion-removal issue, but they do not replace the skipped provenance comparisons.

A [controlled offline documentation check](tests/workflow-guide-documentation/validation.json) reproduced this behavior using a synthetic archive and mismatched receipt: normal execution returned nonzero; -O, -OO and PYTHONOPTIMIZE=1 returned zero. Both explicit if/SystemExit validators still rejected their invalid synthetic inputs under -O. This probe did not execute Oracle, SQLcl or a GitHub workflow and does not qualify an optimized deployment.

The [test evidence reader](../../tests/native_hosted.py) also uses assert for its verification checks. It reads GitHub run/step metadata and downloads artifacts; it does not dispatch delivery or run native lifecycle commands. Its verification likewise must not be treated as optimization-resistant. Replacing mandatory assertions with explicit exception/exit checks, or enforcing non-optimized execution, would be a separate code change requiring appropriate verification. This documentation request records the limitation and makes no claim that it is fixed.

## Qualification, operation and recovery

The [source review](sprint_E.16_source_review.md#named-actions-correction-source-review) binds tested workflow 03f18caa0ff3f1bd5c1d75e280d5bf038f9996e9, generated release history and qualified bytes to observed target state. [Native run 45810907563](https://github.com/rstyczynski/APEX_CICD_E.16/actions/runs/45810907563) passes all 39 recorded job steps. The [test record](sprint_E.16_tests.md#fresh-named-actions-correction-verification) and [correction acceptance](sprint_E.16_actions_refactor.md#final-verification-and-acceptance) record the six passing gates and their exact source/qualification scope. They are historical execution evidence, not proof for every environment or optimization setting. [Retained raw evidence](tests/actions-refactor/README.md) includes complete native output, receipts, ZIPs and Git bundle with byte-level preservation checks.

Use the manual's dispatch procedure and inspect the first failing named step, not merely whether an artifact uploaded. Preserve its diagnostics and rerun the corrected trusted workflow with fresh disposable services. Later normal steps are skipped after a failure; always-run cleanup/upload still run. Do not replay fixture bootstrap against retained or production databases, use unqualified SQLcl, weaken native error checks or infer target-wide preservation from the single fixture row. If a selected core technology cannot meet an accepted requirement, stop and report the evidenced mismatch to the Product Owner under the standing rule before implementing a substitute.
