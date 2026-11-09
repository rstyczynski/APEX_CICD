# E.3 — Final lifecycle gap reassessment

Reopened correction dated 2026-11-05. This reassessment supersedes the earlier LC-1 completeness claim in the [scope record](sprint_E.3_pipeline_scope.md#lc-1-correction--native-release-omission-2026-11-05). The supplied [Understanding the Oracle APEX Application Development Lifecycle](../../refs/apex-lifecycle-management-v3.pdf), Version 3.2, June 2025, is the authoritative E.3 lifecycle reference. Printed page numbers below refer to that exact paper. [PLAN](../../PLAN.md) owns sprint state; [the correction record](sprint_E.3_release_correction.md) owns current validation and limitations; [BACKLOG](../../BACKLOG.md) owns follow-up criteria.

## Release preparation — PBI-058

Paper p.26 describes project release on main after merging the milestone branch, moving dist/releases/next into a numbered distribution. P.27 commits the native release changes, optionally tags, generates the artifact and deploys it. Historical E.3 v1.0.4 packaged next and did not run project release. This was a deviation from the requested native lifecycle and was missed by the closing gap review. GitHub Release Please did not replace this native operation. PBI-058 registers the defect and the Product Owner authorized its correction.

The corrected sequence retains export, stage and verify on the change branch; merges reviewed source/distribution; merges the proposed version/changelog; performs native release on main; reviews and commits the native metadata/distribution; then tags/publishes, generates and deploys the archive. Release Please proposes version/changelog only. Deployment rejects an unfrozen, mismatched or dirty source before target operations. Exact evidence and remaining qualification scope are in the correction record. Historical tags/receipts are preserved and do not retroactively qualify the fix.

## Target-product PR-only release preparation — PBI-059

On 2026-11-06 the Product Owner explicitly permitted the existing release-on-main sequence for the E.3 prototype and deferred its adjustment to the target product. The prototype follows the paper's simplified example on pp.26–27: run native release on main and commit its generated distribution and metadata. This demonstrates the native lifecycle, but the direct-main step is unsuitable for the target product's required pull-request controls. It is a governance gap to adapt, not a reason to remove native SQLcl release preparation or a claim that Oracle prohibits PR-based delivery.

[PBI-059](../../BACKLOG.md#pbi-059-require-pull-requests-for-target-product-release-preparation) owns PR review and validation of native release-generated files, protection against direct main writes, and publication from the accepted merged revision. The target implementation must adapt the paper's example to that policy. This item is Proposed and unscheduled; it does not redesign the E.3 prototype, reopen implementation, change sprint status or qualify PR-only release preparation as already delivered.

## Authoring, Git and collaboration

Paper pp.12–14 and 32 describe Working Copies, comparisons and coordinated Main checkpoints; E.3 demonstrated one serial checkpoint. Pp.18–20 describe PROJECT export/stage; these are native E.3 operations. Pp.32–39 describe private feature environments, update/conflict handling and review. E.3's shared-Main capture with Git PR review is a bounded adaptation, not proof of the complete feature-centric topology. Private branch environments remain PBI-056; broader contention/integration remains PBI-019 and central DEV synchronization remains PBI-042. PBI-020/035 retain completeness/adoption work. Optional common/mini-app subscriptions and authentication on pp.7 and 15–16 remain PBI-044; logical Foundation/Hello/World parts within one app do not demonstrate separate mini apps.

## Tests and quality inspection

Paper pp.22–25 and 45 cover PL/SQL tests, measured coverage and Cypress UI tests. Native PROJECT verification and bounded readiness/preservation checks do not substitute for that coverage. PBI-040 owns utPLSQL/coverage; PBI-034 owns automated browser journeys. Pp.30–31 and 45 describe Advisor and code/security/performance audits, retained by PBI-041. The wider automated build/test/deploy outcome remains PBI-043. A successful native package or import alone does not establish these capabilities.

## Environment mappings and automation

Paper pp.27–30 recommends separate DEV/TEST/PROD and explains target mappings. E.3 demonstrates author/target schemas and workspaces on one instance, not a fully independent production topology. GitHub environment variables supply nonsecret mappings, temporary properties select the native installer and secrets supply job credentials. The paper's committed properties example is adapted to the Product Owner's configuration policy. PBI-027/054 retain broader configuration and clean-host reproducibility requirements. The fresh disposable-schema attempt during this correction failed the inherited initial-data guard requiring E3_TARGET (ORA-20860); it is not qualified as a clean installation. PBI-054/038 own reproduction and supported initial-installation coverage. The prepared-host read-only credential exception remains limited to its explicit policy; it is not production compliance.

Paper pp.40–44 explicitly allows GitHub Actions and on-demand scheduling as alternatives to its Jenkins examples. Manual promotion is retained; no PR merge performs deployment. A runner-local ZIP is used by project deploy and uploaded separately as GitHub Actions artifacts. This is not a GitHub artifact-download promotion proof. Source, hash and local/remote run provenance must be distinguished. PBI-031/038/043 retain broader provenance/promotion outcomes.

The paper recommends private team repositories (pp.16–17 and 45). The public teaching seed/operator-lab repository is a deliberate topology departure, not implementation of that recommendation. Public PR jobs have no lab credentials/runner access; shared hosting and reuse controls remain PBI-025/026/032. A public teaching prototype does not qualify a private production delivery topology.

## Versions, identity and recovery

Paper p.2 uses APEX 24.2 and SQLcl 25.1.1; E.3 uses APEX 24.2 and the approved SQLcl 25.4.1.022.0618 / Java 21. This is an explicit qualified-tool adaptation, not silent adoption of latest SQLcl. The project's NFR-5 version/build gate takes precedence over the paper's download-latest sample helper. PBI-028 retains wider toolchain profiles. The APEX display/native app metadata mismatch remains PBI-057; correcting native distribution release does not implement that separate display requirement.

E.3 availability restrictions are not atomic fencing. Existing data checks cover selected tables/fields, not general DDL rollback or arbitrary recovery. Wider drift, fencing, identity and repair remain PBI-022–024/045, privileges/credentials PBI-025 and hosting PBI-026. Independent reproduction/comparison remains PBI-046/047. These are project protections beyond the narrow paper release example and are not presented as Oracle-prescribed acceptance tests.

## Decision boundary

Every remaining limitation above has an explicit backlog owner. The native release omission cannot be treated as a justified project choice. No new production-readiness or paper-wide compliance claim follows from PBI-058. Reclosure requires the actual corrected evidence and Product Owner review; the historical 2026-11-05 acceptance remains attributable to its original implementation.
