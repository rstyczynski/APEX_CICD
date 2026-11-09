# E.4 — Contract and analysis

## Contract

The Product Owner selected only [PBI-042 and PBI-060](../../BACKLOG.md), excluded
PBI-056 and classified the other suggested additions as Construction work.
On 2026-11-09 the Product Owner accepted and closed E.3 and authorized E.4.
[PLAN](../../PLAN.md) owns assignment/status; [the board](../../PROGRESS_BOARD.md)
owns execution tracking. Managed mode, Test: smoke, integration; Regression:
smoke. This is an Elaboration experiment. External review was completed for the
superseded sequential design. The Product Owner selected independent parallel work
and the announced-release participation flow below, waived another design review,
then approved implementation through handover preparation on 2026-11-09. The
[approved handoff](sprint_E.4_implementation_handoff.md) requires a new dedicated
Astra handover review after implementation and test evidence exist.

The manager, contractor, analyst, designer and test-architecture procedures are
applied with the local patch and Product Owner preferences. The manager's combined
setup record replaces separate contract/analysis summaries. Native SQLcl and
APEX perform capture, staging, release and installation; GitHub provides source
review and visible run evidence. No independent reservation service, private
branch provisioning, production hardening or new test framework is selected.
The explicit approval satisfies the local P8 construction gate. Token usage is not available per phase.

Use GitHub variables/secrets for workflow configuration; generate connections
in RUNNER_TEMP and clean them. Do not create authoritative scratch settings or
expand the prepared-host credential exception. Preserve unrelated working edits.
The review checkpoint may include the existing PBI-060 definition as necessary
review context, without claiming completion or changing its acceptance criterion.

## Analysis

### System boundary and actors

