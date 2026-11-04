# Sprint E.3 technical handover — round 2 correction recheck

**Round:** E.3, round 2, original reviewer's correction recheck, 2026-11-04.

**Revisions:** Parent [rstyczynski/APEX_CICD](https://github.com/rstyczynski/APEX_CICD), branch/ref `main`, exact reviewed source **d37b461e23bf459ba34d5e5298a7f47af0306750**. Corrected application controller **eac24dedab3f611ef09b0196623cfabf674e7e1c**, obtained from that parent's tracked bundle. Historical application tag `v1.0.4` remains **fbda57a0cbe4d32961ad826852bd04394a500c11**. The [complete round-2 prompt](https://github.com/rstyczynski/APEX_CICD/blob/cb1d2aab5a6ba0921b2c696a2c289084730b2f37/progress/E.3/sprint_E.3_handover_review-2-prompt.md) was read at its specified **cb1d2aab5a6ba0921b2c696a2c289084730b2f37** revision, also the maintained checkout at entry. Inspection and authorized tests used an isolated extraction of the corrected source, not later working content. No implementation patch was supplied. The unrelated untracked `progress/E.3/model.drawio` was excluded and was not read or modified.

**Reviewer:** The original Codex GPT-6-based engineering review agent; exact model build is not exposed. This is a reviewer source, presentation and offline-test recheck, not independent human review or native runtime qualification.

**Scope and exclusions:** Rechecked R1-M1, R1-M2 and R1-L2 against their agreed closing conditions, and assessed the explicitly approved R1-L1 deferral. Ran only the two offline commands authorized by the prompt. Imported the actual corrected PPTX and rendered slides 4 and 10 into disposable storage using the bundled presentation runtime. No integration/platform tests, SQLcl, setup scripts, repository presentation build script, database/browser login, runner/container operation, workflow dispatch, deployment, credential/private-snapshot access, remote mutation, commit or push was performed. The only project write is this report; source and earlier review artifacts remain unchanged.

**Inputs:** [Original review](sprint_E.3_handover_review-1.md), [engineering response](sprint_E.3_handover_review-1-response.md), [reviewer feedback](sprint_E.3_handover_review-1-feedback.md), [selected decisions](sprint_E.3_handover_review-1-decisions.md), [correction receipt](tests/review-1-correction-checks.json), [recorded offline cases](tests/review-1-offline-diagnostics.log), [recorded static smoke](tests/review-1-static-smoke.log), [walkthrough](sprint_E.3_increment_demo.md), [implementation](sprint_E.3_implementation.md), [manual](user_manual.md), [configuration](sprint_E.3_github_configuration.md), [handover](sprint_E.3_handover.md), [test record](sprint_E.3_tests.md) and [audit](sprint_E.3_documentation_audit.md). Also compared the relevant corrected policy, SRS, test profile, presentation/package/source, assertions, workflow and test callers with the original reviewed implementation. All correction inputs refer to the pinned parent revision above.

## Per-finding result

`verified` here means reviewer verification at the stated documentation/source/offline level. It does not mean a new native qualification or deployment succeeded.

| Finding | Closing condition | Reviewer status | Validation level |
|---|---|---|---|
| R1-M1 | Met | verified@d37b461 | Actual slide/notes/source comparison, package preservation and rendered inspection |
| R1-M2 | Met | verified@d37b461 | Current documentation compared with fixed test inputs and replay acceptance instructions |
| R1-L1 | Met as an approved deferral | deferred | Explicit policy exception, owner, reason, scope and ending/reconsideration triggers |
| R1-L2 | Met for the selected offline correction | verified@d37b461 | Shared assertion/caller inspection, 21/21 actual offline cases and static smoke |

No new material E.3 finding or regression was identified in this recheck. No additional R2 finding IDs are introduced.

## R1-M1 — Corrected presentation operating commands

**Evidence:** Actual `sprint_E.3_increment_demo.pptx` slides 4/10 and their notes; [presentation authoring source lines 35–60](https://github.com/rstyczynski/APEX_CICD/blob/d37b461e23bf459ba34d5e5298a7f47af0306750/progress/E.3/presentation-handover/build.mjs#L35); walkthrough B/F.

Slide 4 now defines `e3_repo` in the parent terminal using the authenticated operator's GitHub login and the `APEX_CICD_E3_LAB` repository name. Both launcher calls pass that repository and the same explicit `$HOME/actions-runner-e3-lab` directory. The notes identify the parent repository root, completed step-A LAB/environment setup, the current step-B instructions and the requirement to leave the listener running. They no longer direct the operator to the historical seed runner chapter.

Slide 10 independently defines `e3_repo` in the application terminal, prompts for the already published tag from step E, displays `gh release view` for that LAB/tag and dispatches the same selected values. Notes explain the tag's provenance and require the listener to serve that LAB. The fixed v1.0.4/run 41679427616 text is visibly labeled a historical seed observation; the replay instructions require inspection of the newly dispatched LAB run.

The actual deck and authoring source agree on these operations. The PPTX SHA-256 is **9b3423fbc29a037ee92fd58b10e8bb8aa8288ec96b68abd0ce12c022bec3e71f**, matching the receipt. Package comparison against the pre-correction deck confirmed exactly four changed file parts: slides 4/10 and their notes. The other **75 file parts** are byte-identical; directory entries are excluded from that count. ZIP integrity passed and the runtime imported twelve slides.

I rendered and visually inspected slides 4 and 10 from this actual PPTX. The corrected commands, explanatory text and historical labels are readable, with no observed clipping or overlap. This was not a native PowerPoint inspection or a fresh visual review of every unchanged slide. No seed dispatch or runner operation is necessary to establish the correction. **R1-M1 is verified at the documentation/presentation level; no remaining closing action.**

## R1-M2 — Fixed reference checks are distinguished from LAB acceptance

**Evidence:** [manual lines 252–269](https://github.com/rstyczynski/APEX_CICD/blob/d37b461e23bf459ba34d5e5298a7f47af0306750/progress/E.3/user_manual.md#L252), [test profile's E.3 section](../../docs/test-profile.md#e3-implemented-pipeline-checks), current command-behavior section and historical boundary in the test record, configuration/handover clarifications, implementation correction section, and [integration test source](../../tests/integration/test_pipeline.sh).

The selected documentation-only correction is implemented. Current guidance names the hard-coded seed, committed journey, v1.0.4, deployment 41679427616 and qualification 41679432928. It states that IT-1/IT-2 download existing evidence without dispatching workflows, injecting another defect or accepting an operator's selected replay. The integration functions still use those fixed inputs, and their result messages now identify reference or legacy evidence explicitly.

The test profile and manual separately identify SM-1 as a static example/metadata check, platform smoke as a current HTTP login-form probe using seed environment variables, and IT-1/IT-2 as historical workflow-evidence readers. Seed environment API permission is distinguished from public source access or LAB ownership. Artifact expiry is acknowledged. The test record now places current behavior before the older execution account and corrects the explanation adjacent to the copyable commands; it no longer says those commands create the native experiment clone or need a private preservation snapshot.

New-LAB acceptance is tied to that operator's actual repository, change/release PRs, generated tag/source SHA, receipt/archive/native logs, qualification result if performed, and browser title/history observations. The documents expressly reject seed-reader success as a substitute for another LAB's acceptance or a prerequisite available to every operator. Parameterized replay validation is not claimed.

This satisfies the selected bounded correction without requiring new deployment evidence. I inspected the integration/platform sources but did not execute them. **R1-M2 is verified by source/document reconciliation; no remaining closing action.**

## R1-L1 — Approved prepared-host exception

**Evidence:** [AGENTS.md lines 70–83](https://github.com/rstyczynski/APEX_CICD/blob/d37b461e23bf459ba34d5e5298a7f47af0306750/AGENTS.md#L70), the R1-L1 selected decision, [SRS NFR-4 qualification](../../docs/srs.md#quality-requirements-and-initial-release), walkthrough step A and startup explanation, and the manual/configuration/handover/implementation statements.

The decision record and prompt explicitly record Product Owner approval of the fixes and temporary lookup on this prepared host. AGENTS now states the narrow exception directly: read-only interactive lookup of the existing E.1/E.2 credential record on the already prepared E.3 host, with no new authoritative scratch settings, copying to another host, migration/deletion or use by GitHub jobs. It identifies the record as a retained dependency while required. Native author profiles remain outside checkout scratch; workflow secrets and temporary job connections remain separate.

The Product Owner owns the exception and eventual remedy. Its reason is preservation of the requested existing-source credential retrieval for the prepared-host demonstration. The exception ends when a compliant credential-source remedy is selected and must be reconsidered before new-host reproduction, scratch cleanup or expansion. Current guidance and the SRS explicitly distinguish this accommodation from NFR-4 compliance and PBI-054 completion.

The inherited VM-start fallback still reads the scratch `containers.conf` override. The corrected walkthrough and connected guidance disclose that dependency and exclude the fallback from the supported explicit-VM-start sequence until separately corrected. They require completing the explicit VM checks and stopping on failure, rather than presenting the fallback configuration as disposable or unnecessary.

This is a coherent **approved deferral**, not a technical removal of the dependency. No evidence in this correction establishes that an ending/reconsideration trigger has occurred, and no private record was accessed to assess it. **The deferral condition is met; retain status `deferred` with its existing owner and triggers.**

## R1-L2 — Specific missing-file assertion and receipt

**Evidence:** [shared AWK assertion](../../examples/git-pipeline/.github/assert-missing-changeset.awk), [receipt filter](../../examples/git-pipeline/.github/qualification-receipt.jq), [qualification workflow](../../examples/git-pipeline/.github/workflows/qualification.yml), [offline test source](../../tests/unit/test_missing_changeset.sh), integration IT-2, and walkthrough chapter H.

The AWK assertion now requires exactly one numeric summary with a positive error count, agreement between that count and observed ERROR rows, and ERROR rows belonging to `stage stagechangelogfilesvalid`. It tracks the failing rule's diagnostic block, requires the missing-file message and compares the selected path literally. A new INFO/WARN/ERROR row ends the preceding block. ANSI sequences and trailing padding are removed; continuation fragments are joined only while they form the expected path. An unrelated ERROR or a path found under another rule cannot satisfy the intended check. This addresses the demonstrated false-positive mechanism without claiming a general SQLcl diagnostic parser.

The workflow obtains `missing` before removing the file and passes it to the controller checkout's shared assertion. It records `verification_schema: 2`, the selected path, controller `GITHUB_SHA`, application SHA, run ID and captured SQLcl version output, then validates its receipt with the same expected path. The jq filter requires the schema-2 path, a 40-hex controller identity and nonempty tool output in addition to source/run/outcome agreement. These fields are recorded provenance, not independent attestation or a new full-build compatibility gate.

Legacy compatibility is explicit and narrow: a receipt with neither schema nor path field is accepted only with the original v1.0.4 application SHA, run 41679432928 and pinned missing path. The fixed parent reader supplies that path and uses the shared assertion on the historical negative log. The old receipt was not retrofitted with new fields. The manual exercise obtains the corrected assertion from the parent checkout before switching to its temporary tagged application clone, so the historical tag need not contain the new helper. It passes the actual selected path and discloses that the old manual rehearsal is historical. Existing LAB repositories must adopt the reviewed controller/helpers before claiming the corrected behavior.

The parent assertion/filter/workflow files are byte-identical to those in corrected controller **eac24dedab3f611ef09b0196623cfabf674e7e1c**. The tracked bundle passed verification, contains complete history and retains v1.0.4 at its original SHA. Its SHA-256 is **f7963088c2ee0a888973c2ecf54782c66490a4b555f0e2f36a44844fd57f5c38**, matching the correction receipt.

I executed `bash tests/unit/test_missing_changeset.sh` in the isolated pinned extraction: **21 checks, zero failures, exit 0**. These run the actual AWK/jq assertions against retained logs and bounded fixtures. Coverage includes the original unrelated-error/INFO-rule false positive, wrong literal path, a path outside the error block, zero/missing/conflicting summaries, inconsistent counts, missing diagnostic message, additional unrelated error, connection failure, ANSI/padding, wrapped path, pinned legacy compatibility and new-receipt missing/mismatched fields. I also executed the authorized static smoke command: **1 test, zero failures, exit 0**.

This verifies the selected source/offline classification correction. The corrected qualification workflow has not been executed in this review or in the supplied correction evidence. Its next native run must retain its own controller/application/tool/path/log/receipt/cleanup identity before anyone claims fresh runtime success. That future native run was not selected as a condition of this correction. **R1-L2 is verified at the authorized offline level; no remaining closing action at that level.**

## Checks performed and evidence limits

The two executed project commands were:

```text
bash tests/unit/test_missing_changeset.sh
  Checks: 21; failed: 0; offline only — exit 0

bash tests/run.sh --smoke --new-only progress/E.3/new_tests.manifest
  Tests: 1; failed: 0 — exit 0
```

Installed `actionlint` was available at `/opt/homebrew/bin/actionlint`; no tools were installed. The static smoke includes workflow linting and nine PR-classification fixtures. Broader tests were not run. The reviewer results agree with the two committed correction logs.

Additional checks were exact Git revision/diff inspection, isolated source extraction and controller clone, bundle/ref/checksum verification, shared-file byte comparison, source/document/caller review, actual PPTX XML/notes/package comparison and two-slide rendering/visual inspection. The original report and feedback hashes remain respectively `532cbcc6a732a7b654cc858a4985f417e2ccf500af834825a79695dc0973a57f` and `3433744fc3c8f91393bb3efdd58bd68e386c1215b150702a69f05dabf07a2c82`, matching their recorded identities.

No fresh public workflow-artifact retrieval or current runtime-state assertion was needed for these closing conditions. The earlier review's limitations on private preservation snapshots, authenticated browser evidence, immutable promotion, toolchain qualification, identity/drift/fencing, concurrency, recovery and clean-host reproduction remain. This report does not reinterpret those production follow-ups as delivered or as new blockers for the accepted E.3 slice.

## Recommendation

**The bounded technical review can close with the approved R1-L1 deferral.** R1-M1 and R1-M2 meet their documentation/presentation closing conditions; R1-L2 meets its selected source/offline-test condition. No further correction is required by this recheck for the bounded Elaboration handover.

The coordinator can record the verified correction statuses and retain L1's approved owner, reason and triggers. This recommendation does not itself edit maintained decisions, close the sprint, establish a fresh native workflow pass or authorize production operation. Product Owner handover acceptance and sprint closure remain separate decisions.
