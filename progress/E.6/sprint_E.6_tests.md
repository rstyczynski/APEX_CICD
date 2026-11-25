# E.6 — Executed tests

## Gate results

A1 passes the source/declaration/transaction smoke check. A2 passes one registered unit gate executing three real utPLSQL consumers with zero failures/errors/disabled tests. A3 passes three integration groups: compatible/mutated consumers, native sessions plus partial failure and competing requests, and separate browser/native archive evidence. B1 passes the selected five smoke checks. B2 passes two unit groups: the prior five-test backend suite and the three-test contract suite. [Gate receipts](tests/gates.json) own exact timestamped log names and statuses. The scope is explicit in PLAN; inactive E.1 controller fixtures are not claimed as regression evidence. Prior E.5 runtime evidence is unchanged; fresh backend regression output is under E.6/tests/regression-backend.

## Compatibility and versions

Three existing consumers pass against pre-extension 1.0, corrected 1.0.1 and additive 1.1. The patch separately returns trimmed padded text; the minor suffix and structured renderer work without replacing legacy output. A deliberate BREAKING RESULT implementation fails existing consumers; finally restores the original and the suite passes again. The deprecated hello call remains callable. The native builder consumes and validates explicit component dependency bounds and records the declaration hash/version map with the archive. A smoke negative case rejects Greeting 2.0 against Request's declared <2.0 bound. [The contract document](../../docs/component-contracts.md) records the semantic review, including APEX items/requests, shared LOV codes and retained-data implications. No automatic compatibility inference is claimed.

## Native context and transaction evidence

The session integration allows ALICE/PL and BOB/DE, rejects an argument/session country mismatch (-20401) and denied access (-20402), then explicitly rolls back the allowed test requests. INIT_FAIL causes the real application's initialization branch to fail; APEX propagates ORA-20987. Sessions are deleted and before/after workspace session counts match. This is privileged supplied-identity setup, not password authentication. The separate Chrome observation rejects an incorrect password, authenticates ALICE and exercises an allowed and a denied page submission; live database checks confirm the observed business-state boundary.

A test-only BEFORE INSERT audit trigger raises -20499 on FAIL-AUDIT after the request insert. The package rolls back to its operation savepoint, preserving a prior caller marker. The caller explicitly rolls back afterward; no request or marker remains. The fault trigger is removed in finally and excluded from the native release.

Two subprocesses create independent native APEX sessions and Oracle connections. Writer A inserts and holds a unique country/key. The test observes writer B in an actual enq: TX - row lock contention wait before releasing A. With A commit, B receives -20403; with A rollback, B succeeds. Each interleaving leaves exactly one request and one matching audit before run-owned cleanup. Both processes have bounded client deadlines; no general scheduling/fairness or all-isolation-level guarantee is claimed. Unrelated request snapshots match before/after. [Transaction receipts](tests/transaction-results.json) preserve the selected cases and outcomes.

## Native release and manual observations

Qualified SQLcl 25.4.1.0 / build 25.4.1.022.0618 performs native export, stage, verify, release and gen-artifact. [The 20-entry archive](tests/e6-backend-1.0.0.zip) contains the application and selected E6_APP database source. It excludes E6_TEST, its suite and the temporary fault trigger. [The receipt](tests/native-release.json) records archive/declaration hashes, component versions and selected Git source commit. The delivered application source is copied from fresh native export. This is whole-application package evidence, not a target deployment or data-upgrade result.

[Browser observations](tests/browser-observations.json) record the actual developer-operated password/page actions. [Live business checks](tests/page-business-check.log) independently require the allowed request, absent denied request and absent fault trigger. Native session tests do not stand in for that manual authentication check. Earlier failed native import used an unsupported initialization parameter; vendor signature inspection identified p_vpd and the corrected import succeeded. No code/toolchain version check was bypassed.

## Artifacts

The timestamped gate logs and all supporting runtime logs are linked below during final audit. Raw source-discovery output is retained compressed where verbose. [The walkthrough](sprint_E.6_increment_demo.md) provides executable commands, full SQL and expected results before invocation; [the audit](sprint_E.6_documentation_audit.md) records syntax, links, rendering, hashes and final scoped commits.

## Retained gate and runtime logs

[application-install.log](tests/application-install.log)

[archive-listing.log](tests/archive-listing.log)

[auth-cleanup-E6_TEST.log](tests/auth-cleanup-E6_TEST.log)

[auth-start-E6_TEST.log](tests/auth-start-E6_TEST.log)

