# E.1 — Answers to external review 1

Response to [sprint_E.1_review-1.md](sprint_E.1_review-1.md), reviewed on 2026-10-18. The expert reviewed public commit `0f5ce70`; the local committed baseline is the same. This response checks the findings against source, existing evidence and a small read-only experiment. It proposes corrections; it does not claim they are implemented or change sprint/backlog status.

## Overall answer

The review identifies material defects. The most important is **independent reproducibility**: our demonstrated rebuild preserves host archives, while the public clone does not supply or automatically reconstruct them. The README's fresh-start journey is therefore incomplete for a new operator. Successful delivery on the existing host does not resolve this gap.

Accept the identifier-validation, partial-DDL, exit-status and test-provenance findings. Treat upgrade offsets as an unvalidated identity policy whose user-state impact still requires a targeted experiment. Keep exact version checks as an intentional prototype boundary, while removing duplicated declarations over time. A general platform or immediate Linux integration runner is not needed to address these issues.

The review's positive assessment also needs boundaries: same-artifact promotion and selected guards are evidenced, but builds are not independently reproducible from Git alone, publication is not a transaction covering the entire migration/import, and complete concurrent/request/verifier fencing remains open. The [assessment](sprint_E.1_assessment.md) remains the completion boundary.

## High-severity findings

### H1. Fresh clones cannot reproduce the walkthrough

**Agree; a release-blocking defect for the reusable public example.** [Prerequisites](../../scripts/cicd-walkthrough-prerequisites.sh) reads `initial-selected.txt` and `patch-selected.txt` under ignored `.local-apex/releases/` before destruction. No release archives are tracked. The current [patch manifest](../../release/manifest.json) pins `base_artifact` to `d99fe83e…02ab45`, and [patch admission](../../deploy/release_control.sql) requires its matching initial receipt, otherwise ORA-20642.

[Packaging](../../scripts/cicd-artifact.py) fixes tar ordering/mode/timestamps, but includes both `candidate.log` and `candidate.json`; the latter contains the log hash. Candidate execution output can vary. Thus packaging is deterministic for identical input bytes, not necessarily for a fresh validation run of the same source. Moving only the raw log outside the archive would not solve it if its changing hash remains in the package identity.

The two historical assembly commits are present in Git. Referencing them is not itself a full-clone blocker, although abbreviated commits and shallow clones make the contract brittle. Tags/full commit IDs would improve selection but would not supply the missing archives or remove validation's dependency on the development runtime.

**Proposed correction:** first provide a verified acquisition path for the existing exact initial/patch archives, for example versioned GitHub Release assets with their full hashes/source identities and required download instructions. That is the shortest way to reproduce this historical walkthrough. Independently design deterministic source payloads with validation evidence stored and bound separately, then build a new reviewed release chain. Do not silently edit retained archives or overwrite the current baseline hash. Stable tags identify source; asset hashes identify bytes; neither replaces actual validation.

**Acceptance:** on a second clean checkout with no copied `.local-apex/`, acquire documented prerequisites, obtain/build release inputs, run A–H and match initial/patch receipts. A deterministic-build claim additionally requires two isolated builds from the same accepted inputs to have identical payload hashes, with variable logs still retained as evidence.

### H2. Configuration is interpolated into privileged SQL without validation

**Agree.** [Platform provisioning](../../scripts/cicd-platform.py) formats schema/workspace names and application IDs into queries, DDL and APEX administration calls. It uses `admin=True`; [the SQL boundary](../../scripts/apex_sql.py) then connects as SYSDBA. Tracked configuration is operator-controlled input, so this is not an exposed anonymous HTTP injection endpoint. Nevertheless, malformed or compromised configuration must not become privileged SQL.

The [isolation helper](../../scripts/cicd-isolation.py) validates identifiers locally, but that protection is not shared by provisioning. Validating just schema names would also miss workspace string literals, numeric IDs, connection tokens and other interpolated values.

**Proposed correction:** validate the complete area configuration before any Oracle connection: a deliberately restricted unquoted identifier grammar/length, positive bounded integer IDs, valid known target tokens and uniqueness of mappings. Reject invalid values rather than sanitize them. Use bind variables for data where supported and checked identifiers/`DBMS_ASSERT` for dynamic DDL. Separate necessary SYS-level infrastructure installation from a project-provisioning identity with explicitly tested grants. Do not merely rename a broadly privileged account and call it least privilege.

