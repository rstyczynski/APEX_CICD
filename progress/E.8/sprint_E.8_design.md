# E.8 design

Status: Accepted under delegated YOLO authority

[Setup](sprint_E.8_setup.md) owns analysis; [backlog](../../BACKLOG.md) owns criteria. [Implementation](sprint_E.8_implementation.md) will own actual behavior.

Trusted Python controller accepts base/head revisions and cadence, creates a merge commit in a disposable local repository, selects mandatory suites from its own inventory, then checks source before any database preparation. Candidate content cannot replace this inventory. Unknown files select all suites. Migration and contract edits always include their respective checks. Disabled critical coverage rejects the plan. Reports bind cadence, merge SHA, tree, policy digest and suite counts; every mandatory result must be successful and nonempty. Reporting cannot overwrite the original failure.

One no-authentication disposable schema receives merged SQL. Each case records preparation, deployment, compilation, state and backend results, then drops only its generated schema. SQLcl qualification precedes mutation. Database probes use the existing prepared-host local laboratory SQLPlus transport; no GitHub privileged execution or native PROJECT production deployment is claimed.

### Testing Strategy

Test: smoke, unit, integration. Regression: full smoke, unit. No skipped criteria or flaky deferrals.

| ID | PBI | Check | Expected |
|---|---|---|---|
| SM-1 | 066 | Python syntax, trusted inventory and baseline SQL present | pass before DB |
| UT-1 | 067 | missing/empty/unknown/weakened/disabled plan, missing report; skipped/neutral/cancelled/failure and attribution mismatch | reject |
| UT-2 | 076 | PR/scheduled/prerelease selection, unknown fallback, migration/contract inclusion | required suites |
| IT-1 | 066,076 | real merged candidate, all three cadences | deploy and pass |
| IT-2 | 066,067 | migration, compilation, state, assertion faults; cheap source failure | non-success, dependent work absent |

## Test Specification

Register smoke/unit/integration wrappers in new_tests.manifest and component_candidate.manifest. Unit tests use synthetic result records explicitly; integration tests require real Oracle and retained per-stage logs. Write tests before controller; expected initial failure is import of missing controller. Candidate source may contain only SQL/data; trusted controller executes no candidate script. This bounds, but does not solve, malicious SQL isolation (E.10).
