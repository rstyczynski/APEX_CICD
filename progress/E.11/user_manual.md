# E.11 operating reference

The [complete walkthrough](sprint_E.11_increment_demo.md) owns commands, prerequisites, input acquisition, expected results and recovery. Start there; [handover](sprint_E.11_handover.md) states actual acceptance. This manual supports only the selected E.10 isolated candidate boundary on ARM64 Podman, not full APEX delivery or host installation.

The driver needs Git, Python 3, curl, tar and private access to a running Podman service under the declared apex-cicd connection. Fresh synthetic inputs are generated per candidate; no credential file is requested. Tool archives are pinned and checksum-validated before reuse. The output receipt contains source/tool identities, sample counts, durations and limitations.

An acquisition error, invalid checksum, unexpected BusyBox release, failed assertion or cleanup failure stops execution. Restore service/network access or obtain correct bytes, investigate retained errors and retry deliberately with a new receipt path. TemporaryDirectory removes local caches/clone on ordinary failure. A killed process can leave a container/image: identify only the exact e10 candidate created by this run and the imported e11.session image before scoped manual cleanup; never prune the service. Forced termination recovery for this new benchmark driver has not been qualified. The prior E.10 reaper experiments do not establish it for this driver.

Do not run multiple copies concurrently as a measured throughput claim. Unique import labels prevent shared image deletion, but concurrency latency was not measured. Preserve earlier receipts and never infer independent operation or clean-host success from a same-operator rerun.
