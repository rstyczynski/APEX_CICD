# E.9 demonstration walkthrough

E.9 promised current AI Review evidence alongside Testing and controlled ordinary
integration. This delivered prototype demonstrates the local policy portion;
server enforcement remains unfinished. [Manual](user_manual.md) owns operation,
[implementation](sprint_E.9_implementation.md) owns limitations and
[handover](sprint_E.9_handover.md) owns the decision. The presentation pair is
[sprint_E.9_increment_demo.pptx](sprint_E.9_increment_demo.pptx).

## 1. Starting state and scope — slides 1–4

Use this clone with Git and Python 3. No database or SQLcl processing occurs.
The actors are developer, Codex reviewer, trusted controller and integrator.
The report lives outside proposed source. Publisher and identity inputs are
synthetic trusted-caller values; no hosted authentication is implied.

## 2. Run the real local journey — slides 5–6

The driver explained in the [manual](user_manual.md) makes two real source
revisions, runs one greeting assertion and retains a Git bundle. It refreshes
summaries without losing the annotation and removes an unsupported success
claim. This exercises PBI-068 and the bounded portions of 069–071.

```bash
cd "$(git rev-parse --show-toplevel)"
python3 tests/review_lab.py
code progress/E.9/tests/initial.diff
code progress/E.9/tests/refreshed.diff
code progress/E.9/tests/summary-initial.md
code progress/E.9/tests/summary-refreshed.md
```

Expect name.strip() plus one assertion in the refreshed diff; the first summary
states tests were not run, the second states the exact passing assertion. Both
retain the developer annotation. The corrected claim is visible in the second.

## 3. Inspect accepted evidence and merge — slides 7–8

```bash
code progress/E.9/tests/agent-review-template.json
code progress/E.9/tests/reports
code progress/E.9/tests/journey.json
```

Inspect the security/correctness/testing assessments, minor blank-name finding,
base/head/policy and hashed report revision. Expect decision.allowed true and a
merge SHA. Independent approval is injected true, not a human approval. The real
agent report is Codex's retained serial review; repeated driver runs reuse its
content for identical source, rather than invoke a new reviewer.

## 4. Challenge failures and limits — slides 9–10

The unit script invokes three groups that mutate report policy, freshness and
merge evidence. Inputs are synthetic to isolate rejection decisions. It rejects
missing assessments, unauthorized values, unknown severity, unresolved blockers,
unsupported dismissals, changed base/head/policy/report, withdrawal/deletion,
a publication race, wrong publishers and missing/nonpassing checks. Bypass is
recorded separately when the injected administrator identity requests it.

```bash
python3 tests/test_review.py
```

Expect three passing groups. These tests cannot prevent a local user running
Git directly or a change occurring after the final publication read. E.9 cannot
close until an authenticated server boundary is implemented and verified.

## 5. Decision — slides 11–12

All four assigned PBIs remain unfinished as end-to-end outcomes. No later sprint
is activated. No remote push occurred. The local prototype is useful evidence,
but its passing tests do not discharge the missing repository controls.
