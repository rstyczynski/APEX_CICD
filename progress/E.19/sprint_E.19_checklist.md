# E.19 requirement-to-evidence checklist

## Mandatory acceptance — BACKLOG PBI-087

Inventory every workflow Python support check and document dispositions: partial, [initial inventory](sprint_E.19_inventory.md); completeness pending.

Provide discoverable reusable action catalogue, purpose/inputs/outputs/failures/usage: initial three actions implemented in [catalogue](../../sprint-work/E.19/CATALOGUE.md), broader inventory pending.

Remove migrated checks' Python dependency and optimization-sensitive provenance assertions: implemented in initial three-action slice, explicit JavaScript exceptions; [local tests](tests/initial-unit.log) pass 3 test groups. Hosted source 6b6a412 uses Node action runtime and no Python command.

Demonstrate every in-scope check through catalogued actions in real GitHub workflows with valid, malformed/missing inputs and source/artifact/tool mismatches before mutation: partial. [Run 45873741697](https://github.com/rstyczynski/APEX_CICD_E.19/actions/runs/45873741697) executes all three valid actions and malformed provenance rejection with skipped filesystem mutation sentinel. Other negative contracts run as unit functions, not yet every catalogued-action case. Synthetic file fixtures do not establish real SQLcl/Oracle target behavior.

Preserve native technology responsibilities and historical evidence: initial implementation performs checks only; old evidence retained. Native workflow migration pending.

Acceptance and full smoke/unit/integration regression: pending. Initial Node unit tests do not satisfy all six RUP gates.

## Mandatory plan additions — PLAN E.19

Equivalent Python/JavaScript workloads and runner conditions; versions, counts, cold/warm setup/check/overall timings; installation/dependency/maintenance assessment: pending. Preinstalled Python must not be reported as installation cost. No performance benefit claimed.

Official OCI JavaScript SDK for any needed OCI interactions: none selected so far; full inventory pending.

## Mandatory execution instructions and method

Screenshots: two real Chrome application-window captures retained; [gallery](screenshots/index.html) pending rendering/navigation verification. Opening workflow summary and job detail captured after actions occurred; no earlier dispatch capture exists.

Chat archive: [index](chat/index.md) records native JSONL snapshots and readable companions with writer-lag limits. Snapshot refresh required before handover/final response.

Demonstration, PPTX walkthrough pair, manual, rendered-slide review, documentation audit, completed-increment commits and closure: pending. No Product Owner reaction or acceptance invented.

## Implementation choices

Three native node24 actions sharing dependency-free CommonJS logic; regular-file validation; explicit throws; synthetic fixture sentinel. These are design choices, not extra acceptance requirements.

## Blocker audit

No external blocker is established. Remaining items are implementation and verification work, not grounds for closure or a blocker claim. Browser connector is unavailable, but native Chrome control succeeded. No authorization clarification is needed.
