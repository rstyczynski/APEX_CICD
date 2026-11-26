# E.19 test execution — ongoing

Initial Node unit contract run passes three groups, recorded in [initial-unit.log](tests/initial-unit.log). These are synthetic valid/negative file contracts. Real [hosted run 45873741697](https://github.com/rstyczynski/APEX_CICD_E.19/actions/runs/45873741697) passes three valid catalogued actions and expected malformed provenance rejection. Its mutation sentinel step is skipped; the final assertion verifies rejection and absence of the file. This is a filesystem orchestration contract, not proof of Oracle target preservation. Full action-level negative coverage, native behavior and timing comparison remain pending.

Full unfiltered smoke regression passes 17/17 manifest entries; full unfiltered unit regression passes 19/19. Full integration regression is not yet run. These counts are manifest entry counts, not unique acceptance scenarios. New-code A1/A2/A3 manifest gates have not yet been registered/executed; initial direct Node execution is supplemental evidence only. No six-gate pass is claimed.

## Artifacts

[Initial unit log](tests/initial-unit.log), [hosted metadata](tests/initial-hosted-run.json), [hosted log](tests/initial-hosted-run.log), [exact hosted workflow](tests/hosted-checks.yml), [full smoke regression](tests/regression-smoke.log), [full unit regression](tests/regression-unit.log).
