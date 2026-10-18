# RUP Patch — Method Adoption and Iteration Semantics

This is an optional local wrapper over the canonical RUP Strikes Back method in the `RUPStrikesBack` submodule. A project may use RUP Strikes Back without this directory. When this wrapper is present, its policies refine or override the generic method only where stated below.

## P0. Include RUP Strikes Back as a controlled project method

The project adopts RUP Strikes Back through the `RUPStrikesBack` Git submodule, tracked on the selected method branch and pinned by this repository’s Git submodule revision. The submodule is the source for the generic manager, phase-agent procedures, sprint/backlog formats, and generic rules.

The project root contains the local adoption layer:

1. `.gitmodules` registers the RUP Strikes Back submodule and selected branch.
2. `AGENTS.md` tells Codex where the method is and when to use it.
3. `RUPStrikesBack.patch/RUP_patch.md` records project-specific method refinements and overrides; the root `RUP_patch.md` is its compatibility entry point.
4. `.agents/skills/rup-strikes-back/` is the Codex cycle entry point, while `rup-backlog`, `rup-sprint`, and `rup-progress` are mandatory artifact adapters. Their references map to the canonical manager, command, and phase procedures in the submodule.
5. `BACKLOG.md` holds Product Owner priorities and backlog-item acceptance signals.
6. `PLAN.md` holds RUP Strikes Back sprint definitions, statuses, modes, and quality expectations.

Do not copy the submodule’s `AGENTS.md`, `HUMANS.md`, `RUP_patch.md`, or Claude command files into the project root. The local `AGENTS.md`, this patch, and the Codex skill provide the project-specific integration layer. The submodule remains the canonical generic agentic method; Codex adapters provide host-specific invocation and apply local refinements.

Update the submodule only through an explicit Product Owner request. Before adopting an update, review the changed method rules, confirm that this patch and the Codex wrapper still apply, and commit the resulting submodule revision together with any required local changes. Do not update the method during an active sprint unless the Product Owner explicitly treats it as a process change.

## P0.phase. Use stable phase-based sprint IDs

By Product Owner direction on 7 October 2026, project sprint scheduling uses
`I.n` for Inception and `E.n` for Elaboration. The Product Owner
also designated `ES.1` for the deferred Elaboration baseline. The ordinal advances within its phase prefix; inserting work in
another phase does not renumber a sprint. The current mapping is recorded in
`PLAN.md`. In this project, these phase IDs override the generic numeric,
gap-free sprint-number rule and are the labels in `PLAN.md` and
`PROGRESS_BOARD.md`.

By Product Owner direction on 9 October 2026, historical evidence directories
also use phase IDs, with maintained links and scripts updated to those paths.
Sprint evidence uses the phase ID in its path, for example `progress/E.5/`.
`PLAN.md` records the former numeric labels. Historical filenames, raw outputs,
logs and decisions retain their original content; paths recorded inside raw
evidence describe the location at execution time. `ES` is still Elaboration.
Reserve `C.n` for work actually classified as Construction.

## P0.0. Establish the Git baseline during bootstrap

Bootstrap validates that the project is a Git repository and has an `origin` remote. If Git is absent, bootstrap initializes the repository and uses `main` as its default branch. If `origin` is absent, bootstrap creates a private repository on GitHub.com using the authenticated GitHub account, names it after the project directory, and configures it as `origin`. An existing origin is preserved; bootstrap does not rewrite it or force-push.

After installing only the method and generic-bootstrap artifacts, bootstrap creates one semantic baseline commit and pushes the current branch to `origin`. This authorization applies to the bootstrap flow itself. Subsequent remote repositories, remote changes, and pushes still require an explicit Product Owner request.

## P0.1. Initialize process artifacts when needed

`BACKLOG.md` and `PLAN.md` are created before the first sprint. Progress artifacts, including `PROGRESS_BOARD.md` and sprint-specific records under `progress/`, are created and maintained by the RUP Strikes Back cycle when a sprint starts; do not create placeholder progress files in advance unless the Product Owner explicitly requests a pre-sprint artifact. Such a file does not start the sprint.

Before the first code-bearing sprint, define the project’s test profile in this patch or a referenced project rule. The project uses `docs/test-profile.md` for this purpose. It must map the generic test and regression fields to the actual project’s build, smoke-test, unit-test, integration-test, and applicable operational-validation commands. Do not claim that the submodule’s sample shell-test commands apply to the project. A test-profile template does not satisfy this gate: PBI-009 must replace its pending command fields with the candidate architecture's actual commands before Sprint 2 starts.

## P0.2. Generic artifacts bootstrap Sprint 0

`RUPStrikesBack.patch/bootstrap/` contains reusable RUP roadmap, backlog, sprint-plan, and test-profile templates, a generic `AGENTS.md`, and Codex skill adapters. `RUPStrikesBack.patch/BOOTSTRAP_PROMPT.md` is the operator-only bootstrap prompt and is deliberately kept outside the overlay. These artifacts are inputs to Sprint 0 only; they are not product requirements or active product backlog items. The bootstrap plan preselects Sprint 0 with `Status: Progress`, but execution still requires an explicit Product Owner request.

