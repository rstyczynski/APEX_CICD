# E.4 design — Round 1 independent feedback

**Round:** Sprint E.4 design, round 1, focused expert feedback.
**Revision:** Corrected source `0ad508b6e872ca500c5ac92c6b60d555fc154cb4`, matching local HEAD; original reviewed source `0eb39eb7b42b08092e491820fbb29f4b30920e12`. Repository: https://github.com/rstyczynski/APEX_CICD.git, `main`. Publication is reported by the supplied coordinator prompt; this recheck inspected the exact local commit, without independently querying the remote. No working design patch was reviewed.
**Reviewer:** Same dedicated independent E.4 Codex reviewer, requested as Astra; actual runtime model identity is not independently exposed.
**Scope:** Textual closing-condition recheck of R1-M1/R1-M2 only. No runtime acceptance, implementation approval, production fencing or PBI-056 assessment.
**Inputs:** [Original report](sprint_E.4_design_review-1.md), [engineering response](sprint_E.4_design_review-1-response.md), [feedback prompt](sprint_E.4_design_review-1-feedback-prompt.md), corrected [design](sprint_E.4_design.md) and [audit](sprint_E.4_documentation_audit.md). Response and feedback prompt were supplied working coordination files outside the corrected source commit; they were not treated as committed design.

| Finding | Response assessment | Current status | Verification boundary |
| --- | --- | --- | --- |
| R1-M1 | Accept | verified@0ad508b6 | Independent textual design correction only |
| R1-M2 | Accept | verified@0ad508b6 | Independent textual design correction only |

## Verdict

**The corrected design is ready for Product Owner review and design approval.** Both round-1 design-level closing conditions are met. No further correction is requested for these findings, and no new finding candidate is raised in this focused recheck. This is independent review advice, not Product Owner acceptance or permission to begin implementation.

The findings concerned missing or contradictory experiment instructions. Their textual verification does not establish that the planned native reconciliation, deployment, preservation or repeat checks pass. Those remain execution gates after approval; inability to establish a trusted baseline must still block PBI-042.

## R1-M1 — Accept; design closing condition met

The corrected [Trusted baseline qualification](sprint_E.4_design.md#trusted-baseline-qualification) section explicitly rejects source-label matching and the first live checksum as sufficient authority. It provides two bounded entry paths: qualified retained checksum evidence, or read-only reconciliation against the APEX source installed by the verified accepted archive. The latter preserves raw source/diffs, requires explanations tied to mappings and actual identity, and blocks unknown differences without reinstalling, resetting or adopting live content.

The approved baseline persists between attempts and binds source/archive, target, profile and availability state. Two unchanged reads establish stability only after source reconciliation. Revised [IT-3](sprint_E.4_design.md#it-3--unexported-work-preserved-pbi-042) adds rejection of an edit present before baseline qualification and retains the post-baseline pending-edit case. These changes address the original gap directly.

The engineering response accurately limits its claim to a specified safe procedure. Native export comparability and the explanation of actual target-specific differences are still to be demonstrated. Failure to establish equivalence is an explicit blocked outcome, not a reason to weaken the check.

## R1-M2 — Accept; design closing condition met

The corrected [Availability, deployment and receipt lifecycle](sprint_E.4_design.md#availability-deployment-and-receipt-lifecycle) separates coordinated participant exclusion from technical availability and explicitly recognizes that import can restore AVAILABLE. It specifies observation and renewed restriction, read-only verification before publication, and separation of the inherited combined acceptance/publication script after approval.

Receipt finalization follows restoration to the selected AVAILABLE state and two checksum observations in that state. Subsequent admission/repeat uses that receipt. Rehearsal must observe fingerprints across status transitions rather than assume status neutrality or normalize unexplained differences away. Revised [IT-4](sprint_E.4_design.md#it-4--combined-synchronization-and-repeat-both-pbis) carries these requirements into the planned evidence.

Failure instructions now require observing actual status, reporting whether a supported restriction attempt succeeds, maintaining coordinated exclusion and withholding success/readiness claims. They no longer infer continuous unavailability from a failed deployment. This closes the contradiction without introducing an import-spanning lock or expanding the selected experiment.

## Checks and limitations

Inspected working status and confirmed local HEAD equals the requested correction SHA. Read the corrected design directly with `git show` at that full SHA, inspected the audit/setup diff from the original baseline, and compared both corrections with the original findings and supplied engineering response. The response is intentionally outside the source commit and was read from its supplied working file after confirming that distinction.

No database/native commands, browser tests, workflows, source edits, commits, pushes or cross-chat messages were performed. Only this feedback file was written. Prior review text remains unchanged. All E.4 runtime cases remain unrun; the Product Owner retains the design decision and subsequent implementation authorization.
