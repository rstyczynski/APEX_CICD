# I.1 inception analysis — final review, release 2

Date: 2026-10-16. Scope: expert review of [the engineering responses](analysis_review-answers_1.md), [review 1](analysis_review_1.md), and the current Inception baseline. This document supersedes review 1's recommendations where it explicitly refines them. It is review evidence, not Product Owner approval or a change to sprint/PBI status.

## Final assessment

**The responses provide sound proposed resolutions to R1–R5. They do not yet close the findings, because the corresponding baseline contracts remain unchanged.** Retain the concept and actor/use-case model. Incorporate a small set of coherent policy corrections before unconditional Inception acceptance, then prove their implementation during Elaboration.

I agree with the response's overall direction. I qualify several recommendations to avoid turning this laboratory into a general delivery platform: a fourth reservation scope is optional; a separately deployed control service is unnecessary unless evidence requires it; validation roles need not each consume permanent infrastructure; and the supported upgrade matrix can remain deliberately small.

One additional core inconsistency needs an explicit resolution, recorded as R6 below: the journey delivers Foundation before Hello and World exist, while release compatibility rules require all three versions and reject missing metadata. Separating the delivery-control bootstrap from Foundation helps, but does not by itself resolve this initial application assembly contract.

No baseline documents, managed artifacts, application code or infrastructure were changed for this review. No runtime validation, commit or push was performed.

## Evidence and current closure status

The current [SRS](../../docs/srs.md), [architecture](../../docs/architecture.md), [test profile](../../docs/test-profile.md), [continuation proposal](sprint_I.1_proposedchanges.md), and [deployment procedure](../../docs/deploy.md) still contain the conditions identified in review 1. In particular, the architecture describes pre-merge source validation followed by post-merge build/promotion; the test profile still says repair uses the same archive and names only LAB_DEV/LAB_TEST as provisioning targets. Shared-scope attribution, verifier permissions and recovery entry conditions are not yet incorporated.

The responses are therefore accepted here as engineering proposals, with the qualifications below. “Resolved in the response” must not become “implemented,” “tested,” or “baseline accepted.” The implementor's final decisions and subsequent document reconciliation are the next steps. Historical review and response files should remain historical evidence.

## R1 — Shared ownership: accept, with a simpler minimum contract

**Disposition: proposed resolution accepted with qualifications; baseline correction still required.** The response correctly distinguishes semantic ownership from file paths, and generated metadata from automatically harmless content. Its treatment of component-owned navigation entries versus shared navigation behavior is useful. An explicit inventory and conservative rules are proportionate; a general SQL semantic parser is unnecessary.

**Required in Inception:** define ownership of shared composition/database contracts, application-wide behavior and delivery assets; distinguish permitted reconciliation of generated metadata from semantic changes requiring additional ownership; and specify safe failure when task scope expands. Preserve work, acquire the expanded scope atomically or return a conflict, and revalidate the baseline before continuing. Avoid an indefinite hold-and-wait path between tasks requiring each other's scopes.

**Qualification:** I do not require a distinct shared reservation scope. Mapping shared changes to Foundation or an explicit multi-component reservation may be sufficient. If a shared scope is selected, document its conflict relationship with Foundation/Hello/World and distinguish it from the three versioned components. Merely adding a fourth lock name does not establish which combinations can coexist. Prefer the least complex rule that permits the required independent Hello/World work and blocks unsafe shared changes.

One attribution detail remains incomplete: when C incorporates B's already accepted Hello change into C's World branch, that inherited change must not be treated as a new unauthorized Hello edit by C. Capture, integration and delivery need to distinguish task-authored changes from accepted integration changes. A full-application artifact also must not require its deployer to hold active authoring reservations for every unchanged or previously accepted component. Preserve task-to-change provenance; keep the separate target deployment lock responsible for serializing the full import.

**Elaboration proof:** extend IT-5/6/12 to cover concurrent page additions, generated metadata reconciliation, unauthorized shared behavior, scope expansion conflict, and C integrating B's accepted change without acquiring ownership of B's completed task. Exact object mappings and enforcement belong in E.1 design.

## R2 — Qualification and promotion: accept, bound the support matrix

**Disposition: proposed resolution accepted; baseline correction still required.** Pre-merge candidate validation and post-merge qualification of one immutable archive are distinct gates. Recording environment mappings separately is correct. Reusing one disposable validation area sequentially after a verified reset is also reasonable; retained TEST state must remain separate from unaccepted candidate work.

**Required in Inception:** specify build-once, qualify-exact-bytes, promote-same-bytes; link qualification and deployment receipts to the artifact hash, accepted revision, supported starting state and controlled nonsecret configuration inputs. State that stale candidate evidence or a changed package invalidates the relevant gate. Correct the target-role model and the LAB_DEV/LAB_TEST-only prerequisite.

