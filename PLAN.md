# Sprint Plan

## Completed preliminary work

The Product Owner confirmed on 2026-10-16 that the existing local Oracle APEX
setup is completed initial work. The baseline includes the Podman environment,
Oracle Database/APEX/ORDS installation, lifecycle and verification scripts,
and the [deployment runbook](docs/deploy.md). Its verification record documents
database and HTTP access, administrator login, and a full VM stop/restart.
This work predates Sprint 0; it is not a retrospectively executed RUP sprint.

Treat this as completed preliminary work available for potential reuse.
Future work will assess suitability for the chosen CI/CD approach and
validate current runtime behavior as needed. Historical checks remain
historical evidence; this entry does not claim a fresh execution or completion
of the Hello World application or its CI/CD pipeline.

The supplied [Oracle APEX lifecycle PDF](refs/apex-lifecycle-management-v3.pdf)
is preserved as an external reference for the research.

## Planning decisions

The Product Owner accepted the vision, roadmap, and next-sprint proposal on
2026-10-16 and explicitly requested Sprint 0 closure. The mapping is now
Sprint 1 → I.1 and Sprint 2 → E.1, following the local phase-based ID policy.
Sprint 0 keeps its original identifier. I.1 was activated and later explicitly closed with all material accepted by the Product Owner on 2026-10-16. E.1 activation is authorized following I.1 closure.
See the [Sprint 0 handover](progress/sprint_0/sprint_0_handover.md) for outcomes,
review evidence, and the next-session prompt.

## Sprint 0 - Vision and initial plan

Status: Done
Mode: managed
Test: none
Regression: none

Backlog Items:

* PBI-001. Establish the product vision
* PBI-002. Derive the initial project plan from the vision

## Sprint I.1 - APEX CI/CD research and Inception baseline

Status: Done
Mode: managed
Test: none
Regression: none

Research credible APEX and database CI/CD alternatives against the accepted
vision and supplied external reference. Assess the preliminary Podman setup
for potential reuse. Define the Hello/World behavior, system boundary,
stakeholders, use cases, requirements, priorities, release scope and risks;
then materialize the SRS, candidate architecture and exact test-profile
commands. Review this coherent baseline before proposing executable work.
This iteration changes documents and decisions, not application code.

The Product Owner accepted the revised baseline with the presentation wording
correction and explicitly closed I.1 with all material accepted on 2026-10-16.
See its handover and review results for actual evidence and remaining limits.

Backlog Items:

* PBI-003. Define system view and stakeholders
* PBI-004. Define actors, use cases, and success criteria
* PBI-005. Materialize the Software Requirements Specification
* PBI-006. Establish and prioritize the Product Backlog
* PBI-007. Define the initial release scope
* PBI-008. Identify constraints, assumptions, and major risks
* PBI-009. Materialize the candidate architecture
* PBI-010. Review the Inception baseline for consistency and viability

## Sprint E.1 - Validate the local APEX delivery path

Status: Done
Mode: managed
Test: smoke, unit, integration
Regression: smoke, unit, integration

