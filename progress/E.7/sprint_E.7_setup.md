# E.7 — Contract and analysis

## Contract

The Product Owner explicitly authorizes activation and autonomous implementation through local commits and closure. [PLAN](../../PLAN.md) owns assignments and smoke/unit/integration plus full smoke/unit regression. [The board](../../PROGRESS_BOARD.md) tracks execution. The RUP manager roles run serially, with local P8 increment commits replacing phase commits and no remote push. Existing runtime and historical artifacts are preserved. Credentials use ephemeral memory only. Token accounting is unavailable.

## Analysis

The release engineer installs a known previous laboratory release, retains synthetic greeting data, upgrades and repeats deployment. The operator checks actual columns, constraints, grants, invalid objects and reference data rather than trusting migration history. The APEX user reads installed release metadata, reconciled to source, contracts, migration hashes and test evidence. These bounded journeys implement [PBI-065, PBI-077 and PBI-057](../../BACKLOG.md). SRS requirements remain authoritative in [the SRS](../../docs/srs.md); [architecture](../../docs/architecture.md) owns production direction.

## YOLO decisions

Use a new isolated E7_APP schema/workspace and app 810703 on the prepared database, avoiding E.5/E.6 mutations. Use small explicit immutable SQL migration bundles for this state/identity experiment; this does not qualify a replacement for SQLcl PROJECT production packaging. Qualify the approved SQLcl release/build before any deployment. Keep component contract identity independent of application release. No later sprint is activated.

## Finalization baseline

The completed run uses the design's finalization correction: fresh E7R/E7C targets, clean committed release inputs and verification before any target creation. The earlier E7_APP experiment remains historical. [Handover](sprint_E.7_handover.md) records exact source/target and delegated acceptance; no scope or acceptance criterion was removed.
