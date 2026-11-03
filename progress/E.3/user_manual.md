# E.3 operator manual

This operates the small Git/Working Copy architecture prototype in the private
[application repository](https://github.com/rstyczynski/APEX_CICD_E3). Start with
the [presentation walkthrough](sprint_E.3_increment_demo.md), which owns the
end-to-end sequence and evidence. The [design](sprint_E.3_design.md) owns mechanisms;
[implementation](sprint_E.3_implementation.md) records corrections;
[tests](sprint_E.3_tests.md) records actual validation. This is a lab, not a shared
production delivery service.

## Current environment and prerequisites

Run from the parent APEX_CICD checkout. Require Git, authenticated gh with access
to the private example, Python 3, actionlint and the existing Oracle/APEX lab.
`code` must be on PATH for the file-viewing examples. The demo release client is
SQLcl 25.4.1.022.0618 with the retained Java 21 runtime. The older E.1 client is
unchanged. Podman operations use the named apex-cicd connection, not whichever
machine happens to be the global default.

Authoring uses E1_DEV_C / Main application 810003 and retained Working Copy 100,
“E3 heading patch”. Working Copies share the schema. Only the reviewed Home
page was merged, with native backup enabled. Target is the new disposable
E3_TARGET schema/workspace and application 810203. E1_UAT is not a target.
Existing user credentials remain in the private lab store; do not copy passwords
into shell commands, source, screenshots or CI variables. Deployment config is
`.local-apex/e3/lab.json` with mode 0600. The local runner inherits its path;
the runner registration/connection stores remain private.

## Inspect and replay the completed release

From the parent repository:

```bash
cd "$(git rev-parse --show-toplevel)"
export E3_LAB_CONFIG="$PWD/.local-apex/e3/lab.json"
gh pr view 1 --repo rstyczynski/APEX_CICD_E3
gh pr view 2 --repo rstyczynski/APEX_CICD_E3
gh release view v1.0.1 --repo rstyczynski/APEX_CICD_E3
code progress/E.3/sprint_E.3_increment_demo.md
```

The PRs show the patch label/title and generated 1.0.1 version/changelog change.
The release has the two patch entries. Neither publishing it nor opening a PR
deploys. Start the dedicated runner in a separate terminal if it is offline:

```bash
cd "$(git rev-parse --show-toplevel)"
python3 scripts/e3-runner.py run
```

Then explicitly request deployment from Git main, choosing the version tag:

```bash
gh workflow run release.yml --repo rstyczynski/APEX_CICD_E3 --ref main -f version_tag=v1.0.1
gh run list --repo rstyczynski/APEX_CICD_E3 --workflow release.yml --limit 3
```

Use the resulting run ID in `gh run view RUN_ID --repo rstyczynski/APEX_CICD_E3`
and `gh run download RUN_ID --repo rstyczynski/APEX_CICD_E3 --dir DESTINATION`.
RUN_ID and DESTINATION are explicit operator choices; do not reuse a populated
download directory. Inspect the receipt's version tag, resolved commit, target,
archive hash and preservation result. Actual reference run IDs are in
[tests](sprint_E.3_tests.md). A workflow success does not replace the browser check.

Open [the deployed application](http://127.0.0.1:8080/ords/f?p=810203:1), sign in
as LAB_USER using the existing lab credential, and confirm “Hello World - Git
pipeline”. Open Greeting history and inspect the retained greeting. Source APEX
application display version remains independent from the repository release tag;
this prototype reports the selected tag in the release/run receipt.

## A new developer change

Coordinate a single-author checkpoint; preserve any unexported work first.
Create a new Working Copy of 810003 in App Builder, edit one supported page
property, save, compare with Main, review the exact selected page, then merge
with target backup enabled and without deleting the copy. For the executed
example the Home region Name changed from “Hello World - Working Copy” to
“Hello World - Git pipeline”. Do not replay that replacement over unrelated work.

In the application checkout, start a new slashless branch from accepted main,
set pipeline.json's baseline_sha to that accepted base and expected_heading to
the intended visible heading. Create/update local e3-base at that base. Then:

```bash
bash scripts/capture.sh
git diff -- src pipeline.json
git add src pipeline.json
git commit -m "fix: update Home heading"
python3 scripts/lab.py stage
python3 scripts/lab.py verify
git diff -- dist
git add dist
git commit -m "fix: stage reviewed Home heading distribution"
```

Capture uses native export then an explicit pre-stage source adapter replacing
only the legacy E1_CTRL session hook with LAB_RUNTIME.assert_ready in SQL/YAML.
Review it with the heading diff. Do not edit source after stage without restaging
and revalidating. No native verify errors are waived. After review, push the new
branch and open a PR with label patch and title `fix: update Home heading`.
The branch name/heading are new experiment inputs; the performed example and its
actual evidence are in the walkthrough rather than claimed as a new run here.

For minor use label minor/title `feat: ...`; for major use major/title `feat!: ...`.
Missing/multiple labels or a mismatch fails the PR check. Squash merge preserves
the title. The reviewer checks Release Please's generated release PR and manually
dispatches pr.yml with its PR number before merging it. That merge creates the
tag/GitHub Release; the deployer still chooses when to deploy it. Accumulation
into one release and leaving later prepared versions undeployed are supported.

## Provisioning and retention

[Preparation](../../scripts/e3-prepare.py) creates only E3_TARGET and refuses an
existing schema/workspace/application; it does not destroy/rebuild the lab or
silently overwrite a retained experiment. The source bundle under
[the example](../../examples/git-pipeline/) preserves the inspected Git baseline
and history. Runner installation/configuration use `e3-runner.py install` and
`configure`; do not overwrite a retained runner directory or registration.
These provisioning steps are not repeated as part of a normal deployment.
No whole-lab cleanup or automated teardown is provided by E.3.

## Failure handling and limits

An invalid tag, failed native verify, missing mapping or failed SQL operation
stops the run. Inspect logs before retrying. A failure after committed Oracle DDL
requires inspection and a reviewed repair; there is no general rollback promise.
Never change the selected release tag to conceal a failed run. Native verify
requires a named local build branch, which the corrected workflow creates from
the exact selected tag. Both slash-stage and detached-HEAD observations are
retained in the test/implementation records.

This prototype does not qualify parallel team work, full identity preservation,
production privileges, atomic ownership, drift rejection, fencing or recovery.
Those remain existing backlog requirements. Stop the foreground runner with
Control-C when finished; this does not delete the registration or application.
