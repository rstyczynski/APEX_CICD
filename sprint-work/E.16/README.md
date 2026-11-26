# E.16 native provenance experiment

This disposable hosted experiment uses the E.15 pinned Oracle image and a checksum-pinned SQLcl 25.4.1.022.0618 download. It prepares native PROJECT releases, installs, upgrades and repeats into an isolated target. The APEX_CICD progress repository owns acceptance and lifecycle records under progress/E.16; repository existence or a dispatched run is not completion evidence.

The workflow initializes two disposable schemas. lifecycle.py records tool identity, generates native metadata, exports and stages source, verifies changes, releases and packages native archives. Before deployment, provenance.py compares source, build and archive digest. Oracle assertions check the seeded row after upgrade/repeat. Negative preflight checks do not call deployment. Workflow artifacts retain logs, receipts, archives and a Git bundle. Runner disposal removes the Oracle service and job-private material. No retained laboratory credential is used.

Run with `gh workflow run native.yml --repo rstyczynski/APEX_CICD_E.16` and inspect the actual terminal result. This is a bounded Elaboration experiment, not production multi-user authority or full APEX qualification.
