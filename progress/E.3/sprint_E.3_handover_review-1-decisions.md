# Sprint E.3 technical handover — round 1 decisions

**Round:** E.3, round 1, Product Owner decisions and implementation checkpoint, 2026-11-04.

**Revision:** Original reviewed parent
`b695ec9627f1453220a04032563f812242f7ac0f`; application
`fbda57a0cbe4d32961ad826852bd04394a500c11` / v1.0.4.
The expert assessed the engineering response published at
`b0e4580a9b099b622dd217694431b71a1070c94f`. The maintained parent at feedback
entry was `9987e529caf8b9ad15f05cf536afc6c6baded036`; intervening changes are
review coordination only. The Product Owner subsequently selected the focused corrections and the temporary prepared-host credential accommodation. Correction evidence is linked below; no fresh runtime qualification is claimed.

**Reviewer:** Original external Codex engineering reviewer; exact model build
not exposed. Decision coordinator: Codex. Decision owner: Product Owner.

**Scope:** Assess the received feedback and present bounded corrections and
closing conditions. No runtime execution, source fixes, credential access,
production qualification or sprint-status change.

**Inputs:** [Original review](sprint_E.3_handover_review-1.md),
[engineering response](sprint_E.3_handover_review-1-response.md),
[expert feedback](sprint_E.3_handover_review-1-feedback.md),
[feedback prompt](sprint_E.3_handover_review-1-feedback-prompt.md) and
[offline counterexample](tests/review-1-negative-predicate.json).

## Current finding status

Corrections are committed and published at parent
`d37b461e23bf459ba34d5e5298a7f47af0306750` and seed controller
`eac24dedab3f611ef09b0196623cfabf674e7e1c`. Fixed labels below identify
committed corrections with engineering offline evidence; expert recheck is pending.

The expert accepts the proposed direction and requests the closing conditions
below. The Product Owner explicitly approved the fixes and selected Option B for L1:
“Approve fixes; allow temporary lookup on this prepared host.” M1/M2/L2 are
selected for implementation with offline validation. L1 is explicitly deferred
under the narrow accommodation and ending/reconsideration trigger below.

| Finding | Current status | Reviewer reaction | Proposed Product Owner action |
|---|---|---|---|
| R1-M1 | fixed@d37b461 | Accept | Select focused deck/notes/authoring-source correction. |
| R1-M2 | fixed@d37b461 | Accept documentation-only option | Select clarification of fixed reference-evidence tests and separate LAB acceptance. |
| R1-L1 | deferred | Accept with clarification | Option B approved: temporary retained-host lookup; supported explicit VM startup; no new store. |
| R1-L2 | fixed@d37b461 | Accept with clarification | Select a specific negative assertion with offline validation; keep runtime claims separate. |

## R1-M1 — Proposed focused presentation correction

**Owner if selected:** Codex implementation/documentation, reviewed by Product
Owner. **Why now:** Current presentation commands can select the shared seed
instead of the operator's LAB during the promised demonstration.

Pass the explicit LAB repository and runner directory on both setup and run.
Identify how the command terminal obtains `e3_repo` and `version_tag` from the
current setup/release-selection steps. Dispatch against those values, not a
fixed seed/tag. Retain the v1.0.4 result as visibly historical. Synchronize slide
notes, authoring source, walkthrough references and presentation validation.

**Closing evidence:** Committed correction; extracted command/notes comparison
with walkthrough B/F; rendered inspection of changed slides and preservation
of unrelated deck content. No runner registration or deployment is needed.

## R1-M2 — Proposed documentation-only evidence clarification

**Owner if selected:** Codex documentation, reviewed by Product Owner.
**Why now:** Fixed seed evidence-reader results cannot accept another operator's
new LAB journey, and access to seed environment variables is not implied by
public source visibility.

Keep current tests rather than adding parameterization to this prototype.
Correct the current descriptions in the manual, test profile, test record,
configuration/handover and implementation as needed. Name the hard-coded seed,
reference deployment/qualification IDs and API permissions. Distinguish fresh
downloads from fresh execution. Label the older throwaway-clone/private-state
description historical. Explain that current platform smoke probes the seed's
configured HTTP endpoint while IT-1/IT-2 inspect recorded workflows.

New LAB acceptance must use that operator's repository and actual change/release
PRs, generated tag and resolved source SHA, deployment receipt/archive identity,
native logs, separate qualification result if performed, and browser title/history
observation. Passing seed-evidence readers is not a substitute or a prerequisite
available to every LAB operator.

**Closing evidence:** Committed documentation reconciliation and static comparison
with actual test inputs. Preserve historical passes and artifact availability
limits. No new workflow, download or database operation is needed for this wording
correction. Selected-replay automated validation would be a separate choice.

## R1-L1 — Product Owner policy choice required

