# E.12 design

Status: Accepted (YOLO self-approval)

## Scope and decisions

[Setup](sprint_E.12_setup.md) defines the actors and contract. Use an isolated E12_APP schema and unchanged stored Hello/World consumers with legacy positional calls and direct table access. Add nullable language storage and a separate optional-language entry point, retaining the legacy specification/body untouched to avoid invalidating active packages. A transactional change journal captures inserts, updates and tombstones. Catch-up reconciles from current source under a short shared source lock at the explicitly selected boundary, rather than assuming sequence order equals commit order. No production rollout or E.13 dual-write bridge is claimed. These mechanisms and a finite workload are implementation choices, not new acceptance requirements.

### Testing Strategy

Test and regression: smoke, unit, integration, full suite. Smoke checks source parsability. Unit checks reconciliation expectations with insert/update/delete and stale snapshots. Integration uses real separate Oracle sessions, both unchanged consumers and direct legacy DML, interrupted backfill and restart. Historical suites retain their actual infrastructure prerequisites. No mock can establish availability or migration correctness.

## Test Specification

SM-1: compile Python experiment without executing SQL. UT-1: compare complete keyed representations; reject missing, duplicate and stale values. IT-1: run both legacy consumers during additive schema changes and interrupted migration; verify journal attribution, identifiers, no lost/duplicated changes, preserved baseline history/configuration, and optional language behavior. Real workload errors fail the experiment. A finite successful sample establishes availability for that sample, not a universal zero-downtime bound.

## Requirement-to-evidence checklist

PBI-048, BACKLOG paragraphs 347–351: pending continuous Hello and World legacy reads/writes during upgrade and recovery; pending both PL/SQL and schema compatibility; pending optional-language behavior; pending history and configuration retention. Evidence target: tests/experiment.json and raw SQL session logs.

PBI-081, BACKLOG paragraphs 611–615: pending attributable concurrent insert/update/delete; pending interrupted restart without overwriting newer values; pending preserved IDs; pending exact accepted source/target equality and unique identifiers at selected cutover. Same evidence target, with explicit source lock boundary.

PLAN E.12: pending A1/A2/A3 and full B1/B2/B3. Patch P8: pending reconciled documentation audit and local completion commits. Patch P9 and quality adapter: pending real live demo, presentation pair, manual, rendered inspection and handover record. Canonical sprint close: pending all quality gates and truthful recorded closure. No acceptance item is waived by YOLO thresholds.
