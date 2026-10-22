# E.1 — Prototype assessment and proposed next work

E.1 was explicitly closed by the Product Owner on 2026-10-18 and is **Done** in [PLAN](../../PLAN.md) and the [progress board](../../PROGRESS_BOARD.md). The evidence-level item statuses and remaining criteria below preserve the pre-closure assessment; they are not claims that unexecuted gates passed. See the [closure handover](sprint_E.1_handover.md#sprint-closure).

Read this alongside the [handover](sprint_E.1_handover.md), [presentation walkthrough](sprint_E.1_increment_demo.md), [accepted prototype design](sprint_E.1_design.md), [SRS](../../docs/srs.md), [architecture](../../docs/architecture.md) and [test profile](../../docs/test-profile.md). The requirements and board own scope/status; this document assesses evidence and proposes the next decision.


The [first external review](sprint_E.1_review-1.md) and [engineering response](sprint_E.1_review-1-response.md) add concrete reproducibility, privileged-input, migration-recovery, exit-status and provenance findings. In particular, the demonstrated host rebuild retains archives; the initial release-input acquisition defect is addressed by [exact archive reconstruction](cicd-walkthrough.md#prepare-reviewed-release-inputs), and the [independent clean-checkout A–I rehearsal](tests/clean_checkout_20261018.txt) now passes from newly provisioned infrastructure. Six selected corrections are registered individually in the [bug register](sprint_E.1_bugs.md). This API-driven rehearsal supplements the earlier assisted walkthrough; wider sprint gates remain open.

## What the selected walkthrough established

The operator can build a greenfield Foundation/Hello/World application from reviewed source snapshots, install an immutable Git-built release in integration_test and promote the same archive to user_acceptance_test. The prototype runs in separate workspaces/schemas on one host. It does not copy developer business data into deployment targets.

The compatible Hello 1.0.1 release passes both fresh-install and baseline-upgrade integration testing before UAT upgrade. The handover check confirms that every field of **21 earlier greeting-history rows**, earlier entries and the full configuration still matches E's saved baseline. New history may append. Foundation and World remain 1.0.0.

The compatibility gate rejects a proposed Foundation 2.0.0 while Hello/World declare Foundation 1.0.0 dependencies. The drift gate rejects an actual Page Designer change without overwriting it. Both validate unchanged target/control snapshots around the rejected preflight. The regular `drift --show` command captures native live source and compares it with the exact successful archive, allowing an explicit keep/undo decision.

These controls demonstrate the value of accepted source, component versions, explicit dependencies, immutable migrations, archive hashes, deployment receipts and live fingerprints together. Component versions alone do not identify actual installed content. The exact-version rules cover the prototype's two supported component triples, not arbitrary semantic-version range resolution.

## Assigned outcomes and current status

### PBI-011 — Executable architectural prototype

Item evidence status at closure: **under_construction**. Its selected delivery/patch/protection slice has substantial working evidence. The full parent acceptance scope remains incomplete.

1. [PBI-011.1](sprint_E.1_design.md#pbi-0111--toolchain-lifecycle-and-isolated-areas), **tested**: pinned tools, separate infrastructure/project provisioning, identity and cross-area isolation evidence. Current platform: SQLcl 25.3.0.274.1210, Java 21.0.12.1+1, Database 23.26.3.0.0 and APEX 24.2.0. Preserve the lifecycle boundary in [deploy.md](../../docs/deploy.md).
2. [PBI-011.2](sprint_E.1_design.md#pbi-0112--durable-atomic-reservations), **under_construction**: durable package-controlled reservations support the sequential journey. Synchronized competing Hello clients, scope expansion and safe reassignment evidence remain incomplete.
3. [PBI-011.3](sprint_E.1_design.md#pbi-0113--foundation-first-assembly), **tested**: Foundation-first construction declares absent components accurately and keeps incomplete applications unavailable.
4. [PBI-011.4](sprint_E.1_design.md#pbi-0114--stable-capture-and-reconstruction), **under_construction**: repeated native capture and reconstruction evidence exists. Comprehensive private-target identity, deletion and capture-reconciliation acceptance is not complete.
5. [PBI-011.5](sprint_E.1_design.md#pbi-0115--parallel-helloworld-integration), **under_construction**: accepted sequential contributions produce a complete application. Independent simultaneous branches/clients and full conflict/provenance proof remain open.
6. [PBI-011.6](sprint_E.1_design.md#pbi-0116--qualify-and-promote-identical-artifacts), **under_construction**: D/E initial release and F fresh/upgrade patch receipts establish the selected identical-artifact path. The full child criterion, including its dependencies and complete repeat/tamper/stale-candidate negative coverage, has not received a complete gate/acceptance review.
7. [PBI-011.7](sprint_E.1_design.md#pbi-0117--compatibility-drift-and-maintenance), **under_construction**: selected incompatibility, live-page drift, restricted verification and guarded publication work. Schema-definition drift, competing deployments, in-flight requests, stale workers and full verifier fencing remain open.
8. [PBI-011.8](sprint_E.1_design.md#pbi-0118--failed-additive-deployment-and-forward-repair), **under_construction**: the [bounded integration-only failure/forward-repair proof](tests/recovery_proof_20261018.txt) now passes with committed DDL, retained attempts, changed-observation rejection and preserved history. Full IT-3/9 unknown-state/concurrency/session coverage and gate reconciliation remain open.

### PBI-012 — Validate critical assumptions and use cases

Item evidence status at closure: **under_design**. Selected native/browser/receipt evidence is collected in the [test record](sprint_E.1_tests.md) and [handover checks](tests/handover_checks_20261018.txt). The remaining child proofs, complete gate reconciliation, resource/timing measurements and independent reproduction limits still need assessment. Focused test successes do not mean that the full smoke/unit/integration contract has passed.

### PBI-013 — Refine use cases and supplementary requirements

Item evidence status at closure: **under_design**. Preserve these findings in the existing requirements refinement:

1. UC-4/FR-6/FR-8: an accepted Git revision supplies the release, while C is a private development assembly.
2. UC-5/FR-10: expose drift details before the operator chooses restoration or reviewed Git reconciliation. Preserve unexpected source and refuse silent baseline adoption.
3. UC-8/FR-13: infrastructure initialization ends at DB/APEX/ORDS; delivery control and each project area have separate provisioning steps.
4. UC-11: distinguish missing browser verification, successful publication and later test-data preparation. Checkpoint continuation must not become arbitrary partial-deployment repair.

The current [SRS](../../docs/srs.md) remains authoritative. This is evidence for final refinement, not blanket reacceptance of every requirement.

### PBI-014 — Stabilize the architecture baseline

Item evidence status at closure: **under_design**. Retain explicit SQLcl/APEX interfaces, immutable migration files, source-built archives, separate E1_CTRL authority and private logical areas. The selected one-host topology is feasible for this lab. Keep the wider ownership/fencing/schema-drift/repair architecture provisional until its evidence exists. No general delivery platform is warranted by this prototype.

### PBI-015 — Lifecycle Architecture assessment

Item evidence status at closure: **under_design**. Recommendation: **further focused Elaboration**. The happy path and selected protections are useful and reviewable, but the core collaboration/exclusion/repair risks remain material to the accepted release. The current evidence does not justify full Lifecycle Architecture acceptance or production readiness.

### PBI-016 — Construction plan

Item evidence status at closure: **under_design**. Proposed order, subject to Product Owner selection:

1. Finish the missing architectural proofs below and reconcile their full test outcomes.
2. Review requirements and architecture against that evidence, then decide Lifecycle Architecture.
3. If accepted, complete a reproducible operator reference and release workflow for Construction. The separately proposed [PBI-017](../../BACKLOG.md#pbi-017-deliver-a-repository-and-pipeline-reference-guide) is **Proposed and unscheduled**; its [repository guide](repo_layout.md) remains a draft.

No C.n or follow-up Elaboration sprint is created or activated by this document.

## Proposed focused Elaboration follow-up

Use the existing child definitions and the proposed follow-up backlog references below to select the remaining proof:

1. **Reservation and collaboration proof:** synchronize competing Hello requests, prove exactly one winner and an early unchanged loser, then integrate genuine parallel Hello/World contributions. PBI-011.2/.5, IT-6/12 and the integration cases own this evidence.
2. **Deployment and maintenance proof:** exercise competing attempts, stale epochs/workers, interrupted processes, existing sessions and verifier revocation. Extend the drift comparison to the scoped database definitions. PBI-011.7 and IT-7/8/9 own this evidence.
3. **Broader recovery proof:** retain the now-passing bounded additive-failure experiment and validate additional supported partial states, interruptions and unknown-state rejection. PBI-011.8 and IT-3/9 retain the current evidence contract.

Reuse the same host, application and public Oracle interfaces. The original design estimates for these full children were 4–6, 6–10, 6–10 and 4–6 engineering hours respectively; they are planning assumptions, not measured remaining effort. Re-estimate the selected remainder before scheduling. No fresh throughput/resource benchmark or actual total engineering-cost claim is available from this handover.

## Review decision requested

Review the demonstrated slice and the recommendation above. Decide whether to complete the missing proofs within E.1 or revise its accepted boundary and schedule further Elaboration through the existing backlog/sprint procedures. The Product Owner has now closed this iteration; remaining acceptance work is represented by the follow-up backlog without activating another sprint.

## Open-work backlog coverage

The Product Owner requested backlog coverage for all known open problems on 2026-10-18. The items below are **Proposed and unscheduled**. They expose remaining outcomes for future selection; they do not transfer, remove or complete the existing E.1 child criteria. Selecting a follow-up sprint must reconcile that overlap explicitly through the sprint procedure.

### Remaining architectural and acceptance proofs

1. [PBI-018 — atomic reservations](../../BACKLOG.md#pbi-018-prove-atomic-task-reservations-under-contention) covers PBI-011.2, IT-6/12: synchronized contention, expanded scope and reassignment.
2. [PBI-019 — parallel collaboration](../../BACKLOG.md#pbi-019-prove-parallel-component-collaboration-and-integration) covers PBI-011.5, UC-7/9/10 and IT-5/6/11: independent branches/areas, provenance and safe integration.
3. [PBI-020 — APEX capture/reconstruction](../../BACKLOG.md#pbi-020-complete-apex-capture-and-reconstruction-validation) covers PBI-011.4, IT-1/6/7 and review R1-M2's broader boundary: private target identities, deletion, shared metadata and explicitly supported user state beyond the one saved-report proof.
4. [PBI-021 — release admission negatives](../../BACKLOG.md#pbi-021-complete-release-admission-and-promotion-negative-coverage) covers PBI-011.6 and IT-1/2: remaining repeat/tamper/stale-evidence and unsupported-start cases.
5. [PBI-022 — deployment/maintenance fencing](../../BACKLOG.md#pbi-022-prove-deployment-ownership-and-maintenance-fencing) covers PBI-011.7 and IT-8/9: competing attempts, stale workers/epochs, interruption, active sessions/direct submits and verifier revocation.
6. [PBI-023 — schema drift/reconciliation](../../BACKLOG.md#pbi-023-detect-schema-drift-and-reconcile-unauthorized-changes) covers PBI-011.7, UC-5 and IT-7: scoped database definitions and explicit keep/restore/reconcile outcomes. The retained manual APEX edit still needs the operator decision described in the handover; creating this item does not authorize overwriting it.
7. [PBI-024 — broader partial-state recovery](../../BACKLOG.md#pbi-024-validate-recovery-beyond-the-selected-additive-failure) covers the remainder of PBI-011.8 and IT-3/9. The passing bounded BUG-7 experiment remains evidence, not an open defect.
8. [PBI-034 — browser acceptance](../../BACKLOG.md#pbi-034-automate-application-browser-acceptance-checks) covers the browser contract in the [test profile](../../docs/test-profile.md#required-evidence-not-tests-implemented-in-i1) and user-facing UC-2/3/11 behavior; API fixtures and SQL checks do not establish that complete contract.

Full gate reconciliation, risk/resource/timing assessment, requirement refinement, architecture stabilization, Lifecycle Architecture decision and Construction planning remain assigned to **PBI-012–016**. The consolidated repository/operator reference remains **PBI-017**. These existing outcomes need no duplicate backlog entries. Requirements, current test specifications and the board continue to own their respective scope, evidence contract and status.

### Deferred review concerns and conditional extensions

1. [PBI-025 — privileges and credentials](../../BACKLOG.md#pbi-025-restrict-privileges-and-protect-deployment-credentials): R1-H2's remaining shared-service boundary; validated lab input handling is already fixed.
2. [PBI-026 — gateway exposure](../../BACKLOG.md#pbi-026-minimize-gateway-exposure-for-shared-hosting): R1-L2, before shared or remote hosting.
3. [PBI-027 — environment configuration](../../BACKLOG.md#pbi-027-unify-delivery-environment-configuration): R1-M3, broader consolidation after current strict validation.
4. [PBI-028 — release/toolchain profiles](../../BACKLOG.md#pbi-028-extend-supported-release-and-toolchain-profiles): R1-M4, when another supported release/toolchain is selected; no general version solver is requested.
5. [PBI-029 — diagnostics](../../BACKLOG.md#pbi-029-strengthen-automation-failure-diagnostics): R1-M6, broader client diagnostic coverage; existing exit/marker fixes remain complete.
6. [PBI-030 — hosted source CI](../../BACKLOG.md#pbi-030-automate-source-validation-in-hosted-ci): R1-L3 and the [future pipeline](repo_layout.md#future-pipeline-automation); database-independent checks first.
7. [PBI-031 — independent validation provenance](../../BACKLOG.md#pbi-031-establish-independent-release-validation-provenance): R1-M5's deferred shared-runner attestation boundary; complete local test provenance is already fixed.
8. [PBI-032 — licensing/reference distribution](../../BACKLOG.md#pbi-032-resolve-repository-licensing-and-reference-distribution): R1-L4; the owner decision remains open and public visibility is not license clearance.
9. [PBI-033 — additional host platform](../../BACKLOG.md#pbi-033-validate-an-additional-infrastructure-host-platform): the explicitly deferred Linux/other-host infrastructure proof, conditional on selecting that platform.
10. [PBI-035 — existing-application adoption](../../BACKLOG.md#pbi-035-validate-adoption-of-an-existing-apex-application): UC-12/IT-10, retained as a future adoption path. The current prototype remains greenfield and does not construct this path or package business seed data.

These proposals record the concerns without treating shared hosting, additional platforms or existing-application adoption as current E.1 implementation requirements. Related review dispositions remain in [review decisions](sprint_E.1_review-1-decisions.md), and demonstrated corrections remain in the [bug register](sprint_E.1_bugs.md).
