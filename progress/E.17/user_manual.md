# E.17 clean-host reproduction — working draft

This guide operates the sprint experiment, not a production deployment. [PBI-085](../../BACKLOG.md#pbi-085-reproduce-complete-native-delivery-on-a-clean-host) and [PLAN E.17](../../PLAN.md#sprint-e17---reproduce-complete-native-delivery-on-a-clean-host) own requirements. The [checklist](sprint_E.17_checklist.md) records observed acceptance; the [design](sprint_E.17_design.md) owns implementation choices. The end-to-end presentation walkthrough will be the handover entry point when verified. Platform qualification is still in progress; do not interpret draft commands as accepted reproduction evidence.

## Prerequisites and inputs

Use GitHub CLI with access to rstyczynski/APEX_CICD_E.17 and its candidate companion. A GitHub-hosted Ubuntu 24.04 job provisions a new host and two digest-pinned Oracle Database containers. The job removes unused preinstalled SDK payloads to provide disk capacity, then installs the qualified SQLcl build, checksum-pinned APEX and digest-pinned ORDS. No local Oracle service, saved connection, laboratory credential or retained database is a prerequisite. Passwords are newly generated and masked within each job. Job-private connection state belongs in RUNNER_TEMP and is removed by an always-run cleanup step. The native project records SQLcl 25.4.1.0 and execution requires qualified build 25.4.1.022.0618; no project-version bypass is used.

Discover the checkout root with `git rev-parse --show-toplevel`. To inspect delivered source locally, the `code` command must be available on PATH. Inspect `sprint-work/E.17/.github/workflows/native.yml`, `provision_host.py`, `sql.sh`, validators and `application.sql`. The workflow is the sequence; the Python platform adapter accepts one explicitly selected phase per invocation and does not run the release pipeline. SQLcl PROJECT owns native source export, staging, verification, release, archive construction and deployment. Git retains generated history. The source implementation record links trial identities and failures; final run identity remains pending.

## Read the native workflow before reproduction

The first named steps prepare disk capacity and start isolated author/target databases. Platform steps generate fresh private inputs, acquire/verify APEX, run native installation, configure the workspace, install ORDS and start its listener. The dependent application is imported only after native table installation and seeding. The script does not advance automatically between phases. The SQLcl invocation adapter measures the actual tool before each invocation, checks available native project metadata, enables SQL/OS failure exits, records native output and rejects reported SQL/native errors even if the process exits zero.

Release steps create the preserved table on the author, initialize a new native project and use native export/stage/verify/release/gen-artifact for 1.0.0. A receipt binds workflow source/run, reviewed source manifest, generated native Git history, actual tool build and archive digest. Installation invokes project deploy only after provenance checks. The target receives one committed row. The author then adds a nullable column, prepares 1.1.0 through the same native sequence, upgrades the target and repeats the identical archive. Native SQL asserts that the committed row survives both operations. Explicit negative steps challenge artifact evidence, source identity, actual older SQLcl build and changed archive bytes, then compare target observations.

## Inspect outcomes and recover

A completed workflow alone is insufficient. Inspect individual named steps, archive receipts, native SQL logs, application HTTP observation and cleanup receipt. The first trial exhausted hosted disk and could not retain normal runner logs; its check annotation remains available. The second trial exposed a genuine APEX prerequisite failure that a zero process exit concealed. Its redacted install log is retained. The full-image retry and explicit output checks address those observed causes; final qualification is pending.

The initial HTTP check targets the imported login page. The final declared Chromium check signs in with a new LAB_USER and requires the native retained row on the small fixture page. That final authenticated observation remains pending; no greeting-component workflow or production application readiness is claimed. The native delivery fixture is the table/row experiment inherited from E.16; it does not establish a production release of every earlier product component. Report these boundaries alongside any successful observation.

## Candidate validation and merge

Candidate code is SQL data supplied to a trusted workflow, not host code run with operator credentials. Candidate repository Actions are disabled. The trusted workflow checks changed-file scope and candidate digest against its base-branch review, executes the bounded Oracle query under the application user, verifies private-table denial and proves its token cannot publish a status. After inspecting actual successful terminal results and exact current candidate identity, the authorized operator publishes TrustedOracle through GitHub's native API. Ordinary protected merge then succeeds without an admin bypass. A changed candidate with stale review fails before SQL execution and remains unmergeable.

Real E.17 evidence: candidate PR 1 and run 45819877026 establish the accepted reviewed journey; PR 2 and run 45820491077 establish stale-review refusal. PR 2 was closed after the negative case. These do not establish unperformed platform acceptance.

## Cleanup and limits

Each hosted job removes only its RUNNER_TEMP private connection/configuration paths and named E.17 containers. GitHub disposes of the ephemeral host. Keep the sprint repositories and retained evidence for audit; repository deletion is not part of this reproduction. Never apply hosted SDK cleanup commands to the prepared laboratory host. The prepared-host retained credential accommodation is unrelated and is not read or expanded by E.17 provisioning. Capacity/latency benchmarking remains E.18 scope.
