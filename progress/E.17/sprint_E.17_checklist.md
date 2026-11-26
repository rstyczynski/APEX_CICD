# E.17 requirement-to-evidence checklist

[PBI-085](../../BACKLOG.md#pbi-085-reproduce-complete-native-delivery-on-a-clean-host) owns acceptance; [PLAN E.17](../../PLAN.md#sprint-e17---reproduce-complete-native-delivery-on-a-clean-host) adds the combined E.15/E.16 journey. The [SRS actor boundary](../../docs/srs.md#actors), FR-5 and NFR-5 apply to interpretation, ordering and tool compatibility. [Local P8/P9](../../RUPStrikesBack.patch/RUP_patch.md) and RUP manager Phases 4/5 own audit, tests, demonstration, presentation, commits and closure. [Source review](sprint_E.17_source_review.md) explains exactly what was observed and what remains unverified.

## R1 — Clean-host automated reproduction accepted

Mandatory source: amended PBI-085 and PLAN E.17, following the explicit [Product Owner decision of 2026-11-26](sprint_E.17_acceptance_amendment.md). Codex-driven automated reproduction satisfies E.17 without another external operator. Actual [run 45828709006](https://github.com/rstyczynski/APEX_CICD_E.17/actions/runs/45828709006), its [host receipt](tests/native-qualified/native-45828709006/host.json) and inspected immutable source establish a new Ubuntu job and fresh author/target databases without retained laboratory inputs. The uid=1001 runner remains an internal execution principal. The former operator-attribution acceptance blocker is resolved by the explicit amendment; broader UC-6/NFR-4 requirements and all remaining sprint gates remain applicable within their stated scope.

## R2 — Verified fresh private inputs and declared prerequisites

Mandatory source: PBI-085 description/test and PLAN E.17. The reviewed workflow declares tools, vendor payloads, digest/checksum pins, native container setup, job-private paths and cleanup. The executed source generates new random private values per run and registers masking before use. It reads no prepared-host record/settings. Actual schema/ORDS/APEX creation and authenticated browser access demonstrate use of those job inputs. Values are deliberately not retained. [Manual](user_manual.md) owns operating prerequisites; the historical regression boundary is explicitly separate.

## R3 — Verified Database/APEX/ORDS provisioning and application access

Mandatory source: PBI-085 test and PLAN E.17; FR-5 requires database-before-dependent-application order. All named provisioning steps pass in the real run. Native table installation/seeding precede the APEX import. Actual Chromium logs in as new LAB_USER and displays the native row, as recorded in [authenticated receipt](tests/native-qualified/native-45828709006/authenticated-access.json) and [capture](tests/native-qualified/native-45828709006/authenticated-application.png). This verifies the small native data-inspection fixture; it does not claim a release of every earlier product component.

## R4 — Verified native install, upgrade, repeat and retained data

Mandatory source: PBI-085 test and PLAN E.17. SQLcl PROJECT executes native 1.0.0 installation, 1.1.0 additive upgrade and identical repeat. Target SQL assertions retain the seeded row and upgraded EXTRA column. [Repeat output](tests/native-qualified/native-45828709006/repeat.log) reports zero new changesets/two previously run. Both qualified archive receipts and generated Git history are retained in [native evidence](tests/native-qualified/native-45828709006/). All inherited refusal cases pass before target mutation and the before/after observations agree. These are actual native operations, not synthetic migrations or a custom pipeline engine.

## R5 — Verified combined reviewed candidate journey

Mandatory source: PLAN E.17's combined E.15/E.16 journey. Fresh run 45819877026 validates candidate PR 1's reviewed bytes, actual Oracle greeting, application schema identity, private-table denial and denied workflow-token publication. Ordinary protected merge fails before validation and succeeds after exact-head trusted publication without admin bypass. Stale-review run 45820491077 rejects changed PR 2 bytes before SQL execution; ordinary merge remains refused. Candidate Actions are disabled and strict TrustedOracle protection applies to administrators. [Source review](sprint_E.17_source_review.md) and retained tests/ records identify actual runs, source and merge. The integration reader rechecks those authoritative observations; it does not infer them from E.15 history.

## R6 — Verified tool identities and scoped cleanup

Mandatory source: PBI-085 test and SRS NFR-5. Actual SQLcl is release 25.4.1.0/build 25.4.1.022.0618, matching native project metadata. Temurin 21.0.13+2, Node 22.23.5, pinned Playwright, APEX payload checksum, actual ORDS 25.3.0.r2671248 and the exact Oracle full-image digest are recorded in source/native job evidence. Native output/metadata checks precede PROJECT operations; the actual older SQLcl executable is refused. Cleanup removes private connection/configuration paths and all three owned containers; the job log and receipt show those actions. GitHub then decommissions its hosted VM. No private-value markers were found in retained text/job log/native archives, and no credential DDL was in those archives. This is not a claim of broader production NFR-4 completion.

## R7 — Five gates pass; full integration regression running

Mandatory source: PLAN Test/Regression and RUP manager Phase 4. From pinned source 33df904, A1/A2/A3 pass 1/1 each, B1 passes 16/16 and B2 18/18. Timestamped logs under tests/ identify exact commands/results. B3 is running unfiltered in the same isolated checkout. New remote hosted regression dispatches use E.17. Unit fixtures prove reader/refusal contracts only; A3 verifies actual hosted execution and source/archive bytes but does not establish another external operator. The separate-operator condition is resolved by the explicit R1 acceptance amendment, not by a unit-test claim.

## R8 — Documentation, live demonstration and final audit in progress

Mandatory source: RUP manager Phase 5 and local P8/P9, plus explicit Product Owner commit/final-push instructions. Setup/design/implementation/source review/manual/walkthrough and local checkpoint commits exist. Native run 45828709006 is a verified rehearsal; live workflow demonstration 45831994665 is repeating the same qualified source on a new host. A 19-slide private draft passes package/layout/font/import checks; final factual reconciliation, visual inspection and canonical presentation pair remain pending. Complete demonstration, final audit, recorded closure and final origin publication are not yet claimed.

## Implementation choices and limits

Hosted Ubuntu, the full Oracle image, AMD64 ORDS, native SYS setup through the image's supported resetPassword command, the small APEX report and Chromium observation are implementation choices. They do not add acceptance requirements. A capacity benchmark, production deployment, full earlier-component delivery or human study is not added to this sprint. R1 records the explicit Product Owner acceptance amendment; no runner is relabelled as an external actor. [Bug history](sprint_E.17_bugs.md) retains failed approaches and repairs without treating recoverable failures as external blockers.
