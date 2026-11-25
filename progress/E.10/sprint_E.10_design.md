# Sprint E.10 design

Status: Accepted autonomously under the authorized YOLO mode.

## Architecture and actor journey

The developer supplies candidate shell text. The trusted operator starts concurrent PR and release containers; the validator alone owns policy, event deduplication and authoritative results. Candidate containers have no host mounts, network, runtime socket or privileged token. Root filesystem is read-only, capabilities are dropped, no-new-privileges is set and each container has private ephemeral /work data. Review text is serialized as JSON, never evaluated. These are implementation choices, not additional acceptance requirements. The trusted host and Podman VM remain outside the threat model.

The controller keys events by stream/revision/event; duplicate admission returns the same run. A new PR revision cancels only its prior run. A deliberate retry requires a new event identity. Completion requires the current generation. Cleanup requires the controller's random session label plus exact resource identity and verifies removal. SIGKILL can bypass finally; a separate reaper lists only that session's labeled resources. Finite subprocess deadlines and classified retries bound unavailable-service behavior. Assertion failures are never retried.

### Testing Strategy

Use planned smoke/unit/integration and full smoke/unit regression. Smoke checks syntax. Unit checks event deduplication, supersession, stale completion, release independence, retry classification and inert text. Integration runs actual containers concurrently, adversarial candidate commands, success/failure/timeout/cancellation cleanup, deliberate cleanup failure and forced-termination orphan recovery. No mock result establishes container isolation. Tests are in the execution domain, not sprint-named files.

## Test Specification and requirement-to-evidence checklist

SM-1: compile controller and lab. Expected success; prerequisite only.

UT-1: scheduler and retry unit cases. PBI-073 deduplication, permitted retry, stale completion and own-stream cancellation; PBI-074 transient maximum and one assertion attempt. Expected exact counters and refusal. PBI-072 JSON shell text round trip must create no file.

IT-1: real Podman laboratory. PBI-072 denied marker/policy/release paths and privilege escalation; JSON command remains inert; scan captured output and retained reports for marker. PBI-073 concurrently running PR A, PR B and release, separate private files and credentials, supersede A only, refuse stale A and preserve B/release. PBI-074 success, assertion failure, timeout, cancellation and SIGKILL orphan must leave no session resources after recovery; deliberate cleanup failure must be reported and repaired. Pending until fresh evidence is recorded.

## Decisions and limits

Use local container streams as the laboratory PR abstraction: the backlog requires candidate streams, not remote PR publication. Remote pushes remain prohibited. Synthetic markers are generated in memory and never printed. Pinned image digest will be recorded after acquisition. No production credential, host escape resistance against kernel vulnerabilities, Oracle schema isolation or hosted GitHub enforcement is claimed.

## Related authority

[SRS](../../docs/srs.md) owns full product requirements; [architecture](../../docs/architecture.md) owns production design; [test profile](../../docs/test-profile.md) owns project checks. This design is limited to the assigned backlog experiment. [Verification](sprint_E.10_tests.md) owns observed evidence and [walkthrough](sprint_E.10_increment_demo.md) owns operations.
