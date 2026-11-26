# E.15 remaining-requirement audit

[PBI-083](../../BACKLOG.md#pbi-083-validate-integrated-github-and-oracle-execution) requires the integrated boundary to prevent invalid merge or damage to another run from stale evidence, unauthorized publication, cross-candidate access and interrupted cleanup. [PLAN](../../PLAN.md#sprint-e15---validate-integrated-github-and-oracle-execution) requires all three test/regression levels. [Checklist](sprint_E.15_checklist.md) owns the current outcome of every criterion.

## Cross-candidate authority — failed, remedy pending scope decision

The actual untrusted-candidate workflow requested actions:write and invoked `gh api --method POST repos/rstyczynski/APEX_CICD_E.15/actions/runs/45781363137/cancel`. Run 45781496510 succeeded; target run 45781363137 attempt 1 was cancelled. [Exact execution log](tests/cross-candidate-attack.log) and [run receipt](tests/attacked-candidate.json) retain the observation. This is a real hosted failure, not injected policy data. The accepted run was subsequently rerun successfully; that recovery does not negate the interference.

Separate Oracle services and loopback binding protect database resources but cannot limit repository-wide Actions API authority. Read-only defaults are not a maximum: a branch-owned workflow requested write permissions successfully. A dedicated publisher app would separate check issuance but would not alone prevent this cancellation. Code-owner review mitigates unauthorized merge approval but does not protect running jobs.

Supported alternatives examined: protected branches and strict expected-app checks are enabled after resolving the initial private-plan limitation through sanitized public visibility. Actual same-app spoofing succeeded. Native code-owner review was then added and ordinary invalid merge refused; an independently reviewed bot-authored candidate reached ordinary merge. Push path restrictions were attempted using `gh api --method POST repos/rstyczynski/APEX_CICD_E.15/rulesets`; HTTP 422 states that public repositories cannot have push rules and only organization-owned repositories can have them. The authenticated account has no available organizations; the other configured account has invalid authentication. A self-fork request using the existing repository name returned that same non-fork repository, not a separate candidate boundary. No successful companion-fork arrangement is claimed.

A companion candidate fork with Actions disabled would allow candidate source to remain separate from trusted validation authority; its API behavior and isolation still require implementation and real tests. The explicit temporary-repository grant names APEX_CICD_E.15. A narrow scope extension for APEX_CICD_E.15-candidates is pending; no authorization is inferred from silence. If that arrangement is unsupported, an independently owned fork or restricted source-proposer identity must be supplied or separately authorized. This is the exact next external decision, not a claim that every technical alternative has already failed.

## Other unfinished acceptance

Head/base/report freshness: mechanisms exist, but the complete required negative journey has not been verified under a corrected authority boundary. Completing it is pending the boundary remedy and new real evidence; current successful positive checks do not substitute.

Interrupted cleanup: actual interrupted initialization and successful retry exist, but complete noninterference after cleanup remains unverified under corrected authority. It must be executed after the boundary is fixed.

Full regression: initial integration run invalidated its result because new executable test files were introduced during execution. The following retry was interrupted. The current frozen-source run is independent work in progress, not an external blocker. Missing results will be resolved before final reporting.

Documentation, presentation, live demonstration, audit and closure: current materials are being reconciled to the actual failures and ordinary merge. The final integrated handover and closure depend on verified unresolved acceptance criteria. Documents and commits can preserve partial work but cannot satisfy those criteria. PLAN stays Progress/YOLO and PBI-083 stays under construction.

Browser/app access: Chrome computer-use permission was declined and no app installation was performed. The earlier app request is not approved. App creation is not treated as the only remedy; the companion-boundary alternative is being evaluated through the pending scope question.
