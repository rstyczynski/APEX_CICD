# E.6 — Operating reference

The [complete walkthrough and slide deck](sprint_E.6_increment_demo.md) are the demonstration entry point. [Contract rules](../../docs/component-contracts.md) own compatibility, [test results](sprint_E.6_tests.md) own measured evidence and [handover](sprint_E.6_handover.md) records actual live observations.

## Prerequisites and supported operations

This is a prepared-host laboratory experiment: apex-cicd Podman VM, running apex-db/apex-ords, FREEPDB1, APEX 24.2, E6_APP workspace/app 810603, E6_TEST and the existing pinned utPLSQL 3.2.3 framework. SQLcl must match release 25.4.1.0 / qualified build 25.4.1.022.0618 before native processing. Python, Git, the existing pipeline smoke prerequisites and the code command are required. Bootstrap creates new isolated names only and rejects preexisting schemas; it is not an implicit reset or fresh-host qualification.

ALICE is permitted PL and BOB is permitted DE. The page accepts country, request key and greeting text. Successful Submit greeting displays “Greeting request saved.” A denied country displays ORA-20402 and does not save a request. A duplicate country/key raises -20403 rather than overwriting. Choose a fresh synthetic key when repeating a successful manual demonstration; inspect the database evidence before retrying an uncertain request.

## Transaction and security boundary

The application request owns neither caller commit nor caller rollback. The page submission commits a successful request through normal APEX processing. Backend callers choose commit/rollback explicitly. Native session creation with a supplied username is privileged test setup; it does not validate a password. Do not expose the fixture setup APIs as a public impersonation service. The tests do not model an attacker holding parsing-schema or database-administrator privileges.

The concurrency test holds two real Oracle sessions and expects a unique-key transaction wait. It owns only its generated E6 request keys and deletes those rows explicitly after assertion. The fault trigger owns only the FAIL-AUDIT scenario and is removed in finally. If interrupted, inspect the exact fixture owners, open test processes and trigger before repeating; never drop unrelated objects or reset a retained environment. The test runner is serial at gate level and is not a concurrent test-orchestration service.

## Recovery and limits

A native import expires browser sessions; reload and sign in again. Start Oracle before ORDS to avoid a cached invalid connection pool. The login helper lets the operator supply a new ALICE password for the isolated workspace; it saves no password file. Database test passwords are temporary and removed in finally. If a client is killed before cleanup, use the prepared database operator to restore NO AUTHENTICATION for E6_APP/E6_TEST after stopping that test; no credentials belong in scratch.

The INIT_FAIL identity intentionally exercises failing application initialization. Schema owners/admins remain trusted, and country authorization is synthetic. Version declarations and their supported simple dependency bounds are reviewed inputs, not automatic inference or a production dependency resolver. Deployments remain whole-application. PBI-052/063/064/079 qualify this bounded experiment, not all authentication, isolation levels, distributed transactions, data upgrades or production readiness.
