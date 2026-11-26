# E.16 correction — native lifecycle in GitHub Actions

The Product Owner requests named GitHub Actions steps for the native release lifecycle, Python limited to small checks, all acceptance/regression tests rerun, updated documentation/presentation and commit/push. The follow-up instruction makes [native technology responsibilities](../../AGENTS.md#use-core-technologies-for-their-native-responsibilities) mandatory for this correction and every future sprint; [the local method rule](../../RUPStrikesBack.patch/RUP_patch.md#p14-use-core-technologies-in-their-native-areas) governs review and escalation.

## Design and responsibility review

GitHub Actions owns the ordered steps, conditions, failure propagation and execution timeline. Each initial-release and upgrade export, stage, verification, release preparation, package and deployment is a separate named step. Oracle assertions, repeat deployment and individual negative cases also have named steps. Git commands remain native Git commands in those steps. SQLcl PROJECT remains the release/deployment implementation.

The removed lifecycle.py combined those responsibilities in a second orchestrator. It is replaced by native workflow commands and one thin sql.sh invocation adapter, which invokes SQLcl once, enables SQL/OS error exits, retains visible output, and calls small output/tool validators. Python only validates output, measured build/metadata compatibility and archive/source/build provenance. It never runs Git, SQLcl or a lifecycle sequence. jq and sha256sum generate receipts; native Git bundles preserve generated history. Job-private saved connections stay in RUNNER_TEMP and an always-run cleanup step removes them. This preserves the original independent author/target databases and accepted table fixture; no production toolchain metadata or acceptance requirement is weakened.

The selected technologies support this requirement directly. There is no evidenced core-technology mismatch requiring a Product Owner substitution decision. The standing rule prohibits building another orchestration/migration/version-control framework if a mismatch is discovered later.

## Requirement-to-evidence checklist

R1–R6 retain their authoritative definitions in [the original checklist](sprint_E.16_checklist.md). Original closed-baseline evidence remains historical; it does not establish the changed workflow's acceptance. This correction does not invent a Done-to-Progress transition or start another sprint.

- [ ] R1: rerun real native installation, additive upgrade, identical repeat and retained-data assertions.
- [ ] R2: bind current reviewed workflow/helpers, generated Git history, both archive digests and observed target state.
- [ ] R3: rerun mismatched receipt/source and substituted archive refusals, with unchanged target observations.
- [ ] R4: rerun qualified actual tool/build checks, metadata checks and actual older-build refusal before mutation.
- [ ] R5: rerun A1/A2/A3 and unfiltered B1/B2/B3 against stable final executable source.
- [ ] R6: reconcile docs, render/inspect presentation, demonstrate actual named steps, audit, commit and push.
- [ ] R7: independently visible successful Actions steps for export, stage, verify, release, package, install, upgrade, repeat and refusals. Source: Product Owner refactor request.
- [ ] R8: apply the standing native-responsibility/no-reinvention/technology-mismatch escalation rule in design and audit. Source: Product Owner follow-up instruction and linked project policy.

Initial smoke/unit checks pass 1/1 each. Real hosted acceptance and all full regression outcomes remain pending for this correction.
