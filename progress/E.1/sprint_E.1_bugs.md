# E.1 — Fold-in fixes

## BUG-1 — SQLcl could finish without executing buffered interactive SQL

Item: PBI-011.1. Status: fixed. Severity: high.

A preservation fixture prepared with piped interactive MERGE was absent in a later session. A separately committed INSERT survived qualification-area recreation. The SQLcl wrapper now executes protected script files and requires a server-side completion marker before success. Rechecked MERGE persistence and deliberate Oracle-error propagation. The fix is included in the current platform increment; no broader scope is introduced.

## BUG-2: Fresh checkout lacks exact walkthrough release inputs

**Item:** PBI-011.6
**Severity:** high
**Status:** fixed

- **Symptom:** prerequisites reads ignored selected-archive pointers; a clean checkout cannot reach A–H.
- **Root cause:** reviewed archives/candidate evidence are local; patch admission pins the initial archive hash.
- **Fix:** reconstruct reviewed exact archive bytes from pinned Git source and checked-in original candidate evidence; verify members/archive SHA and atomically select inputs. Add a visible input-preparation step before infrastructure precheck. Evidence replay is not a fresh validation claim.
- **Verification:** independent local clone with no copied releases rebuilds matching archives; missing source, tampering and conflicting existing inputs reject; native walkthrough validation follows.

## BUG-3: Infrastructure SQL failure can return success

**Item:** PBI-011.1
**Severity:** high
**Status:** fixed

- **Symptom:** native ORA-20224 returns shell 0 with EXIT SQL.SQLCODE.
- **Root cause:** Unix status truncates Oracle error codes.
- **Fix:** EXIT FAILURE and OS-error handling in all affected infrastructure paths.
- **Verification:** native SQLPlus error probe returns nonzero; infrastructure regression/syntax checks.

## BUG-4: Privileged provisioning accepts unchecked configuration

**Item:** PBI-011.1
**Severity:** high
**Status:** fixed

- **Symptom:** schema/workspace names and application IDs enter SYS SQL before validation.
- **Root cause:** validation exists only in the isolation helper.
- **Fix:** shared strict complete-config validation before SQL or secret access; reject unsafe names, IDs, service values, duplicates and unsupported mappings. Keep the scoped lab bootstrap boundary; production privilege redesign is deferred.
- **Verification:** malformed input fails before any Oracle call; valid existing mappings and native area checks pass.

## BUG-5: Candidate tests may run from dirty untracked provenance

**Item:** PBI-011.6
**Severity:** high
**Status:** fixed

- **Symptom:** runner/manifests/Python/shell tests can change without the candidate clean-source gate rejecting them.
- **Root cause:** package/check scope includes tests/sql only.
- **Fix:** include the full test harness in source cleanliness and packaging; retain exact candidate revision binding.
- **Verification:** dirty runner, manifest and Python/shell test fixtures reject; clean source passes without relying on current runtime state.

## BUG-6: Replacement imports do not preserve a recorded APEX offset

**Item:** PBI-011.4
**Severity:** high
**Status:** open

- **Symptom:** patch import calls GENERATE_OFFSET for an existing application; APEX user-state preservation is unproved.
- **Root cause:** first-install identity setup reused for replacement.
- **Fix:** read the existing application's supported exported offset, validate it and reuse for replacement imports; generate only on fresh installation. New reviewed archive required; retained archive bytes remain unchanged.
- **Verification:** repeated native imports preserve component IDs and one saved report; wrong/missing context rejects. Business-history preservation remains checked separately.

## BUG-7: Failed committed additive DDL has no bounded automated repair

**Item:** PBI-011.8
**Severity:** high
**Status:** open

- **Symptom:** later migration failure can leave committed DDL and prevent a blind retry.
- **Root cause:** Oracle DDL and migration bookkeeping are separate commit boundaries; selected repair proof was not built.
- **Fix:** one integration-only failed additive migration, retained attempt/evidence, observation-bound reviewed repair artifact and history comparison; no rewrite of applied 005 or universal repair framework.
- **Verification:** fail after committed DDL, block ordinary access, reject changed observations, repair automatically from the exact supported state, preserve twenty sentinel rows/all settings and retain failure/success receipts.

Verification for BUG-2–5: [review correction increment 1](tests/review_fixes_20261018.txt). BUG-2 fixes exact input reconstruction; complete independently provisioned A–H acceptance is still tracked separately. BUG-6/7 remain open until their native experiments/repair pass.

BUG-6 importer correction: native [C experiment](tests/apex_identity_20261018.txt) passes two imports, one private saved report, all region IDs, field snapshots and wrong-target rejection. C is now 1.0.1. The historical patch recipe remains unchanged until a new reviewed archive is built and selected for fresh cycles; bug closure awaits that delivery input.
