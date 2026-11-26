# E.15 implementation — in progress

[Design](sprint_E.15_design.md) defines the experiment and [checklist](sprint_E.15_checklist.md) tracks outstanding acceptance. [Manual](user_manual.md) provides usage, prerequisites and recovery; [walkthrough](sprint_E.15_increment_demo.md) provides inspectable steps.

Dedicated remote repository https://github.com/rstyczynski/APEX_CICD_E.15 contains sanitized fixture commits 90b967d (initial), 53f1d13 (YAML repair) and 1a68f4d (private Oracle sentinel and publication challenge). Candidate PR 1 changes only the greeting expression. The workflow retrieves SQL by immutable event head and validator code by base revision, executes Oracle as candidate and has read-only GitHub contents authority. The current artifact is a partial prototype; no production or complete integrated boundary is claimed.

The initial workflow failed before jobs because a colon in the API header needed a YAML block scalar. actionlint identified line 38; revision 53f1d13 repairs it and dispatch then started successfully. This recoverable implementation failure is retained in GitHub run 45779197486. Hosted initialization remains under observation.

Material decisions: preserve existing scheduling edits, activate only E.15, and keep all retained credentials out of the sprint repository. No SQLcl PROJECT step is introduced, so this increment does not change approved SQLcl metadata or qualify native release operations. Read-only private-branch/ruleset probes both returned HTTP 403; a pending Product Owner choice determines the supported remedy.
