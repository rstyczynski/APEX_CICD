# E.4 — Handover readiness assessment

## Current outcome

2026-11-09. The approved PBI-042/PBI-060 experiment has current native, GitHub and
browser evidence. Three independent author processes overlapped; later announced
release-e4-candidate admitted A/C, preserved B and promoted/froze 1.0.7. Central DEV
refused stale/pending work and successfully installed/repeated the selected artifact
with all business fields preserved. The original exact-checksum restoration assumption
failed on the generated version counter; the Product Owner explicitly approved the
reviewed counter-only recovery recorded in [tests](sprint_E.4_tests.md).

[Implementation](sprint_E.4_implementation.md), [the manual](user_manual.md),
[complete walkthrough](sprint_E.4_increment_demo.md) and [handover](sprint_E.4_handover.md)
form the concrete delivery package. The temporary central users were removed and
Available status confirmed. [PLAN](../../PLAN.md) remains Progress. Independent
Astra handover review found the package ready with a nonblocking overlap-duration
label correction (R1-L1), now implemented and awaiting focused recheck. Live Product
Owner demonstration/acceptance and sprint closure are not inferred from technical success. The wider product requirements,
production fencing, arbitrary fresh install and PBI-056 remain outside this experiment.

## Historical design assessment (superseded status)


## Current outcome

2026-11-09. E.4 remains active for PBI-042/PBI-060 in [PLAN](../../PLAN.md),
with both items under_design on [the board](../../PROGRESS_BOARD.md). The Product
Owner selected independent parallel work and the release-announcement participation
flow in the [analysis](sprint_E.4_setup.md#analysis). The
[design/test specification](sprint_E.4_design.md) translates it into proposed native
APEX/SQLcl and GitHub steps; full design approval and execution remain pending.

Developers start changes independently without needing a release target. Later the
Release Manager creates the candidate branch from current accepted main, announces
the branch name and invites submissions. The candidate baseline need not equal the
developers' starting commits. A/C choose to participate and submit PRs to that branch;
B chooses to wait. The manager separately reviews submitted changes and admits A/C
after checks/dependency review. The accepted candidate contains its inherited main
baseline plus A/C, with B's work excluded and preserved for a later announcement.

## Source-backed policy and experiment evidence

The [analysis reference section](sprint_E.4_setup.md#authoritative-devops-references-and-project-policy)
links GitHub's feature/PR practices, explicit base/head targeting and branch updates,
plus Microsoft's release-from-main guidance. It distinguishes those documented
mechanisms from this project's chosen opt-in policy. Neither GitHub Flow nor
Microsoft's complete branching strategy is claimed to prescribe this exact workflow.

Revised IT-1 requires independent native capture/stage provenance, later candidate
creation from then-current main, an announcement, A/C participation PRs, B deferral,
manager admission and combined native verification. Candidate-to-main promotion
must not import unselected later mainline content unnoticed. IT-4 inspects the
selected application behavior and preserved data after deployment/repeat.

## Prior independent review and remaining boundary

The [original dedicated Astra report](sprint_E.4_design_review-1.md) and
[feedback](sprint_E.4_design_review-1-feedback.md) reviewed the superseded sequential
scenario. Their earlier readiness verdict does not validate this topology or release
policy. R1-M1/R1-M2's trusted-baseline and availability/receipt corrections remain
in PBI-042; the [round dispositions](sprint_E.4_design_review-1-decisions.md) retain
the original textual verification boundary. Expert text is preserved unchanged.

The Product Owner explicitly waived further Astra review and will inspect this
revision directly. No new reviewer contact or round, implementation, fixture setup,
native execution, workflow dispatch or release announcement has occurred. Source/
artifact provenance and runtime checks are specifications, not passing evidence.

Qualified author fixtures, native identity/source-path equivalence, resource capacity
and combined source/distribution reconciliation remain execution prerequisites.
PBI-056 and other Construction capabilities remain excluded. The root PBI-060 still
says all three contributions in one release; its acceptance alignment with A/C-now,
B-later must be resolved at design approval before claiming PBI completion.

## Documentation checks and next decision

[The documentation audit](sprint_E.4_documentation_audit.md#release-announcement-and-developer-participation)
records source checks, link/anchor validation and consistency checks for this revision.
All native/runtime tests remain unrun. The next decision is Product Owner review of
the proposed design; implementation stays stopped until explicit approval.
