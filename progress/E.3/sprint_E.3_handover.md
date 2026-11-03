# E.3 — Technical handover

Delivered on 3 November 2026 under the Product Owner's instruction to implement
through the end of handover without further questions. The prototype was
executed against real GitHub and Oracle/APEX, with browser verification.
This record does not infer final Product Owner acceptance or sprint closure.

Start with the [end-to-end presentation walkthrough](sprint_E.3_increment_demo.md)
and its [editable deck](sprint_E.3_increment_demo.pptx). The
[operator manual](user_manual.md) explains replay and recovery; the
[implementation](sprint_E.3_implementation.md), [tests](sprint_E.3_tests.md) and
[documentation audit](sprint_E.3_documentation_audit.md) identify evidence and limits.
The [design](sprint_E.3_design.md) is Accepted; [PLAN](../../PLAN.md) retains E.3
as Progress, with the [board](../../PROGRESS_BOARD.md) showing tested outcomes.

## What can now be demonstrated

A developer edits a Working Copy and merges one reviewed page into DEV Main.
Native capture and an explicit pre-stage adapter produce reviewed Git source
and native distribution. The developer opens a classified PR; hosted checks
validate patch/minor/major against the Conventional Commit squash title.
Release Please creates a release PR with version.txt and CHANGELOG.md updates.
Review/merge creates the version tag and matching GitHub Release notes. The
deployer explicitly selects that tag for the separate manual workflow.

The performed change became v1.0.1 in the private
[application repository](https://github.com/rstyczynski/APEX_CICD_E3).
[Successful manual deployment](https://github.com/rstyczynski/APEX_CICD_E3/actions/runs/41664798289)
installed that tagged source in E3_TARGET/810203. The browser showed
“Hello World - Git pipeline”, while every prior business field and the existing
Hello World history row were retained. A missing native changeset was rejected
before deployment with the target unchanged. PR/version/tag events never
triggered a lab deployment.

## Assigned outcomes and evidence

PBI-053.1 is tested: Working Copy 100, one-page native diff, Main merge,
source capture/stage and zero-error native verification. PBI-053.2 is tested:
classified PRs 1/3, reviewed squash integration, generated release PR 2,
version 1.0.1 and both changelog outputs. PBI-053.3 is tested: selected-tag
workflow, real archive/receipt binding, live browser result, preserved fields,
pre-deployment rejection and the reproducible operating record. The parent
PBI-053 is tested against its bounded architecture-prototype criterion.

New smoke passed 1/1, new integration 2/2 and full smoke regression 2/2.
The operator/CI roles were exercised sequentially by Codex; this does not claim
independent human review or a Product Owner-run live session. The known native
branch, mapping, inherited runtime-hook and detached-HEAD failures are retained
with their corrections rather than erased. The first remote failure remains
visible; the unchanged tag succeeded after the workflow-context correction.

## Current state and material limits

The application remains installed and usable at
[the lab endpoint](http://127.0.0.1:8080/ords/f?p=810203:1). The lab's existing
LAB_USER credential applies. No password or business snapshot is in Git/CI
artifacts. The source bundle and source/workflow examples remain in the parent
repository. Private tools, config, runner credentials and raw business snapshots
remain under .local-apex. No OS runner service was installed; the manual explains
starting/stopping its foreground process. Retained UAT and historical E.1/E.2
sprint records are unchanged.

Repository version/tag is v1.0.1; APEX source display-version metadata still
shows 1.0.0. Automatic display stamping was not qualified. Workflow definitions
come from accepted main while application source comes from the selected tag;
the source/run identities are preserved. Release Please's later proposal
[PR 5 for 1.0.2](https://github.com/rstyczynski/APEX_CICD_E3/pull/5) remains
unmerged and undeployed, illustrating that preparation does not force promotion.

Parallelism, complete identity/saved-user-state capture, atomic ownership,
maintenance fencing, automatic live-drift rejection, production privilege
boundaries and general committed-DDL recovery remain existing backlog work.
The prototype's readiness adapter is not full replacement of E.1's protections.
No full Lifecycle Architecture or production-readiness acceptance is claimed.

## Product Owner feedback boundary

The Product Owner approved the label/Conventional Commit design and directed
implementation through handover without further questions. No post-execution
questions, reactions or acceptance decision were supplied during this delivery;
none are invented. The technical journey, checks, operating material and limits
are delivered. E.3 is not automatically closed and no next sprint is activated.
