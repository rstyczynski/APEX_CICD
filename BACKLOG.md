# Product Backlog

### PBI-001. Establish the product vision

Produce `README.md` as the accepted product vision, using the Product Owner’s stated intent. It must clearly state the intended user value, problem, outcome, and important constraints.

Test: Review confirms that the product vision is understandable, internally consistent, and accepted by the Product Owner.

### PBI-002. Derive the initial project plan from the vision

Create the project-specific roadmap and propose the next sprint from the accepted vision. The resulting work must be prioritized, outcome-oriented, and open to iterative refinement.

Test: Review confirms that the roadmap and proposed next sprint are traceable to the accepted vision and ready for Product Owner acceptance.

### PBI-003. Define system view and stakeholders

Define the system boundary, context, and stakeholders that shape the accepted vision.

Test: Review confirms that the system view and stakeholders are understandable and traceable to the vision.

### PBI-004. Define actors, use cases, and success criteria

Identify the actors and define representative end-to-end use cases and success criteria for the accepted vision.

Test: Review confirms that each use case has a clear actor, outcome, and success criterion.

### PBI-005. Materialize the Software Requirements Specification

Create `docs/srs.md` as the Software Requirements Specification for the agreed system boundary, stakeholders, use cases, success criteria, functional and non-functional requirements, release scope, constraints, assumptions, and risks.

Test: Review confirms that the SRS is understandable, testable, and traceable to use cases and the accepted vision.

### PBI-006. Establish and prioritize the Product Backlog

Establish and prioritize Product Owner-level product increments from the agreed requirements.

Test: Review confirms that the backlog is outcome-oriented, ordered, and traceable to requirements.

### PBI-007. Define the initial release scope

Select the smallest valuable initial release from the prioritized backlog, with acceptance criteria and explicit exclusions.

Test: Review confirms that the initial release scope has measurable acceptance criteria and explicit exclusions.

### PBI-008. Identify constraints, assumptions, and major risks

Identify material product, legal, technical, delivery, and usability constraints, assumptions, and risks affecting the initial release.

Test: Review confirms that significant risks have a planned mitigation or validation approach and assumptions are explicit.

### PBI-009. Materialize the candidate architecture

Create `docs/architecture.md` as a candidate architecture that supports the selected initial release and identifies assumptions requiring validation. Identify the architectural guidance needed to refine the later prototype work without inventing that work prematurely. Complete the project test profile with the selected toolchain's exact build and test commands before the Elaboration iteration starts.

Test: Review confirms that the candidate architecture addresses essential requirements and significant risks, and that the project test profile contains the exact commands required for the Elaboration iteration.

### PBI-010. Review the Inception baseline for consistency and viability

Review the vision and intended outcomes, `docs/srs.md`, `docs/architecture.md`, Product Backlog, and test profile as one coherent Inception baseline. Record the checkpoint requiring the next Elaboration iteration to refine the prototype PBI into independently reviewable work items from the accepted architecture.

Test: Review confirms that the baseline is internally consistent, viable, ready for Elaboration, and has the required prototype-refinement checkpoint.

### PBI-011. Build an executable architectural prototype

Build a focused executable prototype that exercises the initial release's architecturally significant paths without claiming to be production implementation.

Test: Review confirms that the prototype can be executed and covers the intended architectural paths.

### PBI-012. Validate critical technical assumptions and use cases

Use the prototype to gather evidence for the highest-risk technical assumptions and use cases.

Test: Review confirms that each significant assumption and use case has validation evidence or explicitly defined remaining work.

### PBI-013. Refine use cases and supplementary requirements

Refine the use cases and supplementary requirements when prototype evidence exposes gaps, constraints, or changed assumptions.

Test: Review confirms that refinements are traceable to prototype evidence and remain consistent with the accepted vision.

### PBI-014. Stabilize the architecture baseline

Formulate and stabilize the architecture baseline from prototype evidence.

Test: Review confirms that the baseline addresses the initial release and its significant risks.

### PBI-015. Assess the Lifecycle Architecture milestone

Decide whether the stabilized architecture is ready to support Construction. If it is not, identify the remaining Elaboration objective rather than asserting the milestone prematurely.

Test: Review confirms that the milestone decision has explicit supporting evidence and remaining objectives where needed.

### PBI-016. Create the Construction plan

Create the Construction plan from the validation evidence, including the updated backlog, delivery order, resource assumptions, and remaining risks.

Test: Review confirms that the Construction plan follows accepted decisions, unresolved risks, resource assumptions, and the milestone assessment.

### PBI-017. Deliver a repository and pipeline reference guide

Provide a consolidated guide explaining how shared application sources, developer work, release artifacts and deployment environments fit together. Keep it consistent with requirements, architecture, operator guidance and validation evidence, with navigable links between related documents. Distinguish implemented behavior from planned capabilities so people and agents can follow the delivery model reliably.

Test: Review confirms that the guide matches the selected pipeline, covers its supported paths and limitations, and has working reciprocal references to related guidance.

Status: Proposed

### PBI-018. Prove atomic task reservations under contention

Demonstrate that competing tasks cannot own the same component simultaneously. Cover complete scope expansion, interruption and safe reassignment so work cannot proceed under stale or partial authority.

Test: Demonstrate exactly one winner for synchronized conflicting requests, an unchanged rejected competitor and safe scope expansion and reassignment.

Status: Proposed

### PBI-019. Prove parallel component collaboration and integration

Validate independent Hello and World contributions from private developer areas through shared source control. Preserve both contributions while rejecting ownership violations, stale integration bases and unresolved shared-source conflicts.

Test: Demonstrate parallel contributions reaching one validated application with complete provenance, and rejection of conflicting or stale candidates.

