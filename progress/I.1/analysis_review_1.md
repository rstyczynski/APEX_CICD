# I.1 inception analysis review

Review date: 2026-10-16. Scope: Sprint I.1, formerly Sprint 1, PBI-003 through PBI-010. This is an independent assessment of the current working-tree documents, including their latest refinements. It is not Product Owner acceptance, a sprint transition, or evidence of executed application tests.

## Assessment

**The concept is credible and the principal user journeys are covered, but the baseline is not yet gap-free.** It provides a sound direction for Elaboration. Before accepting it as a coherent Inception baseline, clarify the core contracts identified in findings R1–R5 below. Their implementation and technical proof belong in Elaboration; a complete implementation is not required to finish Inception.

The most significant weakness is the interaction between individually sensible controls. Component reservations, full-application exports, PR validation, immutable artifacts, maintenance, drift rejection and recovery are all described. The documents do not yet consistently explain how those controls cooperate when shared metadata changes, a release is rebuilt after merge, or a deployment stops halfway through. These are central to the promised delivery demonstration.

This review does not recommend expanding the example into a production platform. Production backups, high availability, cloud delivery, destructive migrations and independent component deployment remain reasonable exclusions. Nor should the review reopen the explicitly required A/B/C developer journey or early rejection of competing Hello tasks.

## Review basis and limits

Reviewed the accepted [vision](../../README.md), [roadmap](../../ROADMAP.md), [backlog](../../BACKLOG.md), [plan](../../PLAN.md), [SRS](../../docs/srs.md), [candidate architecture](../../docs/architecture.md), [research](../../docs/cicd-research.md), [test profile](../../docs/test-profile.md), and [infrastructure procedure](../../docs/deploy.md). Also reviewed the I.1 [setup](sprint_I.1_setup.md), [design](sprint_I.1_design.md), [change proposal](sprint_I.1_proposedchanges.md), and [documentation audit](sprint_I.1_documentation_audit.md), with the local RUP policies and narrative-document preferences.

The review evaluates internal consistency, actor coverage, APEX-specific feasibility assumptions, release safety and proportionate Inception completeness. Targeted checks against Oracle's version-specific documentation support the technical observations linked below. The supplied lifecycle PDF and historical runtime experiments were not independently revalidated in this review. No environment provisioning, application export/import, deployment, race test or browser test was executed. Existing uncommitted work was treated as the review baseline and preserved.

## What is properly addressed

**Purpose and application scope.** The laboratory has a concrete educational outcome: reproduce a reviewed change, retain history, identify its source/artifact, and demonstrate failure and repair. Hello/World configuration, composition and immutable history are specified sufficiently for Inception. A small application can exercise both APEX metadata and database changes without requiring a larger business domain.

**Actors and end-to-end work.** A-01 through A-05 distinguish developers, reviewers, operators, users and the repository host. UC-8–12 close the often-missed gaps before and after coding: onboarding, initial source adoption, task preparation, capture, feedback and refresh. UC-1–7 cover application behavior, integration, delivery and recovery. The A/B/C scenario and exactly-one-winner Hello race are observable core acceptance criteria.

**APEX and database boundaries.** The baseline correctly distinguishes a Git branch from a live APEX development area, and a Working Copy from isolated schema state. It also separates component versions from release units: Foundation, Hello and World can have distinct versions while being delivered as one application. Explicit migrations and full split exports are a defensible candidate, with SQLcl PROJECT retained as an alternative.

**Data, configuration and failure awareness.** User-maintained settings, target configuration, secrets, source definitions and runtime history have distinct responsibilities. Additive migrations, repeat deployment, retained sentinels and forward repair address the essential database-delivery risks. The documents correctly avoid promising an atomic release across DDL and APEX import.

**Evidence discipline.** Tool/API availability, proposed commands, historical checks and unrun experiments are distinguished. FR-13 and AI-1–10 make automation feasibility visible. Deferring the exact control-store implementation, browser tool versions and export normalization to Elaboration is appropriate, provided those experiments remain explicit acceptance gates.

## Core findings to resolve in the baseline

### R1 — Component ownership needs a rule for shared APEX and delivery assets

**Priority: high.** Evidence: SRS FR-8 and UC-9/10; architecture sections “Early component change ownership,” “Data and application design,” and “Capturing developer changes into a Git branch”; test cases IT-5/6/12.

Hello and World reservations may coexist, and capture must reject changes outside the reserved scope. However, one application also contains shared navigation, application attributes, authentication/authorization, composition code, install controllers, the changelog root and compatibility metadata. The baseline acknowledges cross-task review but does not define how these assets belong to a reservation scope or how necessary generated changes are distinguished from unauthorized semantic changes.

For example, adding a Hello page can also change shared navigation and export install files. Rejecting every shared-file change can prevent the promised independent development; allowing every such change can defeat scope enforcement. Oracle's [split-export example](https://docs.oracle.com/en/database/oracle/apex/24.2/aeadm/exporting-one-or-more-applications.html) explicitly shows a page/shared-component change accompanied by changes to `create_application.sql` and `install.sql`.

