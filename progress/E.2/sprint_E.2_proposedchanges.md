# E.2 E.1 gap analysis against Oracle lifecycle guidance

## Decision, status and authoritative documents

On 2026-10-19 the Product Owner made E.2 a gap-analysis iteration with required
focused exercises and the established end-to-end walkthrough. It works on the
current technology developed in E.1. Complex Foundation upgrades are deferred
to E.5, the final currently planned Elaboration step, after stabilization of
the technology/toolchain. E.2 remains Planned in managed mode; this record
schedules analysis, not its execution or an implementation approval.

The [Sprint Plan](../../PLAN.md#sprint-e2---assess-e1-against-oracle-lifecycle-guidance)
owns assignment and lifecycle status. The
[Product Backlog](../../BACKLOG.md#pbi-051-assess-the-e1-delivery-approach-against-oracle-lifecycle-guidance)
owns PBI-051 and the [progress board](../../PROGRESS_BOARD.md) tracks its
Planned row. The [SRS](../../docs/srs.md) owns requirements, the
[architecture](../../docs/architecture.md) owns mechanisms, the
[research](../../docs/cicd-research.md) records earlier recommendations and the
[test profile](../../docs/test-profile.md) owns executable verification.
The [README](../../README.md) and [roadmap](../../ROADMAP.md) orient the reader.

The supplied [Oracle lifecycle paper](../../refs/apex-lifecycle-management-v3.pdf)
is the primary comparison source. Use exact pages/sections and applicable
version-specific official Oracle documentation for technical claims. The
[E.1 handover](../E.1/sprint_E.1_handover.md),
[assessment](../E.1/sprint_E.1_assessment.md) and
[walkthrough](../E.1/sprint_E.1_increment_demo.md) identify the delivered baseline
and its limitations. Historical results do not establish current reproducibility
or completion of unfinished E.1 criteria.

## Objective and analysis boundaries

PBI-051 establishes an evidence-backed evolution decision: what to retain,
replace or investigate in E.1 and in what order. Start from its implemented
source capture, database migrations, release artifacts, validation, deployment
and recovery rather than presume that the recommended native replacement is
already available. Assess developer collaboration as well as the release
pipeline, including the boundary between authoring and accepted Git authority.

For each relevant recommendation, connect its source to the observed E.1
behavior, the underlying requirement, the gap or equivalence, evidence and
proposed disposition. Distinguish missing implementation, an unavailable
capability, a tool/version limitation and a project policy conflict. Record
unknowns explicitly. Do not declare a blocker from documentation absence,
unrun behavior or preference alone, and do not assume every custom mechanism
must be retained or replaced.

In particular, investigate APEX Working Copies against the Git-authoritative
method. Authoring outside Git is a concern to examine, not an established
blocker. Trace capture, review, reconstruction, validation and promotion of
the accepted result; identify which conflicts can be resolved by integration
or an explicit policy decision. Any unavoidable conflict needs supporting
source/evidence, impact, attempted alternatives and a recommended disposition.

## Required exercises

Select the smallest exercises needed to resolve material uncertainty or
show a problem/solution from E.1. Each exercise states its question, baseline,
inputs, expected observation, actual result, source/tool versions, interpretation
and effect on the recommendation. A documented limitation can be an experiment
result; it must not be presented as delivery of the missing capability.

Use the existing E.1 environment and supported interfaces as the baseline.
Where a comparison needs a native capability, introduce only the bounded
experimental setup needed to test the hypothesis and distinguish it from
adoption of a replacement toolchain. Preserve accepted application data and
reconcile any retained code or policy change through the managed design.
Full Oracle-style workflow delivery and complex upgrades are later outcomes.

During design, state the exact smoke, unit and integration checks applicable
to each code-bearing exercise and the E.1 regression it must preserve. Review
and source-traceability checks cover analysis-only findings; do not invent
passing runtime tests for document work or reuse old results as fresh runs.

## Deliverables, backlog and roadmap

Deliver a source-linked gap report, evidence for required exercises, and a
recommendation covering retain/replace/investigate decisions with known
blockers, alternatives and justified deviations. Propose a dependency-ordered
roadmap toward Oracle-recommended delivery, preserving accepted product goals
or explicitly identifying decisions needed to change them.

Map follow-up outcomes to existing PBIs before proposing new ones. Register
new, independently valuable work through the backlog procedure and keep
unscheduled proposals off the board. Identify any evidence-based changes
needed to later sprint scope for the Product Owner's decision; this analysis
must not silently duplicate, close or reassign later implementation work.

E.3's [APEX-native exercise](../E.3/sprint_E.3_proposedchanges.md) and E.4's
[Git-based exercise](../E.4/sprint_E.4_proposedchanges.md) remain the current
implementation/evaluation hypotheses. E.2 informs their refinement without
claiming their acceptance evidence. The
[E.5 upgrade scope](../E.5/sprint_E.5_proposedchanges.md) retains PBI-048–050
and requires a stabilized accepted toolchain before complex upgrade construction.
The gap report may identify upgrade risks, but E.2 does not implement those PBIs.

## Walkthrough and handover acceptance

Prepare the established sprint presentation pair and a complete runnable
walkthrough, with prerequisites, real inputs, actions, intermediate results,
checks and the relevant sources/findings. Show the E.1 baseline, reproduce
each required exercise and its material failure or limitation, inspect the gap
report, then walk through the proposed backlog and roadmap decisions. Documents
must be directly inspectable; slides or previous logs alone do not establish
a live exercise. Label unexecuted paths and unresolved questions.

The Product Owner must be able to follow how each material recommendation
arises from source guidance and observed evidence, and what investment or
policy decision follows. Record the actual review decision and remaining
work. No gap findings, blocker conclusions, runtime results or handover
acceptance are claimed by this planning update.

## Activation and design review — 2026-10-19

The Product Owner explicitly activated E.2 and requested execution using the
rup-strikes-back skill in managed mode. This supersedes the Planned/no-execution
wording above; the original planning decision is retained. PLAN now records
Progress. The [setup](sprint_E.2_setup.md) records completed contract/analysis;
the [proposed design and test specification](sprint_E.2_design.md) defines the
next approval gate. The board remains under_design until design acceptance.

The current request clarifies that focused exercises may introduce bounded
Oracle-recommended capabilities beyond E.1's technology. This does not authorize
replacement-toolchain adoption or later-sprint delivery. The design tests
Working Copies with Git acceptance without assuming incompatibility, and
keeps complex Foundation upgrades in E.5. No exercise implementation, runtime
success, permanent policy change or handover acceptance is claimed.

## Analysis before exercise design — 2026-10-19

The separate [analysis](sprint_E.2_analysis.md) now owns the actor journeys,
requirements, comparison findings and unresolved evidence questions.
Contracting is complete; analysis is in progress. The earlier analysis-complete
claim and design approval request are withdrawn. The board is corrected to
under_analysis for E.2/PBI-051. The exercise draft is retained pending analysis
review, with no implementation or test-skeleton authorization.

## Analysis baseline ready for review — 2026-10-19

The [analysis](sprint_E.2_analysis.md) and
[review summary](sprint_E.2_inception.md) now cover fourteen findings and five
prioritized evidence questions, mapped to existing PBIs and the dependency
direction toward stabilized tooling before E.5. Desk analysis is complete;
PBI-051's exercise-backed outcome remains unfinished. Its board status is
analysed, with E.2 under_analysis at the review checkpoint. The held exercise
draft requires revision from these findings; no implementation is authorized.

## Working Copy usability reevaluation — 2026-10-19

The Product Owner clarified that break-glass-only authoring and component-wide
reservations were E.1-stage policies. E.2 must reevaluate Working Copy usability
for ordinary development and Git pipeline integration, rather than assume those
policies constrain the future approach. The [analysis](sprint_E.2_analysis.md)
and [review summary](sprint_E.2_inception.md) now state that applicability and
include developer coordination, comparison, refresh/merge, abandonment and
recovery effort in the evidence questions. This directs the assessment without
selecting a replacement policy or approving exercise implementation.

## Optional-tool compatibility — 2026-10-19

The Product Owner added two hypotheses: PROJECT and Working Copies may remain
optional, while the repository should retain viable supported paths to use them.
The [analysis](sprint_E.2_analysis.md#optional-tool-compatibility-hypotheses)
defines H-1/H-2 independently and together, including counter-evidence and
switching costs. README records the guiding principle: give developers
flexibility through stable, industry-standard tools. Compatibility remains
unverified; this refinement selects no layout, migration authority or default
tool and does not approve exercises. Existing backlog reconciliation and E.5
allocation remain unchanged.
