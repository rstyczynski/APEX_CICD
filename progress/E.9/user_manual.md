# E.9 authenticated review laboratory

[Walkthrough](sprint_E.9_increment_demo.md) owns the complete user journey;
[implementation](sprint_E.9_implementation.md) explains mechanisms and limits.
Use Python 3, Git with merge-tree --write-tree, and VS Code's `code` command on
PATH. The prepared host already supplies them. No external account, database,
credential record or remote repository is used by the E.9 experiment itself.

## Run the service experiment

The driver creates a private temporary directory, two real Git histories and a
loopback HTTP service. It generates separate role capabilities in memory,
submits the actual retained Codex review, authenticates publisher requests and
exercises negative cases. Report revisions are kept outside source. Concurrent
HTTP clients challenge publication and the final merge lock. Native send-pack
attempts a write to the temporary filesystem repository and is rejected by its
pre-receive hook; this uses local Git processes only, with no external host.
The integrator then performs a checked merge and the administrator demonstrates
a recorded exception. The driver saves redacted receipts, events, diffs and
bundles in progress/E.9/tests/service and closes the server before removing only
its own temporary directory. There is no persistent runner or credential setup.

```bash
cd "$(git rev-parse --show-toplevel)"
python3 tests/review_service_lab.py
code progress/E.9/tests/service/results.json
code progress/E.9/tests/service/direct-write.log
code progress/E.9/tests/service/events.json
```

Expect status PASS, an ordinary_merge receipt and a reasoned administrator bypass.
The direct-write log must show pre-receive hook declined. The results file
contains HTTP 403 authorization refusals, HTTP 409 evidence/refusal cases and
HTTP 200 accepted operations. Observation counts include setup/inspection calls;
they are not independent test-case counts. Saved reports contain no bearer keys.

## Context and pure-policy checks

The original local driver creates the same greeting change in a disposable work
repository. It retains initial/refreshed summaries and the developer annotation,
removes an unsupported claim and runs the one added Python assertion. Its pure
controller uses injected identities; the service experiment above supplies the
actual authentication/ref boundary. Run it to inspect PBI-068 context in order.

```bash
python3 tests/review_lab.py
code progress/E.9/tests/summary-initial.md
code progress/E.9/tests/summary-refreshed.md
code progress/E.9/tests/refreshed.diff
```

The unit runner isolates report policy, freshness and merge decisions using
synthetic records. Run it when diagnosing policy behavior, independently of HTTP.

```bash
python3 tests/test_review.py
```

## Recovery and boundaries

On unexpected failure retain the traceback and logs, correct its cause and rerun
the affected driver. No success may be substituted for absent evidence. Reruns
replace current receipts/events and retain report snapshots by hash; inspect a
receipt only with its corresponding candidate. The temporary service has no
production deployment command, TLS, identity provider or durable crash recovery.
The trusted host administrator can alter files and process memory; E.10 owns
hostile execution isolation. Independent approval is exercised by a separate
capability role, not a claim of human approval. The greeting fixture still allows
blank names and assumes strings. GitHub protection and merge queues are not
selected implementations. Production adoption requires a separate reviewed design.
