# E.15 operating reference — work in progress

[Setup](sprint_E.15_setup.md) owns scope, [design](sprint_E.15_design.md) owns the trusted/candidate split and [checklist](sprint_E.15_checklist.md) owns acceptance status. The [walkthrough](sprint_E.15_increment_demo.md) is the demonstration entry point.

The supported current task is a disposable GitHub-hosted Oracle greeting assertion. It requires GitHub CLI authenticated to the sprint repository, enabled Actions and a hosted Linux runner. The workflow downloads Oracle Free and installs the pinned Python Oracle driver. Application credentials are deliberately disposable fixture values, not retained laboratory credentials. Each run initializes its own database; no retained application or data is deployed.

The workflow uses trusted base-owned Python and only the candidate SQL file from the event head. It executes that SQL through the application schema, expects exactly one Hello World row and checks the effective schema. Later workflow revision 1a68f4d creates a real private sentinel before the candidate checks it cannot read that table. SQL errors fail the job. Job timeout is 15 minutes; superseding a PR run cancels only that PR's concurrency group. Hosted cleanup behavior remains to be challenged before claiming acceptance.

To inspect rather than execute, use `gh run list --repo rstyczynski/APEX_CICD_E.15` and `gh pr view 1 --repo rstyczynski/APEX_CICD_E.15`. To rehearse the trusted main fixture, dispatch `gh workflow run testing.yml --repo rstyczynski/APEX_CICD_E.15`. A dispatch receipt is not proof the run passed. Inspect its steps and conclusion with `gh run view RUN_ID --repo rstyczynski/APEX_CICD_E.15 --log`; substitute the actual emitted run ID.

Recovery is to inspect the failed step, fix trusted code on main if necessary, and start a fresh run. Do not merge a candidate based on a dispatch result or an obsolete PR run. The private repository cannot currently enforce ordinary branch protection on this account. No enforced merge capability is claimed. Never use `--admin` to replace the ordinary merge acceptance exercise.

## Initializer SQL explained

The trusted workflow executes the following complete SQL through the disposable container's operating-system SYSDBA authentication. It switches from root to FREEPDB1, creates the private table and commits a sentinel before candidate execution. The application user has no grants on this object. Any SQL failure makes SQLPlus return failure and stops the job. This initializer affects only that run's throwaway database.

```sql
whenever sqlerror exit failure
alter session set container=FREEPDB1;
create table system.e15_private (value varchar2(80));
insert into system.e15_private values ('private sentinel');
commit;
```

The reviewed candidate B SQL is complete below. The validator expects exactly its single greeting result and checks SESSION_USER=CANDIDATE. A trusted base report contains the SHA-256 of these exact bytes; any other candidate SQL requires new review.

```sql
select concat('Hello', ' World') from dual
```

The rejected PR 3 uses this complete SQL. It receives Oracle ORA-00942 because the initialized private table has no candidate grant. That database refusal is demonstrated independently from hosted merge controls.

```sql
select value from system.e15_private
```
