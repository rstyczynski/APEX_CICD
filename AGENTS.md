# RUP Strikes Back Process

This project uses the `RUPStrikesBack` submodule as its agentic delivery method.

## Process entry point

The Codex method entry point is `.agents/skills/rup-strikes-back/SKILL.md`. Its references map Codex invocation to the canonical manager, agent-role, and rule procedures in `RUPStrikesBack/.claude/commands/` and `RUPStrikesBack/rules/`.

The root `BACKLOG.md` is the Product Owner’s prioritized backlog. The root `PLAN.md` is the sprint plan and identifies the active sprint. When present, `RUPStrikesBack.patch/` is an optional local wrapper; its root `RUP_patch.md` is the compatibility entry point for the full local policy at `RUPStrikesBack.patch/RUP_patch.md`.

For an explicit request to start, plan, inspect, or manage a RUP Strikes Back sprint in Codex, read and use `.agents/skills/rup-strikes-back/SKILL.md`. Do not load that workflow for ordinary product, documentation, or implementation requests.

## External expert review

For a request to start or continue an external expert review, use
`.agents/skills/rup-external-review/SKILL.md`. Codex coordinates the round,
prepares prompts for the Product Owner to relay, reads expert replies from
files and writes engineering responses and decisions. The skill owns the
external-review procedure; review alone does not start or close a sprint.

## Mandatory RUP artifact routing

RUP Strikes Back procedures are mandatory for every change to its managed
artifacts. Before changing `BACKLOG.md`, use
`.agents/skills/rup-backlog/SKILL.md`; before changing `PLAN.md` or a sprint
status, use `.agents/skills/rup-sprint/SKILL.md`; and before changing
`PROGRESS_BOARD.md`, use `.agents/skills/rup-progress/SKILL.md`. For an active
sprint cycle, use `.agents/skills/rup-strikes-back/SKILL.md` and the phase
adapters it selects.

When a request affects more than one managed artifact, read and follow every
applicable skill before editing. Do not infer a procedure from prior turns or
conversation context. If the canonical method and local patch do not state how
to proceed, stop and request a Product Owner decision; do not invent a state,
transition, or artifact format.

## Starting a sprint

Do not start a RUP cycle automatically. Start one only when the Product Owner explicitly requests it and the selected sprint has `Status: Progress` in the root `PLAN.md`.

Before executing the cycle:

1. When the optional wrapper is present, read `RUP_patch.md`, then `RUPStrikesBack.patch/RUP_patch.md`.
2. Read the Codex skill's manager adapter and only the phase adapters selected by the iteration profile.
3. Read the canonical submodule procedures identified by those adapters.
4. Apply the local wrapper only where it conflicts with or refines the generic method.

Codex does not natively register the submodule's Claude slash commands. An explicit request to use the `rup-strikes-back` skill for the active sprint is the Codex invocation.

## Scope

The submodule’s instructions describe the adopted delivery method. They do not authorize unrelated actions such as remote pushes, copying submodule policies wholesale, or changing project scope without a Product Owner request.

## Environment configuration and temporary files

By explicit Product Owner instruction, `.local-apex/` is disposable scratch only:
download caches, temporary checkouts, build outputs and diagnostic evidence. Never
use it as the authoritative store for environment settings, credentials, saved
connections, runner registration or executable-path environment files.

GitHub Actions must declare tool setup and configuration explicitly. Use GitHub
environment/repository variables for nonsecret settings and GitHub secrets for
credentials. Generate required private connection files and mappings in
`RUNNER_TEMP`, clean them on success or failure, and use `GITHUB_PATH`,
`GITHUB_ENV` or step outputs for generated job paths. Persistent runner
registration belongs in the runner's managed host directory outside the
checkout. Preserve historical evidence without presenting its retired local
configuration instructions as the current setup.

### Temporary prepared-host credential accommodation — 2026-11-04

The Product Owner explicitly approved retaining read-only lookup of the existing
E.1/E.2 `.local-apex/e1-secrets.json` record on the already prepared E.3 host.
This narrow R1-L1 deferral preserves requested Builder, author-schema and LAB_USER
password retrieval; it does not authorize creating new settings/credentials in
scratch, copying the record to another host, or using it in GitHub jobs. The
record is a retained dependency while this exception applies and must not be
discarded as disposable scratch. Do not move/delete it or introduce a new store.
GitHub environment secrets remain the job authority and native author profiles
remain outside checkout scratch. End the accommodation when a compliant source
remedy is selected; reconsider before new-host reproduction, scratch cleanup or
expanding this exception. See the [review decision](progress/E.3/sprint_E.3_handover_review-1-decisions.md#r1-l1--product-owner-policy-choice-required).
This is a temporary prepared-host exception, not production NFR-4 compliance.

## SQLcl PROJECT toolchain compatibility

Treat [SRS NFR-5](docs/srs.md#quality-requirements-and-initial-release) as a
production requirement. For every accepted Git state, the running SQLcl release
must match `.sqlcl.version` in `.dbtools/project.config.json`; developer and
pipeline processing must use the same approved release and qualified build.
Discovering an executable or installing a newer SQLcl does not satisfy this rule.
Check compatibility before export, stage, verify, package or deployment and
stop on a mismatch before changing source/distribution files or target state.
Record the actual release/build; pin automated downloads and their checksums.

Do not silently edit the project version to bypass SQLcl's native check. An
upgrade is a reviewed change to project metadata, tool setup and version pins,
followed by native pipeline and data-preservation validation. Multiple tool
versions may coexist; select the version required by the Git state being
processed, including a previously released tag. See the
[architecture policy](docs/architecture.md#sqlcl-project-toolchain-compatibility).
