# E.3 — Git workflow prototype walkthrough

This is the end-to-end handover entry point. The [presentation](sprint_E.3_increment_demo.pptx)
follows the slide map below. The [operator manual](user_manual.md) owns operating
prerequisites, safe replay and recovery limits. [Implementation](sprint_E.3_implementation.md)
explains corrections; [tests](sprint_E.3_tests.md) identifies actual execution;
[handover](sprint_E.3_handover.md) records delivery and remaining acceptance.
The [accepted design](sprint_E.3_design.md) owns architectural intent.

## Goal and actual starting state — slides 1–3

Follow one visible heading change from an APEX Working Copy through Git review,
automated version/changelog preparation and manual deployment by tag. The live
exercise began with the existing Oracle/APEX/ORDS lab and Main app 810003 in
E1_DEV_C. A new E3_TARGET workspace/schema/application 810203 was provisioned;
retained UAT was not used. SQLcl 25.4.1, Java 21, gh, actionlint and a dedicated
local runner provide the tooling. Hosted PR/version jobs never receive lab
credentials. The prototype supports a single sequential change and one target.

Use a Bash terminal at the parent repository root:

```bash
cd "$(git rev-parse --show-toplevel)"
export E3_LAB_CONFIG="$PWD/.local-apex/e3/lab.json"
code progress/E.3/user_manual.md
```

The normal current replay is deployment of the existing 1.0.1 tag, described in
stage 5. Recreating historical PRs or overwriting the current Main app is not a
hidden fixture step. Stage 1–4 below inspect the performed authoring/integration
journey with its live records, screenshots and source; a new change follows the
manual with a new heading and branch. The prepared source bundle preserves
baseline history; provisioning explicitly refuses existing named resources.

## 1. Working Copy edit and Main checkpoint — slides 4–5

Developer A-01 opened Main 810003 in App Builder, created Working Copy 100 named
“E3 heading patch”, and selected Home's Hero region. Its Name changed from
“Hello World - Working Copy” to “Hello World - Git pipeline”. Save the property,
compare/merge into Main, select only Page Home, leave target backup enabled and
retain the Working Copy. The actual native diff showed one changed page; the [merge observation](tests/working-copy-merge.json) records the performed operation. The earlier narrow captures remain historical evidence; slide 4 uses a later readable inspection.

Inspect [the later inspection of the saved copy](tests/working-copy-inspection.png) and
[the native comparison](tests/working-copy-diff.png). In App Builder the Main
application now has the accepted heading; the Working Copy remains available
for inspection. Its metadata isolation does not isolate database schema changes.
The Main merge is an authoring checkpoint, not a release deployment.
This covers PBI-053.1 and the thin UC-9/10 authoring slice.

## 2. Native source and distribution — slide 6

Native PROJECT exported Main 810003, scoped to the application/business objects,
then staged the reviewed source. These are the executed command interfaces in
the application checkout:

```bash
bash scripts/capture.sh
git diff -- src pipeline.json
python3 scripts/lab.py stage
python3 scripts/lab.py verify
```

The first command now includes the explicitly reviewed pre-stage runtime adapter:
the source inherited an E1_CTRL session hook unavailable in a native disposable
target. Conversion to LAB_RUNTIME.assert_ready occurs before staging and native
verification, not inside the archive afterward. PR 3 records that correction.
Source/runtime rows, credentials and private Working Copies are not conflated.
Both initial and corrected native source/distribution verification reported zero
errors. Slashless demonstration branches avoid the reproduced slash-stage issue.

To inspect the actual reviewable diff without replaying capture:

```bash
gh pr diff 1 --repo rstyczynski/APEX_CICD_E3
gh pr diff 3 --repo rstyczynski/APEX_CICD_E3
```

Look for the intended heading, generated export bookkeeping and explicit runtime
adapter. Database object changes are absent from the heading patch. The baseline
comparison is recorded in pipeline.json, not guessed from current main.

## 3. Classified PR and reviewed integration — slide 7

