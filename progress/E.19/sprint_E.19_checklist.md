# E.19 requirement-to-evidence checklist

## Acceptance authority

[BACKLOG PBI-087](../../BACKLOG.md#pbi-087-provide-javascript-support-checks-as-catalogued-github-actions) owns migration/catalogue/refusal acceptance. [PLAN E.19](../../PLAN.md#sprint-e19---validate-catalogued-javascript-support-actions) adds equivalent Python comparison, conditional official OCI SDK use and all three test/regression levels. The Product Owner's archived execution instructions add screenshots/gallery, chat snapshots, demonstration/presentation, commits/publication and truthful closure. [Local method P8/P9](../../RUPStrikesBack.patch/RUP_patch.md) governs audits and developer-led handover. These sources are acceptance requirements; implementation choices below do not add stricter criteria.

## PBI-087.1 — inventory and catalogue

Verified. [Complete inventory/dispositions](sprint_E.19_inventory.md) and [line-numbered workflow scan](tests/workflow-inventory.json) cover hidden delivery workflows, standalone/inline Python checks and historical/application/telemetry code. Five migrated checks have purpose, required inputs, validated output, failure behavior, examples and actual workflow wiring in the [catalogue](../../sprint-work/E.19/CATALOGUE.md). Historical source/evidence is preserved. Root examples contain no Python execution to migrate. Separate application testing and measurement baseline retain explicit Python dispositions.

## PBI-087.2 — actual reusable guards and native safety

Verified. Five native Node24 action entrypoints use no Python installation/execution or npm package. Native and acceptance workflow source checks pass; [final real matrix](tests/qualified/45876173032.json) invokes 24 actions, five valid and nineteen refusing missing/malformed/mismatched inputs. Every expected refusal has a skipped mutation sentinel and successful assertion. The matrix is real GitHub Actions execution over synthetic file fixtures; it does not substitute for native target evidence.

[Actual native run](tests/qualified/45874462191.json) executes SQLcl PROJECT export/stage/verify/release/package/install, additive upgrade and repeat using release 25.4.1.0/build 25.4.1.022.0618 and matching generated project metadata. Actual archive/source/tool/substituted-byte mismatches reject; before/after target observations match. Native provenance actions run before deployments. [Native success receipt](tests/qualified/native-45874462191/success.json), archives and [source applicability audit](tests/source-applicability.log) establish exact version/byte scope. No native lifecycle operation was replaced by a custom controller.

[Real PR trial](tests/real-candidate-success.json) exercises actual candidate API metadata, trusted Review binding and Oracle application isolation. Its HTTP 403 failure was repaired through scoped PR-read permission; no failed trial is accepted as success. [Optimization regression](tests/optimization-check.log) demonstrates the original -O bypass and unconditional replacement refusal on the same bytes.

## PBI-087.3 — comparison, regression and handover

Verified functional outcomes. [Accepted comparison](comparison_report.md) and [raw paired metadata](tests/timing-paired-run.json) use both runtimes on each of two hosts, reversed order, identical five-helper inputs, actual Node/Python/image versions, first-invocation n=2 and repeated n=20 per runtime. Availability/setup, helper execution and total workflow times are separate. Python was preinstalled; zero installation cost is claimed for either runtime. JavaScript was slower in the measured helper workload. Dependencies/setup/maintenance and cold/warm/provider limits are explicit. Unequal-image and initial three-helper cohorts are excluded from the accepted comparison.

[All six gates](sprint_E.19_tests.md) pass: A1/A2/A3 1/1 each, B1 18/18, B2 20/20, B3 28/28. Full integration exit zero includes stable executable source and private cleanup. [Historical preservation](tests/regression-replay/restoration-receipt.txt) retains current outputs under E.19 without rewriting earlier sprint records. Historical receipt revalidation is distinguished from fresh hosted/native execution.

## Conditional OCI requirement

Satisfied within selected scope: no OCI secrets/Object Storage/API interaction is needed. No OCI feature is added. The inventory and architecture retain the mandatory official Oracle JavaScript/TypeScript SDK rule for any later selected OCI interaction; public APEX software distribution download is not an OCI API operation.

## Execution and method requirements

[Gallery](screenshots/index.html) contains actual application/browser captures, readable derivatives, captions, requirements/evidence links, thumbnails, previous/next and full-resolution links. [Index](screenshots/evidence-index.md) records source/run provenance and unavailable earlier dispatch/expanded-error captures without inventing UI. [Actual rendering/navigation](tests/gallery-verification.md), direct image inspection and [local-link validation](tests/handover-links.log) are separate evidence. Actual blank APEX login and post-Sign-In retained row were captured during the hosted interaction without private values.

[Presentation walkthrough](sprint_E.19_increment_demo.md), matching PPTX, [manual](user_manual.md), [developer demonstration](tests/live-guard-demo.log), [slide review](tests/slide-verification.md) and [handover](sprint_E.19_handover.md) document inputs/actions/results, native SQL disclosures, failure/recovery, measured limits and decisions. The actual guard was operated live; prior logs/slides alone are not claimed as that demonstration. Product Owner reaction is not invented. YOLO self-review uses the existing delegation.

[Chat index](chat/index.md) links timestamped native JSONL snapshots and readable companions, includes the first continuation archive, corrects its initial context label and records writer lag/redactions. Exports preserve accessible records rather than reconstructing turns. [Documentation audit](sprint_E.19_documentation_audit.md), local commits and [closure](sprint_E.19_closure.md) own final wrap-up/publication.

## Implementation choices and remaining scope

Native node24 actions, shared CommonJS, regular-file checks, explicit exceptions, synthetic sentinel fixtures and paired-host measurement are implementation choices. They do not add mandatory product criteria. No unfinished assigned requirement or external blocker remains once the recorded closure transaction is committed. Production rollout, larger timing cohorts, Lifecycle Architecture acceptance and new OCI features are separate future decisions, not invented requirements or silently registered backlog items.
