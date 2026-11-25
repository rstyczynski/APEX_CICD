# E.7 — Implementation status

[Setup](sprint_E.7_setup.md) owns scope, [design](sprint_E.7_design.md) owns the intended experiment, [tests](sprint_E.7_tests.md) owns measured results, and [handover](sprint_E.7_handover.md) owns remaining closure gates. [The walkthrough](sprint_E.7_increment_demo.md) provides operating steps.

## Implemented

The isolated E7_APP/E7_CONSUMER fixture retains greeting 7 through an additive 1.0.0 to 1.1.0 schema upgrade. The assertion checks actual dictionary state and reference contents independently of the migration ledger. Five faults are detected by their specific STATE label and restored in finally. The retained row and greeting consumer result are checked after upgrade and repeat. APEX app 810703 is installed with corresponding metadata and a public release information page. Native Chrome accessibility and screenshot inspection showed release 1.1.0 in the region and footer; HTTP checks cover all three installation stages.

The integrity prototype hashes migration, application, contract, configuration, report and source snapshot bytes. Verification requires a separately trusted manifest digest before upgrade/application import. Content-addressed archive names preserve distinct manifests. ZIP timestamps are fixed for deterministic output. The receipt distinguishes the Git base commit from bundled working source; this is not yet an accepted Git release/tag trace.

## Remaining implementation gaps

The first baseline database setup runs directly before bundle verification. The bounded integrity tests reject substitution, but do not yet prove that every database mutation is behind the verification boundary. The receipt's Git identity is a base commit plus bundled source files, rather than the selected accepted Git release required for full PBI-077/057 acceptance. The schema consumer assertion runs through the trusted operator connection, rather than proving an ordinary consumer login. Production SQLcl PROJECT installation/upgrade and migration-history verification are not qualified by these small SQL bundles. These gaps must be resolved before claiming completion; the design has not been weakened to hide them.

## Corrections and preservation

The first baseline seed used two SQL statements on one line and SQLPlus rejected the trailing command. The corrected seed uses separate commands and a bounded resume merge. The final state was checked successfully. Full regression initially wrote fresh E.5/E.6 unit logs to their default evidence locations; the new logs were retained under E.7 and historical files restored byte-for-byte from Git. No prior sprint changes remain. Database accounts use NO AUTHENTICATION; no private passwords were created in scratch.
