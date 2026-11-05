# E.3 — Analysis

Status: Complete. The approved prototype has since been executed; actual results
are recorded in [tests](sprint_E.3_tests.md) and [handover](sprint_E.3_handover.md).

The [setup](sprint_E.3_setup.md) owns the execution contract;
[scope](sprint_E.3_pipeline_scope.md) owns the bounded iteration goal;
[design](sprint_E.3_design.md) owns proposed mechanisms and tests.
[PLAN](../../PLAN.md) assigns PBI-053 and [SRS](../../docs/srs.md) owns wider
product requirements. This analysis does not complete that PBI.

## Actors and observable goals

Use existing SRS actors: A-01 Developer saves a small Working Copy change as
reviewable Git source; A-02 Reviewer accepts the intended change; A-03 Deployer
chooses which accepted version tag to release and when; A-04 Lab user sees the change and
retained greeting history; A-05 Git hosting service records PR/check/run results.
The runner and SQLcl are internal implementation components, not extra actors.
One person may demonstrate multiple human roles sequentially.

## PBI-053 — Requirement and use-case analysis

The prototype covers a thin slice of UC-9/10 (author/capture/submit), UC-7
(review/integrate), UC-4 (release) and UC-11 (verify). It does not prove their
complete SRS acceptance. Preconditions are an accepted source baseline, a
prepared author application and disposable release target, Git access, a
qualified pinned client and a runner able to reach that target.

The trigger is one request to change the Home heading. The developer creates
a Working Copy, edits the heading, compares it with APEX Main and selectively
merges it into that development application.

Capture agreed Main through PROJECT into a Git feature branch, review source
and generated distribution, then commit/push and manually open a PR.

The change PR carries exactly one patch/minor/major label and a matching
Conventional Commit title. For this heading correction use `patch` and
`fix: update Home heading`. A PR check rejects missing, conflicting or mismatched
classification. The reviewer checks the diff and results, then squash merges
using that title as the commit message.

A GitHub workflow runs Release Please on main to propose version.txt and
CHANGELOG.md from Conventional Commit history. It no longer creates the tag
or publishes the release automatically. After the reviewer merges that version
proposal, the operator performs native project release on main, reviews and
commits the numbered distribution/metadata, then tags/publishes that accepted
commit with matching changelog notes. Several change PRs may accumulate before
that decision. Deployment consumes the selected version and never assigns it.

The deployer explicitly selects the version tag and manually triggers a different
release workflow. It resolves that tag to its accepted commit, verifies and
packages that exact Git state under the selected version, deploys the archive
and checks behavior/history. Creating the version tag does not trigger deployment.

Success leaves traceable change/release PRs, version.txt, CHANGELOG.md, matching
GitHub Release notes, version tag, resolved native-release commit, artifact
identity and target result.

APEX Main is an authoring/capture checkpoint; Git main is release integration
authority. Native merging before the PR changes DEV, not the release target.
If the PR is rejected, preserve the Git branch and reconcile/revert that DEV
checkpoint before starting another capture. The sequential prototype requires
no other author to edit Main during capture. It makes no concurrent isolation claim.

If PR checks fail, the developer corrects the branch and repeats them. If native
verification fails, release stops before deployment. If deployment fails after
Oracle commits, report failure and retain observations; do not promise rollback
or automatic retry/repair. PR opening, updating and merging do not trigger release.

## Prior evidence and compatibility

[E.2's accepted assessment](../E.2/sprint_E.2_handover.md) demonstrated Working
Copy comparison/refresh/merge and agreed Main capture. It did not demonstrate
a qualified direct-copy-to-release path; choosing that path would add an
identity/capture experiment before the core pipeline. Reuse the demonstrated
checkpoint for this simplest journey, rather than infer equivalence.

[The clean verification comparison](../E.2/tests/project-verify-fix-validation.json)
records SQLcl 25.4.1.022.0618 succeeding with consistent native source/staging.
It does not certify retained F archives or an E.3 release. Rebuild and verify
E.3 inputs with that pinned client. Do not reuse the F source edits after stage.
Mapped component IDs and saved-report preservation remain broader qualification
work. An application heading change avoids new database migration semantics;
the established database definitions are still part of the baseline.

## Requirements reconciliation

Ordinary Working Copy authoring intentionally differs from the SRS/E.1
break-glass-only policy. Propose an E.3-only authoring policy for the lab; Git
review remains authoritative for releases. Manual native Main merge is a
prototype authoring checkpoint, not proof of fully automated FR-13 operations.
Atomic reservations, complete fencing/drift admission and reviewed recovery
remain deferred requirements. Record their absence rather than claim FR-8/9/10
or FR-13 is fully satisfied. The design requests these bounded dispositions.

## Feasibility and remaining risks

At the analysis baseline, feasibility was supported by documented APIs and
bounded E.2 evidence; end-to-end execution was then unrun. Complexity is moderate because runner connectivity,
PROJECT Git/staging behavior and a consistent baseline need proof; the visible
journey itself is small. Installed actionlint/act/Podman and the pinned SQLcl
client were located; runner/database connectivity was still to be verified
at that stage. Subsequent execution and limitations are recorded in the tests.

The principal risks are capturing unrelated DEV changes, source/dist mismatch,
branch-name handling, schema/app mapping and dispatching a stale/unaccepted
revision. Use a single-author checkpoint, reviewed staged files, explicit base
version tag and resolved commit identities, and one fixed disposable target. Existing 25.3 tooling
remains separate. Stop on an unsupported command or unexpected state instead
of implementing a second migration controller.

The [design](sprint_E.3_design.md) was accepted and implemented under the Product
Owner's explicit instruction. [Implementation](sprint_E.3_implementation.md) and
[test evidence](sprint_E.3_tests.md) now establish the bounded runtime result;
this does not establish the wider production architecture.

## PBI-058 — Native release correction, 2026-11-05

The Product Owner explicitly reopened E.3, assigned PBI-058 and directed implementation through completion without further approval pauses. This direction supersedes the earlier closure for this correction; prior runtime evidence remains historical. The supplied [Oracle lifecycle paper](../../refs/apex-lifecycle-management-v3.pdf), Version 3.2, June 2025, is the authoritative lifecycle reference for E.3. [PLAN](../../PLAN.md) owns the reopened sprint, [BACKLOG](../../BACKLOG.md#pbi-058-fix-e3-omission-of-native-sqlcl-project-release) owns the defect and the [correction record](sprint_E.3_release_correction.md) owns current execution evidence.

The defect is omission of native project release, not absence of a ZIP. Paper p.26 requires project release on main after the milestone merge, moving the next distribution into a versioned release directory. P.27 commits that change before optional tagging and artifact generation. Existing E.3 instead published a Git tag and packaged the next distribution; the final LC-1 mapping failed to disclose this deviation. Release Please's version calculation does not perform native distribution release preparation.

Preserve Release Please as a version/changelog proposal service, disable its automatic tag/publication, and perform native release on main after the version PR merge. Review and commit native changes before tagging/publishing. Deployment must reject tags whose native lastReleaseVersion differs from version.txt or whose versioned distribution is missing. No live DEV export is added to deployment. The approved SQLcl release/build remains 25.4.1.022.0618 with Java 21; project metadata must match before any native operation.