**Owner:** Product Owner chooses policy; Codex implements the selected
documentation/startup boundary. **Why now:** The required existing-source password
lookups and categorical temporary-only scratch policy currently conflict.
Neither engineering nor external reviewer may invent an exception or silently
remove the requested lookup.

**Option A — consistent assigned-credential path.** Use already assigned Builder,
author-schema and LAB_USER credentials obtained through a Product Owner-confirmed
compliant existing source. Current instructions use that path; scratch lookup
examples become historical. This does not authorize creating a new store,
copying/moving private records, deleting them, or retrieving plaintext secrets
from GitHub. GitHub secrets cannot supply readable interactive passwords through
their API. The concrete credential-source instruction must be confirmed before
claiming this option implemented.

**Selected Option B — temporary prepared-host accommodation.** Explicitly retain the
requested lookup from the existing E.1/E.2 record on the already prepared lab
host as a narrow temporary exception. Do not create new authoritative settings
there or present the file as disposable while it remains required. Keep GitHub
environment secrets authoritative for jobs and native author profiles outside
the checkout. Do not move/delete any private record. This is the approved **deferral**, not verification of the scratch prohibition.

**Approved deferral trigger for Option B:** End the accommodation when a compliant
credential-source remedy is selected; reconsider before independent/new-host
reproduction, scratch cleanup or any expansion of this retained-host exception.
PBI-054 remains the wider reproduction proof, not a completion claim here.

**Startup boundary under either option:** The supported sequence explicitly
starts/checks the retained VM before containers. Document that the inherited
VM-start fallback reads a scratch `containers.conf` override and is outside
that supported sequence until separately corrected. Do not claim the fallback
has no local configuration dependency. No infrastructure reset is needed.

**Closing evidence:** Either a consistent committed supported path with a
confirmed credential source, or an explicit Product Owner deferral naming the
residual prepared-host dependency, owner, reason and trigger. Merely calling
the file legacy does not close the contradiction. No credential values need
to be supplied to the reviewer.

## R1-L2 — Proposed assertion correction and validation level

**Owner if selected:** Codex implementation/test/documentation, reviewed by
Product Owner. **Why now:** The current predicate can label an unrelated native
error as the intended missing-file rejection. The recorded missing-file failure
itself remains genuine.

Require a positive error count, ERROR on `stagechangelogfilesvalid` and the
exact path selected for removal, associated with the same verification result
and failing rule message. Preserve the association through supported ANSI,
padding and continuation-line normalization; do not independently match unrelated
whole-log occurrences. Use literal path comparison or correctly escaped matching.
Require consistency between the selected path, diagnostic and new-format receipt.
Apply the same semantics to qualification, evidence reading and manual exercise.

Keep the historical v1.0.4 log/receipt unchanged: its receipt lacks the new path
field. Explicitly distinguish that pinned legacy evidence from new-format
qualification. Identify corrected controller revision separately from selected
application SHA; correcting main does not change the application tag.

**Proposed validation level:** Offline checks first. Execute the actual corrected
predicate against retained positive/negative logs and fixtures for unrelated
errors with INFO stage rows, wrong paths, incomplete/connection failures and
supported formatting variants. Check receipt/path agreement and all callers'
acceptance semantics. This can verify the classification correction without
a database, deployment or fresh native workflow claim.

**Runtime follow-up, only if separately selected:** A fresh qualification run
must identify controller revision, application SHA, SQLcl build, removed path,
positive/negative native logs, unchanged-target comparison, receipt and cleanup.
No deployment is required. Do not call offline parser checks a native workflow
success. Do not rewrite the accepted v1.0.4 tag or historical evidence.

**Closing evidence:** Committed correction with actual offline results and exact
source identities; any claimed fresh native success additionally needs its own
run evidence. The next independent recheck must say which validation level it
assessed.

## Outcome and next step

The Product Owner selected M1's focused PPTX correction, M2's documentation-only
clarification, L2's specific assertion with offline validation, and L1 Option B.
Codex owns the selected implementation/documentation; the Product Owner owns
L1's exception and eventual remedy. No fresh native qualification or deployment
was selected. The next independent review will assess the committed correction
and its stated offline validation level; it must not infer a runtime result.
The [correction checks](tests/review-1-correction-checks.json) identify evidence.
No sprint acceptance, new backlog assignment or next-sprint activation is implied.

The original feedback's SHA-256 is
`3433744fc3c8f91393bb3efdd58bd68e386c1215b150702a69f05dabf07a2c82`.
Its text is preserved unchanged. Checks for this coordination step were reading
the feedback against the prior engineering response, verifying exact revisions,
original-report/feedback integrity, relative navigation and whitespace. No code
or runtime check was repeated. The selected disposition is recorded above. No private records were read, moved
or deleted to implement the accommodation.

The [round-2 recheck prompt](sprint_E.3_handover_review-2-prompt.md) pins the
committed source and evidence. No independent recheck or round closure is claimed.
