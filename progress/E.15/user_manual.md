# E.15 operating reference

The [walkthrough](sprint_E.15_increment_demo.md) is the complete staged journey and presentation map. [PBI-083](../../BACKLOG.md#pbi-083-validate-integrated-github-and-oracle-execution) owns acceptance, [SRS](../../docs/srs.md) owns product requirements, [architecture](../../docs/architecture.md) owns durable design, and the [test report](sprint_E.15_tests.md) owns observations and limits.

## Supported task and prerequisites

Validate a reviewed SQL candidate against a real disposable Oracle database, publish current evidence to its GitHub PR and perform ordinary protected merge. The candidate repository is rstyczynski/APEX_CICD_E.15-candidates; Actions must stay disabled. Trusted execution lives in rstyczynski/APEX_CICD_E.15. The controller is published at tag e15-qualified and mirrored in sprint-work/E.15/controller.py in the progress repository.

The qualified operator uses macOS Bash, Git, Python 3 and authenticated GitHub CLI with administrative access to these disposable sprint repositories. Credentials remain in the normal GitHub CLI credential facility and are never supplied to candidate code. Only the trusted owner has target-repository write access in this experiment; arbitrary additional writers or organization-wide IAM are not qualified. Public contributors need no target write permission to propose changes. The code command must be on PATH for the optional VS Code viewing instructions. No local Oracle installation is required for the hosted journey. The separate full regression uses the prepared laboratory described by the project test profile.

GitHub jobs declare Ubuntu 24.04, the pinned gvenzl Oracle image digest and oracledb 3.4.1. The actual image reports Oracle Free 23.26.4.0.0. The candidate password is fixed public fixture data; generated disposable administrator passwords are redacted from retained logs. No retained laboratory connection, settings file or secret is copied into a job or companion repository. This does not change the prepared-host credential accommodation or qualify a new SQLcl PROJECT release.

## Controller behavior before invocation

The trusted Python controller reads the PR, requires candidate Actions disabled, checks current head/base and allows only candidate.sql in the diff. It downloads trusted Review from the current validator commit and requires the exact approved SQL digest. It publishes pending, dispatches with a random correlation label and waits up to 700 seconds. The GitHub job fetches immutable SQL as data, checks Review and runs actual Oracle assertions. The controller independently checks terminal success, source-specific log provenance and current source/policy again before success publication. Failure, cancellation or mismatch cannot produce success. The workflow's 15-minute job timeout bounds hosted execution separately.

The publish action revalidates an existing receipt against live GitHub state; it is not a way to inject a success claim. The merge action revalidates the receipt and invokes ordinary native merge with --match-head-commit. It never uses --admin. A merged/closed PR cannot be republished through this interface. The optional --pause enables a trusted 60-second inspection interval after Oracle assertions for the controlled cleanup exercise; normal validation does not pause.

## Complete SQL executed by the fixture

The trusted initializer uses OS-authenticated SYSDBA only inside the disposable service. It selects FREEPDB1, creates a real private table and commits the sentinel. SQL errors fail initialization. This is the complete initializer:

```sql
whenever sqlerror exit failure
alter session set container=FREEPDB1;
create table system.e15_private (value varchar2(80));
insert into system.e15_private values ('private sentinel');
commit;
```

The accepted candidate source is exactly:

```sql
select concat('Hello', ' World') from dual
```

The Python validator requires exactly one Hello World row. It also executes these complete queries through the CANDIDATE connection:

```sql
select sys_context('USERENV','SESSION_USER') from dual
```

```sql
select * from system.e15_private
```

The first must return CANDIDATE. The private-table query must fail Oracle ORA-00942 after initialization has proved that the table exists. SQL is submitted through oracledb; it is never executed as runner shell code. Before loading SQL, the validator rejects wrong paths, symlinks, empty input and input over 8192 characters.

## Interface, results and recovery

After staging an open reviewed PR as described in the walkthrough, the qualified commands are `python3 controller.py validate PR receipt.json`, `python3 controller.py publish PR receipt.json` and `python3 controller.py merge PR receipt.json`. Substitute the actual staged numeric PR ID. The receipt directory must exist. The validate command prints its actual correlated run URL and saves the source head/base, trusted commit, report digest and run identity plus a redacted readable log. Success publication occurs only after all checks. Inspect a saved receipt with VS Code using `code receipt.json`; a path or ID by itself is not the verification outcome.

On stale source base, update the branch through GitHub and obtain a new validation; an old receipt is rejected. A changed SQL body requires actual trusted review and an updated trusted report before it can qualify. Do not edit the receipt to claim success. On Oracle failure or cancellation, inspect the actual run, correct the cause and request a fresh validation. The live cleanup exercise proved owned container/network removal and an unaffected peer. Do not cancel another candidate's run. No routine retry changes source or disables mandatory checks.

The harmless candidate-owned dispatch remained zero-job metadata under disabled Actions. GitHub's normal cancel, force-cancel and delete APIs could not remove that never-assigned record. It allocated no runner/container or runtime token. Retain it as evidence and keep Actions disabled; deletion of all CI history is not the active Oracle cleanup claim. The controller requires the disabled state before publication and merge.

## Reproducibility and known limits

The walkthrough includes forward-only fixture preparation and the exact source/validation/merge sequence executed for companion PR 3. Tags e15-baseline and e15-accepted plus retained Git bundles preserve the starting and accepted history. Restoring the literal source fixture is an explicit owner maintenance step, not an ordinary candidate acceptance merge, and administrator enforcement is restored before validation.

This is a bounded Elaboration experiment with a trusted prepared operator. No fully autonomous publisher service, hostile-administrator resistance, general multi-user organization policy, arbitrary-load capacity, clean-host reproduction or native release delivery is claimed. E.16/PBI-084, E.17/PBI-085 and E.18/PBI-086 retain their planned work. [The former blocker audit](sprint_E.15_blockers.md) explains resolved alternatives and the final disposition.
