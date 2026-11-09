# E.4 design — Round 1 engineering response

**Round:** E.4 design, round 1, engineering response.
**Revision:** Original 0eb39eb7b42b08092e491820fbb29f4b30920e12;
corrected design 0ad508b6e872ca500c5ac92c6b60d555fc154cb4, current source checkpoint.
**Reviewer:** Dedicated E.4 local Astra chat; this response is the coordinator's.
**Scope:** Textual design corrections only; no implementation or runtime validation.
**Inputs:** [Original report](sprint_E.4_design_review-1.md),
[corrected design](sprint_E.4_design.md), [audit](sprint_E.4_documentation_audit.md),
[feedback prompt](sprint_E.4_design_review-1-feedback-prompt.md).

| Finding | Status | Closing evidence required |
| --- | --- | --- |
| R1-M1 | agreed | Dedicated expert textual recheck of trusted-baseline procedure and IT-3 |
| R1-M2 | agreed | Dedicated expert textual recheck of availability/receipt lifecycle and IT-4 |

## R1-M1 — Agreed

The E.3 receipt binds source/archive but provides no trusted application checksum.
The first live observation is therefore not sufficient baseline authority. The
new Trusted baseline qualification section requires either qualified retained
checksum evidence or explicit read-only comparison of live export against the
source actually installed by the hashed accepted archive. Exact target/settings
and generated differences require evidence-backed explanation; unexplained
content blocks without reinstall, reset or silent adoption. Two unchanged reads
establish stability only after reconciliation, and the baseline persists between
attempts. IT-3 adds pending work already present before baseline qualification.

The correction closes a design omission, not a runtime proof. If reconciliation
cannot establish equivalent accepted source, PBI-042 execution remains blocked;
the design does not promise an effortless native semantic comparison command.
Acceptance for this review is a complete, safe first-run procedure and explicit
stop condition; planned runtime checks remain mandatory after approval.

## R1-M2 — Agreed

Inherited native imports may restore AVAILABLE, so the old continuous-unavailability
claim was incorrect. The revised Availability, deployment and receipt lifecycle
section distinguishes coordinated participant exclusion from technical access state.
It requires observations before/after restriction, import, renewed restriction and
restoration. Failure requires reporting actual status and retaining coordinated
exclusion; it does not establish that restriction persisted. The known supported
restriction API may be attempted and its outcome recorded; unknown partial states
remain blocked for a separate recovery decision.

Split inherited accept.sql's read-only acceptance checks from its publication
step after approval, and update its hard-coded heading expectation. Complete
preservation/behavior checks while restricted, restore the intended AVAILABLE state,
then compute and finalize the checksum receipt in that same state used by next
admission. IT-4 measures actual status/checksum transitions; it does not assume
availability is checksum-neutral or normalize unknown differences away.

Acceptance for this review is coherent state/receipt sequencing and honest failure
instructions, not qualification of an import-spanning lock. Production fencing is
still out of scope. The dedicated reviewer is asked to recheck both corrections.

## Checks performed

Inspected the original report, E.3 retained receipt and inherited restrict/deploy/
accept SQL. Checked revised design and IT-3/IT-4 against each finding. All E.4 local
Markdown file targets and git diff --check passed before the source checkpoint.
No database connection, SQLcl command, browser interaction, workflow dispatch,
implementation or test skeleton was executed/created. The original report remains
unchanged. Source checkpoint push succeeded and git ls-remote confirmed the full
corrected source SHA. Product Owner approval remains pending.
