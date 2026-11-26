# E.18 verification — in progress

## Current observations

New source smoke A1 passes 1/1 and arithmetic/refusal unit A2 passes 1/1 in the linked logs. These establish source syntax, preserved named E.17 validation steps and reporting contracts, not performance. Real integration and full regression remain pending. [Checklist](sprint_E.18_checklist.md) retains unmet requirements; [bug record](sprint_E.18_bugs.md) preserves failed native attempts.

Initial source f2be037 fails utPLSQL installation because the copied native source directory is not writable. Corrected d878df0 installs the vendor objects, then its exploratory SYS-executed test fails ORA-06598 insufficient INHERIT PRIVILEGES. The current source aea3a77 executes the existing five-case backend suite through its own schema account instead of expanding SYS inheritance privileges. It retains every named E.17 validation and adds a zero-failed/zero-errored utPLSQL gate. Current real trials remain pending.

## Artifacts

- [Initial A1](test_run_A1_smoke_20261126_150322.log) and [initial A2](test_run_A2_unit_20261126_150322.log).
- [Checkpoint A1](test_run_A1_smoke_20261126_150711.log) and [checkpoint A2](test_run_A2_unit_20261126_150711.log).
- [Initial installer failure](tests/trial-45844508366-1/utplsql-install.log), [SYS-inheritance refusal](tests/trial-45845314659-1/utplsql-tests.log) and [UI gallery](screenshots/index.html).

Full gate and final accepted-source receipts will be added after execution. No skipped or cancelled native run is counted as acceptance.

## Repair observation

Current concurrent run 45846150456 at aea3a77 visibly reports five actual backend tests, zero failed, zero errored, zero disabled and zero warnings. [Capture 04](screenshots/04-backend-framed.png) shows the actual test-output line rather than its grep command. Native release/upgrade checks continue; this partial observation is not the real integration gate result.
