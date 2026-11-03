# E.3 — Simple Git-based development pipeline prototype

## Purpose and status

Prepared on 2026-11-03 from the Product Owner's direction. Subsequently activated
on the same date by explicit request to prepare the design. E.3 is Progress in
managed mode. The [setup](sprint_E.3_setup.md), [analysis](sprint_E.3_analysis.md)
and [proposed design](sprint_E.3_design.md) record that work; implementation
approval remains pending. Its purpose is an understandable,
executable architecture prototype of the happy path, rather than a complete
delivery solution.

The [plan](../../PLAN.md) owns assignments and status; the
[backlog](../../BACKLOG.md#pbi-053-prove-a-simple-git-based-development-to-release-journey)
defines PBI-053; the [progress board](../../PROGRESS_BOARD.md) tracks its state.
The [README](../../README.md) and [roadmap](../../ROADMAP.md) provide orientation.
The [SRS](../../docs/srs.md) owns product requirements, the
[architecture](../../docs/architecture.md) owns architectural decisions and the
[test profile](../../docs/test-profile.md) owns verification commands. Analysis
must reconcile affected requirements and policies before design approval.

This scope replaces E.3's earlier full native-team exercise in the
[19 October planning record](sprint_E.3_proposedchanges.md). That record is
retained as prior planning context. Its complete paper-coverage, comparison and
quality-suite obligations are not E.3 prototype exit criteria. Applicable
Oracle operations still need accurate version-specific source support.

## Actor journey

The developer makes one small, visible change in an APEX Working Copy, captures
the intended change as reviewable source in a Git feature branch, commits and
pushes it, and manually opens a pull request. The reviewer inspects the change
and accepts its merge. The deployer separately selects the accepted revision
and manually triggers the release workflow. The workflow builds, checks and
deploys the selected candidate to a named laboratory target. The operator
opens the application and verifies the intended change and retained baseline
history. Record the source revision, release artifact and target result.

Use the existing greeting application, lab and native tooling where suitable.
One developer change, one PR and one target are enough for the prototype.
Sequential role demonstration is sufficient; genuine parallel collaboration
is not claimed. Keep explicit manual steps visible and explainable.

## Questions for analysis and design

Establish the simplest supported Working Copy-to-Git capture path. E.2 proved
agreed APEX Main checkpoints, not a qualified direct private-copy release path.
Choose and explain direct capture or a coordinated Main checkpoint using the
prior evidence and a focused experiment if necessary. Distinguish APEX Main
from Git main, explain identities and dependencies, and prevent unreviewed
Working Copy changes from silently becoming the release source. Working Copies
do not isolate database schema changes.

Keep PR validation separate from release/deployment. A PR may run proportionate
checks, but opening, updating or merging it must not itself deploy to the
release target. Manual release selection is the E.3 baseline. During design,
describe a small future automation option, such as an explicitly approved
release tag or promotion action, including eligibility, required validation
and target selection. Explain how several accepted PRs could form one release.
Do not implement a release policy engine or automatic deployment for every PR.

Select the smallest runner and native command sequence that demonstrates the
real journey. Reuse existing scripts where they simplify it. Do not carry
forward Jenkins, hosted runners, private branch instances or a custom controller
as mandatory choices from the old plan. Confirm runner-to-lab connectivity,
credential handling and tool versions before promising execution. Keep one
migration authority and build from the selected accepted Git revision.

Use [E.1's assessment](../E.1/sprint_E.1_assessment.md),
[E.2's decision brief](../E.2/sprint_E.2_handover.md),
[gap analysis](../E.2/oracle-gap-analysis.md) and
[walkthrough](../E.2/cicd-walkthrough.md) as knowledge and evidence, with their
dates, versions and limitations. E.2 acceptance remains separate. Its retained
release-verification failure, source/distribution inconsistency and mapped
identity findings must inform the chosen narrow path; they are not waived by
calling the result a prototype.

## Demonstration and acceptance boundary

Demonstrate the complete actor journey live with one small compatible change.
Show the source diff, manually opened PR, accepted merge, explicit release
trigger, selected revision, generated artifact, workflow result and changed
application. Confirm a PR alone leaves the release target unchanged and that
the release workflow stops when its required command/check fails. Verify the
selected baseline history remains present. This is focused prototype evidence,
not a comprehensive negative-test programme.

Analysis/design must define exact commands, supported starting state, small
checks, expected observations and any needed sprint children before prototype
construction. Include only checks needed to trust this slice. Produce a short
architecture explanation, reproducible walkthrough and list of remaining risks;
apply the normal managed design and handover decisions. Do not count E.1/E.2
historical runs as new E.3 execution.

## Deferred work and later iterations

The former E.3 assignments PBI-036/037/035/039/040/034/041/027/038/021/029/045/
044/043/047 retain their full backlog definitions and return to unscheduled
work. The prototype contributes knowledge to them without claiming their full
acceptance. Schedule completion in Construction, or a bounded later Elaboration
experiment when an identified architectural risk justifies it.

Parallel development, contention/conflict matrices, complete capture/adoption
coverage, central DEV synchronization protections, extensive browser and
coverage suites, audits, mini-app reuse, broad drift/fencing/recovery and full
three-approach comparisons are not required to finish this prototype. Keep
known limitations visible; do not claim these capabilities have been delivered.

[E.4's existing scope](../E.4/sprint_E.4_proposedchanges.md) needs refinement
against E.3 evidence before activation; E.3 no longer promises its former
complete native release/test foundation. This preparation does not activate or
implement E.4, move its items to E.3, or create a Construction sprint.
The [E.5 upgrade scope](../E.5/sprint_E.5_proposedchanges.md) remains separate and
requires its stated toolchain entry gate. Further Elaboration should be driven
by remaining risks rather than completion of every delivery capability.
