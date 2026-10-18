# E.1 — Validate the local APEX delivery path

The [repository and pipeline draft](repo_layout.md) consolidates this design's shared-source, developer-area and release-path decisions for PBI-017. It records the current slice and gaps without completing the broader design or assigning the new item to a sprint.

Status: Accepted

Approval scope: the first happy-path implementation, compatible patch upgrade, focused drift-stop demonstration and incompatible Foundation-upgrade rejection below. The remaining design is retained for later selection.

### DevOps evidence in the selected slice

The happy path includes two releases, not just a first installation. Establish Foundation/Hello/World at 1.0.0, then make one compatible Hello correction and advance Hello to 1.0.1 while Foundation and World remain 1.0.0. Explain patch versus minor/major changes against the component contract; version syntax alone does not establish compatibility. Declare and validate the two supported complete triples and the actual upgrade path before writes. Display installed component versions and compare them with the source manifest and release receipt.

For both releases, retain the local task branch/base, reviewed diff, candidate check result, accepted Git revision, immutable migration identities, artifact hash and qualification/promotion results. Qualify the initial release on an empty area; qualify the patch on both fresh reconstruction and the accepted 1.0.0 baseline, then promote those same bytes to TEST. The patch preserves earlier greeting snapshots and user-maintained configuration. A release label, Git revision, migration identity, installed component version and content fingerprint have different purposes and must remain distinguishable.

Use dedicated target connections, versioned nonsecret mappings and external credentials. Pre-merge candidate validation and post-merge release qualification are separate gates even in this local run. Remote PR/runner integration is not claimed. The drift demonstration changes content without changing its version and proves why live fingerprints supplement semantic versions. This adds the successful additive/patch-upgrade and history-preservation assertions from IT-2 to the selected happy path; concurrency and injected-failure repair remain later work.

## Scope and proposed result

Build a local architectural prototype of the accepted workflow, using one APEX application containing Foundation, Hello and World in each isolated target. Demonstrate A delivering Foundation, B/C integrating separate component changes, one early loser in a real Hello reservation race, exact-byte release qualification/promotion and one failed additive deployment followed by automated forward repair with history retained. The result is evidence for a Construction decision, not a production delivery platform.

Keep shell entry points, small Python standard-library helpers for archive/file handling where useful, and explicit SQL/PLSQL rules. No new control service, generic dependency resolver, SQL semantic parser, remote runner, remote workstation support or independent component deployment. Author APEX pages in App Builder; capture/install and operational steps run through SQLcl and supported public APIs. Execute Oracle-generated export files unchanged; do not hand-author internal APEX repository calls.

## PBI-011 — Bounded prototype children

### Construction selection

Retain children PBI-011.1–PBI-011.8 as the broader prototype design. Select the happy-path slice below for the first implementation. Keep the broader design options and existing analysis for later work.

The application will be created from scratch. In child 3, A builds Foundation and the initial APEX shell in an empty prepared area, then captures the first application source baseline. No supplied seed application, separate seed deliverable or application-data seeding mechanism is selected. In child 4, implement capture/reconstruction of the newly created application and its private developer copies. Existing-application adoption under UC-12/IT-10 remains a design option and is not selected for E.1 construction or its completion gate.

The remaining selected work is control/bootstrap and isolation, atomic reservations, parallel Hello/World integration, exact-artifact qualification/promotion, compatibility/drift/maintenance controls and the failed additive deployment with automated repair. Preservation checks create their own synthetic history through the application/test fixtures; that test preparation does not require a product seeding feature.

This selection governs E.1 implementation and test manifests wherever a child description below includes the broader seed/adoption option. Keep those descriptions intact. The selected scope is approved for construction.

### First implementation — happy path

Implement one successful journey from an empty application area to a working greeting in TEST, in this order:

1. Prepare SQLcl/Java and the required private development, disposable qualification and TEST areas in the current apex-cicd environment. Check their identities and keep credentials local. Recreate the runtime only if needed; maintain the verified procedure in docs/deploy.md.
2. Bootstrap the minimum control authority. A reserves Foundation, builds its database contracts/history and the initial authenticated APEX shell from scratch, captures the source and completes Foundation-specific verification. Release A's reservation; incomplete application behavior remains unavailable.
3. B reserves Hello, creates its minimal entry/configuration page and captures the change. Review/integrate it locally. C then follows the same successful sequence for World from the accepted baseline. Use private areas, but execute these tasks sequentially in this first slice.
4. Enter Hello and World values through the application and verify the composed greeting in the development/validation area. Capture the integrated sources and migrations, review the diff and commit the accepted application revision.
5. Build one archive from that revision. Import its exact contents into the empty disposable qualification area, using supported Oracle mappings and ordered migrations. Verify the complete component versions and actual greeting/history behavior; record the archive hash and fresh-install qualification result.
6. Promote those same archive bytes into the identified empty TEST area. Keep access restricted during installation and verification, record installed versions and the release receipt, then make the application available after successful checks. Follow with the compatible Hello patch and supported upgrade specified in the DevOps evidence section.
7. Sign in to TEST, enter the component values, create Hello World and reopen history. Acceptance is the visible greeting and saved snapshot, successful refresh, matching component versions, and identical qualified/promoted archive hashes. Leave this data available for later upgrade/preservation experiments.

This is a first slice through children 1–7. Implement only the mechanisms needed for this journey: target identity, ordinary task acquire/release, explicit versions, safe initial installation and traceable capture/build/promotion. Keep component authoring, review and release steps visible instead of hiding them in a general pipeline framework.

Later slices retain parallel Hello/World work, the competing Hello race, scope expansion/reassignment, negative compatibility and drift cases, deployment races/interruption, successful additive upgrade/repeat deployment, and failed additive deployment/automated repair. Existing-application adoption and seed construction remain unselected options. None of this later work is deleted or reported as proven by the happy path.

The first test manifest selects positive assertions from SM-1/2, UT-1/2 and IT-1/4/5/11, with browser greeting/history checks. Record the assertions actually exercised; the full cases and child acceptance criteria remain pending wherever their later scenarios are unrun. PBI-011–016 and Lifecycle Architecture are not complete after this first slice.

Planning estimate for this slice: 18–28 engineering hours, using the existing resource allocation. The broader estimate below remains for the remaining prototype design. The happy path and selected rejection demonstrations are approved; broader experiments remain later work.

### Selected unhappy scenario — detect drift and stop deployment

After a successful TEST release, change a visible APEX page attribute directly in the controlled demonstration target, outside capture/release, without changing the component version. Attempt promotion against the last recorded successful baseline. Recompute the live application fingerprint before installation, detect the mismatch and return a nonzero drift rejection before migrations, import or maintenance transition. Show the changed page still present, the prior history unchanged and a rejection receipt explaining the mismatch. Do not silently recapture or accept the altered target as the new baseline.

This selects SM-3 and IT-7's focused page-drift assertion from child 7. Comprehensive drift coverage, emergency reconciliation and repair remain later work. Allow approximately 2–4 additional engineering hours. Test successful unchanged-baseline comparison as well as the drift rejection, so a check that rejects every deployment cannot pass. The implementation must propagate SQL/import errors as failure; a printed Oracle error cannot produce a successful release receipt.

### Selected unhappy scenario — reject an incompatible database contract

On an already working target, choose a small proposed Foundation change that breaks the schema contract required by the installed Hello/World components. A Foundation major version change with dependents still requiring the earlier contract is one suitable example. The pre-deployment validation must explain the incompatibility and stop before executing migrations/imports. Verify unchanged installed definitions, versions and greeting history. Keep the example focused on the observable benefit of dependency declarations and compatibility gates; no general dependency resolver or destructive migration execution is required.