**Qualification:** “each supported starting baseline” must mean an explicitly declared, small set. For the first demonstration, a fresh installation and one accepted upgrade path can be enough. This review does not require supporting every historical component triple or testing all combinations. An approved final version triple is not itself an approved migration path. Candidate validation and release qualification are logical roles; they do not require two permanent additional schemas or VMs.

**Elaboration proof:** qualify clean reconstruction and the declared upgrade path; reject an unsupported start, stale evidence, altered archive or missing qualification; demonstrate unchanged archive bytes through TEST promotion. Resource allocation and precise reset procedures remain design work.

## R3 — Maintenance verification: accept the permission, constrain the exception

**Disposition: proposed resolution accepted with clarification; baseline correction still required.** A deployment-scoped verifier is a credible way to reconcile real browser checks with blocked ordinary access. Binding permission to the active target and deployment attempt, preserving normal authentication/business validation, and accounting for import-time exposure are all appropriate.

**Required in Inception:** state that verification may bypass only the deployment maintenance restriction needed to run the intended checks. It must not grant blanket access through arbitrary failed dependencies or unknown state. Verification starts only after the required installation/preliminary integrity steps succeed. A test that checks failure-state blocking must still observe that blocking. Otherwise a verifier that ignores every state guard could produce misleading success evidence.

Specify the required outcomes for stopping new ordinary work, fencing/draining active mutations, restricting verifier access, revoking permission and failing closed after interruption. Include import behavior and the final availability/fingerprint transition. The response correctly identifies that an import must not create a transient unrestricted window.

**Qualification:** requiring these outcomes is appropriate now; fixing a particular token format, lease service or native/custom permission composition is premature. Oracle's [restricted-access application status](https://docs.oracle.com/en/database/oracle/apex/24.2/aeapi/APEX_APPLICATION_ADMIN.SET_APPLICATION_STATUS-Procedure.html) is a candidate primitive, not a complete solution for the custom guards. If the selected combination cannot keep ordinary access blocked across import and verification, revise the mechanism before declaring architecture stability.

**Elaboration proof:** execute the real application journey with the authorized verifier while ordinary identities and existing sessions are denied; test import/connection interruption, stale verification permission, and state guards themselves. Identify synthetic verification rows without modifying or deleting retained history. Separate fixtures may be reset only within their declared disposable scope.

## R4 — Recovery: accept, without promising arbitrary-state repair

**Disposition: proposed resolution accepted; baseline correction still required.** The response properly distinguishes the last successful baseline, observed partial state and a reviewed recovery starting point. Live inspection after interruption is essential; the last logged checkpoint cannot establish everything that committed. Rechecking the approved observation under deployment ownership prevents a repair authorization from becoming permission to overwrite later changes.

**Required in Inception:** define recovery as a guarded path within UC-5, linked to the failed attempt and exact observed starting state. Keep the old success/failure evidence. Distinguish safe retry of unchanged bytes from a new reviewed repair artifact, and correct the test-profile same-archive wording. State that qualification for a normal successful baseline does not prove safety against the selected partial state.

**Qualification:** require evidence for the chosen injected failure and supported repair path. Do not promise a general engine that can reconstruct or repair every possible interrupted state. When observation is incomplete or the state is unsupported, remaining blocked with an actionable diagnosis is correct behavior. Any manual diagnostic decision must still lead to automated operational execution under FR-13.

**Elaboration proof:** committed-DDL failure, live partial-state inspection, rejection after an intervening unexplained change, and qualified retry or forward repair with unchanged sentinel history. Oracle's [transaction documentation](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqlrf/COMMIT.html) supports the underlying commit boundary; the repair protocol itself remains project behavior to validate.

## R5 — Multi-developer topology: accept as the candidate proof boundary

**Disposition: single-host recommendation accepted as a proportionate candidate; explicit baseline selection still required.** Separate developer identities, private application/schema areas, independent checkouts/sessions and synchronized clients against one ownership authority can exercise the required logical concurrency without weakening loopback-only access.

**Required in Inception:** make the chosen supported variant explicit. Describe the proof as a single-host multi-developer workflow; do not infer remote workstation access, strong host-level isolation or operational support for both onboarding alternatives. Preserve A/B/C responsibilities and actual concurrent acquisition. A sequential demonstration by one client does not prove the race.

**Qualification:** “identities cannot write each other's private state” should be scoped to the documented ordinary database/APEX privileges. This does not establish isolation from the shared host owner or platform administrator. No additional OS tenancy or remote networking project is required. Human usability and second-operator reproduction remain distinct evidence from automated concurrent clients.

**Elaboration proof:** private-area permissions, common ownership authority, capture identity mapping, real simultaneous requests and measured resources. Allocate areas according to the experiment; the review does not require all possible environments to remain provisioned indefinitely. If resource/identity constraints invalidate the candidate, return a revised topology decision.

## R6 — Complete the initial assembly and compatibility contract

**Priority: high; new clarification required before baseline acceptance.** Evidence: SRS “Establish the three components,” UC-9, FR-7 and FR-9; architecture “Three versioned components” and the proposed ready/maintenance/failed model.

