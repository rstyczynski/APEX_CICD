# Sprint I.1 — Design

Status: Accepted

The Product Owner explicitly accepted the revised I.1 analysis baseline with the presentation wording correction on 2026-10-16 in the E.1 startup instruction. This accepts the Inception direction and evidence obligations, not the unbuilt prototype. Earlier pending-approval statements below describe the proposal history and are superseded by this decision. Handover acceptance and closure are tracked separately in the handover record.

## Baseline and scope

PBI-003 through PBI-010 deliver a research-backed Inception baseline, not an application. The [SRS](../../docs/srs.md) contains UC-1 through UC-12 and FR-1 through FR-13. The [architecture](../../docs/architecture.md) and [research](../../docs/cicd-research.md) distinguish documented APEX capabilities, user-directed policy, proposed implementation and unrun validation. E.1 remains Planned. This update records feedback; it is not overall design acceptance.

## Requirements and priorities — PBI-003 through PBI-008

The SRS now explicitly enumerates A-01 Developer, A-02 Reviewer/integration maintainer, A-03 Delivery operator, A-04 Laboratory application user and A-05 Git hosting service in a separate Actors chapter. Stakeholders and internal components are distinguished. Each use case identifies its primary/supporting actors, preconditions, main/alternative flows, postcondition, success criterion and requirement references. The developer's cycle starts with onboarding; application adoption establishes the initial golden Git baseline before ordinary branch work. Its core acceptance journey assigns Foundation to developer A, Hello to B and World to C, permits B/C work on distinct components, then rejects exactly one simultaneous Hello task in UC-9 before editing. Early authoring ownership is distinct from target deployment serialization.

Establish the database Foundation first, then Hello/World behavior and preserved greeting history. All three components have explicit semantic versions and compatibility declarations. The implementor recommends capturing browser-authored changes through SQLcl into a local task-branch checkout, then submitting focused-page or module changes through PRs. CI validates the combined candidate; CD installs the accepted revision through our tool. State metadata and drift protection are first-class requirements alongside interface/version compatibility.

The SRS defines boundary, stakeholders, use cases, measurable behavior, scope, exclusions and eleven risks. The [proposal](sprint_I.1_proposedchanges.md) retains assigned PBIs and proposes product-level continuation. Backlog promotion, priorities and future assignment await their managed decision; no new schedule or prototype children are created here.

## Candidate controls — PBI-009

Propose split APEX exports and explicit migrations through SQLcl's bundled Liquibase; PROJECT remains the integrated alternative. The exact toolchain, runner and affordable developer-target topology still require approval/validation. I.1 owns [docs/deploy.md](../../docs/deploy.md) as the infrastructure lifecycle procedure. The analysis reference is Podman 6.0.0, database 23.26.3.0.0, APEX 24.2.0 and ORDS 25.3.0.r2671248. E.1 must take this procedure and supporting scripts, assume execution/adaptation responsibility, and validate create/verify/destroy operations for its experiment targets. A running VM is not a dependency; retained data, credentials and unrelated resources remain protected. Supporting sources need a reviewed adoption commit before reproducibility can be claimed.

The implementor owns the branch/PR/CI/CD recommendation and its technical rationale. Git is authoritative for accepted code/policy; target receipts record actual installed state. The architecture now specifies the missing developer capture step: branch/base-to-target mapping, staged split export, scoped file reconciliation, migration/version updates, diff review and commit. Native Working Copies are reserved for break-glass diagnosis/ repair. A controlled target must not acquire unreviewed changes through native merge or browser editing without drift detection and reconciliation.

The architecture's **Drift detection and expected-revision guard** chapter defines live APEX CHECKSUM-SH256 comparison, separate scoped schema drift, guarded revision checks and protected export/reconciliation. The **Component and page state machine** chapter defines ready/maintenance/failed, parent inheritance, proposed ancestor/dependency vetoes, controlled transitions and runtime enforcement. A blocked precheck is an attempt outcome, not automatic target failure. These are project controls; no claim is made that APEX natively supplies this hierarchy or that a pipeline lock constrains an unrestricted administrator.

SRS FR-13 requires automated lifecycle operations through available Oracle tools and supported interfaces. The architecture enumerates AI-1–10 with tool, purpose, interface, access and Elaboration proof. Project orchestration composes these capabilities; native APEX APIs do not supply the custom version/ownership/state policy. The test profile requires evidence for the selected interfaces, including automated browser behavior; manual administration is not a substitute for an unresolved automation path. These remain proposed and unvalidated.

## Final expert review reconciliation

[Review 2](analysis_review_2.md) and the [final engineering decisions](analysis_review-answers_2.md) reconcile R1–R6 in the SRS, architecture and test profile. Select the single-host proof; use the existing three reservation scopes with semantic ownership and inherited-change provenance; bootstrap logically separate durable control authority; explicitly permit restricted Foundation-first assembly; qualify exact post-merge archive bytes before promotion; verify through a narrowly scoped maintenance exception; and recover from an inspected, approved partial state. The supported matrix is fresh complete installation, one declared additive upgrade and the chosen injected-failure repair. No fourth component, separate service or arbitrary-state repair engine is required.

The continuation proposal consolidates the newer journeys/controls. Elaboration first validates bootstrap/topology and minimal atomic reservations, then assembly/capture, artifact qualification and guarded repair before the complete A/B/C proof. These are corrected document contracts with future evidence, not accepted design or implemented behavior.

## Coherent review — PBI-010

After design acceptance, reconcile all baseline artifacts and approved backlog/ plan changes. Assess each assigned acceptance criterion, audit completed increments and commit them. The [P9 presentation pair](sprint_I.1_increment_demo.md) is prepared at the Product Owner's request. Conduct the presenter-led artifact inspection and record the actual decision before handover acceptance/closure. No application construction, E.1 activation or push is authorized by this document update.

### Testing Strategy

I.1 keeps Test: none and Regression: none. No application code, PL/SQL tests or test skeletons are created or run. Use document/source/consistency review and record mechanical checks honestly. Future commands and SM/UT/IT cases are defined once in the [test profile](../../docs/test-profile.md), explicitly proposed and unrun. Prioritize E.1's guarded round-trip, drift/concurrency/state risks and the core A/B/C multi-developer cycle and early same-Hello reservation race during its approved decomposition; if the scope exceeds one useful experiment, return a refinement proposal rather than silently expanding.

## Test Specification

**REV-1 (PBI-003/004/005):** Explicit actor coverage, use-case flows/outcomes and requirement references are traceable; onboarding, initial adoption, the complete developer cycle and Foundation/component/history behavior are testable. **REV-2 (PBI-006/007):** Priorities, release scope and exclusions follow the vision without unapproved assignments. **REV-3 (PBI-008/009):** Risks have owners/validation; sources apply to the selected versions; state, version and fingerprint controls have distinct semantics and future cases. **REV-4 (PBI-010):** The accepted baseline is coherent, records remaining uncertainty and preserves the Elaboration refinement gate.

Code gates A1–A3/B1–B3 and a new-tests manifest are inapplicable, not passed. The documentation audit records actual checks. Final review remains pending.

## Design approval status

The revised Inception baseline is accepted by the explicit Product Owner instruction quoted above. Detailed implementation choices, fingerprint coverage and lock/runtime enforcement require E.1 design approval and technical validation. No successful application behavior is claimed. The separate P9 handover decision remains pending.
