# Round files and findings

## File convention

Use the current sprint's evidence directory and identify the reviewed document
or stage in every round filename. Choose `<base>` from the document's filename
without its extension, or from the established stage name. For example,
`sprint_E.2_analysis.md` gives `sprint_E.2_analysis`; a review of
`project-fit-assessment.md` gives `project-fit-assessment`. Append the following
suffixes to that base for round N:

- `<base>_review-<N>-prompt.md`: coordinator's outbound review prompt.
- `<base>_review-<N>.md`: original expert review.
- `<base>_review-<N>-response.md`: engineering response.
- `<base>_review-<N>-feedback-prompt.md`: outbound prompt requesting expert feedback.
- `<base>_review-<N>-feedback.md`: original expert reaction, if requested/supplied.
- `<base>_review-<N>-decisions.md`: actions, rationale, owners and closing conditions when decisions exist.

Keep one review/response/feedback exchange under one number. Number rounds
within the subject base and name the subject explicitly in each artifact
header so finding IDs remain unambiguous. Increment for a new review pass
against changed source or newly scoped findings. If clarification within the
same round is necessary, preserve successive messages as
`<base>_review-<N>-clarification-<K>-prompt.md`, `-clarification-<K>.md` (expert
reply) and `-clarification-<K>-response.md` (engineering answer). Use the next
unused K; never overwrite prior expert messages. Only create files actually
needed. Do not rename completed historical rounds solely for conformity unless
the user requests it. When renaming, keep original expert text byte-identical,
update maintained navigation/output paths, and record old-to-new names. Leave
captured ZIPs, manifests and raw receipts intact as historical evidence; explain
their historical names rather than silently rewriting their bytes or hashes.

Inspect existing rounds before choosing N. Continue a pending exchange; never silently replace a prompt the user may already have relayed. A material correction to an issued prompt uses a numbered clarification explaining what changed. A new pass is warranted when requested, when selected fixes are ready for independent recheck, or when a material change alters the reviewed boundary. Do not fabricate evidence of independent expert verification.

## Artifact header

Every newly authored round artifact begins with:

- **Round:** sprint ID, round number and artifact type.
- **Revision:** full SHA reviewed/answered, whether it matches the maintained baseline, and any separately supplied working patch.
- **Reviewer:** human/agent role and model/tool where known; state unknown rather than inventing identity.
- **Scope:** inputs read, checks executed and material exclusions.
- **Inputs:** links to prior round artifacts and relevant source/evidence.
- **Status table:** one row per finding with its current status before detailed discussion. For an initial prompt, state “No findings yet”; do not invent rows.

Ask the expert to use the header. If their supplied report omits it, preserve their original text and provide missing context/mappings in the response. Tables here are the explicit review-file convention; do not force them into other narrative project documents.

## Stable finding IDs

Use `R<N>-<severity><k>` where severity is H, M or L, for example `R1-H1` or `R2-M3`. Map any expert numbering once in the response, then retain it. A split finding keeps its ID with a suffix, such as `R1-M5a`. Re-raised findings keep their original IDs across rounds. Use those IDs in decisions and fix references rather than renumbering by the latest severity/order.

Each finding should identify severity, source location, impact, proposed correction and an acceptance check. Severity reflects the accepted phase and product boundary. Record source-inspected risks separately from reproduced defects.

## Finding statuses

| Status | Meaning and authority |
|---|---|
| `open` | Raised without an engineering answer. |
| `agreed`, `partly-agreed`, `disputed` | Engineering position, supported by evidence. |
| `selected`, `deferred`, `rejected` | Product Owner disposition; record owner, rationale and closing condition or deferral trigger. |
| `fixed@<sha>` | Correction committed; the agreed acceptance evidence is not yet complete. |
| `verified@<sha>` | Agreed acceptance evidence recorded for that revision. State whether this is engineering validation or an independent expert recheck. |
| `regressed@<sha>` | Previously verified behavior now fails, with evidence. |

Use one current status per finding in each status-changing artifact. Short SHAs may label statuses when unambiguous; the revision header carries the full SHA. A commit message alone does not establish fixed/verified. Expert agreement with a proposal is not implementation or Product Owner acceptance. Preserve earlier report/response status snapshots; maintain current dispositions in the decisions file and sprint assessment.

## Engineering response

For each finding, state the position, actual facts and limits, evidence links, proposed correction or explicit deferral, and an acceptance criterion. Correct errors in the report openly. End with **Checks performed**, including commands/outcomes or document checks and what was not run. Never convert a proposed test into a passed result. Link the response, feedback, decisions and maintained assessment bidirectionally where appropriate; preserve raw expert evidence.

## Decisions and closure

A selected correction names its finding ID, owner, why it matters now and evidence needed to close it. A deferral names its reason and trigger for reconsideration. A rejection gives rationale and evidence; reopen only on new evidence. In later review passes, first recheck earlier findings not verified/rejected, including whether deferral conditions still apply, before adding new findings. Label newly discovered regressions against previously verified findings explicitly.

Close a round only when all its findings are verified, deferred with reasons, or rejected. Do not create an empty closure artifact; record useful closure in the maintained assessment/decisions. No round status changes backlog assignments or sprint status. Use the project's normal routing for those changes. In a RUP project, existing documentation/handover controls (such as P8/P9) still apply; this skill replaces only the external-review procedure.