At project initialization, overlay the complete contents of `RUPStrikesBack.patch/bootstrap/` onto the project root, including hidden directories. Do not copy `RUPStrikesBack.patch/BOOTSTRAP_PROMPT.md` into the project root. The Product Owner explicitly requests execution of the preselected Sprint 0 and supplies the initial product intent through the working conversation. PBI-001 creates and accepts the project `README.md` as the vision product. Sprint 0 then derives this project’s real roadmap and proposes the next sprint from that vision. The generic later-sprint entries are initial hypotheses: Sprint 0 or subsequent iterations may retain, refine, split, reorder, or replace them. After Sprint 0, the root project artifacts—not the generic templates—are the sources of truth for the project’s scope and delivery work.

The generic bootstrap is deliberately tailored over its first three iterations. Sprint 0 proposes an initial lifecycle and iteration plan from the vision. Sprint 1 tests and refines that plan against business context, requirements, scope, risks, and an initial architecture. Sprint 2 refines it again from technical-validation evidence and the Lifecycle Architecture assessment. In each of these iterations, the agent must propose additions, removals, mergers, splits, reordered work, or a simpler path when the project’s size, uncertainty, existing assets, constraints, or risk profile justify it. In managed mode, the Product Owner accepts each material plan change. The plan must record the decision and rationale; generic tasks are defaults, never mandatory ceremony.

## P0.3. Place project artifacts by lifecycle role

The root `README.md` holds the accepted product vision and project orientation. `docs/` holds durable shared project deliverables created and accepted during sprints, such as requirements, architecture, decisions, and operating documentation.

`progress/<phase-ID>/` directories hold evidence and review artifacts for one sprint, including migrated historical evidence. `tmp/` holds provisional material retained only for reference; it is not a source of truth and must be recreated in `docs/` or another approved location when a sprint formally delivers it. `RUPStrikesBack.patch/bootstrap/` remains the reusable bootstrap input described above.

## P0.4. Anchor progress-board items to an assigned sprint

`PROGRESS_BOARD.md` follows the canonical four-column form and tracks both a
sprint's real-time status and the real-time statuses of backlog items assigned
to that sprint. Every backlog-item row must name the Sprint that contains the
item in `PLAN.md`; an unscheduled item never receives a standalone progress
board row.

A Product Owner may promote an accepted review or feedback proposal into the
root backlog with `Status: Proposed`. It remains there, without a progress
board row, until the Product Owner prioritizes and assigns it to a named Sprint
in `PLAN.md`. The sprint procedure then creates its board row. This refines the
canonical `/backlog add` instruction only for unscheduled proposals.

## P1. Apply the RUP Strikes Back cycle proportionately

The Codex RUP Strikes Back manager's complete contracting, analysis/design, construction, quality-validation, and wrap-up pipeline is primarily a code-bearing Construction-iteration workflow. It should run fully when a sprint creates or materially changes production code.

Sprint 0 and Inception iterations use the same collaboration discipline, but produce vision, requirements, plans, risk evidence, and reviews rather than forcing implementation. An Elaboration iteration may construct a prototype and run technical tests when that is needed to retire risk, but it need not produce a production feature. In non-code-bearing iterations, construction and automated-test gates may be not applicable; the plan and sprint evidence must state the reason and define the appropriate review or experiment instead.

This is not a waterfall handoff. Every iteration consciously considers the relevant RUP disciplines, at a depth proportional to its purpose, risk, and lifecycle phase. The RUP Strikes Back workflow inside an iteration does not itself advance the product from one project-level RUP phase to the next.

## P1.1. Use progressive plan refinement as a first-class outcome

The plan is an evolving project artifact, not a one-time bootstrap output. Sprint 0 creates the initial project plan. Sprint 1 establishes or revises the Inception plan and evaluates the Lifecycle Objectives decision. Sprint 2 establishes or revises the Construction plan from technical evidence and evaluates the Lifecycle Architecture decision. Later iterations continue to refine scope, risks, ordering, quality expectations, and release plans when evidence requires it.

## P1.2. Materialize durable Inception requirements and architecture artifacts

When an Inception iteration establishes the initial requirements, PBI-005
materializes `docs/srs.md` as the Software Requirements Specification (SRS).
It records the accepted system boundary, stakeholders, use cases and success
criteria, functional and non-functional requirements, initial release scope,
constraints, assumptions, and risks needed to guide the next iteration.

PBI-009 materializes `docs/architecture.md` as the accepted candidate
architecture. It explains how the proposed architecture supports the SRS,
identifies the assumptions requiring Elaboration validation, and defines the
project's concrete test-profile commands before a code-bearing iteration
starts. An accepted candidate architecture is an accepted direction for
validation, not evidence that its technical risks have been retired.

