# E.13 design

Status: Accepted (YOLO self-approval)

## Decisions

Retain one canonical history table and a structured companion table. Both legacy and new APIs use one transactional writer with a savepoint; a failure between corresponding writes rolls back the entire call even if the caller catches the exception and commits. Legacy arbitrary text maps to a literal template. New contract requires a known template and a structured name parameter. Both read the canonical history; new fields preserve the rendered message needed by legacy operation. Consumer registry gates retirement; retirement disables legacy writes only after both consumers use version 2. Return to legacy before retirement changes consumer routing, preserving new writes. These mechanisms are implementation choices, not extra acceptance requirements.

### Testing Strategy

Test and full regression: smoke, unit, integration, as [PLAN](../../PLAN.md) requires. Smoke parses driver; unit checks rejection of inconsistent paired representations (synthetic only). Integration uses real Oracle sessions for injection, caught-exception commit, concurrent mixed API traffic, retained history/configuration, consumer migration, return to legacy and guarded retirement. A finite traffic stream proves only its observed sample. Use isolated E13 schema; never reset retained application schemas.

## Test Specification

SM-1: parse bridge driver. UT-1: reject inconsistent representations. IT-1: establish baseline; compile bridge; inject failure after first insert, catch and commit, assert neither row remains; issue concurrent legacy World and migrated Hello reads/writes; assert exact counts and shared visibility; return Hello to legacy after new writes; reject early retirement; migrate World, retire, reject legacy and accept new writes. PBI-082 maps to failure/visibility/return checks; PBI-049 maps to mixed traffic, preserved data and gated retirement. Full regression remains separate. See [checklist](sprint_E.13_remaining_work.md).

## Binding, data ownership and bounded availability

The numbered caller routes identify the legacy 1.x arbitrary-text contract and breaking 2.0 template contract in this isolated fixture. They are laboratory contract bindings, not published package versions or deployment receipts. No different artifact is published as the E.12 1.1.0 extension. E.14 retains responsibility for actual in-place deployment/version binding and component windows. Shared history is canonical; companion template/name details are new-contract metadata. All supported writes in this experiment pass the transactional bridge; direct SQL queries inspect history, but uncontrolled direct DML is not a supported writer. The fixture has exactly two callers and no scheduled jobs or external sessions. Retirement is permitted after both controlled routes move; production inventory/fencing is unqualified.

The source baseline is created without concurrent traffic; E.12 separately owns and verified initial migration/catch-up. No snapshot-to-bridge gap with concurrent initial writers is claimed here. During mixed operation both sessions issue separately committed operations with 0.05-second pacing, no allowed failed supported call and a 180-second subprocess deadline for each SQL operation/complete stream. This selected bound fails a hung experiment; it is not a production latency objective. The measured overlapping spans and largest completion gaps are retained in [availability observations](tests/availability-observations.json).

## Test sensitivity and procedure record

The new tests were specified before implementation, but no failing test skeleton was recorded before the first implementation. To verify the important assertion actually detects the defect, an in-memory test-only mutation omitted the savepoint rollback without changing the repository source. Real Oracle then failed with ORA-20121 partial history, as retained in [the mutation log](tests/atomicity-mutation-red.log). This is a later sensitivity check, not a retroactive claim of test-first execution. The current implementation's independent green runs retain their own schema/source receipts. No acceptance criterion is waived by this process deviation.
