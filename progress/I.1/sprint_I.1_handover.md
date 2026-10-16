# Sprint I.1 — Product Owner handover

Date: 2026-10-16. Status: accepted and closed by explicit Product Owner decision. Sprint: “APEX CI/CD research and Inception baseline,” formerly Sprint 1. Earlier pending statements below describe the prepared handover and are superseded by the final decision at the end.

Presentation companion: [PowerPoint](sprint_I.1_increment_demo.pptx) and [slide-by-slide artifact walkthrough](sprint_I.1_increment_demo.md).

## Recommendation

Proceed to a bounded Elaboration prototype. The analysis now covers the core developer-to-release journey and identifies concrete experiments for the remaining risks. Elaboration should establish whether Oracle's available tools support the proposed workflow and how much effort it takes to operate.

Keep the prototype small: one APEX application, three logical components, private developer areas on one host, explicit compatibility rules, a small ownership/state model and scripts using supported Oracle interfaces. The example must show a successful change, early rejection of competing Hello work, and failure followed by repair with history retained. There is no recommendation to build a general delivery platform.

Technical feasibility and effort are still unmeasured. Elaboration setup must decompose the prototype into reviewable experiments and give an effort/resource estimate before construction approval. If the agreed effort is exceeded or a critical assumption fails, review the scope and recommend a smaller approach or further Elaboration. More Elaboration may be needed; the core demonstration must not quietly disappear to fit a sprint.

## What Inception has produced

The product is a reproducible delivery example and operating guidance for APEX developers and DevOps engineers. Hello and World provide a deliberately small application with configurable greetings and persistent history, making code changes and data preservation visible.

The proposed baseline contains:

- [SRS](../../docs/srs.md): five actors, twelve use cases, requirements, initial release scope and risks. It covers onboarding, initial source adoption, Foundation-first assembly, development, integration, delivery and recovery.
- [Candidate architecture](../../docs/architecture.md): repository authority, component versions, ownership, isolation, exact-artifact qualification, drift protection, maintenance and repair. Its automation inventory enumerates tool, purpose, interface, permissions and validation obligations.
- [Research and alternatives](../../docs/cicd-research.md): the supplied lifecycle PDF, version-specific Oracle sources and independent practitioner material. The recommendation is SQLcl split exports with explicit migrations through its bundled Liquibase; SQLcl PROJECT remains the integrated alternative to reconsider if custom orchestration becomes disproportionate.
- [Infrastructure procedure](../../docs/deploy.md): I.1-owned lifecycle guidance assessed against identified Podman, database, APEX and ORDS versions. Elaboration takes responsibility for execution/adaptation and must preserve retained data, credentials and unrelated resources.
- [Test profile](../../docs/test-profile.md) and [continuation proposal](sprint_I.1_proposedchanges.md): proposed commands, observable acceptance cases and the checkpoint for refining the next prototype before implementation.

An independent expert reviewed the analysis twice. The six findings concern shared ownership, release qualification, maintenance verification, partial-state repair, the supported developer topology and initial assembly. [My final decisions](analysis_review-answers_2.md) explain the resulting document corrections. The [final expert review](analysis_review_2.md) assessed the preceding baseline and clarification; it is not a post-correction endorsement.

## Six simple scenarios for the future demonstration

1. **Build the system together.** A delivers Foundation; B adds Hello; C adds World. Foundation can be verified before the complete application exists, while ordinary use remains blocked. The first complete release requires all three compatible components. Covers UC-1/7/9/10/11.
2. **Use the application.** Configure Hello and World, create a greeting and inspect history. Change configuration and show that earlier greetings retain their original values. Covers UC-2/3.
3. **Develop in parallel.** B changes Hello while C changes World in separate areas and branches. Integrate through PR checks, qualify the accepted archive and deploy it; demonstrate that both changes survive. Covers UC-7/9/10/4.
4. **Reject a conflicting task immediately.** B and C request Hello concurrently. Exactly one obtains ownership; the other receives the owner/task conflict before managed editing. The running application remains healthy. Covers UC-9.
5. **Block an unsafe release.** Try an incompatible component set and, separately, a target changed outside the pipeline. Reject each before overwrite, retain the reason and route any retained emergency change through reviewed reconciliation. Covers UC-4/5.
6. **Recover from failure.** Inject a failure after an additive database change. Keep ordinary access blocked, inspect the partial state, execute an approved automated repair and show unchanged earlier history. Covers UC-5.

