# E.16 correction — native lifecycle in GitHub Actions

The Product Owner requests named GitHub Actions steps for the native release lifecycle, Python limited to small checks, all acceptance/regression tests rerun, updated documentation/presentation and commit/push. The follow-up instruction makes [native technology responsibilities](../../AGENTS.md#use-core-technologies-for-their-native-responsibilities) mandatory for this correction and every future sprint; [the local method rule](../../RUPStrikesBack.patch/RUP_patch.md#p14-use-core-technologies-in-their-native-areas) governs review and escalation.

## Design and responsibility review

GitHub Actions owns the ordered steps, conditions, failure propagation and execution timeline. Each initial-release and upgrade export, stage, verification, release preparation, package and deployment is a separate named step. Oracle assertions, repeat deployment and individual negative cases also have named steps. Git commands remain native Git commands in those steps. SQLcl PROJECT remains the release/deployment implementation.

The removed lifecycle.py combined those responsibilities in a second orchestrator. It is replaced by native workflow commands and one thin sql.sh invocation adapter, which performs a version probe and one SQL payload invocation, enables SQL/OS error exits, retains visible output, and calls small output/tool validators. Python only validates output, measured build/metadata compatibility and archive/source/build provenance. It never runs Git, SQLcl or a lifecycle sequence. jq and sha256sum generate receipts; native Git bundles preserve generated history. Job-private saved connections stay in RUNNER_TEMP and an always-run cleanup step removes them. This preserves the original independent author/target databases and accepted table fixture; no production toolchain metadata or acceptance requirement is weakened.

The selected technologies support this requirement directly. There is no evidenced core-technology mismatch requiring a Product Owner substitution decision. The standing rule prohibits building another orchestration/migration/version-control framework if a mismatch is discovered later.

## Requirement-to-evidence checklist

R1–R6 retain their authoritative definitions in [the original checklist](sprint_E.16_checklist.md). Original closed-baseline evidence remains historical; it does not establish the changed workflow's acceptance. This correction does not invent a Done-to-Progress transition or start another sprint.

- [x] R1: rerun real native installation, additive upgrade, identical repeat and retained-data assertions.
- [x] R2: bind current reviewed workflow/helpers, generated Git history, both archive digests and observed target state.
- [x] R3: rerun mismatched receipt/source and substituted archive refusals, with unchanged target observations.
- [x] R4: rerun qualified actual tool/build checks, metadata checks and actual older-build refusal before mutation.
- [ ] R5: rerun A1/A2/A3 and unfiltered B1/B2/B3 against stable final executable source.
- [ ] R6: reconcile docs, render/inspect presentation, demonstrate actual named steps, audit, commit and push.
- [x] R7: independently visible successful Actions steps for export, stage, verify, release, package, install, upgrade, repeat and refusals. Source: Product Owner refactor request.
- [x] R8: apply the standing native-responsibility/no-reinvention/technology-mismatch escalation rule in design and audit. Source: Product Owner follow-up instruction and linked project policy.

Initial smoke/unit checks pass 1/1 each. Real hosted acceptance and all full regression outcomes remain pending for this correction.

## Verified native acceptance

Run 45810907563 at 03f18caa0ff3f1bd5c1d75e280d5bf038f9996e9 passes all 39 job steps. [Source review](sprint_E.16_source_review.md#named-actions-correction-source-review) connects reviewed workflow/helpers to generated history, both qualified archives and Oracle observations. [A3](tests/actions-refactor/A3.log) passes 1/1 and independently verifies named outcomes and downloaded evidence. R1–R4 and R7 pass on that real run. R8 is applied by committed project rules and design/source review; final audit will recheck it. No native acceptance case failed.

Fresh [A1](tests/actions-refactor/A1.log), [A2](tests/actions-refactor/A2.log), [B1](tests/actions-refactor/B1.log) and [B2](tests/actions-refactor/B2.log) pass 1/1, 1/1, 15/15 and 17/17. [B3](tests/actions-refactor/B3.log) remains running against stable test source. [Handover](sprint_E.16_handover.md#named-actions-correction-demonstration) records actual live named-step execution; [the revised deck validation](tests/actions-refactor/presentation.json) covers the 15-slide pending-results presentation. R5/R6 are not yet claimed complete.

## Reproduce validation

The existing runner selects the same acceptance and unfiltered regression levels as the accepted E.16 plan. The native reader checks the actual successful refactored workflow and its individual step results; it does not invoke delivery. Full integration uses the prepared host's isolated historical fixture and refuses changed executable/test source during its run. Position at the repository root with GitHub CLI access and the prerequisites in the test profile/manual, then run:

```bash
cd "$(git rev-parse --show-toplevel)"
bash tests/run.sh --smoke --new-only progress/E.16/new_tests.manifest
bash tests/run.sh --unit --new-only progress/E.16/new_tests.manifest
E16_RUN_ID=45810907563 bash tests/run.sh --integration --new-only progress/E.16/new_tests.manifest
bash tests/run.sh --smoke
bash tests/run.sh --unit
E16_RUN_ID=45810907563 bash tests/run.sh --integration
```

Expected result: zero failed selected entries at every level. Source smoke and isolated unit checks prove syntax, boundaries and refusal contracts. A3 proves the bounded real hosted lifecycle/provenance observations described above. Full regression re-executes its accepted historical behavior; it does not expand those experiments into production qualification.

## Regression source isolation

The first correction B3 attempt observed concurrent unrelated additions of scripts/sprint-finalize.sh and tests/test_sprint_finalize.py after its source snapshot. The mandatory stable-source result could therefore not pass, regardless of individual test outcomes. Preserved that attempt and interrupted its exact process group with SIGINT so normal cleanup could run. A native local Git clone pinned to a2e95ea isolates the E.16 code and tests from concurrent checkout edits. Its disposable scratch-tool path links to this prepared host's existing scratch; no credential is copied and the narrow retained read-only prepared-host exception is unchanged. Full historical integration still uses its owned separate E.12 database and private temporary inputs. The same suites will rerun in the stable clone; no test or source-stability condition is removed. Unrelated E.17 files remain untouched.

The first pinned-clone unit run exposed an invalid verification layout: symlinking the whole scratch directory changed path containment, so the checkout-profile rejection test no longer exercised an inside-checkout path. That failed run is retained under tests/actions-refactor/symlink-layout-attempt. Corrected the clone layout to use real scratch/tools directories and links only to installed tool payloads, cached artifacts and the same read-only retained prepared-host record. No credential is copied, no new credential store/profile is created, and no guard or test is weakened. All six gates rerun after this environment-only correction.

The tool installation also contained historical SQLcl-home/profile and runtime.env entries. These are not executable payloads and must not be mirrored as verification configuration. The final clone layout excludes all SQLcl-home/profile directories and runtime.env; it links only installed tool payloads/caches and the existing approved read-only record. The checkout-profile fixture consequently resolves inside the clone, and the unchanged unit suite passes 17/17. Five gates now pass from the pinned checkout: 1/1, 1/1, 1/1, 15/15, 17/17; full B3 is running. The corrected layout neither relocates nor writes the retained record, nor introduces new persistent settings.
