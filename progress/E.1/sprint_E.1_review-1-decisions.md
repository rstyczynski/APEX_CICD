# E.1 — Review 1 selected corrections

The Product Owner selected implementation of the required Elaboration fixes on 2026-10-18, with special emphasis on fresh-checkout reproduction and one bug entry per fix. See [review](sprint_E.1_review-1.md), [response](sprint_E.1_review-1-response.md), [feedback](sprint_E.1_review-1-feedback.md) and the [bug register](sprint_E.1_bugs.md).

BUG-2 through BUG-7 cover release-input acquisition/reconstruction, reliable failure status, scoped provisioning validation, complete test provenance, stable replacement identities and the bounded failed-additive-deployment/repair proof. These fold into existing PBI-011 child scope and PBI-012 validation; no other sprint is changed or selected.

Use exact reviewed historical release reconstruction to make the current demonstration accessible without remote release uploads. Preserve historical artifacts/evidence; a changed importer/controller requires a new reviewed archive and independent checks. Input reconstruction does not attest a new candidate test. Keep scripts small and operator-visible, and document commands/results alongside each step.

Keep Linux hosting, hosted CI, generalized version resolution, independent signing/attestation and production secret/privilege architecture deferred. SYS remains a lab-owned infrastructure/project bootstrap boundary with strict input validation; ordinary deployments remain under target credentials. Saved-report preservation receives a bounded APEX identity experiment, not a broad APEX feature expansion. No license or third-party redistribution decision is made here.

The [design](sprint_E.1_design.md) and [test profile](../../docs/test-profile.md) retain authority over required proofs. No fix is complete merely because code exists: native evidence and focused negative/regression tests determine each bug's status. E.1 remains open.
