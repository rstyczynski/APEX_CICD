# E.11 walkthrough — reproducible candidate execution

## Goal and starting state — slides 1–3

Reproduce the bounded E.10 container candidate boundary from clean tracked source and compare empty-download-cache and reused-tool execution. [PLAN](../../PLAN.md#sprint-e11---validate-reproducible-delivery-and-measured-feedback) owns the second-operator requirement. [Design](sprint_E.11_design.md) identifies the exact acceptance criteria. [Tests](sprint_E.11_tests.md) owns observed results; [handover](sprint_E.11_handover.md) owns remaining acceptance. The [editable deck](sprint_E.11_increment_demo.pptx) follows this sequence.

This slice supports Linux ARM64 containers through the declared Podman connection only. It does not install APEX, deploy SQLcl PROJECT or reproduce an entire fresh host. Python 3, Git, curl, tar and a running accessible Podman service are required. For viewing files, install the VS Code `code` command on PATH. A second operator must supply their own private service access; do not copy retained credentials or the E.1 secrets record. No credential record is needed by the candidate itself: every run generates a fresh synthetic private input in memory.

## 1. Inspect prerequisites — slides 4–5

Position the shell in the cloned repository. Inspect the actual service, which must support ARM64 image execution. The selected local connection is explicitly named apex-cicd. A new operator may configure that connection using their own Podman-supported SSH access; the experiment does not provision the service or supply a private key.

```bash
cd "$(git rev-parse --show-toplevel)"
git status --short
podman --connection apex-cicd version
```

Expected: accessible client/server version output. Qualification evidence used client 6.0.0 and server 6.0.2. An unreachable endpoint must be repaired before running. No running database or retained container should be stopped. The driver checks cleanliness of its new clone, not the user's working checkout.

## 2. Understand and execute the driver — slide 6

The driver resolves HEAD, clones that revision into a temporary checkout and verifies no tracked/untracked changes. It loads scripts/isolated_execution.py from that clone. It obtains Alpine 3.23.0 aarch64 minirootfs from the pinned HTTPS release URL, checks the hardcoded SHA-256, imports a uniquely labelled disposable image and uses the clean controller to run the candidate. The candidate tests denied writes/socket paths, prints BusyBox identity and verifies its own fresh private input in private tmpfs. It never prints that input. No retained credential files or business data are read. Each of three empty-cache acquisitions is followed by a warm cache hit. Import, execution and cleanup happen every time. Cache corruption and a wrong release are rejected before import; no failing assertion is retried into success.

All downloaded caches, clones, containers and imported images are temporary. Retained output is the nonsecret JSON receipt only. The only option is required --output. Choose a new receipt path to preserve earlier observations. Execution is unattended; there is no guided interactive runner and no simulated human inspection.

```bash
python3 scripts/reproducible_delivery.py --output /tmp/e11-independent.json
```

Expected: six PASS sample lines, cold 4038406 bytes and warm zero bytes, then a final PASS covering checkout, integrity and cleanup. A nonzero command or unexpected runtime identity fails the run. Stop and inspect the error; repair its cause and rerun with a new output path. Do not suppress errors or infer success from an older receipt.

## 3. Inspect the result — slide 7

Use the actual receipt, rather than a retained claim, to check all six measurements. source_revision identifies the checkout and source_sha256 identifies the executed clean controller. tools records exact observed identities. statistics contains sample count, median and nearest-rank 95th percentile in seconds for each phase. Credentials are neither included in the receipt nor cached.

```bash
code /tmp/e11-independent.json
```

For the verified implementor result, inspect the checked-in receipt:

```bash
code progress/E.11/tests/benchmark.json
```

The copyable driver command was executed with that checked-in output path during qualification; the independent filename above is an output destination, not a required pre-existing input. VS Code viewing is an operator instruction; no GUI inspection by the Product Owner is claimed.

## 4. Show rejection and interpret measurements — slides 8–12

The unit entry checks pinned-byte acceptance, wrong-release rejection, corrupt-byte rejection and percentile calculation using synthetic bytes; it does not establish runtime compatibility. The integration driver additionally challenges the actual cache and records real runtime identity. Run this focused check to inspect explicit PASS output without new downloads:

```bash
bash tests/run.sh --unit --new-only progress/E.11/new_tests.manifest
```

Compare actual phase statistics in the receipt. Cold means an empty experiment download cache, not cold host storage. Three observations cannot establish a stable tail-latency estimate. Keep one worker; no parallel throughput comparison was performed. Reuse checksum-verified public tool archives only. Proposed follow-up budgets are 20 samples per mode, investigation when setup exceeds 15 seconds or execution exceeds 5 seconds; these are experimental proposals, not new acceptance criteria.

## 5. Return independent evidence — slides 13–14

The second operator should record their identity/context, source revision, newly supplied access method without secret values, exact command, receipt and observed limits. Do not send passwords, keys or private business data. The plan says second operator; it does not explicitly require a human or a different physical host. A repeated execution controlled by this same implementor with retained service access does not establish that separate context. Independent execution and its assessment remain pending; no Product Owner reaction is inferred. See the [blocker audit](sprint_E.11_blockers.md).

## 6. Reproduce as the technical second operator — revised slides 11–14

### What the provisioning script does

The Product Owner explicitly requested technical execution of the second-operator requirement. The [provisioner](../../scripts/reproduce_second_operator.py) creates a disposable rootless outer container from the recorded immutable Podman image digest. Its privileged flag supplies nesting permissions within the existing rootless VM user namespace; it mounts no host path or runtime socket. This is trusted laboratory provisioning, not privilege granted to a candidate. Python, Git, curl and the nested engine are supplied by that pinned image; host prerequisites additionally include OpenSSL and access to the existing apex-cicd provisioning connection.

The script generates a fresh one-day CA and separate server/client keys in an OS temporary directory. Only the new server/client material enters the operator container; the CA signing key stays in the temporary provisioning directory. The server's private directory is root-only. The operator is uid 1000 with a separate HOME, environment cleared with env -i, its own connection configuration and newly issued client certificate. It must be denied without that certificate and must see an initially empty engine/image store. This is actual mutual TLS authentication, not an invented role name.

The provisioner exports only the two selected Python source files, records their SHA-256 and the original repository base revision, creates a self-contained Git source snapshot/bundle and has the operator clone it cleanly. This deliberately omits the original checkout's private configuration, original Git object database, business data and retained credentials. The source snapshot includes the small current connection/logging adapters; its content hashes identify the tested bytes even before their completion commit. It is a clean checkout of the selected slice, not a complete application checkout or APEX installation.

The operator runs the same six-sample workload with --connection second-operator. The new driver option defaults to apex-cicd for existing users. The source controller explicitly selects k8s-file logging so output can be inspected without a journald service. The nested engine uses vfs storage and cgroups disabled because its environment cannot expose the memory.max control file. Candidate shell, network denial, read-only root, capability removal, private tmpfs, integrity and cleanup assertions remain identical. CPU/memory/PID limit enforcement is explicitly unsupported in this nested path and is not a PBI-078 acceptance claim. Neither a different human nor a different kernel is claimed.

The source of this supported approach is [Red Hat's Podman nesting guidance](https://www.redhat.com/en/blog/podman-inside-container); [Podman's service reference](https://docs.podman.io/en/stable/markdown/podman-system-service.1.html) defines client-certificate authentication. The experiment itself, rather than those references, establishes the recorded result.

### Execute and inspect

The command creates a uniquely named container, provisions the technical account, performs all six runs, retrieves only nonsecret receipts and removes the entire container/private tmpfs in finally. It never prunes the service or touches the retained database. A nonzero result is failure; exact sanitized diagnostics are retained in the second-operator evidence directory. This operator experiment was executed live and through the A3 gate.

```bash
python3 -u scripts/reproduce_second_operator.py
code progress/E.11/tests/second-operator/receipt.json
code progress/E.11/tests/second-operator/benchmark.json
```

Expected: distinct uid/new mTLS access/unauthenticated rejection/empty-engine/clean-source PASS, six sample PASS lines and a final scoped-cleanup PASS. receipt.json identifies the account, certificate fingerprint, exact selected-source hashes, source snapshot, pinned image, command, empty before/after stores and cleanup verification. The benchmark contains real measurements on this new operator runtime. Do not interpret its timings as an isolated performance improvement over the prepared-host baseline: the runtime, storage driver and cgroup support differ.

The first SSH-based VM-account approach was denied and was abandoned. Initial nested tests exposed missing stdin attachment during credential transfer, unavailable memory cgroups and remote logging defaults. These were diagnosed and repaired; earlier sanitized failures remain evidence. The supported nested path succeeds without changing host accounts or relying on copied private access. No Product Owner satisfaction or independent human review is inferred.
