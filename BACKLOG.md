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

### PBI-036. Define Oracle lifecycle use-case coverage

Extend the laboratory scenarios with the actor journeys presented in the Oracle lifecycle paper. Require traceability from every scenario in both Oracle-style iterations to exact paper pages and applicable version-specific Oracle documentation, with observed evidence and explicit scope decisions. Distinguish documented recommendations from project extensions so native tool adoption does not silently weaken existing acceptance criteria.

Test: Review complete bidirectional scenario-to-paper-and-Oracle-documentation coverage for both iterations, with assigned outcomes, evidence requirements and approved dispositions for deviations or exclusions.

Status: Proposed

### PBI-037. Establish native Oracle source capture and staging

Make application and database changes reviewable and reconstructible through the Oracle-recommended project lifecycle. Preserve complete dependencies, stable identities and intentional data changes without maintaining a competing source or migration authority.

Test: Demonstrate initial capture, a subsequent application and database change, reviewed distribution changes and reconstruction with consistent source identity.

Status: Proposed

### PBI-038. Deliver native Oracle release artifacts

Reproduce the initial release and compatible Hello upgrade using Oracle-recommended release and deployment capabilities. Qualify and promote the same artifact while retaining source identity, supported starting states and existing user data.

Test: Demonstrate fresh installation, baseline upgrade and safe repeat using one qualified native artifact per release, with unchanged prior data and traceable results.

Status: Proposed

### PBI-039. Demonstrate native team-centric APEX collaboration

Show a small team completing a fix in shared development using native page coordination and isolated working changes. Include refresh, comparison, integration and abandonment so developers understand when this approach fits and where schema isolation stops.

Test: Demonstrate competing page access, an isolated fix refreshed and merged into Main, and discarded experimental work without unintended application or data changes.

Status: Proposed

### PBI-040. Measure PL/SQL regression coverage with utPLSQL

Make business-logic regression results and measured code coverage available for the laboratory releases. Use uncovered behavior to improve the tests and make failures visible to release reviewers.

Test: Demonstrate a detected regression, archived test and coverage reports with an explicit denominator, and improved coverage after adding a missing test.

Status: Proposed

### PBI-041. Demonstrate Oracle-recommended application quality audits

Expose application quality, security and performance findings before release using the audits described in the Oracle paper. Show how a developer investigates and corrects a finding, with unavailable or optional external products clearly distinguished from executed checks.

Test: Demonstrate repeatable built-in audits and code inspection detecting a controlled finding, its correction and retained results with stated tool coverage.

Status: Proposed

### PBI-042. Synchronize central development after accepted merges

Keep the central development application aligned with the accepted source revision after a feature is integrated. Make stale builds and unexported work visible so synchronization cannot silently overwrite another developer contribution.

Test: Demonstrate an accepted merge reflected in central development and a blocked stale or unsafe refresh with pending work preserved.

Status: Proposed

### PBI-043. Operate the Oracle lifecycle automation pipelines

Automate the paper’s source-to-release and build-test-deploy journeys with reviewable run history and downloadable artifacts and test results. Failed tests must stop downstream deployment, while a changed candidate requires fresh validation.

Test: Demonstrate successful runs of both journeys and a failing test that blocks deployment, with attributable source, artifact and archived reports.

Status: Proposed

### PBI-044. Demonstrate native mini-app component reuse

Show the paper’s optional modular application pattern separately from the single-application greeting release. Explain shared component subscriptions, controlled propagation and seamless authenticated navigation without presenting them as independent versioning of page groups.

Test: Demonstrate a common component subscribed by two mini apps, publish and refresh behavior, and authenticated navigation across the applications.

Status: Proposed

### PBI-045. Preserve scenario protections around native Oracle delivery

Retain the demonstrated incompatible-upgrade rejection, live application drift protection and inspected additive-failure repair when adopting the native lifecycle. Identify which protections Oracle supplies and justify any remaining project-specific control with observed evidence.

Test: Demonstrate the three protection scenarios with native release artifacts, preserved prior data and failure evidence, and refusal of an interveningly changed repair state.

Status: Proposed

### PBI-046. Compare and independently reproduce the Oracle-style laboratory

