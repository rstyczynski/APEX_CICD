# E.16 operator reference

The [walkthrough](sprint_E.16_increment_demo.md) owns the end-to-end journey. [Design](sprint_E.16_design.md) owns mechanisms; [checklist](sprint_E.16_checklist.md) owns acceptance. The supported experiment uses dedicated disposable Oracle services, SQLcl 25.4.1.022.0618 and Java 21 on GitHub-hosted Ubuntu. No local database credential is required. GitHub CLI authentication needs access to the private sprint repository. The current native run passes; see the verification report for regression and closure state.

## Explain the workflow before invocation

The workflow downloads SQLcl from its versioned Oracle URL, verifies the pinned SHA-256, initializes two isolated Oracle services, then runs lifecycle.py. That script generates native project metadata, commits exported source and prepared release history in a job-private repository, stages and verifies changes, creates release archives and invokes PROJECT deploy only after provenance checks. Oracle assertions inspect the seeded row after upgrade and exact repeat. Evidence upload runs even after failure. GitHub service disposal removes the experiment databases. The workflow and full SQL currently live in the mirrored source; the walkthrough displays the complete significant SQL before invocation.

From a checkout root discovered with `git rev-parse --show-toplevel`, dispatch the hosted workflow:

```bash
gh workflow run native.yml --repo rstyczynski/APEX_CICD_E.16
gh run list --repo rstyczynski/APEX_CICD_E.16 --workflow native.yml --limit 5
```

Inspect the actual run and download its evidence before assessing success. Failed or cancelled runs are diagnostic evidence. Do not retry against production or retained laboratory targets. A fresh hosted run creates fresh disposable services. The current bounded table fixture does not establish complete APEX/ORDS delivery or independent clean-host reproduction.

## Complete native procedure

The [walkthrough](sprint_E.16_increment_demo.md) now includes the complete SQL, lifecycle explanation, expected retained row and failure branches. Use it with the editable presentation. For a failed hosted attempt, retain its uploaded result, inspect the first failed native step, repair the source and rerun with fresh services. Never replay these bootstrap operations against a retained target. `code` must be on PATH for the documented file viewer. Workflow dispatch requires GitHub authentication and Actions availability; pending infrastructure is not a passing run.
