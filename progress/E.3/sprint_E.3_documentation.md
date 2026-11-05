# E.3 — documentation

## PBI-058 — 2026-11-05 native release correction

The [correction record](sprint_E.3_release_correction.md) owns changed behavior, actual native execution and limitations. The [final gap reassessment](sprint_E.3_final_gap_analysis.md) replaces the incomplete closing mapping. Required gates use release_correction_tests.manifest: SM-1/SM-058 pass workflow and fail-closed source checks; IT-058 checks the fresh local native evidence and archive/bundle hashes. The actual native commands ran separately and are retained under tests/release-correction. The integration test function is an evidence reader, not a new remote run. Full smoke regression is required. Native release/verify/package, supported-target upgrade/repeat and APEX sessions passed; a fresh disposable-schema attempt failed the inherited seed guard and remains an explicit limitation.
