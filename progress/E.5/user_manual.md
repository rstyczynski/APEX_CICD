# E.5 — Operating reference

## Scope and prerequisites

Use the [complete walkthrough](sprint_E.5_increment_demo.md) for the page-to-package demonstration, commands, expected results and slide references. [Handover](sprint_E.5_handover.md) owns the live observations and limitations; [test results](sprint_E.5_tests.md) owns verification. This is a prepared-host Elaboration experiment. It does not install a production CI/CD system or qualify another host.

The existing apex-cicd Podman VM must be running with apex-db and apex-ords. The database needs FREEPDB1, APEX 24.2 and the isolated E5_UT/E5_TEST/E5_PAGE fixtures. SQLcl must be 25.4.1.0 build 25.4.1.022.0618, with the qualified Java 21 runtime. utPLSQL is pinned to 3.2.3 and its published SHA-256 in the toolchain receipt. Python 3, Git, Node, gh and the existing smoke prerequisites are needed. The code command must be on PATH for viewing artifacts.

The backend runner uses OS database authentication only to establish a temporary random test-account password, connects as E5_TEST, and removes password authentication in finally. It does not save credentials or native connections in scratch. Do not run concurrent copies: this prepared-host runner does not implement competing-client credential coordination. Backend unit tables reproduce input constraints; the separate page schema retains actual application constraints and readiness triggers. Never substitute these fixtures for retained author work.

## Recovery and preservation

A native APEX import invalidates the active session. Close any stale drawer, reload, and sign in again; do not repeat an uncertain CREATE until inspecting the list for its saved row. If ORDS starts before database service registration, its pool can remain invalid: start the database first, then restart the existing ORDS container. Do not delete or recreate retained volumes.

The runner rejects missing/zero-test suites. Suite and suitepath annotations must be separated from procedure annotations by a blank line. A failed mutation experiment restores the original package body in finally. Interrupted DDL can leave E5_TEST_DDL; inspect the exact owner and current test state before any explicit cleanup. The ordinary structural script refuses to adopt an existing object. Never broaden cleanup to unrelated schemas or records.

Fixture bootstrap scripts are one-time operations that reject preexisting names. They are not automatic reset commands. The native release builder operates only in disposable .local-apex/e5/native-project; the delivered native source and retained release receipt are the reviewable artifacts. The existing prepared-host credential exception remains unchanged. No credentials from it are needed by the backend tests.
