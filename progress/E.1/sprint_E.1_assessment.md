# E.1 — Prototype assessment and proposed next work

Prepared for Product Owner review on 2026-10-18. E.1 remains **Progress** in [PLAN](../../PLAN.md) and **under_construction** on the [progress board](../../PROGRESS_BOARD.md). This assessment does not change either status.

Read this alongside the [handover](sprint_E.1_handover.md), [presentation walkthrough](sprint_E.1_increment_demo.md), [accepted prototype design](sprint_E.1_design.md), [SRS](../../docs/srs.md), [architecture](../../docs/architecture.md) and [test profile](../../docs/test-profile.md). The requirements and board own scope/status; this document assesses evidence and proposes the next decision.


The [first external review](sprint_E.1_review-1.md) and [engineering response](sprint_E.1_review-1-response.md) add concrete reproducibility, privileged-input, migration-recovery, exit-status and provenance findings. In particular, the demonstrated host rebuild retains archives; independent reproduction from a public clone remains blocked until release acquisition/build is supplied. Review responses propose corrections; they do not claim implemented fixes.

## What the selected walkthrough established

The operator can build a greenfield Foundation/Hello/World application from reviewed source snapshots, install an immutable Git-built release in integration_test and promote the same archive to user_acceptance_test. The prototype runs in separate workspaces/schemas on one host. It does not copy developer business data into deployment targets.

The compatible Hello 1.0.1 release passes both fresh-install and baseline-upgrade integration testing before UAT upgrade. The handover check confirms that every field of **21 earlier greeting-history rows**, earlier entries and the full configuration still matches E's saved baseline. New history may append. Foundation and World remain 1.0.0.

The compatibility gate rejects a proposed Foundation 2.0.0 while Hello/World declare Foundation 1.0.0 dependencies. The drift gate rejects an actual Page Designer change without overwriting it. Both validate unchanged target/control snapshots around the rejected preflight. The regular `drift --show` command captures native live source and compares it with the exact successful archive, allowing an explicit keep/undo decision.

These controls demonstrate the value of accepted source, component versions, explicit dependencies, immutable migrations, archive hashes, deployment receipts and live fingerprints together. Component versions alone do not identify actual installed content. The exact-version rules cover the prototype's two supported component triples, not arbitrary semantic-version range resolution.

## Assigned outcomes and current status

### PBI-011 — Executable architectural prototype

Official status: **under_construction**. Its selected delivery/patch/protection slice has substantial working evidence. The full parent acceptance scope remains incomplete.

