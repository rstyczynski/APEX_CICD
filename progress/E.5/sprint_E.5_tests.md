# E.5 — Executed verification

## Final quality gates

A1 smoke passed: 1/1 registered source-boundary check. A2 unit passed: 1/1 gate running five real utPLSQL tests, with zero failed, errored or disabled tests. A3 integration passed: 2/2 groups cover repeat/reorder preservation, explicit structural cleanup, coverage improvement, mutation detection/restoration, live page metadata assertions and native artifact exclusion. B1 existing smoke regression passed: 4/4 checks, including the live configured ORDS/APEX login probe and the native pipeline/release-boundary checks. Unit/integration regression was not selected in PLAN. The final logs below supersede failed earlier attempts; failures remain retained evidence.

The fixed test fixture uses an explicit 2026-11-25 12:00:00 UTC timestamp to derive its input text. Session language and date language are AMERICAN and the time zone is UTC. The API has no clock dependency. Repeating and reversing the five test paths leaves every committed unrelated row identical; identity sequence advancement is an expected nontransactional effect and is not mistaken for a leaked business row. The structural fixture demonstrates DDL survival after rollback, explicitly drops its own table and confirms absence.

## Coverage and deliberately detected regression

The retained final XML reports cover only E5_TEST.HELLO_ENTRY_API package-body executable lines, excluding tests and framework. The initial three-case subset covers 9/11 lines (81.8%); adding the overlength and invalid-active cases produces 11/11 (100%). The complete XML retains line and conditional-branch metadata. These figures describe this recorded execution; profiler attribution on condition lines varied across repeats, including 8/11 to 11/11 in another successful run. A one-case comparison initially showed unchanged aggregate coverage despite reaching the new rejection line; the final comparison transparently uses both missing rejection cases. Coverage measures observed execution, not semantic completeness or a production quality threshold.

Removing trimming from the isolated API insert causes the real trimming test to report one failed test. The runner restores the original source in finally, then runs all five tests successfully. No mutant was imported into E5_PAGE or packaged. The integration runner requires nonempty coverage denominators and improvement, and rejects missing/empty/errored suites. Test outcome checks do not accept a zero-test schema run.

## Page and release evidence

A native Chrome walkthrough compared actual page 101 before and after extraction: one identical required-field message, both beside Entry Text and in the notification; padded input saved as trimmed E5 before / E5 after; successful Create closes the dialog and refreshes the list. Native metadata inspection verifies the custom validation maps to P101_ENTRY_TEXT, the API process runs only for CREATE and native DML only for SAVE/DELETE. A direct invalid API call raises -20320 and preserves row counts. The page schema retains actual constraints and its enabled readiness trigger. The unit schema is a deliberately smaller constraint fixture, not a claim of full application integration.

SQLcl release 25.4.1.0, qualified build 25.4.1.022.0618, performed native export, staging, verification, release and gen-artifact. The 33-entry archive includes E5_PAGE and excludes E5_TEST/E5_UT/test packages/structural fixture. ZIP SHA-256 and selected source commit are in the native release receipt. The example application source was copied from the freshly exported native application, not a fabricated snapshot. No source-version bypass, remote push or release deployment is claimed.

## Failure analysis and recovery

The installed system helper rejected VM startup. The compatible prepared helper, temporary configuration and launchd lifecycle restored it without replacing persistent host settings. ORDS initially cached an invalid pool because it started before database registration; restarting ORDS after database readiness restored the default pool. An invalid bootstrap CREATE CONTEXT grant was corrected before installing utPLSQL. The official download checksum matched its published value.

ORA-20204 was caused by contiguous suite and procedure annotations: inspection showed suite/suitepath attached to trims_text. A separating blank line fixed discovery; all five tests then executed. Owner recompilation, cache inspection/rebuild and visibility changes had not fixed it. Diagnostic internal grants and unnecessary API/test execute grants were revoked. Both new database test accounts and the page schema finish with NO AUTHENTICATION; per-call test passwords exist only in memory and cleanup is in finally.

The guessed gen-artifacts and a stale native-help gen_artifacts example were rejected. The existing qualified project recipe's gen-artifact command produced the actual archive. The builder now detects the subcommand error and requires the archive, its package entry and its exclusion assertions. Earlier missing-artifact attempts are retained, not reported as successes.

## Artifacts

