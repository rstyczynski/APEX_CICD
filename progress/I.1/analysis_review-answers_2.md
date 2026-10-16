# Final engineering decisions after expert review 2

Date: 2026-10-16. Basis: [final expert review](analysis_review_2.md), [first review](analysis_review_1.md) and [my first response](analysis_review-answers_1.md). This file records my final engineering judgment and the document corrections implemented in response. The baseline remains Proposed for Product Owner review; technical mechanisms require Elaboration evidence.

## Judgment

I accept the six findings. The expert's qualifications improve the design by keeping the demonstration bounded. I have corrected the contracts in the SRS, architecture and test profile, and reconciled the research, infrastructure procedure, design record and proposed continuation. These are implemented analysis changes, not implemented application or automation behavior.

I revised two recommendations from my first response: there is no additional shared reservation type, and no mandatory separately deployed control service. I also moved the first reservation/reassignment experiment earlier. The newly identified initial-assembly gap required a substantive correction: Foundation-specific success and full-application readiness now have different acceptance conditions.

## R1 — Ownership, shared assets and inherited changes

**Decision:** use the existing Foundation/Hello/World reservation scopes. Foundation owns shared composition/database contracts; component-owned pages, objects and navigation entries belong to their component regardless of export directory. Changes to application-wide behavior/security/settings or delivery-controller behavior reserve the full three-component set. This conservative rule has an explicit conflict relationship and avoids a fourth lock category. Reserving a component does not itself require changing its semantic version.

Permit generated bookkeeping reconciliation only through bounded rules and validation. Unknown semantic changes fail closed. Scope expansion preserves work and atomically obtains the full additional set or reports a conflict, without incremental partial acquisition or indefinite hold-and-wait. Revalidate the base before resuming.

Accepted changes incorporated into another task retain their provenance: C may integrate B's accepted Hello change into C's World branch without claiming a new Hello edit. A further C-authored Hello change still requires ownership. Full-application deployment uses target ownership and accepted-change provenance; it does not reacquire authoring reservations for all completed components.

