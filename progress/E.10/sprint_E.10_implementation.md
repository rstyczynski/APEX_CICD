# E.10 implementation

## Delivered prototype

[Design](sprint_E.10_design.md) defines the bounded experiment. [Controller](../../scripts/isolated_execution.py) provides a locked in-memory admission/result registry, bounded timeout classification, JSON review serialization and an owner-scoped Podman lifecycle. [Real integration driver](../../tests/execution_lab.py) executes concurrent containers and failure/recovery paths. No source from E.9 was changed; its host-trust limitation is addressed by a separate execution boundary. Retain this as a laboratory prototype, not a production scheduler.

## User documentation

Use the [complete walkthrough](sprint_E.10_increment_demo.md) and [manual](user_manual.md) for prerequisites, command explanations, normal operation, expected outputs and recovery. The entry command is `python3 -u tests/execution_lab.py` from the Git root. No arguments are required. The pinned image, named connection and resource restrictions are constants recorded in the design. Internal `wait` accepts a deadline, `bounded` accepts one to three attempts, and `Containers` accepts an optional recovery session. Invalid ownership, stale completion and exhausted deadlines raise errors. A candidate assertion's code 1 is retained and verified rather than retried.

## Material decisions and observed repairs

The default Podman socket refused connection. Starting its default VM failed because the existing apex-cicd VM was running. Selecting `--connection apex-cicd` succeeded without altering defaults or restarting retained workloads. The presentation finalizer initially lacked RUNTIME_NODE_MODULES; setting it to the installed primary runtime repaired import validation. These are recovered environment issues, not blockers.

Synthetic trusted-policy marker exists only in a temporary host file and is not mounted. Candidate credentials differ by stream and are kept in private tmpfs. Candidate source has no controller object or publisher/release credential; JSON review text is inert. The experiment does not establish production NFR-4 or full SRS FR-6 Oracle workspace/application separation.
