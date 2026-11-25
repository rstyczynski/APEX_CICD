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
the follow-up visible at closure; the expanded Elaboration sequence is scheduled below. The original objective
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

## Elaboration E.2 — Accepted Oracle lifecycle assessment

The Product Owner accepted and closed E.2 on 2026-11-03. PBI-051 delivered
[findings and follow-up](progress/E.2/oracle-gap-analysis.md), focused native
exercises, the [walkthrough](progress/E.2/cicd-walkthrough.md) and
[accepted handover](progress/E.2/sprint_E.2_handover.md). PROJECT, Working Copies
and Git coexist in the demonstrated path. Toolchain qualification, component
compatibility, drift protection and reviewed recovery remain explicit follow-up.
Closure accepts the assessment, not production readiness. No next sprint starts
automatically. Complex Foundation upgrades now follow the smaller validation increments described below.

## Elaboration E.3 — Simple Git-based pipeline prototype

On 2026-11-03 the Product Owner narrowed E.3 to an understandable architecture
prototype, assigned PBI-053. The [E.3 preparation](progress/E.3/sprint_E.3_pipeline_scope.md)
plans one Working Copy change captured in Git, manual PR creation and accepted
integration, followed by a manually triggered release workflow. Keep PR checks
separate from deployment and consider selective future automation during design.
Reuse prior evidence and simple native mechanisms. Demonstrate the real happy
path and expose remaining risks without completing all delivery capabilities.
E.3 was activated on 2026-11-03 for design preparation; E.2 is closed.
The [accepted design](progress/E.3/sprint_E.3_design.md) now has
[executed evidence and technical handover](progress/E.3/sprint_E.3_handover.md).
The [native correction](progress/E.3/sprint_E.3_native_correction.md) removes E.3
Python and reuses E.2 native APEX/SQLcl with GitHub Actions control.
Required gates and browser verification passed; wider capabilities remain
deferred, and final acceptance/closure remains a separate Product Owner decision.

The former 15 E.3 items return to the backlog with full criteria unchanged.
Complete them in Construction or schedule a focused later Elaboration proof
when a specific architectural risk requires it. The former exhaustive paper
coverage and comparative programme remains prior planning context, not this
prototype's exit gate. Verify sources for the actual Oracle operations used.

## Elaboration E.4 — Native integration experiment

E.4 and PBI-042/PBI-060 are Done following explicit Product Owner acceptance
and closure on 2026-11-25. The [closure handover](progress/E.4/sprint_E.4_handover.md#sprint-closure--2026-11-25)
records the decision, native validation, independent review and experiment limits.
No subsequent sprint is activated.

## Elaboration E.5 — Testable backend behind APEX pages

Planned. Backlog: PBI-061, PBI-040, PBI-062.

Extract one greeting rule into a package API while preserving page feedback.
Demonstrate direct backend enforcement, a regression detected by utPLSQL,
useful coverage and repeatable fixtures with explicit cleanup boundaries.

## Elaboration E.6 — Secure contracts and transactions

Planned. Backlog: PBI-063, PBI-052, PBI-064, PBI-079.

Validate the component contract under allowed and denied identity/country
contexts, compatible and breaking changes, and competing requests. Establish
version classifications and transaction responsibility through consumer tests,
retaining whole-application deployment.

## Elaboration E.7 — Upgrades and traceable releases

Planned. Backlog: PBI-065, PBI-077, PBI-057.

Upgrade one supported previous release while preserving synthetic data.
Verify actual database state and connect source, contracts, migrations and
test evidence to the release displayed in APEX. Demonstrate rejection of
incorrect deployed state and substituted artifacts.

## Elaboration E.8 — Complete PR candidate testing

Planned. Backlog: PBI-066, PBI-067, PBI-076.

Test one integrated PR candidate from suite selection through deployment and
reporting. Exercise PR, scheduled and prerelease applicability. Demonstrate
that missing, empty, skipped or failed mandatory validation prevents Testing
success and that cheap failures stop expensive dependent work.

## Elaboration E.9 — AI review and merge decisions

Planned. Backlog: PBI-068, PBI-069, PBI-070, PBI-071.

Demonstrate the developer journey from an accurate PR summary and real agent
review to a current Review result and controlled merge alongside Testing.
Exercise report changes, revision races, blocking findings, stale evidence
and publisher controls in a disposable repository.

## Elaboration E.10 — Isolated execution and interrupted cleanup

Planned. Backlog: PBI-072, PBI-073, PBI-074.

Run two candidate streams with separate data, credentials and validator
authority. Supersede or interrupt one without harming the other. Challenge
privilege boundaries, retry limits and cleanup, including forced termination
and scoped orphan recovery.

## Elaboration E.11 — Reproducible delivery and feedback latency

Planned. Backlog: PBI-075, PBI-078.

Have a second operator reproduce the supported journey with fresh private
inputs and pinned tools. Compare cold and warm feedback for the same workload,
test tool/cache integrity and expose hidden host dependencies before
recommending setup or concurrency changes.

## Elaboration E.12 — Compatible Foundation upgrade and catch-up

Planned. Backlog: PBI-048, PBI-081.

Demonstrate the compatible language extension while unchanged consumers
continue operating. Preserve retained data through upgrade and recovery,
then validate live backfill/catch-up without losing or overwriting concurrent
changes. This establishes the data boundary for the breaking transition.

## Elaboration E.13 — Breaking Foundation transition and recovery

Planned. Backlog: PBI-082, PBI-049.

Validate bridge consistency and recovery before moving one consumer to
Foundation 2.0 while the other remains on 1.x. Exercise partial dual writes,
shared-data visibility and return to legacy operation before demonstrating
supported retirement.

## Elaboration E.14 — Component windows and architecture assessment

Planned. Backlog: PBI-050, PBI-080.

Demonstrate separate Hello and World migration windows and interrupted-component
recovery using the qualified mixed-version fixtures. Review the accumulated
evidence and remaining risks to recommend Construction or further Elaboration;
the Product Owner makes the architecture milestone decision separately.

The [plan](PLAN.md) owns assignments and activation; the
[validation programme](docs/validation-programme.md) explains dependencies and
evidence boundaries. The [original Foundation scope](progress/E.5/sprint_E.5_proposedchanges.md)
remains input for E.12–E.14. These are Elaboration experiments; production
completion belongs to Construction.

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