This selects SM-2's incompatible-combination assertion. Pair it with the accepted patch upgrade so the demonstration shows both useful acceptance and useful rejection. The scenario demonstrates practical DevOps controls rather than treating the particular version numbers as the goal.

### PBI-011.1 — Toolchain, lifecycle and isolated areas

Parent: PBI-011. Outcome: review/adopt existing lifecycle sources and ignore rules, pin SQLcl 25.3.0.274.1210 with private Java 21, verify the owned platform under docs/deploy.md, bootstrap a separate control schema and provision collision-checked private developer, disposable validation and retained TEST areas. The control authority exists before the first task and is excluded from Foundation migrations/imports. Use dedicated schema credentials and protected named connections; no routine CI use of administrator credentials.

Dependencies: accepted I.1 baseline and this design's approval. Acceptance evidence: SM-1 and IT-11 show actual versions, grants, target identity, unattended connectivity, denied cross-area reads/writes and resource use; disposable-area create/reset/destroy leaves retained markers unchanged. E.1 owns docs/deploy.md. Exercise the authorized destruction/reconstruction of the current apex-cicd environment and update that procedure with verified steps. Preserve host credentials/evidence and any retained data outside the VM before its removal; do the initial rebuild before creating retained prototype history. Estimate: 6–10 engineering hours.

### PBI-011.2 — Durable atomic reservations

Parent: PBI-011. Outcome: implement Foundation/Hello/World task ownership, all-or-none acquisition/expansion, safe release and inspected reassignment. Commit durable owner/task/base/generation rows; connection lifetime is not ownership lifetime. Use authenticated database identity mappings and package-only control writes. A short control transaction locks a single coordination row with NOWAIT, validates the complete scope and commits all changes together. Busy coordination returns a retryable conflict immediately; it never grants a partial scope or waits indefinitely.

Dependencies: child 1. Acceptance evidence: IT-12 runs synchronized independent SQLcl clients against a barrier, repeatedly obtaining exactly one Hello winner, owner/task information for the loser and no loser branch/area/code/state change. Hello and World coexist. IT-6 covers expanded-scope conflict, preservation and stale generation rejection. IT-8 covers committed ownership surviving DDL, subprocess exit and disconnect. Reassignment requires prior owner quiescence and inspection, never a timeout alone. Estimate: 4–6 hours.

### PBI-011.3 — Foundation-first assembly

Parent: PBI-011. Outcome: create the reviewed greenfield seed, Foundation migrations/history/contracts and a minimal authenticated APEX shell with no completed Hello/World behavior. A authors the shell through supported App Builder authoring, captures it and establishes its accepted source baseline. Foundation-only assembly declares Hello/World not installed and keeps ordinary access blocked. Component-specific verification releases A's task without declaring a complete ready release.

Dependencies: children 1–2. Acceptance evidence: IT-4 reconstructs Foundation without dependent objects, checks explicit absent-component metadata and root maintenance, verifies its contracts and releases ownership. It rejects the same missing metadata on a previously complete target. No status/export API is called on a nonexistent app during the earlier database-only stage. Estimate: 4–6 hours.

### PBI-011.4 — Stable capture and reconstruction

Parent: PBI-011. Outcome: associate source identity, branch/base and private area; export to staging using the accepted SQLcl split profile; reconcile only the managed source tree; import through public APEX_APPLICATION_INSTALL mappings. Keep schema migrations separately authored and immutable. Establish canonical original identities from the accepted Foundation shell before B/C work.

Dependencies: child 3. Acceptance evidence: IT-1/5/10 capture two private targets, explain any identity differences, obtain an unchanged second capture, reconstruct accepted definitions and prove deletion handling. Wrong source, missing dependency, unknown normalization and dirty/unrelated file overwrite are rejected. IT-10 adopts the actual accepted source application into a separate candidate source area and reconstructs it; it does not reinitialize this project repository. If supported identity mapping cannot preserve meaningful stable source, stop this path for a smaller alternative decision. Estimate: 6–10 hours.

