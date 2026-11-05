# E.3 — Native release correction (PBI-058)

The Product Owner reopened E.3 on 2026-11-05 and directed implementation through completion. The [Oracle lifecycle paper](../../refs/apex-lifecycle-management-v3.pdf), Version 3.2, June 2025, is the authoritative E.3 reference. Printed pp.26–27 require native release preparation, review/commit, optional tag, artifact generation and deployment in that order. This record supersedes the earlier design exclusion of project release. [Analysis](sprint_E.3_analysis.md#pbi-058--native-release-correction-2026-11-05), [design](sprint_E.3_design.md#pbi-058--native-release-preparation), [final gap reassessment](sprint_E.3_final_gap_analysis.md), [walkthrough](sprint_E.3_increment_demo.md#native-release-preparation--oracle-paper-pp2627), [PLAN](../../PLAN.md) and [PBI-058](../../BACKLOG.md#pbi-058-fix-e3-omission-of-native-sqlcl-project-release) define the related authorities.

## Implementation

Release Please now proposes version/changelog only; skip-github-release prevents premature publication. The operator runs sql/release.sql on main after the milestone and version merges, reviews the numbered distribution and metadata, commits them, then tags/publishes the accepted commit. The manual deployment workflow rejects unfrozen, mismatched or dirty source before native setup and target mutation. Native verify, gen-artifact and deploy retain their responsibilities. Missing-changeset qualification derives the numbered distribution path instead of assuming next. No native release is hidden inside packaging or performed after the selected tag.

The local baseline.bundle now contains native release 1.0.5 and the corrected controller at 5e0ac11fb93955f3806f5b55f917eb0c36196864, with historical tags preserved. This is a local seed update; no remote push or GitHub publication is claimed. The live historical seed repository can differ until an authorized publication. The creation walkthrough must use the local bundle for this correction, rather than silently fetching the older seed main.

## Fresh execution evidence

Actual SQLcl release/build was 25.4.1.022.0618 with Java 21 and project sqlcl.version 25.4.1.0; metadata was not edited to bypass compatibility. Native project release moved next to 1.0.5 and set lastReleaseVersion. The native changes were committed before artifact generation. [release.log](tests/release-correction/release.log), [verify.log](tests/release-correction/verify.log) and [package.log](tests/release-correction/package.log) retain the native results. Verification reports zero errors and zero warnings.

The numbered [archive](tests/release-correction/e3-1.0.5.zip) was installed over the existing supported E3_TARGET deployment and reapplied successfully. Native readiness, expected Home heading and real APEX session initialization passed after both operations. Before/after snapshots of the existing history/configuration/component-state fields compared equal. Raw business rows and private connection material were removed from shared evidence; the [integration receipt](tests/release-correction/integration.json) binds the exact archive hash, source commit, corrected controller and bundle. This was local native execution, not a GitHub Actions run.

A temporary qualification proxy supplied private native target connections under the OS temporary directory without reading/changing the retained target password. The proxy grant/user and temporary connection files were removed after the checks. The target schema/workspace/application remain the existing supported E3_TARGET / 810203; no retained data reset was performed.

Deleting one included SQL changeset from a qualification checkout produced one native verification error. The [negative log](tests/release-correction/missing-changeset.log) and shared diagnostic assertion identify the exact numbered path. The file was restored after the check; deployment was not called by the negative case. Smoke checks accept matching frozen metadata and reject unfrozen, wrong-version, unsafe-version, missing-distribution and dirty inputs.

## Inherited fresh-install restriction

A disposable-schema installation attempt failed at the inherited seed-data guard with ORA-20860: only E3_TARGET is permitted. The [failure log](tests/release-correction/fresh-install.log) is retained; the disposable schema/workspace was removed. This was not a successful fresh installation and is not reported as one. The native-release fix does not loosen the historical seed guard or rewrite a historical changeset. PBI-054/038 retain independent/fresh-environment delivery, now explicitly recorded in the final gap reassessment. Upgrade/repeat validation above uses the actual supported target.

## Presentation and model

The supplied model.drawio is preserved as the editable source. Its general lifecycle page is included as editable PowerPoint shapes, with enlarged release/deployment explanations. The deck updates native release ordering, evidence limits and the missed gap. The current slide map is in the walkthrough; validation/render evidence remains in the presentation build directory. Historical screenshots retain their attribution and are not presented as new GitHub operations.

## Completion boundary

The native release omission is implemented and qualified locally for the supported upgrade/repeat path. Source, tests, seed bundle, operating guidance and gap assessment are corrected. The sprint remains reopened pending Product Owner handover/reclosure; prior closure is historical. No new GitHub execution, remote seed publication, clean-host installation or production readiness is claimed.
