# E.1 — Setup

## Contract

Sprint E.1: Validate the local APEX delivery path. Mode: managed. Test and Regression: smoke, unit, integration; full suite. The Product Owner authorized activation after I.1 closure; the accepted baseline is available at commit ebf1a1a. Only E.1 sprint artifacts and necessary shared product/process files are in scope. Other sprint artifacts remain untouched.

Use the accepted README, ROADMAP, BACKLOG, PLAN, SRS, candidate architecture, test profile, final review decisions and handover as inputs. Apply AGENTS, the local patch/preferences, manager and selected phase adapters, canonical role/test procedures and generic rules. Local P8 replaces phase-only commits with audited completed increments. Local P6 requires the prototype decomposition in the design and board; the root backlog/plan retain PBI-011 as the parent. No subagents are needed.

The implementor owns technical design, scripts, tests and recommendations. The Product Owner approves the E.1 design before code or test skeleton construction and decides material changes. Keep records short and focused on decisions, deliverables and test results. Do not push. Preserve retained data, credentials and unrelated Podman resources; use docs/deploy.md for scoped lifecycle operations.

## Analysis

PBI-011 builds one architectural prototype: one application per target, Foundation/Hello/World, private single-host developer areas and supported Oracle interfaces. Its eight bounded children are specified in the [design](sprint_E.1_design.md). Bootstrap and atomic reservations precede application expansion; capture/identity stability precedes parallel integration; qualification precedes retained TEST promotion; maintenance and inspected partial-state recovery precede the final demonstration.

PBI-012 gathers observed success/failure evidence and resource/effort measurements across these children. It separates actual API behavior from candidate mechanisms and distinguishes real concurrent clients from sequential simulations. PBI-013 updates requirements only where evidence exposes a gap. PBI-014 records which architectural controls are proven and which remain uncertain. PBI-015 assesses Lifecycle Architecture against the core proofs. PBI-016 proposes Construction from that assessment, or further focused Elaboration when essential controls remain unproven. These items do not create extra implementation platforms.

## Feasibility and resources

Read-only observations on 2026-10-16: Podman 6.0.0; the owned apex-cicd VM is running with four CPUs, 6 GiB RAM and a 30 GiB sparse disk; apex-db and apex-ords are running. The separate podman-machine-default is stopped and unrelated. Host memory is 48 GiB with twelve logical CPUs. Host free disk is approximately 13 GiB. No lifecycle operation was executed for setup. SQLcl is absent from PATH; the accepted SQLcl/Java pair must be provisioned privately and tested before Oracle experiments. Existing script sources and .gitignore remain untracked and require review/adoption in child 1.

Use the current scoped VM and allocate logical areas rather than another database runtime. The Product Owner authorized destroying/recreating it as needed and assigned E.1 ownership of docs/deploy.md and its lifecycle procedure. Run the complete lifecycle proof within that scope, preserve host credentials/evidence and retained application data, and document verified steps in the procedure. More disk space will be available; measure actual headroom at execution rather than treating the initial observation as a fixed limit.

The selected happy path, compatible patch and incompatibility/drift demonstrations are approved for construction. Runtime feasibility is tested incrementally. The selected test skeletons exist and the first platform checks pass; application assertions remain pending. Token accounting is unavailable.

The design's construction selection starts the application from scratch. Seed preparation and existing-application adoption remain documented options but are not selected for E.1 implementation. Existing design work is retained.

First implementation selects the design's happy path: sequential Foundation, Hello and World authoring/capture, fresh-install qualification and same-archive promotion, ending with a greeting and saved history in TEST. Parallel, rejection, drift and repair scenarios remain later work within the retained design.