Onboarding provides the starting conditions through UC-8. UC-12 adopts an application that already exists; a new system instead starts from a reviewed seed. UC-11 prepares the next task, and UC-6 requires independent operator reproduction. These scenarios are specified for demonstration; they have not been executed.

## What the prototype must tell us

The main questions are whether capture/import preserves developer intent, whether the workflow prevents conflicting managed work, whether qualified releases are repeatable, and whether failure can be repaired without losing history. Also record setup effort, run times, peak resource use, manual decision points, custom code required and practical operating friction. Use these observations to judge whether the workflow is useful and manageable; test results alone do not answer that question.

Test bootstrap/topology and minimal atomic reservations early. Then prove initial assembly, stable capture/integration, archive qualification and guarded delivery/repair before completing the A/B/C journey. Full page polish, additional workstation variants and remote runner integration can wait when unnecessary for these experiments. Generic dependency resolution, a separate control service, independent production component deployment and production operations are outside this prototype recommendation.

After the experiments, recommend Construction when the core workflow is proven and the remaining work is understood. Otherwise simplify the approach or identify the next focused Elaboration experiment. Critical unresolved safety/feasibility gaps prevent architecture acceptance.

## Evidence and current limits

I.1 produced research, analysis, review decisions and document consistency checks. Read-only platform observations and script syntax checks support the environment assessment. Historical browser/restart checks are identified separately in the infrastructure procedure. The [documentation audit](sprint_I.1_documentation_audit.md) records the evidence and approval dependencies.

No application, pipeline, reservation controller, state engine or automated repair has been delivered or proven by this sprint. SQLcl/Java provisioning and the supported API/permission paths remain Elaboration obligations. Supporting lifecycle scripts still require reviewed source adoption. The prototype must establish repeatability and recovery in practice.

## Product Owner review

Start with the six scenarios above, then inspect the [final decisions](analysis_review-answers_2.md), [SRS](../../docs/srs.md), [architecture](../../docs/architecture.md) and [test profile](../../docs/test-profile.md) where detail is needed. The review should establish whether the scenarios explain the intended value, the scope is small enough, and the proposed evidence is sufficient to judge whether the architecture works.

The requested decision is acceptance of the revised Inception direction and bounded Elaboration objective, or specific corrections. No acceptance is recorded on the Product Owner's behalf. I.1 remains Progress and E.1 remains Planned. The presentation pair is prepared. Managed approval, completion audits/commits and the presenter-led artifact review remain pending; this prepared handover does not claim they occurred or authorize E.1 to start. No push is authorized.

## Final Product Owner decision — 2026-10-16

In the E.1 startup instruction, the Product Owner explicitly accepted the revised I.1 analysis baseline with the presentation wording correction, requested completion of I.1 handover/audits/closure, and authorized E.1 activation once I.1 is closed. After the current artifact-review summary and handover question, the Product Owner stated: “sprint I.1 closed, all accetped”. This is the explicit acceptance and closure instruction. It does not authorize remote pushes or E.1 construction before its design approval.

The current review explained Foundation-first assembly, private-area Hello/World collaboration and the early Hello race, exact-artifact qualification, drift rejection and inspected automated repair. The requested documents were read. Attempts to display the walkthrough, SRS and architecture through open_in_codex returned queued; no new live display or operator interaction is asserted. The existing wording-corrected deck is byte-identical to its retained visual-validation receipt. No application demonstration occurred in I.1.

The implementor initially described the closure decision as a waiver of the remaining display requirement. The Product Owner challenged that characterization; it is not the recorded decision. Record the acceptance and closure instruction above exactly, retain the actual review limits, and proceed to E.1 under the supplied authority.

The [final review results](sprint_I.1_tests.md), [documentation summary](sprint_I.1_documentation.md), [operating reference](user_manual.md) and [audit](sprint_I.1_documentation_audit.md) support closure. The accepted scope remains analysis and candidate architecture; runtime feasibility and effort remain unproven.
