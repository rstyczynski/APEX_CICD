# E.15 design

Status: Accepted

The accepted current revision is the companion-boundary refinement below. Earlier mechanism paragraphs record the tested evolution and are not the active same-repository execution design. The final checklist and closure own current acceptance/lifecycle status.

YOLO self-approval covers this bounded Elaboration experiment. [Setup](sprint_E.15_setup.md) defines actors and scope; [checklist](sprint_E.15_checklist.md) owns requirement tracking. Retain prototype for evidence, not production deployment.

Trusted pull_request_target workflow takes immutable event candidate identity, uses base-owned validation code, and obtains only candidate SQL as data. Candidate SQL runs as an unprivileged Oracle application user in a dedicated hosted job service. It never executes as runner shell. Oracle SYS credentials belong only to the disposable fixture initializer; no retained host credentials are copied. Testing checks actual Oracle results and rejects SQL errors. Concurrency groups distinguish PRs and cancel superseded runs. GitHub runner disposal owns cleanup after cancellation; negative attempts must verify another candidate remains healthy.

### Testing Strategy

Test and Regression: smoke, unit, integration; full regression scope. Smoke compiles trusted validator and verifies fixture shape. Unit rejects invalid candidate path and empty and oversized SQL input. Integration executes real hosted Oracle SQL assertions; after hosted infrastructure is qualified, exercise concurrent PRs and cancellation. Existing full regression commands are bash tests/run.sh --smoke, --unit and --integration, each logged separately. Estimated hosted Oracle initialization is several minutes, bounded by job timeout.

## Test Specification

SM-15 validates validator syntax and fixture presence. UT-15 validates input rejection without database access. IT-15 executes SQL against Oracle and confirms expected data plus isolation from an independently initialized user. Hosted follow-on cases correspond exactly to checklist items 1–5. Failed/skipped hosted cases remain pending regardless of local results.

## Verified refinements and open design defect

Public sanitized visibility enabled native protection. Strict Integrated check source, administrator enforcement, stale-review dismissal and the named code owner protect ordinary merge. PR 4 was created by GitHub Actions and reviewed as the separately authenticated owner; the trusted report also binds exact candidate SQL bytes. The privileged initializer and publisher never execute candidate shell code. Trusted code now comes from github.sha, after the first report checkout failure. Oracle service publication binds 127.0.0.1.

A candidate-owned workflow in the same writable repository can request broader GITHUB_TOKEN permissions. Actual check spoofing and cancellation succeeded; independent owner review addresses merge approval but not run cancellation. This design is not accepted as complete isolation. A companion candidate fork with Actions disabled is a proposed supported remedy subject to scope approval and real tests. No app creation or approval is inferred from unanswered questions.

## Approved companion-boundary refinement

The Product Owner explicitly authorized APEX_CICD_E.15-candidates in the conversation. GitHub's self-fork API returned the original non-fork repository even with the new name; the authorized companion was therefore created as a standalone candidate repository. This preserves the requested candidate/validator separation without claiming a fork network that does not exist. The change is self-approved under the continuing YOLO delegation and recorded as a material implementation decision.

Candidate SQL and ordinary PRs now live in the companion with repository Actions disabled. A harmless candidate-owned dispatch sentinel may be accepted into GitHub's queue, but actual observations show no job allocation while trusted validation proceeds. Queue acceptance is not claimed as execution refusal: native configuration, zero-job observations and subsequent cleanup are retained separately. No candidate source is checked out or executed as host code in the trusted repository. A candidate-owned workflow cannot obtain a runtime token through a job that is never allocated. This is the corrected boundary for untrusted candidate code; an administrator's independent GitHub credential remains trusted and is not given to candidate code.

Trusted workflow_dispatch accepts a numeric companion PR identifier, retrieves immutable candidate SQL as data, validates changed paths and the exact trusted report bytes, and executes the real Oracle checks. The trusted local operator controller independently checks Actions-disabled state, current PR head/base, trusted policy commit, exact source digest, correlated run identity, terminal success and actual job provenance before publishing TrustedOracle to the companion. It sets pending before validation and failure on validation/cancellation failure. Ordinary merge revalidates the receipt and uses native strict protection plus --match-head-commit; --admin is never used for candidate acceptance. The trusted operator's GitHub credentials are never mounted into Oracle or passed to candidate code.

GitHub's same-account owner remains the real authenticated integration actor. In this corrected boundary Review is the actual inspected report and its trusted byte binding, rather than an invented independent human or self-approval through GitHub's native review UI. Native owner review in the earlier single-repository experiment remains historical evidence. Cross-repository publication is done by the trusted operator, not by the candidate workflow token. New smoke compilation and receipt-binding unit contracts accompany actual companion end-to-end execution; injected unit contracts are not hosted acceptance evidence.
