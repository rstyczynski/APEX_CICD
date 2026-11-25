# E.10 increment walkthrough

## Goal and starting state — slides 1–4

Demonstrate separation of proposed code and validator authority, concurrent private streams and interruption recovery. [PLAN](../../PLAN.md#sprint-e10---validate-secure-isolated-execution-and-interrupted-cleanup) owns scope; [design and acceptance checklist](sprint_E.10_design.md) maps PBI-072/073/074 to tests. The [manual](user_manual.md) owns operating limitations, and [handover](sprint_E.10_handover.md) records what actually happened.

The starting environment is the existing running apex-cicd rootless Podman VM, Python 3 and Podman 6.0.0. No database or SQLcl operation occurs. The developer operates this journey; the Product Owner can inspect each source and result. No production secrets are used.

## 1. Prepare — slides 5–6

Position at the repository root and inspect the actual runtime. The named connection avoids a stale default endpoint. These commands do not restart or modify existing workloads.

```bash
cd "$(git rev-parse --show-toplevel)"
podman --connection apex-cicd info
podman --connection apex-cicd pull docker.io/library/alpine@sha256:49340b346798875b5592e5d420241f2f9cfba5f47e62ebb1446a1b34734e898f
```

Expect successful runtime information and a verified image pull. If the VM is unavailable, repair its named connection before running the driver; do not automatically recreate a retained VM.

## 2. Inspect the hidden operations — slides 7–8

The driver below executes candidate shell commands in real containers, using the controller in `scripts/isolated_execution.py`. Each candidate runs as UID 65534 with a read-only root filesystem, no capabilities, no-new-privileges, no network, and a private size-limited /work tmpfs. No host directory, runtime socket or privileged credential is passed. The candidate writes its own synthetic credential into /work/private; the trusted controller reads it to verify stream separation. Candidate commands try to read a private host policy path, find a privileged token/socket, write protected policy and mount a filesystem. Any unexpected privilege aborts the test.

The host registry deduplicates stream/revision/event admission, advances only the selected stream and refuses duplicate or stale completion. Supersession removes old PR A while B and release remain running. A deliberate retry uses a distinct event. Review command text is JSON data, never passed to a shell. This is a local PR-stream abstraction, not a remote GitHub adapter.

Inspect source using the VS Code `code` command when available; it must be on PATH. Read the source before execution, particularly cleanup scope.

```bash
code scripts/isolated_execution.py
code tests/execution_lab.py
```

## 3. Execute and inspect — slides 7–11

The driver performs the concurrent journey above, then success and failed-assertion cleanup, a timed-out sleep, three finite unavailable-service attempts, a SIGKILL orphan and independent reaping. It refuses foreign-session cleanup, deliberately breaks cleanup transport and recovers after restoring it. Every created resource is session-labeled. A final reaper runs even after assertions fail. No global prune is used. Expected assertion failures remain nonzero candidate outcomes and are checked as such; they are not retried until success.

```bash
python3 -u tests/execution_lab.py
```

Expect PASS lines identifying concurrency, bounded failure, privilege denial and orphan recovery, followed by the pinned IMAGE identity. Any traceback means the journey failed. The unavailable transport and candidate assertion failure are expected negative cases, not silent exceptions. A successful driver proves its listed laboratory assertions, not production qualification.

Inspect the current recorded gate output and requirement-specific interpretation. Re-running the driver creates fresh ephemeral resources and does not overwrite the recorded logs.

```bash
code progress/E.10/test_run_A3_integration_20261125_192849.log
code progress/E.10/sprint_E.10_tests.md
```

## 4. Review results and limits — slides 12–15

Use [test report](sprint_E.10_tests.md) for each gate and [implementation](sprint_E.10_implementation.md) for retained behavior. There is no persistent fixture/cache mount, so candidate files vanish with removal. The registry is in memory and trusted-host-only; forced-termination recovery reclaims containers rather than reconstructing authoritative history. No production identity, hostile kernel, Oracle deployment or hosted branch protection claim follows.

Discuss the observed results and record actual feedback in [handover](sprint_E.10_handover.md). The deck supports this real journey; opening slides alone does not demonstrate isolation. No new sprint is activated.