**Minimum Inception correction:** state the ownership policy for shared assets, including the shared composition package. Define which semantic changes require a Foundation or multi-component reservation and which generated bookkeeping changes may be reconciled under validation. Explain scope expansion discovered after task acquisition: pause, preserve work, and acquire the additional scope safely or reject it. Do not silently grant ownership during capture.

**Elaboration proof:** extend IT-5/6 with simultaneous Hello/World page additions that touch shared export metadata, plus an unauthorized shared behavior change. Legitimate integration must preserve both changes, while undeclared semantic changes are rejected. Exact file/object mappings can be designed in E.1.

### R2 — Separate PR validation from release-artifact validation and promotion

**Priority: high.** Evidence: SRS UC-4, FR-5 and NFR-2; architecture “Sources, packaging and promotion” and “Developer/task integration model”; test-profile prerequisites and IT-1/5.

The SRS requires the same package for validation and promotion. The architecture validates combined sources before merge, then builds/promotes an archive from the accepted merged revision. It does not explicitly require the final archive to pass release validation after that build. A passing PR candidate is valuable, but it is not automatically evidence for a later package with a different commit, manifest or packaging result.

There is also an unresolved target role: the architecture mentions a controlled validation area, while the concrete prerequisite list names only LAB_DEV and LAB_TEST and IT-1 deploys directly to TEST. Reusing TEST for unmerged candidates would undermine its role as the accepted promotion target unless its lifecycle is explicitly disposable and reset between roles.

**Minimum Inception correction:** distinguish candidate validation from release qualification. Define a disposable validation role, separate from the accepted TEST installation and its retained history, even if both share one database. After merge, build the release archive once, qualify those exact bytes, and promote them with a receipt referencing their hash and accepted revision. Alternatively, define a precise equivalent artifact-reuse policy; do not rely on assumed equivalence.

**Elaboration proof:** show that a stale PR check, changed final package, or missing final-package evidence blocks promotion. Demonstrate both clean reconstruction and upgrade from the supported installed baseline; a fresh import alone does not prove upgrade safety. Record the unchanged artifact hash across qualification and deployment.

### R3 — Maintenance and browser verification currently form an incomplete transition

**Priority: high.** Evidence: SRS FR-9 and NFR-3; architecture AI-7/9, “Component and page state machine,” and “Failure handling and validation decisions”; IT-9 and browser assertions.

Deployment enters application-wide maintenance, blocks ordinary requests on the server, and becomes ready only after behavior checks pass. Those checks include authenticated browser submissions. The documents do not say how the verifier exercises normal behavior while both native application availability and the custom ancestor/dependency guards deny access. A separate diagnostics path is mentioned, but diagnostics are not necessarily the application behavior being qualified.

**Minimum Inception correction:** define a controlled verification window or identity with narrowly scoped authorization while ordinary users remain blocked. Explain how it interacts with both native APEX availability and project state guards, how in-flight user requests drain, and how it is revoked on success or interruption. This is an operational testing permission, not a requirement for a new business-role subsystem. Specify that the accepted fingerprint represents the final intended availability/configuration, or accounts explicitly for the subsequent availability transition.

