# APEX CI/CD validation programme

## Purpose

E.x iterations validate architectural ideas through bounded experiments in
the Foundation/Hello/World laboratory. Production completion belongs to later
C.n Construction iterations. Each sprint groups related, independently
checkable backlog outcomes into one coherent capability demonstration.

[PLAN](../PLAN.md) owns assignments and activation, [BACKLOG](../BACKLOG.md)
owns acceptance criteria, and [PROGRESS_BOARD](../PROGRESS_BOARD.md) owns
execution status. [README](../README.md) and [ROADMAP](../ROADMAP.md) provide
orientation. The [laboratory SRS](srs.md), [architecture](architecture.md) and
[test profile](test-profile.md) retain their respective authority.

## Capability sequence

### E.5 — Validate a testable backend behind APEX pages

Demonstrate one greeting rule from its APEX page through a package operation to repeatable utPLSQL tests and useful coverage. Show preserved page feedback, direct invalid-input rejection, a detected regression and independent fixtures, including one cleanup boundary beyond rollback.

Backlog outcomes: PBI-061, PBI-040, PBI-062.

### E.6 — Validate secure component contracts and transaction behavior

Demonstrate a documented component contract used under allowed and denied identity/country contexts, compatible and breaking changes, and competing requests. Establish version classifications and transaction responsibility through observable consumer behavior while retaining whole-application deployment.

Backlog outcomes: PBI-063, PBI-052, PBI-064, PBI-079.

### E.7 — Validate upgrades and traceable application releases

Demonstrate one supported previous-release upgrade with preserved synthetic data, verified database state and a traceable release visible in APEX. Show wrong deployed state and substituted artifacts being rejected; connect source, component contracts, migrations and test evidence to the installed result.

Backlog outcomes: PBI-065, PBI-077, PBI-057.

### E.8 — Validate complete PR candidate testing

Demonstrate one integrated PR candidate from trusted suite selection through deployment, tests and reporting, with PR, scheduled and prerelease applicability. Show cheap failure stopping dependent work and missing, empty, skipped or failed mandatory validation preventing Testing success.

Backlog outcomes: PBI-066, PBI-067, PBI-076.

### E.9 — Validate AI review and ordinary merge decisions

Demonstrate a developer journey from an accurate PR summary and real agent review to a current Review result and a controlled merge alongside Testing. Exercise report changes and revision races, rejected blockers and stale evidence, expected publishers and selected repository controls in a disposable repository.

Backlog outcomes: PBI-068, PBI-069, PBI-070, PBI-071.

### E.10 — Validate secure isolated execution and interrupted cleanup

Demonstrate two candidate streams with separated data, credentials and validator authority, then supersede or interrupt one without harming the other. Challenge the trust boundaries, retry/time limits and scoped cleanup, including one forced-termination orphan; mandatory failures remain visible.

Backlog outcomes: PBI-072, PBI-073, PBI-074.

### E.11 — Validate reproducible delivery and measured feedback

Have a second operator reproduce the selected supported delivery journey with fresh private inputs and pinned tools. Compare cold and warm feedback for that same workload, challenge tool/cache integrity and expose hidden host dependencies before recommending setup or concurrency changes.

Backlog outcomes: PBI-075, PBI-078.

### E.12 — Validate a compatible Foundation upgrade with live data

Demonstrate the compatible language extension with unchanged consumers, retained data and interrupted-upgrade recovery. In the same bounded evolution journey, validate live backfill/catch-up and concurrent change preservation as the prerequisite for the later compatibility bridge.

Backlog outcomes: PBI-048, PBI-081.

### E.13 — Validate the breaking Foundation transition and recovery

Demonstrate the compatibility bridge and one consumer moving to Foundation 2.0 while the other remains on 1.x. Challenge partial dual writes, shared-data visibility and return to legacy operation before demonstrating supported retirement; a failed bridge hypothesis must be resolved before dependent migration.

Backlog outcomes: PBI-082, PBI-049.

### E.14 — Validate component windows and assess the architecture

Demonstrate separate Hello and World migration windows and interrupted-component recovery using the qualified mixed-version fixtures. Review the accumulated evidence and remaining risks in the same handover to propose Construction or further Elaboration; Lifecycle Architecture acceptance remains a separate Product Owner decision.

Backlog outcomes: PBI-050, PBI-080.

## Experiment and evidence boundaries

Reuse one small greeting application and synthetic fixtures. Within each
capability, establish prerequisite behavior before exercising dependent
operations. Record the hypothesis, actor journey, starting state, exact
toolchain and candidate identities, expected and observed outcomes, failure
cases, preservation and cleanup checks, and remaining limitations.

Keep backend tests distinct from manual page-mapping and authentication
checks. Use synthetic identity and country permissions for authorization
experiments. Select exact commands and bounded cases during managed design;
the plan does not claim that these tests or mechanisms already work.

E.12 establishes compatible evolution and catch-up before the breaking
transition. E.13 validates bridge consistency and recovery before dependent
consumer migration. E.14 reuses the qualified fixtures for separate maintenance
windows and reviews the accumulated evidence for a separate architecture
milestone decision. No milestone acceptance or production readiness follows
automatically from completing the planned experiments.

Demonstrate the actual capability and its material failure cases at handover.
A reproducible negative finding can inform a design decision; a failed mandatory
test cannot be recorded as a pass. Preserve backlog criteria when refining or
splitting scope. All future iterations remain Planned until explicitly activated.
