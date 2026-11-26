# E.15 design

Status: Accepted

YOLO self-approval covers this bounded Elaboration experiment. [Setup](sprint_E.15_setup.md) defines actors and scope; [checklist](sprint_E.15_checklist.md) owns requirement tracking. Retain prototype for evidence, not production deployment.

Trusted pull_request_target workflow takes immutable event candidate identity, uses base-owned validation code, and obtains only candidate SQL as data. Candidate SQL runs as an unprivileged Oracle application user in a dedicated hosted job service. It never executes as runner shell. Oracle SYS credentials belong only to the disposable fixture initializer; no retained host credentials are copied. Testing checks actual Oracle results and rejects SQL errors. Concurrency groups distinguish PRs and cancel superseded runs. GitHub runner disposal owns cleanup after cancellation; negative attempts must verify another candidate remains healthy.

### Testing Strategy

Test and Regression: smoke, unit, integration; full regression scope. Smoke compiles trusted validator and verifies fixture shape. Unit rejects invalid candidate path and empty and oversized SQL input. Integration executes real hosted Oracle SQL assertions; after hosted infrastructure is qualified, exercise concurrent PRs and cancellation. Existing full regression commands are bash tests/run.sh --smoke, --unit and --integration, each logged separately. Estimated hosted Oracle initialization is several minutes, bounded by job timeout.

## Test Specification

SM-15 validates validator syntax and fixture presence. UT-15 validates input rejection without database access. IT-15 executes SQL against Oracle and confirms expected data plus isolation from an independently initialized user. Hosted follow-on cases correspond exactly to checklist items 1–5. Failed/skipped hosted cases remain pending regardless of local results.

## Verified refinements and open design defect

Public sanitized visibility enabled native protection. Strict Integrated check source, administrator enforcement, stale-review dismissal and the named code owner protect ordinary merge. PR 4 was created by GitHub Actions and reviewed as the separately authenticated owner; the trusted report also binds exact candidate SQL bytes. The privileged initializer and publisher never execute candidate shell code. Trusted code now comes from github.sha, after the first report checkout failure. Oracle service publication binds 127.0.0.1.

A candidate-owned workflow in the same writable repository can request broader GITHUB_TOKEN permissions. Actual check spoofing and cancellation succeeded; independent owner review addresses merge approval but not run cancellation. This design is not accepted as complete isolation. A companion candidate fork with Actions disabled is a proposed supported remedy subject to scope approval and real tests. No app creation or approval is inferred from unanswered questions.