### PBI-011.5 — Parallel Hello/World integration

Parent: PBI-011. Outcome: B and C start from the accepted Foundation baseline, hold distinct reservations, author their own entry/configuration pages and greeting behavior, capture changes into separate local task branches, and integrate both component additions. Use disjoint reviewed page ranges and an explicit ownership map; shared composition belongs to Foundation, application-wide behavior requires all three scopes. Generated include/changelog bookkeeping is reconciled only by bounded rules.

Dependencies: children 2–4. Acceptance evidence: IT-5/6 and UT-1/2 preserve both page/navigation additions, ordered migrations and accepted-change provenance when C incorporates B's accepted Hello work. Reject newly authored out-of-scope changes, missing ownership and stale candidate evidence. The merged candidate imports successfully and browser checks show a composed greeting with retained snapshots. Use local review/merge receipts binding exact commits; remote PR/CI integration stays unexercised until separately authorized. No remote branch publication is required for this experiment. Estimate: 6–10 hours.

### PBI-011.6 — Qualify and promote identical artifacts

Parent: PBI-011. Outcome: build once from a clean accepted source commit; package split APEX source, immutable migrations, controllers and nonsecret manifest; hash the finished archive; qualify those exact bytes and promote them unchanged to retained TEST. Candidate validation and post-merge qualification remain separate receipts. Never execute mutable checkout files during qualification/promotion.

Dependencies: children 4–5; child 7's controls must pass before retained TEST mutation. Acceptance evidence: IT-1/2 bind hash, commit, starting state, configuration revision and tool versions; qualify fresh complete install plus one additive upgrade from the named baseline. A repeated artifact preserves settings and all twenty history sentinels without duplicated seeds/migrations. Reject altered bytes, missing qualification, stale candidates and unsupported starts before writes. Assembly archives qualify only for their declared stage. Estimate: 4–6 hours.

### PBI-011.7 — Compatibility, drift and maintenance

Parent: PBI-011. Outcome: enforce explicit complete version triples and supported starts, live APEX/schema fingerprints, per-target durable deployment ownership and ready/maintenance/failed guards. Ownership is committed state with an epoch; it survives installation commits and disconnects. An interrupted owner leaves the target blocked until inspected recovery. Controlled-target editor access is restricted and any emergency authoring is coordinated separately.

Dependencies: children 1–5; may be developed before child 6 is used for retained promotion. Acceptance evidence: SM-2/3 and IT-7/8/9 reject incompatibility, unexplained page/object drift and stale generations without overwriting the target. Browser tests deny new/direct/existing-session actions during import and maintenance. A narrow attempt-bound verifier runs only after installation/integrity checks, retains ordinary authorization and cannot bypass unknown/failed dependencies. Expired/stale permission is rejected and final readiness agrees with the receipt/fingerprint. Estimate: 6–10 hours.

### PBI-011.8 — Failed additive deployment and forward repair

Parent: PBI-011. Outcome: deliberately fail after committed additive DDL, retain partial-state evidence, inspect live definitions and execute a new reviewed repair archive qualified for that exact partial state. Keep earlier success/failure receipts and original artifacts. Repair is automated after the review decision; arbitrary-state repair is excluded.

Dependencies: children 6–7. Acceptance evidence: IT-3/9 preserve every field of twenty sentinel rows through failure and repair, retain committed DDL evidence, block ordinary access and reject repair after an intervening unexplained change. Recheck the authorized observation under target ownership before writes. Prove safe repeat of unchanged bytes separately. Stop with a diagnosis for incomplete observations or unsupported partial states. Estimate: 4–6 hours.

## Control and application mechanisms

