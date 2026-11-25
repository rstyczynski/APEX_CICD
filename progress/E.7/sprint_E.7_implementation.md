# E.7 — Implementation status

[Setup](sprint_E.7_setup.md) owns scope, [design](sprint_E.7_design.md) owns the intended experiment, [tests](sprint_E.7_tests.md) owns measured results, and [handover](sprint_E.7_handover.md) owns remaining closure gates. [The walkthrough](sprint_E.7_increment_demo.md) provides operating steps.

## Implemented

The isolated E7_APP/E7_CONSUMER fixture retains greeting 7 through an additive 1.0.0 to 1.1.0 schema upgrade. The assertion checks actual dictionary state and reference contents independently of the migration ledger. Five faults are detected by their specific STATE label and restored in finally. The retained row and greeting consumer result are checked after upgrade and repeat. APEX app 810703 is installed with corresponding metadata and a public release information page. Native Chrome accessibility and screenshot inspection showed release 1.1.0 in the region and footer; HTTP checks cover all three installation stages.

The integrity prototype hashes migration, application, contract, configuration, report and source snapshot bytes. Verification requires a separately trusted manifest digest before upgrade/application import. Content-addressed archive names preserve distinct manifests. ZIP timestamps are fixed for deterministic output. The receipt distinguishes the Git selected exact committed revision from later evidence commits; no remote release/tag publication is claimed.

## Finalization and qualified boundaries

The source checkpoint b2e8b9b15916783278727188f51601cdc3adb743 closes the earlier provenance and verification gaps. Every selected release source must match the committed revision exactly. The baseline ZIP is verified before even the isolated owners/workspace are created; SQL migrations and APEX imports use bytes read from that verified ZIP. Each execution selects a fresh E7R owner and unused app ID, proving a real database baseline-to-upgrade journey rather than only reimporting baseline APEX metadata over an upgraded database. The visible release region exposes the same exact source revision. The final receipts bind that revision, component contracts, configuration, migration bytes, report bytes and actual target observations. The field source_base_commit retains its old JSON name for compatibility, but now identifies the exact clean source revision.

The declared supported upgrade is this bounded explicit SQL-bundle laboratory release, not production SQLcl PROJECT deployment. The latter remains an architecture requirement outside these Elaboration criteria. Assertions run as a trusted database operator and validate the declared consumer EXECUTE grant; they do not demonstrate consumer password authentication. Hashes rely on an externally trusted digest pin and are not publisher signatures. Accounts have no password authentication. Targets and synthetic rows are retained for inspection; no automatic broad cleanup or interrupted-process recovery is claimed.

## Corrections and preservation

The first baseline seed used two SQL statements on one line and SQLPlus rejected the trailing command. The corrected seed uses separate commands and a bounded resume merge. The final state was checked successfully. Full regression initially wrote fresh E.5/E.6 unit logs to their default evidence locations; the new logs were retained under E.7 and historical files restored byte-for-byte from Git. No prior sprint changes remain. Database accounts use NO AUTHENTICATION; no private passwords were created in scratch.
