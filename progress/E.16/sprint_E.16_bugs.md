# E.16 observed failures and repairs

## Native target schema

Run 45800222128 attempted PROJECT deploy as TARGET16. The archive contained `create table author16.preserved`; native execution failed ORA-01031. The retained [installation log](tests/run-45800222128/native-45800222128/install.log) is the authority. SQLcl 25.4 lacks the newer schema-substitution feature described in Oracle's later release notes. The repair uses separate source and target Oracle services with identical schema names. No archive rewriting, broader target privileges or version bypass is accepted.

The same run's native verify output reported Errors: 1 for a missing dist/releases/apex path. Process exit alone missed this. The repair initializes the expected empty path and rejects nonzero native Errors counts; it still requires a clean real verification result.

## Saved connection reuse

Run 45800911668 failed before native initialization because the controller attempted to save native-author a second time. It now saves each job-private connection once and uses `connect -name` thereafter. This is an implementation defect, not an external blocker. Run 45801589178 exercises the correction.

## Superseded execution

Run 45800871631 was cancelled after the verification-error correction superseded it. Cancellation is not a passing lifecycle result. No successful installation, upgrade or repeat is claimed from these runs.
