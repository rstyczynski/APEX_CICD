# E.15 setup

This setup snapshot records activation-time observations. Its initial private-plan limitation and earlier scope question were resolved; the current [checklist](sprint_E.15_checklist.md), [implementation](sprint_E.15_implementation.md) and [closure](sprint_E.15_closure.md) own the final disposition.

## Contract

The Product Owner explicitly authorizes activation, YOLO execution, temporary GitHub repository operations and final origin publication. [PLAN](../../PLAN.md#sprint-e15---validate-integrated-github-and-oracle-execution) assigns PBI-083 alone. The inherited uncommitted E.15–E.18 scheduling edits are preserved; only E.15 is activated. The previous [scope audit](sprint_E.15_scope_audit.md) is historical: its missing-assignment finding is superseded by the present plan.

## Analysis

Developer proposes source; trusted Testing executes Oracle assertions; reviewer assesses the actual diff; GitHub enforces ordinary merge. Reuse E.8 candidate policy, E.9 review freshness and E.10 isolation evidence only as design inputs, never hosted acceptance evidence. GitHub E.10 repository lookup failed; E.14 remote contains README/tests. This sprint creates a dedicated sanitized fixture repository, not a copy of retained credentials or application state. No SQLcl PROJECT operation is planned in this candidate experiment; native release delivery remains E.16.

Repository creation succeeded at https://github.com/rstyczynski/APEX_CICD_E.15. Both protected branches and rulesets returned HTTP 403 requiring GitHub Pro or public visibility. Visibility approval is pending; no silence will be treated as approval. Hosted Oracle execution and local regression remain independent work.
