# E.16 requirement and evidence checklist

The original closure/evidence below describes the Python-controller baseline. The authorized [named-Actions correction](sprint_E.16_actions_refactor.md) owns current refactor acceptance and fresh verification; prior completion does not prove the changed workflow.

Authoritative acceptance: [PBI-084](../../BACKLOG.md#pbi-084-validate-provenance-through-native-oracle-release-delivery), [E.16 plan](../../PLAN.md#sprint-e16---validate-provenance-through-native-oracle-release-delivery). [Design](sprint_E.16_design.md) owns implementation choices.

- [x] R1: Native SQLcl PROJECT installation, upgrade and safe repeat; preserve existing data. Source: PBI-084 Test and PLAN E.16.
- [x] R2: Verifiable reviewed-source, preparation, artifact and observed-target provenance. Source: PBI-084 description/Test.
- [x] R3: Reject substituted artifacts and mismatched evidence before mutation. Source: PBI-084 Test.
- [x] R4: Reject incompatible tools before mutation for every processed Git state; record actual build. Source: PBI-084 and AGENTS SQLcl compatibility/NFR-5.
- [x] R5: New smoke/unit/integration and full regression gates. Source: PLAN E.16 Test/Regression and manager Phase 4.
- [x] R6: Documentation audit, live demonstration, presentation pair, traceability, local commits and recorded closure. Source: local P8/P9, manager Phase 5 and user instruction.

The pinned hosted image, bounded table fixture, Python controller and disposable users are implementation choices, not additional acceptance requirements.

R1–R4 evidence: [current source review](sprint_E.16_source_review.md#verified-current-revision), [native artifacts](tests/native-current/) and [A3 integration](test_run_A3_integration_20261126.log). R5 evidence: [all six final gate results](sprint_E.16_tests.md#final-gate-results--pbi-084), including the full wrapper’s zero exit, source stability and cleanup. R6 evidence: [handover](sprint_E.16_handover.md), [presentation walkthrough](sprint_E.16_increment_demo.md), [documentation audit](sprint_E.16_documentation_audit.md), [documentation summary](sprint_E.16_documentation.md), traceability links and [closure](sprint_E.16_closure.md).

Every assigned acceptance requirement is verified. No remaining E.16 requirement or external blocker is deferred. Production and later-sprint boundaries are preserved in the closure record.

Current corrected implementation: [all R1–R8 requirements](sprint_E.16_actions_refactor.md#final-verification-and-acceptance) pass on fresh named-Actions/native and full regression evidence. The original evidence above remains baseline history, not a substitute for the correction runs.
