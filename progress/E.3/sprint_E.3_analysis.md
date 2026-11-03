# E.3 — Analysis

Status: Complete for design preparation; runtime feasibility not yet demonstrated.

The [setup](sprint_E.3_setup.md) owns the execution contract;
[scope](sprint_E.3_pipeline_scope.md) owns the bounded iteration goal;
[design](sprint_E.3_design.md) owns proposed mechanisms and tests.
[PLAN](../../PLAN.md) assigns PBI-053 and [SRS](../../docs/srs.md) owns wider
product requirements. This analysis does not complete that PBI.

## Actors and observable goals

Use existing SRS actors: A-01 Developer saves a small Working Copy change as
reviewable Git source; A-02 Reviewer accepts the intended change; A-03 Deployer
chooses when to release an accepted revision; A-04 Lab user sees the change and
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
merges it into that development application. Capture agreed Main through
PROJECT into a Git feature branch, review source and generated distribution,
then commit/push and manually open a PR. The reviewer checks the diff and
checks, then merges it. The deployer explicitly selects the accepted commit
and triggers a different release workflow. It verifies and packages the
selected Git state, deploys that archive and checks behavior/history. Success
leaves a traceable PR, source commit, artifact identity and target result.

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

Feasibility is supported by documented APIs and bounded E.2 evidence; end-to-end
execution remains unrun. Complexity is moderate because runner connectivity,
PROJECT Git/staging behavior and a consistent baseline need proof; the visible
journey itself is small. Installed actionlint/act/Podman and the pinned SQLcl
client were located; a running runner/database was not verified.

The principal risks are capturing unrelated DEV changes, source/dist mismatch,
branch-name handling, schema/app mapping and dispatching a stale/unaccepted
revision. Use a single-author checkpoint, reviewed staged files, explicit base
and commit identities and one fixed disposable target. Existing 25.3 tooling
remains separate. Stop on an unsupported command or unexpected state instead
of implementing a second migration controller.

Design is ready for review. Implementation prerequisites and choices are
explicit in the [design](sprint_E.3_design.md); no fresh delivery result is claimed.
