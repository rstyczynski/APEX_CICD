# E.15 trusted Oracle validator

Candidate SQL and ordinary pull requests live in
rstyczynski/APEX_CICD_E.15-candidates with GitHub Actions disabled. Only the
trusted operator has target-repository write access in this bounded experiment.
Candidate source is data; it receives no trusted operator credential.

This repository supplies the trusted Oracle workflow, exact-byte Review report
and Python/GitHub CLI controller. The controller checks current candidate
head/base, trusted policy commit, report identity, correlated real run and
actual job provenance before publishing TrustedOracle or requesting ordinary
protected merge. Pending, cancelled, failed or stale evidence cannot pass.

The original same-repository design allowed workflow check spoofing and
cross-run cancellation. The companion boundary replaced that design. Actual
stale base/head/report and peer-evidence refusals, live Oracle cleanup with an
unaffected peer, recovery and ordinary protected merge are recorded in the
APEX_CICD progress repository. A harmless disabled companion dispatch remains
zero-job metadata; it allocated no runtime and is not an Oracle resource leak.

Use `python3 controller.py --help` for the validate/publish/merge interface.
The optional --pause creates a bounded inspection interval for the live cleanup
exercise. The published walkthrough in APEX_CICD owns complete staged inputs,
operating steps, verification limits and sprint lifecycle status. This is an
Elaboration experiment, not production multi-user IAM or native release delivery.
