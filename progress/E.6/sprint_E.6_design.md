# E.6 — Accepted design and test specification

Status: Accepted

Self-approved under the explicit YOLO instruction. [Setup](sprint_E.6_setup.md) owns scope/actors, [SRS](../../docs/srs.md) owns requirements and [architecture](../../docs/architecture.md) owns the native toolchain boundary. [Component contracts](../../docs/component-contracts.md) owns the version promises and representative classifications.

## Secure operation and trust boundary

E6_APP.secure_greetings.submit_request accepts a request key, country and text. It requires app 810603, a nonanonymous native APEX session, a matching P1_COUNTRY session item and an enabled identity/country permission. The country argument is untrusted. Request and audit inserts share a savepoint; any exception rolls back only this operation and propagates. A duplicate country/key is rejected with -20403. No internal commit or autonomous transaction is allowed. The caller commits or rolls back. A row lock waits at most the test session's timeout budget, bounded by client process timeouts; no general scheduling or exactly-once product claim is made.

E6_TEST session integration uses native CREATE_SESSION/SET_SESSION_STATE/DELETE_SESSION under the associated test schema. Supplied test identities are not password authentication. The real native APEX Accounts page separately signs in and submits, including a denied-country request. Failed initialization on invalid app ID propagates; finally clears native sessions. Permission tables are seeded with synthetic ALICE/PL and BOB/DE. Schema owners/admins can bypass database application logic and remain trusted. There is no public impersonation helper in release code.

## Compatibility and versions

The pure greeting_contract component has stable named arguments, greeting text and -20410 invalid-input behavior. A patch corrects whitespace to its documented behavior. A minor version adds an optional suffix and a new structured renderer while unchanged consumers keep working. The callable hello legacy wrapper remains supported/deprecated. Replacing legacy text with structured JSON is a detected major break; it is never released as a compatible variant. Shared LOV additions preserving existing codes/labels are minor; removed/reinterpreted codes are major; a typo-only label fix is patch only when label identity is explicitly not contractual. Component contracts, application release identity and migration identities are separate. Native packaging still contains the whole application and database source.

### Testing Strategy

Test: smoke, unit, integration. Regression: smoke, unit, scope secure_backend. SM-1 checks required sources and no internal transaction commits. UT-1 executes real utPLSQL pure-rendering consumers and invalid-input contract. IT-1 compares passing old consumers across baseline/patch/minor and detects a deliberate incompatible result, then restores. IT-2 exercises native sessions: permitted access, denied country, cross-country mismatch, failed initialization and cleanup. IT-3 verifies caller rollback, a caller marker preserved through injected second-write failure, and two competing sessions where commit causes duplicate rejection while rollback permits the waiter to succeed. IT-4 independently records real password authentication and page submission and validates the whole-application native archive. Exact observed results must pass; no YOLO failure allowance weakens an accepted criterion.

## Test Specification

PBI-052 maps to the explicit contract/classification review and IT-1 consumer results. PBI-064 maps to UT-1 and IT-1, including a callable deprecated interface and whole-application packaging. PBI-063 maps to IT-2 and the separate manual IT-4 password/page journey. PBI-079 maps to IT-3's real Oracle sessions, duplicate handling, savepoint preservation and no partial request/audit data. The temporary audit-failure trigger, suite packages and privileged session-setup helpers remain outside selected release source. Native implementation refines the initialization experiment to an explicit synthetic INIT_FAIL branch inside the laboratory application itself, so the real application initializer is exercised; this branch is intentionally visible in the whole-application prototype archive and is not a production initialization recommendation. This refinement is self-approved under YOLO and does not weaken any acceptance criterion. A red unit skeleton is executed before implementation. Native tools must match the approved SQLcl release/build before export, stage, verification or packaging.
