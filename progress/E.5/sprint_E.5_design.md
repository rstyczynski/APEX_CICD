# E.5 — Design and test specification

Status: Accepted

Accepted autonomously under the Product Owner's explicit YOLO instruction. [Setup](sprint_E.5_setup.md) owns scope and actor analysis. [SRS](../../docs/srs.md) owns requirements; [architecture](../../docs/architecture.md) owns the native delivery boundary.

## PBI-061 — One entry-creation operation

HELLO_ENTRY_API.validation_error returns the existing required-field message for null/space-only text and an explicit maximum-length message beyond 100 characters. create_entry validates text and active state before DML, trims text, returns the generated identifier and never commits. Existing table constraints/triggers stay enabled. No APEX globals enter the API. A page adapter maps the validation error to P101_ENTRY_TEXT and calls the operation for CREATE; native SAVE/DELETE remain unchanged. No editing of generated native source without toolchain qualification.

## PBI-040 — Regression and coverage

Install a pinned utPLSQL release only in an explicitly selected test database. Test successful trimming, blank rejection, 100/101-character boundaries and invalid active state. Archive native test output and coverage XML for HELLO_ENTRY_API only, including executable and covered-line counts. Measure the initial trimming, blank and maximum-valid-length subset; then add the missing overlength and invalid-active cases and measure the full suite. Keep the complete XML reports, including condition-line instrumentation differences. Temporarily change the trim expression in the test fixture, prove the trimming test fails, then restore and rerun. Never promote the mutant.

## PBI-062 — Fixture boundaries

Ordinary cases use utPLSQL automatic rollback and exact test-owned values. Compare unrelated data before/after. Reorder named test paths and repeat them. Keep deterministic text and explicitly set session language/date language/time zone; no wall-clock-dependent API behavior is introduced. Separately create an E5_TEST_DDL table, prove rollback leaves it present, explicitly drop it and confirm removal. A failed test must not drop unrelated objects. Test packages and structural fixture scripts reside under tests/, outside release inputs.

### Testing Strategy

Smoke validates source boundaries and required artifacts. Unit executes real utPLSQL tests; integration checks fixture isolation, mutation detection, coverage improvement and live page mapping/outcomes. Smoke regression uses the existing project manifest. Required runtime or browser failures remain failures, even in YOLO. Test-owned DDL cleanup is explicit and bounded.

## Test Specification

SM-1 checks API transaction ownership and test/release separation. UT-1 covers trimming and valid entry creation; UT-2 covers blank and length rejection without writes; UT-3 covers active-state rejection. IT-1 compares repeated/reordered fixture runs and unrelated rows. IT-2 demonstrates structural cleanup beyond rollback. IT-3 archives regression detection and measured coverage improvement. IT-4 compares page outcomes and manually inspects the item mapping. Each identifier maps respectively to PBI-061 (SM-1, UT-1/2/3, IT-4), PBI-040 (UT-1/2/3, IT-3) and PBI-062 (IT-1/2, SM-1).
