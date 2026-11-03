# E.3 — Native Git pipeline walkthrough

This is the corrected handover: **APEX/SQLcl provide native capabilities;
GitHub Actions controls execution. No Python pipeline or recurring source
adapter remains.** Read alongside the [editable deck](sprint_E.3_increment_demo.pptx),
[manual](user_manual.md), [design](sprint_E.3_design.md) and
[native correction evidence](sprint_E.3_native_correction.md).

## Goal and inherited foundation

E.2 established native Working Copy collaboration, PROJECT capture/staging and
native APEX availability. E.3 adds classified Git review, generated version and
both changelogs, then manual release by a selected tag. This is an Elaboration
architecture prototype, with broader construction work deferred.

The initial E.3 run used the uncorrected E1 authoring definition and a Python
adapter; that was an implementation mistake. On Product Owner correction,
Main's legacy initialization code was cleared **in App Builder**, once, before
native export. The [saved native baseline](tests/native-author-baseline.png)
and corrected source prove the change. No exported source/archive is rewritten.
Native APEX availability is used; business-schema readiness stays in LAB_RUNTIME.

## 1. Working Copy and Main checkpoint

The original performed authoring change remains valid evidence: Working Copy
100, “E3 heading patch”, changed Home's heading to “Hello World - Git pipeline”.
Native comparison showed one changed page, none added or missing. Page 1 was
merged to Main 810003 with a backup; the Working Copy was retained.
Inspect the [native comparison](tests/working-copy-diff.png) and
[readable Working Copy screen](tests/working-copy-inspection.png).

The retained old Working Copies predate the baseline correction. Refresh their
application definition from Main or create a new Working Copy before later work.
Do not merge the old E1 initialization hook back into Main.

## 2. Native capture, review, staging and verification

In the prepared private application checkout, load the operator's SQLcl/Java
paths as described in the [manual](user_manual.md#prepared-laboratory). The
correction was performed on slashless branch e3-native-only. The actual commands
are SQLcl calls, with small SQL files that expose the native operations:

```bash
git branch -f e3-base "$(jq -r .baseline_sha pipeline.json)"
"$SQLCL" -nohistory -noupdates -home "$SQLCL_HOME" -S -L /nolog @sql/capture.sql
git diff -- src
```

Inside `capture.sql`: `connect -name lab-dev-c`, `project export -list`,
`project export`. The native source now has a blank initialization setting;
it contains neither E1_CTRL's controller hook nor an adapter-inserted hook.
Review and commit the source before native staging:

```bash
"$SQLCL" -nohistory -noupdates -home "$SQLCL_HOME" -S -L /nolog @sql/stage.sql
"$SQLCL" -nohistory -noupdates -home "$SQLCL_HOME" -S -L /nolog @sql/verify.sql
git diff -- dist
```

Those files run `project stage -branch-name e3-base` and
`project verify -cbn e3-base -verbose`. The performed correction reported
**Errors: 0, Warnings: 0**. Review/commit the native distribution. Capture does
not transform source; release does not recapture live DEV.

## 3. Manual PR and automated release preparation

[PR6](https://github.com/rstyczynski/APEX_CICD_E3/pull/6) removes the Python implementation:
`fix: use native APEX and SQLcl controlled by GitHub Actions`, label `patch`.
The hosted check passed, the diff was reviewed and the PR was squash merged.
[PR7](https://github.com/rstyczynski/APEX_CICD_E3/pull/7) completes the native baseline and adds native session validation. The PR policy is a small jq metadata expression. It requires one change label
matching `fix:`, `feat:` or `feat!:`; scopes are supported. Application/native
migration code remains SQL. No database credentials reach hosted PR jobs.

Release Please updated [release PR8](https://github.com/rstyczynski/APEX_CICD_E3/pull/8)
for 1.0.3. Its changed files are version.txt, CHANGELOG.md and the Release Please
manifest. Its latest head was checked through the manual hosted PR-check entry
point in [run 41673185644](https://github.com/rstyczynski/APEX_CICD_E3/actions/runs/41673185644).
The reviewer merged the release PR; the version workflow publishes v1.0.3 and
matching GitHub Release notes. PR merge and version publication do not deploy.
Roles were exercised sequentially by Codex, not an independent human reviewer.

## 4. Deployer selects the version

Start the existing official runner with `./run.sh` as shown in the
[manual](user_manual.md#manual-deployment-and-runner). In GitHub Actions choose
**Deploy selected version**, main, **v1.0.3**, then Run workflow. The same
explicit manual selection is available through gh:

```bash
gh workflow run release.yml --repo rstyczynski/APEX_CICD_E3 --ref main -f version_tag=v1.0.3
```

Inspect each workflow step. GitHub Actions checks out control SQL from accepted
main separately from the tagged application. It verifies the selected state
before writes, builds one native archive, records private business fields,
uses native APEX restriction, deploys with PROJECT, reapplies restriction,
compares every field, checks native readiness/heading and publishes availability.
A later step cannot run after an earlier required failure. The receipt binds
tag, source and ZIP hash; full business snapshots remain private.

APEX import can restore source availability during import. Reapplying restriction
does not establish atomic fencing; that broader risk remains deferred. No
custom controller is added to conceal this native boundary.

## 5. Application and rejection evidence

Open [application 810203](http://127.0.0.1:8080/ords/f?p=810203:1), sign in as
LAB_USER with the existing credential, inspect the Home heading and greeting
history. The inherited APEX footer still says 1.0.0; repository versions identify
the pipeline release and do not claim automatic display stamping.

The correction record links the actual deployment run, source/ZIP identity,
browser observation and fresh test results. IT-2 removes one included native
changeset in a disposable clone. Real PROJECT verify must reject it, and the
target snapshot must remain unchanged. No deployment is invoked in that case.

## Slide map and handover boundary

| Slide | Topic |
|---|---|
| 1 | E.3 goal and architecture prototype |
| 2 | Walkthrough agenda |
| 3 | E.2 native foundation and GitHub responsibilities |
| 4 | Retained Working Copy heading change |
| 5 | Native comparison and Main checkpoint |
| 6 | Direct SQLcl capture, stage and verify |
| 7 | PR labels and Conventional Commit titles |
| 8 | Release Please version and both changelogs |
| 9 | Manual selected-tag native deployment |
| 10 | Deployed application and retained history |
| 11 | Baseline correction and remaining native limitations |
| 12 | Assigned outcomes and next acceptance decision |

PBI-053.1/.2/.3 retain their original criteria and SM-1/IT-1/IT-2 tests.
Construction completeness, full fencing/drift/identity coverage and general DDL
recovery remain deferred. The [handover](sprint_E.3_handover.md) records the final
outcome. Product Owner acceptance and sprint closure remain separate.

The native correction initially published 1.0.2. Its workflow passed, but the
browser exposed whitespace left in the initialization field. That version is
historical failed browser evidence. The final 1.0.3 correction clears the field
without inserting editor indentation and adds native APEX_SESSION.CREATE_SESSION
plus DELETE_SESSION before publication. This executes initialization and would
reject that observed failure; it does not replace real authentication/browser
validation. See the [correction record](sprint_E.3_native_correction.md).
