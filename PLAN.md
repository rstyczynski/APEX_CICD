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
Sprint 0 keeps its original identifier. Both later sprints remain Planned.
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

Status: Planned
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

Status: Planned
Mode: managed
Test: smoke, unit, integration
Regression: smoke, unit, integration

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
