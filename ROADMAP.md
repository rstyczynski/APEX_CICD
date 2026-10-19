# Oracle APEX CI/CD Laboratory Roadmap

## Basis and decision status

The Product Owner accepted this roadmap and the next-sprint proposal on
2026-10-16, following acceptance of the README vision. The platform installation is preliminary historical work; I.1 owns the maintained infrastructure lifecycle procedure and its assessment. Sprint 0 is complete. I.1 is closed with all material explicitly accepted by the Product Owner on 2026-10-16; E.1 was subsequently closed by the Product Owner on 2026-10-18; follow-up work remains in the backlog.

## Completed preliminary work

The local Oracle Database, APEX, and ORDS setup, lifecycle scripts, and
access/restart verification are documented in [docs/deploy.md](docs/deploy.md).
Elaboration takes this procedure and supporting scripts to provision, verify and destroy scoped experiment infrastructure. The analysis reference versions and historical checks are recorded there; the architecture does not depend on a particular VM continuing to run. Supporting sources still require reviewed Git adoption before reproducibility can be claimed.
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

I.1 is complete, formerly labeled Sprint 1. Its accepted analysis retains the following scope. Keep PBI-003 through PBI-010 as one proportionate baseline:
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

E.1, formerly labeled Sprint 2, concluded in managed mode on 2026-10-18 with
the demonstrated A–I prototype and recorded remaining work. PBI-018–035 made
the follow-up visible at closure; E.2–E.5 are now scheduled below. The original objective
for PBI-011 through PBI-016 follows below as planning context. Use a thin Hello/World slice to validate source export,
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

## Elaboration E.2 — E.1 gap analysis and focused exercises

E.2 is active in managed mode with PBI-051, starting from the current E.1 technology.
The [E.2 scope record](progress/E.2/sprint_E.2_proposedchanges.md) defines a
source-backed gap analysis against the supplied Oracle lifecycle paper,
focused exercises to demonstrate material problems or solutions, and the
established runnable walkthrough. Its outcome is an evidenced retain/replace/
investigate recommendation, proposed backlog items and a dependency-ordered
roadmap toward Oracle-recommended delivery. Working Copies and Git authority
are a compatibility question to investigate, not an assumed product blocker.
The analysis informs refinement of E.3/E.4; complex upgrades move to E.5.
The [execution setup](progress/E.2/sprint_E.2_setup.md) records contracting;
the separate [analysis](progress/E.2/sprint_E.2_analysis.md) establishes the
problems, evidence and questions that drive exercise selection. Analysis was
approved on 2026-10-19 after external review. The
[revised exercise design](progress/E.2/sprint_E.2_design.md) and test specification
are Proposed for managed approval. No exercise implementation or runtime success
is claimed; its E.2-specific regression-scope proposal remains unapproved.

## Elaboration E.3 — APEX-native team-centric development

The Product Owner split the Oracle-style exercise on 2026-10-19. E.3 is Planned
in managed mode and demonstrates shared DEV, page locks, Working Copies and
APEX Main integration, followed by coordinated Git checkpoints. It establishes
the native release/deployment, test/coverage, audit and pipeline foundation
while reproducing the demonstrated E.1 protections and showing mini-app reuse.
The [E.3 scope and backlog review](progress/E.3/sprint_E.3_proposedchanges.md)
defines its 15 assigned outcomes, mandatory E.1 comparison and independent handover evidence.

## Elaboration E.4 — Git-based feature-centric development

E.4 is separately Planned in managed mode, depending on E.3's applicable
accepted native tooling. It demonstrates private APEX branch environments,
parallel feature branches, PR/conflict integration and central DEV refresh
from Git main. Its five assigned outcomes also complete private-target
reconstruction validation, the consolidated guide and independent reproduction
and comparison of both approaches against E.1. The
[E.4 scope record](progress/E.4/sprint_E.4_proposedchanges.md) owns that exercise;
the [plan](PLAN.md) owns both iterations' assignments. Both require exact paper-page and version-specific Oracle-documentation
traceability, recorded execution evidence and an E.1 comparison at their own
handover; E.4 also delivers the final three-approach decision package. Neither sprint has
started. Broader unresolved controls and Lifecycle Architecture acceptance
remain explicit, evidence-based decisions.

## Elaboration E.5 — Foundation upgrades on the stabilized toolchain

E.5 is the final currently planned Elaboration step, in managed mode with
PBI-048–050. The [E.5 upgrade scope](progress/E.5/sprint_E.5_proposedchanges.md)
retains compatible and breaking API/schema evolution, initial data migration,
legacy-write propagation and separate consumer maintenance windows. Entry
requires an accepted, reproducible, stabilized technology/toolchain informed
by E.2 findings and applicable E.3/E.4 evidence. Resolve blockers or refine the
plan before implementation; the scheduling alone does not establish Lifecycle
Architecture acceptance or make a particular toolchain the final choice.

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
