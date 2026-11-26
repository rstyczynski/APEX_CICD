# E.17 handover — in progress

## Scope and review entry point

[PBI-085](../../BACKLOG.md#pbi-085-reproduce-complete-native-delivery-on-a-clean-host) and [PLAN E.17](../../PLAN.md#sprint-e17---reproduce-complete-native-delivery-on-a-clean-host) define the independent clean-host native journey. The [walkthrough](sprint_E.17_increment_demo.md) is the end-to-end entry point; [manual](user_manual.md) owns prerequisites/recovery and [source review](sprint_E.17_source_review.md) binds actual source and evidence. The canonical PPTX is not yet finalized. No sprint acceptance or closure is recorded here.

## Preflight and rehearsal

Actual run 45828709006 at 5f135bd completes all 51 steps. It provisions fresh Database/APEX/ORDS, installs native 1.0.0, seeds data, imports/accesses the dependent APEX definition, upgrades to 1.1.0, repeats the archive and signs in through Chromium to the retained row. Native repeat applies zero new changesets/two already run. Refusal cases preserve observations; private paths and three owned containers are removed. The native job, input manifest, archives/receipts, generated Git history, target assertions and browser capture are retained under tests/native-qualified. The capture was visually inspected and shows authenticated lab_user and row 1's retained message. It is supporting evidence, not a claim that a saved image itself is a live demo.

Initial platform failures and supported repairs are explained in the bug record, source review and presentation draft. Those failed attempts are not acceptance. Dedicated A1/A2/A3 pass 1/1 each, B1 16/16 and B2 18/18; full B3 is running. The standalone fresh-hosted regression also passes with its dispatch routed to E.17. The explicit acceptance amendment governs operator attribution.

## Live developer-operated workflow demonstration

The developer dispatched the actual qualified workflow again as run 45831994665 through GitHub's native CLI, then followed its live native step states with `gh run watch --compact --exit-status`. Source, new host/private-input provisioning, actual native delivery and resulting application/data/cleanup outputs are the demonstrated product journey. Live watch output is retained under tests/. The completed terminal outcome is recorded below.

During an earlier live inspection, the browser access host was unavailable; the native Google Chrome interface successfully opened the actual E.17 Actions job and showed source revision, host preparation and individual named lifecycle steps. That inspection was intermediate; it did not establish a finished journey. No unobserved browser operation, Product Owner reaction, satisfaction or manual application step is asserted.

## Product Owner decision and current verification

The Product Owner explicitly accepts automated reproduction; the [acceptance amendment](sprint_E.17_acceptance_amendment.md) resolves the former attribution question without changing broader production requirements. No Product Owner satisfaction or additional reaction is invented. YOLO authorizes self-review of remaining delivery artifacts after verification.

Live run 45831994665 completed successfully in 13m44s, at the same immutable 5f135bd source. The developer followed native steps through provisioning, install, upgrade, repeat and refusal checks and inspected the successful final UI. [Run metadata](tests/live-demo-run.json), [full log](tests/live-demo-job.log), [retained artifacts](tests/live-demo/native-45831994665/cleanup.txt) and [independent result/source verification](tests/live-demo-verification.log) establish terminal behavior. Actual Chromium authenticated and observed the retained row before cleanup. Private inputs and owned containers were removed. This is a developer-operated automation demonstration; no manual remote browser login is claimed.

Full B3 regression remains in progress; final closure is not yet recorded.

## Screenshot evidence

The [local screenshot gallery](screenshots/index.html) provides original captures, captions, observed outcomes, requirement references and navigation. Capture gaps are explicitly labelled.
