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

Status: Done
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

The Product Owner accepted the assessment and handover and authorized closure on
2026-11-03. PBI-051 and its four sprint-scoped children are complete as assessment
outcomes. Native verification, identity, protection and reviewed-repair limits
remain explicit follow-up, not production-readiness claims. E.3 remains Planned.
See the [final assessment](progress/E.2/sprint_E.2_assessment.md) and
[accepted handover](progress/E.2/sprint_E.2_handover.md).

Backlog Items:

* PBI-051. Assess the E.1 delivery approach against Oracle lifecycle guidance

## Sprint E.3 - Prototype the Git-based development pipeline

Status: Progress
Mode: managed
Test: smoke, integration
Regression: smoke

On 2026-11-03 the Product Owner narrowed E.3 to a simple Elaboration
architecture prototype. Demonstrate one Working Copy change captured in Git,
a developer manually opening a PR, accepted integration and a deployer
manually triggering the release workflow. Keep PR validation separate from
deployment. Analysis/design considers selective future release automation
without implementing automatic deployment for every PR. The
[E.3 preparation](progress/E.3/sprint_E.3_pipeline_scope.md) owns the bounded
journey, design questions, evidence and deferrals. Exact focused checks are
selected during analysis/design; comprehensive delivery suites are deferred.
Activated on 2026-11-03 by explicit Product Owner request to prepare the design.
The Product Owner approved implementation through technical handover on
2026-11-03 without further questions. Prototype implementation, required gates
and browser verification are complete. The Product Owner's subsequent native-only
correction is implemented and freshly verified; see the
[native correction record](progress/E.3/sprint_E.3_native_correction.md).
The later [GitHub configuration correction](progress/E.3/sprint_E.3_github_configuration.md)
removes retained local settings and provides the requested versioned local lab
runner launcher; its release/qualification and required gates passed.
Sprint closure and final Product Owner
acceptance are not inferred. See the
[setup and analysis](progress/E.3/sprint_E.3_setup.md) and
[accepted design and test specification](progress/E.3/sprint_E.3_design.md),
[executed walkthrough](progress/E.3/sprint_E.3_increment_demo.md) and
[handover](progress/E.3/sprint_E.3_handover.md).

The former 15 assigned items return to the unscheduled backlog with their
acceptance criteria unchanged. PBI-053 owns the independently reviewable
prototype; partial reuse of broader capabilities does not complete their PBIs.
Complete those items in Construction or schedule focused later Elaboration
proofs when an identified risk warrants them. No Construction sprint is
created by this refinement. E.2 was accepted and closed on 2026-11-03; E.3 activation was explicitly requested separately.

Backlog Items:

* PBI-053. Prove a simple Git-based development-to-release journey

## Sprint E.4 - Validate Git-based feature-centric development

Status: Planned
Mode: managed
Test: smoke, unit, integration
Regression: smoke, unit, integration

The earlier [E.4 scope record](progress/E.4/sprint_E.4_proposedchanges.md)
retains the planned feature-centric exercise and its five assignments below.
Following the 2026-11-03 [E.3 refinement](progress/E.3/sprint_E.3_pipeline_scope.md),
E.3 no longer promises the former full native release/test foundation.
Before E.4 activation, refine its scope from the prototype's actual evidence:
retain bounded architectural-risk experiments in Elaboration and schedule
completion work in Construction. The former broad comparison and qualification
obligations remain backlog requirements, not implied E.3 completion. This
preparation neither activates E.4 nor approves its earlier implementation scope.

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
