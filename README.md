# Oracle APEX CI/CD Laboratory

**From Git to APEX: traceable releases, safe upgrades and protected deployments.**

An executable delivery example for Oracle APEX and Oracle Database. A small Foundation/Hello/World application makes the important operations visible: capture source, review it in Git, build one release, validate it in integration testing, promote the same artifact to UAT and preserve application data through an upgrade.

The prototype runs on one Podman host using supported Oracle automation interfaces and small Bash/Python scripts. The source is public at [rstyczynski/APEX_CICD](https://github.com/rstyczynski/APEX_CICD). Hosted CI automation and production operation remain future work.

## What works today

The assisted A–H walkthrough and native review-correction experiments demonstrate:

1. **Separate infrastructure and project setup.** Provision Oracle Database/APEX/ORDS first, then delivery control and individually assigned project schemas/workspaces. Check target identity and logical isolation.
2. **Foundation-first assembly.** A, B and C have private areas. Reviewed source snapshots build Foundation, Foundation/Hello and the complete application respectively. Incomplete checkpoints remain unavailable.
3. **Delivery of the same release artifact.** Build an immutable archive from reviewed Git source, validate it in **integration_test**, then promote those identical bytes to **user_acceptance_test**. Receipts bind the source revision, archive hash and target state.
4. **A compatible Hello patch.** Advance Hello from **1.0.0 to 1.0.1** while Foundation and World remain **1.0.0**. Integration testing checks fresh installation and upgrade from the initial release. The UAT preservation check confirms all fields of **21 baseline greeting-history rows**, earlier entries and complete configuration remain unchanged.
5. **Rejection of a known incompatible upgrade.** A Foundation **2.0.0** proposal conflicts with Hello/World dependencies and stops before maintenance, migration or application import.
6. **Detection and inspection of live drift.** A real Page Designer edit changes the live fingerprint without changing the component version. Deployment stops; the operator can compare published/live source before choosing restoration or Git reconciliation.

7. **One bounded forward repair.** In integration_test, fail after an additive index commits, retain the failed attempt and block ordinary access. Reject a changed partial observation, then apply a separate repair archive, preserve the 21-row baseline/settings and repeat unchanged without writes. See [chapter I](progress/E.1/cicd-walkthrough.md#i-inspect-and-repair-one-failed-additive-deployment).

These are demonstrated prototype outcomes, not a declaration that the complete sprint acceptance scope or full test suite has passed. See the [handover](progress/E.1/sprint_E.1_handover.md), [test evidence](progress/E.1/sprint_E.1_tests.md) and [completion assessment](progress/E.1/sprint_E.1_assessment.md).

## Explore the delivery story

- **[From Git to APEX — presentation](progress/E.1/sprint_E.1_increment_demo.pptx):** 29 slides covering architecture, Oracle interfaces, Git layout/cooperation, the A–I results and future CI pipelines. Includes editable diagrams adapted from the [draw.io model](progress/E.1/model.drawio).
- **[Presentation walkthrough](progress/E.1/sprint_E.1_increment_demo.md):** slide-linked review, commands, visible results and decisions.
- **[A–I use-case walkthrough](progress/E.1/cicd-walkthrough.md):** the main guided operating journey, with a separate script for each stage.
- **[Operator manual](progress/E.1/user_manual.md):** application inventory, endpoints, accounts and detailed operations.
- **[Repository and pipeline guide](progress/E.1/repo_layout.md):** shared source, private areas, merge guidance and proposed CI automation. This remains an Elaboration draft for [PBI-017](BACKLOG.md#pbi-017-deliver-a-repository-and-pipeline-reference-guide).

## Oracle interfaces and toolchain

1. **APEX / ORDS:** App Builder authors application definitions; ORDS serves the HTTP runtime.
2. **SQLcl with Java:** native `apex export` captures split SQL source for Git. Deployment maps the target through `APEX_APPLICATION_INSTALL` and executes the exported `install.sql`.
3. **SQLcl's bundled Liquibase:** applies separate, ordered database migrations. An application export does not contain the runtime greeting data or replace schema migration management.
4. **APEX export fingerprint:** `APEX_EXPORT.GET_APPLICATION` with `CHECKSUM-SH256` compares live application definitions with the successful deployment receipt.
5. **Git, SHA-256 and E1_CTRL:** identify accepted source/package bytes and manage reservations, deployment epochs and receipts.
6. **Bash/Python and Podman:** expose operator steps, run focused checks and host the lab.

Git is the integration authority. APEX Working Copies and Team Development are not used for release integration or promotion in this prototype. Split exports are text and can be diffed/merged by Git; shared files, IDs and dependencies still need review, followed by complete-candidate import and testing. See the [merge guidance](progress/E.1/repo_layout.md#merging-apex-export-files).

## Repository layout and environments

One repository contains all three components:

- [apex/f810001/](apex/f810001/): complete canonical split APEX application export, mapped to each target on import.
- [db/changes/](db/changes/) and [changelog](db/changelog.xml): versioned database migrations.
- [release/](release/): component versions, dependencies, supported starts and release proposals.
- [deploy/](deploy/): control definitions, guards, verification, import and publication SQL.
- [config/areas.json](config/areas.json): schema/workspace/application mappings.
- [scripts/](scripts/) and [tests/](tests/): operator entry points and executable checks.
- [docs/](docs/) and [progress/E.1/](progress/E.1/): requirements, architecture, procedures and current evidence.

A/B/C use **E1_DEV_A/B/C**, applications **810001/810002/810003**. The disposable integration area is **E1_INTEGRATION / 810004**; retained UAT is **E1_UAT / 810005**. These are private logical areas in one Oracle installation, not separate component repositories or isolated database servers. Hello and World both depend on Foundation.

Current A–C scripts replay reviewed sequential Git snapshots. Independent task branches, genuine parallel Hello/World integration and hosted PR/CI execution are proposed extensions, not demonstrated by that replay. Ignored `.local-apex/` contains local tools, credentials, staging, release archives and host evidence; credentials and runtime business data stay outside Git.

## Run the walkthrough

Clone with the delivery-method submodule:

```bash
git clone --recurse-submodules https://github.com/rstyczynski/APEX_CICD.git
```

The infrastructure provisioning path currently supports **macOS Apple Silicon**. Pure source/Python checks are separate from that host requirement. Open a Bash terminal inside the full checkout, position at its Git root, reconstruct reviewed release inputs and run local preflight:

```bash
cd "$(git rev-parse --show-toplevel)"
python3 scripts/cicd-release-inputs.py
bash scripts/cicd-walkthrough.sh --preflight
```

Then follow the [preparation chapters](progress/E.1/cicd-walkthrough.md#prerequisites-and-infrastructure-precheck) in order:

1. Check prerequisites and prepare the Podman host.
2. Choose whether to destroy an existing disposable lab. **Complete cleanup removes all lab applications and history, including UAT.** It preserves host credentials/tools, retained archives/evidence and unrelated Podman resources.
3. Install vanilla Database/APEX/ORDS using the [infrastructure procedure](docs/deploy.md#fresh-walkthrough-infrastructure-sequence).
4. Initialize project control, provision each area and configure its assigned developer.
5. Check readiness; run A–I using each chapter's script and browser instructions.

Preflight alone does not provision the lab or prove database readiness. Normal upgrades preserve UAT data; destruction is a separate explicit lifecycle operation. Scripts and their walkthrough chapters are maintained together as one operating artifact.

## Remaining validation

The [external review](progress/E.1/sprint_E.1_review-1.md) and [engineering response](progress/E.1/sprint_E.1_review-1-response.md) identified missing release inputs as an independent-reproduction blocker. The [BUG-2 correction](progress/E.1/cicd-walkthrough.md#prepare-reviewed-release-inputs) now reconstructs the exact historical archives from versioned recipes and pinned Git source. The [independent clean-checkout A–I rehearsal](progress/E.1/tests/clean_checkout_20261018.txt) now passes on newly provisioned infrastructure with new credentials and no copied release archives. It uses explicit runtime API fixtures; browser acceptance remains the separate assisted walkthrough.

Sprint **E.1 remains active**. Important unfinished proofs are synchronized competing reservations, genuine parallel component integration, complete maintenance/request/verifier fencing, scoped schema-definition drift and broader recovery/concurrency coverage beyond the single integration-only failed-DDL/forward-repair proof. A verification retry or restored drift fixture is not that repair proof.

The [assessment](progress/E.1/sprint_E.1_assessment.md) recommends focused further Elaboration before full Lifecycle Architecture acceptance. Remote CI runners, protected-branch automation and release approvals are [future extensions](progress/E.1/repo_layout.md#future-pipeline-automation). Cloud deployment, production readiness and high availability are outside the demonstrated scope.

Known open work is registered as **Proposed, unscheduled PBI-018–035** in the [Product Backlog](BACKLOG.md#pbi-018-prove-atomic-task-reservations-under-contention). The [coverage map](progress/E.1/sprint_E.1_assessment.md#open-work-backlog-coverage) connects each proposal to current E.1 criteria or deferred review concerns. PBI-012–017 retain their existing assessment, planning and reference-guide outcomes.

## Vision

The Product Owner accepted the vision on 2026-10-16: help Oracle APEX developers and DevOps engineers choose and reproduce a practical CI/CD approach, explain its tradeoffs and validate it with a small application. The product is an evidenced delivery example and its operating guidance. Foundation/Hello/World provides configurable greeting entries and persistent history so the workflow exercises application definitions, database objects and retained data.

See the [SRS](docs/srs.md), [candidate architecture](docs/architecture.md), [test profile](docs/test-profile.md) and [roadmap](ROADMAP.md) for the wider contract.

## External references

The supplied [Oracle APEX lifecycle reference](refs/apex-lifecycle-management-v3.pdf) remains external research input.

## Method

[RUPStrikesBack](https://github.com/rstyczynski/RUPStrikesBack) is an iterative delivery method for collaboration between a Product Owner and AI agents. It combines RUP lifecycle phases with a prioritized backlog, bounded iterations, explicit requirements/design, executable validation and Product Owner review. Each increment connects its implementation, tests and documentation so decisions can be checked against evidence.

This project includes the method as a [Git submodule](RUPStrikesBack/) and applies [project-specific policy](RUP_patch.md). [AGENTS.md](AGENTS.md) defines the agent entry points. [BACKLOG](BACKLOG.md), [PLAN](PLAN.md) and [PROGRESS_BOARD](PROGRESS_BOARD.md) track priorities, sprint selection and execution respectively. Sprint 0 and I.1 are closed; E.1 is the active Elaboration sprint, focused on proving the delivery architecture before broader construction.

For external expert review, use the [rup-external-review skill](.agents/skills/rup-external-review/SKILL.md). Codex prepares the prompts and engineering replies; the Product Owner relays them to the expert through the linked round files. Review outcomes and implementation evidence remain distinct from sprint acceptance.