**Acceptance:** invalid quotes, separators, identifiers and IDs fail before execution; valid provisioning/reset remains confined to owned areas. Prove the provisioning account's allowed and denied operations. Ordinary migration/import continues under its target identity, not SYS.

### H3. A migration can partially commit

**Agree; this is a core unfinished recovery proof.** [Changeset 005](../../db/changes/005-hello-1.0.1.sql) adds a constraint, replaces a trigger and updates a component version within one [Liquibase changeset](../../db/changelog.xml). Oracle commits before syntactically valid DDL and after successful DDL. A subsequent failure can leave the constraint committed without a successful changeset receipt. Rerunning can encounter ORA-02264. See [Oracle COMMIT semantics](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/COMMIT.html).

Stopping on failure and retaining ownership prevents a success claim; it does not repair the partial schema. That remains [PBI-011.8](sprint_E.1_design.md#pbi-0118--failed-additive-deployment-and-forward-repair).

**Proposed correction:** use smaller future changesets around independently committed DDL boundaries, with explicit expected-start checks. Splitting alone cannot remove the crash window between a successful DDL and recording the Liquibase result. Preconditions must distinguish absent, exactly matching and conflicting objects; do not blanket `MARK_RAN` or ignore duplicate-object errors. Version publication must follow validated schema/application state.

Do **not** rewrite the already deployed 005 file or clear checksums to conceal the mismatch. Define a reviewed recovery transition/new repair artifact for the known partial start, preserving original archives, attempts, Liquibase history and business data.

**Acceptance:** inject failure after the constraint commits, retain the failed attempt, reject blind normal retry, then execute a reviewed automated forward repair and verify schema, component version, prior configuration and history. Whole-lab destruction is not the repair.

## Medium-severity findings

### M1. Oracle error codes can become shell success

**Agree; reproduced.** The four listed infrastructure paths use `WHENEVER SQLERROR EXIT SQL.SQLCODE`: [configuration](../../scripts/apex-configure.sh), [verification wrapper](../../scripts/apex-verify.sh), [APEX installation](../../scripts/apex-db-install.sql) and [database verification](../../scripts/apex-db-verify.sql). Oracle documents that Unix SQL*Plus return codes occupy one byte, [0–255](https://docs.oracle.com/en/database/oracle/oracle-database/18/unxar/administering-sqlplus.html).

A read-only native SQL*Plus block raising ORA-20224 produced:

- `EXIT SQL.SQLCODE ROLLBACK`: process return **0**, expected Oracle error present.
- `EXIT FAILURE ROLLBACK`: process return **1**, the same error present.

No DDL or application data was changed. The reviewer’s example need not be a naturally occurring ORA-00512; a valid application error divisible by 256 demonstrates the defect.

**Proposed correction/acceptance:** use `EXIT FAILURE` plus OS-error handling on every wrapper path, retain detailed diagnostics and require a server-side completion marker for assertions where appropriate. Test SQL, PL/SQL, client-command, connection and OS failures. The main Python SQL boundary already uses failure status plus a marker; that does not protect these separate infrastructure scripts.

### M2. Patch imports regenerate the APEX offset

**Agree with the code finding; user-state damage is not yet established.** [Patch import](../../deploy/operator/import_patch.sql) calls `GENERATE_OFFSET` on every invocation. Oracle describes [offset generation](https://docs.oracle.com/en/database/oracle/apex/24.2/aeapi/GENERATE_OFFSET-Procedure.html) and [SET_OFFSET](https://docs.oracle.com/en/database/oracle/apex/24.2/aeapi/SET_OFFSET-Procedure.html) as installation-context mechanisms for avoiding metadata collisions. This is not proof that regenerating on replacement preserves every installed component identity.

The existing 21-row preservation check covers our business tables/configuration, **not** saved interactive reports, subscriptions or active APEX sessions. It cannot answer this risk. The [drift fixture](../../scripts/cicd-drift-demo.py) already demonstrates reusing the existing offset for its separate import/restore operation.

**Proposed correction:** establish and record an application-specific target offset on first installation; verify and reuse it for replacement imports. Inspect the installed/exported identity with supported interfaces; `GET_OFFSET` reads installation context, not an arbitrary installed application's history. Avoid a blanket global constant or private APEX repository-table updates.

**Acceptance:** compare component IDs across repeated imports/upgrades and verify saved reports/subscriptions where those features are included. Prove that wrong/missing identity context is rejected. Until then, do not claim general preservation of APEX user state.

### M3. Environment identities and endpoint are duplicated

**Agree.** [areas.json](../../config/areas.json) coexists with hardcoded target/schema/app mappings in shell/SQL and fixed endpoint/Java paths in [apex_sql.py](../../scripts/apex_sql.py). Exact config-hash comparison catches some changed-input mismatches; it does not establish that every literal agrees with that config.

**Proposed correction/acceptance:** one validated nonsecret mapping/profile, consumed consistently by host commands and a verified deployment-target contract. Keep target-side allowlists and identity checks, deriving or validating them against that contract rather than deleting them. Test mapping disagreement as a rejection before mutation. Make endpoint configuration explicit without introducing a general environment platform.

### M4. Versions are hardcoded

**Partly agree.** Exact checks in [release_environment.sql](../../deploy/checks/release_environment.sql), the [artifact inspector](../../scripts/cicd-artifact.py) and [compatibility checker](../../scripts/cicd-compatibility.py) deliberately restrict this prototype to the tested toolchain and two component triples. Rejecting an unvalidated version is the correct default. These checks are not evidence that SQLcl only supports this database/APEX version.

The maintenance issue is duplicated declarations and updating code to express every supported profile. Move verified environment/start/compatibility rules into a versioned validated profile, and retain an explicit qualification gate for adding another combination. Do not replace exact rules with permissive semantic-version ranges without contract tests.

**Acceptance:** unknown combinations still reject; a newly approved profile has fresh/upgrade evidence and consistent source, installed metadata and receipts.

### M5. Test provenance and the trust model

**Agree, with a correction.** The clean-tree scope includes **`tests/sql`**, not zero test files. It excludes [tests/run.sh](../../tests/run.sh), shell/Python test code and [manifests](../../tests/manifests/). The [candidate checker](../../scripts/cicd-candidate-check.sh) executes the working-tree runner, so uncommitted changes to excluded tests can affect the claimed result. Expand the checked/packaged execution scope or, preferably, run the complete candidate harness from a clean immutable checkout. Bind its revision, manifest, tools and result to the candidate/base.

Integration qualification is written through the [E1_CTRL package](../../deploy/release_control.sql), not a freely writable integration-owned receipt table. However, the authorized integration identity supplies publication assertions/fingerprints through that interface. The same host owner controls credentials, scripts and database administration. This proves protection against mistakes and competing ordinary operations within the lab trust boundary, not independent attestation against a malicious runner or administrator.

Secrets are in protected local files and saved connections under one operator's control. File mode 0600 and redaction reduce exposure; they are not secret encryption or role separation. Creation mode also does not automatically repair an existing file's insecure permissions.

**Acceptance:** dirty runner/manifest/Python-test edits reject; the executed test revision is identifiable. Before a shared/hosted pipeline, separate bootstrap/provisioning, integration, promotion and runtime credentials/permissions, with protected release authority. Do not add a signing service merely to conceal the current lab trust model.

### M6. Output-text matching can misclassify failures

**Partly agree.** [Release](../../scripts/cicd-release-step.sh) and [patch](../../scripts/cicd-patch-step.sh) controllers already require both nonzero-status rejection and a server-side completion marker; they additionally reject diagnostic patterns including broad `^Error` matches. They are not relying only on matching output text.

That extra scan can produce false positives; relying only on status/marker would also miss tool-specific failures that continue and reach the final marker. In particular, SQLcl client/Liquibase commands need explicit tested failure handling, not assumptions about `WHENEVER SQLERROR` covering every client operation.

**Proposed correction/acceptance:** keep fail-closed status and operation-specific markers; make diagnostic classification narrow and tested, adding structured results where the tool supports them. Test harmless diagnostic-looking text, real SQL/client/Liquibase errors, missing markers and failure output with misleading success text. Existing drift classification tests cover only a selected part of this problem.

## Lower-severity findings

### L1. Host platform is missing from README prerequisites

**Agree.** [Prerequisites](../../scripts/cicd-walkthrough-prerequisites.sh) explicitly requires Darwin/arm64, macOS tools and a macOS JDK layout. The public README says Podman on one host without prominently stating **macOS Apple Silicon**. Describe that as the supported lab-provisioning path; pure Python/source checks need not inherit that restriction. Linux provisioning/integration is future work, not an already portable walkthrough.

**Acceptance:** README prerequisites and failure messages agree, and supported-host installation is independently reproduced. No cross-platform support claim without execution evidence.

### L2. Unneeded gateway accounts/features are enabled

**Agree on the configuration; assess necessity rather than disable blindly.** [apex-configure.sh](../../scripts/apex-configure.sh) unlocks ANONYMOUS; [ORDS installation](../../scripts/apex-ords-install.sh) enables SQL Developer Web, REST-enabled SQL and Database API. The selected delivery path uses SQLcl/JDBC plus APEX runtime; these extra web features have no demonstrated pipeline requirement. Loopback binding limits exposure but does not justify unused functionality.

**Proposed correction/acceptance:** use a minimal declared ORDS profile and lock unused accounts after verifying the required proxied APEX gateway path. Preserve the Oracle-required accounts and grants; test App Builder, runtime, assets and export/import afterward. Decide any separately wanted database web tooling explicitly. No immediate live reconfiguration is performed by this answer.

### L3. There is no CI workflow

**Agree on the missing automation, not on treating every `--unit` test as pure Python.** No `.github/workflows` is tracked. Some Python and shell outcome tests are suitable for a small hosted job, while the default unit manifest invokes SQLcl/database composition/history checks. Start with an explicit database-free manifest and pinned/checkable tools, then add shell linting against the supported Bash version.

A Linux database integration job is useful later, but it must also solve APEX/ORDS installation, required installers, resource limits, release acquisition and runner-secret boundaries. A running gvenzl database image alone does not reproduce this full APEX lab. Hosted CI was already labeled a future extension in the deck/[guide](repo_layout.md#future-pipeline-automation); that disclosure does not replace implementing reproducibility.

### L4. Licensing and binary material

**Agree that distribution needs an explicit decision.** There is no root project LICENSE. Public visibility does not itself grant an open-source license. The Product Owner must select a license for original project material and review third-party/submodule/generated-source terms before a licensing claim is made.

The supplied [Oracle PDF](../../refs/apex-lifecycle-management-v3.pdf) is about 13 MB. The fact that it was supplied for research is not redistribution permission; this review has not established such permission. Prefer an authoritative external link unless redistribution rights are confirmed. Removing a current-tree file alone also leaves it in already published history; assess any history action separately before making disruptive changes.

The PPTX and supporting images are intentional review deliverables, not application source. Their binary format is not itself a defect. Keep only useful artifacts, review their ownership/content and manage repository size separately. Do not silently delete the requested presentation in response to a general binary-file concern.

## Recommended order

1. **Independent reproduction and publication clarity:** state the supported host/missing release-acquisition boundary; provide verified historical artifacts or a complete new deterministic release chain. Resolve root licensing and PDF distribution before presenting the project as freely reusable.
2. **Correctness before additional automation:** reject invalid provisioning inputs, fix infrastructure exit handling, enforce complete test provenance and establish stable upgrade identities. Use a separate provisioning privilege boundary.
3. **Finish the core architectural proofs:** exercise partial additive DDL plus forward repair, real contention/parallel integration and complete fencing/schema drift already identified in the design. Preserve deployed migration/archive history while doing so.
4. **Automate the proven flow:** add database-free CI/lint first; consider full integration runners after clean-clone reproduction works. Generalized versions, another host OS or a broader delivery platform are not prerequisites for repairing the bounded example.

This is an engineering recommendation, not a new sprint schedule or an assertion that these fixes passed. Changes to backlog, approved scope or sprint status must use the existing project procedures.

## Checks performed for this response

- Inspected current scripts, provisioning/import SQL, release control, migration/changelog, profiles, candidate packaging and runner/test manifests against the expert's reviewed commit.
- Confirmed the historical assembly commits exist, no archive tar files are tracked and no GitHub workflows are tracked. Did not execute a fresh-clone end-to-end rebuild.
- Ran `bash tests/run.sh --unit --new-only tests/manifests/drift_review.manifest`: **1 wrapper passed**, five underlying Python cases.
- Ran `bash tests/run.sh --unit --new-only tests/manifests/protection_outcomes.manifest`: **10 passed, 0 failed**. Expected negative-case diagnostic lines are part of the passing assertions, not fresh live deployment failures.
- Executed the two native SQL*Plus error-status probes described in M1. Both raised only ORA-20224 and rolled back; no schema/application/history change.
- No induced DDL failure, offset-changing import, report/subscription loss test, credential/feature reconfiguration, archive publication or runtime fix was performed. The expert's source review and this response do not replace independent full acceptance testing.

Related: [expert review](sprint_E.1_review-1.md), [handover](sprint_E.1_handover.md), [completion assessment](sprint_E.1_assessment.md), [architecture](../../docs/architecture.md), [test profile](../../docs/test-profile.md), [repository guide](repo_layout.md) and [implementation record](sprint_E.1_implementation.md).
