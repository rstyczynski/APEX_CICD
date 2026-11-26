# E.18 handover — verified increment

The [complete walkthrough](sprint_E.18_increment_demo.md) leads through prerequisites, complete SQL sources before dispatch, actual Actions phases, user-visible outcomes and recovery. The [25-slide presentation](sprint_E.18_increment_demo.pptx), [manual](user_manual.md), [offline gallery](screenshots/index.html), [capture index](screenshots/evidence-index.md), [report](capacity_report.md) and [requirement checklist](sprint_E.18_checklist.md) provide the delivery package. Lifecycle closure is recorded separately after final audit.

## Delivered result and limits

PBI-086 has eight successful, source-identical measured jobs: cold/warm archive downloads × one/two runner slots × two replicas. The complete native E.17 workload is retained, with five real backend cases in each job. Feedback, queue, individual phases and sampled resources are reported with medians and nearest-rank p95. Two samples make p95 the observed maximum. Hardware/JDK differences, provider-layer warmth and overlapping cohorts prevent a causal cache or production-tail claim.

Recommend two independently isolated slots of the measured four-CPU, approximately 16-GiB-class shape for a two-candidate batch. Cold batch completion changes from 22.6 to 13.1 minutes and warm from 23.7 to 11.1 minutes. Immutable verified archive caching is optional: acquisition plus cache overhead differs by only 2–3.5 seconds in this cohort. Fresh databases, mandatory validation and cleanup remain in every sample. No production policy, cost qualification or shared-physical-host packing decision is made.

## Actual live journey

The developer dispatched run 45848145737 in [APEX_CICD_E.18](https://github.com/rstyczynski/APEX_CICD_E.18/actions/runs/45848145737) at screenshot revision 920b1c4 and opened Actions while both replicas ran. Native processing completed and the refreshed page showed Success for both. Actual browser execution captured blank APEX login controls, entered job-private inputs, activated Sign In and waited for the authenticated retained row. Captures 06–09 preserve the visible transitions; [live verification](tests/live-demo-verification.log) checks source/run identities, five backend cases, native install/upgrade/repeat/refusal, retained data, real authentication and cleanup. These are separate live observations, excluded from frozen capacity-v1 timing samples.

Population run 45846157988 passed as rehearsal/cache population and is excluded from warm statistics. The real installer ownership and SYS invoker-rights failures, their repairs and fresh successful reruns remain in the [bug record](sprint_E.18_bugs.md). The demonstration explains these failures and the small-sample limit. No Product Owner login, reaction, satisfaction or participation is invented. YOLO authorizes technical self-review without a routine confirmation gate.

## Verification and technical review

All six gates pass: A1/A2/A3 1/1 each, B1 17/17, B2 19/19, B3 27/27. The [test record](sprint_E.18_tests.md) distinguishes actual fresh hosted/local execution from historical receipt revalidation and synthetic arithmetic contracts. Regression-generated outputs are preserved within E.18, with historical tracked evidence restored byte for byte.

All 25 slides were rendered and inspected, and changed slides/ending rechecked. [Native PowerPoint QA](tests/presentation-verification.md) opened, edited, resized, saved and reopened a disposable chart copy; numeric data remained equivalent within 1e-12-minute serialization tolerance. The canonical file was not edited by Office. [Gallery QA](tests/gallery-verification.md) verifies actual offline browser rendering and navigation, including boundary wrapping, full images and evidence links. Static checks resolve local targets and synchronize full SQL disclosures.

Codex acts as developer and documentor. The technical review accepts the measured scope and handover usability subject to the final recorded P8 audit, package receipt and closure commit. There is no outstanding mandatory acceptance criterion or external blocker. [Documentation wrap-up](sprint_E.18_documentation.md), [audit](sprint_E.18_documentation_audit.md) and [closure](sprint_E.18_closure.md) record final decisions; PBI-087 stays Planned in E.19.
