# E.13 setup

## Contract

Product Owner explicitly authorized activation, YOLO execution, local commits and sprint-specific GitHub work. E.13 activated from Planned; no previous E.13 implementation or evidence exists. Unrelated .codex-cli changes are preserved. [PLAN](../../PLAN.md#sprint-e13---validate-the-breaking-foundation-transition-and-recovery) owns scope and lifecycle; [BACKLOG](../../BACKLOG.md) owns acceptance. Apply [local policy](../../RUP_patch.md), including P8/P9. No time limit overrides completion requirements.

## Analysis

Actors: legacy Hello/World consumers, new template consumer, migration operator and recovery operator. Journey: establish retained history/settings, install transactional bridge, challenge the gap between paired writes, verify mixed reads, migrate Hello while World remains legacy, roll back after new writes, migrate both and retire only after no legacy callers remain. The prepared apex-cicd Podman connection is live; the default connection is stale. Use isolated schema and real Oracle sessions, preserving retained application targets. No SQLcl PROJECT export/stage/package/deploy is selected; this is an explicit SQL architectural experiment following E.12, not production deployment qualification.

## Actor-goal journey and system boundary

Primary actor A-03 Delivery operator (the [SRS actor model](../../docs/srs.md#actors)) wants to move a consumer to the breaking contract without losing shared data and retain a supported recovery path. Hello and World are internal product components; they serve as separate contract clients outside the bridge under test, not additional human roles. Oracle/Podman are supporting execution infrastructure. The fixture boundary is the PL/SQL bridge and its owned tables; the production application boundary is unchanged.

Trigger/precondition: the prepared Oracle environment is available and the operator selects this isolated experiment following E.12's compatible/catch-up evidence. Main flow: establish history/configuration; install both contract paths; challenge failure between writes; migrate one route and observe both traffic streams; return to legacy after new writes; migrate both and retire old writes. Alternative flow: any SQL/timeout/assertion failure rejects success and retains the unique schema/logs for diagnosis. A caught partial-write exception and interrupted session must leave no partial row. Postcondition/success: every accepted finite-stream greeting is preserved and visible, original history/settings survive, pre-retirement return succeeds, premature retirement rejects and new calls succeed after valid retirement. The walkthrough exposes these intermediate outcomes to the operator. This refines UC-1/UC-3/UC-5 as a bounded experiment; it does not replace their broader product acceptance requirements.
