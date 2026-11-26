# E.16 observed failures and repairs

## Native target schema

Run 45800222128 attempted PROJECT deploy as TARGET16. The archive contained `create table author16.preserved`; native execution failed ORA-01031. The retained [installation log](tests/run-45800222128/native-45800222128/install.log) is the authority. SQLcl 25.4 lacks the newer schema-substitution feature described in Oracle's later release notes. The repair uses separate source and target Oracle services with identical schema names. No archive rewriting, broader target privileges or version bypass is accepted.

The same run's native verify output reported Errors: 1 for a missing dist/releases/apex path. Process exit alone missed this. The repair initializes the expected empty path and rejects nonzero native Errors counts; it still requires a clean real verification result.

## Saved connection reuse

Run 45800911668 failed before native initialization because the controller attempted to save native-author a second time. It now saves each job-private connection once and uses `connect -name` thereafter. This is an implementation defect, not an external blocker. Run 45801589178 exercises the correction.

## Superseded execution

Run 45800871631 was cancelled after the verification-error correction superseded it. Cancellation is not a passing lifecycle result. No successful installation, upgrade or repeat is claimed from these runs.

## Full-regression recovery

The resumed B3 attempt began before the stronger native artifact reader was finalized. It was superseded to preserve the historical harness's mandatory stable-source check, rather than suppressing that check. A replacement initially refused the fixture lock while the prior worker still held it. The old worker and its orphaned disposable ORDS uninstall client were terminated by their exact process IDs. No passing result is attributed to either attempt.

The VM's Podman API and SSH then stopped answering; even the ordinary `podman machine stop apex-cicd` hung. TCP/SSH, machine inventory and out-of-sandbox API checks were tried. Recovery stopped the identified apex-cicd krunkit backend with TERM and restarted the existing machine, preserving all disk volumes. The interrupted replacement log records connection refusal during restart. This is a recoverable execution problem, not grounds to weaken B3 or delete/recreate retained laboratory disks. A clean final stable-source B3 retry is required.

The direct restart selected the installed default helper and failed with exit 2. An explicit temporary helper configuration and launchd start recovered the existing VM successfully. The normal retained database/ORDS services were started using scripts/apex-start.sh; the owned e12-regression-db also required an explicit start because legacy_database.py expects an already healthy existing fixture. No fixture ownership check was removed. Smoke/unit attempts made during the outage failed and require successful retries after service readiness.
