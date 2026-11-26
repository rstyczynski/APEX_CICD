# E.15 blocker and remaining-requirement audit

## Final functional disposition

No assigned functional acceptance criterion remains externally blocked. [PBI-083](../../BACKLOG.md#pbi-083-validate-integrated-github-and-oracle-execution) owns the required ordinary merge and negative authority/freshness/isolation/cleanup outcomes. [The checklist](sprint_E.15_checklist.md) links actual evidence for each. All six required quality gates pass. Final documentation/presentation approval and lifecycle/commit publication are recorded by the handover, audit and closure records; no criterion is waived by this disposition.

## Original cross-candidate failure and the supported remedy

Exact unmet criterion at discovery: cross-candidate access/interrupted cleanup must not damage another run or authorize invalid merge. A candidate-owned same-repository workflow requested actions:write and cancelled run 45781363137 attempt 1; the actual attack log and target receipt are retained. Candidate-owned same-app check publication also succeeded. Read-only defaults and expected GitHub Actions identity alone could not satisfy the criterion.

Attempted alternatives and observed limits: private branch protection/rulesets returned HTTP 403 requiring plan/public visibility. The existing explicit repository configuration/publication authority allowed the sanitized public remedy, so that was resolved. Native owner review then blocked invalid merge but did not remove Actions cancellation authority. Push-path rules returned HTTP 422: public repositories cannot have those push rules and the source must be organization-owned. No organization was available to the authenticated account. A dedicated app/browser route was not completed: Chrome access was declined and no app installation consent was inferred.

The Product Owner explicitly authorized APEX_CICD_E.15-candidates. The self-fork request returned the original repository, so the authorized companion was created standalone with Actions disabled. Trusted validation now fetches immutable SQL as data and retains its execution credential outside candidate source. A real source-owned dispatch allocated zero jobs; an actual read-only hosted principal was refused companion publication with HTTP 403. The only configured human target writer is the trusted owner. This supported alternative resolves the assigned candidate-code boundary without requiring the unused app or another account.

Actual corrected-boundary evidence includes ordinary merges of companion PRs 1 and 3, stale base/head/report refusals, peer-run substitution refusal, active Oracle cancellation with explicit owned resource removal and successful peer completion, and a successful fresh recovery. These are real API/Oracle/native outcomes. The earlier unsafe architecture is not reclassified as passed.

## Recoverable verification failures — resolved

The first full integration attempt invalidated itself after executable sources changed. The next retry was interrupted. A later full run had 23 passes and one checker failure because a skipped PR-only publisher made the job count exceed one. The test assumption was fixed without relaxing mandatory Oracle success. Fresh focused and full frozen-source retries passed, including 24/24 full integration. All 253 executable scripts/tests match the qualified snapshot. Missing implementation and failed checks were resolved rather than called external blockers.

## Retained metadata and scope limits

The harmless disabled dispatch remains zero-job metadata: cancellation reported completed, force-cancel returned HTTP 409 not yet queued, and deletion returned HTTP 403. No compute resource was allocated; actual Oracle cleanup is separately proven. Removing all CI history is not the accepted resource-cleanup claim. Actions remains disabled and is checked before publication/merge.

The experiment has a trusted prepared operator and a bounded SQL candidate. Organization-wide multi-user IAM, hostile administrators, native release delivery, an independent clean host and capacity recommendations remain outside this item's verified scope. Their existing requirements/backlog assignments are unchanged. E.16/PBI-084, E.17/PBI-085 and E.18/PBI-086 remain planned. No additional access, unanswered permission or external change is needed to close the assigned E.15 outcomes after final document audit.