Let another operator reproduce the Git-based Oracle-style exercise and compare it with both the earlier custom prototype and the APEX-native exercise. Require paper and version-specific Oracle-documentation traceability alongside matched scenario results, operating effort and remaining gaps. Preserve historical evidence and provide a decision-ready recommendation without assuming which approach should win.

Test: Demonstrate independent reproduction and review a three-approach comparison with source-backed Oracle conformance, attributable results, comparable measurements, limitations and an explicit Product Owner decision record.

Status: Proposed

### PBI-047. Compare APEX-native delivery with the earlier prototype

Provide an evidence-based comparison of the APEX-native exercise with the earlier custom delivery prototype before accepting the native iteration. Map the scenarios to the Oracle paper and applicable Oracle documentation and explain observed benefits, limitations and remaining custom responsibilities. Preserve absent historical measurements as unknown rather than assuming improvement.

Test: Review matched scenario evidence, Oracle traceability, operating and maintenance measures, limitations and a decision-ready recommendation at the APEX-native iteration handover.

Status: Proposed

### PBI-048. Prove an available compatible Foundation extension

Extend Foundation from 1.0.0 to 1.1.0 with optional greeting-language support while preserving the existing public contract and legacy behavior. Cover both the PL/SQL interface and database schema so unchanged Hello and World consumers continue reading and writing throughout deployment and data migration. Preserve existing history and configuration, and demonstrate recovery from an interrupted upgrade without interrupting supported consumers.

Test: Demonstrate continuous successful legacy reads and writes during upgrade and recovery, correct optional-language behavior after upgrade, and preserved history and configuration.

Status: Proposed

### PBI-049. Prove an available breaking Foundation transition

Introduce a Foundation 2.0.0 public contract requiring greeting templates and structured parameters in place of arbitrary-text submission, following the compatible Foundation extension. Keep the legacy 1.x contract operational while Hello and World adopt the new contract independently, including simultaneous reads and writes against the evolving database schema. Preserve previously recorded greetings and configuration, and establish the supported return to legacy operation after new-contract writes before retiring legacy support.

Test: Demonstrate continuous successful old and new contract traffic with one consumer migrated and the other unchanged, preserved data through interruption and return to legacy operation, and legacy retirement only after all old callers have left.

Status: Proposed

### PBI-050. Prove an in-place Foundation upgrade with component windows

Upgrade the existing Foundation deployment from 1.1.0 to the breaking 2.0.0 contract across its PL/SQL API and database schema while preserving history and configuration. Keep Hello and World using Foundation 1.1.0 until each moves to Foundation 2.0.0 during its own maintenance window. Limit unavailability to the component being migrated while the other continues reading and writing, including during the interval when they use different Foundation versions. Establish safe recovery from an interrupted component migration without disrupting the other component.

Test: Demonstrate separate Hello and World maintenance windows in the existing deployment, uninterrupted reads and writes by the other component, correct operation against Foundation 1.1.0 and 2.0.0 during coexistence, and preserved data through migration and interrupted-migration recovery.

Status: Proposed

### PBI-051. Assess the E.1 delivery approach against Oracle lifecycle guidance

Assess the existing E.1 delivery approach against the supplied Oracle APEX lifecycle guidance to establish an evidence-backed evolution direction. Distinguish technology limitations, implementation gaps and project policy conflicts, using focused exercises where needed to demonstrate problems or solutions. Produce traceable gap findings, proposed backlog items and a dependency-ordered roadmap toward the Oracle-recommended approach, with explicit evidence for blockers and justified deviations. Present the findings and required exercises through a reproducible walkthrough on the current E.1 technology.

Test: Review source-linked gap findings and blocker evidence through the walkthrough, reproduce required exercises and verify that proposed follow-up items and roadmap decisions follow the findings.

Status: Proposed

### PBI-052. Define semantic versioning rules for component contracts

Define the observable interfaces and compatibility promises of APEX and database components, and map changes to major, minor and patch version increments. Cover consumer-facing behavior, shared definitions and retained-data expectations so developers can classify breaking changes, compatible extensions and compatible fixes consistently. Connect these rules to component version and dependency declarations understood by the delivery toolchain without requiring automatic inference from code changes.

Test: Review representative APEX and database changes, including shared LOV changes, and demonstrate justified major, minor and patch classifications against explicit component contracts and consumer compatibility expectations.

Status: Proposed
