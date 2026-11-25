# E.9 implementation

[Design](sprint_E.9_design.md) owns interfaces; [tests](sprint_E.9_tests.md)
own actual verification and [walkthrough](sprint_E.9_increment_demo.md) owns the
reproducible journey. This is an Elaboration experiment retained for evidence,
not a production GitHub integration or security-isolation deliverable.

## Actors and executed journey

Developer supplies context and chooses Codex as the reviewing agent. Codex's
serial reviewer role inspected the actual initial/refreshed greeting diffs and
recorded security, correctness and testing observations. The exact report content
is in [agent-review-template.json](tests/agent-review-template.json). The report
records no new I/O/credentials, preserved Hello prefix, the one-assertion coverage
limit and remaining blank-input behavior. This is actual Codex review, reused for
identical source content, not a claim of fresh inference on every replay. The
review task was to assess the retained initial and refreshed diff under those
three policy headings; no external model tool or hidden prompt was used.

The initial summary states tests unrun; the refreshed summary includes the new
assertion and its passing state, retains the developer annotation and explicitly
corrects the deliberately unsupported all-security-tests-passed claim. No report
submission/rejection changes reviewed source. Git bundles retain actual history.

## Mechanisms

`scripts/review_control.py` implements pure policy and canonical SHA-256 report
identity. `scripts/review_service.py` adds a real loopback HTTP boundary. Each
role has a distinct random bearer capability. Tokens remain in test-process
memory and are never written to retained logs. Requests authenticate before
role authorization. A developer cannot claim reviewer, Testing publisher,
approver, integrator or administrator privileges by changing JSON fields.

Report revisions are stored outside source under their content hash, created
exclusively, marked read-only and integrity-checked on retrieval. Editing changes
the current pointer; withdrawal/deletion revoke current evidence while accepted
history remains retrievable. Head/base/policy events revoke Review and approval.
Publication captures generation and candidate, then validates both again under
the server lock after preparation. Four real concurrent HTTP cases interrupt
publication. The test synchronization controls live only in the trusted fixture;
no client API permits bypassing synchronization or checks.

Merge holds the same lock used by all events. It rechecks report, Testing,
Review, authenticated publishers, conversations and independent approval. It
uses native Git merge-tree/commit-tree and update-ref with expected old SHA.
An edit arriving during integration waits and then fails against the changed
base; an earlier candidate event rejects the merge. After integration old checks
cannot authorize the new base. The native pre-receive hook rejects direct
receive-pack writes. The trusted service is the sole ordinary integration path.
Administrator bypass requires a reason and records actor, candidate and commit.
Merge queue is not selected: this service has no queue endpoint.

## Earlier failed approach and repair

Commit 3f3b2f0 preserved the initial pure library. That library accepted injected
identity strings and only double-read publication state; it could not establish
actual caller permissions or protect the final integration interval. The earlier
hosted-only blocker was unsupported: backlog requires a disposable repository,
not GitHub. The implemented local service resolves those experiment gaps using
real capabilities, HTTP concurrency, a protected receive path and serialized
compare-and-swap. Synthetic persisted-record corruption remains explicitly
fault injection; it supplements actual unauthorized API and native Git refusals.

## Limits and retention decision

The service owns a temporary local bare repository; no network repository is
published. Host administrators and processes with the same OS account can change
repository files or read process memory, just as repository administrators can
bypass controls. E.9 tests ordinary API/receive callers, not hostile-host
isolation (E.10). Loopback bearer capabilities are not a production identity
provider, TLS deployment, GitHub check app, durable crash-recovery service or
production merge queue. Testing in this fixture is one executed Python assertion;
E.8 owns comprehensive candidate-suite validation. Agent evidence is process
validation, not independent approval or proof every defect was discovered.
The selected approver is a separate capability role exercised by the laboratory,
not an invented human approval. These limits do not waive any E.9 criterion.
