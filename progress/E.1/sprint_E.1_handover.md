# E.1 — Product Owner handover

Prepared on 2026-10-18 for review of the APEX CI/CD delivery pipeline prototype. Start with the [presentation walkthrough](sprint_E.1_increment_demo.md) and its [PowerPoint companion](sprint_E.1_increment_demo.pptx). The [A–I guide](cicd-walkthrough.md) remains the main operating journey, and the [operator manual](user_manual.md) contains the detailed procedures.


The [first external review](sprint_E.1_review-1.md) and [engineering response](sprint_E.1_review-1-response.md) add concrete reproducibility, privileged-input, migration-recovery, exit-status and provenance findings. In particular, the demonstrated host rebuild retains archives; the initial release-input acquisition defect is addressed by [exact archive reconstruction](cicd-walkthrough.md#prepare-reviewed-release-inputs), and the [independent clean-checkout A–I rehearsal](tests/clean_checkout_20261018.txt) now passes from newly provisioned infrastructure. Six selected corrections are registered individually in the [bug register](sprint_E.1_bugs.md). This API-driven rehearsal supplements the earlier assisted walkthrough; wider sprint gates remain open.

[Expert feedback on the response](sprint_E.1_review-1-feedback.md) is retained with the same review round. Selection of corrections remains a separate Product Owner decision under the [external-review convention](../../RUPStrikesBack.patch/RUP_patch.md#p10-use-proportionate-external-review-rounds).

## The important outcomes

1. **A complete local application:** Foundation-first assembly grows into Hello/World with configurable entries and immutable greeting history. A/B/C are private logical areas in one host and one shared source repository.
2. **Traceable release delivery:** the development team supplies an archive from reviewed Git source. D validates it in integration_test; E promotes the identical archive to UAT. Live C is not the promotion source.
3. **A compatible patch:** F advances Hello to 1.0.1 while Foundation/World remain 1.0.0. It tests both fresh and baseline-upgrade starts, then upgrades UAT with the same patch bytes. The handover preservation check confirms all fields of **21 earlier history rows**, old entries and complete configuration unchanged.
4. **A rejected breaking proposal:** G rejects Foundation 2.0.0 because Hello and World still require Foundation 1.0.0, before maintenance, migration or import. Target/control comparisons verify no deployment side effects.
5. **A rejected real page change:** H detects the Product Owner's Page Designer change even though component versions stay the same. `drift --show` exposes published/live source differences and preserves the live edit for a keep/undo decision. The scripted fixture remains available as a separate repeatable detection test.

These outcomes directly support the [accepted vision](../../README.md), selected [E.1 design](sprint_E.1_design.md) and [SRS](../../docs/srs.md) delivery/protection goals. The [assessment](sprint_E.1_assessment.md) states the incomplete acceptance scope and proposed follow-up.

## APEX automation interfaces

Application definitions use native SQLcl `apex export` to produce split SQL source, and native exported `install.sql` for deployment after `APEX_APPLICATION_INSTALL` maps the target. `APEX_EXPORT.GET_APPLICATION` supplies the live APEX metadata fingerprint used by the drift guard. Schema changes use separate Liquibase migrations. App Builder is the authoring UI; ORDS serves HTTP. APEX Working Copies and Team Development are not used for release integration or promotion. See slide 7 and the [architecture interfaces](../../docs/architecture.md) for the boundary.

## Git cooperation and automation boundary

Slides 8–11 show the actual shared repository layout, proposed task-branch cooperation, safe review of text-based split SQL exports and future CI automation of existing delivery gates. The [repository draft](repo_layout.md#merging-apex-export-files) owns detailed merge/pipeline guidance. Current A–C stages replay accepted snapshots; parallel authoring/merging and hosted PR/CI execution remain future work.

## Live journey already inspected

The assisted Product Owner walkthrough produced PASS results for D, E, F and G; retained stage markers also show A/B/C completion. The Product Owner exercised VERIFIER/LAB_USER runtime interactions and reported successful manual drift rejection. Subsequent native read-only checks reproduce that rejection and show the current Home Title and region Name changes without restoring them.

The live interaction exposed two operator issues: missing required VERIFIER data stopped publication, and later test-example creation incorrectly relied on an unset World default. The bounded verification/example continuations and explicit entry selections corrected those issues while preserving publication guards and saved history. These fixes do not prove generic failed-migration repair.

This package consolidates those observed results. Its preparation did not destroy/rebuild the lab, reinstall the patch, execute synthetic drift over the current manual edit, or undo the edit.

## Current application and data state

- **A / E1_DEV_A / 810001:** incomplete Foundation checkpoint, intentionally unavailable.
- **B / E1_DEV_B / 810002:** Foundation/Hello checkpoint, intentionally unavailable.
- **C / E1_DEV_C / 810003:** now Hello 1.0.1 / Foundation and World 1.0.0 after the BUG-6 identity experiment; the earlier A–C walkthrough evidence describes its initial 1.0.0 checkpoint.
- **integration_test / E1_INTEGRATION / 810004:** the patch integration area used by F; disposable for declared validation starts.
- **user_acceptance_test / E1_UAT / 810005:** retained Hello 1.0.1 release with the manually changed Home Title/region Name still present at handover preparation. Ordinary application/history use remains available; another deployment must stop on drift.

Use [UAT](http://127.0.0.1:8080/ords/f?p=810005:1) as LAB_USER. Retrieve that one password with `python3 scripts/cicd-password.py LAB_USER`; no password values are included in the handover.

## Review and restoration decision

Run from the repository root:

```bash
bash scripts/cicd-protection-check.sh drift --show
```

The current report shows:

1. Page Title: **APEX Delivery Laboratory** became **Manual drift demonstration**.
2. Region Name: **APEX Delivery Laboratory** became **APEX Delivery XX Laboratory**.
3. Additional SQL/export differences remain in review.diff/raw.diff for inspection; no automatic comparison rule silently accepts them.

Choose whether to restore the published properties in Page Designer or retain the export for reviewed Git reconciliation and a new release. [H.1](cicd-walkthrough.md#h1-change-a-page-in-app-builder) gives the exact steps. Restoration remains pending; its acceptance signal is **NO DRIFT** against the original receipt, not an updated version label or changed baseline.

## Release identities

The pointers identify retained immutable archives; they are not instructions to rebuild:

- Initial 1.0.0: SHA-256 `d99fe83ec3d149739a12ec0cf2f01081ae027d1ec015e16d5a971ff3c602ab45`, source `08a5cf27e8a31ff7b77b6fd694f673847726eda1`.
- Patch 1.0.1: SHA-256 `4ba3abb8709f256c7a47e3e9294d3e7303f742145a95cb58d808ca6c6bcf7200`, source `ee8f1af8e35f81bb3b75051243df2ab9c6e4c0e5`.

Native initial receipts remain historical evidence after upgrade. Old pre-rename archives/receipts remain historical as documented in the [environment rename evidence](tests/environment_rename_20261018.txt); they are not evidence for changed inputs. See the [repository draft](repo_layout.md) for source/artifact roles and the [architecture](../../docs/architecture.md) for design responsibilities.

## Completion boundary and recommendation

The [official board](../../PROGRESS_BOARD.md) still records E.1 as under_construction and PBI-011 through PBI-016 as unfinished parent outcomes. The full [plan](../../PLAN.md) remains Progress. In particular, real concurrent reservations/integration, full request/verifier fencing, broader schema drift and unsupported repair states remain open. The bounded integration-only failed additive deployment/forward repair now passes; see [native evidence](tests/recovery_proof_20261018.txt).

Recommend a focused Elaboration follow-up, using the existing child definitions, before full Lifecycle Architecture acceptance. The [assessment](sprint_E.1_assessment.md) supplies each assigned item's exact status, demonstrated subset, remaining criterion and a conditional Construction sequence. No new sprint is scheduled, no backlog item is marked complete, and no push is authorized by preparing this package.

## Materials and evidence

- [Presentation walkthrough](sprint_E.1_increment_demo.md): complete guided review and optional fresh replay, with slide references.
- [Presentation](sprint_E.1_increment_demo.pptx): 29 slides, editable draw.io-derived diagrams and editable version comparison.
- [Completion assessment](sprint_E.1_assessment.md): parent/child outcomes, open risks, milestone recommendation and proposed next work.
- [Documentation summary](sprint_E.1_documentation.md): reconciliation and presentation/source checks.
- [Handover checks](tests/handover_checks_20261018.txt): exact recent checks, observed results and limits.
- [Current drift output](tests/handover_live_drift_20261018.txt): read-only rejection/review output.
- [Detailed test record](sprint_E.1_tests.md): earlier and current evidence with its applicability.
- [Original draw.io model](model.drawio): source diagrams. [Frozen figure data](presentation/model-source.json) records the source labels/geometry and SHA-256 used by the [presentation builder](presentation/build.mjs); the original working model is unchanged.

## Product Owner review status

The package is prepared for your review. The earlier stage PASS observations remain recorded as demonstrated outcomes. Handover acceptance, the manual restoration choice and the boundary for sprint conclusion are not decided by creating these documents.
