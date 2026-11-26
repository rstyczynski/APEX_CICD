# E.16 implementation

## Current named-Actions correction — PBI-084

The Product Owner requested removal of Python lifecycle orchestration. [The accepted correction design and checklist](sprint_E.16_actions_refactor.md) records implementation boundaries and fresh acceptance status. [The original closure](sprint_E.16_closure.md) preserves the earlier baseline; its passing results do not prove this refactor. The authorized implementation repository is `rstyczynski/APEX_CICD_E.16`, mirrored in [sprint-work/E.16](../../sprint-work/E.16).

GitHub Actions sequences individual export, stage, verify, release, package, install, upgrade, repeat, assertion and refusal steps. SQLcl PROJECT performs native release operations. Git commands in the steps commit generated source and release preparation; jq/sha256sum bind source, build, reviewed inputs and archive bytes. Separate digest-pinned Oracle services retain native schema qualification and isolate author from target. Approved SQLcl 25.4.1.022.0618 is checksum-pinned and measured before each native invocation; native metadata must match 25.4.1.0. No production project metadata is upgraded or bypassed.

## Supporting files and their limits

The [workflow](../../sprint-work/E.16/.github/workflows/native.yml) owns sequencing and visible stage outcomes. The [SQLcl adapter](../../sprint-work/E.16/sql.sh) performs one invocation per call: measured tool preflight, error-exit directives, selected connection, streamed/retained output and output validation. It contains no lifecycle loop or next-stage decision. Saved connections and temporary inputs live in RUNNER_TEMP; traps and an always-run cleanup remove private connection material. Hosted service disposal removes the experiment databases.

[check_tool.py](../../sprint-work/E.16/check_tool.py) reads measured identity and metadata. [check_output.py](../../sprint-work/E.16/check_output.py) rejects native SQL/PROJECT errors including nonzero verification counts even when the process returns zero. [provenance.py](../../sprint-work/E.16/provenance.py) compares selected source, measured approved build and exact archive digest before deployment. These Python checks launch no subprocesses. The former lifecycle.py is removed. The [integration evidence reader](../../tests/native_hosted.py) independently reads GitHub job steps and downloaded artifacts; it does not orchestrate delivery.

These helpers fill narrow validation/invocation gaps and support Actions/SQLcl/Git rather than replace them. The [standing project rule](../../AGENTS.md#use-core-technologies-for-their-native-responsibilities) applies during this correction and all future sprints. A core-technology mismatch requires stopping and reporting to the Product Owner before any substitute is built. No such mismatch is established here: the native tools support the required behavior.

## Operating procedure and verification

The [manual](user_manual.md) owns prerequisites, supported tasks and recovery. The [walkthrough](sprint_E.16_increment_demo.md) gives the complete significant SQL and commands, expected retained row, refusal behavior and current slide map before invocation. The public operator interface is native.yml workflow dispatch; there is no custom Python lifecycle CLI. E16_RUN_ID selects the actual run checked by the integration reader.

[The correction record](sprint_E.16_actions_refactor.md) tracks fresh R1–R8 evidence. [The source review](sprint_E.16_source_review.md) links generated release history, native SQL, receipts and target observations. Production multi-user authority and full APEX/ORDS clean-host reproduction remain outside the bounded table experiment. The prototype is retained as experiment source, not promoted as a production delivery engine.
