# E.9 setup

## Contract

E.9 is activated under explicit Product Owner authority: Planned → Progress,
managed → YOLO. Test: smoke, unit, integration; regression: full smoke, unit.
Only E.9 and shared documentation change. No remote pushes or next activation.
The RUP manager and all five role adapters apply, with local P8 increment commits
and P9 handover. Credentials and retained E.3 secrets remain untouched.

## Analysis

[Backlog](../../BACKLOG.md#pbi-068-validate-agent-generated-pull-request-context-against-the-diff)
owns PBI-068–071 acceptance; [programme](../../docs/validation-programme.md#e9--validate-ai-review-and-ordinary-merge-decisions)
owns the experiment question. E.8 validates Testing content; E.9 binds evidence
to a candidate and evaluates ordinary integration. Developer supplies annotations
and chooses an agent; validator authenticates submission separately from report
claims. Integrator rechecks current evidence at publication and merge.

YOLO decision: use a disposable local Git repository and trusted controller for
bounded merge decisions without remote pushes. This cannot establish GitHub
branch-rule or publisher enforcement. That distinction must remain explicit and
hosted verification must not be silently replaced by synthetic proof.

YOLO decision: perform the real agent review as a separate serial Codex reviewer
responsibility, retaining report and exact diff. No independent human approval
is inferred. Select explicit independent-approval and recorded bypass scenarios;
merge queue is not selected. No SQLcl processing is needed for this controller.

[Design](sprint_E.9_design.md) owns interfaces and tests. Token telemetry is not
available per phase; no measurements are invented.
