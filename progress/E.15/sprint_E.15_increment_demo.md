# E.15 end-to-end walkthrough

The increment lets the trusted operator take a real SQL pull request through exact Review, real hosted Oracle Testing and ordinary protected merge. It also exposes stale/cross-candidate evidence, unauthorized publication and interrupted cleanup outcomes. [PBI-083](../../BACKLOG.md#pbi-083-validate-integrated-github-and-oracle-execution) owns acceptance; [checklist](sprint_E.15_checklist.md) maps every criterion, [manual](user_manual.md) owns operating details and [test report](sprint_E.15_tests.md) owns observations. The [editable presentation](sprint_E.15_increment_demo.pptx) follows the slide map below.

## Starting state, goal and variations — slides 1–6

Use one named Bash session, E15-DEMO, with Git, Python 3 and authenticated GitHub CLI. The operator must administer the two disposable sprint repositories. The code command is needed only for optional VS Code views. The qualified host is macOS; a new host/other operator is E.17 work. No local Oracle installation or retained laboratory secret is needed for this hosted journey.

Candidate source/PRs live in rstyczynski/APEX_CICD_E.15-candidates with Actions disabled. Trusted workflow and Review live in rstyczynski/APEX_CICD_E.15. Only the trusted owner has target write access in the configured fixture; no operator credential is provided to candidate code. The default dispatch is an Oracle-only preflight. Companion dispatch adds immutable PR source and mandatory Review. The optional inspection interval is used only for the controlled cleanup exercise. No backend/language variation beyond this declared SQL/Oracle fixture is promised.

The starting literal query and accepted candidate query both return Hello World. The value of this increment is the verified delivery/authority journey, not a new greeting feature. Oracle executes real SQL; no model inference or simulated database result is substituted.

## 1. Acquire the qualified validator and inspect prerequisites — slides 7–8

The clone command retrieves the actual qualified trusted source tag. GitHub CLI checks the active identity and native repository policy. These reads do not grant new access. The clean validator clone and help invocation were executed during finalization. Use a fresh temporary directory so an existing checkout is not overwritten.

```bash
cd "$(git rev-parse --show-toplevel)"
E15_DEMO_ROOT=$(mktemp -d)
git clone --branch e15-qualified https://github.com/rstyczynski/APEX_CICD_E.15.git "$E15_DEMO_ROOT/validator"
git clone https://github.com/rstyczynski/APEX_CICD_E.15-candidates.git "$E15_DEMO_ROOT/candidates"
E15_REPO=rstyczynski/APEX_CICD_E.15-candidates
gh api user --jq .login
gh api repos/rstyczynski/APEX_CICD_E.15-candidates/actions/permissions --jq .enabled
gh api repos/rstyczynski/APEX_CICD_E.15-candidates/branches/main/protection/enforce_admins --jq .enabled
python3 "$E15_DEMO_ROOT/validator/controller.py" --help
```

Expected native policy values are false for candidate Actions and true for administrator enforcement. The recorded active operator is rstyczynski. A different configured account with invalid authentication was not used as an independent actor. The controller help exposes validate, publish and merge plus --pause.

## 2. Prepare a known source fixture — slides 8–9

This is explicit disposable-laboratory preparation, not ordinary candidate acceptance. After a previous accepted run, the owner restores the literal source using a forward-only commit; Git history and accepted commits remain intact. Administrator enforcement is temporarily exempted for this maintenance push, then immediately restored. No candidate is merged through that exemption. Stop on a preparation error and restore administrator enforcement before continuing. The recorded preparation and later ordinary merge are separate evidence.

The complete starting SQL is:

```sql
select 'Hello World' from dual
```

The following operations were exercised during the live replay preparation. They preserve history and modify only the fixture SQL. If the checkout already contains this literal baseline, omit its no-change commit/push and retain enforcement. Tags e15-baseline and e15-accepted plus the [source bundle](tests/candidate-journey.bundle) preserve actual history.

```bash
git -C "$E15_DEMO_ROOT/candidates" switch main
printf '%s\n' "select 'Hello World' from dual" > "$E15_DEMO_ROOT/candidates/candidate.sql"
git -C "$E15_DEMO_ROOT/candidates" add candidate.sql
git -C "$E15_DEMO_ROOT/candidates" commit -m 'test: prepare forward-only literal baseline'
gh api --method DELETE repos/rstyczynski/APEX_CICD_E.15-candidates/branches/main/protection/enforce_admins
git -C "$E15_DEMO_ROOT/candidates" push origin main
gh api --method POST repos/rstyczynski/APEX_CICD_E.15-candidates/branches/main/protection/enforce_admins
```

## 3. Propose and inspect the actual candidate — slides 10–11

A unique branch avoids colliding with retained demonstration branches. The candidate file below is complete and matches the real trusted Review report. The GitHub PR is the actual candidate, not an injected run identity. Creating a PR in this repository does not execute candidate-owned code because Actions is disabled.

```sql
select concat('Hello', ' World') from dual
```

```bash
E15_BRANCH="e15-demo-$(date -u +%Y%m%dT%H%M%SZ)"
git -C "$E15_DEMO_ROOT/candidates" switch -c "$E15_BRANCH"
printf '%s\n' "select concat('Hello', ' World') from dual" > "$E15_DEMO_ROOT/candidates/candidate.sql"
git -C "$E15_DEMO_ROOT/candidates" add candidate.sql
git -C "$E15_DEMO_ROOT/candidates" commit -m 'feat: propose reviewed Oracle greeting'
git -C "$E15_DEMO_ROOT/candidates" push -u origin "$E15_BRANCH"
E15_PR_URL=$(gh pr create --repo rstyczynski/APEX_CICD_E.15-candidates --base main --head "$E15_BRANCH" --title 'Reviewed Oracle candidate' --body 'Requires trusted Review, real Oracle Testing and ordinary protected merge.')
E15_PR="${E15_PR_URL##*/}"
gh pr diff "$E15_PR" --repo rstyczynski/APEX_CICD_E.15-candidates
```

The expected visible diff is the literal query changing to concat with the same result. The actual live replay used companion PR 3; [its exact diff](tests/live-companion-diff.patch) is retained. The trusted Codex reviewer inspected the constant-expression change and its lack of new privileges/data access. The report makes no claim of general application security qualification.

## 4. Validate, inspect intermediate output and publish — slides 6, 11–12

Before invocation, understand the encapsulated code: the controller checks disabled Actions, immutable head/base, allowed paths and exact trusted Review digest. It publishes pending, dispatches with a random correlation, then independently verifies actual successful Oracle execution and current provenance before success publication. SQL is data, never runner shell code. Failed, cancelled, stale or substituted evidence cannot pass. [The complete controller](../../sprint-work/E.15/controller.py) and [trusted workflow](../../sprint-work/E.15/.github/workflows/testing.yml) are retained.

The trusted initializer runs this complete SQL only in the disposable service through OS-authenticated SYSDBA:

```sql
whenever sqlerror exit failure
alter session set container=FREEPDB1;
create table system.e15_private (value varchar2(80));
insert into system.e15_private values ('private sentinel');
commit;
```

The application connection executes the complete candidate query from stage 3 and these complete identity/isolation queries:

```sql
select sys_context('USERENV','SESSION_USER') from dual
```

```sql
select * from system.e15_private
```

The candidate result must be exactly one Hello World row and the effective schema CANDIDATE. Access to the initialized private table must fail ORA-00942. A read-only hosted token's publication attempt must return explicit HTTP 403. All private administrator passwords are disposable and redacted from retained logs.

```bash
python3 "$E15_DEMO_ROOT/validator/controller.py" validate "$E15_PR" "$E15_DEMO_ROOT/receipt.json"
gh pr checks "$E15_PR" --repo rstyczynski/APEX_CICD_E.15-candidates
code "$E15_DEMO_ROOT/receipt.json"
```

VS Code viewing is optional. The visible required result is PASS real Oracle, exact Review and current provenance, an actual run URL, a saved receipt/log and successful TrustedOracle. The receipt binds source head/base, trusted commit, report digest and correlated run. The live replay used run 45787535780 and [this saved receipt](tests/live-companion-receipt.json). That run is completed evidence, not a claim that an already merged PR can be revalidated as open.

## 5. Perform ordinary merge and inspect the result — slide 13

The merge action independently revalidates the receipt, checks current source/policy again and requests native merge with the expected head. It never uses --admin. Native strict protection remains active. The actual command was executed for the live PR; the portable variables above stage a new PR when replaying the journey.

```bash
python3 "$E15_DEMO_ROOT/validator/controller.py" merge "$E15_PR" "$E15_DEMO_ROOT/receipt.json"
gh pr view "$E15_PR" --repo rstyczynski/APEX_CICD_E.15-candidates
```

The live result is [companion PR 3 MERGED](tests/live-companion-merge.json), commit 2d5a94a55fef741f052a061ee06470439624e3e8. Earlier corrected-boundary PR 1 merged at 640bee9f260b52a85a212183fbc1c1938c696473 after recovery. Both are ordinary candidate merges; fixture preparation exemptions are not their acceptance evidence.

## 6. Inspect failures, repairs and safe recovery — slides 14–20

The original same-repository approach let candidate workflow code obtain publication/cancellation authority. Native code-owner approval mitigated merge approval but did not prevent run cancellation. The companion boundary replaced that approach. The self-fork API returned the original non-fork repository, so the explicitly authorized companion is standalone. Candidate dispatch was accepted as zero-job queued metadata under disabled Actions; this was not falsely reported as HTTP refusal. Its never-assigned record remains a documented platform limit, with no runner/container or runtime token allocated.

Actual negative paths and expected visible results are retained: [stale base and native refusal](tests/companion-stale-base-merge.txt), [changed-head receipt refusal](tests/companion-stale-head-controller.txt), [stale Review](tests/companion-stale-report-controller.txt) and [substituted peer-run evidence](tests/companion-cross-evidence-refusal.txt). The latter was attempted against the live candidate and native merge was refused before fresh validation. No negative fixture was merged.

For cleanup, the trusted operator used --pause on two real companion validations. After both services passed actual assertions and entered Inspection interval, A was cancelled. [The simultaneous observation](tests/companion-cleanup-both-live.json), [owned container/network removal](tests/companion-live-oracle-cleanup.log) and [terminal A-cancelled/B-success outcomes](tests/companion-cleanup-final-results.json) prove the exercised cleanup/noninterference case. Cancelled A published failure and native merge was refused; a later fresh validation recovered and merged. The earlier image-download interruption proved only network cleanup and was not substituted for this case.

The YAML parse, report checkout and hosted-checker job-count defects were corrected and rerun. [Defect record](sprint_E.15_bugs.md) and [test report](sprint_E.15_tests.md) distinguish failed attempts, contract checks and real hosted outcomes. A read-only hosted principal's actual companion publication received HTTP 403; the configured target has only the trusted owner as a writer. No hostile administrator or arbitrary future writer qualification is claimed.

## 7. Evidence, limitations and final decision — slides 21–25

All six gates passed: new smoke 1/1, unit 2/2, integration 1/1; full regression smoke 14/14, unit 16/16, integration 24/24. All 253 executable scripts/tests in the full-regression snapshot remain unchanged. The final deck contains 25 editable slides; its package/render audit and slide map must pass before closure. [Audit](sprint_E.15_documentation_audit.md), [handover](sprint_E.15_handover.md) and [closure](sprint_E.15_closure.md) own the recorded final disposition.

This is the assigned Elaboration experiment with one trusted prepared operator and a bounded SQL/Oracle candidate. Production organization-wide IAM, native release delivery, independent clean-host reproduction and capacity measurement are not claimed. PBI-084/E.16, PBI-085/E.17 and PBI-086/E.18 retain their planned work. The Product Owner delegated YOLO execution/closure; no unprovided satisfaction, feedback or milestone decision is invented.

Slide map: scope/architecture 1–6; staged user journey 7–13; original failures, replacement, repairs, freshness and cleanup 14–20; evidence/limits 21–23; outcome/next decision 24; Q&A 25. Earlier 12/14-slide receipts are superseded by the current validated presentation pair.
