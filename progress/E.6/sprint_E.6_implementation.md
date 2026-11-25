# E.6 — Implementation

[Setup](sprint_E.6_setup.md) defines the bounded actor journey and [design](sprint_E.6_design.md) defines the accepted interfaces/cases. [The component contract](../../docs/component-contracts.md) owns promises and version classification; [the walkthrough](sprint_E.6_increment_demo.md), [manual](user_manual.md) and [handover](sprint_E.6_handover.md) explain operation. [Tests](sprint_E.6_tests.md) owns actual evidence.

## Secure component and transaction ownership

The new E6_APP schema contains country_permissions, greeting_requests, greeting_audit, the pure greeting_contract package and session-dependent secure_greetings package. Requests require app 810603, a nonanonymous APEX context, matching country session state and an enabled permission. ALICE/PL and BOB/DE are synthetic permissions. Every call checks access; untrusted country input is never treated as authority. The schema owner and database operator remain trusted. Native CREATE_SESSION accepts a supplied identity and is privileged test setup, not authentication; real APEX Accounts sign-in was exercised separately in Chrome.

submit_request establishes an operation savepoint. Request and audit insert together; duplicate keys raise -20403 and failures roll back only this operation. The package never commits. Prior caller work survives a second-write failure and remains rollbackable by the caller. Two independent Oracle connections exercise actual unique-key waiting: first commit leads to duplicate rejection, first rollback allows the waiter to succeed. Client deadlines bound these selected tests. There is no general concurrency, fairness, retry or exactly-once claim.

The app's laboratory initialization code deliberately raises for synthetic INIT_FAIL so native session-setup error propagation is observable. The reported ORA-20987 is APEX's wrapper around that initialization error. This is explicit laboratory fixture behavior, not a generic identity/initialization framework or a production release recommendation. The separate audit-failure trigger is temporary, removed in finally and absent from native release source. Tests compare native workspace session counts and unrelated business rows before/after cleanup.

## Compatibility and native delivery

The baseline supports the original named and deprecated calls. The patch fixes whitespace to the stated contract; the minor version adds an optional suffix and opt-in structured result. Existing consumers pass for each. A deliberately incompatible legacy return causes real utPLSQL failures; finally restores the original package, and consumers pass again. The legacy hello entry point remains callable. Contract, migration and application release identities remain distinct.

The reviewed JSON declares component versions and dependency ranges. The native builder executes the declaration guard before native operations, records declaration hash/component versions alongside the artifact and rejects unsupported/incompatible bounds. It does not infer compatibility from a diff. SQLcl itself retains whole-application/schema packaging; this thin guard is not generalized dependency resolution or selective component deployment. The qualified 25.4.1.0 / build 25.4.1.022.0618 export, stage, verify, release and gen-artifact create a 20-entry native archive. Test owners/suites and the temporary trigger are excluded. No target deployment is claimed by packaging.

## Tooling, preservation and corrections

New E6_APP/E6_TEST database accounts end without password authentication. Per-gate passwords are random, held in memory and removed in finally; temporary initial browser credentials are OS-private and removed at delivery. The ALICE access helper updates only the existing isolated native APEX account without storing its password. No credentials/configuration authority were added to checkout scratch. The existing utPLSQL 3.2.3 installation is reused through explicit E6 grants; framework code is unchanged.

An initial unsupported native initialization parameter failed before a complete application existed. Read-only vendor package inspection identified p_vpd, and the supported field imported successfully. A helper-copy output-path error was caught before staging: new logs were moved into E.6 and every overwritten E.5 evidence file was restored byte-for-byte from Git. Final validation checks E.5 remains unchanged. The shared backend runner now accepts an optional evidence-output directory so E.5 unit regression writes fresh results under E.6 rather than rewriting historical artifacts.

The prototype sources and isolated fixtures are retained as Elaboration assets. Broader security hardening, migration/data preservation, general concurrent operations and new-host reproduction remain later programme work. No remote push, submodule change or subsequent sprint activation is authorized.