A-01 developers A/B/C independently author and test changes, preserve their feature
branches and choose whether to submit to an announced release. A-02 performs the
Release Manager/integrator responsibility: creates the candidate branch from current
accepted main, announces it, reviews submitted PRs, admits or defers contributions,
and validates the selected combination. A-03 explicitly synchronizes central DEV;
A-04 inspects visible behavior and retained history. A-05 GitHub hosts branches,
release-planning records, PRs and checks. These are responsibilities within the
[SRS actor model](../../docs/srs.md#actors), not additional infrastructure actors.
The bounded journey covers UC-10/7/4/11; it does not complete UC-8/9 onboarding or
FR-8's full atomic reservation contract.

### PBI-060 analysis

Developers work independently in parallel on their feature branches and separate
prepared author fixtures. They do not need a release branch name to begin authoring,
exporting or staging. Each records the accepted main commit from which their own
work started. In the controlled A/B/C demonstration the three start from one common
accepted commit to make independent deltas easy to inspect; this is a fixture choice,
not a rule that constrains when the Release Manager can create a release branch.

Later, the Release Manager creates the next release branch from then-current accepted
main and shares its name with the team. That starting commit can be newer than the
developer starting commits. Git records ancestry; the Release Manager need not locate
or reuse a particular developer's old starting commit. The release baseline is all
accepted content already in main at branch creation, not an empty container for A/C.
The manager records that actual branch-point revision for release provenance.

Developers decide whether their change is ready and whether to join this release.
Those opting in submit a PR whose head is their feature branch and whose base is
the announced release branch. Not submitting to this release is a valid deferral,
not a review failure. The Release Manager then makes a separate admission decision
from source/distribution review, check results and dependencies. A submitted change
can still require correction or be deferred; opting in does not guarantee inclusion.

For the selected scenario, A and C opt in and are admitted. B chooses to wait for a
later release, preserving its independently captured/staged work without merging it
into this release branch or main. A/C's combined source and native distribution are
validated before publication and central DEV synchronization. Later B can opt into
a newly announced release and update/revalidate against its actual target branch.
The complete PBI-019 ownership/contention contract remains outside this assignment.

Three fixed author fixtures are an experiment prerequisite, not implementation of
PBI-056's branch-environment service. Their native identity/source-path equivalence
and host capacity remain to be qualified. A shared author Main capture or serial
reset cannot replace independent work. Missing fixtures block execution rather than
justify serialized development. Source/snapshot/changelog conflicts during integration
are the principal native risk; a successful text merge alone cannot qualify a release.

The Product Owner approved aligning PBI-060 to the selected A/C-now, B-later
scenario. The root criterion now preserves three independent staged contributions
and requires selected A/C delivery with B excluded and retained.

### Actor-led release participation journey

Trigger: developers have changes in progress or ready for delivery, and the Release
Manager decides to assemble the next release. Preconditions are accepted main and
independent developer source/fixtures. The announcement may happen after work starts;
no prior release target is required for development. Observable success is an accepted
release with the participating A/C changes, no deferred B change, and B's work intact.

1. Developers independently edit, test, export and stage on their feature branches.
They record source bases, heads and native evidence without waiting for other PRs.
2. The Release Manager creates the candidate branch from current accepted main and
records its actual starting SHA. It need not equal any developer's starting SHA.
3. The manager shares the branch name, intended release and submission expectations
in a GitHub release-planning issue. A sprint can organize the timing, but GitHub does
not infer a PR target from sprint membership.
4. Each developer elects to join or wait. A/C opt in; B records deferral in the planning
record and keeps working independently. A/C submit PRs to the announced branch.
5. The manager reviews each submitted PR and its checks/dependencies, requests corrections
where needed and merges admitted changes into the release branch. B has no admission
PR for this release. Source changes after review require fresh candidate validation.
6. Resolve A/C integration conflicts against the release branch's current state, retaining
independent original provenance. Validate its inherited main baseline plus selected A/C;
require B's deferred change to be absent from source, distribution and application behavior.
7. Review/promote the candidate through the selected native release sequence, then let
the operator explicitly synchronize central DEV and verify behavior/data preservation.
8. For a later release announcement, B decides again whether to participate, updates its
branch/fixture as necessary, submits a PR to the new candidate and obtains fresh review.

Alternative outcomes: a developer does not opt in; a submitted PR is not ready; an
admitted change depends on deferred work; main or the candidate advances; or native
combined verification fails. Keep unadmitted work intact and report the reason. Do
not include B through a whole-application export, blindly pull newer main into a frozen
candidate, or treat an old successful check as evidence for changed bytes. A release
must not wait for a nonparticipant to finish. Postconditions and checks are specified
in the [design/test specification](sprint_E.4_design.md#test-specification).

### Authoritative DevOps references and project policy

[GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
supports independent feature branches, review through PRs and checks before merging.
Its published flow merges to the default branch. It supports the underlying collaboration
practice, but does not prescribe our developer opt-in announcement or release-selection
policy. This project deliberately adds a release-candidate integration branch.

[GitHub: Creating a pull request](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-a-pull-request)
documents choosing the PR base and head. This directly supports submitting an existing
feature branch to a release branch announced later; the branch from which development
started need not be the PR destination.
[GitHub: Keeping a PR in sync](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/keeping-your-pull-request-in-sync-with-the-base-branch)
documents updating from the target branch and resolving conflicts to check compatibility
before merging. Our native source/distribution revalidation builds on that mechanism.

[Microsoft: Adopt a Git branching strategy](https://learn.microsoft.com/en-us/azure/devops/repos/git/git-branching-guidance?view=azure-devops)
documents feature isolation, PR review and release branches created from main near a
release milestone to coordinate stabilization. Microsoft's detailed flow usually
integrates features into main first and ports fixes between branches; it is not an
exact prescription of our direct feature-to-release selection. The selected workflow
is an explicit project adaptation using documented industry mechanisms, not a claim
that one formal DevOps standard mandates developer opt-in or this exact branch model.
References were checked on 2026-11-09. The [design](sprint_E.4_design.md) turns this
analysis into the proposed native/GitHub experiment; no runtime success follows from
reading these sources.

### PBI-042 analysis

Central DEV is the separate prepared release target, distinct from all three
independent author fixtures. An accepted revision must update that target while preserving
uncaptured target edits and refusing an older candidate after a newer revision
is selected/applied. Native PROJECT verify checks project structure; it does not
establish absence of target drift. Use native APEX checksum observations and an
explicit operator admission decision under a coordinated no-edit interval.
This validates the safe procedure, not an unattended race-proof enforcement service.

### Compatibility and feasibility

Reuse E.3's corrected local bundle and qualified native lifecycle. Its historical
remote seed can differ. The [E.3 correction](../E.3/sprint_E.3_release_correction.md)
records SQLcl 25.4.1.022.0618 / project 25.4.1.0 / Java 21 and APEX 24.2.
Before native writes compare the actual selected checkout metadata and executable
release/build. Never change the metadata to bypass the native version check.

The retained E3_TARGET upgrade/repeat path is qualified; independent initial
installation failed ORA-20860 and is excluded. Existing author/target mappings,
permissions and current baselines must be checked before execution. Do not
promise successful reuse based solely on old receipts. Design feasibility is
supported by documented interfaces and E.3 evidence; E.4 runtime results are now recorded in [the implementation](sprint_E.4_implementation.md)
and [tests](sprint_E.4_tests.md). The [design](sprint_E.4_design.md) specifies the experiment and stop rules.

## Readiness

The intended scenario is clear. The independent fixtures and native reconciliation were qualified during the
approved execution; see the implementation and test records. New replay still
requires the stated identity/toolchain/access preflight.
Design is Accepted for mandatory parallel independence. Construction starts with
read-only host/toolchain/fixture qualification; unavailable prerequisites remain
blockers, and approval does not establish native feasibility.
