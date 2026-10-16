# E.1 — Fold-in fixes

## BUG-1 — SQLcl could finish without executing buffered interactive SQL

Item: PBI-011.1. Status: fixed. Severity: high.

A preservation fixture prepared with piped interactive MERGE was absent in a later session. A separately committed INSERT survived qualification-area recreation. The SQLcl wrapper now executes protected script files and requires a server-side completion marker before success. Rechecked MERGE persistence and deliberate Oracle-error propagation. The fix is included in the current platform increment; no broader scope is introduced.
