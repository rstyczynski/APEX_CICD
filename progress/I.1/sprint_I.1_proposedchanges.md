# Sprint I.1 — Proposed changes

## Product scope and refinement

Status: Proposed

Retain PBI-003 through PBI-010 in I.1 and PBI-011 through PBI-016 in E.1. Keep E.1 Planned. Refine its objective to proving one safe release path: compatible tools/target guards, a minimal Hello/World/history slice, a reviewed source archive, additive schema change, repeat deployment, deliberate failure after committed DDL, and forward repair with retained history. Gather actual automated browser evidence for the slice. Include the six reconciled contracts in [final engineering decisions](analysis_review-answers_2.md): semantic ownership/provenance, exact-byte qualification, restricted verification, partial-state repair, the single-host proof and Foundation-first assembly. Prove minimal atomic reservation/reassignment early, after control/topology bootstrap; then capture/integration, qualification and guarded repair support the full A/B/C demonstration. Defer complete pages and remote runner integration when unnecessary to retire those risks; the slice is not the release.

At E.1 setup/design, refine PBI-011 into bounded `PBI-011.n` children with outcomes, acceptance evidence and dependencies; obtain approval before prototype construction. Do not create those children in I.1. Use PBI-012 evidence to refine requirements/architecture in PBI-013/014, assess Lifecycle Architecture in PBI-015 and formulate Construction in PBI-016. If critical risks survive, propose further Elaboration. This replaces no assigned PBI.

## Proposed backlog continuation, in priority order

Status: Proposed

The root backlog stops at planning Construction. Propose these product outcomes after PBI-016. IDs are proposed reservations only; recheck the next available numbers before rup-backlog promotion. They have no sprint assignments or board rows.

### PBI-017. Complete the greeting application and preserved history

Provide the Hello and World data/configuration journeys and greeting history needed to make a visible component change meaningful. Preserve existing greeting snapshots through later changes and releases.

Test: Demonstrate independent component edits, valid and rejected greetings, and unchanged earlier history across the selected upgrade.

### PBI-018. Deliver the reviewed automated release and repair path

Let an operator promote a reviewed application/database change using one traceable release artifact and automated checks. Block failing changes and support a demonstrated repair without losing greeting history.

Test: Demonstrate initial assembly from the reviewed seed or verified UC-12 adoption; task preparation/capture and PR integration; A/Foundation, B/Hello and C/World with concurrent distinct-component work and exactly-one-winner Hello reservation. Qualify exact post-merge archive bytes and promote them unchanged. Demonstrate version compatibility, shared-scope/provenance enforcement, drift rejection, restricted maintenance verification, repeat deployment and inspected partial-state repair with retained history and source/artifact receipts. Covers UC-1/4/5/7/9/10/11/12 and FR-5–13.

### PBI-019. Reproduce and hand over the local delivery example

Enable a second operator to reproduce the selected workflow and understand why it was selected over alternatives. Provide operating guidance with prerequisites, actual results and material limitations.

Test: Have a second operator follow the selected single-host onboarding and complete task-to-release walkthrough, including the initial adoption/greenfield distinction, early component conflict, successful qualified promotion and documented failure/repair; record feedback and limits without claiming remote-workstation support. Covers UC-6/8–12 and NFR-1–3.

These outcomes trace respectively to UC-2/3, UC-1/4/5/7/9–12 and UC-6/8–12 in the [SRS](../../docs/srs.md). Priority follows architecture risk retirement, visible application behavior, release automation, then independent reproduction. Existing priorities and assignments remain unchanged until acceptance. Schedule Construction/Transition from E.1 evidence, without speculative extra sprints.

## Three-component compatibility refinement

Status: Proposed

The Product Owner requires explicit Foundation, Hello and World versions and pipeline validation of the complete component combination. Include an accepted and a rejected version set in E.1's risk validation and in the release path acceptance evidence proposed for PBI-018. Apply Foundation first and preserve history across supported upgrades. The updated SRS/architecture specify this without creating extra PBIs, schedules, applications or a dependency resolver.

## Parallel development refinement

Status: Proposed

Include UC-7's focused-page and two-developer integration experiment in E.1's risk retirement, under the existing PBI-011/012 refinement gate. Use the selected single-host private-area proof; first establish resource feasibility, ordinary privilege separation and stable export identities; do not assume a Git branch or APEX Working Copy isolates database objects. Use concurrent Hello/World page additions, shared bookkeeping/dependency attribution, deletion and migration ordering. Same-component competing managed tasks are rejected early; same-page merge conflicts remain a controlled out-of-tool/break-glass case. Retain safe scope expansion and attribution when incorporating accepted changes. Add collaboration/rebuild evidence to the proposed PBI-018 release acceptance; keep its root promotion/assignment pending. No extra sprint or new runtime is created.

## Drift, break-glass use and state refinement

Status: Proposed

The Product Owner requested updating the design with Git-controlled delivery, Working Copies reserved for break-glass use, live drift checks and inherited component/page states. Cover FR-9/10 through the existing PBI-011/012 risk refinement checkpoint: prioritize a guarded round-trip with stale-target rejection, fingerprint coverage, state enforcement and repair. Retain collaboration validation; if combined prototype scope is too large, return a focused split or simpler experiment for approval. Do not create children or start E.1 in I.1. Proposed release outcome PBI-018 must include drift reconciliation and state/ concurrency protection before it can claim a controlled delivery path.


## Infrastructure procedure ownership

Status: Proposed

By explicit Product Owner direction, I.1 owns `docs/deploy.md` as the infrastructure lifecycle procedure; architecture depends on that procedure, not a particular running VM. E.1 must take it and the supporting scripts, assume execution/adaptation responsibility, record exact revisions/versions and validate provisioning, access and teardown for its chosen topology. I.1's analysis reference is Podman 6.0.0, database 23.26.3.0.0, APEX 24.2.0 and ORDS 25.3.0.r2671248 on 2026-10-16. Use create/destroy operations for owned disposable experiment infrastructure as needed, preserving retained data, credentials and unrelated resources. This records the Elaboration handoff without activating E.1 or executing a lifecycle operation now.


## Initial Git adoption and actor-led developer lifecycle

Status: Proposed

The Product Owner requested a separate actor model, developer onboarding and the complete cycle, then identified initial repository adoption from a source application as a prerequisite to Git authority. SRS UC-8–12 and FR-11/12 now cover those outcomes, retaining UC-1–7 identities. E.1's PBI-011/012 refinement must include a bounded initial-capture/reconstruction and onboarding/task-to-release demonstration before claiming developer reproducibility. The proposed PBI-019 handover scope must start before repository access/tooling setup, and proposed PBI-018 must preserve the transition from reviewed initial adoption to Git-controlled releases. No root backlog promotion, new sprint assignment or implementation is performed here.


## Core multi-developer proof of concept

Status: Proposed

The Product Owner requires the complete developer journey to demonstrate A delivering Foundation, B delivering Hello, C delivering World, then competing B/C Hello changes with one rejected as early as possible. This is core proof-of-concept acceptance under PBI-011/012, not an optional extension. The implementor proposes component-scope reservation before managed task editing in UC-9; separate component work may proceed in parallel, while conflicting component tasks are rejected. IT-5/12 define the future evidence, and IT-8 retains the separate deployment-race check. The coarser ownership requirement supersedes earlier normal same-module parallel-page assumptions. No child PBIs, schedules or implementation are created during Inception.
