# Sprint E.10 setup

## Contract

The Product Owner authorized activation and autonomous YOLO execution, local commits and closure, with no remote publication. E.10 alone is activated. Test: smoke, unit, integration; Regression: smoke, unit (full suite). The user overrides the manager time limit and local requirement for personal status editing. P8 increment audits replace phase-only commits. Unrelated .codex-cli modifications are preserved. No credentials will be read from scratch.

## Analysis

[Assigned requirements](../../BACKLOG.md#pbi-072-validate-separation-of-proposed-code-and-privileged-validation) and [plan](../../PLAN.md#sprint-e10---validate-secure-isolated-execution-and-interrupted-cleanup) require actual candidate isolation, authority separation, concurrent streams, supersession and scoped cleanup. E.9's capability service explicitly excludes a sandbox; it is context, not isolation evidence. Use separate unprivileged containers for candidate execution and a host controller for validation authority. No SQLcl PROJECT changes are needed. The system boundary is a local laboratory, not GitHub enforcement or production release qualification.

## YOLO decisions

Use the existing named apex-cicd rootless Podman connection: the default endpoint refused connection, and starting the default VM was rejected because apex-cicd is already running. This avoids disruption to retained database workloads. Use synthetic markers only. Phase token accounting is unavailable from the runtime; no measured token count is claimed.
