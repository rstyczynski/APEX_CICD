# E.13 publication destination correction

## Product Owner direction

The Product Owner clarified: APEX_CICD_E.13 is only for experiments in this sprint; actual progress must go to APEX_CICD. This supersedes the earlier interpretation that the sprint-specific experiment repository was the delivery destination. Publish committed project progress to the existing [APEX_CICD origin](https://github.com/rstyczynski/APEX_CICD), main branch. Keep [APEX_CICD_E.13](https://github.com/rstyczynski/APEX_CICD_E.13) reserved for experiments.

## Historical rejected attempt

After local closure commit ec4e6bf, the requested command was `git push https://github.com/rstyczynski/APEX_CICD_E.13.git HEAD:main`. The permission tool refused process creation with `Rejected("rejected by user")`. No push process ran. Read-only inspection confirmed the private experiment repository had no default branch. No retry to that destination is authorized by the corrected direction.

## Corrected publication scope

Publish the committed project history, including implementation f5bc924, closure ec4e6bf, historical boundary record 87d6e33 and this documentation correction, to origin/main. The origin also lacks earlier local E.5–E.12 progress; normal fast-forward publication includes that history. Leave unrelated uncommitted .codex-cli changes outside the commit. Preserve both configured remotes and use no force push.

The [closure](sprint_E.13_closure.md), [handover](sprint_E.13_handover.md), [requirement checklist](sprint_E.13_remaining_work.md) and [documentation audit](sprint_E.13_documentation_audit.md) carry this correction. Technical acceptance and local lifecycle closure are unchanged. Remote publication is verified by comparing origin/main with the resulting local commit after push.
