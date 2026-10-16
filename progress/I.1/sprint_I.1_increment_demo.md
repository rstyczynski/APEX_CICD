# Sprint I.1 — Product Owner presentation walkthrough

Companion to [the PowerPoint presentation](sprint_I.1_increment_demo.pptx) and [Product Owner handover](sprint_I.1_handover.md). This is an artifact walkthrough for the Inception increment. The application scenarios describe what Elaboration must demonstrate; they are not executable functionality delivered in I.1.

## Starting conditions

Use this project checkout and a presentation viewer. Keep the linked Markdown documents available for inspection. No running Oracle, APEX or Podman instance is required to review this increment. Design acceptance and sprint closure remain pending.

The presenter follows the nine stages below, opens the actual source document at each relevant stage, and invites the Product Owner to inspect the rule or ask for a different path. Record the actual review outcome in the handover after the review; file availability or rendering alone does not establish that the Product Owner viewed or accepted it.

## Walkthrough and slide references

1. **Purpose — slide 1.** Open the deck and the [handover recommendation](sprint_I.1_handover.md#recommendation). Explain the CI/CD concept and the bounded prototype that will test it. Expected result: the Product Owner can explain the evidence the next iteration should provide. Trace: PBI-003/007/010 and the accepted README vision.
2. **Analysis delivered — slide 2.** Open [the final engineering decisions](analysis_review-answers_2.md) and inspect the six corrected contracts. Expected result: clear distinction between a reviewed analysis direction and unproven runtime mechanisms. Show the scope of the [expert review](analysis_review_2.md), which predates the final edits. Trace: PBI-008/009/010.
3. **Components — slide 3.** Open [initial assembly](../../docs/architecture.md#initial-assembly-and-first-complete-release). Follow A's Foundation work, then B's Hello and C's World. Expected result: Foundation can complete its own checks while ordinary use remains blocked until the complete release is ready. Trace: UC-1, FR-7/9, PBI-004/005/009.
4. **Developer cycle — slide 4.** Inspect [the developer journey](../../docs/srs.md#complete-developer-journey) and [capture into Git](../../docs/architecture.md#capturing-developer-changes-into-a-git-branch). Identify when the task branch is created, how browser edits become files, and why post-merge archive qualification is a distinct gate. Expected result: an understandable path from task ownership to verified delivery. Trace: UC-7–11, FR-5/8/11, PBI-004/005/009.
5. **Everyday behavior — slide 5.** Inspect [the six demonstration scenarios](sprint_I.1_handover.md#six-simple-scenarios-for-the-future-demonstration), items 1–3. Follow the greeting, preserved history and parallel Hello/World changes. Expected result: three small observable demonstrations without extra business features. Trace: UC-1/2/3/4/7/9/10/11, PBI-004/007.
6. **Protection and failure — slide 6.** Inspect scenario items 4–6 and [future acceptance cases](../../docs/test-profile.md). Follow the simultaneous Hello request, incompatible/drifted release, and committed-DDL failure/repair. Expected result: the Product Owner can identify who is blocked, when rejection occurs, and which evidence proves history survived. Show that these tests remain unrun. Trace: UC-4/5/9, FR-6–10, PBI-005/008/009.
7. **Automation — slide 7.** Open [the tool/interface inventory](../../docs/architecture.md#automation-tools-and-interfaces). Select export, import or availability control and inspect its tool, supported interface and Elaboration obligation. Expected result: concrete automation paths and visible gaps, rather than a promise that API names alone prove automation. Trace: FR-13, PBI-009.
8. **Bounded prototype — slide 8.** Inspect [experiment order and architecture exit](../../docs/test-profile.md#elaboration-order-and-architecture-exit) and [the refinement proposal](sprint_I.1_proposedchanges.md). Expected result: an agreed small proof boundary, early reservation feasibility checks, and a decomposition/effort estimate before construction approval. Trace: PBI-006/007/008/010; future PBI-011–016.
9. **Elaboration outcomes — slide 9.** Return to [the Product Owner review section](sprint_I.1_handover.md#product-owner-review). Discuss the working delivery cycle, operating effort and evidence needed to accept or revise the architecture. Expected result: actual feedback or a recorded decision, without inferring acceptance. I.1 closure and E.1 activation follow their managed procedures separately. Trace: PBI-010 and the next Lifecycle Architecture assessment.

## Demonstration status

The deck and linked artifacts can be inspected now. Runtime behavior, concurrent acquisition, automated verification and repair remain future evidence. Rendering and package checks prepare the material; a presenter-led Product Owner review has not been recorded by preparing these files.
