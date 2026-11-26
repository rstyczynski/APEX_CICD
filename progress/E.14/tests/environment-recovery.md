# Integration fixture interruption and recovery

## Requirement and failure

PLAN E.14 requires full integration regression; the corrected default registry includes the three new E.14 entries. The first full run of that registry failed before its actual test functions, during owned isolated ORDS installation. The exact command and TimeoutExpired traceback are in test_run_B3_integration_20261125_224649.log: the pinned ORDS image's install command through apex-cicd exceeded 300 seconds. Passwords were passed via stdin and are not recorded. That run is failed, never waived or represented as a pass.

## Diagnosis and alternatives

The existing `podman --connection apex-cicd ps --format '{{.Names}} {{.Status}}'` query also stopped responding. A bounded `podman --connection apex-cicd info --format '{{.Host.Uptime}}'` probe timed out after ten seconds; podman-stall-probe.log preserves the command/result. Host process inspection showed the VM process consuming substantial CPU; host disk inspection showed about 100 GiB available. These observations did not identify a cause.

A direct read-only SSH diagnostic of VM load, disk and service status was rejected by the permission tool with `Rejected("rejected by user")`, without a reason. One scoped clarification was requested; SSH was not retried or used. After the timed-out worker exited, the already authorized Podman API responded again, so direct SSH was no longer needed for immediate recovery. podman-post-timeout-probe.log records that transition. The diagnostic container inventory later returned and the removed isolated ORDS name was correctly absent.

`podman inspect apex-ords --format '{{.State.Status}} OOM={{.State.OOMKilled}} exit={{.State.ExitCode}} error={{.State.Error}}'` reported stopped, OOM=false, exit=137. SQLPlus `select status from v$instance` in the retained database reported ORA-01034; database-post-timeout.log preserves it. Oracle's adrci was unavailable on PATH, and dmesg was absent in the container. Podman OOM event inspection returned no events. No cause is inferred from those missing convenience tools. A code-137 exit alone does not prove memory exhaustion.

## Supported recovery performed

Using the existing Podman exec/SYS SQLPlus boundary, `startup; select status from v$instance;` successfully reopened apex-db, then e12-regression-db, without deleting or recreating their volumes. retained-database-recovery.log and regression-database-recovery.log preserve OPEN results and actual SGA sizes (about 1.6 GB and 0.8 GB). The stored regression memory settings were already bounded by its original fixture helper; no resource configuration was silently changed.

`podman start apex-ords` restored the retained service. `curl --max-time 10 -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8080/ords/` returned 302. Both FREEPDB1 databases were READ WRITE; other historical PDB states were inspected but not changed. run_18259/post-recovery-inspection.log independently requires all 163 history/detail rows and the original English setting after restart. It passes.

## Retry and limits

The failed B3 integration gate was retried with unchanged executable sources and the corrected registry. The five passing gates were retained rather than rerun without a reason. resource-monitor.log samples API responsiveness, free memory and aggregate CPU; Linux free memory excludes reclaimable cache and must not be treated as available memory. One /proc/meminfo inspection showed about 1.37 GB MemAvailable despite low MemFree. No fixed-capacity or production reliability claim follows from this single-host recovery. Final test records must state the retry result explicitly. No external blocker is established by the recovered API interruption.

## Verified retry result

The unchanged-source B3 retry passed all 23 registered integration entries, and its source snapshots match current files. Post-recovery full smoke passed 13/13 and unit 14/14. The monitored oom_kill counter stayed at 33 through the observed retry. No flaky test was deferred, no failure was waived, and no SSH command was executed. The lab interruption’s cause remains undiagnosed. Recovery, data-preservation checks and regression passed. This incident does not establish an additional E.14 acceptance gate.
