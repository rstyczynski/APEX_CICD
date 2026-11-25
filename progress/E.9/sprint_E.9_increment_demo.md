# E.9 increment walkthrough

Goal: take accurate change context and a real agent report to current Review
and Testing evidence and controlled ordinary integration. The supported journey
uses an authenticated local disposable repository service. No external repository
is published. [Manual](user_manual.md) owns operation, [design](sprint_E.9_design.md)
owns policy, [implementation](sprint_E.9_implementation.md) owns mechanisms,
[tests](sprint_E.9_tests.md) owns evidence and [handover](sprint_E.9_handover.md)
owns acceptance. The matching editable deck is
[sprint_E.9_increment_demo.pptx](sprint_E.9_increment_demo.pptx).

## 1. Scope and architecture — slides 1–4

Start in this clone with Python 3, Git supporting merge-tree --write-tree and the
VS Code `code` command. Developer, Codex agent, authenticated Testing/Review
publishers, integrator, separate approver and administrator are distinct roles.
The Python service owns current refs, evidence and policy. Git owns actual
objects and compare-and-swap. No database or SQLcl operation is performed here.
Host administrator privileges are outside this bounded ordinary-caller test.

## 2. Initial context and scope change — slides 5–7

The context driver explained in the [manual](user_manual.md#context-and-pure-policy-checks)
creates a real change from name to name.strip(), then expands scope with one
assertion. It retains actual diffs and summaries, the developer annotation and
honest test states. This is PBI-068; the matching slides show the actual change.

```bash
cd "$(git rev-parse --show-toplevel)"
python3 tests/review_lab.py
code progress/E.9/tests/initial.diff
code progress/E.9/tests/refreshed.diff
code progress/E.9/tests/summary-initial.md
code progress/E.9/tests/summary-refreshed.md
```

Expect the Hello prefix preserved, whitespace removed and one assertion added.
The first summary says tests unrun; the second names the executed assertion and
explicitly removes an unsupported all-security-tests-passed claim. Both retain
“Developer: keep the Hello prefix; whitespace normalization only.” Blank input
remains a limitation. The assertion checks Hello World from spaced World input.

## 3. Real review and service journey — slides 8–10

The agent report is Codex's retained actual serial review of those source diffs,
not generated synthetic findings. Replays reuse it only for identical source
content. Security, correctness and testing assessments and the minor blank-name
finding are inspectable before submission. The service driver, explained in the
[manual](user_manual.md#run-the-service-experiment), runs the full HTTP/Git journey.
It generates temporary scoped capabilities, retains immutable-content report
revisions outside proposed source, executes the assertion, publishes authenticated
Testing/Review and integrates under one lock. This exercises PBI-069–071.

```bash
code progress/E.9/tests/agent-review-template.json
python3 tests/review_service_lab.py
code progress/E.9/tests/service/receipt.json
code progress/E.9/tests/service/results.json
code progress/E.9/tests/service/events.json
```

Expect PASS and an ordinary merge whose parents are the accepted base/head.
The actual merged greeting is executed and must produce Hello World. Receipt
identifies exact base/head/policy/report hash; retrieve its matching JSON from
the same service evidence directory. The service verifies accepted report bytes
remain retrievable after logical deletion. Independent approval is a distinct
credential role exercised by the laboratory, with no invented human reaction.

## 4. Refusals, races and recovery — slides 11–14

The same service run exercises invalid credentials, role spoofing, missing
assessments, unknown severities, unresolved blockers and acknowledgement-only
dismissal without altering reviewed source. Head/base/policy changes, report
editing, withdrawal and deletion revoke Review. Four concurrent HTTP events
interrupt publication; each prevents stale success. A report edit arriving inside
the integration interval waits on the merge lock, then rejects against its new
base. A change arriving first blocks integration. Native local receive-pack is
refused by a real hook. Publisher corruption tests are explicitly server-state
fault injection, supplementing actual unauthorized endpoint refusals.

```bash
code progress/E.9/tests/service/direct-write.log
code progress/E.9/tests/service/results.json
code progress/E.9/tests/service/events.json
```

Look for 403 role refusals, 409 policy/freshness failures, native hook refusal,
ordinary merge and a reasoned administrator bypass. Missing independent approval,
unresolved conversation and nonpassing/missing/stale evidence prevent ordinary
integration. Fix unexpected errors and rerun; no failing mandatory check is
waived. A bypass is an explicit separate event, not ordinary Review success.

The pure-policy unit runner explained in the manual supplies isolated synthetic
negative cases. It prints three passing groups and is distinct from HTTP tests.

```bash
python3 tests/test_review.py
```

## 5. Results and limits — slides 15–17

PBI-068 delivers context refresh/correction; PBI-069 delivers real review and
policy rejection; PBI-070 delivers revocation and concurrent freshness;
PBI-071 delivers authenticated combined checks, direct-write refusal and
recorded exception/approval behavior. Each maps to the accepted criteria in the
[test report](sprint_E.9_tests.md). Merge queue is not selected. GitHub portability,
production identity, hostile-host isolation and crash recovery are not claimed;
E.10 and later planned work remain unactivated. No new root backlog item is
introduced. The earlier pure-library failure and repair remain explicit.
