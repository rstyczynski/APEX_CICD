# E.14 implementation

[Design](sprint_E.14_design.md) is implemented in [foundation_windows.py](../../tests/foundation_windows.py). It extracts the existing E.13 setup SQL from its Python syntax tree, preserving the qualified fixture contract while avoiding replay of its migration journey. The same populated schema persists through both windows. Per-component maintenance flags and transactional route/journal changes are prototype choices. Session exit with rollback tests interruption, not host-crash recovery. The first direct execution failed ORA-03405 on multiple SQLPlus statements per line; normalization now separates statements. The later run passes.

Test-first deviation: specifications preceded implementation, but executable skeletons were registered after the first direct integration run. No earlier red test is fabricated. [Tests](sprint_E.14_tests.md) distinguish syntax, synthetic unit assertions and real Oracle behavior. [Assessment](architecture_assessment.md) delivers PBI-080 without claiming milestone acceptance.

## User documentation

[Walkthrough](sprint_E.14_increment_demo.md) explains the actual driver, prerequisites, invocation, outputs and recovery. [Manual](user_manual.md) owns operation limits. No settings or credentials are created in scratch. Prepared container SYS access is used only for isolated laboratory schemas. No SQLcl PROJECT processing occurs in the new driver; historical native regression must qualify its own selected Git state before source or target changes.

[Defect record](sprint_E.14_bugs.md) preserves implementation, registration and environment failures separately from the final accepted results.

## PBI-050 — component-window implementation

Implementation complete; final quality disposition is owned by the test record. The driver provides separate maintenance gates, unaffected read/write traffic, interrupted route/journal rollback and retry with preserved history and configuration. Source and current evidence are linked above.

## PBI-080 — architecture assessment implementation

The [assessment](architecture_assessment.md) and [existing follow-up inventory](production_follow_up.md) deliver the source-linked risk synthesis and proposed Construction sequence. The recommendation remains conditional, identifies untested production cases and prior lifecycle discrepancies, and leaves Lifecycle Architecture acceptance to the Product Owner.
