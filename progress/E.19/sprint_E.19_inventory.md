# E.19 initial inventory

## Examined sources

The tracked `sprint-work/` Python inventory contains E.15 controller/validator, E.16 three checks, E.17 their copies plus provisioner/validator, and E.18 those five plus resource sampling. Current latest native workflow was read from the retained E.18 checkout `.github/workflows/native.yml`; hosted candidate workflow `.github/workflows/oracle.yml` was also inspected. Repository-wide and remote-source completeness remain to be verified.

## Initial migration scope

E.16/E.17/E.18 `check_tool.py`, `check_output.py`, `provenance.py` are repeated pure support checks. The E.19 shared implementation replaces their current logic without editing historical files. The provenance asserts are replaced by explicit exceptions. Tool metadata becomes mandatory, consistent with NFR-5. Original copies remain historical acceptance/benchmark inputs.

E.18 `provision_host.py` provides disposable host setup and application provisioning. E.18 `sample_resources.py` measures resources. E.15 `controller.py` owns the historical custom controller. These are initially classified outside pure supporting-check migration, with historical use preserved. This disposition does not authorize adding a new lifecycle controller or claiming a Python-free complete native workflow. The embedded supporting checks and current-use status still require complete review before accepting the inventory.

E.15/E.17/E.18 `validate.py` executes actual Oracle application checks; it must be examined separately from pure file checks. Inline Python in oracle.yml verifies candidate metadata, exact trusted Review bytes and freshness. Those inline supporting checks require migration or a justified disposition; they are not silently excluded. No OCI interaction has been found in the initial three checks. Full source inventory remains open.
