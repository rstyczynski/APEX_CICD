# E.17 implementation — in progress

The finalized E.16 correction c7218cd is published at origin and its immutable companion workflow 03f18ca has real native qualification. E.17 reuses those individual Actions steps and one-invocation SQLcl adapter, with generated private input provisioning and actual APEX/ORDS access checks. No historical run is counted as E.17 acceptance. Trial companion commit 5b5de5a dispatches run 45818534213. Outcomes are pending.

The earlier unrun lifecycle.py draft is obsolete and must be removed from the delivered source once its replacement is verified. The platform provisioning helper currently encapsulates multiple native operations; source review must split visible phases before final acceptance under the native-responsibility rule. The login-page observation establishes HTTP delivery only; no authenticated application interaction is claimed. [Checklist](sprint_E.17_checklist.md) tracks remaining work against sources, and [design](sprint_E.17_design.md) records choices.

## Trial 45818534213 — exhausted hosted disk

The two pinned Oracle containers initialized successfully and qualified SQLcl installed. Platform provisioning then lost the runner: check-run 139904448901 reports System.IO.IOException: No space left on device in the runner diagnostic log. `gh run view --log-failed` could not obtain that job's log, and `gh run download` found no artifacts; this is an observed worker failure, not evidence of a platform API failure. The retained check annotation records the exact error. This is recoverable environment work, not an external blocker.

Retry 45819313293 at companion 7e23337 frees unneeded hosted Android/.NET/GHC/CodeQL payloads before explicit pinned Docker startup. The workflow owns this preparation and platform-phase sequencing. SQLcl PROJECT retains export/stage/verify/release/package/deploy. No prepared-host input or credential is transferred. Local smoke initially flagged intentional child-shell quoting (SC2016); the source now explains the intended deferred expansion and the smoke check passes. Native platform qualification remains pending.

## Combined reviewed candidate journey

Trusted testing.yml run 45819877026 on an independent ephemeral runner validates candidate PR 1 head 556adf7 against the trusted report. Actual Oracle greeting, candidate schema identity and private-table denial pass. Workflow-token status publication is denied by HTTP 403. Ordinary merge before validation is refused. The authorized operator checks exact current head and successful required steps, publishes the trusted status through GitHub's native status API, then uses ordinary `gh pr merge --merge --match-head-commit` without admin bypass. PR 1 merges as 1763f1b.

PR 2 changes candidate bytes without changing trusted review. Run 45820491077 fails with `AssertionError: stale Review` in the byte-matching step; candidate SQL execution is skipped. Ordinary merge is refused and the negative PR is closed. Candidate Actions remain disabled; branch protection requires TrustedOracle with strict current-base checks and enforcement for administrators. These are real E.17 observations, rechecked by the integration reader, not reused E.15 pass claims.

Actions owns hosted validation and publication privilege separation. The native GitHub CLI operator publishes a result after inspecting actual terminal outcomes and exact candidate identity; no custom Python pipeline controller sequences those operations. Logs distinguish that authorized operator authority from the restricted job token.

## Full-image progress and authenticated inspection

Run 45820349969 progresses beyond the previous XDB failure through native APEX installation, workspace/user creation and application import, then reaches ORDS installation. It then fails with ORA-65066 when attempting to change common SYS credentials from a PDB. A cancellation request found the run already completed. Run 45822055484 at companion 838c79b tests the connected authenticated APEX/native-row fixture and explicit ORDS uid/gid, proxy-user and fresh stdin password handling. The actual failure occurs before invoking the ORDS installer. Replace this invalid common-user mutation with a newly generated PDB-local E17_ADMIN credential and native DBA grant, matching the supported isolated-regression pattern. Run 45822055484 is cancelled before reaching this known defective statement; the corrected immutable source must be dispatched anew. Raw partial artifacts will be retained where the cancelled job supplies them; only the final successful immutable source can establish complete acceptance.

## Architecture-qualified ORDS retry

Run 45824130390 proves the corrected account/grant syntax but rejects the ARM64 ORDS executable on AMD64. Source 1414877 moves ORDS_IMAGE to the declared job environment, pins the same release's inspected AMD64 digest and introduces early native CLI/private-configuration qualification. Checkout precedes that preflight so its nonsecret results survive in result/. Current run 45826292633 remains a trial until the entire native/application/cleanup journey succeeds.

## Native SYS provisioning and database-before-application ordering

The actual ORDS grant script rejects the attempted local DBA authority with ORA-01031. Use the native image resetPassword command for freshly generated SYS/SYSTEM input, then invoke Oracle's installer as SYS; source 7bded06 records that correction. Source review also aligns the small application fixture with SRS FR-5: native table installation and seeding precede the dependent APEX import. Actions source 5f135bd/run 45828709006 tests that complete corrected sequence. The earlier 45828501708 run was cancelled early; it is not counted as acceptance.
