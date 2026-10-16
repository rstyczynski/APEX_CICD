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

Model the workflow on a local Oracle APEX service, preferably using Podman. The Product Owner recognizes the existing environment setup, [local deployment runbook](docs/deploy.md), lifecycle scripts in `scripts/`, and recorded access/restart checks as completed preliminary work available for potential reuse. Assess its suitability for the selected CI/CD approach and verify the current runtime when needed. Preserve existing data, configuration, credentials, and unrelated Podman resources during that assessment.

Keep the application small and use synthetic greeting data. Keep secrets outside version control, identify exact tool and runtime versions, and state local resource requirements. Cloud deployment, production operations, high availability, and a feature-rich business application are outside the initial demonstration scope. The CI service, migration tool, packaging strategy, and physical separation of targets remain open choices.

## Delivery method and current state

The project uses [RUP Strikes Back](AGENTS.md) with the [local policy](RUP_patch.md). Sprint 0 is running in managed mode for PBI-001 (accepted vision) and PBI-002 (initial plan). The [roadmap](ROADMAP.md) proposes the delivery sequence from this vision; its next-sprint proposal awaits Product Owner review. The [backlog](BACKLOG.md) retains the bootstrap definitions, and the [plan](PLAN.md) records completed preliminary work alongside the current sprint entries.

The [Sprint 0 setup](progress/sprint_0/sprint_0_setup.md) records scope, review criteria, existing assets, and outstanding decisions. No application implementation or runtime validation is claimed by this document. The [test profile](docs/test-profile.md) remains pending candidate architecture.

## External references

The supplied [Oracle APEX application lifecycle reference](refs/apex-lifecycle-management-v3.pdf) is retained unchanged in `refs/`. It is external research input; recommendations will be checked against the selected local tool versions and experimental evidence.
