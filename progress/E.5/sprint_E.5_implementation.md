# E.5 — Implementation record

## Delivered prototype

The [design](sprint_E.5_design.md) and [setup](sprint_E.5_setup.md) bound PBI-061, PBI-040 and PBI-062 to one Hello-entry CREATE operation. [The walkthrough and slide deck](sprint_E.5_increment_demo.md) are the complete demonstration entry point; [the manual](user_manual.md) owns operation/recovery, [tests](sprint_E.5_tests.md) owns measured evidence and [the handover](sprint_E.5_handover.md) records actual live observations. [Architecture](../../docs/architecture.md) owns the wider native delivery policy.

HELLO_ENTRY_API exposes validation_error and create_entry. Text validation and active-state rejection occur before insertion; text is trimmed, the generated ID is returned and the caller retains transaction ownership. Existing database constraints and readiness/default triggers remain enabled. The package uses no APEX globals or wall clock. It does not define new identity/country authorization or concurrency behavior.

The isolated native APEX application 810503 maps validation to P101_ENTRY_TEXT and routes only CREATE through the package. Native form DML is limited to SAVE/DELETE. Native required-field feedback remains intact. The current application source under examples/testable-backend/apex was freshly exported with qualified SQLcl PROJECT. The separate page_create_adapter.sql is an explanatory CREATE fragment; the full native source owns the installed mapping and conditions.

## Fixtures, native release and configuration

The new E5_TEST schema contains an isolated input-constraint table, committed unrelated sentinel, API and real utPLSQL test package. E5_UT contains pinned utPLSQL 3.2.3; no public grants were added. The actual page fixture E5_PAGE contains the full retained native application table/trigger/package baseline and synthetic data, not copied retained business records. Its provenance is in fixtures/native-baseline/provenance.json. All three new database accounts finish with NO AUTHENTICATION. Only the existing isolated APEX VERIFIER account has a native application login.

The unit runner temporarily assigns an in-memory random E5_TEST password, connects as that owner and removes password authentication in finally. It fixes AMERICAN language/date language and UTC time zone. A fixed UTC timestamp derives deterministic test input. Ordinary tests use utPLSQL rollback; a separate structural experiment demonstrates why DDL requires explicit cleanup. Repeated/reordered runs preserve unrelated rows. These local test helpers are not concurrent-client infrastructure or new-host qualification.

SQLcl 25.4.1.0 build 25.4.1.022.0618 exported, staged, verified, released and packaged only E5_PAGE. The actual 33-entry native ZIP excludes E5_TEST, E5_UT, test packages and structural fixtures; its receipt records archive hash and source commit. Its creation is a bounded release-content experiment, not a deployment or upgrade proof. The source project's version is pinned in examples/testable-backend/.dbtools/project.config.json; no project version was changed to bypass native compatibility checking.

Scratch holds only downloads, a disposable native project and presentation build outputs. Private per-call database passwords stay in memory; temporary initial APEX login material was OS-private and is removed after setup. The operator can supply a fresh VERIFIER password through backend_login.py, which edits only that native account and redacts diagnostics. No new authoritative settings, credential store, saved connection or executable-path environment file was placed in scratch. The earlier prepared-host E1 secret exception remains unchanged and is not used by these helpers.

## Failures and engineering corrections

Initial startup attempts failed or were denied; renewed execution restored the VM with the compatible helper and launchd using OS-temporary configuration. ORDS required restart after the database service registered. An invalid bootstrap privilege was corrected to the vendor's grant list. These are historical setup failures, not current blockers.

Suite discovery failed because contiguous annotations attached suite/suitepath to trims_text. A blank line fixed the source defect; visibility/cache experiments did not fix it and their unnecessary diagnostic grants were revoked. The runner explicitly rejects a missing or zero-test suite. Removing trimming produced a real failed assertion; finally restored the source and the complete suite passed again.

A one-case coverage comparison initially showed no aggregate increase because profiler attribution on a condition line changed. The measured initial subset now omits both rejection cases, and the full suite adds them; raw reports retain the actual denominator/conditional metadata. The final retained run reports 9/11 to 11/11 executable lines. Earlier successful runs differed on condition-line attribution. This is recorded instrumented execution, not a correctness score.

The guessed gen-artifacts and a stale help example gen_artifacts were unsupported. The qualified existing project's gen-artifact recipe generated the real archive. The builder now rejects that subcommand diagnostic and requires archive presence/content. Bootstrap scripts refuse existing names rather than implicitly resetting fixtures.

## Operating and retention decision

Retain the small package/page prototype, isolated test sources and evidence as Elaboration assets. Retain the native release archive as experiment evidence. Do not silently promote them into a production delivery implementation. The [walkthrough](sprint_E.5_increment_demo.md) explains every supported command, SQL source and visible outcome before execution, including session expiry after import. Subsequent changes to page behavior, native release contents or package semantics require their applicable checks again; later host/concurrency/security obligations remain in the existing programme.
