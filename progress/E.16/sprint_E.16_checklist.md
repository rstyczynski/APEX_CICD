# E.16 requirement and evidence checklist

Authoritative acceptance: [PBI-084](../../BACKLOG.md#pbi-084-validate-provenance-through-native-oracle-release-delivery), [E.16 plan](../../PLAN.md#sprint-e16---validate-provenance-through-native-oracle-release-delivery). [Design](sprint_E.16_design.md) owns implementation choices.

- [ ] R1: Native SQLcl PROJECT installation, upgrade and safe repeat; preserve existing data. Source: PBI-084 Test and PLAN E.16.
- [ ] R2: Verifiable reviewed-source, preparation, artifact and observed-target provenance. Source: PBI-084 description/Test.
- [ ] R3: Reject substituted artifacts and mismatched evidence before mutation. Source: PBI-084 Test.
- [ ] R4: Reject incompatible tools before mutation for every processed Git state; record actual build. Source: PBI-084 and AGENTS SQLcl compatibility/NFR-5.
- [ ] R5: New smoke/unit/integration and full regression gates. Source: PLAN E.16 Test/Regression and manager Phase 4.
- [ ] R6: Documentation audit, live demonstration, presentation pair, traceability, local commits and recorded closure. Source: local P8/P9, manager Phase 5 and user instruction.

The pinned hosted image, bounded table fixture, Python controller and disposable users are implementation choices, not additional acceptance requirements. All acceptance remains unverified at activation.
