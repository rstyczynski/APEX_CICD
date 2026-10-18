# Repository and delivery pipeline — E.1 draft

## Purpose and status

This guide connects the shared Git repository, private developer areas and release pipeline so a Product Owner or agent can follow where each change goes.

**Elaboration draft, not an accepted final delivery.** [PBI-017](../../BACKLOG.md#pbi-017-deliver-a-repository-and-pipeline-reference-guide) tracks delivery of the consolidated reference. It is not assigned to a sprint. This draft records the E.1 design and implemented slice; it does not complete the backlog item or broader prototype proofs. Formal delivery should materialize the accepted guide as `docs/repo_layout.md` and update its incoming links.

## Related documents and sources

- [Product Owner handover](sprint_E.1_handover.md), [presentation walkthrough](sprint_E.1_increment_demo.md) and [completion assessment](sprint_E.1_assessment.md): demonstrated results and remaining architectural proofs.

Use this guide as a map; the linked documents retain their own responsibilities. Review both ends of these links when related behavior changes.

- [README](../../README.md): product purpose and main entry points.
- [SRS developer journey and use cases](../../docs/srs.md#complete-developer-journey): actor goals and acceptance; see UC-7/8/9/10/11 and UC-4/5.
- [Architecture: sources, packaging and promotion](../../docs/architecture.md#sources-packaging-and-promotion): source and release boundaries.
- [Architecture: developer/task integration](../../docs/architecture.md#developertask-integration-model): branches, integration and ownership.
- [Architecture: initial Git adoption and onboarding](../../docs/architecture.md#initial-git-adoption-and-developer-onboarding): source authority and private areas.
- [E.1 design](sprint_E.1_design.md): selected implementation and remaining architectural proofs.
- [Main walkthrough](cicd-walkthrough.md): ordered Product Owner demonstrations and exact script invocations.
- [Operator manual](user_manual.md): detailed operations, accounts and runtime use.
- [Infrastructure procedure](../../docs/deploy.md): scoped host/database/APEX/ORDS lifecycle and separate onboarding.
- [Test profile](../../docs/test-profile.md) and [E.1 results](sprint_E.1_tests.md): intended checks and actual evidence.

## One repository, three components

Foundation, Hello and World share one Git repository and form one APEX application per target. Component ownership is a change/review boundary; it is not a separate repository or deployment package.

1. **Foundation** supplies shared database contracts, greeting history, component/version records and the application shell.
2. **Hello** supplies Hello entries, configuration and owned pages/database behavior.
3. **World** supplies World entries, configuration and owned pages/database behavior.

A developer works with the dependencies installed in their private area. They can see the whole assembly present there, while their managed task authorizes a declared component scope. Broad App Builder access within a private workspace does not technically prevent other local edits; ownership and review must control accepted changes. Ordinary schema credentials cannot read/write another developer's private schema. This lab does not isolate developers from the host administrator.

See [component ownership and integration policy](../../docs/architecture.md#early-component-change-ownership) for shared-file and inherited-change rules, and [E.1 design](sprint_E.1_design.md) for what is implemented versus pending.

## Repository contents

These are the current versioned source locations, inspected against the repository. They have different roles in delivery.

- [apex/f810001/](../../apex/f810001/): complete native split APEX export. The canonical source application ID is mapped to each target during import; there is not a separate canonical export tree for every environment.
- [db/changelog.xml](../../db/changelog.xml) and [db/changes/](../../db/changes/): ordered database migrations. Applied changesets remain unchanged; a correction adds a later changeset.
- [deploy/](../../deploy/): guards, import/publication/verification SQL and project-control definitions. [control.sql](../../deploy/control.sql) and [release_control.sql](../../deploy/release_control.sql) bootstrap E1_CTRL separately from application migrations.
- [config/areas.json](../../config/areas.json): nonsecret schema/workspace/application mappings for the five areas.
- [release/inputs/](../../release/inputs/): exact historical archive-reconstruction recipes and original candidate evidence; see [input preparation](cicd-walkthrough.md#prepare-reviewed-release-inputs). Replay is not new candidate validation.
- [release/manifest.json](../../release/manifest.json): current release/component versions, dependencies, supported starts and capture/fingerprint/tool profiles. Current checkout describes release **1.0.1**, Foundation/World **1.0.0**, Hello **1.0.1**. Historical archives retain their own manifest.
- [release/proposals/foundation-major.json](../../release/proposals/foundation-major.json): incompatible-upgrade proposal used for rejection; it is not an installed Foundation 2.0.0 release.
- [scripts/](../../scripts/): small operator, pipeline and walkthrough entry points. Release controllers execute verified archive contents; see [cicd-artifact.py](../../scripts/cicd-artifact.py) for the exact package selection and integrity rules.
- [tests/](../../tests/): executable checks, SQL fixtures and test-selection manifests. Test examples are created explicitly; business data is not packaged as release seed.
- [docs/](../../docs/), [README](../../README.md) and [progress/E.1/](./): durable product guidance, orientation and current iteration design/evidence respectively.

The ignored `.local-apex/` holds local tools, protected credentials/connections, staging, immutable release archives and host evidence. These are not additional developer source repositories. Credentials and runtime business data do not belong in Git or release contents. E1_CTRL receipts live in the database; host logs are supporting evidence rather than substitutes for target state.

## Private areas and assembled applications

The public environment names are **integration_test** and **user_acceptance_test**. Their physical workspace/schema names are **E1_INTEGRATION** and **E1_UAT**; application IDs remain **810004** and **810005**. The script boundary accepts the former connection tokens as legacy aliases, but saved SQLcl connections and current configuration use the new names. Old physical schemas were removed only after evidence preservation; historical archives/receipts retain their original names and do not qualify the new mapping.

Integration testing is a deployment gate. Successful delivery to user_acceptance_test makes the release available for Product Owner acceptance; it does not itself record user acceptance.

Areas separate editing, release integration_test and retained operation within one database/APEX installation. Their authoritative identities are in [areas.json](../../config/areas.json).

- **A — lab-dev:** E1_DEV_A workspace/schema, application **810001**. Walkthrough A installs Foundation only.
- **B — lab-dev-b:** E1_DEV_B workspace/schema, application **810002**. Walkthrough B installs Foundation plus Hello.
- **C — lab-dev-c:** E1_DEV_C workspace/schema, application **810003**. Walkthrough C installs the complete 1.0.0 assembly. C owns its World/integration task, not an isolated World-only application.
- **integration_test — integration_test:** E1_INTEGRATION workspace/schema, application **810004**. Disposable reconstruction/upgrade verification before promotion.
- **user_acceptance_test — user_acceptance_test:** E1_UAT workspace/schema, application **810005**. Receives identical qualified archives and retains data during normal upgrades.

There is **no separate shared DEV deployment target** in this prototype. C demonstrates the complete development assembly. It is not the release source of truth: the accepted Git revision is. VERIFIER signs in to the particular application URL being checked; each workspace has its own account. VERIFIER has runtime access without App Builder/SQL Workshop privileges. See [provisioning and account instructions](cicd-walkthrough.md#provision-each-assigned-area).

## Developer branches and integration

The intended developer workflow uses independent checkouts/task branches against one shared repository. A branch is neither a private database nor proof of component ownership.

1. Reserve the declared component scope using the shared control authority before managed work.
2. Start a task branch from the accepted Git base and prepare its private APEX/schema area with the required dependencies.
3. Author the change, capture native APEX definitions into files and maintain migrations alongside them. App Builder Save alone does not update Git.
4. Validate and review the combined candidate against the current integration base. Incorporating another developer's accepted changes retains their provenance; new edits to their component need the corresponding ownership.
5. Accept/merge the reviewed source, then build a release from that accepted revision. Updated candidate/base invalidates earlier candidate evidence.

**Current walkthrough:** A–C replay reviewed sequential source snapshots from this repository; they do not create new developer branches or perform live PR authoring. Parallel Hello/World work, complete capture-scope/provenance enforcement and the competing-Hello race remain broader proofs. The [architecture integration model](../../docs/architecture.md#developertask-integration-model) defines the intended workflow; [current results](sprint_E.1_tests.md) delimit demonstrated behavior. No particular branch naming scheme or hosted CI service is established by this draft.

## Merging APEX export files

Native split application exports are SQL text: Git can diff and perform text merges on them. Keep the complete tree, including install/environment/shared-component files. The preferred source form is the unpacked split tree, rather than a ZIP marked as binary. Oracle explains the component-level review benefits in its [APEX 24.2 split-export guidance](https://docs.oracle.com/en/database/oracle/apex/24.2/aeadm/exporting-one-or-more-applications.html).

1. Start from a common accepted source/capture profile. Original-ID capture and omitted dates reduce noise; they do not by themselves prove cross-area identity stability.
2. Review different page files independently where possible. Shared navigation, application definitions, install lists, IDs and cross-page references can still collide even if page edits do not.
3. Have an APEX-aware reviewer resolve conflicts and inspect the combined tree. Do not automatically use one side for all generated files, or treat a clean line merge as application validation.
4. Import the complete candidate into a disposable area, check identity/dependencies/compilation and exercise affected runtime behavior. Check stable recapture as applicable. Parallel capture/merge and comprehensive provenance enforcement still need their planned E.1 proof.
5. Review database migration order and compatibility separately. Preserve already-applied changesets; corrections add later changesets. APEX export merging is not database-data merging.

Binary assets, when present, require suitable asset-specific handling. Their existence does not make the generated application SQL binary. No custom Git merge driver or blanket binary attribute is introduced by this guidance.

## Future pipeline automation

This is an extension proposal, not a hosted CI system delivered by E.1. No CI vendor or new sprint is selected.

1. A pull-request runner checks the declared task scope, accepted base, source diff, dependency manifest and combined candidate in a disposable area. A changed base invalidates earlier evidence.
2. After source acceptance, a release job builds one immutable archive from that accepted Git revision and retains provenance/hash.
3. An integration-test job runs required fresh/upgrade starts, runtime verification and publication checks on that archive.
4. A controlled promotion job checks the successful receipt and target preflight, then installs those same bytes in UAT while preserving data/configuration.

Protected branches, runner secrets/permissions, release approvals and concurrent task integration need design and verification before automation is claimed. The [presentation section](sprint_E.1_increment_demo.md#git-layout-cooperation-and-future-pipelines) introduces this proposal; the [assessment](sprint_E.1_assessment.md) retains the unfinished architectural proofs. The existing local operator scripts remain the implemented delivery path.

## Pipeline paths and release identities

The development team, acting as **Packager (A-02)**, smoke-checks the development assembly and releases the reviewed package. **Deployer (A-03)** takes that package through integration_test and promotes the identical bytes to user_acceptance_test. VERIFIER is the runtime account used by these people for checks, not a separate human role.

The editable [delivery model](model.drawio) shows the lifecycle and the numbered D integration_test sequence. Its **Deployer** maps to SRS actor A-03; keep the model and [walkthrough D](cicd-walkthrough.md#d-qualify-the-initial-release) synchronized with this guide.

The same source organization supports several bounded paths. An initial assembly checkpoint is different from a qualified complete release.

1. **Development assembly — A/B/C:** install reviewed Foundation-only, Foundation/Hello and complete source checkpoints into their private areas. Incomplete A/B remain unavailable. These steps do not pass through integration_test or promote anything to user_acceptance_test. C has an explicit bounded resume at its restricted-verification pause; it is not a general deployment-recovery mechanism. See [C’s continuation command](cicd-walkthrough.md#c-deliver-world-and-complete-the-assembly).
2. **Candidate validation:** check the combined revision before packaging. The current [candidate checker](../../scripts/cicd-candidate-check.sh) and [packager](../../scripts/cicd-artifact.py) bind validation evidence to the source commit; intended PR automation remains distinct from the scripted replay.
3. **Initial complete release — D/E:** verify one immutable 1.0.0 archive, qualify a fresh installation, then promote identical bytes to empty user_acceptance_test. Build does not copy live developer data or re-export DEV during promotion.
4. **Compatible patch — F:** verify the 1.0.1 archive; qualify both a fresh installation and upgrade from 1.0.0. Upgrade retained user_acceptance_test with those same bytes and compare pre-upgrade history/settings. integration_test may be recreated; user_acceptance_test is not reset by the patch.
5. **Incompatible proposal — G:** reject proposed Foundation 2.0.0 because the dependents require 1.0.0. No major-upgrade database migration is executed.
6. **Unexpected live change — H:** detect a controlled Home-page fingerprint mismatch and stop redeployment before maintenance/migration/import. Explicit fixture restoration is separate from deployment and is not automated failed-deployment repair.
7. **Failure recovery — designed, incomplete:** inspected failed additive deployment and automated forward repair remain unproved. Retain the original archive, attempts and data; do not claim the demonstration's whole-lab destruction is repair.

A **Git commit** identifies source, a **semantic version** identifies the declared contract, an **archive SHA-256** identifies packaged bytes, and a **live fingerprint** identifies observed APEX definitions. integration_test/promotion receipts bind these to a target and starting state. None alone proves functional correctness. See [manifest](../../release/manifest.json), [control implementation](../../deploy/release_control.sql), [test profile](../../docs/test-profile.md) and the [D–H walkthrough](cicd-walkthrough.md#d-qualify-the-initial-release).

## Maintenance and final-delivery gaps

Keep this draft synchronized with its authoritative sources and incoming references; update both sides when filenames, responsibilities or status change.

1. Reconcile source layout, manifest/package rules, area mappings and branch/integration behavior when the corresponding implementation changes.
2. Keep planned mechanisms separate from implemented and tested paths. Architecture/test-profile passages retained from Inception describe candidate contracts; the implementation and results provide current evidence.
3. Before PBI-017 acceptance, review this guide against the final selected pipeline, resolve stale descriptions, validate its links/examples and materialize the durable guide with updated backlinks.
4. Continue to report concurrency, complete maintenance/request fencing, broader schema drift and failed-additive repair as open until supported evidence exists. This document does not resolve Lifecycle Architecture or schedule another sprint.

## Retained initial UAT verification checkpoint

The [E continuation](cicd-walkthrough.md#resume-e-at-its-restricted-verification-checkpoint) reuses the same immutable Git-built initial archive and owned UAT attempt. It does not capture C, rebuild a package or reinstall the target. The browser assertion loop runs outside immutable archive contents; final publication still executes the archived SQL and guards. Keep this description synchronized with the [operator manual](user_manual.md#resume-initial-uat-verification) and [test profile](../../docs/test-profile.md#release-browser-verification-retry-and-bounded-uat-resume).

## Post-publication UAT examples

The [E examples continuation](cicd-walkthrough.md#resume-e-after-publication-prepare-upgrade-examples) validates the published initial archive and target fingerprint, then completes explicitly announced local test-data/baseline preparation. It does not create a new package or deployment receipt. The fixture selects active entries explicitly rather than depending on saved defaults, preserving operator settings. Existing baseline files are compared, never silently replaced. See the [operator manual](user_manual.md#resume-uat-upgrade-example-preparation).
