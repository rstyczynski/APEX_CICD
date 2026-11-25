# E.5 — Contract and analysis

## Contract

The Product Owner explicitly requested E.5 implementation in YOLO mode and then directed “go” after the activation prerequisite was explained. That instruction authorizes recording activation on their behalf. [PLAN](../../PLAN.md) owns the active assignment; [the board](../../PROGRESS_BOARD.md) tracks PBI-061, PBI-040 and PBI-062. Test: smoke, unit, integration. Regression: smoke. No remote push is authorized. Existing working changes are preserved. Token usage per phase is unavailable.

The manager and its contractor, analyst, designer, constructor, test and documentor responsibilities apply serially with the local patch. This is a bounded Elaboration experiment, not Construction readiness. [The design](sprint_E.5_design.md) owns implementation and verification. [The validation programme](../../docs/validation-programme.md) owns the wider sequence; the old Foundation proposal in this directory is historical.

## Analysis

The developer extracts Hello entry input validation into a package; an APEX user receives feedback on P101_ENTRY_TEXT; a backend caller receives rejection before insertion. The existing page 101 has a required text item, maximum length 100 and BOTH trimming, with native form DML. HELLO_ENTRIES additionally enforces not-null, trimmed length and active Y/N. Existing readiness and default/deactivation triggers remain authoritative. The selected boundary is creating one Hello entry; editing and deleting retain their existing behavior.

PBI-061 requires real before/after page observations and manual mapping inspection, in addition to API checks. PBI-040 requires actual utPLSQL execution, a deliberately broken implementation detected by a test, and measured coverage before/after adding a missing case. PBI-062 requires repeated and reordered runs, explicit locale/time inputs, preserved unrelated rows and cleanup of a structural effect that rollback cannot undo. Static source checks cannot substitute for these runtime results.

## YOLO decisions

Use one package and the existing Hello constraints rather than generalizing the application. Keep all tests outside release source. Use only explicit native connections or OS database authentication; do not expand retained scratch credential exceptions. The prepared VM was stopped at entry; runtime startup is a prerequisite, not evidence of a successful test.
