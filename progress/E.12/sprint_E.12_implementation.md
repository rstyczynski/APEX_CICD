# E.12 implementation

The [accepted design](sprint_E.12_design.md) is implemented in [foundation_lab.py](../../tests/foundation_lab.py), with centralized smoke/unit/integration functions and component manifests. [Walkthrough](sprint_E.12_increment_demo.md) provides the explained complete SQL and runnable usage; [manual](user_manual.md) records prerequisites, recovery and limits. This is a retained Elaboration prototype, not production pipeline code.

## PBI-048

An isolated 1.0.0 Foundation baseline retains its PL/SQL signature, body and unchanged Hello/World consumers. The 1.1.0 extension adds nullable language storage and a new optional-language function. Both clients continue separately committed operations. Assertions verify 240 accepted writes, legacy greeting, Polish greeting, setting preservation, newer history value and valid database objects.

## PBI-081

The journal records committed insert/update/delete with a client identifier in the same transaction. The initial backfill commits, a later migration transaction rolls back, live mutations commit, then reconciliation under a shared source lock compares full sets in both directions. The source remains authoritative. This handles deletion and newer-data overwrite without assuming sequence allocation equals commit order. The selected boundary is the locked comparison, not the end of the later traffic sample.

## Decisions and limitations

YOLO self-approved isolated prototype and new optional entry point instead of replacement of the active legacy package. Separate transactions replaced long PL/SQL loops to permit DDL interleaving. Per-process schema names avoid concurrent reset collisions. SQLPlus SET directives are separate to preserve output evidence. No remote write occurred. No simulator establishes any database outcome; synthetic unit cases only validate the equality assertion. Test results and unresolved regressions belong to the [test record](sprint_E.12_tests.md).
