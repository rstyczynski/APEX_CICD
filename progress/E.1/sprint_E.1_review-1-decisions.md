# E.1 — Review 1 selected corrections

- **Round:** E.1 review 1, decisions.
- **Revision:** reviewed `0f5ce709685508e56e255bc7b0331c89daec0917`; implementation follows later commits, so this is not the current implementation baseline.
- **Reviewer/owner:** external expert report supplied by the Product Owner; Codex engineering implements selected corrections.
- **Scope:** original source review plus focused native/source checks listed in the response; full independent fresh-stack replay remains pending.
- **Inputs:** [review](sprint_E.1_review-1.md), [response](sprint_E.1_review-1-response.md), [feedback](sprint_E.1_review-1-feedback.md).

Original headings H1–H3, M1–M6 and L1–L4 map to stable IDs by prefixing `R1-`. Each selected correction is owned by Codex engineering in E.1; Product Owner review controls scope/acceptance. Current statuses retain each decision's closing condition rather than equating a code commit with full acceptance.

| Finding | Decision/status | Closing condition or deferral boundary |
|---|---|---|
| R1-H1 | selected — BUG-2 | Clean-checkout input reconstruction plus independent A–H replay; the input defect is fixed at 7976a9e, full replay pending. |
| R1-H2 | selected — BUG-4 | Invalid config fails before SQL and native scoped provisioning works; validated at 7976a9e. Production privilege redesign deferred until shared deployment. |
| R1-H3 | verified@e7ee3de | Native committed-DDL failure, blocked runtime, changed-observation rejection, forward repair, unchanged 21-row field snapshot and repeat passed. |
| R1-M1 | verified@7976a9e | Native ORA-20224 returns nonzero with EXIT FAILURE; all affected wrappers corrected. |
| R1-M2 | verified@0cc6c68 | Stable IDs/private saved report and corrected archive qualified fresh/from initial; new patch recipe is versioned at e7ee3de. |
| R1-M3 | deferred | Broader mapping consolidation waits for Construction; validation/endpoint use is corrected in BUG-4. |
| R1-M4 | deferred | General release/version profiles wait for another selected supported release/toolchain. |
| R1-M5 | verified@7976a9e | Dirty runner/manifests/Python/shell tests reject; full tests tree is checked/packaged. Shared-runner attestation deferred until hosted automation. |
| R1-M6 | deferred | Broad diagnostic-parser redesign waits for tool invocation changes; existing nonzero/marker guards remain. |
| R1-L1 | verified@7976a9e | README explicitly identifies macOS Apple Silicon for infrastructure provisioning. |
| R1-L2 | deferred | Minimal gateway feature/privilege profile before shared or remotely exposed hosting. |
| R1-L3 | deferred | Hosted CI after the independently reproducible local flow is proved. |
| R1-L4 | deferred | Product Owner must select licensing/PDF distribution treatment before claiming freely licensed reuse; public visibility is not license clearance. |

The Product Owner selected implementation of the required Elaboration fixes on 2026-10-18, with special emphasis on fresh-checkout reproduction and one bug entry per fix. See [review](sprint_E.1_review-1.md), [response](sprint_E.1_review-1-response.md), [feedback](sprint_E.1_review-1-feedback.md) and the [bug register](sprint_E.1_bugs.md).

BUG-2 through BUG-7 cover release-input acquisition/reconstruction, reliable failure status, scoped provisioning validation, complete test provenance, stable replacement identities and the bounded failed-additive-deployment/repair proof. These fold into existing PBI-011 child scope and PBI-012 validation; no other sprint is changed or selected.

Use exact reviewed historical release reconstruction to make the current demonstration accessible without remote release uploads. Preserve historical artifacts/evidence; a changed importer/controller requires a new reviewed archive and independent checks. Input reconstruction does not attest a new candidate test. Keep scripts small and operator-visible, and document commands/results alongside each step.

Keep Linux hosting, hosted CI, generalized version resolution, independent signing/attestation and production secret/privilege architecture deferred. SYS remains a lab-owned infrastructure/project bootstrap boundary with strict input validation; ordinary deployments remain under target credentials. Saved-report preservation receives a bounded APEX identity experiment, not a broad APEX feature expansion. No license or third-party redistribution decision is made here.

The [design](sprint_E.1_design.md) and [test profile](../../docs/test-profile.md) retain authority over required proofs. No fix is complete merely because code exists: native evidence and focused negative/regression tests determine each bug's status. E.1 remains open.
