# E.19 workflow support inventory and dispositions

## Discovery boundary and evidence

[Machine inventory](tests/workflow-inventory.json) records paths, SHA-256 and line-numbered Python references for every tracked `.github` YAML file found by `git ls-files '*yml' '*yaml'` at the accepted starting state plus the initial E.19 actions. This covers the Git pipeline example and sprint-work E.15–E.18 workflow sources. There is no root `.github` delivery workflow. The dedicated E.19 repository owns the new live workflows. Its source is mirrored under `sprint-work/E.19/`; historical files are preserved unchanged. The scan includes hidden directories, correcting the first attempt's incomplete discovery.

## Migrated reusable supporting checks

E.16/E.17/E.18 `check_tool.py` validates SQLcl release/build and metadata. E.19 `actions/tool` replaces it, requiring metadata to enforce NFR-5. Before a native project exists, committed `toolchain.json` declares the approved initialization version; once initialized, the actual `.dbtools/project.config.json` takes precedence. This is not a metadata edit to bypass native compatibility.

E.16/E.17/E.18 `check_output.py` rejects native error text despite a zero process exit. E.19 `actions/output` replaces it and rejects empty output as missing evidence. Native process exit checks remain mandatory.

E.16/E.17/E.18 `provenance.py` binds source, qualified tool build and archive hash with optimization-sensitive assertions. E.19 `actions/provenance` replaces them with unconditional exceptions. The native workflow invokes the action before each deployment. The small `guard.cjs` adapter invokes the same check for existing refusal exercises; it owns no lifecycle operation.

E.15/E.17/E.18 testing.yml inline candidate JSON validation checks open state, main base and exact head/base SHA syntax. E.19 `actions/candidate` replaces it; jq copies already validated fields to Actions environment variables. The trusted workflow still obtains metadata through GitHub API and candidate SQL as data.

E.15/E.17/E.18 testing.yml inline trusted Review validation checks the sole changed file, accepted decision and exact candidate SQL hash. E.19 `actions/review` replaces it. GitHub Actions still owns trusted-source selection, conditions, permissions and publication. Neither action authenticates an arbitrary supplied report by itself.

## Outside reusable supporting-check migration

E.15 `controller.py` is the historical local custom admission/publisher experiment, not invoked by these native hosted workflows. Retain it as historical evidence and regression input. E.15 authority.yml/propose.yml use native GitHub API/Bash, with no Python helper to migrate. The root `scripts/*.py` controllers and local experiment drivers are historical/local executable regression profiles, not Python support checks invoked by the inventoried hosted workflow sources; replacing them would redesign earlier delivery experiments and is outside PBI-087.

E.15/E.17/E.18 `validate.py` performs the actual application regression against Oracle, including greeting, schema identity and denied private-table access. It remains an application test with the pinned oracledb dependency in the separate trusted testing workflow. It is not a pure pipeline support check. This explicit disposition means that separate application-test workflow is not claimed Python-free. Migrated checks, their acceptance workflow and the complete native qualification workflow execute without Python.

E.17/E.18 `provision_host.py` supplies disposable platform inputs, Docker/SQL*Plus provisioning and HTTP readiness. It is per-operation platform glue, outside reusable check actions. E.19 translates it to `host.cjs` solely to run native qualification without Python. Native SQLcl PROJECT lifecycle stages remain separate visible workflow steps. Its native output check reuses the migrated shared implementation; APEX installer archive checksum remains explicit per-operation acquisition validation. It does not create an OCI API interaction. Public Oracle software download uses curl, followed by the same pinned checksum.

E.18 `sample_resources.py` and inline measurement JSON output are telemetry for the completed capacity experiment, not delivery acceptance checks. E.19 does not rerun capacity measurement or introduce a telemetry action. Historical logs, screenshots, Python helpers and measurement source remain untouched.

The earlier `examples/git-pipeline` workflows use native Bash/Git/SQLcl and contain no Python execution. Their PR workflow's `*.py` absence assertion is a Bash repository-content policy, not a Python dependency.

Progress evidence readers, archive export, test harnesses and deck generation are development/evidence tools outside migrated delivery check runtime. `baseline/` contains unchanged historical helper implementations and exact extracted inline checks for controlled benchmark comparison only. `actions/benchmark` is a measurement harness, not a catalogue delivery guard; its Python branch intentionally runs the old solution. No Python-free claim includes that comparison branch.

## OCI decision

None of the inventoried selected checks calls OCI secrets or Object Storage. No OCI feature or dependency is added. If an OCI interaction is later selected, PLAN requires Oracle's official OCI JavaScript/TypeScript SDK; curl or a custom signed REST client is not an approved substitute for that SDK.
