# Oracle APEX CI/CD Laboratory

## Vision

Accepted by the Product Owner on 2026-10-16.

Help Oracle APEX developers and DevOps engineers choose and reproduce a practical approach to continuous integration and continuous delivery. Research the available automation options, explain their tradeoffs against established DevOps practices, and validate the selected approach with a small local application. The main product is an evidenced, reusable delivery example and its operating guidance.

The laboratory should make changes to database objects, APEX application definitions, and application configuration understandable in version control, reviewable before release, and repeatable when deployed. It should demonstrate automated checks, traceable release artifacts, controlled promotion between logically separate development and test targets, and a documented response to failed changes. The exact automation tools and environment topology remain decisions for research and validation.

## Reference application

Use a deliberately simple Hello World application with persistent greeting history. A Hello component has its own data and configuration pages; a World component has its own data and configuration pages. Together they provide the greeting recorded in the history. The example should support a visible change to either component and a database change so that the delivery workflow exercises more than a static page deployment.

One APEX application with separate Hello, World, and history areas is the initial proposal. Here, a component means a bounded functional area; it does not yet imply a separate APEX application, schema, service, or independently deployable package. Research may propose a different shape when it demonstrates useful CI/CD cases more clearly without adding unnecessary application complexity. Exact data fields, configuration semantics, and deployment boundaries will be defined in the requirements and candidate architecture.

## Research and demonstration outcomes

Compare credible approaches for capturing APEX and database changes, reviewing them in Git, packaging releases, and deploying them through automated checks. Assess configuration and secret handling, environment separation, dependencies between components and schema changes, and recovery or forward repair after a failed deployment. Explain what the evidence supports and where each approach has limits; do not treat “industry standard” as a single prescribed toolchain.

A successful demonstration takes a reviewed source change through the selected pipeline into a local target, shows the changed behavior and retained greeting history, and identifies the source revision and release artifact responsible. It also shows an intentionally failing check or deployment and the agreed recovery procedure. A second operator should be able to reproduce the documented path with the stated prerequisites. Detailed acceptance criteria and executable quality gates will be agreed before implementation.

## Local environment and constraints

Model the workflow on a local Oracle APEX service, preferably using Podman. E.1 maintains the [infrastructure lifecycle procedure](docs/deploy.md), building on the initial assessment. Elaboration takes this procedure and supporting scripts to create, verify and destroy the experiment infrastructure as needed; the project does not depend on a particular VM remaining present. The assessed versions and preliminary verification evidence are recorded with the procedure. Preserve retained data, configuration, credentials and unrelated Podman resources during lifecycle work.

Keep the application small and use synthetic greeting data. Keep secrets outside version control, identify exact tool and runtime versions, and state local resource requirements. Cloud deployment, production operations, high availability, and a feature-rich business application are outside the initial demonstration scope. The CI service, migration tool, packaging strategy, and physical separation of targets remain open choices.

## Delivery method and current state

The project uses [RUP Strikes Back](AGENTS.md) with the [local policy](RUP_patch.md). Sprint 0 is complete: PBI-001 delivered the accepted vision and PBI-002 delivered the accepted [roadmap](ROADMAP.md) and next-sprint plan. The [plan](PLAN.md) records I.1 (formerly Sprint 1) as closed in managed mode. The Product Owner accepted its revised analysis baseline with the presentation wording correction on 2026-10-16. The Product Owner subsequently accepted all I.1 material and explicitly closed the sprint. E.1 is now active under that authorization. The [Product Owner handover](progress/I.1/sprint_I.1_handover.md) summarizes the concept, six demonstration scenarios and proposed Elaboration scope. Its [presentation walkthrough](progress/I.1/sprint_I.1_increment_demo.md) links the PowerPoint companion. The [final engineering review decisions](progress/I.1/analysis_review-answers_2.md) link the reconciled contracts and remaining Elaboration proof. The [backlog](BACKLOG.md) defines its assigned outcomes.

### Sprint 0 — Vision and initial plan

The Product Owner accepted the vision and roadmap and requested closure on 2026-10-16. Preliminary deployment work and external references are recorded for potential reuse. See the [handover and new-session prompt](progress/sprint_0/sprint_0_handover.md) and [document walkthrough](progress/sprint_0/sprint_0_increment_demo.md). No application code or runtime validation was delivered in Sprint 0. The [test profile](docs/test-profile.md) contains accepted future E.1 command contracts; none has been executed as an application test.

### Sprint E.1 — Validate the local APEX delivery path

E.1 is active in managed mode. Its [setup](progress/E.1/sprint_E.1_setup.md) and [design](progress/E.1/sprint_E.1_design.md) define the bounded prototype and selected construction scope. The [construction document](progress/E.1/sprint_E.1_implementation.md) tracks the working platform, private areas, Foundation and pending application/release work. The approved slice covers the happy path, compatible versioned patch, incompatible Foundation-upgrade rejection and live-drift rejection. E.1 owns the infrastructure lifecycle procedure and may recreate the current scoped Podman environment as experiments require.

Use the [E.1 operator guide](progress/E.1/user_manual.md) for the current application/workspace inventory, endpoints, logins, local password retrieval, atomic SQL checks and pipeline stage-by-stage status. Run bash scripts/cicd-walkthrough.sh for chapter-linked, keypress-guided execution of the implemented operator stages. The manual and script are maintained as one artifact. The [developer outcome walkthrough](progress/E.1/developer_walkthrough.md) groups A/B/C delivery stages with Product Owner URL checkpoints; its current runner inspects Foundation and stops before pending Hello construction.

## External references

The supplied [Oracle APEX application lifecycle reference](refs/apex-lifecycle-management-v3.pdf) is retained unchanged in `refs/`. It is external research input; recommendations will be checked against the selected local tool versions and experimental evidence.
