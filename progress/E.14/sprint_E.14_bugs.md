# E.14 defect record

## BUG-1 — SQLPlus statement separation — corrected

The first direct Oracle run failed with ORA-03405 because an UPDATE and COMMIT shared a SQLPlus input line. [Exact failed SQL/output](tests/run_16473/Hello-start.log) is preserved. The driver now separates statements before sending them through the existing fail-on-error boundary. Rehearsal run_16505 and live run_18259 pass. This was an implementation defect, not an environmental blocker or expected acceptance result.

## BUG-2 — default regression registration — corrected

The Foundation component manifest included E.14, but the default runner uses component_delivery.manifest. Initial full regression therefore exercises the previous registered suite while new-code gates independently exercise E.14. After that source-stable run ended, the three E.14 registrations were appended to the default manifest and all final gates rerun successfully. No old result is relabelled as a run of the corrected registry.

## Presentation environment — recovered

The first package finalization could not import because RUNTIME_NODE_MODULES was unset. Supplying the installed runtime package directory repaired first-party import; the final package/layout/import receipt passes. No substitute package or new dependency was installed.

## BUG-3 — final integration environment interruption — recovered

The corrected-registry B3 attempt timed out during pinned ORDS installation after 300 seconds. The API later responded, but the retained Oracle instance was down and ORDS had exited with code 137. Both databases were reopened through supported SQL startup and the retained ORDS service restarted; existing demonstration data/configuration passed independent checks. [Recovery evidence](tests/environment-recovery.md) records exact observations, rejected SSH diagnostics and the supported Podman alternative. The root cause remains unconfirmed. The unchanged-source retry passed 23/23 entries under resource monitoring; no failed gate was waived. Post-recovery smoke/unit also pass. The monitored kill counter remained unchanged, and the earlier cause remains unconfirmed.

[Implementation](sprint_E.14_implementation.md) explains the resulting behavior; [test record](sprint_E.14_tests.md) owns accepted outcomes.
