# E.4 design — External review round 1 prompt

**Round:** E.4, round 1, outbound design review.
**Revision:** 3f4dc63a35390fccf9ee0683e3ff5c831a7d9f75; current committed design baseline.
**Reviewer:** existing local Codex reviewer chat, requested model gpt-6-astra.
**Scope:** independent read-only design/context inspection; no runtime experiments.
**Inputs:** [design](sprint_E.4_design.md), [setup](sprint_E.4_setup.md),
[audit](sprint_E.4_documentation_audit.md), [PLAN](../../PLAN.md),
[backlog](../../BACKLOG.md), [review contract](../../.agents/skills/rup-external-review/references/round-contract.md).
**Status:** No findings yet.

## Reviewer instruction

Act as the independent external reviewer for APEX_CICD, active sprint E.4,
Elaboration, design review round 1. The Product Owner explicitly requested
this review in the existing local Astra chat before their own design approval.
This authorizes the local handoff in place of the skill's usual human relay.

Repository URL: https://github.com/rstyczynski/APEX_CICD.git
Branch/ref: main.
Exact source revision: 3f4dc63a35390fccf9ee0683e3ff5c831a7d9f75.
Publication evidence: git ls-remote origin refs/heads/main returned that full SHA
on 2026-11-09 after the source checkpoint push. The local tracking-ref update was
sandbox-blocked after successful push; remote verification confirmed publication.
Source access: existing local checkout and the published pinned commit. Review
committed files using git show or an isolated git archive so unrelated working
changes cannot affect the subject. Local BACKLOG has an additional uncommitted
PBI-059 definition; use the source revision for PBI-060 and the design's explicit
PBI-059 deferral. Unrelated E.3 model/deck/gap edits are excluded. No working
patch is part of this round. The prompt itself is coordination metadata, not an
additional design change.

Start with progress/E.4/sprint_E.4_design.md, sprint_E.4_setup.md,
sprint_E.4_documentation_audit.md and the appended accepted refinement in
sprint_E.4_proposedchanges.md. Read PLAN, board, BACKLOG, SRS, architecture,
test profile and E.3 release-correction evidence as needed. The approved boundary
is ONLY PBI-042 and PBI-060. PBI-056 is explicitly excluded as Construction-level
work; do not require it merely to make this experiment resemble the full private
feature-environment pattern. Other proposed enhancements are Construction work.

Assess whether three separately attributable native staging windows accumulating
into one numbered release satisfy PBI-060, with explicit native comparison bases,
source/distribution provenance, include coordination and dependency explanation.
Check whether the coordinated shared-author model is honestly represented and
whether the design needs a stronger demonstrated dependency or conflict case to
meet the unchanged acceptance criterion. For PBI-042, assess safe central DEV
synchronization, stale candidate refusal and pending-edit preservation. In
particular challenge the sufficiency and honesty of operator-enforced refusal,
the no-edit interval, baseline/checksum selection, prepared target reuse, native
semantics, and the unsupported initial-install guard. Do not conflate native
PROJECT verify with target drift detection or promise atomic fencing.

Read the linked version-specific official Oracle docs where needed. Distinguish
interface-supported feasibility, E.3 evidence, and E.4 cases not run. Identify
material missing experiment steps, unsafe target transitions, unsupported native
assumptions and misleading claims. Production hardening belongs to explicit
follow-up, not automatic Elaboration blockers. No earlier E.4 rounds exist.

Allowed actions: read-only source/document inspection and public documentation
lookup. You may write ONLY progress/E.4/sprint_E.4_design_review-1.md in the shared
checkout. Do not modify project source/design/board, commit/push, dispatch any
workflow, connect to the database or run exports/staging/deployment. No credentials
or business rows are needed. Do not message another chat.

Save the original report at progress/E.4/sprint_E.4_design_review-1.md. Begin with
subject/round/type, full revision, reviewer model where known, scope/exclusions,
inputs and per-finding status table. Use IDs R1-H1/R1-M1/R1-L1 etc. Each finding
needs source location, impact on this sprint, proposed correction and acceptance
check; distinguish inspected risks from reproduced defects. Give a clear verdict
on readiness for Product Owner design approval and what you did not run. Follow
the round contract linked above. Do not declare Product Owner acceptance.
