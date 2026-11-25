# E.10 operating reference

The [walkthrough](sprint_E.10_increment_demo.md) is the complete execution order and explains scripts before invocation. It requires Python 3, Podman, the running apex-cicd named rootless connection and the pinned Alpine image. VS Code's code command is optional for source viewing; a text reader is an equivalent inspection method.

The [controller](../../scripts/isolated_execution.py) is a trusted laboratory API, not a public service. Never expose its Podman connection, session identifier or Registry object to candidate code. No host mounts or production credentials are supported. The [design](sprint_E.10_design.md) owns policy decisions and [test report](sprint_E.10_tests.md) owns verified outcomes.

Each Containers instance owns a random e10.session label. cleanup checks ownership before removal; reap discovers only that session. Keep the session value available to a trusted recovery operator after a killed controller. Do not prune globally. Transport/permission failures raise errors and must remain visible until recovery. In-memory event/results state does not survive controller restart; this prototype cannot serve as a production durable scheduler. Each CLI call is bounded at 30 seconds and candidate wait at the caller deadline; cleanup adds its own bounded calls.