The journey says A authors, delivers and verifies Foundation before B and C implement Hello and World. FR-7 requires durable records for all three versions and fails closed on missing metadata. The architecture permits an empty starting installation, but requires the intended final set to match an approved triple. It does not explain whether a Foundation-only installation is an allowed intermediate baseline, which checks apply to it, or why missing Hello/World metadata there differs from missing metadata in an established release.

The response's separate delivery-control bootstrap solves the reservation-authority dependency. It does not solve this application-level dependency. Likewise, the SRS mentions a reviewed initial source baseline for a new system, but does not distinguish that seed from UC-12's adoption of an already existing application or define what A can reconstruct before Foundation exists.

**Required in Inception:** name the reviewed greenfield seed and bootstrap preconditions; define the intended status and permitted operations of the Foundation-only stage; distinguish deliberately absent, not-yet-delivered components from unknown/inconsistent metadata; and state when complete-triple compatibility and the greeting journey become mandatory. Keep ordinary users from reaching incomplete dependent functionality. Explain how Foundation-specific verification can complete A's task and release its reservation without claiming the complete laboratory release is ready.

This can be expressed as a constrained initial-assembly procedure. It does not require adding a new runtime state vocabulary, fake component versions or independently deployable production packages. Alternatively, a reviewed scaffold could supply real initial Hello/World contracts, but that would need an explicit explanation consistent with B/C's promised authoring roles. Do not silently substitute an already completed application for the required journey.

**Elaboration proof:** start from the selected seed, reserve and deliver A's Foundation work, prepare B/C's areas from that accepted baseline, and reach the first valid complete release. Reject the same missing-component condition when encountered unexpectedly on a previously established complete release. Extend IT-5 and relevant bootstrap/version assertions rather than inventing a new business use case.

## Control authority, automation and scope

**Control bootstrap and survival — accept the lifecycle separation, qualify the implementation.** The minimum invariant is an ownership/evidence authority that exists before the first Foundation task and is not replaced by ordinary application import or Foundation migration. A separate schema/store is a reasonable candidate; a separate service, database or failure domain is not mandated. A shared database outage may block progress in this local lab. After restart, the system must inspect and recover safely rather than silently infer readiness or abandon ownership. Exact persistence, privileges and lock mechanics remain Elaboration choices. Prove exclusion across DDL commits, subprocesses and disconnects; a row lock held on a connection that commits cannot alone supply that guarantee.

**Automation — agree.** Keep AI-1–10 as candidate interfaces until exercised. Clarify that human emergency authoring is allowed where already specified, while capture/reconciliation/deployment are automated after the relevant decision. Do not claim complete onboarding or recovery merely because API names are listed. Adopt the lifecycle scripts into reviewed source before claiming reproducibility from Git; this review does not request that commit.

**Traceability — agree.** Consolidate continuation outcomes so the newer actor journeys and controls are visible in their acceptance summaries. Preserve proposed status and the mandatory backlog/plan routing. Update current contradictory wording, while preserving historical execution evidence. A PBI per mechanism is unnecessary.

**Experiment order — refine the response.** Establish bootstrap and topology first, but test the minimal atomic reservation/reassignment behavior early rather than postponing its first proof until after the full delivery system. It is a core feasibility risk and can be tested independently. Capture/identity, immutable qualification and guarded repair then support the complete A/B/C demonstration. This is recommended dependency ordering, not creation of E.1 child PBIs or a promise that one iteration can retire every risk.

## Minimum correction package and closure criteria

Before declaring the Inception baseline coherent, the implementor should record its final choices for R1–R6 and reconcile them across the existing documents. The SRS should express externally observable policy, the architecture should explain the selected responsibilities and candidate mechanisms, and the test profile should state bounded evidence obligations. Keep one authoritative description of each rule and use references rather than repeating detailed algorithms everywhere.

Closure of an Inception finding requires that its contradictory clauses are reconciled and a representative success/failure assertion is present. It does not require a working controller or executed test today. Review the resulting documents against the six findings before asserting closure; the answers file alone is not closure evidence.

Elaboration then needs actual evidence for the selected topology and supported APIs, initial assembly, stable capture/integration, qualified artifact promotion, ownership/concurrency, maintenance/state enforcement, drift and interrupted-deployment repair. Keep unknown/unsupported conditions fail-closed and visible. If critical feasibility remains unresolved, continue Elaboration rather than treating the candidate architecture as proven.

## Final recommendation

**Retain the concept; revise the baseline contracts before unconditional acceptance.** The responses substantially improve the proposed resolution and do not justify a redesign or new business scope. Adopt their direction with the bounded qualifications above, and explicitly resolve R6. After document reconciliation, an Inception acceptance decision can be made while the named technical proof remains assigned to Elaboration.

This final review release preserves managed approval gates. It neither accepts the design on behalf of the Product Owner nor activates E.1, creates implementation work, changes the backlog, or closes I.1.
