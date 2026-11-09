# E.4 — Test results

## Authority, environment and outcome

The [accepted design](sprint_E.4_design.md) owns SM-1 and IT-1–IT-4. The
[implementation](sprint_E.4_implementation.md) explains fixes and actual participants;
[the walkthrough](sprint_E.4_increment_demo.md) provides commands, complete helper SQL
and expected results. The selected pipeline smoke regression is governed by
[the test profile](../../docs/test-profile.md). No unit suite is selected for this
native, operator-controlled Elaboration experiment.

All five scenario outcomes are demonstrated, with IT-3's restoration rule explicitly
amended by the Product Owner after its original exact-checksum hypothesis failed.
This is not an unchanged 5/5 pass claim. Independent native processes, real GitHub
PRs, actual Oracle operations and browser observations are distinct evidence types.
One Codex operator simulated the roles; three concurrent human authors are not claimed.

## SM-1 — Identity and native integrity: PASS

Before native operations the checked-out .dbtools version 25.4.1.0 was compared with
actual SQLcl build 25.4.1.022.0618. The ZIP pin is recorded in implementation; Java 21,
Oracle Free 23.26.3.0.0, APEX 24.2 and ORDS 25.3 were used. Each fixture's effective
USER/service was qualified. The native helper rejects positive Errors summaries even
when SQLcl exits zero. Baseline and post-resolution source/snapshot qualification,
native numbered freeze and clean-source packaging passed. APEX-only stage/verify
reports one no-soft-object warning; it is not an unresolved verification error.

The shared [archive receipt](tests/release-artifact.json) binds commit
`e0f60ff5efc6905c3b6a4c0e7a7a79a6b0134b0c`, tag v1.0.7 and SHA-256
`27541bed6550c9f2dcfb36aeabd5e903bfe09a475fda0b0ec1972aa8ad9a1535`.
[Native frozen verification](tests/frozen-native-verify.log),
[release](tests/native-release.log) and [package](tests/package.log) are current E.4
runtime evidence. Historical E.3 readers are not substituted for these results.

## IT-1 — Independent contributions and selective release: PASS

[Parallel provenance](tests/parallel-contributions.json) records E4A/E4B/E4C,
separate checkouts/homes, common accepted developer start, original source/stage
commits and 24.84 seconds of overall author-worker overlap, including non-SQLcl
work. The individual native receipts show 14.757295 seconds of three-way capture
overlap and 4.155229 seconds of three-way stage/verify overlap. Individual process receipts
record real PIDs and intervals. The late ps snapshot did not capture those processes
and is not concurrency proof. Each original source diff contains only its own edit.

Later main advanced through PR #7. The manager created and announced
release-e4-candidate at that later SHA in issue #8. A/C opted in via PRs #9/#10;
manager admission followed source/dependency/check review. B remained unsubmitted
and intact. C's actual conflict log, qualified native reconstruction and fresh
restage/verify show resolution preserving A/C. The corrected C head passed check
run 42621680105 before merge. PR #11 promoted the validated candidate. Version PR
#6's checked head selected 1.0.7. See github-pr-*.json and release-branch.json.

Source, distribution and ZIP inspection proves inherited baseline and selected A/C,
no B label or B stage member. B's original head remains
ed9fe37bbebe30306ce91e981da9b5565b44c5c5 locally and remotely with a clean checkout.
Browser final observations corroborate installed A/C and the baseline Hello label.
Deferred B's later delivery is documented, not executed in this release.

## IT-2 — Stale source refused: PASS

[The refusal](tests/it2-refusal.json) records requested old accepted source versus
selected 1.0.7 source, no deployment invocation, identical before/after live checksum,
identical private all-field data snapshots and unchanged prior receipt hash.
This is an operator-enforced admission decision, not a claim of atomic stale-worker
protection. A failed connection was not counted as a refusal pass.

## IT-3 — Pending work preserved: PASS with approved recovery correction

Before any trusted checksum existed, a saved Home-title edit blocked full-source
qualification and remained intact. [IT-3a](tests/it3a-refusal.json) records no baseline
creation/no deployment and unchanged business fields. Restoring only the title,
reviewing the complete mapped-reference diff and obtaining two identical readings
established the initial baseline. The reference came from the verified previously
installed archive, not the current target export adopted as authority.

