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

In the prepared private application checkout, use SQLcl on the author's ordinary PATH and the native author profile described
in the [manual](user_manual.md#native-authoring-and-developer-pr). The
correction was performed on slashless branch e3-native-only. The actual commands
are SQLcl calls, with small SQL files that expose the native operations:

```bash
git branch -f e3-base "$(jq -r .baseline_sha pipeline.json)"
sql -nohistory -noupdates -S -L /nolog @sql/capture.sql
git diff -- src
```

Inside `capture.sql`: `connect -name lab-dev-c`, `project export -list`,
`project export`. The native source now has a blank initialization setting;
it contains neither E1_CTRL's controller hook nor an adapter-inserted hook.
Review and commit the source before native staging:

```bash
sql -nohistory -noupdates -S -L /nolog @sql/stage.sql
sql -nohistory -noupdates -S -L /nolog @sql/verify.sql
git diff -- dist
```

Those files run `project stage -branch-name e3-base` and
`project verify -cbn e3-base -verbose`. The performed correction reported
**Errors: 0, Warnings: 0**. Review/commit the native distribution. Capture does
not transform source; release does not recapture live DEV.

## 3. Manual PR and automated release preparation

The original heading PR1 and native-baseline corrections PRs6/7 remain historical
source evidence. The current configuration correction is
[PR9](https://github.com/rstyczynski/APEX_CICD_E3/pull/9), title
`fix: configure native workflows through GitHub environments`, label patch.
Its hosted checks passed; the reviewed diff was squash merged. The policy
requires exactly one patch/minor/major label matching its Conventional Commit
squash title. Hosted PR jobs receive no database credentials.

Release Please prepared
[release PR10](https://github.com/rstyczynski/APEX_CICD_E3/pull/10) for 1.0.4.
Only version.txt, CHANGELOG.md and its manifest changed in that release PR.
Its latest head passed the manually dispatched
[hosted check 41676987381](https://github.com/rstyczynski/APEX_CICD_E3/actions/runs/41676987381).
Merging it published v1.0.4 and matching GitHub Release notes. None of these
events deploys. Roles were exercised sequentially by Codex under the Product
Owner's instruction; independent human review is not claimed.

## 4. GitHub configuration and explicit setup

The GitHub **e3-lab** environment is the configuration authority: eight nonsecret
variables and two database-password secrets, restricted to main. The
[configuration guide](sprint_E.3_github_configuration.md) records the correction
requested after the native.env discussion. The old file and E.3 lab.json were
removed; the runner registration moved outside disposable scratch.

The workflow runs the shared setup-native action: actions/setup-java selects
Java 21; pinned SQLcl is downloaded and checksum verified, then added to
GITHUB_PATH. GitHub inputs generate new private connections/mappings under
RUNNER_TEMP. Output paths feed later steps through GITHUB_ENV. Always-run cleanup
removes private material. No runner-inherited tool paths or saved connection
files are read. The manual contains the complete configuration matrix.

## 5. Deployer selects the version

The lab operator uses the versioned [runner launcher](../../scripts/e3-runner.sh)
in the parent lab repository. On a new macOS ARM64 host, with authenticated `gh`,
the documented command dependencies and the existing Oracle/APEX/ORDS lab ready,
run this sequence from the repository root (presentation slide 4):

```bash
./scripts/e3-runner.sh setup  # Once per host: install and register with GitHub
./scripts/e3-runner.sh        # Each lab session: start the foreground listener
```

Setup downloads and checksum-verifies the official GitHub runner, registers it
using a short-lived token, and checks Oracle/ORDS access. It retains a matching
existing registration. Expect **Setup complete**; setup alone does not start the
listener. The second command must reach **Listening for Jobs**. Keep that terminal
open and perform the dispatch below in another authenticated terminal or GitHub's
UI; stop the listener with Control-C after the lab session. The default persistent
installation is `~/actions-runner-e3`, outside the checkout. Setup does not provision
the database/APEX lab; workflow steps prepare Java, SQLcl and temporary connections.
If registration or connectivity fails, correct the reported prerequisite before
dispatching. See the [manual](user_manual.md#runner-infrastructure-and-workflow-setup)
for dependencies and options, and the [implementation record](sprint_E.3_implementation.md#current-runner-installation-and-launch)
for setup behavior. Once the local runner is online, the deployer only selects
the tag. In GitHub Actions choose
**Deploy selected version**, main, **v1.0.4**, then Run workflow. The same
explicit manual selection is available through gh:

```bash
gh workflow run release.yml --repo rstyczynski/APEX_CICD_E3 --ref main -f version_tag=v1.0.4
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

## 6. Application and rejection evidence

Open [application 810203](http://127.0.0.1:8080/ords/f?p=810203:1), sign in as
LAB_USER with the existing credential, inspect the Home heading and greeting
history. The inherited APEX footer still says 1.0.0; repository versions identify
the pipeline release and do not claim automatic display stamping.

The latest [GitHub setup record](sprint_E.3_github_configuration.md) links the actual deployment run, source/ZIP identity,
browser observation and fresh test results. IT-2 now uses a separately manual qualification workflow with the same explicit
setup. It first verifies valid source, then removes an included native changeset
in the temporary checkout. PROJECT must reject it and the private target snapshot
must remain unchanged; the workflow contains no deployment command. Parent tests
read fresh GitHub evidence, not a retained local source/data snapshot.

## Slide map and handover boundary

| Slide | Topic |
|---|---|
| 1 | E.3 goal and architecture prototype |
| 2 | Walkthrough agenda |
| 3 | E.2 native foundation and GitHub responsibilities |
| 4 | GitHub configuration and generated job setup |
| 5 | Retained Working Copy heading change |
| 6 | Native comparison and Main checkpoint |
| 7 | Direct SQLcl capture, stage and verify |
| 8 | PR labels and Conventional Commit titles |
| 9 | Release Please version and both changelogs |
| 10 | Manual selected-tag native deployment |
| 11 | Deployed application and retained history |
| 12 | Baseline/configuration corrections and native limits |
| 13 | Assigned outcomes and next acceptance decision |

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