**Implemented:** [SRS FR-8](../../docs/srs.md#functional-requirements), [architecture ownership policy](../../docs/architecture.md#early-component-change-ownership), and test-profile IT-5/6. Elaboration proves shared-file additions, unauthorized changes, expanded-scope conflict and inherited-change attribution; no generic SQL parser is prescribed.

## R2 — Exact artifact qualification

**Decision:** pre-merge candidate checks and post-merge release qualification are separate gates. Build the accepted revision once, qualify the finished archive, and promote those exact bytes. Receipts bind archive hash/commit, declared starting baseline and controlled nonsecret inputs. Changed bytes, stale candidate evidence, missing qualification or unsupported starts block the relevant gate.

Candidate/qualification roles may reuse a disposable area sequentially after a verified reset. Retained TEST remains separate. The initial support matrix is clean complete installation and one declared additive upgrade path, plus qualification for the selected partial-state repair. Approved version triples do not imply arbitrary migration paths.

**Implemented:** UC-4, FR-5/6, NFR-2, [packaging and promotion](../../docs/architecture.md#sources-packaging-and-promotion), and test-profile qualification/promotion command contracts and IT-1/2/3. Commands remain proposed; the controllers must execute verified archive contents rather than mutable checkout files.

## R3 — Maintenance verification

**Decision:** permit a dedicated authenticated verifier only after installation and preliminary integrity/dependency checks. Its deployment-scoped exception covers the active maintenance restriction needed for the intended checks. It does not bypass unknown state, unrelated failed dependencies, normal authorization or business validation. Negative state tests must still observe rejection.

Stop new ordinary work and drain/fence active mutations before installation. Ordinary identities and existing sessions remain blocked, including during import. Revoke verification permission and account for the final native availability/configuration in the fingerprint/receipt before publishing readiness. Interruption stays blocked; a timeout never establishes readiness. Synthetic verification rows must be identifiable without altering retained history.

**Implemented:** FR-9, [restricted verification contract](../../docs/architecture.md#verification-while-ordinary-access-remains-blocked), delivery order and IT-9. Native restricted access is a candidate primitive. Exact native/custom guard sequencing and request fencing remain mandatory experiments; no token format or lease service is imposed.

## R4 — Recovery from partial state

**Decision:** UC-5 authorizes a repair against inspected partial definitions and the current generation, linked to the failed attempt, intended artifact and previous successful receipt. Recheck that observation under target ownership before writes. Incomplete observation, unsupported partial state or subsequent unexplained changes block recovery with a diagnosis. A logged checkpoint alone cannot establish what committed.

Unchanged bytes may resume only after safe repetition is established. Corrected code/migrations require a new reviewed immutable archive, qualified for the chosen partial starting state. Keep original artifacts and success/failure evidence; never edit an applied changeset. This supports the selected injected-failure repair, not an arbitrary-state recovery engine.

**Implemented:** UC-5, [recovery contract](../../docs/architecture.md#recovery-from-a-recorded-partial-attempt), corrected same-archive wording and IT-3/8/9. Human diagnosis/authorization remains intentional; execution after that decision follows the automated path.

## R5 — Supported topology

**Decision:** select the single-host proof. A/B/C use separate identities, private application/schema/workspace areas and independent checkouts/browser sessions. Synchronized clients issue genuinely concurrent requests to one authority. Privilege separation covers ordinary developer access; it does not claim isolation from host/platform administrators. Services remain on loopback.

Remote workstations and independent developer-local installations are researched alternatives requiring a revised decision and evidence. Allocate areas according to the experiment and measure resource use. This preserves the multi-developer acceptance scenario while avoiding an unrequested networking or OS-tenancy project.

**Implemented:** SRS journey, UC-8/9 and FR-11; [architecture boundaries](../../docs/architecture.md#components-and-boundaries); test prerequisites and IT-11/12; infrastructure procedure. Second-operator reproduction remains separate human evidence.

## R6 — Foundation-first initial assembly

**Decision:** distinguish a reviewed greenfield seed from UC-12 adoption of a source application. The seed supplies source layout, empty migration root, mappings and constrained assembly policy, without completed Hello/World behavior. Bootstrap infrastructure and durable control authority before A reserves Foundation. Foundation must reconstruct without undelivered Hello/World-owned objects.

An explicit assembly manifest distinguishes installed versions from deliberately not-installed components. Foundation-only and subsequent intermediate component assembly are permitted in identified incomplete development/validation areas, with the application root in maintenance and incomplete dependent behavior blocked. Foundation-specific checks complete A's task and release its reservation without claiming a ready full release. Do not export or set native application status on a nonexistent application.

B/C then author their components from the accepted Foundation baseline. Complete-triple compatibility and the greeting/history journey become mandatory for the first operational TEST release. Unexpectedly missing components on a previously complete target still fail closed; assembly mode cannot excuse drift. No fake versions, new runtime state vocabulary or independent production deployment packages were added.

**Implemented:** SRS journey, UC-1/8/9/10 and FR-7; [initial assembly contract](../../docs/architecture.md#initial-assembly-and-first-complete-release); test-profile build-stage rules and IT-4/5.

## Supporting decisions and scope

The delivery-control authority has a lifecycle independent of ordinary Foundation upgrades/imports. It must exist before the first task, retain reservations/generations/attempt evidence, and support safe restart/inspection. A same-database schema is a candidate, not a mandatory service or separate failure domain. Exclusion across DDL commits, subprocesses and disconnects is an Elaboration requirement; a commit-released row lock alone is insufficient.

The continuation proposal now consolidates onboarding, adoption, collaboration and FR-8–13 in its acceptance summaries while retaining Proposed status. It creates no child PBIs or assignments. The experiment order proves bootstrap/topology and minimal reservation/reassignment early, then assembly/capture/integration, immutable qualification, guarded delivery/repair and the complete A/B/C proof. Critical feasibility gaps require further Elaboration; full page layouts and additional topology variants may wait.

Corrected the runbook's inaccurate “checked-in” wording and workstation-specific command paths. Script adoption into accepted Git remains pending. Reconciled current roadmap infrastructure ownership while preserving historical review files and execution evidence. FR-13 remains the single automation requirement; interface enumeration and validation are its evidence obligations.

## Reconciliation result and remaining decision

All six findings now have a document contract and representative success/failure assertions in the baseline. This closes their identified Inception wording gaps in my engineering assessment. It does not establish tool compatibility, lock enforcement, safe import behavior, fingerprint completeness or recoverability in practice. Those remain explicit Elaboration acceptance risks.

The [documentation audit](sprint_I.1_documentation_audit.md) and [check record](tests/review2_reconciliation_checks_20261016.log) describe the performed review and mechanical checks. The expert's review 2 assessed the earlier documents and responses; it is not a post-edit endorsement of these revisions.

Ready for Product Owner review of the revised Inception baseline and these decisions. I.1 remains active, E.1 remains Planned, and no application implementation, runtime mutation, commit or push occurred in this correction pass. Overall design acceptance, backlog promotion and sprint closure remain separate managed decisions.
