# E.13 requirement-to-evidence checklist

## Authoritative scope

[PBI-082](../../BACKLOG.md#pbi-082-validate-dual-write-failure-and-mixed-version-data-visibility) and [PBI-049](../../BACKLOG.md#pbi-049-prove-an-available-breaking-foundation-transition) own mandatory acceptance. [PLAN](../../PLAN.md#sprint-e13---validate-the-breaking-foundation-transition-and-recovery) owns assignment and six test/regression levels. The [validation programme](../../docs/validation-programme.md#e13--validate-the-breaking-foundation-transition-and-recovery) requires bridge validation before dependent migration. [Local policy](../../RUP_patch.md) owns P8 audit/commits and P9 demonstration/presentation; the [canonical sprint procedure](../../RUPStrikesBack/.claude/commands/sprint.md) owns closure after gates and wrap-up. The [original combined scenario](../E.5/sprint_E.5_proposedchanges.md) remains design input; E.12 owns compatible extension/catch-up and E.14 owns separate component windows. No criterion is weakened or newly assigned here.

## PBI-082 — verified

Partial-write failure and recovery: [caught error and commit](tests/run_94961/failure-recovery.log) proves neither corresponding row remains after the injected inter-write error. [Session interruption](tests/run_94961/interruption.log) records nonzero child termination and [independent verification](tests/run_94961/interruption-check.log) proves rollback. This is real Oracle session-exit recovery, not a crash-recovery claim.

Old/new visibility and return limits: [assertions](tests/run_94961/assertions.log) check rendered/structured consistency, shared messages, retained original greeting/configuration and legacy operation after new writes. [Direct live inspection](tests/run_94961/live-inspection.log) shows both representations contain 165 rows, original ID 0 is unchanged and both final routes use API 2. Return is supported before retirement because rendered text is retained. No post-retirement reactivation is claimed.

## PBI-049 — verified bounded Elaboration outcome

The breaking public entry point requires a greeting template and structured name collection; the legacy arbitrary-text entry point remains operational. [Setup SQL](tests/run_94961/setup.log.sql) defines these contracts. [Assertions](tests/run_94961/assertions.log.sql) reject an unknown template and verify specific failure outcomes.

Independent adoption and simultaneous reads/writes: Hello uses the new route while World remains legacy. [Hello](tests/run_94961/hello.log) and [World](tests/run_94961/world.log) each commit/read back 80 calls. The complete final comparison checks shared representations. [Timing observations](tests/availability-observations.json) confirm overlapping streams. This is a finite real Oracle sample, not universal availability or an independent-human study.

Preservation, interruption and legacy return: the failure and return assertions above preserve original history/settings and make new-contract writes readable on the old path. Both legacy consumers succeed again before retirement. Retirement rejects while World remains legacy; after both migrate it disables old writes while both new consumers succeed. [Live handover](sprint_E.13_handover.md) exposes actual outcomes and limitations.

## Mandatory workflow outcomes

All six gates pass with no retries: new 1/1/1, full 12/13/22; [test report](sprint_E.13_tests.md) and [gate receipt](tests/final-gates.json) distinguish each proof. The full run used unchanged source and real Oracle/native/HTTP behavior where selected; historical hosted-evidence readers remain explicitly identified.

P8 documentation reconciliation and P9 actual developer demonstration, complete explained walkthrough/manual, canonical presentation pair, rendered visual inspection and package validation are recorded in [audit](sprint_E.13_documentation_audit.md), [handover](sprint_E.13_handover.md) and [presentation](sprint_E.13_increment_demo.pptx). Technical review is accepted through explicit YOLO delegation; Product Owner reactions are not invented. Local completion commit `f5bc924` exists; [recorded closure](sprint_E.13_closure.md) completes lifecycle finalization.

## Implementation choices and unverified product behavior

[Design](sprint_E.13_design.md) owns the common savepoint, shared rendered history plus structured companion, controlled caller registry and 180-second operation deadline. Those choices do not add acceptance criteria. The numbered bindings identify laboratory contract versions; no production release or E.12 artifact version is republished. One operator uses separate real sessions. Production caller/session/job fencing, APEX UI rollout, crash recovery, native release deployment/version binding and E.14 component windows remain unqualified; they are not claimed as E.13 outcomes. The recorded test-first chronology deviation is exposed in design, with a real defect-sensitivity check rather than a fabricated earlier red run. No failed acceptance criterion or external blocker remains.

## Corrected publication destination

The Product Owner clarified that [APEX_CICD_E.13](https://github.com/rstyczynski/APEX_CICD_E.13) is reserved for sprint experiments. Actual project progress belongs in [APEX_CICD](https://github.com/rstyczynski/APEX_CICD), the existing origin. The [publication boundary record](sprint_E.13_publication_boundary.md) preserves the rejected attempt and the superseding direction. Publication now targets origin/main; no experiment-repository push or remote rewrite is required.
