# Proposed production follow-up sequence

[BACKLOG](../../BACKLOG.md) owns each item's definition, priority and literal status. This is PBI-080's proposed dependency grouping for Product Owner consideration, not a backlog reorder, new sprint assignment or new requirement. [Assessment](architecture_assessment.md) explains the evidence and limits behind it. Existing Proposed items below remain Proposed; a related experiment does not automatically complete their broader criteria.

## 1. Resolve shared-service admission and operational authority

[PBI-018 — Prove atomic task reservations under contention](../../BACKLOG.md#pbi-018-prove-atomic-task-reservations-under-contention). Current status: Proposed.

[PBI-021 — Complete release admission and promotion negative coverage](../../BACKLOG.md#pbi-021-complete-release-admission-and-promotion-negative-coverage). Current status: Proposed.

[PBI-022 — Prove deployment ownership and maintenance fencing](../../BACKLOG.md#pbi-022-prove-deployment-ownership-and-maintenance-fencing). Current status: Proposed.

[PBI-023 — Detect schema drift and reconcile unauthorized changes](../../BACKLOG.md#pbi-023-detect-schema-drift-and-reconcile-unauthorized-changes). Current status: Proposed.

[PBI-024 — Validate recovery beyond the selected additive failure](../../BACKLOG.md#pbi-024-validate-recovery-beyond-the-selected-additive-failure). Current status: Proposed.

[PBI-025 — Restrict privileges and protect deployment credentials](../../BACKLOG.md#pbi-025-restrict-privileges-and-protect-deployment-credentials). Current status: Proposed.

[PBI-026 — Minimize gateway exposure for shared hosting](../../BACKLOG.md#pbi-026-minimize-gateway-exposure-for-shared-hosting). Current status: Proposed.

[PBI-027 — Unify delivery environment configuration](../../BACKLOG.md#pbi-027-unify-delivery-environment-configuration). Current status: Proposed.

[PBI-028 — Extend supported release and toolchain profiles](../../BACKLOG.md#pbi-028-extend-supported-release-and-toolchain-profiles). Current status: Proposed.

[PBI-029 — Strengthen automation failure diagnostics](../../BACKLOG.md#pbi-029-strengthen-automation-failure-diagnostics). Current status: Proposed.

[PBI-031 — Establish independent release validation provenance](../../BACKLOG.md#pbi-031-establish-independent-release-validation-provenance). Current status: Proposed.

[PBI-032 — Resolve repository licensing and reference distribution](../../BACKLOG.md#pbi-032-resolve-repository-licensing-and-reference-distribution). Current status: Proposed.

[PBI-045 — Preserve scenario protections around native Oracle delivery](../../BACKLOG.md#pbi-045-preserve-scenario-protections-around-native-oracle-delivery). Current status: Proposed.

[PBI-054 — Generate the complete local environment from a fresh checkout](../../BACKLOG.md#pbi-054-generate-the-complete-local-environment-from-a-fresh-checkout). Current status: Proposed.

[PBI-059 — Require pull requests for target-product release preparation](../../BACKLOG.md#pbi-059-require-pull-requests-for-target-product-release-preparation). Current status: Proposed.

## 2. Package the supported native delivery and quality paths

[PBI-017 — Deliver a repository and pipeline reference guide](../../BACKLOG.md#pbi-017-deliver-a-repository-and-pipeline-reference-guide). Current status: Proposed.

[PBI-019 — Prove parallel component collaboration and integration](../../BACKLOG.md#pbi-019-prove-parallel-component-collaboration-and-integration). Current status: Proposed.

[PBI-020 — Complete APEX capture and reconstruction validation](../../BACKLOG.md#pbi-020-complete-apex-capture-and-reconstruction-validation). Current status: Proposed.

[PBI-030 — Automate source validation in hosted CI](../../BACKLOG.md#pbi-030-automate-source-validation-in-hosted-ci). Current status: Proposed.

[PBI-034 — Automate application browser acceptance checks](../../BACKLOG.md#pbi-034-automate-application-browser-acceptance-checks). Current status: Proposed.

[PBI-036 — Define Oracle lifecycle use-case coverage](../../BACKLOG.md#pbi-036-define-oracle-lifecycle-use-case-coverage). Current status: Proposed.

[PBI-037 — Establish native Oracle source capture and staging](../../BACKLOG.md#pbi-037-establish-native-oracle-source-capture-and-staging). Current status: Proposed.

[PBI-038 — Deliver native Oracle release artifacts](../../BACKLOG.md#pbi-038-deliver-native-oracle-release-artifacts). Current status: Proposed.

[PBI-039 — Demonstrate native team-centric APEX collaboration](../../BACKLOG.md#pbi-039-demonstrate-native-team-centric-apex-collaboration). Current status: Proposed.

[PBI-041 — Demonstrate Oracle-recommended application quality audits](../../BACKLOG.md#pbi-041-demonstrate-oracle-recommended-application-quality-audits). Current status: Proposed.

[PBI-043 — Operate the Oracle lifecycle automation pipelines](../../BACKLOG.md#pbi-043-operate-the-oracle-lifecycle-automation-pipelines). Current status: Proposed.

## 3. Extend and compare only after the supported baseline

[PBI-033 — Validate an additional infrastructure host platform](../../BACKLOG.md#pbi-033-validate-an-additional-infrastructure-host-platform). Current status: Proposed.

[PBI-035 — Validate adoption of an existing APEX application](../../BACKLOG.md#pbi-035-validate-adoption-of-an-existing-apex-application). Current status: Proposed.

[PBI-044 — Demonstrate native mini-app component reuse](../../BACKLOG.md#pbi-044-demonstrate-native-mini-app-component-reuse). Current status: Proposed.

[PBI-046 — Compare and independently reproduce the Oracle-style laboratory](../../BACKLOG.md#pbi-046-compare-and-independently-reproduce-the-oracle-style-laboratory). Current status: Proposed.

[PBI-047 — Compare APEX-native delivery with the earlier prototype](../../BACKLOG.md#pbi-047-compare-apex-native-delivery-with-the-earlier-prototype). Current status: Proposed.

[PBI-055 — Reduce repeated pipeline toolchain setup](../../BACKLOG.md#pbi-055-reduce-repeated-pipeline-toolchain-setup). Current status: Proposed.

[PBI-056 — Provide isolated APEX environments for Git feature branches](../../BACKLOG.md#pbi-056-provide-isolated-apex-environments-for-git-feature-branches). Current status: Proposed.

## Recorded lifecycle inconsistencies

Resolved on 2026-11-26 at the Product Owner’s explicit request to reconcile the five backlog statuses with sprint closure evidence. Before this correction, BACKLOG recorded PBI-072, PBI-073, PBI-074, PBI-049 and PBI-082 as Proposed, while PLAN and the board recorded their assigned sprints and outcomes Done. The [E.10 documentation wrap-up](../E.10/sprint_E.10_documentation.md) treated Proposed as a product-definition field independent of execution acceptance. That historical interpretation left conflicting literal status records; this correction aligns the five root statuses with the accepted bounded outcomes.

PBI-072, PBI-073 and PBI-074 now record Done. The [E.10 acceptance checklist and test results](../E.10/sprint_E.10_tests.md#requirement-to-evidence-checklist) map each criterion to denied privileged access and inert adversarial input, concurrent stream isolation and stale-result refusal, and bounded retries/scoped cleanup including forced-termination recovery. The [handover and sprint closure](../E.10/sprint_E.10_handover.md#sprint-closure) record delegated YOLO acceptance; the [completion report](../E.10/sprint_E.10_completion.md) records five passing gates and implementation commit `e395d12`. These establish completion within the selected local container boundary, with hosted enforcement and host/kernel compromise outside the claim.

PBI-049 and PBI-082 now record Done. The [E.13 requirement checklist](../E.13/sprint_E.13_remaining_work.md) traces paired-write failure/rollback, mixed-version visibility, overlapping old/new traffic, preserved history/settings, pre-retirement return and guarded legacy retirement to real Oracle evidence. The [test report](../E.13/sprint_E.13_tests.md) and [gate receipt](../E.13/tests/final-gates.json) record six passing gates with zero failures or retries. The [handover](../E.13/sprint_E.13_handover.md) and [closure](../E.13/sprint_E.13_closure.md) record delegated acceptance and completion commit `f5bc924`. These establish the bounded Elaboration criteria; production caller discovery/fencing, crash recovery and universal availability remain unqualified.

The [backlog adapter](../../.agents/skills/rup-backlog/SKILL.md), [canonical backlog procedure](../../RUPStrikesBack/.claude/commands/backlog.md), [item definition](../../RUPStrikesBack/rules/generic/backlog_item_definition.md) and [local policy](../../RUP_patch.md) govern this correction. Only the five Status lines change in BACKLOG. Definitions, criteria, priority order, sprint assignments, PLAN and the board are preserved. Earlier sprint artifacts and raw evidence retain their original interpretation and dates; this record and the [assessment](architecture_assessment.md#existing-backlog-and-governance-disposition) provide the current disposition. No sprint is reopened or activated, no new item is registered, and no new runtime execution or production acceptance is claimed.

No new item was registered during E.14. The separate Product Owner Lifecycle Architecture decision remains pending; conditional Construction planning is the recommendation, not an accepted project phase transition.