Oracle documents restricted access through an allowed-user list in [SET_APPLICATION_STATUS](https://docs.oracle.com/en/database/oracle/apex/24.2/aeapi/APEX_APPLICATION_ADMIN.SET_APPLICATION_STATUS-Procedure.html). That is a candidate primitive; it does not automatically override the proposed custom guards or prove that existing requests have drained.

**Elaboration proof:** ordinary existing sessions and direct submissions remain blocked while an authorized verifier performs the real greeting/history journey. A failing verifier or interrupted controller must not expose the application or leave a reusable bypass.

### R4 — Repair needs an explicit entry contract for known partial state

**Priority: high.** Evidence: SRS UC-5, FR-6/10; architecture “Drift detection and expected-revision guard” and “Failure handling and validation decisions”; IT-3/7/9.

Normal delivery rejects definitions differing from the last successful baseline. A failed migration/import can legitimately leave exactly that difference, along with failed state and an advanced attempt generation. Recovery is said to use the same guarded scope, but the baseline does not explain which expected state authorizes a repair without either rejecting it forever or disabling drift protection. It needs to distinguish recorded partial work from a later unexplained edit.

There is a related ambiguity in the test profile: integration “deploys, repeat-deploys and repairs using the same archive,” while the architecture allows repair with a new reviewed changeset. A new changeset necessarily belongs to a new artifact. Retrying an unchanged artifact and deploying a repair artifact are different cases.

**Minimum Inception correction:** define a recovery attempt linked to the failed attempt, the operator-reviewed observed partial state, expected generation, and approved repair artifact. Preserve the old successful receipt and failure evidence. Require unexplained subsequent changes to block repair too. Clarify when a retry may reuse the original archive and when forward repair requires a newly reviewed archive. Never edit an applied changeset or overwrite the original archive to make a test pass.

**Elaboration proof:** fail after committed DDL, inspect the partial state, reject an unauthorized intervening change, then apply an authorized repair and retain history. Oracle's [COMMIT reference](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqlrf/COMMIT.html) confirms implicit commits around DDL; this failure boundary is central to the concept.

### R5 — Define the supported multi-developer deployment model under loopback-only access

**Priority: medium.** Evidence: SRS complete developer journey, UC-8/9, FR-11 and NFR-1; architecture “Components and boundaries” and “Initial Git adoption and developer onboarding”; infrastructure procedure.

The required scenario has three developer participants, while the assessed services bind to one Mac's loopback. Onboarding offers either operator-provided private areas on a shared platform or developer-local infrastructure. The authoring reservation store must be shared across those participants, but no selected access model connects the alternatives. This is a missing supported-environment statement, not a recommendation to expose database ports.

**Minimum Inception correction:** explicitly select the initial proof model: for example, separate developer identities and private areas exercised on one host, with independently synchronized clients for the race. State that this proves logical concurrency rather than remote workstation connectivity. If separate workstations are required for acceptance, identify their authorized access path and shared reservation authority, and reconcile it with NFR-1. Clarify that only the chosen onboarding variant is promised initially.

**Elaboration proof:** validate the chosen topology, permissions, resource use, export identity stability and shared reservation visibility before constructing the larger workflow. Multiple private local copies without a common authority cannot prove the early conflict requirement.

## Elaboration risks and smaller consistency corrections

**Control-store bootstrap and survival.** AI-8 deliberately leaves the shared store open, while Foundation owns installed-component and state records. E.1 must decide what exists before the first Foundation task can be reserved and how deployment ownership/receipts remain available during Foundation upgrades and failures. Also prove that deployment ownership survives migration commits and all SQLcl/import connections. This is a known design risk to retire, not a demand to implement the store in Inception.

**Automation completeness.** AI-2 explicitly leaves user/access provisioning and cleanup unresolved. FR-13 is therefore a requirement with a validation gap, not an established platform capability. Keep that distinction at baseline acceptance. Record a complete unattended path for the selected topology, including first installation and recovery, before calling the prototype reproducible. Source adoption of the currently untracked lifecycle scripts remains necessary; their historical availability is not reproducibility from an accepted Git revision.

**Release and prototype traceability.** The continuation proposal still describes PBI-017–019 using primarily UC-1–6, with later paragraphs adding onboarding, adoption and concurrency. Consolidate those acceptance summaries when promoting them so UC-7–12 and FR-8–13 cannot disappear from release planning. The root backlog legitimately remains unchanged while these proposals await acceptance. PBI-006 and the full baseline review should not be called complete solely because the proposal exists.

**E.1 scope and exit decision.** “Thin slice” now includes substantial control infrastructure and twelve integration cases. That may still be a sensible risk-driven prototype, but the candidate selection has not established its effort. At E.1 decomposition, order the experiments by dependency: topology/API and capture feasibility; combined-source/artifact reconstruction; guarded deployment and recovery; full A/B/C journey and reservation race. State which evidence is mandatory for Lifecycle Architecture and which full-page behavior can wait for Construction. Split further Elaboration if needed, as the existing proposal already allows; retain the required multi-developer proof.

**Stale wording.** The test-profile prerequisite “Provision only … LAB_DEV and LAB_TEST” needs reconciliation with task and validation areas. The runbook calls the image-pinning file “checked-in” while also saying the scripts remain untracked. Its absolute workstation path should become a documented example rooted in the operator's checkout. These are small corrections, not reasons to reject the concept.

## Appropriate deferrals

Inception does not need final table DDL, detailed page layouts, complete provisioning SQL, the reservation database implementation, every API permission, every migration edge case, an executable test harness or a registered CI runner. These are reasonable Elaboration/Construction work when their expected outcomes and decision gates are explicit.

The documented APEX checksum capability supports the drift experiment, but does not establish complete schema coverage or source normalization. Oracle's [GET_APPLICATION reference](https://docs.oracle.com/en/database/oracle/apex/24.2/aeapi/GET_APPLICATION_Function.html) describes ID-independent checksums and configurable export contents. Keep repeated-export stability, target configuration effects and separately scoped schema drift as experiments, as the baseline already does.

No additional business use case is necessary to resolve the core findings. The missing work is to connect the existing use cases with consistent ownership, artifact, target, maintenance and recovery rules.

## Recommended acceptance disposition

**Recommend revisions before unconditional baseline acceptance.** Resolve R1–R5 with concise policy decisions and corresponding acceptance assertions in the SRS, architecture and test profile. E.1 should then prove the mechanisms; lack of runtime evidence today is expected for Inception.

Against the design's review criteria, REV-1 has substantial actor/use-case coverage, with shared scope and supported participant topology needing clarification. REV-2 has clear release exclusions and a proposed continuation, with approval and consolidated traceability still pending. REV-3 has a credible research basis and visible technical risks, but the artifact, maintenance and repair contracts need reconciliation. REV-4 should remain pending until those contracts and the approved scope agree.

This assessment preserves I.1 as the active documentation iteration and E.1 as planned. It does not approve the design, close any PBI, change the backlog or authorize implementation. The requested review deliverable is this file.
