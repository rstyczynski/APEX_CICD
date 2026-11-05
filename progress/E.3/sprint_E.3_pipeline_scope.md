# E.3 — Simple Git-based development pipeline prototype

## Purpose and status

Prepared on 2026-11-03 from the Product Owner's direction. Subsequently activated
on the same date by explicit request to prepare the design. E.3 closed as Done on 2026-11-05 in
managed mode by explicit Product Owner instruction. The [setup](sprint_E.3_setup.md), [analysis](sprint_E.3_analysis.md)
and [proposed design](sprint_E.3_design.md) record that work; implementation
was subsequently authorized through technical handover by explicit Product
Owner direction. See the [handover](sprint_E.3_handover.md) for actual results;
final acceptance and closure were explicitly granted on 2026-11-05. Its purpose is an understandable,
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
and accepts a squash merge with a patch label and matching `fix:` title for
this heading-only change. Release Please prepares a version/changelog release
PR; its reviewed merge lets the workflow create the version tag and matching
GitHub Release notes. The deployer separately selects that version tag and manually triggers
the release workflow. The workflow builds, checks and
deploys the selected candidate to a named laboratory target. The operator
opens the application and verifies the intended change and retained baseline
history. Record the version tag, resolved source revision, release artifact and
target result.

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
promotion action for an existing version tag, including eligibility, required validation
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
trigger, selected version tag and resolved revision, generated artifact, workflow result and changed
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

## LC-1 — Oracle APEX lifecycle alignment validation

Status: Accepted by the Product Owner on 2026-11-05.

The Product Owner accepted the lifecycle mapping and directed that remaining
gaps become backlog follow-up. This decision replaces the earlier requirement
for a separate LC-1 report and acceptance gate. The accepted outcome is the
bounded E.3 mapping on slides 19–21 of the [deck](sprint_E.3_increment_demo.pptx),
including printed page references, evidence pointers in speaker notes and the
follow-up dispositions below. The [plan](../../PLAN.md) records the decision;
the [test record](sprint_E.3_tests.md) and [handover](sprint_E.3_handover.md)
record its result. No additional LC-1 acceptance is required.

### Accepted mapping

The [Oracle paper](../../refs/apex-lifecycle-management-v3.pdf), pp. 12–14 and
32, maps to E.3's Working Copy comparison and selected Main checkpoint.
Pp. 18–20 and 26–27 map to native PROJECT capture, staging, packaging and
deployment. Pp. 40–44 permit GitHub Actions and on-demand jobs as an adaptation
of the Jenkins examples. E.3 combines shared-Main capture with Git PR review;
it does not demonstrate the full private-instance feature-centric approach on
pp. 32–34. Release Please and deliberate manual promotion are project choices.
The paper's SQLcl 25.1.1 example and E.3's pinned 25.4.1.022.0618 remain distinct.

The [native correction](sprint_E.3_native_correction.md) and
[GitHub configuration correction](sprint_E.3_github_configuration.md) own the
implemented behavior. The [v1.0.4 journey receipt](tests/github-environment-journey.json)
binds retained source and run identities. These are retained observations,
not newly executed runtime experiments. Acceptance establishes alignment of
the demonstrated slice, with explicit limits rather than full production or
paper-wide qualification.

### Backlog dispositions

PL/SQL regression and coverage (paper pp. 22–25, 45) remain owned by
[PBI-040](../../BACKLOG.md#pbi-040-measure-plsql-regression-coverage-with-utplsql).
Automated user journeys remain owned by
[PBI-034](../../BACKLOG.md#pbi-034-automate-application-browser-acceptance-checks).
Quality, performance and security inspection (pp. 30–31, 45) remain owned by
[PBI-041](../../BACKLOG.md#pbi-041-demonstrate-oracle-recommended-application-quality-audits).
Their results feed the broader build/test/deploy outcome in
[PBI-043](../../BACKLOG.md#pbi-043-operate-the-oracle-lifecycle-automation-pipelines).
These existing items retain their acceptance criteria and ordering.

Private APEX branch environments (pp. 32–34, 45) gain the new
[PBI-056](../../BACKLOG.md#pbi-056-provide-isolated-apex-environments-for-git-feature-branches).
It owns repeatable environment preparation, isolation, refresh and retirement;
[PBI-019](../../BACKLOG.md#pbi-019-prove-parallel-component-collaboration-and-integration)
continues to own parallel contribution/integration behavior, and
[PBI-042](../../BACKLOG.md#pbi-042-synchronize-central-development-after-accepted-merges)
continues to own central development synchronization. Their assignments are
unchanged. Optional mini-app subscriptions and navigation (pp. 7, 15–16) remain
owned by [PBI-044](../../BACKLOG.md#pbi-044-demonstrate-native-mini-app-component-reuse).

The observed difference between repository release v1.0.4 and APEX display
metadata 1.0.0 gains new
[PBI-057](../../BACKLOG.md#pbi-057-show-the-deployed-release-identity-in-apex).
This is a project observability gap, not a claim that Oracle mandates our Git
version format. Wider fencing, drift and recovery limits retain their owners
PBI-022–024/045; the prepared-host credential accommodation remains governed by
its existing decision and PBI-025/054. New PBI-056/057 are Proposed and
unscheduled. Acceptance of this mapping does not mark those capabilities
implemented or change another sprint's scope.

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
