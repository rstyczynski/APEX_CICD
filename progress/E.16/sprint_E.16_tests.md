# E.16 verification

The original closure/evidence below describes the Python-controller baseline. The authorized [named-Actions correction](sprint_E.16_actions_refactor.md) owns current refactor acceptance and fresh verification; prior completion does not prove the changed workflow.

[Checklist](sprint_E.16_checklist.md) owns requirement coverage; [design](sprint_E.16_design.md) owns test scope. A1 smoke and A2 unit pass 1/1 each. A3 integration passes 1/1 against real hosted run 45802390235. Recovered full smoke and unit regression pass 15/15 and 17/17. Full B3 integration passes 25/25; the enclosing stable-source/cleanup wrapper exits zero.

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

## Final gate results — PBI-084

| Gate | Passed / selected | Evidence |
|---|---|---|
| A1 smoke | 1 / 1 | test_run_A1_smoke_final_20261126.log |
| A2 unit | 1 / 1 | test_run_A2_unit_final_20261126.log |
| A3 integration | 1 / 1 | test_run_A3_integration_20261126.log |
| B1 smoke | 15 / 15 | test_run_B1_smoke_recovered_20261126.log |
| B2 unit | 17 / 17 | test_run_B2_unit_recovered_20261126.log |
| B3 integration | 25 / 25 | test_run_B3_integration_ready_20261126.log |

All selected gates pass with zero waived failures. The fresh E.15 hosted dependency run is 45806529936, success at 3f760373127b1ea5c2e74a80833ebfa6d8cd0536. The E.16 native reader checks immutable run 45802390235. The final full wrapper completed its source-hash comparison and removed its disposable ORDS container/volume. Its exact source snapshots and environment evidence are retained under [regression replay](tests/regression-replay/progress/E.12/tests/legacy-regression/run-20261126T114425-80613/). Historical tracked artifacts were restored after retaining their fresh replay outputs under E.16; raw paths inside those outputs describe execution time. [The replay index](tests/regression-replay/index.json) maps all 313 preserved files. Failed/interrupted earlier attempts remain diagnostic evidence, not passing gates.

## Fresh named-Actions correction verification

The [correction record](sprint_E.16_actions_refactor.md#final-verification-and-acceptance) supersedes the baseline table for the changed implementation. Fresh A1/A2/A3 pass 1/1 each; unfiltered B1/B2/B3 pass 15/15, 17/17, 25/25 at pinned E.16 source a2e95ea. Its full wrapper exits zero with unchanged source snapshots and scoped cleanup. [The machine-readable receipt](tests/actions-refactor/verification.json) records the exact tested source and workflow identities. No failed or interrupted attempt is counted as a pass.

## Actions correction artifacts

The successful gate logs are [A1](tests/actions-refactor/README.md#read-the-retained-evidence), [A2](tests/actions-refactor/README.md#read-the-retained-evidence), [A3](tests/actions-refactor/README.md#read-the-retained-evidence), [B1](tests/actions-refactor/README.md#read-the-retained-evidence), [B2](tests/actions-refactor/README.md#read-the-retained-evidence) and [B3](tests/actions-refactor/README.md#read-the-retained-evidence). Earlier [A1](tests/actions-refactor/README.md#read-the-retained-evidence), [A2](tests/actions-refactor/README.md#read-the-retained-evidence), [A3](tests/actions-refactor/README.md#read-the-retained-evidence), [B1](tests/actions-refactor/README.md#read-the-retained-evidence), [B2](tests/actions-refactor/README.md#read-the-retained-evidence) and the [interrupted B3](tests/actions-refactor/README.md#read-the-retained-evidence) are retained as earlier attempts. Failed clone-layout runs are retained under [symlink-layout-attempt](tests/actions-refactor/README.md#read-the-retained-evidence) and [tool-home-layout-attempt](tests/actions-refactor/README.md#read-the-retained-evidence). The correction record explains observed failures, alternatives and the successful native Git isolation remedy. [Native evidence](tests/actions-refactor/README.md#read-the-retained-evidence), [workflow steps](tests/actions-refactor/workflow.json), [source review](tests/actions-refactor/source-review.json), [replay index](tests/actions-refactor/README.md#read-the-retained-evidence) and [final presentation validation](tests/actions-refactor/presentation-final.json) complete the evidence chain.

Current raw gate paths are archive members A1-pinned.log, A2-pinned.log, A3-pinned.log, B1-pinned.log, B2-pinned.log and B3-pinned.log in [the retained evidence archive](tests/actions-refactor/README.md#read-the-retained-evidence). The per-member manifest and extraction procedure preserve complete raw logs, including native formatting.

## Native workflow technical reference

The [native release workflow reference](native_release_workflow.md#assert-limitation) records the assertion/optimization boundary. The existing native run demonstrates refusal in its observed execution environment; it does not prove provenance checks with `-O`, `-OO` or effective `PYTHONOPTIMIZE`. The test-side evidence reader also uses assertions.