Use a proposed E1_CTRL schema for the control authority; developer A/B/C, one validation schema and retained TEST each receive separate schema/workspace/application mappings after collision checks. Names are proposals, not authorization to replace matching existing resources. Keep credentials in protected local storage, nonsecret mappings in versioned configuration and artifacts free of passwords/runtime data. Schema identities map to the owner server-side; a client-supplied owner name is not authentication. Developers receive scoped package execution, not DML access to authority tables or other private schemas.

The small authority records tasks/reservations, registered targets, deployment attempts and receipt references. Foundation owns the application version/state registry; the external authority keeps an additional maintenance gate that an APEX import cannot reset. A protected target coordination row serializes admitted runtime requests with entering maintenance: each supported ordinary request holds the row through its request transaction; the deployment transition drains those requests, sets the persistent gate and commits before DDL. New requests then fail closed. Verify APEX request/commit boundaries and asynchronous requests explicitly in IT-9; no autonomous request path may bypass the guard. Do not hold a transaction row lock as the durable deployment lock. This prototype may serialize ordinary requests; throughput optimization is out of scope.

Every APEX page/process checks the persistent gate on the server. Application SQL errors reject the operation; missing control state cannot default to ready. Restrict the native application with APEX_APPLICATION_ADMIN while retaining the custom gate across import. Qualification exercises concurrent ordinary requests throughout import. The verifier exception is bound to the current target/attempt, activated only after preliminary integrity checks and revoked before readiness; it bypasses only that attempt's maintenance gate. Negative failed-dependency tests use identities without the exception. Final native availability, live fingerprints and receipt publication are reconciled while the external gate is still closed. Publish ready only at the end.

Fingerprint only inventoried application/schema definitions with a versioned profile; exclude runtime rows and operational receipts. For APEX use the public export checksum; for owned schema definitions use DBMS_METADATA plus dictionary object inventory. Unknown/unreadable objects block the comparison. Record target-specific settings separately; no general SQL parser or automatic drift adoption. A disconnected worker cannot be replaced while it may still write: stop/verify its sessions and subprocesses, inspect state and issue a new epoch before recovery.

Proposed command surface keeps the accepted build/qualify/promote entry points and adds narrowly scoped area/task/capture/recovery helpers. Exact argument parsing is finalized with the test skeletons after approval. No daemon, scheduler or plugin framework is introduced. The runner supports --smoke, --unit, --integration and --new-only; unsupported/missing tests fail rather than returning an empty successful gate.

## Supported interfaces and feasibility

