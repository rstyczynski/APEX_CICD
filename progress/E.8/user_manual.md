# E.8 operating reference

[Walkthrough](sprint_E.8_increment_demo.md) gives the complete journey; [design](sprint_E.8_design.md) owns scope and [implementation](sprint_E.8_implementation.md) owns mechanisms. [Test report](sprint_E.8_tests.md) owns executed evidence.

Run from the repository root on the prepared host. Python 3, Git, Podman connection apex-cicd, container apex-db with FREEPDB1 and its existing local administrator transport are required. SQLcl must be the retained .local-apex/tools/sqlcl-25.4.1.022.0618/sqlcl/bin/sql with JDK .local-apex/tools/jdk-21.0.12.1+1/Contents/Home. These are disposable tool caches, not credential stores. The driver validates release/build before database writes.

`python3 tests/test_candidate.py` tests policy with synthetic report records. `python3 tests/candidate_lab.py` executes all eight real laboratory cases. Each case allocates and drops a new E8_ schema; it never imports APEX or changes prior sprint targets. No password is generated or stored. Receipts and logs are overwritten by a repeat at the same evidence path, so preserve any reviewed run in Git first.

Inspect tests/executions.json for merge identity, cadence, suites, first failure, timing and schema. Inspect each cleanup.log. An unexpected transport or cleanup error is a failed experiment, never an accepted injected failure. Fix the host connection and rerun; do not suppress the failure. If termination prevents cleanup, use the exact schema in the preserved receipt/log and review ownership before any manual removal. Forced-termination cleanup guarantees belong to E.10.

The policy intentionally selects every suite for every change because this prototype has one greeting behavior unit. Unknown impact therefore cannot reduce coverage. Critical suites cannot be disabled or marked flaky. All report rows must match merge/tree/cadence/policy and contain positive integer counts. A local result is not a GitHub Testing status, signed publisher attestation or a production permission boundary.
