# Sprint I.1 — Setup

## Contract

Activated from Planned to Progress on 2026-10-16 by explicit Product Owner instruction. Mode: managed. Test: none. Regression: none. E.1 remains Planned. Assigned scope is PBI-003 through PBI-010: research and an Inception baseline, with no application implementation or Elaboration execution.

Read AGENTS, root/local patch, preferences, accepted README, ROADMAP, BACKLOG, PLAN, board and Sprint 0 handover. Read the manager and contract/analysis, design/test and quality/wrap-up adapters, applicable canonical setup/design/test procedures, and all generic rules. P0.phase selects `progress/I.1/`; P1 substitutes document review for code construction/tests; P8 governs completion commits; P9 governs eventual handover. Narrative documents use headings/paragraphs. No extra agents are needed. Actual token accounting is unavailable.

Maintain assigned artifacts and evidence, propose material decisions, audit completed increments before committing, and never push without explicit request. Preserve data, credentials, unrelated resources and pre-existing untracked `.DS_Store`, `.gitignore` and scripts. The subsequent user instruction assigns ownership of `docs/deploy.md` to I.1 as a maintained sprint product. Earlier platform installation is not retrospectively claimed as I.1 work.

## Analysis

PBI-003 establishes the lab boundary/stakeholders and explicit actor model; PBI-004 defines twelve actor-goal use cases, including onboarding, initial Git adoption and the complete developer cycle; PBI-005 materializes these and testable behavior in the [SRS](../../docs/srs.md). These depend on the accepted vision, not a new app.

PBI-006 proposes prioritized product outcomes through the [change proposal](sprint_I.1_proposedchanges.md); PBI-007 defines minimal release scope/exclusions in the SRS. Approval is needed before changing priorities or adding root items. PBI-008 records eleven risks and validation responsibilities.

PBI-009 supplies the [architecture](../../docs/architecture.md), [research/reuse assessment](../../docs/cicd-research.md), maintained [runbook](../../docs/deploy.md) and [test profile](../../docs/test-profile.md). PBI-010 will review these together with backlog and plan after the design decision. Scope is feasible as documents; technical viability remains conditional on executable evidence in E.1.

Research used the PDF (version 3.2, APEX 24.2/SQLcl 25.1.1 examples) and version-specific primary references. Read-only assessment confirms current APEX/database versions, but SQLcl is absent from PATH and host Java 25 is outside SQLcl 25.3's documented Java 17/21 profile. Existing scripts are plausible platform assets; eight shell files pass syntax checks. No credentials were printed and no lifecycle operations were executed.

Analysis is sufficient to propose the design. Greeting configuration semantics, toolchain and runner selection remain review decisions. The current gate is the [design proposal](sprint_I.1_design.md). Nothing is marked tested or complete.