These artifacts are created from the accepted project vision during Inception;
they are not blank bootstrap templates. Later iterations refine them when
validation evidence or product decisions change their content. The Inception
review evaluates them together with the Product Backlog and test profile.

### Keep materialized documents connected

By Product Owner direction on 2026-10-18, every new or materially revised project document must identify its related authoritative documents with descriptive, actionable links. Add a reciprocal reference in the related maintained document so humans and agents can navigate from either side. State the relationship and which document owns requirements, design, operating steps or evidence; avoid duplicating specifications that can drift. Use section links where useful.

When a source decision, interface, path or status changes, review the connected documents and update affected descriptions, links and backlinks in the same increment. Preserve historical sprint evidence rather than rewriting it; link to its successor/current interpretation from maintained guidance. Validate link targets and relevant anchors during P8, and explicitly label drafts, planned behavior and remaining gaps. For backlog definitions, retain the canonical concise item format: link from the elaboration/delivery guide to the item and place reciprocal navigation in the maintained project orientation, rather than embedding implementation paths in the backlog. This is the local materialization rule; it does not authorize changing the canonical method submodule or unrelated sprints.

## P1.3. Adopt RUP analysis and use-case modeling explicitly

By explicit Product Owner instruction on 2026-10-16, RUP Strikes Back is the project's agentic adaptation of the Rational Unified Process (RUP). Apply RUP's use-case-driven, architecture-centric, iterative and risk-driven approach throughout delivery. The implementor is responsible for performing the analysis and explaining technical recommendations; the Product Owner supplies product intent, priorities and acceptance decisions.

Identify the system boundary and external interactions before designing the solution. The SRS must contain a separate **Actors** chapter that explicitly enumerates human roles and relevant external-system actors, gives each a stable identifier, and describes its responsibilities and goals. Distinguish actors from stakeholders, internal system components and individual people occupying the same role. Do not substitute scattered references to participants for an actor model.

Define actor-goal use cases covering the representative end-to-end journeys. Each use case must identify its primary actor, supporting actors where applicable, observable outcome and success criterion. Describe triggers/preconditions, the main flow, material alternative/failure flows and postconditions for architecturally significant or high-risk cases. Identify the remaining cases at a proportionate level during Inception and refine them from evidence during Elaboration. Include onboarding, environment preparation, ordinary work, integration, operation and recovery when they are part of the accepted system boundary; technical pipeline steps alone do not describe a complete actor journey.

Keep requirements focused on externally observable behavior. Put implementation mechanisms and technical recommendations in the architecture/design and trace them to actor goals, requirements, risks and validation evidence. Review actor coverage and complete journeys before presenting the Inception baseline for acceptance; missing actors or unexplained gaps must be corrected. Scale detail to the project's size and phase under P1; use diagrams when they improve understanding and avoid duplicating the same specification across artifacts.

