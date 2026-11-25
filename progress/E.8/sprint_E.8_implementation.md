# E.8 implementation

[Design](sprint_E.8_design.md) owns the accepted experiment; [manual](user_manual.md) owns usage; [tests](sprint_E.8_tests.md) owns measured outcomes.

The trusted controller in scripts/candidate_testing.py fixes the five-suite inventory and policy digest. The laboratory driver in tests/candidate_lab.py constructs an actual Git merge after base advancement, extracts migration and package SQL from that merge, and executes it in generated no-authentication schemas. Every cadence executes independently. Missing downstream reports remain failures, while first_failure preserves the earliest failed suite. Cleanup runs in finally and propagates failures.

YOLO decisions: conservative full inventory for the single greeting impact unit; no optional critical suites; local PR candidate simulation with explicit base/head/merge/tree records. Candidate SQL is not a hardened security boundary and transport uses prepared-host administrator access only in this bounded experiment. Production isolation, native PROJECT deployment and GitHub status publication remain outside this sprint.

## User documentation

Prerequisites: prepared Podman apex-cicd connection, running apex-db/FREEPDB1, qualified SQLcl 25.4.1.022.0618 and retained JDK 21 path. From repository root run `python3 tests/candidate_lab.py`. Expected output: PASS three real integrated candidate cadences and five fail-closed fault paths. Logs and result.json records are in progress/E.8/tests. A transport failure raises an exception and cannot count as successful negative behavior. Inspect cleanup.log before retrying; the driver never drops prior sprint schemas.
