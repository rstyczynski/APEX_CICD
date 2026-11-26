# E.15 walkthrough — partial increment, sprint open

The goal is a real GitHub PR through Oracle Testing, trusted Review and ordinary enforced merge, with stale evidence, unauthorized publication, cross-candidate access and interrupted cleanup unable to authorize invalid merge or damage another run. [PBI-083](../../BACKLOG.md#pbi-083-validate-integrated-github-and-oracle-execution) owns acceptance, the [checklist](sprint_E.15_checklist.md) owns current status and the [manual](user_manual.md) explains operation. The [editable presentation](sprint_E.15_increment_demo.pptx) describes the delivered positive journey and unresolved failure; it is not a closure claim.

## 1. Starting state and preflight — slides 1–4

Use a terminal with Git, GitHub CLI, authenticated access to the sprint repository and the code command on PATH for viewing local files. The sanitized repository is public, native branch protection is enabled and PR 4 is already merged. There are no retained production inputs in this fixture. The companion candidate-boundary proposal is not implemented. Full Oracle regression runs separately in the prepared local laboratory.

The following commands position the terminal at the progress repository root, check the active GitHub identity and inspect the actual accepted PR. They read data and do not publish checks or merge anything.

```bash
cd "$(git rev-parse --show-toplevel)"
gh api user --jq .login
gh pr view 4 --repo rstyczynski/APEX_CICD_E.15
```

The active identity used for the recorded owner review is rstyczynski. PR 4 shows MERGED. Do not infer that another configured but invalid CLI account supplied an independent operator. The bot PR author and authenticated owner review are distinct actual GitHub identities; no Product Owner reaction is invented.

## 2. Inspect the accepted change — slides 5–7

This command displays the exact actual diff. The source-only SQL change preserves the single greeting result. Trusted Review binds the exact reviewed file bytes and rejects changes outside candidate.sql; it is not a general-purpose application review engine.

```bash
gh pr diff 4 --repo rstyczynski/APEX_CICD_E.15
```

The complete accepted SQL is:

```sql
select concat('Hello', ' World') from dual
```

The trusted Python validator submits it through oracledb as CANDIDATE, expects exactly one Hello World row, checks SESSION_USER and attempts an unauthorized private-table read. The workflow initializer uses disposable OS-authenticated SYSDBA only to establish that private table first. Its complete SQL is:

```sql
whenever sqlerror exit failure
alter session set container=FREEPDB1;
create table system.e15_private (value varchar2(80));
insert into system.e15_private values ('private sentinel');
commit;
```

SQLPlus stops on initialization errors. The candidate has no grant to that table. The service is unique to a throwaway GitHub-hosted job. The candidate password is a fixed public fixture value; generated disposable administrator passwords are redacted from retained logs. Source, candidate and publisher responsibilities are described in the [design](sprint_E.15_design.md).

PR 4's real Oracle run 45781363137 attempt 2 passed and published the current Integrated result. Required code-owner review and strict base freshness were active. Ordinary merge produced 8ee003ad9f45ae62d5fe0d1a0bb389e311c1b27a without --admin. The [receipt](tests/ordinary-merge.json) and [owner review](tests/owner-review.json) preserve that result. Setup-policy administrator changes are separate from this ordinary merge.

## 3. Run the current Oracle preflight — slides 6–7

The dispatch command invokes trusted main code with a unique correlation label. GitHub initializes the pinned Oracle image, installs the pinned driver, creates the private sentinel and runs the current main SQL. The job's read-only token must receive explicit HTTP 403 when it tries to publish a status. This dispatch is an Oracle preflight, not a PR Review or merge replay; those branches are conditional on a PR event.

```bash
E15_DEMO_CORRELATION="manual-e15-$(date -u +%Y%m%dT%H%M%SZ)"
gh workflow run testing.yml --repo rstyczynski/APEX_CICD_E.15 -f "correlation=$E15_DEMO_CORRELATION"
gh run list --repo rstyczynski/APEX_CICD_E.15 --event workflow_dispatch --limit 5
```

Match the Oracle run title to the emitted correlation string. A queued receipt is not success. Use GitHub's returned run URL or inspect the actual selected run ID; RUN_ID is a substitution, not a preverified example. The current scripted integration test performs that correlation and waits for terminal success automatically. The manual's earlier dispatch form without correlation is superseded by the complete command above.

The [new integration log](tests/new-integration.log) records an independently correlated real run already passed. The [live dispatch receipt](tests/live-oracle-dispatch.txt) records the current demonstration/preflight invocation; run 45782725015 completed successfully, with its actual result and redacted log retained alongside the receipt. The browser is not required for CLI inspection; `code progress/E.15` opens local evidence when the code command is installed.

## 4. Inspect failures and limits — slides 8–11

The first workflow failed YAML parsing; a block scalar repaired it. The first report-bound run lacked review.json because of code checkout selection; trusted github.sha code selection repaired it. These are resolved implementation issues, not external blockers.

The candidate-private sentinel access failed ORA-00942 after real initialization. A read-only publication attempt failed explicit HTTP 403. However, a candidate-owned workflow requesting write permission forged an Integrated check under the same GitHub Actions app. Native code-owner review was then added; an invalid ordinary merge was refused. The [test report](sprint_E.15_tests.md) identifies exactly what each observation proves.

The remaining cross-candidate failure is material: a candidate-owned workflow cancelled another run using repository-wide Actions authority. Separate Oracle containers and a later successful retry do not prevent or erase that interference. The complete [remaining-requirement audit](sprint_E.15_blockers.md) preserves evidence and alternatives. Do not run or merge negative fixtures as an operating step. A harmless comment-only SQL revision separately exercises stale native approval dismissal; its actual review and refusal receipts are in the tests directory.

## 5. Remaining acceptance and decision — slides 12–14

The candidate authority boundary must be corrected and tested. A companion candidate fork with Actions disabled is proposed, subject to the explicit pending scope question and actual GitHub support. No additional repository or app is created on assumed permission. Full head/base/report freshness and interrupted cleanup/noninterference still require complete evidence under the corrected boundary.

The final regression gate, documentation reconciliation, full live integrated demonstration and closure remain governed by the [checklist](sprint_E.15_checklist.md). E.15 stays Progress/YOLO and PBI-083 under construction. The deck has 14 rendered and inspected slides: scope 1–4, ordinary merge 5–7, failures 8–11, remaining acceptance 12–13 and Q&A 14. Package, geometry, fonts and first-party import validation are retained in [the receipt](tests/presentation-validation.json). No native PowerPoint rendering or full handover acceptance is claimed.
