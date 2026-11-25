# E.6 — Contract and analysis

## Contract

The Product Owner explicitly selected E.6 and authorized fully autonomous YOLO implementation. [PLAN](../../PLAN.md) owns activation, assignments and Test: smoke, unit, integration / Regression: smoke, unit. The selected secure_backend regression scope includes all current pipeline smoke and the E.5 backend unit suite, without operating the retired E.1 controller. [The board](../../PROGRESS_BOARD.md) owns tracking and [BACKLOG](../../BACKLOG.md) owns the four unchanged criteria. The manager's contractor/analyst/design/construction/test/documentor responsibilities are performed serially. Existing E.5 artifacts remain immutable; shared test infrastructure can redirect new regression output to E.6. No remote push is authorized. Per-phase token accounting is unavailable.

## Analysis

A developer defines a stable greeting component contract and uses native APEX sessions to supply synthetic identity/country context. An authenticated page user submits a request in their permitted country. A backend consumer calls the same transaction-owned package. A reviewer observes compatible fixes/additions, deliberate incompatible results and real competing Oracle sessions. This is the SRS actor journey at a bounded Elaboration depth; a schema owner or administrator remains trusted infrastructure, not an untrusted application principal.

PBI-063 requires explicit allowed/denied contexts, cross-country rejection, failed initialization propagation, cleanup and separate real password/page observations. Native CREATE_SESSION with a supplied username is a privileged test setup API and does not prove authentication. PBI-052 requires explicit component promises, including shared LOV semantics and retained data. PBI-064 requires unchanged executable consumers across compatible variants and a callable deprecated interface, while retaining whole-application deployment. PBI-079 requires controlled concurrent interleavings, duplicate handling and no unintended partial write under a declared transaction contract.

## YOLO choices

Use a new E6_APP workspace/schema and E6_TEST test schema on the prepared FREEPDB1 host; reuse the pinned utPLSQL framework without changing its implementation. Select one request operation that writes a request and an audit row atomically, with a per-call savepoint and caller-owned commit. Use unique country/request keys for duplicate rejection and a test-only trigger to inject second-write failure. Protect runtime country decisions on every call; leave ordinary rendering independent of APEX session state. [Design](sprint_E.6_design.md) owns exact cases and interfaces.
