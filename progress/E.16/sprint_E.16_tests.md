# E.16 verification

[Checklist](sprint_E.16_checklist.md) owns requirement coverage; [design](sprint_E.16_design.md) owns test scope. A1 smoke and A2 unit pass 1/1 each. A3 integration passes 1/1 against real hosted run 45802390235. Recovered full smoke and unit regression pass 15/15 and 17/17. Full B3 integration is running; no passing result is claimed yet.

Smoke checks source syntax/workflow shape. Unit checks the real provenance guard on controlled inputs; it makes no Oracle claim. Hosted integration downloads actual archives and receipts, verifies both archive digests and immutable workflow identities, checks four rejection outcomes and unchanged target observations, and inspects actual incompatible-tool output. [Source review](sprint_E.16_source_review.md#verified-current-revision) independently reviews exported SQL and release preparation. The native repeat reports zero new changesets and two previously run; both target assertion logs retain ID 1 and the original message. This is bounded table evidence, not full application or independent-host qualification.

## Reproduce the checks

From the repository root, the runner selects the manifest entries defined in the accepted test specification. GitHub CLI must access the private companion, and full regression requires the prepared host's qualified SQLcl/native profiles plus healthy owned database and ORDS services. The runner uses the isolated E.12 database for historical integration and refuses changes to test/executable source during that run. See [test profile](../../docs/test-profile.md) and [manual](user_manual.md).

```bash
cd "$(git rev-parse --show-toplevel)"
bash tests/run.sh --smoke --new-only progress/E.16/new_tests.manifest
bash tests/run.sh --unit --new-only progress/E.16/new_tests.manifest
E16_RUN_ID=45802390235 bash tests/run.sh --integration --new-only progress/E.16/new_tests.manifest
bash tests/run.sh --smoke
bash tests/run.sh --unit
E16_RUN_ID=45802390235 bash tests/run.sh --integration
```

Expected result is zero failed selected entries for each gate. New tests prove only the bounded claims above. Regression re-executes the selected prior behavior on real services; it does not extend its original acceptance scope. Pending/failed native workflow, substituted digest/source/bytes, and wrong build must refuse acceptance. [Failures and recovery](sprint_E.16_bugs.md) distinguish actual failed or interrupted attempts from successful retries. No failure was waived.

## Artifacts

- [test_run_A1_smoke_20261126](test_run_A1_smoke_20261126.log)
- [test_run_A1_smoke_final_20261126](test_run_A1_smoke_final_20261126.log)
- [test_run_A2_unit_20261126](test_run_A2_unit_20261126.log)
- [test_run_A2_unit_final_20261126](test_run_A2_unit_final_20261126.log)
- [test_run_A3_integration_20261126](test_run_A3_integration_20261126.log)
- [test_run_B1_smoke_20261126](test_run_B1_smoke_20261126.log)
- [test_run_B1_smoke_final_20261126](test_run_B1_smoke_final_20261126.log)
- [test_run_B1_smoke_recovered_20261126](test_run_B1_smoke_recovered_20261126.log)
- [test_run_B2_unit_20261126](test_run_B2_unit_20261126.log)
- [test_run_B2_unit_final_20261126](test_run_B2_unit_final_20261126.log)
- [test_run_B2_unit_recovered_20261126](test_run_B2_unit_recovered_20261126.log)
- [test_run_B3_integration_20261126](test_run_B3_integration_20261126.log)
- [test_run_B3_integration_final_20261126](test_run_B3_integration_final_20261126.log)
- [test_run_B3_integration_ready_20261126](test_run_B3_integration_ready_20261126.log)
- [test_run_B3_integration_recovered_20261126](test_run_B3_integration_recovered_20261126.log)
- [test_run_B3_integration_resume_20261126](test_run_B3_integration_resume_20261126.log)

Current native evidence: [retained artifacts](tests/native-current/). Presentation: [package](tests/presentation-package.json), [geometry](tests/presentation-layout.json), [local links](tests/local-links.json).
