# E.1 — Construction test results

## Current scope

Platform/bootstrap checks are running while application construction continues. The full selected prototype suite remains incomplete. Initial unit skeletons reported two expected pending failures; this was test-harness preparation, not a passing unit gate.

## Observed results

Pinned tool checks passed for SQLcl 25.3.0.274.1210 and Java 21.0.12.1+1. All five effective schema/PDB/workspace mappings passed. Cross-area read/write rejection passed for all five areas. Platform database/HTTP/static-asset smoke passed. A committed retained TEST marker survived disposable qualification recreation. Oracle-error propagation and SQLcl MERGE persistence passed after the wrapper fix.

Foundation Liquibase validation/installation and explicit assembly assertions passed. Its unchanged repeated SQLcl capture matched all 38 source files byte-for-byte. Private-copy import stability and the complete release/browser scenarios remain pending.

## Artifacts

The platform subset passed its current new-code checks: [A1 smoke](test_run_A1_smoke_20261016_185650.log) and [A3 platform integration](test_run_A3_integration_platform_20261016_185649.log), each with one test and zero failures. [Earlier smoke](test_run_A1_smoke_20261016_185316.log) also passed before the script-file wrapper fix. The platform subset has no isolated unit assertions; application unit skeletons remain pending. These results do not establish a pass for the full selected release suite.

[B1 smoke regression](test_run_B1_smoke_20261016_185912.log) passed with one test and zero failures after the current wrapper/provisioning changes.

Earlier interactive command results support the additional Foundation/capture observations above; they are not relabeled as complete gate logs. The implementation record links the current scripts and limitations.
