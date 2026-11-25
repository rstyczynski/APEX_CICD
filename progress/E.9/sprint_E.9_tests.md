# E.9 verification

A1 smoke, A2 unit and A3 real local Git integration PASS. B1 full smoke
(7 entries) and B2 full unit (6 entries, including real Oracle suites) PASS.
No selected gate skipped. Initial red test failed importing the absent controller
as specified. Unit coverage comprises three groups with multiple negative cases.
The final integration rerun additionally retained candidate.bundle.

These gates establish only local behavior; authenticated direct-write refusal,
actual publisher identity, immutable server retention and atomic merge remain
unverified. They block acceptance despite passing automated gates.

## Artifacts

[test_run_A1_smoke_20261125_190609.log](test_run_A1_smoke_20261125_190609.log)

[test_run_A2_unit_20261125_190609.log](test_run_A2_unit_20261125_190609.log)

[test_run_A3_integration_20261125_190609.log](test_run_A3_integration_20261125_190609.log)

[test_run_B1_smoke_20261125_190609.log](test_run_B1_smoke_20261125_190609.log)

[test_run_B2_unit_20261125_190609.log](test_run_B2_unit_20261125_190609.log)

[Red test](tests/red.log), [journey](tests/journey.json), [retained source](tests/candidate.bundle), [reports](tests/reports/) and [GitHub read-only permissions](tests/github-readonly-access.json).

[Design](sprint_E.9_design.md) owns expected outcomes; [handover](sprint_E.9_handover.md) owns the pending decision.
