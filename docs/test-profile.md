# Project test profile

## Status and purpose

The [repository and pipeline draft](../progress/E.1/repo_layout.md#pipeline-paths-and-release-identities) maps source/artifact/environment roles to these checks. Keep it aligned with this contract and the linked E.1 execution evidence.

Concrete command contract for PBI-009, accepted with the revised I.1 analysis baseline on 2026-10-16. Commands below describe future E.1 interfaces; **none is claimed working or executed in I.1**. SQLcl, application sources, controllers and test runner do not yet exist as project deliverables. E.1 must implement and verify them after its own setup/design approval. This replaces unspecified toolchain fields with exact intended commands without implementing the application early.

I.1 has `Test: none` and `Regression: none`: document consistency, source review, read-only environment assessment and shell syntax are its checks. No PL/SQL tests or application test skeletons are created or run this sprint.

## Execution prerequisites for E.1

E.1 must take ownership of executing/adapting the I.1-owned [infrastructure lifecycle procedure](deploy.md), using it to provision, verify and destroy scoped experiment infrastructure as needed. I.1's analysis reference was Podman 6.0.0, database 23.26.3.0.0, APEX 24.2.0 and ORDS 25.3.0.r2671248 on 2026-10-16. Record the procedure/script revision and actual tool/image versions used. Validate lifecycle teardown with disposable fixtures only, preserving retained data, credentials and evidence. Do not assume a VM is already present or recreate infrastructure during ordinary application upgrades.

Run from the operator's project checkout. Use the selected single-host A/B/C proof: separate identities, private application/schema/workspace areas, independent checkouts and concurrent clients against one delivery-control authority. Provision approved collision-checked mappings for developer/task areas, a disposable validation area and retained TEST. Candidate and qualification roles may reuse the disposable area sequentially after verified reset; never run unaccepted candidate work in retained TEST. `LAB_DEV` and `LAB_TEST` are example initial mappings, not the only permitted areas. Bootstrap ownership/evidence authority before the first Foundation task; its records must survive ordinary Foundation changes/imports. Use SQLcl 25.3.0.274.1210 and Java 21 with recorded exact patch/checksums. Protected named connections `lab-dev` and `lab-test` must authenticate as their application schemas to `127.0.0.1:1521/FREEPDB1`; check effective identity before writes. Existing administrator credentials must not become CI credentials.

Proposed E.1 entry points, to implement under its accepted test design:

```bash
bash scripts/cicd-build.sh
bash scripts/cicd-qualify.sh .local-apex/releases/lab.tar
bash scripts/cicd-promote.sh .local-apex/releases/lab.tar lab-test
bash tests/run.sh --smoke
bash tests/run.sh --unit
bash tests/run.sh --integration
```

Build must validate the complete source set and package a clean reviewed revision as `.local-apex/releases/lab.tar`, with its commit/tool manifest and external SHA-256 receipt. Reject a dirty product source set or files missing from the declared complete-release/assembly-stage contract. A seed/Foundation-only artifact explicitly contains no application export; its component-specific assembly checks must not be reported as passing the full greeting release gates. Packaging does not export live DEV during promotion. Do not overwrite a retained archive: subsequent archives get distinct retained identities/paths. The example path identifies the selected run's archive. Qualification takes that archive, records its SHA-256/accepted commit, declared starting baseline and controlled nonsecret inputs, and proves clean complete installation plus the one declared additive upgrade path in disposable targets. Assembly archives instead qualify against their declared stage and component-specific checks; they cannot claim complete-release qualification. Promotion rejects missing qualification, changed bytes, an unsupported target start or mismatched configuration evidence. It uses those same qualified bytes; PR candidate validation is a separate gate. The project controller must run SQL from the verified archive rather than mutable checkout files. These entry points are proposed, not scripts delivered in I.1.

Smoke verifies target identity, database/APEX version, expected application identity, installed component versions and an HTTP route; declared initial assembly explicitly checks absence where appropriate and records unavailable full-application cases as not applicable, never passed; incorrect targets or incompatible/unknown version combinations fail before deployment writes. Unit tests use small PL/SQL assertions for composition/validation against dedicated test fixtures; no additional test framework is proposed. Integration qualifies/deploys and repeat-deploys the same archive, retaining seeded history. A retry may reuse it only after safe repeat/resume is established. A forward repair containing changed code/migrations uses a new reviewed archive qualified against the approved partial starting state; preserve the original archive and receipts. Every entry point returns zero only when all assertions pass, prints case IDs and outcomes, and retains a redacted timestamped log. The runner must support the method's `--new-only` manifest filter; unfiltered invocation is regression.

## Underlying tool commands

These interfaces are also **proposed and unrun**. Their referenced SQL files are to be created in E.1, not treated as existing working examples.

```bash
sql -version
java -version
sql -name lab-dev @deploy/export.sql
sql -name lab-qualify @deploy/validate.sql
sql -name lab-qualify @deploy/install.sql
sql -name lab-test @deploy/validate.sql
sql -name lab-test @deploy/install.sql
sql -name lab-test @tests/unit/greeting.sql
```

`lab-qualify` is a protected mapping to the disposable qualification role; candidate jobs use its separately reset candidate role, never TEST. The qualification/promotion controllers establish the verified archive execution directory and input mapping before invoking installation SQL. Low-level SQL commands alone are not a replacement for artifact/ownership/qualification gates.

`export.sql` loads `APP_ID` from the verified DEV mapping and runs:

```text
apex export -applicationid &APP_ID -split -skipExportDate -expOriginalIds -expSupportingObjects N
```

`validate.sql` guards identity, expected target revision, live fingerprints, state, component compatibility and the upgrade path before the first command below. The deployment controller repeats these checks under exclusive ownership before installation; validation alone does not reserve the target. `install.sql` guards identity, runs the second, sets the explicit APEX installation context, imports the split metadata and applies nonsecret target settings:

```text
lb validate -changelog-file db/changelog.xml
lb update -changelog-file db/changelog.xml
```

Options derive from the [APEX 24.2 export reference](https://docs.oracle.com/en/database/oracle/apex/24.2/aeadm/exporting-one-or-more-applications.html) and [SQLcl 25.3 Liquibase reference](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/liquibase.html). Prove shell exit behavior for SQL, Liquibase and APEX failures with negative cases; merely printing an error is insufficient.

## Required evidence, not tests implemented in I.1

**SM-1:** Expected target/version/application identity and HTTP route succeed; wrong schema/workspace/application mapping is rejected without writes.

**SM-2:** A reviewed Foundation/Hello/World version triple and supported upgrade path are accepted. An incompatible Hello/World pair, unsupported Foundation version, unexpectedly missing metadata and a mismatch between APEX labels and registry are rejected before deployment writes. Preserve the observed installed set on rejection. Do not infer compatibility from matching major versions alone.

**UT-1:** Seed composition is exactly `Hello World`; prefixes, Unicode and 100-character boundary entries work; empty, oversized and inactive selections fail. **UT-2:** Default ownership/deactivation rules and atomic history insertion hold; configuration changes leave earlier snapshots unchanged.

**IT-1:** Export twice without edits and inspect differences. Validate the current PR candidate in a disposable area; after merge build one accepted-revision archive, qualify those exact bytes for clean reconstruction and the declared additive upgrade, then promote them to TEST. Record unchanged archive hash, accepted commit, qualification/deployment receipts, target configuration identity and observed greeting. Reject stale PR evidence, changed bytes, missing qualification and unsupported starting versions. Verify disposable reset cannot touch TEST history. **IT-2:** Upgrade with an additive database change and a Hello or World change; all 20 prior sentinel history rows retain their complete values. Repeat the archive: migrations/seeds do not duplicate, TEST settings remain correct, and DEV data is unchanged. **IT-3:** A failing precheck blocks deployment; a separate failure after committed additive DDL stops subsequent steps. Inspect live partial definitions/version records and authorize a recovery linked to the failed attempt and current generation. Inject an intervening unexplained change and reject recovery until reviewed reconciliation. Qualify the selected new repair archive against the inspected partial state, recheck that starting state under ownership, repair and prove history preservation. Separately establish when unchanged bytes can safely resume. Incomplete observation/unsupported recovery stays blocked; logs alone do not prove what committed. A coordinated upgrade cannot report success with mixed versions. **IT-4:** From the reviewed greenfield seed and bootstrapped control authority, verify the explicit assembly manifest: Foundation-only component checks succeed and release A's reservation while root maintenance blocks ordinary/incomplete dependent behavior; deliberately absent Hello/World are recorded without fake versions. Allow only the declared subsequent assembly stages. Require the complete approved triple for the first operational TEST release. The same missing metadata on a previously complete target is rejected. Show Foundation, Hello and World labels, compare them with artifact metadata and installed records, and verify accepted/rejected complete version sets. These are future cases, not tests implemented in I.1.

Automated browser checks sign in, edit each component independently, submit a greeting, reject invalid values, display escaped markup, refresh history and check pagination with 21 rows. SQL and HTTP 200 cannot substitute for that evidence. Manual walkthroughs supplement these automated checks. E.1 covers its accepted thin slice; full-page behavior remains a release gate if deferred from the prototype.

All fixtures are synthetic and confined to dedicated lab targets. Never discard retained history, touch unrelated resources or log secrets; scope teardown to the owned disposable experiment instance. Use local services for execution after tools are provisioned. Record prerequisite failures separately from product failures. Before activating E.1, obtain Product Owner acceptance of this command contract; before claiming tests pass, implement and actually execute them.

## Collaboration evidence proposed after use-case refinement

**IT-5 — Core multi-developer journey:** A starts from the reviewed greenfield seed (or the separately verified UC-12 adoption path), reserves and delivers Foundation through a task branch/PR, passes component-specific assembly checks and releases ownership while the root remains maintenance. Foundation must reconstruct without Hello/World-owned objects. No completed Hello/World application is supplied to bypass their authoring work. From its accepted baseline, B and C reserve and develop Hello and World on separate task branches/targets. The two different-component reservations must coexist. Capture their actual APEX definitions through SQLcl into the appropriate checkout; verify canonical identity/path handling, deletion reconciliation and an unchanged second capture. Reject wrong source mappings or unsafe overwrites of uncommitted work. Merge, import the combined SQL into the validation target and show both intended changes, correct component versions and retained history. Record which state was private/shared. B/C each add a component-owned page/navigation entry so both exports touch shared bookkeeping; retain both additions. After B's acceptance, C incorporates B's accepted revision without treating inherited Hello changes as new C-authored edits. Preserve provenance and revalidate the candidate. The complete accepted application deploys under target ownership without reacquiring authoring reservations for completed/unchanged components.

**IT-6 — Scope enforcement and exceptional reconciliation:** Attempt to capture or integrate a change outside semantic ownership and reject it, including an unauthorized change to shared composition/security/controller behavior. Allow only bounded validated generated-file reconciliation. Discover additional task scope, preserve work, atomically request the complete expanded set and return a conflict if unavailable; verify no partial acquisition or indefinite hold-and-wait. Revalidate the base before resuming. In an explicitly controlled out-of-tool/break-glass variation, introduce same-page/shared version metadata conflicts, then require reviewed reconciliation and renewed import/behavior checks. This variation does not permit two managed tasks to own Hello concurrently. Exercise a page deletion and colliding/ordered database changes. Reject missing dependencies, duplicate page/component identities and stale exports rather than silently dropping work. Use native Working Copy repair only as a break-glass variation, returning the change through reconciliation/PR. Its replacement semantics do not prove Git merge behavior or schema isolation.

E.1 must refine and validate a feasible task-area layout within the selected single-host proof and validate export identity stability before this experiment. These are future case specifications only. No task branches, developer schemas, APEX copies or executable tests were created in I.1.

For the PR flow, IT-5/6 must validate the combined task/target-branch candidate before merge. A changed PR or integration baseline invalidates an earlier result until the updated candidate passes. A failed foundation/compatibility or APEX integration gate blocks merge; CD uses the accepted merged revision. These are pipeline acceptance requirements, not a workflow implemented in I.1.

## Drift, concurrency and state evidence proposed for E.1

**SM-3:** A stale expected generation or changed live APEX fingerprint blocks installation without changing the running target to failed. Missing/mismatched fingerprint profiles or baseline metadata also block an existing-target deploy. Only explicitly approved first provisioning may start without an installed base.

**IT-7 — Drift and break-glass reconciliation:** Establish a successful baseline; recompute its fingerprint without edits and obtain the same result. Change a page in App Builder without changing its version; detect drift and preserve the changed source before any deployment overwrite. Check page deletion/shared metadata coverage and a separate manual schema change. Reconcile a retained emergency fix through a reviewed branch and controlled deployment. Record exact export options and any target-configuration differences. Do not treat an old artifact checksum or migration ledger alone as the live-content check.

**IT-8 — Concurrent deployment:** Two attempts expect the same target revision. Only the owner passing a fresh guarded check may mutate it; the other is rejected or rechecks and rejects the advanced generation. Cover the full application-import scope and dependency versions. Demonstrate how emergency editing is excluded from the check/write interval; our own mutex does not lock App Builder itself. Prove ownership persists across DDL commits, SQLcl subprocesses and connection failure; after restart inspect durable authority/attempt records before recovery. A transaction row lock released by a commit is insufficient.

**IT-9 — State inheritance and recovery:** An untagged Hello page inherits Hello maintenance. An explicitly ready child cannot bypass a blocked ancestor; a failed Foundation blocks dependent actions. Exercise direct URLs, form submits and existing sessions, not merely hidden navigation. Prove maintenance → ready requires all checks, mutation failure remains blocked with a reason, and an interrupted controller cannot silently restore readiness. Reject invalid/missing root state and preserve target state across imports. Verify controlled diagnostics remain usable. After preliminary installation/integrity checks, a dedicated deployment-scoped verifier must exercise the real greeting/history path while ordinary direct submissions and existing sessions remain blocked. Bypass only the active deployment-maintenance restriction; failed/unknown dependencies and normal authorization still block, and negative state tests must observe them. Cover draining/fencing active mutations, no unrestricted import interval, stale verifier permission and interruption. Revoke permission and reconcile final availability/configuration/fingerprint evidence before publishing readiness. Identify verifier-created synthetic rows without changing retained history. Demonstrate authorized failed → maintenance → ready repair with history retained and consistent state/version/fingerprint receipts.

All cases above are specifications only. No SQL, test harness, drift collector, state registry or deployment lock has been implemented or exercised in I.1.


## Initial adoption and complete developer journey

**IT-10 — Bootstrap the golden source (UC-12):** Capture an identified source application and its required database/static dependencies without committing secrets or runtime business data. Record versions/profile/provenance, reconstruct the candidate Git revision in a controlled target and compare required definitions/behavior before accepting the baseline. Missing dependencies, an inconsistent capture, a populated unverified target or unsafe repository overwrite must block adoption. Prove that subsequent release packaging uses the accepted Git revision, not a fresh developer export.

**IT-11 — Developer onboarding and complete cycle (UC-8/9/10/7/4/11):** Start with a documented workstation/access state, verify supported software and permissions, obtain a private development area on the selected single host, and associate it with a task branch/base. Edit a focused page, capture/review/commit, submit and revise a PR, validate/merge, deploy, verify behavior/version/history/receipts, then refresh safely for the next task. Record the environment variant actually tested; do not claim both variants passed from one run. Missing permissions/tooling and uncaptured work must produce actionable blockers rather than silent data loss.

IT-10/11 are future evidence requirements, not implemented or executed tests. The existing smoke/unit/integration command contract remains proposed; Elaboration refines the bounded prototype cases before construction.


**IT-12 — Core early same-component rejection:** After the A/B/C component delivery cycle, synchronize B and C to request Hello in UC-9 from the same accepted base. Exactly one atomic reservation succeeds; the other returns a conflict identifying the owner/task before creating its managed branch, provisioning its task area or permitting editing. Assert no code/version/runtime-state change from the rejected request. Repeat with the other developer winning. Show that reservations of Hello and World can coexist and that reserving Hello prevents a competing task even on another Hello page. After verified completion or safe cancellation, the loser must obtain fresh ownership against the new accepted baseline. Validate stale-token rejection after authorized reassignment and atomic all-or-none acquisition for a change spanning multiple components.

IT-5 and IT-12 are required proof-of-concept evidence for the multi-developer design. IT-8 separately covers the target deployment race; it cannot substitute for early task rejection. These specifications have not been implemented or executed in I.1.

## Automation interface validation

SRS FR-13 is a foundation requirement. Validate architecture inventory AI-1–10 during Elaboration, at the depth of each approved experiment. For each entry record the exact tool/server versions, executable command or API sequence, target and required grants, inputs/outputs, successful unattended run, relevant rejection/failure case, exit status and redacted evidence. Mark each entry validated, failed or not yet exercised; a proposed API or successful administrator-only run does not establish routine CI readiness. This evidence requirement is part of selecting the tools, not a separate product feature.

Use the established cases rather than duplicating them: SM-1/IT-11 for connection/provisioning; IT-1/5/10 for capture/import; IT-2/3 for migrations; SM-3/IT-7 for drift; IT-8/9/12 and SM-2 for release/state/version/ownership controls; UT-1/2 and automated browser assertions for application behavior; IT-5/11 and scoped lifecycle experiments for orchestration/infrastructure. Recovery after an injected failure must also execute through the supported command/API path after the required human decision. Record any uncovered operation as an architectural gap and refine the plan before claiming the automation requirement satisfied. No interface validation or browser test implementation is claimed in I.1.

## Elaboration order and architecture exit

Refine PBI-011 into bounded children at E.1 setup/design, with approval before construction. First prove control bootstrap, topology/permissions and minimal atomic reservation/reassignment with concurrent clients; ownership feasibility must not wait until the full system exists. Then prove initial assembly, capture/identity and combined reconstruction, immutable archive qualification, guarded delivery/verification/repair, and the complete A/B/C cycle including the Hello race. Reuse the cases above rather than creating a feature per mechanism.

Lifecycle Architecture requires evidence for these core controls under the selected topology and supported clean/additive-upgrade/repair paths. Complete page layouts, exhaustive input combinations and additional workstation variants may remain for Construction. If critical feasibility remains open, propose further Elaboration instead of declaring the architecture stable. This is an experiment/exit recommendation, not an E.1 activation or child-PBI assignment.

### Bounded initial-release subcase

Run `bash tests/run.sh --integration --new-only tests/manifests/initial_release.manifest` after initial Q/TEST publication and explicit post-delivery sentinel preparation. This read-only delivery repeat check compares all retained history/configuration fields, requires matching successful archive receipts and live APEX fingerprints, and checks the fixture remains repeatable. It verifies the existing initial result; it does not perform fresh reconstruction. Full IT-1 upgrade/repeat-import and IT-2 patch criteria remain pending. Browser verification is separate, as documented in the E.1 test evidence.

### Selected Hello patch and protection increment

Run `bash tests/run.sh --integration --new-only tests/manifests/patch_protections.manifest` for IT-2, SM-2 and the focused IT-7 page-drift slice after both patch qualifications and TEST publication. IT-2 verifies identical-byte receipts for fresh/initial-upgrade starts, live fingerprints and field-level preservation of the retained 21-row baselines; its correction fixture rolls back. SM-2 exercises the incompatible proposal gate with before/after target/control comparisons. IT-7 checks real Oracle error propagation versus stored diagnostic text, injects the separately authored native page fixture, rejects drift and explicitly restores the original fingerprint while preserving data.

The fixture sequence replaces TEST APEX definitions and may require runtime re-login; stop other TEST authoring/deployment first. It does not rebuild/reset retained TEST or install business seed. The initial-release manifest applies only while both live targets still contain that initial release; it is historical after upgrading. The full IT-1 candidate/reconstruction gate and broader concurrency, schema drift, maintenance/verifier fencing and repair acceptance remain open; passing the selected manifest is not a full integration/sprint-completion claim.

### Fresh walkthrough lifecycle

Run `bash tests/run.sh --unit --new-only tests/manifests/walkthrough_lifecycle.manifest` for the cleanup ownership boundary: allow only the known lab inventory; reject unrelated consumers of named volumes/network/secret and unexpected mounts/images before mutation. These local policy tests do not substitute for Oracle isolation or concurrency tests. After A–H, run `bash tests/run.sh --integration --new-only tests/manifests/walkthrough_lifecycle.manifest` for the registered IT-2 result/preservation assertions against this fresh cycle; it does not rerun cleanup.

The same focused unit manifest also tests infrastructure exclusion, control-only setup, single-area provisioning/reset and developer password/profile scope. These mocks test responsibility boundaries, not Oracle concurrency.

The destructive fresh-start experiment is a separate explicit operator sequence in [deploy.md](deploy.md#fresh-walkthrough-infrastructure-sequence): prerequisites, named host preparation, complete lab cleanup and fresh database/APEX/ORDS installation. It must first prove **zero project schemas/workspaces immediately after infrastructure installation**. Then explicitly initialize project control, provision each named area, configure each developer with only their assigned password, and run readiness/isolation checks before A–H. Provisioning and private developer setup must not be hidden in infrastructure installation. It is not part of ordinary regression and must never be invoked as a hidden fixture reset. The A–H rehearsal then executes reviewed source installation, new qualification/promotion receipts, both patch starts, this-cycle field preservation and selected rejections/restoration. CLI runtime examples are explicitly synthetic verification; browser checkpoints remain separate in live mode. Archives/credentials remain on the host; no prior business history is restored. Broader concurrency/maintenance/recovery criteria remain unchanged.
