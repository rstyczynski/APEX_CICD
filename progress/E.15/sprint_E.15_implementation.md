# E.15 implementation — in progress

[Design](sprint_E.15_design.md) defines the experiment and [checklist](sprint_E.15_checklist.md) tracks outstanding acceptance. [Manual](user_manual.md) provides usage, prerequisites and recovery; [walkthrough](sprint_E.15_increment_demo.md) provides inspectable steps.

Dedicated remote repository https://github.com/rstyczynski/APEX_CICD_E.15 contains sanitized fixture commits 90b967d (initial), 53f1d13 (YAML repair) and 1a68f4d (private Oracle sentinel and publication challenge). Candidate PR 1 changes only the greeting expression. The workflow retrieves SQL by immutable event head and validator code by base revision, executes Oracle as candidate and has read-only GitHub contents authority. The current artifact is a partial prototype; no production or complete integrated boundary is claimed.

The initial workflow failed before jobs because a colon in the API header needed a YAML block scalar. actionlint identified line 38; revision 53f1d13 repairs it and dispatch then started successfully. This recoverable implementation failure is retained in GitHub run 45779197486. Hosted initialization remains under observation.

Material decisions: preserve existing scheduling edits, activate only E.15, and keep all retained credentials out of the sprint repository. No SQLcl PROJECT step is introduced, so this increment does not change approved SQLcl metadata or qualify native release operations. Read-only private-branch/ruleset probes both returned HTTP 403; a pending Product Owner choice determines the supported remedy.

## Verified hosted results and unresolved authority

The private visibility limitation was resolved through PBI-083's explicit configuration/publication authority. Native branch protection now enforces strict Integrated checking, administrator enforcement, code-owner review and stale-review dismissal. A controlled setup push used temporary administrator exemption to install policy; it is explicitly not an ordinary acceptance merge. The later PR 4 completed real Oracle Testing, exact-byte Review, authenticated owner approval and ordinary merge at 8ee003ad9f45ae62d5fe0d1a0bb389e311c1b27a without --admin.

The first report-bound run checked out event base content without the newly added report; it failed FileNotFoundError. Trusted code selection was corrected to github.sha. Candidate workflow publication using the same GitHub Actions app succeeded, so app identity alone was insufficient. Code-owner approval supplies a separate native review identity, and invalid ordinary merge was refused. This mitigation does not prevent Actions API interference: a candidate-owned workflow cancelled the other candidate's first attempt. The real positive rerun passed, but the isolation criterion remains failed. [Remaining-requirement audit](sprint_E.15_blockers.md) records exact evidence, supported alternatives and the pending companion-repository scope decision. No dedicated app or companion fork has been created by assumption.

The accepted run uses the observed Oracle image digest and a loopback-only service port. It is an isolated greeting fixture, not the complete APEX delivery pipeline and not an E.16 native release proof. No SQLcl PROJECT metadata was changed.
