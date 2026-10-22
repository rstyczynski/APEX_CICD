# E.2 — Oracle lifecycle gap analysis

**Recommendation:** use SQLcl PROJECT, APEX Working Copies and Git together.
Retain supplementary controls only where native capabilities do not meet the
requirement. Adoption still requires toolchain and protection qualification.

**Give developers flexibility through stable, industry-standard tools and techniques.**

## What works

| Capability | Finding | Evidence |
|---|---|---|
| PROJECT capture, staging and packaging | Captures APEX/database source and generates a deployable Liquibase distribution. | [Capture receipt](tests/project-component-capture-validation.json) |
| Initial delivery and compatible Hello upgrade | Fresh installation, populated upgrade and repeat succeeded in integration. The same artifact can be promoted with target mappings. | [Initial delivery](tests/project-integration-mapped-validation.json), [upgrade](tests/project-f2-upgrade-validation.json) |
| Working Copies → Main → Git | Selective refresh/merge and capture of agreed Main changes work. Team checkpoints belong to this flow. Private copies need not become release sources. | [Working Copy receipt](tests/project-f1-working-copy-validation.json) |
| Native runtime access controls | Restricted verifier access and publication replace the exercised E1_CTRL runtime access gate. They do not replace its other responsibilities. | [Mapped deployment receipt](tests/project-integration-mapped-validation.json) |
| Shared-instance targets | Workspace, schema and application mappings work through the documented installer/defaults-file hook. Separate-instance qualification remains open. | [Mapped deployment receipt](tests/project-integration-mapped-validation.json) |

The Product Owner reported F completed, including UAT upgrade. Retained preparation
receipts describe their own earlier integration runs; they are not a transcript
of that operator execution.

Oracle basis: [lifecycle paper](../../refs/apex-lifecycle-management-v3.pdf),
[SQLcl 25.3 PROJECT](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/project.html),
[APEX 24.2 Working Copies](https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/about-working-copies.html).

## G, H and I — native support gaps

“Not supported” below refers to the specified automatic capability in the
evaluated APEX/SQLcl PROJECT workflow.

| Scenario | Native support | Consequence |
|---|---|---|
| **G: component version dependency protection** | **Not supported.** Clean PROJECT verification accepted both allowed and conflicting component declarations. | Keep explicit component contracts and supplementary compatibility admission. [Evidence](tests/project-verify-fix-validation.json) |
| **H: automatic live-drift deployment protection** | **Not supported by the evaluated delivery path.** No qualified automatic comparison/rejection gate was supplied. | Require application/schema/code comparison against the accepted target baseline before deployment. The zero-change replay did not test overwrite protection. [Evidence and limits](h-live-drift-evidence.md) |
| **I: automatic failed-deployment repair** | **Not supported.** PROJECT does not design the repair. | Inspect partial state and supply a reviewed forward repair. SQLcl/Liquibase can deliver that repair, but E.2 did not exercise the E.1-equivalent recovery scenario. |

APEX subscriptions provide shared-component reuse and propagation, not our
component SemVer admission. [Oracle APEX 24.2 subscriptions](https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/using-shared-component-subscriptions.html).
Reviewed repair uses changeset execution/history, not automatic repair.
[Oracle Liquibase update](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.2/sqcug/update.html).

## Blockers and corrections

- **Release qualification:** SQLcl 25.3 verification failed on the retained F
  distribution. A clean 25.4.1 comparison passed, but does not certify the old
  artifacts. Select a pinned client and regenerate/verify a consistent release.
  [Correction receipt](tests/project-verify-fix-validation.json).
- **Packaging:** post-stage APEX edits create source/distribution inconsistency.
  Express release configuration before capture or through qualified deployment hooks.
- **Identity:** mapped replacement changed APEX region IDs in the earlier fixture.
  Qualify required identity and saved-report preservation before adoption.
  [Detailed observations](oracle-gap-analysis-detail.md).
- **Recovery:** reviewed partial-failure repair remains missing E.2 validation;
  this is an implementation gap, not proof that Oracle cannot deliver repairs.

No evidence establishes general incompatibility between PROJECT, Working Copies
and Git. Repository coexistence is feasible; source layout and migration ownership
must be explicit. Use one migration authority per target delivery stream.

## Policies and unnecessary custom mechanisms

- Reevaluate E.1's break-glass authoring and component-wide reservations. They are
  project policies; they do not prohibit native Working Copy authoring.
- Prefer native capture, staging, packaging, mappings and access controls.
  Do not rebuild these inside another custom controller.
- E1_CTRL is not wholly redundant: qualification/provenance, ownership, drift
  admission and repair governance need separate decisions.
- Define component contracts and major/minor/patch rules, including LOV return
  values and retained-data expectations. Automatic classification is not required
  for Elaboration.

## Follow-up roadmap — existing backlog, no duplicate items

| Order | Work and acceptance | Existing items |
|---|---|---|
| 1 | Pin the client; qualify consistent source/distribution, mappings and stable required identities. | PBI-028/029/037/038 |
| 2 | Establish PROJECT-compatible source layout, one migration owner and Working Copy team checkpoints. Qualify team contention and central synchronization. | PBI-020/037/039/042 |
| 3 | Define component contracts/SemVer; enforce compatibility and automatic pre-deployment drift rejection. Prove ownership fencing. | PBI-052/021/022/023/045 |
| 4 | Reproduce the integration-only partial failure and reviewed forward repair; preserve committed work and evidence. | PBI-024/045 |
| 5 | Combine utPLSQL/coverage, native audits and browser checks against the same artifact; enforce results in pipelines and independently reproduce the walkthrough. | PBI-040/041/043/046 |
| 6 | Perform complex Foundation upgrades **in E.5, after toolchain stabilization**. | PBI-048/049/050 |

These refine existing backlog acceptance; they do not change priority, assignment
or completion status. E.1 evidence remains unchanged. The
[walkthrough](cicd-walkthrough.md) presents the demonstrated journeys and gaps;
[detailed evidence](oracle-gap-analysis-detail.md) remains available for inspection.