Oracle documents [APEX_APPLICATION_INSTALL](https://docs.oracle.com/en/database/oracle/apex/24.2/aeapi/APEX_APPLICATION_INSTALL.html) for installation mappings, [APEX_EXPORT.GET_APPLICATION](https://docs.oracle.com/en/database/oracle/apex/24.2/aeapi/GET_APPLICATION_Function.html) for split exports/original IDs and identity-independent checksums, [restricted application status](https://docs.oracle.com/en/database/oracle/apex/24.2/aeapi/APEX_APPLICATION_ADMIN.SET_APPLICATION_STATUS-Procedure.html), and [SQLcl 25.3 Liquibase](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/liquibase.html) for migration commands. These references were checked during design. They support the selected primitives; their composition, required grants and failure behavior remain experiment results to obtain. The existing architecture's AI-1–10 inventory supplies the remaining supported-interface obligations.

The main risks are stable private-target source identities, import-time maintenance enforcement, supported unattended credential/provisioning paths, stale-worker exclusion and partial-state repair. Test these early, rather than hiding failures behind additional orchestration. Authoring through App Builder is allowed; unattended administration/capture/delivery must use supported APIs. A failed feasibility experiment may justify a new design or further Elaboration, not a pass for the unresolved requirement.

## PBI-012 through PBI-016

PBI-012 maintains one concise evidence report grouping the test profile's cases by architectural question: isolation/bootstrap/reservations; assembly/capture/integration; qualification/promotion; drift/maintenance/recovery. For each report actual tools, command, outcome, duration/resources and remaining limits. Distinguish local candidate review from unexercised remote PR automation, concurrent clients from human collaboration, and automated browser evidence from second-operator reproduction.

PBI-013 updates the shared SRS only for evidence-backed corrections, retaining stable actors/use-case IDs and linking the experiment. PBI-014 updates the shared architecture/test profile with validated choices and explicit remaining gaps. Neither modifies another sprint's records. Material scope/control changes return for managed approval.

PBI-015 proposes a Lifecycle Architecture decision after the core proofs. Essential ownership, capture/import, exact-artifact promotion, maintenance or data-preserving recovery gaps mean further Elaboration. PBI-016 proposes the smallest Construction sequence from accepted evidence and measured effort; a later sprint is not activated automatically. Any root backlog/plan changes use their required adapters and Product Owner authority.

### Testing Strategy

Test and Regression remain smoke, unit, integration with full regression. Run new-only A1 smoke, A2 unit, A3 integration in sequence, then full B1/B2/B3; retain timestamped redacted logs and actual exit codes. Stop progression at a failed gate; use the method's managed retry rule. These commands are future interfaces, not working examples at this design stage.

Smoke targets are tool/target identity, required source/metadata, approved version/start combinations and live baseline checks; each should normally finish within one minute after the platform is ready. Unit targets are greeting composition/validation and immutable-history behavior from UT-1/2, plus pure manifest/ownership-map decisions under dedicated fixtures. Do not mock Oracle reservation/DDL semantics and call that concurrency evidence. Unit fixture mutations stay in a disposable schema.

Integration uses the real Oracle/APEX/ORDS stack, separately authenticated clients, browser automation and scoped synthetic data. IT-12's reservation barrier is the first concurrency proof; IT-8's deployment race is separate. IT-9 maintains active ordinary sessions and timed submissions across installation/interruption. Measure runtimes; initial planning allowance is 30–90 minutes for the full integration sequence excluding cold provisioning, with the failed-deployment/repair case explicitly included. This is an estimate, not a performance guarantee.

## Test Specification

SM-1/2/3 and UT-1/2 retain their definitions from the accepted [test profile](../../docs/test-profile.md). Proposed target files are tests/smoke/test_delivery.sh and tests/unit/test_greeting.sh with supporting SQL assertions. Smoke passes only after correct identities/HTTP route/versions, expected rejection paths and required fingerprints are observed. UT-1 passes exact greeting and boundary/Unicode/rejection assertions; UT-2 passes configuration/ownership rules and complete prior-history equality.

IT-1/2 cover capture/reconstruction and exact-artifact clean/upgrade/repeat delivery; target tests/integration/test_release.sh. IT-3 covers committed-DDL failure, observation-bound repair and unchanged sentinels; target tests/integration/test_recovery.sh. Preconditions are qualified artifacts, known starting states, explicit disposable versus retained mappings and twenty staged sentinel rows. Success requires matching source/artifact/target receipts and all field-level preservation assertions; a successful SQL exit without those assertions is insufficient.

IT-4/5/6 cover Foundation assembly, genuine concurrent Hello/World development, shared bookkeeping/provenance and scope rejection; target tests/integration/test_development.sh. IT-7/8/9 cover live drift, competing deployments, interruption and actual browser maintenance/state/verifier behavior; target tests/integration/test_controls.sh. IT-10/11 cover supported initial adoption, private-area onboarding and a complete local developer cycle; target tests/integration/test_development.sh. IT-12 uses synchronized clients in tests/integration/test_reservations.sh; both named developers must be observed winning in controlled repetitions, and every race has exactly one winner.

Traceability: child 1 uses SM-1/IT-11; child 2 uses IT-6/8/12; child 3 uses SM-2/IT-4; child 4 uses IT-1/5/10; child 5 uses UT-1/2 and IT-5/6/11; child 6 uses SM-1/2 and IT-1/2; child 7 uses SM-2/3 and IT-7/8/9; child 8 uses IT-3/9. PBI-012 summarizes all cases; PBI-013–016 are reviewed against their resulting evidence and acceptance criteria rather than given artificial code tests.

Executable skeletons, component/new-test manifests and the first expected-failure run follow design approval under local P8. Their absence now is intentional; no test_specified or passing status is claimed.

## Effort, resources and checkpoints

Prototype children total 40–64 engineering hours. Evidence synthesis, requirements/architecture reconciliation, milestone/planning and handover add approximately 16–24 hours: total planning range 56–88 engineering hours for one experienced implementor, roughly seven to eleven eight-hour days. These are human-equivalent planning estimates, not a prediction of agent wall time. Reviewer/operator participation is approximately two to four hours across design review and reproduction/handover; actual second-operator availability remains separate from automated execution.

Use the current owned VM: four vCPUs, 6 GiB RAM and its 30 GiB sparse disk, on the observed 48 GiB/12-logical-CPU host. Its destruction/reconstruction is authorized when useful; validate that lifecycle before retained prototype history is established. Keep A's area only as long as its stage needs it, run B/C concurrently, and reset one validation area sequentially; retain TEST and control data. The initial host observation was about 13 GiB free; the Product Owner will provide more space. Budget roughly 2–4 GiB additional tools/browser/cache and up to 2 GiB bounded artifacts/evidence as an initial estimate; measure actual guest/host headroom before provisioning. Keep one database runtime and leave unrelated resources alone.

Review feasibility after children 1–2, source stability after child 4, and the architecture decision after child 8. If any core proof fails or effort exceeds the proposed range, propose a smaller mechanism or a focused further Elaboration objective. Do not weaken acceptance, declare Lifecycle Architecture early or substitute a large custom platform.

## Approval requested

Approve this bounded decomposition, technical approach, evidence scope and effort/resource range before prototype code or executable test skeletons are constructed. The proposal is ready for review; no PBI is marked complete by writing it.

## Fresh-start walkthrough refinement — 2026-10-18

The Product Owner requests prerequisite checks and explicit scoped cleanup/install/destroy operations before the walkthrough, with no earlier greeting history carried into it. The existing database/APEX lab is disposable for this demonstration. Retain host credentials, verified tool/installer inputs, reviewed release archives and historical evidence; preserve unrelated Podman resources. Reuse the named VM and remove only the owned lab containers/storage/network/secret. Installation creates a new database/APEX/ORDS runtime, isolated empty areas and the control authority; application construction follows afterward.

Replay accepted Foundation/Hello source snapshots and the complete initial archive through native SQLcl/Liquibase and APEX import in A–C. D/E execute new initial qualification/promotion receipts for the retained reviewed archive. F qualifies the existing patch archive for both declared starts, then upgrades TEST without resetting it. Preservation applies to data created during this cycle; full cleanup is not failed-deployment repair. Live verification pauses for the browser; unattended rehearsal announces explicit runtime-API test data and does not claim browser verification. This refinement stays within PBI-011.1/3/4/6/7 and PBI-012; broader concurrent development, maintenance fencing, drift and repair selection remains unchanged.

## Infrastructure and project onboarding responsibilities — 2026-10-18

By Product Owner direction, Oracle infrastructure initialization ends at Database/APEX/ORDS and must not create project schemas/workspaces/accounts, including E1_CTRL. The platform operator separately initializes project control. A privileged operator provisions one named developer/qualification/TEST area per invocation; each developer independently configures only a private SQLcl profile using the assigned schema password, without reading the administrator secret store or creating database objects. A separate readiness check verifies all onboarded areas before A. Qualification reset reprovisions only qualification and its delivery grants. This refines the PBI-011.1/UC-8 preparation boundary; application delivery and broader proof scope remain unchanged.
