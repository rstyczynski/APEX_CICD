# E.17 implementation — in progress

The finalized E.16 correction c7218cd is published at origin and its immutable companion workflow 03f18ca has real native qualification. E.17 reuses those individual Actions steps and one-invocation SQLcl adapter, with generated private input provisioning and actual APEX/ORDS access checks. No historical run is counted as E.17 acceptance. Trial companion commit 5b5de5a dispatches run 45818534213. Outcomes are pending.

The earlier unrun lifecycle.py draft is obsolete and must be removed from the delivered source once its replacement is verified. The platform provisioning helper currently encapsulates multiple native operations; source review must split visible phases before final acceptance under the native-responsibility rule. The login-page observation establishes HTTP delivery only; no authenticated application interaction is claimed. [Checklist](sprint_E.17_checklist.md) tracks remaining work against sources, and [design](sprint_E.17_design.md) records choices.

## Trial 45818534213 — exhausted hosted disk

The two pinned Oracle containers initialized successfully and qualified SQLcl installed. Platform provisioning then lost the runner: check-run 139904448901 reports System.IO.IOException: No space left on device in the runner diagnostic log. `gh run view --log-failed` could not obtain that job's log, and `gh run download` found no artifacts; this is an observed worker failure, not evidence of a platform API failure. The retained check annotation records the exact error. This is recoverable environment work, not an external blocker.

Retry 45819313293 at companion 7e23337 frees unneeded hosted Android/.NET/GHC/CodeQL payloads before explicit pinned Docker startup. The workflow owns this preparation and platform-phase sequencing. SQLcl PROJECT retains export/stage/verify/release/package/deploy. No prepared-host input or credential is transferred. Local smoke initially flagged intentional child-shell quoting (SC2016); the source now explains the intended deferred expansion and the smoke check passes. Native platform qualification remains pending.