Status: Proposed

### PBI-020. Complete APEX capture and reconstruction validation

Establish the supported capture and reconstruction contract across private application identities, page deletion and shared definitions. Extend the current replacement-identity experiment to the application settings and user state explicitly supported by the release.

Test: Demonstrate equivalent supported definitions and retained user state after reconstruction and repeat import, with missing dependencies and identity collisions rejected.

Status: Proposed

### PBI-021. Complete release admission and promotion negative coverage

Complete validation of the immutable release admission contract beyond the demonstrated delivery path. Ensure changed artifacts, stale candidate evidence, missing integration evidence and unsupported starting states cannot be promoted.

Test: Demonstrate each invalid release case rejects before target mutation and an unchanged accepted artifact repeats safely.

Status: Proposed

### PBI-022. Prove deployment ownership and maintenance fencing

Validate exclusive deployment authority across competing attempts, commits, interrupted controllers and stale workers. Ensure ordinary requests and existing sessions remain blocked throughout maintenance and verifier permissions expire before publication.

Test: Demonstrate one authorized writer, rejected stale attempts and blocked ordinary mutations throughout installation, interruption and verifier revocation.

Status: Proposed

### PBI-023. Detect schema drift and reconcile unauthorized changes

Extend drift protection to the database definitions included in the supported release. Preserve unexpected changes for an operator decision and require reviewed reconciliation or restoration before deployment resumes.

Test: Demonstrate manual schema changes and supported application changes are identified before deployment writes, with explicit reconciliation restoring a validated baseline.

Status: Proposed

### PBI-024. Validate recovery beyond the selected additive failure

Define the additional partial deployment states that can be safely resumed or repaired beyond the demonstrated additive-index failure. Preserve committed work and history while keeping unknown, incomplete or changed observations blocked.

Test: Demonstrate approved recovery for each newly supported partial state and refusal of unsupported or interveningly changed states without data loss.

Status: Proposed

### PBI-025. Restrict privileges and protect deployment credentials

Define the minimum authority and credential lifecycle required before the lab becomes a shared delivery service. Separate infrastructure administration from routine provisioning and deployment, retaining auditable authorization boundaries.

Test: Demonstrate routine operations succeed with their assigned privileges while unauthorized administration, credential access and cross-area mutations are denied.

Status: Proposed

### PBI-026. Minimize gateway exposure for shared hosting

Define the required gateway features and access restrictions before exposing the application beyond the private lab. Disable or restrict unused entry points while preserving the supported APEX runtime and administration paths.

Test: Verify only approved gateway features and identities remain accessible in the selected shared-hosting profile.

Status: Proposed

### PBI-027. Unify delivery environment configuration

Consolidate the authoritative environment definitions used by provisioning, delivery and operating guidance. Prevent divergent mappings from directing an operation toward the wrong schema, workspace or application.

Test: Demonstrate all supported operations use consistent validated mappings and reject conflicting environment definitions before mutation.

Status: Proposed

### PBI-028. Extend supported release and toolchain profiles

Define compatibility and qualification rules when another component release or Oracle toolchain is selected. Keep unsupported combinations blocked and require contract evidence before widening the currently supported version sets.

Test: Demonstrate an additional selected profile qualifies its supported starts and rejects incompatible component or toolchain combinations.

Status: Proposed

### PBI-029. Strengthen automation failure diagnostics

Make automation outcomes dependable when Oracle clients produce diagnostics that do not match the current error patterns. Retain actionable context while ensuring client completion messages cannot conceal failed operations.

Test: Demonstrate representative client and server failures return nonzero with an actionable operation-specific error and prevent subsequent mutation.

Status: Proposed

### PBI-030. Automate source validation in hosted CI

Run the database-independent source and script checks on the candidate revision in hosted automation. Make results visible to reviewers and invalidate them when the candidate or required integration base changes.

Test: Demonstrate a clean candidate passes, a deliberately broken candidate fails and changed revisions cannot reuse stale validation results.

Status: Proposed

### PBI-031. Establish independent release validation provenance

Provide independently verifiable evidence binding a release to the reviewed source and validation environment before shared automated promotion. Prevent a deployment actor from substituting self-asserted or modified integration evidence.

Test: Demonstrate promotion validates the evidence issuer and artifact binding and rejects altered, unauthorized or mismatched attestations.

Status: Proposed

### PBI-032. Resolve repository licensing and reference distribution

Decide and document the repository reuse license and the distribution treatment of third-party reference material. Make public reuse conditions clear and ensure distributed material has an approved basis or is replaced by an authoritative reference.

Test: Review confirms explicit repository reuse terms and approved distribution treatment for every retained third-party reference.

Status: Proposed

### PBI-033. Validate an additional infrastructure host platform

Establish a reproducible infrastructure path when a host platform beyond macOS Apple Silicon is selected. Include the complete database, APEX and gateway environment rather than treating a database container alone as equivalent.

Test: Demonstrate the selected additional platform completes clean provisioning and the supported delivery checks with its constraints documented.

Status: Proposed

### PBI-034. Automate application browser acceptance checks

Validate the user-visible application behavior through browser interaction in addition to SQL and runtime API checks. Cover supported account roles, validation, escaped content, history navigation and upgrade behavior.

Test: Demonstrate browser checks pass for the supported release and detect a deliberately broken greeting, authorization or history interaction.

Status: Proposed

### PBI-035. Validate adoption of an existing APEX application

Establish the optional future path from an existing application to an accepted source-controlled baseline. Capture required dependencies and provenance while excluding secrets and business data and preserving uncaptured work.

Test: Demonstrate controlled reconstruction of an adopted application and rejection of incomplete capture, unsafe overwrite or unverified source state.

Status: Proposed