General RUP supplies the analysis discipline; the canonical RUP Strikes Back procedures and this local patch govern artifact routing, approvals and sprint transitions. References: [IBM Rational RUP best practices](https://public.dhe.ibm.com/software/rational/web/whitepapers/2003/rup_bestpractices.pdf), [actors in modeling](https://www.ibm.com/docs/en/dma?topic=diagrams-actors), and [use-case specification outline](https://www.ibm.com/docs/en/engineering-lifecycle-management-suite/doors-next/7.2.0?topic=cases-use-case-specification-outline).

## P2. Project lifecycle phases set emphasis; they do not prohibit refinement

The project lifecycle remains Inception, Elaboration, Construction, and Transition. These phases establish the dominant emphasis of the work:

- Inception emphasizes business context, vision, requirements, scope, and major risks.
- Elaboration emphasizes architecture, risk retirement, design, and validation.
- Construction emphasizes implementation and testing.
- Transition emphasizes deployment, stabilization, and user feedback.

All disciplines remain open to refinement in later iterations. In particular, business modeling and requirements are mostly established early, but evidence from design, implementation, testing, or use may require them to be revisited.

## P3. Sprint wrap-up is not necessarily project Transition

The RUP Strikes Back wrap-up phase completes and documents a sprint. It does not by itself mean that the product has entered the project-level Transition phase or is ready for release. Project-level Transition occurs when the project plan declares release, deployment, and adoption activities to be the dominant focus.

## P4. A sprint may deliver multiple coherent outcomes

A sprint may contain multiple independently coherent backlog items when they share a common iteration objective, have manageable dependencies, and can be reviewed together. This is particularly appropriate for Inception and Elaboration, where one iteration can establish several connected artifacts such as requirements, risks, scope, and an architecture baseline.

Each backlog item must retain its own value statement and acceptance signal. The sprint design and wrap-up must identify the evidence for each item, so grouping does not hide incomplete work or weaken traceability. Split items into separate sprints when their dependencies, risk, approval needs, or validation methods would make a single review unclear.

## P5. Process entry point and local method adoption

The project root `BACKLOG.md` is the source of Product Owner priorities. The project root `PLAN.md` is the source of sprint selection and status. When installed, the root `RUP_patch.md` points to `RUPStrikesBack.patch/RUP_patch.md`, which defines local policy that supplements or overrides the generic method in the `RUPStrikesBack` submodule.

Sprint 0 is marked `Progress` by the bootstrap plan. To execute it, the Product Owner explicitly invokes the Codex `rup-strikes-back` skill in the declared mode. For a later planned sprint, the Product Owner first changes that sprint’s status in the root `PLAN.md` from `Planned` to `Progress`, then explicitly invokes the skill. The agent reads its manager and selected phase procedures from `.agents/skills/rup-strikes-back/references/`, then applies this local patch before executing the sprint.

`rup-strikes-back` is the Codex method entry point. The submodule's `/rup-manager` is a Claude compatibility command, not a native Codex command. Managed mode remains the default: the agent pauses for Product Owner approval at the defined decision points.

## P6. Refine prototype work into hierarchical sub-PBIs

When an accepted Inception architecture identifies a prototype PBI that spans
several independently reviewable pieces of work, the following Elaboration
iteration must refine that parent PBI before prototype construction. This is a
required planning checkpoint, not permission to invent the work during
Inception.

Use hierarchical identifiers in the form `PBI-XX.YY`, where `PBI-XX` is the
accepted parent PBI and `YY` is a sequential child number. For example,
`PBI-011.1`, `PBI-011.2`, and `PBI-011.3` are child work items of `PBI-011`.

Create the child items during the Elaboration sprint's setup/design phase, in
the active sprint's design record. Each child item must state its parent, its
bounded outcome, its acceptance evidence, and its dependency on other child
items. Record the same identifiers on the progress board for status tracking.

Child sub-PBIs are sprint-scoped refinements of their parent, not new
Product-Owner backlog items. Keep the parent PBI in the root `BACKLOG.md` and
`PLAN.md`; promote a child to a new root backlog item only when it gains
independent product value, priority, or deferral authority. In managed mode,
the Product Owner approves the proposed decomposition before prototype
construction starts.

## P7. Read the separate Product Owner preferences file

`RUPStrikesBack.patch/USER_PREFERENCES.md` is this project's plain Markdown
customization file for durable preferences explicitly stated by the Product
Owner. Read it alongside this patch before drafting new or revised
project-authored narrative artifacts or a sprint review. The Product Owner
may amend it through an explicit request; do not infer durable preferences
from incidental conversation. A preference does not change a mandatory
method-defined artifact structure unless the Product Owner explicitly asks
for that process change.

## P8. Reconcile documentation and verify before each commit

Work may use multiple edits while completing one increment. An increment is
an assigned PBI or a sprint-tracked child PBI with its own completion
evidence. Do not commit after each file change or merely because a phase has
advanced. After each increment is complete, reconcile its code, tests, and
documentation as one unit. Before committing it, create or update the active
sprint's documentation audit under `progress/sprint_N/`. The audit must check
the root SRS, architecture, test profile, sprint setup, accepted design and
test specification, implementation record, functional test record, README,
and progress board against the latest Product Owner decisions and actual
executable behavior. Record each checked artifact, the evidence inspected,
corrections made, and any unresolved approval or implementation dependency.
Check copy-paste commands and expected output against real execution before
calling them working examples. Label proposed commands and unrun tests as
pending. Keep the required progress-board table, but follow
`USER_PREFERENCES.md` for narrative documents.

Run the applicable build, tests, experiments, syntax or link checks, and
`git diff --check` before the commit. Record the exact checks and their
results in the sprint evidence. A failed check or unresolved material design
approval blocks that PBI's completion commit. Stage and commit the completed
increment's implementation, tests, documentation, and audit evidence
together. Its Git commit is the durable completion marker; identify that
commit in the next audit or sprint wrap-up. Work shared by multiple PBIs
must be attributed in the audit and included with the first completed
increment that depends on it, without claiming later PBIs are complete.
This local commit rule does not authorize a remote push.

The audit is a pre-commit and pre-advance control, not the canonical Phase 5
documentation wrap-up. A failed or incomplete audit blocks the affected next
step; it does not change a sprint or backlog-item status by itself. In
managed mode, a material design change still requires Product Owner approval
before its code or test skeletons are implemented. Record the approval and
re-run the audit after that change. Do not mark the documentation audit
complete merely because files exist or their headings match.

## P9. Demonstrate each sprint increment at handover

### Purpose

Every sprint ends with a developer-led, live increment demonstration to the
Product Owner before the Product Owner is asked to accept the sprint
documentation or close the sprint. The developer operates the actual product
or opens the actual delivered artifact in front of the Product Owner. A slide
deck, recording, screenshot, test log, or claim that a command ran earlier
does not substitute for this demonstration. This adds a review step to the
existing RUP wrap-up; it does not change the canonical sprint states, PBI
acceptance criteria, or Product Owner decision rights. A demonstration is
required even for a non-code-bearing iteration:
show the actual delivered document, experiment, or decision outcome rather
than pretending that an executable feature exists.

This local practice follows the [Scrum Guide's Sprint Review purpose](https://scrumguides.org/docs/scrumguide/v2020/2020-Scrum-Guide-US.pdf):
inspect the sprint outcome together and determine future adaptations in a
working session.

Demo day should leave the Product Owner confident and satisfied that the
time and money invested produced an understandable, useful result. The
Product Owner should be able to answer: what was promised, what was
delivered, how does it work, what can a user accomplish now, what remains
uncertain, and what should happen next? Earn that confidence through direct
inspection and honest discussion. Record the Product Owner's actual reaction;
the developer cannot declare the Product Owner satisfied on their behalf.

### Prepare the demonstration

The developer owns and presents the handover. Prepare one coherent user
journey tied to the sprint goal and assigned PBIs. Identify local
prerequisites, exact actions, expected visible results, and one relevant
failure or limitation to show. Run a preflight and rehearsal on the intended
environment before inviting the Product Owner. State benefits only when the
demonstration or evidence supports them; do not invent a return on investment.

### Run demo day

1. Set the context in product language: the user problem, sprint goal, and
   specific outcome promised for this sprint.
2. Start with a known product or artifact state and real input. Perform the
   user actions in order. Show intermediate results and the final output so
   the Product Owner can follow the complete path from input to useful
   outcome. For model-backed behavior, use actual model inference when
   claiming model capability; label synthetic or injected data as a contract
   check.
3. Let the Product Owner inspect the result, try a step where practical,
   ask questions, and request a repeat or alternative input. Explain what
   can now be done with the increment and what still requires work.
4. After the journey, show the relevant failure or limitation and the
   supporting test or benchmark evidence. Explain which parts were delivered
   this sprint, what the investment established, and which questions remain
   for later decisions.
5. Discuss feedback and what to change next. In managed mode, ask for the
   Product Owner's explicit handover decision through the existing process.

If the live journey cannot run, record the blocker and arrange a corrected
demonstration. Do not treat slides or earlier test evidence as a completed
live demo.

### Prepare the handover material

#### One presentation pair and its supporting records

Maintain one current presentation pair in `progress/sprint_N/`:
`sprint_N_increment_demo.pptx` and `sprint_N_increment_demo.md`. Their basenames
must match. The Markdown file is the Product Owner's complete end-to-end
walkthrough, including runnable steps and expected results, as well as the
presenter's slide references. It must lead a reader through the increment
without requiring them to assemble instructions from implementation records,
raw logs, screenshots or slide notes. Link this entry point prominently from
the project README, sprint manual and handover record.

Keep the operating reference in `progress/sprint_N/user_manual.md`. State
supported tasks, prerequisites, recovery and known limits, and link to the
presentation walkthrough. A release-ready copy may be promoted to `docs/`
after review, with its scope and links reconciled. Do not create a second
manual in the repository root. Record the demonstration and Product Owner
decision in `progress/sprint_N/sprint_N_handover.md`; place rehearsal logs,
captures, saved outputs and validation receipts in `progress/sprint_N/tests/`.

Use the canonical PPTX path for revisions. Remove superseded working decks
from the user-facing delivery set when authorized; preserve necessary history
in Git and retained evidence. Do not remove a user's open-file lock or session
data. Keep private slide-build intermediates outside the delivery set.

#### The Markdown end-to-end walkthrough

Start with the sprint goal, what the user will accomplish, and the real
starting state. List the supported variations the sprint promised to exercise,
such as languages, backends, input types, optional stages or configuration
profiles. Include their actual paths through the demonstration. For each
numbered stage, provide the action or copyable command, its required inputs,
the expected visible result, how the reader checks it, its relevant requirement
and PBI, and the matching slide or section. Show intermediate outputs as well
as the final result. Include inspection commands or product screens that make
saved output understandable to a person; a UUID or file path alone is
insufficient.

For a CLI product, provide a complete manual sequence in execution order.
Establish the working directory, settings, dependencies, data and result store
before first use. Use staged, verified inputs; do not publish nonexistent
example paths as working commands. When an input needs staging, include the
actual acquisition/preparation steps or a verified linked procedure. State
language, duration and participant characteristics of demo recordings and
retain source URLs and reference provenance in the fixture/evidence record.
Speech clips cannot establish a multi-participant meeting capability. Keep
test-only reference injection in the test documentation; demonstrate product
behavior with the actual inputs and models.

Keep dependent commands in one named shell session, or print complete commands
for another Terminal with actual IDs and paths. Explain prompts, required
operator input and the visible saved change. Do not rely on undefined shell
variables, an unverified personal identity or invented corrections. For a GUI
stage, describe the controls to use, what to listen to or inspect, how to save,
undo or restore, and when an external CLI change requires a refresh or restart.
Show relevant playback, selection and correction controls where delivered.
Label optional steps, the effects of skipping them, and retained neutral or
unknown values. Explain failure/recovery branches and any invalidation of
derived results after a correction or configuration change.

When a guided demo runner is provided, expose one documented entry point with
preflight, live and unattended-rehearsal modes. The live mode must pause for
inspection and genuine operator input; rehearsal must identify skipped human
checks. Match its stages and outputs to the manual sequence and current slide
map. Preflight checks actual data, settings, model/tool dependencies and
required retained evidence. A runner's successful exit records completion of
the walkthrough; report each capability's outcome separately. Failed model
validation may be a demonstrated experiment result, and must remain visible.
Use the project's working language for instructions and status messages;
retain the source language of recordings and transcripts.

For a non-executable iteration, use the same walkthrough structure to open,
inspect and assess the delivered documents, decisions or experiment results.
State which operating steps do not apply and why.

#### PPTX structure and readability

Use a readable, consistent presentation layout with clear titles, adequate
type size and contrast, sufficient spacing, and short text blocks. Add an
agenda near the beginning and titled divider slides between major sections.
Keep the following content in this order, grouping sections proportionately
to the sprint:

1. Sprint goal, user problem, promised outcomes and accepted scope.
2. High-level architecture and processing pipeline, before the walkthrough.
3. The complete user journey, with inputs, actual commands or controls,
   intermediate results and final output.
4. Experiments, material failures, attempted improvements and comparative
   measurements, with their implications and limits.
5. Delivered and unfinished backlog items, conclusions, priorities and the
   Product Owner decision sought. End with conclusions and next decisions.

The deck must allocate enough slides for the user journey to be understood
without narration. An agenda, a single list of steps or a technical parameter
dump does not satisfy that requirement. Show the actual command on a CLI
slide, including how its inputs are obtained; directions such as "enter the
name at stage 4" alone are insufficient. Use real product screens or readable
output to explain the action and result. A slide showing an error must explain
what the user attempted, the effect on saved data, recovery and remaining work.

Architecture slides must identify each component's responsibility, technology
and model, its inputs and outputs, and whether it is optional. Distinguish
model inference, library processing, application logic and operator decisions.
For model-based processing, show prompts or representative interactions,
response validation, bounded repair and final rejection/retention behavior.
Link the complete prompt/interaction ledger in the implementation record.
Show the actual adapter inputs: audio and recognition settings for ASR, and
transcript/task prompts for a text model, including any prompt option genuinely
used by an adapter. Do not invent interactions or imply that syntax validation
proves semantic correctness. Explain grouping/correction rules and
show which parameters users can configure, their defaults, and any remaining
constants or unsupported checks.

Explain before/after examples with actual words, speakers, times and visible
results. Keep internal IDs and hashes in evidence or notes unless they help
the user perform the demonstrated task. Expand technical metric names and
explain what their values mean, their evaluation data and limitations. Follow
`USER_PREFERENCES.md`, including full metric names and narrative Markdown
formatting. Preserve editable charts and their underlying data when revising
slides; verify that presentation edits have not changed the measurements.

#### Explain experimental failure and backlog follow-up

Reserve a complete slide, or several where needed, for each material failed
approach. Explain the intended outcome, observed failure, supporting evidence,
user impact, attempted repair and its measured result. Preserve the earlier
design and failure record so the reader can follow the evolution. Distinguish
observed causes from hypotheses; do not attribute improvement to a model,
prompt or algorithm change when the experiment did not isolate that factor.

Provide decision-ready comparisons in the reports and slides. Include quality,
correctness, coverage, runtime, resource use and other measures relevant to
the sprint's risks. Give the input/model versions, evaluation basis, denominators,
before/after results and limits. Distinguish structural validity, source
coverage, semantic support, speaker accuracy and usable product quality.
Raw logs and saved outputs support these explanations; the Product Owner
must not have to derive the comparison from them. Clearly label historical
controlled results separately from the current live execution.

Enumerate completed assigned PBIs and sprint children, then registered work
still to be done. Give each ID a plain-language outcome, its exact current
status and a link to its definition, including sprint-design definitions for
children. Identify items registered during the sprint, earlier proposals and
already planned later work. Distinguish an unregistered validation direction
from an actual backlog item. Register new work only through the applicable
backlog procedure and Product Owner authority; proposals have no implied
sprint assignment.

Assess completion against each item's accepted criterion. A reproducible
architectural experiment can deliver evidence of a technology's failure;
explain that outcome and the remaining product requirement separately. Do not
silently add production quality to a prototype criterion, weaken a product
criterion, or change board statuses while preparing slides. Any correction
requires the applicable managed-artifact procedure and a recorded explanation
of the previous interpretation, evidence and resulting status. Keep prototype
completion, product readiness, documentation review and handover acceptance
explicit throughout the presentation pair.

### Check quality and record the decision

The developer owns the runnable demonstration and its evidence. The RUP
Documentor owns validation of the handover materials' completeness, usability,
factual accuracy and consistency. Codex may perform both responsibilities;
parallel agents are not required. The Product Owner must be able to reproduce
the journey and understand its outcomes from the delivered documents. Checking
file existence or headings alone does not satisfy this quality gate.

Before the meeting, check every factual claim against the current build,
accepted scope, and sprint evidence. Execute each command
presented as copyable on the stated environment; show actual prerequisites
and expected output, and label paths or commands that require local staging.
Distinguish synthetic or reference-injected contract tests from real-model or
real-user behavior. Perform the manual GUI/listening checks needed for any
claimed user-visible behavior, or expose them as pending. Render every final
slide and inspect readability, clipping, overlap, diagrams and command text;
recheck changed slides and the ending after revisions. Verify the presentation
package and editable chart/data preservation using the applicable presentation
tooling. Record what was actually inspected; structural checks alone do not
prove a live application or audible alignment works.

Recheck local links and new section anchors, slide numbers, current filenames,
and the consistency of the walkthrough, manual, slides, runner, README,
requirements, architecture, accepted design, implementation, tests, benchmark,
backlog, plan and progress board. Label previous snapshots as historical so
their obsolete slide numbers/statuses cannot be mistaken for current guidance.
Apply P8 before each completed handover-material increment is committed:
reconcile documents, run applicable checks, record the audit and commit the
scoped changes together. Reused evidence must name its version, date and
applicability; do not invent a fresh run or repeat inference solely to support
an unchanged factual claim. A changed product behavior still requires its
applicable tests. A local commit does not authorize a remote push.

Record preflight and rehearsal results, live steps performed, observed results,
Product Owner questions, and remaining demonstration limits in
`progress/sprint_N/sprint_N_handover.md`. A broken example, unsupported claim,
missing material limitation, unreadable slide, or live-demo blocker prevents
handover acceptance until corrected. A known product failure may be shown if
its effect and follow-up are made explicit.

In managed mode, inspect the outcome together with the Product Owner and
discuss what should change next. Capture questions, reactions to the user
journey, and feedback in the handover record, then request an explicit
review decision. The Product Owner may accept the handover, request
corrections, or direct new scope through the existing backlog and sprint
procedures. Do not infer acceptance from silence or from passing automated
tests. Continue the canonical Phase 5 documentation approval and sprint
status procedure only after the demonstration decision is recorded; this
patch does not itself mark a sprint complete or authorize a remote push.

## P10. Use proportionate external review rounds

External review supplements the iteration's own validation with another expert perspective, human or AI. Use it when the Product Owner requests it or agrees it will help resolve an important uncertainty. It is not a mandatory gate for every change. A favorable review is not execution evidence and does not mean the sprint is automatically accepted.

### P10.1 Round artifacts

Keep each round under the current sprint's evidence directory, using the sprint's stable phase ID and a round number:

- `sprint_<ID>_review-<N>.md`: the external expert's original review.
- `sprint_<ID>_review-<N>-response.md`: the engineering response to its findings.
- `sprint_<ID>_review-<N>-feedback.md`: the expert's reaction to that response, if supplied.
- `sprint_<ID>_review-<N>-decisions.md`: the selected actions, rationale and deferred issues, once decisions are actually made.

For example, use `sprint_E.1_review-1-response.md`. Keep the review, response and feedback for one exchange under the same number, and increment it for the next review pass. Create only the artifacts the exchange needs, never empty placeholders. Do not rename completed historical rounds just to apply this convention.

### P10.2 Round header

Every round artifact starts with a short header:

- **Round:** `<ID>` review `<N>`, and the artifact type (review, response, feedback or decisions).
- **Revision:** the full commit SHA reviewed or answered, and whether it matches the maintained local baseline.
- **Reviewer:** human or agent, with its role, and the model or tool where relevant.
- **Scope:** what was read, what was executed, and what was explicitly not read or run.
- **Inputs:** links to the prior round artifacts this one depends on.
- **Status table:** one line per finding ID with its current status (see P10.4), placed before any detail.

A reader should be able to tell what a round covers, and where every finding stands, from the header alone.

### P10.3 Finding identity

Every finding gets a stable ID: `R<N>-<severity><k>`, where severity is `H` (high), `M` (medium) or `L` (low). For example, `R1-H1`, `R1-M5` or `R2-L1`.

- If the expert's text uses another numbering scheme, the response maps it once to stable IDs and never renumbers afterwards.
- Later rounds, decisions, backlog items and commit messages refer to the same ID, for example `fix(R1-M1): use EXIT FAILURE in infrastructure wrappers`.
- A finding the response splits keeps its ID with a suffix (`R1-M5a`, `R1-M5b`). A finding raised again in a later round keeps its original ID rather than getting a new one.

### P10.4 Finding status

Use one status per finding, recorded in the status table of each artifact that changes it:

| Status | Meaning | Set by |
|---|---|---|
| `open` | Raised, not yet answered | review |
| `agreed` / `partly-agreed` / `disputed` | Engineering position, with evidence | response |
| `selected` / `deferred` / `rejected` | Product Owner decision | decisions |
| `fixed@<sha>` | Correction committed, acceptance not yet shown | implementation increment (P8) |
| `verified@<sha>` | Acceptance evidence recorded | validation, or a later review round |
| `regressed@<sha>` | Previously verified, now failing | a later review round |

`fixed` is never inferred from a commit message alone, and `verified` requires the acceptance evidence named in the decision. An expert's approval of a response does not change a status by itself.

### P10.5 Review content

Ask the reviewer, in each finding, to give the severity, the location (file and line where possible), the impact, a proposed fix, and an acceptance test that would show the fix works. The review states what it did not read or execute. It should not claim behavior it has not seen in source or evidence.

A follow-up round (`N > 1`) first re-checks every finding from earlier rounds that is not yet `verified` or `rejected`, against the new revision, with evidence. Only then does it add new findings. It does not reopen a `rejected` finding unless it brings new evidence.

### P10.6 Response content

Preserve external review and feedback exactly as supplied. The response:

- identifies the reviewed revision and the limits of the review;
- checks each claim against the actual code, requirements and evidence, and says whether it agrees, partly agrees or disagrees;
- corrects factual errors in the review explicitly, rather than silently;
- distinguishes reproduced defects from plausible but untested risks, and records any read-only experiments under "Checks performed";
- gives proportionate correction and verification proposals, each with acceptance criteria;
- links supporting sources, both project files and authoritative external documentation.

Add navigation from the response and from the current maintained sprint summary. Keep the source text intact rather than inserting our conclusions into the expert's report.

Prioritize findings against the accepted vision, the selected use cases, the lifecycle phase and the architectural risks. During Elaboration, address defects that invalidate the chosen demonstration, its evidence, its reproducibility or the safe experiment boundaries. Production hardening and unrelated enhancements may be deferred explicitly. A long review must not silently expand the prototype into a general platform or make perfection the acceptance threshold.

### P10.7 Decisions

When the Product Owner selects the response, record the useful decisions: what will be corrected now, why, what evidence will establish it, and what is deferred and until when. Each decision line names its finding ID, its decision status, its closing condition and its owner.

Use the existing backlog and sprint procedures for any change to scope, assignments or statuses. A response is a proposal until selected, and a decision is not a completed fix. Link selected work to existing backlog items where it belongs, and create new backlog items only through their normal procedure when needed.

### P10.8 Closing a round

A round is closed when every one of its findings is `verified`, `deferred` with a recorded reason, or `rejected`. Record the closure in the maintained sprint summary. Open a new round when:

- the Product Owner requests it;
- selected corrections are ready for independent re-checking; or
- a material change has altered the reviewed boundary.

Rounds do not continue merely because the expert keeps finding lower-severity items. Stop when the remaining findings are outside the phase's purpose and have been deferred explicitly.

### P10.9 Agent prompts

When an agent takes a role in a round, its prompt states the role, the round, the full revision SHA, the inputs, the allowed actions, and the output path. Start from these templates and adapt them to the round.

**Reviewer**

    Role: external reviewer for <repo>, sprint <ID>, review round <N>.
    Revision: <full SHA>. Read-only: no clone, execution or push unless stated here.
    Read: <files/dirs>. Prior rounds: <links, or none>.
    Task:
    1. (N>1) Re-check every finding not yet verified or rejected; set its status
       (verified / still open / regressed) with file:line evidence.
    2. Add new findings as R<N>-H/M/L<k>: severity, file:line, impact,
       proposed fix, acceptance test.
    3. List what you did not read or run.
    Rules: cite only what you read; mark untested risks as untested; do not
    reopen rejected findings without new evidence; judge against <phase> goals,
    not production completeness.
    Output: progress/<ID>/sprint_<ID>_review-<N>.md, header and status table first.

**Responder (engineering)**

    Role: engineering responder for <repo>, sprint <ID>, round <N>.
    Input: sprint_<ID>_review-<N>.md at revision <full SHA>; sprint design and assessment.
    Task: per finding ID, answer agree / partly agree / disagree, with source
    evidence or a read-only experiment; correct factual errors explicitly;
    propose a proportionate correction and an acceptance test.
    Rules: do not implement fixes, change backlog or sprint status, rewrite
    deployed migrations or archives, send material or push; mark anything
    untested as untested.
    Output: progress/<ID>/sprint_<ID>_review-<N>-response.md, header and status
    table first, ending with "Checks performed".

**Feedback (reviewer reacting to the response)**

    Role: the round-<N> reviewer, reacting to the engineering response.
    Input: review-<N>.md and review-<N>-response.md.
    Task: per finding ID, accept the response, accept it with a change, or
    dispute it with evidence; state the closing condition for each.
    Rules: no new findings here; record them for round N+1.
    Output: progress/<ID>/sprint_<ID>_review-<N>-feedback.md.

### P10.10 Boundaries

Apply P8 to each resulting implementation or documentation increment, and P9 to the sprint handover. Do not close a sprint, grant acceptance or claim a fix solely because an expert approves the response. Review artifacts do not authorize sending material to another person or service, or pushing a repository; those actions keep their existing authorization rules.