After qualification, a second saved title caused checksum mismatch and refusal.
[IT-3b](tests/it3b-refusal.json) records preserved edit, data and prior receipt.
Restoring the exact title did not restore its original checksum. The complete
[raw source difference](tests/postbaseline-restoration.diff) is solely application
p_version_scn 6207684→6208968. The Product Owner explicitly approved **reviewed
counter-only recovery**. Full-source equality except that exact field, all-field
preservation and two identical new readings produced
[the recovery receipt](tests/trusted-recovered-baseline.json). No unknown difference
was ignored and no general rebaselining mechanism was introduced.

## IT-4 — Selected synchronization and safe repeat: PASS

The first native deployment ran 1 changeset, with 22 previously applied. The repeat
ran 0 and found 23 previously applied. Both native acceptance calls verified readiness,
A's header, C's region, baseline Hello, B absence and a real APEX session as VERIFIER.
Every retained business field compared equal before publication and after browser
inspection; raw snapshots remain private.

[First lifecycle](tests/sync-lifecycle.json) observed Available → Restricted →
Available immediately after import → Restricted → Available. [Repeat lifecycle](tests/repeat-lifecycle.json)
observed Available → Restricted → Restricted after no-op deploy → Restricted →
Available. Thus import availability is measured, not assumed. Native status operations
also change checksums/counters; restoring a status is not checksum-neutral. Final
receipts were written only after acceptance, data comparison and two matching reads
in restored Available state. Repeat admission used the first finalized receipt.

[First receipt](tests/sync-receipt.json) and [repeat receipt](tests/repeat-receipt.json)
bind identical source/archive bytes. The final complete source comparison with a
native mapped reference has only exporter/instance comments and generated version
counter differences; see [final reconciliation](tests/final-reconciliation.json).
The checksum is SH256:lC3Z66l3GpaopFf/fj5VddcsUPaC61O57kzlWFdj6SQ=.

The Product Owner authorized temporary developer access and reserved central DEV.
[Cleanup](tests/cleanup.json) and [native counts](tests/temporary-access-cleanup.log)
confirm E4_VERIFY and E4_SYNC removed and target Available. Retained LAB_USER and
other targets remain unchanged. The coordinated reservation was then released.

## Browser validation

[Browser receipt](tests/browser-final.json) distinguishes runtime and Builder checks.
Home visibly displays A's sentence. Runtime accessibility and Builder show C's region
name; Hello retains the baseline region. No create/update/delete business action was
invoked. Desktop captures retain visible app/workspace/page context. The static footer
1.0.0 is inherited and is not release-version stamping. Screenshots do not establish
multi-human concurrency or production usability beyond these observed views.

## Material failed approaches and repairs

Fixture creation first used unsupported PDB admin syntax; it failed before creation
and was corrected. ORDS installer privileges were insufficient initially and were
qualified with the vendor procedure in the fresh fixture. Accepted source DDL
reconstruction produced CHECK-constraint textual/order differences: constraints in
new fixtures were aligned with accepted native SXML and recaptured, not snapshots
edited. The first Page Designer automation did not update its model, so capture
caught missing edits before staging; native keyboard Save corrected it. Mixed
current/original component IDs failed integration in E4I; consistent original-ID
exports and canonical offset yielded the qualified combined source. None of these
failed attempts is counted as successful evidence or as a central deployment.

## Executable evidence gates and regression

The three commands in walkthrough stage 12 execute the repository's existing runner.
A1 passes 1/1 E.4 smoke assertion, A3 passes 3/3 grouped evidence assertions covering
IT-1–IT-4, and B1 passes 2/2 existing native pipeline smoke tests. Timestamped
`test_run_*.log` files retain each execution. The A3 readers inspect retained current
runtime evidence plus read-only GitHub records; they do not repeat target writes.
The 9 PR classification cases and frozen-release boundary negatives remain covered
by the selected regression. Broader historical Oracle/E.1 suites were not run because
they are outside the accepted E.4 native slice.

## Remaining acceptance boundary

Prepared-host feasibility is qualified. Clean-host reproduction, arbitrary fresh
PROJECT install, general schema drift, production fencing/race safety, three-human
concurrency and automated admission are not established. The final live Product Owner
walkthrough/acceptance and requested independent handover review remain separate gates.
