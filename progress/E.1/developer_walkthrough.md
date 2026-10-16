# E.1 — Use-case walkthrough: deployment results and protection

## What this walkthrough shows

- The Product Owner sees application outcomes after successful deployments and evidence that wrong deployments are blocked.
- Developer A/B/C operations run inside the guided stages. The Product Owner does not inspect App Builder, page definitions, SQL source or Git diffs in this workflow.
- Show the actual operation output and a short result: **DEPLOYED**, **REJECTED**, **ERROR** or **PENDING**.
- After a successful deployment, show its result in the running application at the printed URL.
- After an expected rejection, show the exact reason, verify the target was not overwritten, then open the application to demonstrate that its prior behavior and saved history remain intact.
- Keep the [detailed operator walkthrough](user_manual.md) unchanged as the separate technical operating reference.
- This document and [cicd-developer-walkthrough.sh](../../scripts/cicd-developer-walkthrough.sh) are **one artifact**. Always update and review both together.

## Alignment with selected Elaboration use cases

- This is an **end-to-end use-case walkthrough** of the selected E.1 slice. A/B/C stages organize the journey; the Product Owner sees application results and deployment protection.
- The [SRS use cases](../../docs/srs.md#use-cases-and-success-criteria) define actor goals and success criteria.
- The [accepted E.1 design](sprint_E.1_design.md#first-implementation--happy-path), its DevOps section and its two selected unhappy scenarios define the implementation selection.

1. **A / Foundation:** UC-9 task preparation, UC-10 source capture, UC-7 review/integration, UC-1 Foundation assembly, UC-4 controlled delivery and UC-11 verification. The first assembly remains blocked until dependents exist.
2. **B / Hello and C / World:** UC-9 → UC-10 → UC-7 → UC-4 → UC-11, executed sequentially in the first slice. Developer and reviewer decisions stay explicit even though their technical operations are grouped inside the stage.
3. **Use the completed application:** UC-2 component configuration and UC-3 greeting/history, followed by UC-11 delivery verification.
4. **Qualify/promote and compatible Hello patch:** UC-4 delivery plus UC-1's supported upgrade checks, UC-2/3 behavior/history and UC-11 verification. Qualify/promote identical bytes; preserve settings/history through Hello 1.0.0 → 1.0.1.
5. **Reject an incompatible Foundation upgrade:** the incompatible-target alternative in UC-1 and failed-check protection in UC-4. The expected outcome is rejection before writes, with the working target unchanged.
6. **Reject unexpected live drift:** UC-4's stop-before-overwrite alternative and UC-5's drift-detection entry. Demonstrating rejection does not complete UC-5's reconciliation/repair flow.

- **Prerequisites:** provisioning/onboarding from UC-8 and the separate infrastructure/operator procedures. They are not repeated as Product Owner technical inspections here.
- **Reproduction:** this guide contributes to UC-6; its full success criterion is not met by an unattended runner execution.
- **Later evidence outside this selected walkthrough:** parallel Hello/World work, the competing Hello race and other reservation alternatives in UC-9; deployment races/interruption; failed additive deployment and automated repair in UC-5. These remain in the broader design.
- **Unselected:** UC-12 adoption of an existing application. This prototype creates the application from scratch without constructing a supplied seed application.
- **Execution status:** this mapping describes intended coverage, not passed acceptance. Only the current Foundation checks/runtime checkpoint execute; the stages below remain pending as stated.

## Current readiness

- A's Foundation database and application shell exist. Its runtime displays the assembly-blocked message.
- The script can show that current runtime result after internal database checks. This is not a new deployment.
- B contains reviewed Foundation/Hello source; C contains the reviewed World addition and all three database components. Shared composition/browser verification and the grouped delivery/release/rejection demonstrations remain under construction.
- The complete positive/negative deployment demonstration is therefore **not ready**.
- The current script stops with **PENDING**, status 3, before B. It does not print successful deployment or rejection claims for those missing operations.

## Run the results walkthrough

1. Open a Bash terminal in the project:

   ```bash
   cd /Users/rstyczynski/projects/APEX_CICD
   ```

2. Start this separate walkthrough:

   ```bash
   bash scripts/cicd-developer-walkthrough.sh
   ```

3. Read the next developer operation's purpose.
4. Press any key to run it, or **q** to stop.
5. Read the displayed pipeline outcome and any error or rejection reason.
6. When prompted, open the printed **runtime URL** and use the application as described.
7. Press a key to proceed to the next implemented stage.

- No App Builder login or technical inspection is requested.
- An unexpected error stops the workflow.
- An expected negative scenario counts as protected only when the specific rejection and unchanged-target checks pass. A connection error or arbitrary failure is not a successful protection demonstration.
- Browser continuation is not reported as an automated browser test.
- Run with **--preflight** for local tool/file/chapter checks without Oracle access.
- Run with **--rehearse** for the implemented CLI checks without pauses; human viewing is explicitly skipped.
- Current modes all leave unfinished delivery stages pending. Rehearsal also ends with status 3.

## A. Deliver Foundation

### Developer operations inside the stage

1. Establish Foundation from its accepted source and database changes.
2. Verify installed Foundation version, absent Hello/World and blocked incomplete assembly.
3. Show the real operation result.

- The current implementation performs only checks of the already existing Foundation, not steps to redeploy it.
- Internal checks use lab-dev and lab-control; their output is visible but does not require Product Owner technical inspection.

### Product Owner result

1. Open [A's runtime](http://127.0.0.1:8080/ords/f?p=810001:1).
2. See **Application Not Available** and **Foundation assembly: Hello and World are not installed.**
3. Continue in the terminal.

- The useful result at this stage is protection from using an incomplete application.
- This maintenance screen does not prove protection against an incompatible or drifted deployment. Those scenarios require the later real rejection checks.

## B. Deliver Hello — pending construction

### Developer operations inside the stage

1. Reserve Hello and prepare B's private area from accepted Foundation source.
2. Apply the reviewed Hello change and its database migration.
3. Capture/validate/integrate the scoped source and verify the resulting assembly.
4. Show the operation result and resulting runtime URL.

### Product Owner result — available after construction

1. Open the runtime URL printed by the stage.
2. See that complete-application access remains blocked while World is missing.
3. Continue to World delivery.

- No page-definition review is required.
- Hello's usable behavior is demonstrated in the completed application after World is integrated.
- E1_DEV_B / application 810002 now contains the blocked Hello assembly. The grouped delivery/replay operation is still pending.

## C. Deliver World and complete the assembly — pending construction

### Developer operations inside the stage

1. Prepare C from the accepted Foundation-plus-Hello baseline.
2. Apply and integrate the reviewed World change and migration.
3. Verify the complete Foundation/Hello/World assembly before publishing readiness.
4. Show the resulting application URL and installed versions.

### Product Owner result — available after construction

1. Open the printed runtime URL and sign in with the provided runtime account.
2. Enter Hello and World values through the application.
3. Generate a composed greeting and save it.
4. Refresh and reopen history to see the saved snapshot.
5. Continue in the terminal.

- The terminal shows versions **1.0.0 / 1.0.0 / 1.0.0** and actual successful verification output.
- The first slice runs B/C sequentially; it does not claim concurrent-development proof.
- E1_DEV_C / application 810003 contains all three components under verification; its runtime is not yet published.

## Release and compatible update — pending construction

1. Run the stage that builds one accepted artifact and qualifies it in the disposable area.
2. Open the printed qualification URL and use the greeting application.
3. Continue to promotion of the **same artifact bytes** into retained TEST.
4. Open the printed TEST URL, create a greeting and reopen its saved history.
5. Continue to the compatible Hello patch deployment.
6. Reopen TEST and see the corrected Hello behavior, retained configuration and earlier greetings.

- The pipeline shows the same qualified/promoted artifact hash and real deployment outcomes.
- The patch advances Hello to **1.0.1**, with Foundation and World remaining **1.0.0**.
- Qualification application 810004 and TEST application 810005 are not deployed yet.

## Reject an incompatible database upgrade — pending construction

1. Start from the working TEST release with saved greetings.
2. Press a key to attempt the proposed Foundation major upgrade while its installed dependents still require the older contract.
3. Read **REJECTED**, with the specific incompatible dependency/version reason.
4. See the pipeline verification that rejection occurred before database migration or application import, with installed versions/definitions and history unchanged.
5. Open the same TEST URL and use the existing greeting behavior.
6. Reopen earlier history to see that the rejected deployment left it intact.

- Success means a known incompatible change was stopped before it changed the database.
- A failed database migration is not the intended protection result.
- The compatible patch above must succeed as well, so a pipeline that rejects everything cannot pass.

## Reject deployment over unexpected live change — pending construction

1. Start from the working TEST release and its accepted fingerprint.
2. Run the controlled scenario that changes a visible page attribute without changing its component version.
3. Open TEST to see that deliberately changed result.
4. Continue to a deployment attempt against the earlier accepted baseline.
5. Read **REJECTED**, with the actual live-fingerprint mismatch reason.
6. See verification that no migration/import overwrote the target and retained history is unchanged.
7. Refresh the same URL to see that the direct change and earlier greetings are still present.

- Do not silently capture or accept that change as a new release baseline.
- Any restoration/reconciliation follows the reviewed procedure after the demonstration.
- This is a controlled prototype scenario, not permission for unrestricted target editing.

## Maintain this artifact

- Always change this document and its own runner together.
- Use numbered actions, short outcome bullets and runtime URLs.
- Keep developer mechanics inside the stage; retain their real output for diagnosis.
- Add **DEPLOYED** or **REJECTED** only after the corresponding operation and verification exist.
- Keep incomplete stages **PENDING** and preserve existing operator walkthroughs.
- The [accepted design](sprint_E.1_design.md) remains the source for the positive patch, incompatibility and drift acceptance criteria.
