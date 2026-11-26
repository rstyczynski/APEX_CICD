# E.17 Product Owner acceptance amendment

On 2026-11-26 the Product Owner explicitly instructed: “I accept the Codex-driven automated reproduction for E.17. Amend the acceptance condition accordingly and continue the sprint.”

This decision replaces the separate external-operator condition for [PBI-085](../../BACKLOG.md#pbi-085-reproduce-complete-native-delivery-on-a-clean-host) and [PLAN E.17](../../PLAN.md#sprint-e17---reproduce-complete-native-delivery-on-a-clean-host). Codex-driven automated reproduction on an independent clean host is acceptable. No additional GitHub account or external participant is required for E.17, and the internal runner remains an execution principal rather than an external actor.

All other acceptance conditions remain applicable: declared prerequisites, newly supplied private inputs, actual Database/APEX/ORDS provisioning and application access, native install/upgrade/repeat, preserved test data, source/tool identity and cleanup. Existing observed results remain evidence subject to the normal source and result checks. This decision does not waive remaining regression, demonstration, presentation, audit or closure gates, or assert sprint completion.

The broader SRS UC-6 and NFR-4 independent-operator requirements remain in force outside this bounded sprint amendment. The [requirement ledger](sprint_E.17_checklist.md) owns execution tracking; [source review](sprint_E.17_source_review.md) owns observed behavior and limits. Earlier attribution discussions are historical and superseded only for E.17 acceptance.