1. [PBI-011.1](sprint_E.1_design.md#pbi-0111--toolchain-lifecycle-and-isolated-areas), **tested**: pinned tools, separate infrastructure/project provisioning, identity and cross-area isolation evidence. Current platform: SQLcl 25.3.0.274.1210, Java 21.0.12.1+1, Database 23.26.3.0.0 and APEX 24.2.0. Preserve the lifecycle boundary in [deploy.md](../../docs/deploy.md).
2. [PBI-011.2](sprint_E.1_design.md#pbi-0112--durable-atomic-reservations), **under_construction**: durable package-controlled reservations support the sequential journey. Synchronized competing Hello clients, scope expansion and safe reassignment evidence remain incomplete.
3. [PBI-011.3](sprint_E.1_design.md#pbi-0113--foundation-first-assembly), **tested**: Foundation-first construction declares absent components accurately and keeps incomplete applications unavailable.
4. [PBI-011.4](sprint_E.1_design.md#pbi-0114--stable-capture-and-reconstruction), **under_construction**: repeated native capture and reconstruction evidence exists. Comprehensive private-target identity, deletion and capture-reconciliation acceptance is not complete.
5. [PBI-011.5](sprint_E.1_design.md#pbi-0115--parallel-helloworld-integration), **under_construction**: accepted sequential contributions produce a complete application. Independent simultaneous branches/clients and full conflict/provenance proof remain open.
6. [PBI-011.6](sprint_E.1_design.md#pbi-0116--qualify-and-promote-identical-artifacts), **under_construction**: D/E initial release and F fresh/upgrade patch receipts establish the selected identical-artifact path. The full child criterion, including its dependencies and complete repeat/tamper/stale-candidate negative coverage, has not received a complete gate/acceptance review.
7. [PBI-011.7](sprint_E.1_design.md#pbi-0117--compatibility-drift-and-maintenance), **under_construction**: selected incompatibility, live-page drift, restricted verification and guarded publication work. Schema-definition drift, competing deployments, in-flight requests, stale workers and full verifier fencing remain open.
8. [PBI-011.8](sprint_E.1_design.md#pbi-0118--failed-additive-deployment-and-forward-repair), **under_design**: no failed additive deployment with a reviewed automated forward-repair archive has been demonstrated. A rejected preflight, fixture cleanup or verification continuation does not meet this criterion.

### PBI-012 — Validate critical assumptions and use cases

Official status: **under_design**. Selected native/browser/receipt evidence is collected in the [test record](sprint_E.1_tests.md) and [handover checks](tests/handover_checks_20261018.txt). The remaining child proofs, complete gate reconciliation, resource/timing measurements and independent reproduction limits still need assessment. Focused test successes do not mean that the full smoke/unit/integration contract has passed.

### PBI-013 — Refine use cases and supplementary requirements

Official status: **under_design**. Preserve these findings in the existing requirements refinement:

1. UC-4/FR-6/FR-8: an accepted Git revision supplies the release, while C is a private development assembly.
2. UC-5/FR-10: expose drift details before the operator chooses restoration or reviewed Git reconciliation. Preserve unexpected source and refuse silent baseline adoption.
3. UC-8/FR-13: infrastructure initialization ends at DB/APEX/ORDS; delivery control and each project area have separate provisioning steps.
4. UC-11: distinguish missing browser verification, successful publication and later test-data preparation. Checkpoint continuation must not become arbitrary partial-deployment repair.

The current [SRS](../../docs/srs.md) remains authoritative. This is evidence for final refinement, not blanket reacceptance of every requirement.

### PBI-014 — Stabilize the architecture baseline

Official status: **under_design**. Retain explicit SQLcl/APEX interfaces, immutable migration files, source-built archives, separate E1_CTRL authority and private logical areas. The selected one-host topology is feasible for this lab. Keep the wider ownership/fencing/schema-drift/repair architecture provisional until its evidence exists. No general delivery platform is warranted by this prototype.

### PBI-015 — Lifecycle Architecture assessment

Official status: **under_design**. Recommendation: **further focused Elaboration**. The happy path and selected protections are useful and reviewable, but the core collaboration/exclusion/repair risks remain material to the accepted release. The current evidence does not justify full Lifecycle Architecture acceptance or production readiness.

### PBI-016 — Construction plan

Official status: **under_design**. Proposed order, subject to Product Owner selection:

1. Finish the missing architectural proofs below and reconcile their full test outcomes.
2. Review requirements and architecture against that evidence, then decide Lifecycle Architecture.
3. If accepted, complete a reproducible operator reference and release workflow for Construction. The separately proposed [PBI-017](../../BACKLOG.md#pbi-017-deliver-a-repository-and-pipeline-reference-guide) is **Proposed and unscheduled**; its [repository guide](repo_layout.md) remains a draft.

No C.n or follow-up Elaboration sprint is created or activated by this document.

## Proposed focused Elaboration follow-up

Use the existing child definitions rather than inventing more platform features:

1. **Reservation and collaboration proof:** synchronize competing Hello requests, prove exactly one winner and an early unchanged loser, then integrate genuine parallel Hello/World contributions. PBI-011.2/.5, IT-6/12 and the integration cases own this evidence.
2. **Deployment and maintenance proof:** exercise competing attempts, stale epochs/workers, interrupted processes, existing sessions and verifier revocation. Extend the drift comparison to the scoped database definitions. PBI-011.7 and IT-7/8/9 own this evidence.
3. **Failure and forward repair:** deliberately fail after committed additive DDL, preserve attempts and history, qualify a new repair archive against the identified partial start, then repair automatically after the review decision. PBI-011.8 and IT-3/9 own this evidence.

Reuse the same host, application and public Oracle interfaces. The original design estimates for these full children were 4–6, 6–10, 6–10 and 4–6 engineering hours respectively; they are planning assumptions, not measured remaining effort. Re-estimate the selected remainder before scheduling. No fresh throughput/resource benchmark or actual total engineering-cost claim is available from this handover.

## Review decision requested

Review the demonstrated slice and the recommendation above. Decide whether to complete the missing proofs within E.1 or revise its accepted boundary and schedule further Elaboration through the existing backlog/sprint procedures. Until that decision and the remaining acceptance work, leave E.1 open.
