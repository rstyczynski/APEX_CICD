# Oracle APEX CI/CD Laboratory Roadmap

## Basis and decision status

The Product Owner accepted this roadmap and the next-sprint proposal on
2026-10-16, following acceptance of the README vision. Existing local
APEX/Podman setup remains completed preliminary work available for potential
reuse. Sprint 0 is complete. I.1 and E.1 remain Planned.

## Completed preliminary work

The local Oracle Database, APEX, and ORDS setup, lifecycle scripts, and
access/restart verification are documented in [docs/deploy.md](docs/deploy.md).
Assess these assets for reuse rather than assuming a fresh installation is
needed. Their adoption as the project baseline is not yet a technical decision.
Retain the supplied [Oracle APEX lifecycle paper](refs/apex-lifecycle-management-v3.pdf)
as external research input. Any fresh validation will be targeted to the
selected approach and clearly distinguished from the historical checks.

## Sprint 0 — Vision and initial plan

PBI-001 has delivered the accepted vision for a reproducible CI/CD laboratory
and a minimal application with greeting history and Hello/World data and
configuration pages. PBI-002 delivered this accepted roadmap and the next-iteration plan. The
Product Owner explicitly requested closure after reviewing these documents;
the [handover](progress/sprint_0/sprint_0_handover.md) records the decision and review limits.

## Inception — Research and candidate approach

I.1 is the next planned iteration, formerly labeled Sprint 1. Keep PBI-003 through PBI-010 as one proportionate baseline:
define users, system boundary, representative change journeys and success
criteria; materialize the SRS; refine priorities and scope; assess risks;
and deliver a candidate architecture and exact test-profile commands.

Compare SQLcl PROJECT workflows with explicit APEX export/import plus
versioned database migrations, including applicable Liquibase integration.
Assess reviewable source, reproducible exports, release packaging, ordering
of database and application changes, configuration and secrets, developer
collaboration, runner access to the local service, target isolation, failure
detection, and recovery. These are research candidates, not tool selections
or claims of local compatibility.

Use the external paper and version-specific primary documentation, then
recommend the smallest approach that demonstrates the accepted vision.
Define what the Hello and World components own and whether one application
is sufficient. Resolve data/configuration behavior and history preservation
before construction. Select a CI execution model and development/test
separation compatible with local resources. Review requirements, research
conclusions, candidate architecture, and quality profile together before
approving an executable iteration.

## Elaboration — Validate the risky delivery path

E.1, formerly labeled Sprint 2, is planned with
PBI-011 through PBI-016. Use a thin Hello/World slice to validate source export,
database evolution, packaging, target deployment, and an observable behavior
change. Reuse existing assets where the accepted design supports them.
Refine PBI-011 into bounded sprint children before construction, with Product
Owner approval.

Test repeat deployment and a failing change, inspect its effect on saved
history, and demonstrate recovery or forward repair. Record actual version
compatibility, runner/network constraints, evidence, and remaining limits.
Revise the approach when evidence contradicts the research. Assess the
Lifecycle Architecture milestone before committing to full Construction
scope; retain further Elaboration if needed.

## Construction — Complete the reusable example

Define C.n iterations from the validated architecture and remaining backlog.
Complete Hello and World data/configuration pages and greeting history, then
deliver the chosen review, build/check, release, and deployment workflow.
Show a component change and a database change with traceable release artifacts,
preserved data, and failure handling. Prefer a few coherent increments over
separate iterations for every generic discipline. No C.n assignment is made here.

## Transition — Reproduce and hand over

Have an operator follow the local workflow from prerequisites to a deployed
change and known failure/recovery case. Deliver operating guidance, evidence,
limitations, and the comparison explaining why the selected approach fits.
Demonstrate the actual increment and capture the Product Owner decision.
Production rollout, cloud hosting, and high availability remain outside the
accepted initial scope.

## Refinement and acceptance

I.1 refines this plan using research and requirements; E.1 refines it again
using executable evidence. Merge or split later work when outcomes,
dependencies, or risks justify it. See the [Sprint 0 proposal](progress/sprint_0/sprint_0_proposedchanges.md)
for the original proposal and recorded acceptance. The current [plan](PLAN.md)
contains the accepted label mapping and next-sprint context.