The developer explicitly opened [PR 1](https://github.com/rstyczynski/APEX_CICD_E3/pull/1)
with label patch and title `fix: update Home heading`. Hosted checks validated
classification, source/shell syntax and workflows. The reviewer inspected the
diff and squash merged with that title. The runtime correction
[PR 3](https://github.com/rstyczynski/APEX_CICD_E3/pull/3) followed the same patch
path. This was sequential role execution by Codex, not independent peer review.

```bash
gh pr view 1 --repo rstyczynski/APEX_CICD_E3
gh pr checks 1 --repo rstyczynski/APEX_CICD_E3
gh pr view 3 --repo rstyczynski/APEX_CICD_E3
```

Expected: merged patch PRs and successful hosted checks. A missing, duplicated
or mismatched change label fails the local/hosted classification check. Minor
maps to feat, major to feat!, and squash messages retain that intent. Release
Please reads those merged messages, not the labels directly. This covers
PBI-053.2 and the thin UC-7/10 integration slice.

## 4. Version PR, changelog and tag — slide 8

Release Please accumulated both fixes into [release PR 2](https://github.com/rstyczynski/APEX_CICD_E3/pull/2),
updating version.txt to 1.0.1, CHANGELOG.md and its manifest. The reviewer explicitly
ran hosted checks on the bot PR's latest head before merging. The workflow then
created [v1.0.1 and its GitHub Release notes](https://github.com/rstyczynski/APEX_CICD_E3/releases/tag/v1.0.1).
Both changelog outputs contain the same two fixes. No deployment resulted from
these merges, the tag or the published GitHub Release.

```bash
gh pr view 2 --repo rstyczynski/APEX_CICD_E3
gh pr diff 2 --repo rstyczynski/APEX_CICD_E3
gh release view v1.0.1 --repo rstyczynski/APEX_CICD_E3
```

Check the [pre-dispatch observation](tests/pre-dispatch.json): application 810203
still had the original heading and preserved fields after change integration.
The earlier first native baseline had a browser-incompatible legacy hook; its
failure and source correction are disclosed, not presented as a working native
runtime gate. The corrected tagged source is the deployment candidate.

## 5. Manual release by selected version — slide 9

Deployer A-03 chose v1.0.1 and manually dispatched the workflow from Git main.
The first run failed before target writes because native PROJECT cannot verify
detached HEAD. Reviewed [PR 4](https://github.com/rstyczynski/APEX_CICD_E3/pull/4)
changed only the workflow checkout to a named local build branch at the exact
selected tag commit. The same v1.0.1 tag was then selected again; tags were not
moved to hide failure. Current workflow revision and selected application version
are separate traceable identities.

If the runner is not already listening, run in a separate parent-root terminal:

```bash
python3 scripts/e3-runner.py run
```

Then, from any authenticated terminal:

```bash
gh workflow run release.yml --repo rstyczynski/APEX_CICD_E3 --ref main -f version_tag=v1.0.1
gh run list --repo rstyczynski/APEX_CICD_E3 --workflow release.yml --limit 3
```

For the actual performed runs:

```bash
gh run view 41664285664 --repo rstyczynski/APEX_CICD_E3
gh run view 41664798289 --repo rstyczynski/APEX_CICD_E3
```

Expect the first failure to remain visible; the second run's actual outcome and
receipt are recorded in the test record. Inspect the downloadable native archive
and receipt from that run. The workflow resolves the tag, verifies accepted
ancestry/version, checks native source/distribution, packages once, deploys that
archive and compares every retained baseline business field. No export from
live DEV occurs during release. Only E3_TARGET/810203 is allowed.

## 6. Application and retained history — slide 10

Open [the E.3 application](http://127.0.0.1:8080/ords/f?p=810203:1), sign in as
LAB_USER with the retained lab credential, and confirm the deployed heading
“Hello World - Git pipeline”. Open Greeting history and inspect the baseline
Hello World greeting. Do not submit another greeting between field-preservation
checks. The receipt records release 1.0.1 separately from APEX source display
version. Actual post-deploy browser captures are linked from the test record.
This covers PBI-053.3, UC-4/11 and retained user behavior from UC-3.

## 7. Inspect the failure gate and remaining risks — slides 11–12

The integration rejection test removes one included native changeset in a
throwaway clone, invokes real PROJECT verification, requires its specific error,
and compares the target before/after. It does not call deploy. Inspect its
[record](tests/rejection.json) and [native output](tests/native-verification-rejection.log).
The failed remote detached-HEAD run independently demonstrates that a required
check failure stops the workflow before deployment. Reconciliation/repair after
committed DDL is outside this slice; do not infer general rollback from these
pre-deploy failures.

The implementation is intentionally small. Genuine parallel development, complete
identity/user-state preservation, ownership fencing, automatic drift protection,
production privileges and general failure recovery remain backlog work. Changes
and release publication do not authorize deployment. User acceptance and sprint
closure are distinct from the executed technical handover; the handover record
states the actual boundary without inferring a decision from silence.