Activated on 2026-10-16 under the Product Owner's explicit authorization
after I.1 closure. The Product Owner explicitly closed E.1 on 2026-10-18.
The delivered A–I prototype, correction evidence and handover conclude this
iteration; remaining proofs and deferred concerns are tracked in PBI-018–035.
Closure does not assert that the original full validation contract passed or
that Lifecycle Architecture/production readiness is accepted. No next sprint
is activated. See the [closure handover](progress/E.1/sprint_E.1_handover.md#sprint-closure).

This provisional Elaboration iteration uses a minimal Hello/World architectural
prototype to validate the highest-risk technical assumptions and use cases,
refine requirements, stabilize the architecture baseline, assess the
Lifecycle Architecture milestone, and create the Construction plan. I.1 may retain, refine, split, reorder, or replace it; before
prototype construction, iteration setup/design refines the prototype PBI into
independently reviewable `PBI-XX.YY` sub-PBIs from the accepted candidate
architecture without inventing work during Inception.

Backlog Items:

* PBI-011. Build an executable architectural prototype
* PBI-012. Validate critical technical assumptions and use cases
* PBI-013. Refine use cases and supplementary requirements
* PBI-014. Stabilize the architecture baseline
* PBI-015. Assess the Lifecycle Architecture milestone
* PBI-016. Create the Construction plan

## Sprint E.2 - Assess E.1 against Oracle lifecycle guidance

Status: Progress
Mode: managed
Test: none
Regression: none

On 2026-10-19 the Product Owner refined E.2 to gap analysis of the existing
E.1 technology against the supplied Oracle APEX lifecycle paper, with focused
exercises where needed and a reproducible walkthrough. Establish evidenced
gaps, blockers, proposed backlog items and a roadmap toward Oracle-recommended
delivery; assess policy conflicts without assuming they are product limitations.
The [E.2 scope record](progress/E.2/sprint_E.2_proposedchanges.md) defines the
analysis and handover contract. Complex Foundation upgrades move to E.5 after
the technology/toolchain is stabilized. The earlier renumbering of the native
and Git-based exercises to E.3/E.4 remains in effect. Activated on 2026-10-19
by explicit Product Owner request in managed mode. The
[setup](progress/E.2/sprint_E.2_setup.md) records the execution contract. The
separate [analysis](progress/E.2/sprint_E.2_analysis.md) establishes the findings
and evidence questions before exercise selection. The Product Owner approved
analysis on 2026-10-19 after external review. The revised
[exercise design](progress/E.2/sprint_E.2_design.md) and verification plan are
Accepted by the Product Owner on 2026-10-19; construction is authorized.
By Product Owner direction, E.2 uses experiment-based verification without
separate automated/regression suites for disposable helpers. Expected/actual
exercise outcomes and the reproducible live handover remain required.

Backlog Items:

* PBI-051. Assess the E.1 delivery approach against Oracle lifecycle guidance

## Sprint E.3 - Validate APEX-native team-centric development

Status: Planned
Mode: managed
Test: smoke, unit, integration
Regression: smoke, unit, integration

On 2026-10-19 the Product Owner split the Oracle-style exercise into two
iterations. E.3 validates shared APEX development, page locks and Working
Copies, with coordinated Git checkpoints feeding native release, test and
deployment automation. The [E.3 scope record](progress/E.3/sprint_E.3_proposedchanges.md)
defines its independent acceptance and common foundation for E.4. This plans
work without starting execution or approving an implementation design.

Strict acceptance: every scenario must map to exact pages in the supplied
Oracle lifecycle paper and applicable version-specific Oracle documentation,
with execution evidence and explicit approved deviations. Handover must
include an evidence-based E.1 comparison under PBI-047; see the
[shared evidence contract](progress/E.3/sprint_E.3_proposedchanges.md#strict-oracle-traceability-and-comparison-contract).

Backlog Items:

* PBI-036. Define Oracle lifecycle use-case coverage
* PBI-037. Establish native Oracle source capture and staging
* PBI-035. Validate adoption of an existing APEX application
* PBI-039. Demonstrate native team-centric APEX collaboration
* PBI-040. Measure PL/SQL regression coverage with utPLSQL
* PBI-034. Automate application browser acceptance checks
* PBI-041. Demonstrate Oracle-recommended application quality audits
* PBI-027. Unify delivery environment configuration
* PBI-038. Deliver native Oracle release artifacts
* PBI-021. Complete release admission and promotion negative coverage
* PBI-029. Strengthen automation failure diagnostics
* PBI-045. Preserve scenario protections around native Oracle delivery
* PBI-044. Demonstrate native mini-app component reuse
* PBI-043. Operate the Oracle lifecycle automation pipelines
* PBI-047. Compare APEX-native delivery with the earlier prototype

## Sprint E.4 - Validate Git-based feature-centric development

Status: Planned
Mode: managed
Test: smoke, unit, integration
Regression: smoke, unit, integration

Build on the accepted E.3 native release/test foundation to validate feature
branches, private APEX branch environments, PR/conflict integration and safe
post-merge central DEV synchronization. The [E.4 scope record](progress/E.4/sprint_E.4_proposedchanges.md)
owns its separate exercise, regression evidence and final comparison of both
approaches. E.4 requires E.3's applicable baseline and its own activation;
shared tooling does not merge the two development workflows.

Strict acceptance: apply the same
[Oracle traceability and comparison contract](progress/E.3/sprint_E.3_proposedchanges.md#strict-oracle-traceability-and-comparison-contract)
to E.4 scenarios and inherited capabilities. PBI-046 must deliver E.4 versus
E.1 evidence and the final E.1/E.3/E.4 decision package; a narrative preference
or an E.3 test result alone cannot satisfy this requirement.

Backlog Items:

* PBI-019. Prove parallel component collaboration and integration
* PBI-020. Complete APEX capture and reconstruction validation
* PBI-042. Synchronize central development after accepted merges
* PBI-017. Deliver a repository and pipeline reference guide
* PBI-046. Compare and independently reproduce the Oracle-style laboratory

## Sprint E.5 - Validate Foundation upgrades and version coexistence

Status: Planned
Mode: managed
Test: smoke, unit, integration
Regression: smoke, unit, integration

The final currently planned Elaboration step implements the compatible and
breaking Foundation upgrade scenarios on an accepted, stabilized technology/
toolchain informed by E.2 analysis and the applicable E.3/E.4 evidence. Verify
API/schema evolution, data preservation, version coexistence and independent
consumer maintenance windows. The [E.5 scope record](progress/E.5/sprint_E.5_proposedchanges.md)
retains the agreed migration sequence and defines the toolchain entry gate;
unresolved blockers require plan refinement before implementation.

Backlog Items:

* PBI-048. Prove an available compatible Foundation extension
* PBI-049. Prove an available breaking Foundation transition
* PBI-050. Prove an in-place Foundation upgrade with component windows
