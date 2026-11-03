# Oracle APEX CI/CD Laboratory

**From Git to APEX: traceable releases, safe upgrades and protected deployments.**

Our guiding principle: **Give developers flexibility through stable, industry-standard tools and techniques.**
E.2 evaluates optional tool compatibility against this aim in its
[analysis review](progress/E.2/sprint_E.2_inception.md#optional-tool-compatibility-hypotheses).

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

Sprint **E.1 was closed by the Product Owner on 2026-10-18**. Important unfinished proofs are synchronized competing reservations, genuine parallel component integration, complete maintenance/request/verifier fencing, scoped schema-definition drift and broader recovery/concurrency coverage beyond the single integration-only failed-DDL/forward-repair proof. A verification retry or restored drift fixture is not that repair proof.

The [assessment](progress/E.1/sprint_E.1_assessment.md) recommends focused further Elaboration before full Lifecycle Architecture acceptance. Remote CI runners, protected-branch automation and release approvals are [future extensions](progress/E.1/repo_layout.md#future-pipeline-automation). Cloud deployment, production readiness and high availability are outside the demonstrated scope.

Known follow-up work is registered in the [Product Backlog](BACKLOG.md#pbi-018-prove-atomic-task-reservations-under-contention). The historical [E.1 coverage map](progress/E.1/sprint_E.1_assessment.md#open-work-backlog-coverage) connects PBI-018–035 to remaining criteria and deferred review concerns. On 2026-11-03 the Product Owner narrowed **E.3 to a simple Git-based
pipeline architecture prototype**. The [E.3 preparation](progress/E.3/sprint_E.3_pipeline_scope.md)
plans one Working Copy change captured in Git, a manually opened PR, a
label/title classification feeding Release Please version and changelog
automation, and a separately triggered release workflow where the deployer
selects the version tag. A reviewed release PR commits CHANGELOG.md and version
metadata before the workflow creates the tag and matching GitHub Release notes. Analysis/design will consider selective
future release automation. The former 15 full-solution assignments return to
the backlog for Construction or risk-driven later Elaboration; PBI-053 owns
this bounded prototype. E.4's five assignments remain pending scope refinement
against E.3 evidence before activation. The [plan](PLAN.md) owns assignments
and status. Earlier native-team/Git-team split records remain planning history;
their full qualification and comparison gates are not E.3 prototype criteria.

### Sprint E.2 — Oracle lifecycle assessment

**Closed and accepted on 2026-11-03.** PBI-051 delivered the source-backed gap
analysis, focused native delivery/Working Copy exercises, runnable walkthrough
and Product Owner decision package. The [final assessment](progress/E.2/sprint_E.2_assessment.md)
and [accepted handover](progress/E.2/sprint_E.2_handover.md) record the closure.

Use the [gap analysis](progress/E.2/oracle-gap-analysis.md),
[native SQLcl walkthrough](progress/E.2/cicd-walkthrough.md) and
[decision presentation](progress/E.2/sprint_E.2_product_owner_handover.pptx).
The presentation is the 22 October review snapshot; the handover records the
subsequent acceptance and current follow-up decisions. The earlier increment
deck remains historical exercise material.

SQLcl PROJECT, Working Copies and Git can coexist. Component dependency and
automatic drift-protection gaps remain; reviewed forward repair is supported
but unexercised in E.2. Retained F artifacts still have their verification limit,
and a separate clean 25.4.1 comparison does not certify them. Identity and
protection qualification remain backlog work. E.1 evidence is unchanged.
[PBI-052](BACKLOG.md#pbi-052-define-semantic-versioning-rules-for-component-contracts)
retains component-contract/SemVer follow-up. Complex Foundation upgrades stay E.5.

### Sprint E.3 — Git pipeline architecture prototype

E.3 inherits E.2 native APEX/SQLcl capabilities, uses GitHub Actions as controller
and removes every E.3 Python helper and recurring source adapter. It implemented
the Working Copy/Git happy path and deployed selected tag
[v1.0.3](https://github.com/rstyczynski/APEX_CICD_E3/releases/tag/v1.0.3)
through a manually dispatched workflow in the private
[application repository](https://github.com/rstyczynski/APEX_CICD_E3).
PR labels and matching Conventional Commit squash titles feed Release Please's
version/changelog release PR. Both CHANGELOG.md and GitHub Release notes are
generated; neither PR merges nor tag publication deploys to the lab.

Start the [end-to-end walkthrough](progress/E.3/sprint_E.3_increment_demo.md),
[editable presentation](progress/E.3/sprint_E.3_increment_demo.pptx) and
[operator manual](progress/E.3/user_manual.md). The
[handover](progress/E.3/sprint_E.3_handover.md),
[implementation](progress/E.3/sprint_E.3_implementation.md) and
[test evidence](progress/E.3/sprint_E.3_tests.md) state actual results and limits.
Native source/distribution verification, hosted checks, the selected-tag run,
retained business fields, browser behavior and missing-changeset rejection passed.
The first remote run failed before deployment and its workflow correction is
retained. The release/tag is 1.0.3 while APEX's display footer remains 1.0.0;
automatic display-version stamping was not qualified.

PBI-053 and its three children are tested. E.3 remains Progress pending separate
Product Owner acceptance/closure; E.4/E.5 remain Planned. This is an architecture
prototype, with concurrency, full identity preservation, drift/fencing and
broader recovery still registered for later work.

The [native correction record](progress/E.3/sprint_E.3_native_correction.md)
links the final workflow, source, archive and fresh gates. It preserves the
intermediate 1.0.2 browser failure and the native APEX_SESSION check added before
publication.

## Vision

The Product Owner accepted the vision on 2026-10-16: help Oracle APEX developers and DevOps engineers choose and reproduce a practical CI/CD approach, explain its tradeoffs and validate it with a small application. The product is an evidenced delivery example and its operating guidance. Foundation/Hello/World provides configurable greeting entries and persistent history so the workflow exercises application definitions, database objects and retained data.

See the [SRS](docs/srs.md), [candidate architecture](docs/architecture.md), [test profile](docs/test-profile.md) and [roadmap](ROADMAP.md) for the wider contract.

## External references

The supplied [Oracle APEX lifecycle reference](refs/apex-lifecycle-management-v3.pdf) remains external research input.

## Method

[RUPStrikesBack](https://github.com/rstyczynski/RUPStrikesBack) is an iterative delivery method for collaboration between a Product Owner and AI agents. It combines RUP lifecycle phases with a prioritized backlog, bounded iterations, explicit requirements/design, executable validation and Product Owner review. Each increment connects its implementation, tests and documentation so decisions can be checked against evidence.

This project includes the method as a [Git submodule](RUPStrikesBack/) and applies [project-specific policy](RUP_patch.md). [AGENTS.md](AGENTS.md) defines the agent entry points. [BACKLOG](BACKLOG.md), [PLAN](PLAN.md) and [PROGRESS_BOARD](PROGRESS_BOARD.md) track priorities, sprint selection and execution respectively. Sprint 0, I.1, E.1 and E.2 are closed; E.3 has a tested prototype and technical handover; E.4/E.5 remain Planned with distinct assigned Elaboration work recorded in the backlog and plan.

For external expert review, use the [rup-external-review skill](.agents/skills/rup-external-review/SKILL.md). Codex prepares the prompts and engineering replies; the Product Owner relays them to the expert through the linked round files. Review outcomes and implementation evidence remain distinct from sprint acceptance.
