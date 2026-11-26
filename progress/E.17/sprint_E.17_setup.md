# E.17 setup

## Contract

Product Owner explicitly authorizes activation, YOLO execution, companion repositories, local commits and final origin publication. PBI-085 alone is assigned. Test and full Regression select smoke, unit and integration. RUP manager and local P8/P9 govern; no elapsed-time stop applies. No production metadata upgrade or retained credential copying is authorized. Token accounting is unavailable.

## Analysis

Actors are the source developer, fresh-host provisioning authority and independently identified technical deployment operator. The operator receives clean public source and freshly generated private inputs, provisions Database/APEX/ORDS, accesses the application and executes native installation, upgrade and repeat while retaining seeded data. E.15/E.16 repositories supply reusable code, never acceptance evidence for E.17. A second human is not specified; a distinct technical operator must have recorded identity, host and access provenance. E.11's nested-engine experiment explicitly did not qualify another host.

No E.17 repository or evidence directory existed at inspection. Dedicated private repository rstyczynski/APEX_CICD_E.17 was created. Hosted ephemeral Ubuntu is the selected independent host; no prepared lab settings or credentials are transferred. Generated connection state belongs in RUNNER_TEMP and is cleaned on every outcome. [Design](sprint_E.17_design.md) owns choices; [checklist](sprint_E.17_checklist.md) owns acceptance tracking.

## Actor-attribution correction

Review of the authoritative SRS Actors/Stakeholders boundary supersedes the initial statement that a distinct internal technical account alone suffices as another operator. A runner is an internal pipeline component; PBI-085 requires another attributable A-03 participant. This does not introduce a human-only requirement or require a different GitHub account. The actual clean-host automation is verified, but external-operator attribution or an explicit Product Owner acceptance decision is pending. Independent tests and delivery work continue; no acceptance is inferred from silence.

## Product Owner amendment — 2026-11-26

The [explicit acceptance decision](sprint_E.17_acceptance_amendment.md) supersedes the pending decision above for E.17: Codex-driven automated clean-host reproduction is accepted without another external operator. BACKLOG PBI-085 and PLAN E.17 now reflect that decision. Continue the existing YOLO sprint; all other technical and quality gates remain required. Historical analysis above records earlier interpretations, not the current acceptance condition.