[business-after.log](tests/business-after.log)

[business-before.log](tests/business-before.log)

[compat-1.0.1.log](tests/compat-1.0.1.log)

[compat-1.0.log](tests/compat-1.0.log)

[compat-1.1.log](tests/compat-1.1.log)

[compat-baseline-install.log](tests/compat-baseline-install.log)

[compat-minor-install.log](tests/compat-minor-install.log)

[compat-patch-install.log](tests/compat-patch-install.log)

[compat-restored-consumers.log](tests/compat-restored-consumers.log)

[compat-restored.log](tests/compat-restored.log)

[compatible-additions.log](tests/compatible-additions.log)

[compatible-patch-fix.log](tests/compatible-patch-fix.log)

[demo-login.log](tests/demo-login.log)

[fault-cleanup.log](tests/fault-cleanup.log)

[fault-setup.log](tests/fault-setup.log)

[final-runtime-state.log](tests/final-runtime-state.log)

[framework-grants.log](tests/framework-grants.log)

[incompatible-detected.log](tests/incompatible-detected.log)

[incompatible-install.log](tests/incompatible-install.log)

[isolated-alice-access.log](tests/isolated-alice-access.log)

[native-export.log](tests/native-export.log)

[native-init-parameters.log](tests/native-init-parameters.log)

[native-init.log](tests/native-init.log)

[native-package.log](tests/native-package.log)

[native-parameter-discovery.log](tests/native-parameter-discovery.log)

[native-release.log](tests/native-release.log)

[native-stage-verify.log](tests/native-stage-verify.log)

[no-partial-business.log](tests/no-partial-business.log)

[page-business-check.log](tests/page-business-check.log)

[page-native-auth-cleanup.log](tests/page-native-auth-cleanup.log)

[page-native-auth-start.log](tests/page-native-auth-start.log)

[partial-failure.log](tests/partial-failure.log)

[partial-invariants.log](tests/partial-invariants.log)

[race-commit-cleanup.log](tests/race-commit-cleanup.log)

[race-commit-first.log](tests/race-commit-first.log)

[race-commit-invariants.log](tests/race-commit-invariants.log)

[race-commit-second.log](tests/race-commit-second.log)

[race-commit-wait.log](tests/race-commit-wait.log)

[race-rollback-cleanup.log](tests/race-rollback-cleanup.log)

[race-rollback-first.log](tests/race-rollback-first.log)

[race-rollback-invariants.log](tests/race-rollback-invariants.log)

[race-rollback-second.log](tests/race-rollback-second.log)

[race-rollback-wait.log](tests/race-rollback-wait.log)

[regression-backend/utplsql-full.log](tests/regression-backend/utplsql-full.log)

[schema-install.log](tests/schema-install.log)

[session-cleanup-count.log](tests/session-cleanup-count.log)

[sessions-after.log](tests/sessions-after.log)

[sessions-before.log](tests/sessions-before.log)

[sessions.log](tests/sessions.log)

[sqlcl-qualified.log](tests/sqlcl-qualified.log)

[test_run_A1_smoke_20261125_180641.log](tests/test_run_A1_smoke_20261125_180641.log)

[test_run_A1_smoke_20261125_180929.log](tests/test_run_A1_smoke_20261125_180929.log)

[test_run_A2_red_20261125.log](tests/test_run_A2_red_20261125.log)

[test_run_A2_unit_20261125_180641.log](tests/test_run_A2_unit_20261125_180641.log)

[test_run_A3_integration_20261125_180641.log](tests/test_run_A3_integration_20261125_180641.log)

[test_run_A3_integration_20261125_180929.log](tests/test_run_A3_integration_20261125_180929.log)

[test_run_B1_smoke_20261125_180641.log](tests/test_run_B1_smoke_20261125_180641.log)

[test_run_B2_unit_20261125_180641.log](tests/test_run_B2_unit_20261125_180641.log)

[unit-install.log](tests/unit-install.log)

[unit.log](tests/unit.log)

## Final delivery receipts

[delivery-validation.log](tests/delivery-validation.log)

[page-release-final-check.log](tests/page-release-final-check.log)

[test_run_A1_smoke_20261125_181426.log](tests/test_run_A1_smoke_20261125_181426.log)

[Compressed native session-view discovery](tests/session-view-columns.log.gz) preserves its verbose raw output. The final source-pin/build guard rejects both a mismatching project release and an unqualified build; the native package was rechecked against the actual page/business state after that guard was added.
