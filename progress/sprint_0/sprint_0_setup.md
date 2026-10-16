# Sprint 0 — Vision and initial plan

Date: 2026-10-16

Sprint 0 | Mode: managed | Test: none | Regression: none

## Contract

The Product Owner explicitly requested Sprint 0 and supplied the intent: research Oracle APEX CI/CD automation using regular DevOps practices, model it on a local APEX service preferably using Podman, and ultimately build a simple modular Hello World application with greeting history and separate Hello and World data/configuration pages. Alternative application shapes may be proposed.

The assigned outcomes are PBI-001, an accepted product vision in the root README, and PBI-002, a project-specific roadmap and next-sprint proposal derived from that vision. This iteration produces documents and decisions. Application construction, environment changes, comprehensive technology comparison, and technical experiments belong to subsequent accepted work.

The root AGENTS instructions, Codex manager and role adapters, canonical manager, contractor and analyst procedures, generic cooperation, Git, backlog, sprint, bug and test rules were reviewed. The full local patch and Product Owner preferences govern refinements. Narrative documents use paragraphs and headings; the progress board retains its required four-column table. Codex performs the roles serially. No CI provider has been selected, so provider-specific implementation rules are not yet applicable.

The local patch P0.2 and P1 tailor the generic code pipeline to Sprint 0. First draft the vision and obtain Product Owner acceptance; then derive the roadmap and propose the next sprint for a separate decision. P8 supersedes phase-by-phase commits: commit completed increments with a documentation audit, rather than committing phase transitions. No increment is complete at this initial review. The local remote-action rule supersedes generic automatic pushes; this sprint request does not authorize a push.

The bootstrap plan names Sprint 0 explicitly, so this iteration retains that identifier and the canonical `progress/sprint_0/` evidence path. Future phase-based sprint labels will be addressed in the plan proposal under P0.phase, without silently renumbering the existing plan.

Preserve the supplied wrapper, submodule pin, existing deployment material, local credentials and runtime data. Do not overwrite or stage unrelated pre-existing files. Exact phase token usage is not available from the execution interface and is not estimated.

## Analysis

### PBI-001 — Establish the product vision

The README translates the supplied intent into the intended users, problem, outcome, reference application, constraints, and evidence expected from the eventual demonstration. It proposes one application with distinct Hello, World, and history areas while leaving deployment boundaries open. “Component” is not assumed to mean independently deployed applications or schemas. The Product Owner accepted this vision on 2026-10-16 and subsequently confirmed satisfaction with the README.

Sprint 0 can establish this vision without proving runtime feasibility. Podman suitability, version compatibility, runner connectivity, target separation, export reproducibility, database evolution, and recovery remain research and architecture questions. They must not be reported as solved by drafting the vision.

### PBI-002 — Derive the initial project plan

The PBI-001 dependency is now accepted. ROADMAP.md and sprint_0_proposedchanges.md propose proportionate work for the research comparison, requirements and candidate architecture, a risk-focused executable experiment, and the eventual delivery demonstration. The proposal retains the connected Inception outcomes together, incorporates research as supporting evidence, and avoids scheduling the preliminary installation again. The proposed I.1/E.1 label mapping and next-sprint context await acceptance; existing planned assignments remain unchanged.

### Existing assets and compatibility

The repository is on `main`, tracking `origin/main`, with bootstrap commit `120c3ce`. The pinned method is `a875404e4452f77d3c16e08e3e1ab8c0afe5be38`. No earlier sprint evidence existed when this iteration started.

The pre-existing runbook, now at `docs/deploy.md` by Product Owner direction, describes an Apple Silicon Podman setup with Oracle Database Free, APEX, and ORDS. Eleven files in `scripts/` provide setup, lifecycle, and verification helpers. The Product Owner explicitly recognizes this as completed preliminary work available for potential reuse. The runbook's existing verification record reports database and HTTP access, administrator login, and VM stop/restart checks; these are historical inputs, not fresh Sprint 0 evidence. The runbook gained a preliminary-work notice and a corrected path in its optional source-cleanup example; no cleanup was executed.

The supplied PDF was moved to `refs/apex-lifecycle-management-v3.pdf` as an external reference. SHA-256 before and after the move is `6f41b2f4511bfc3e3e4bbe28f3240c897a56006a42e46177d62a06d493cc4425`; its contents have not yet been reviewed in this sprint. The scripts and `.gitignore` remain unchanged. `.local-apex/` remains ignored; credentials and local logs were not read.

### Initial source check

Oracle's [SQLcl 24.3 release notes](https://www.oracle.com/tools/sqlcl/sqlcl-relnotes-24.3.html) describe the PROJECT workflow for versioning database and APEX work and creating ordered release artifacts. Oracle's [APEX export/import documentation](https://docs.oracle.com/en/database/oracle/apex/26.1/apxdc/exporting-and-importing-applications.html) describes SQLcl automation and split application exports. These establish credible research directions, not a selected toolchain. The latter describes a newer APEX version than the local runbook's 24.2; compatibility with the actual local installation must be checked before adopting commands. No tools were installed or candidate workflows executed.

### Review strategy and dependencies

For PBI-001, the developer checked the README against the supplied intent: local APEX, Podman preference, persistent history, separate Hello and World data/configuration pages, source-backed research, and a reproducible CI/CD demonstration. The Product Owner explicitly accepted the vision. The board marks PBI-001 tested on this document-review evidence; no application test or fresh environment validation is implied.

For PBI-002, review traceability from the accepted vision to proposed work and next-sprint outcomes, dependencies, unresolved risks, quality expectations, and a proportionate lifecycle. The developer has prepared the proposal; the Product Owner decision is pending.

No production code changes, automated test skeletons, or runtime gates apply to this document-only increment. The test-profile template remains pending. Later candidate architecture work must define actual commands before a code-bearing iteration. Before any completion commit, record the P8 documentation audit and run applicable link and whitespace checks. Final sprint handover still requires the P9 demonstration of the actual documents and Product Owner decision; this vision review does not close the sprint.

## Current decision point

The vision is accepted. The next decision is acceptance or revision of ROADMAP.md and the I.1/E.1 proposal in sprint_0_proposedchanges.md. No later sprint has started. Sprint 0 remains in progress; its final document demonstration and handover decision have not occurred.