The final gates are [A1](tests/test_run_A1_smoke_20261125_complete.log), [A2](tests/test_run_A2_unit_20261125_complete.log), [A3](tests/test_run_A3_integration_20261125_delivery.log) and [B1](tests/test_run_B1_smoke_20261125_complete.log). [The full suite](tests/utplsql-full.log), [reordered run](tests/utplsql-reordered.log), [repeat](tests/utplsql-repeat.log), [before rows](tests/rows-before.log), [after rows](tests/rows-after.log), [coverage before](tests/coverage-before.xml), [coverage after](tests/coverage-after.xml), [detected mutation](tests/mutation-detected.log), [restored source](tests/mutant-restored.log) and [backend summary](tests/backend-results.json) preserve the executable observations.

[Structural cleanup](tests/structural-cleanup.log), [page assertions](tests/page-assertions.log), [browser observations](tests/browser-observations.json), [native source export](tests/native-export.log), [stage/verify](tests/native-stage-verify.log), [native packaging](tests/native-package.log), [release receipt](tests/native-release.json), [archive](tests/e5-backend-1.0.0.zip), [qualified SQLcl](tests/sqlcl-qualified.log) and [toolchain pins](tests/toolchain.json) preserve the selected runtime/build boundaries. All other logs in tests/ are bootstrap, diagnostic or earlier-attempt evidence. The [walkthrough](sprint_E.5_increment_demo.md) explains runnable entry points before invocation; the [audit](sprint_E.5_documentation_audit.md) records final reconciliation and presentation validation.

## Retained earlier attempts and supporting logs

[access-api-signature.log](tests/access-api-signature.log)

[access-synonym-chain.log](tests/access-synonym-chain.log)

[access-synonym.log](tests/access-synonym.log)

[archive-listing.log](tests/archive-listing.log)

[backend-install.log](tests/backend-install.log)

[bootstrap-existing-refused.log](tests/bootstrap-existing-refused.log)

[bootstrap-preflight.log](tests/bootstrap-preflight.log)

[cache-rebuild.log](tests/cache-rebuild.log)

[coverage-after.log](tests/coverage-after.log)

[coverage-before.log](tests/coverage-before.log)

[debug-cursor.log](tests/debug-cursor.log)

[debug-discovery.log](tests/debug-discovery.log)

[debug-framework.log](tests/debug-framework.log)

[debug-suitepath.log](tests/debug-suitepath.log)

[direct-api-check.log](tests/direct-api-check.log)

[isolated-verifier-access.log](tests/isolated-verifier-access.log)

[local-checks.log](tests/local-checks.log)

[mutant-install.log](tests/mutant-install.log)

[native-init.log](tests/native-init.log)

[native-release-package.log](tests/native-release-package.log)

[page-after-mapping.log](tests/page-after-mapping.log)

[page-api-install.log](tests/page-api-install.log)

[page-baseline-install.log](tests/page-baseline-install.log)

[page-before-mapping.log](tests/page-before-mapping.log)

[page-native-auth-cleanup.log](tests/page-native-auth-cleanup.log)

[page-native-auth-start.log](tests/page-native-auth-start.log)

[page-variant-api.log](tests/page-variant-api.log)

[page-variant-baseline.log](tests/page-variant-baseline.log)

[page-view-columns.log](tests/page-view-columns.log)

[runtime-inventory.log](tests/runtime-inventory.log)

[suite-final-install.log](tests/suite-final-install.log)

[suite-fixed-annotation-spacing.log](tests/suite-fixed-annotation-spacing.log)

[suite-recompiled-as-owner.log](tests/suite-recompiled-as-owner.log)

[test_run_A1_smoke_20261125.log](tests/test_run_A1_smoke_20261125.log)

[test_run_A1_smoke_20261125_delivery.log](tests/test_run_A1_smoke_20261125_delivery.log)

[test_run_A1_smoke_20261125_final.log](tests/test_run_A1_smoke_20261125_final.log)

[test_run_A2_unit_20261125.log](tests/test_run_A2_unit_20261125.log)

[test_run_A2_unit_20261125_final.log](tests/test_run_A2_unit_20261125_final.log)

[test_run_A3_integration_20261125_complete.log](tests/test_run_A3_integration_20261125_complete.log)

[test_run_A3_integration_20261125_complete_v2.log](tests/test_run_A3_integration_20261125_complete_v2.log)

[test_run_A3_integration_20261125_final.log](tests/test_run_A3_integration_20261125_final.log)

[test_run_B1_smoke_20261125_final.log](tests/test_run_B1_smoke_20261125_final.log)

[utplsql-install-retry.log](tests/utplsql-install-retry.log)

[utplsql-install.log](tests/utplsql-install.log)
