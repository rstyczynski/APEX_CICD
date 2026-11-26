# E.18 requirement-to-evidence checklist

## Authority and current result

[PBI-086](../../BACKLOG.md#pbi-086-measure-complete-pipeline-feedback-and-runner-capacity) owns acceptance. [PLAN](../../PLAN.md#sprint-e18---measure-complete-pipeline-feedback-and-runner-capacity) assigns this single item and requires smoke, unit and integration at both new-code and full-regression levels. [SRS](../../docs/srs.md#actors) owns actors/boundary; [architecture](../../docs/architecture.md#native-technology-responsibilities) owns native responsibilities. [README](../../README.md) provides project orientation.

The eight-sample measurement experiment is verified. All six gates, final handover review and P8 audit pass; closure is recorded after qualified increment b454fc5. No external blocker is claimed. [Report](capacity_report.md), [verification](sprint_E.18_tests.md), [implementation](sprint_E.18_implementation.md) and [handover](sprint_E.18_handover.md) own their respective detailed records.

## Mandatory acceptance

- [x] R18-1 — Complete integrated JDK / qualified SQLcl / utPLSQL / Oracle workload on E.17 baseline. Four actual runs, two successful replicas each: cold serial 45846143379, cold concurrent 45846150456, warm serial 45848134832, warm concurrent 45848140354. All use source aea3a771cac687fa32ac09d24faf6d2d55bd2342. A3 verifies native installation/upgrade/repeat, all refusal checks, five backend cases, real authenticated APEX/ORDS and cleanup; [raw receipts](tests/measurements/capacity-results.json) bind source/run identities. Source smoke checks every named E.17 stage remains present and the existing backend fixtures remain unchanged.
- [x] R18-2 — Declared counts, cold/warm phase timings, median/p95 feedback and queue delay. [Report](capacity_report.md) gives n=2 per cell, eight observations, exact phase distributions and raw creation/start wait intervals. Nearest-rank p95 is explicitly the maximum at this sample count. Physical coldness and pure infrastructure queue delay are not claimed.
- [x] R18-3 — Resource use under serial and concurrent workloads, preserving isolation. Actual API intervals establish zero serial overlap and positive concurrent overlap. Per-job five-second counters record host CPU, available memory and root-disk free space. [Cohort audit](tests/cohort-isolation.log) verifies eight distinct runner execution identities, sixteen author/target namespaces, bound receipts and private cleanup. A repeated hostname in nonoverlapping jobs is retained as a limit, not treated as physical identity.
- [x] R18-4 — Justified capacity/cache recommendation with explicit limits and unchanged mandatory validation. [Report recommendation](capacity_report.md#capacity-and-caching-recommendation) retains the measured four-logical-CPU host shape and two isolated slots for a two-candidate batch. Cache remains optional: observed acquisition-plus-cache differences are 2.0–3.5 seconds, with hardware/JDK/sample-size confounding. Fresh databases and every native validation remain required.

## Mandatory delivery controls

Authority: the Product Owner execution request, [RUP manager](../../RUPStrikesBack/.claude/commands/rup-manager.md), [test profile](../../docs/test-profile.md#e18-pipeline-capacity-experiment) and [local P8/P9](../../RUPStrikesBack.patch/RUP_patch.md).

- [x] D18-1 — All new and full regression gates, final audit and scoped completion commit. A1/A2/A3 pass 1/1 each; B1 passes 17/17; B2 passes 19/19. B3 passes 27/27 with source stability and scoped cleanup. P8 audit passes; checkpoint commits d4bc918 and 54bc0d2 remain historical partial evidence. The audited scoped completion commit precedes lifecycle closure.
- [x] D18-2 — Actual live pipeline demonstration. Run 45848145737 at separate screenshot revision 920b1c4 passes both replicas. [Verification](tests/live-demo-verification.log) checks real native archives, retained data, five backend cases, blank login capture, actual authentication and cleanup. The developer opened the running workflow and refreshed its successful outcome. No manual Product Owner login or reaction is inferred.
- [x] D18-3 — Complete walkthrough/manual, inspected PPTX pair and technical handover review. All 25 slides and revisions are visually inspected; native PowerPoint edit/resize/save/reopen and numeric preservation checks pass. Documentation and metadata are reconciled in the P8 audit.
- [x] D18-4 — Legible contemporaneous captures and offline gallery with working thumbnails, previous/next, full images and evidence links. [Gallery](screenshots/index.html) and [complete capture index](screenshots/evidence-index.md) preserve admitted views and explicitly excluded quality attempts. Actual browser navigation passes for thumbnail/next/previous/full image; final reload, sixteen-scenario overview, boundary wraparound and evidence links also pass in native Chrome.
- [x] D18-5 — Recorded closure after every required outcome is verified, local commits and final origin push. The canonical close procedure records PLAN E.18 Done/YOLO and board E.18/PBI-086 Done after b454fc5. The scoped closure commit and authorized origin push finish the delivery transaction.

## Implementation choices and measurement limits

Two replicas per cell, native hosted ubuntu-24.04 jobs, max-parallel one/two, dependency-only caching, source freeze and five-second observation are implementation choices, not new acceptance requirements. The existing five-case backend suite represents this bounded laboratory workload. Cache population and the screenshot-only live revision are excluded from the eight timing samples.

Production tail estimates, shared-physical-host packing, cost, human review/merge lead time and provider-layer warmth are outside this experiment. They are not waived accepted requirements. The [design](sprint_E.18_design.md) and report distinguish those limits from required, verified behavior.
