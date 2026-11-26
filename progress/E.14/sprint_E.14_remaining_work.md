# E.14 requirement-to-evidence checklist

## Authority and acceptance

[BACKLOG PBI-050](../../BACKLOG.md#pbi-050-prove-an-in-place-foundation-upgrade-with-component-windows) requires separate component windows, legacy/new coexistence, unaffected reads/writes and retained data through interrupted migration recovery. [PLAN E.14](../../PLAN.md#sprint-e14---validate-component-windows-and-assess-the-architecture) and [validation programme](../../docs/validation-programme.md#experiment-and-evidence-boundaries) select qualified mixed-version fixtures for this Elaboration experiment. The bounded fixture is the scope of the evidence; no production APEX rollout is claimed.

Separate windows: [Hello start](tests/run_18259/Hello-start.log.sql) and [World start](tests/run_18259/World-start.log.sql) enable only their component maintenance flag. Specific rejection assertions ensure that window blocks its own request. The same populated schema persists across both windows. Legacy arbitrary-text corresponds to the laboratory 1.1 bridge; template/name corresponds to its breaking 2.0 contract. These are fixture contract bindings, not published native release versions.

Unaffected reads/writes and coexistence: [World traffic](tests/run_18259/World-traffic.log) commits and reads back 80 requests while Hello migrates. [Hello traffic](tests/run_18259/Hello-traffic.log) does the same on the new route while World still uses legacy. The controlled caller registry is an implementation choice. Finite successful samples establish observed availability only.

Interrupted migration recovery: each component's interruption log records marked nonzero child termination. Its recovery SQL requires old route=1 and no partial migration journal before retry. Completion SQL commits the new route/journal and resumes the component. [Final assertions](tests/run_18259/assertions.log) and [live inspection](tests/run_18259/live-inspection.log) require both migrated routes, 163 complete history/detail rows and original greeting/configuration. No database-host crash or DDL transaction rollback is claimed.

[PBI-080](../../BACKLOG.md#pbi-080-assess-validation-evidence-and-the-construction-entry-decision) requires traceable risk synthesis, untested/conditional cases and a proposed Construction sequence with separate milestone acceptance. [Assessment](architecture_assessment.md) maps E.3 and E.5–E.14 evidence to risk, distinguishes prototype findings and production gaps, and proposes dependency-ordered work without inventing backlog assignments. No separate milestone acceptance is required to produce that recommendation.

## Mandatory workflow checks

[PLAN](../../PLAN.md) requires new smoke/unit/integration and full smoke/unit/integration regression. [Test report](sprint_E.14_tests.md) owns final outcomes and exact proof boundaries. [Local P8/P9](../../RUPStrikesBack.patch/RUP_patch.md) require audit, commits, actual demonstration, complete walkthrough/manual and rendered presentation: see [audit](sprint_E.14_documentation_audit.md) and [handover](sprint_E.14_handover.md). Local closure follows all gates. [Setup](sprint_E.14_setup.md) records repository and activation authority. Scratch settings and credentials remain unchanged.

## Implementation choices and deviations

Per-component maintenance flags, caller registry, transactional journal, Python syntax-tree setup reuse, no-authentication fixture schemas and 80-call samples are choices. They are not new acceptance requirements. The executable test-skeleton chronology deviation is disclosed in [implementation](sprint_E.14_implementation.md); no fabricated red run is used. Production callers, native release packaging of this Foundation fixture and unbounded-load guarantees remain unverified product behavior, not silently inferred from the experiment.

## Finalization remains open — Git authorization conflict

All technical gates and bounded acceptance observations pass. [Authorization audit](sprint_E.14_blockers.md) enumerates every unfinished mandatory outcome: root progress commit and cached pre-commit control, truthful recorded closure and closure commit, then final origin publication. Normal Git index access was denied by the sandbox and the scoped escalation was rejected by the permission tool. No local progress completion commit, closure or origin push is claimed. [Resumption](resume_after_git_authorization.md) preserves the concrete next actions; PLAN stays Progress and assigned board items stay tested.

## Finalization — 2026-11-26

The Product Owner explicitly requested finalization. The [closure record](sprint_E.14_closure.md) records Done for E.14, PBI-050 and PBI-080, the six passing gates and preserved production/milestone boundaries. This supersedes earlier statements that local commit and closure were still pending.
