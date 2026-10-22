# E.2 — Product Owner decision brief

22 October 2026 · Decisions pending

**Recommendation:** continue with SQLcl PROJECT, APEX Working Copies and Git as
compatible options. Preserve the useful E.1 controls until qualified replacements
meet the same requirements. E.2 supports this direction, not production adoption.

**Give developers flexibility through stable, industry-standard tools and techniques.**

## What E.2 established

**Native delivery works for the selected application.** PROJECT captured source,
staged migrations and packaged mapped deployments. The Foundation/Hello/World
application installed and the compatible Hello 1.0.1 patch passed fresh,
populated-upgrade and repeat exercises in integration. The same initial archive
reached UAT. You reported the complete F upgrade journey finished.
[Initial delivery](tests/project-integration-mapped-validation.json) ·
[UAT promotion](tests/project-uat-promotion-validation.json) ·
[Patch evidence](tests/project-f2-upgrade-validation.json).

**Working Copies coexist with PROJECT and Git.** Native comparison, selective
refresh and merge worked. The demonstrated team checkpoint captures agreed Main
state into Git. Working Copies isolate APEX metadata, not database schema changes.
The direct export of a private copy was described but was not the demonstrated
release path. [Working Copy evidence](tests/project-f1-working-copy-validation.json).

**Some custom mechanisms can be reduced.** Native APEX restricted access and
publication cover the exercised runtime gate. PROJECT/Liquibase supplies migration
history. These do not replace E1_CTRL's qualification, ownership, provenance,
drift and repair responsibilities as a whole.

## G, H and I: native support gaps

**G — Component version dependency protection: not supported by the evaluated
native workflow.** PROJECT verification accepted both allowed and conflicting
component declarations. Keep explicit contracts and compatibility admission.
[Clean comparison](tests/project-verify-fix-validation.json).

**H — Automatic live-drift deployment protection: not supported by the evaluated
delivery path.** No qualified automatic application/schema/code comparison and
rejection gate was supplied. The unchanged-artifact replay ran no pending import
and did not test overwrite protection. [Evidence limits](h-live-drift-evidence.md).

**I — Automatic failed-deployment repair: not supported.** A developer must inspect
and design the repair. SQLcl/Liquibase can deliver a reviewed forward repair, but
E.2 did not validate that E.1-equivalent scenario. This remains missing validation,
not evidence that Oracle cannot perform forward repair.

## What prevents adoption now

**Release verification and source consistency.** Retained F artifacts have a
SQLcl 25.3 verification failure. A separate clean 25.4.1 comparison passed, but it
does not certify those artifacts. Pin the client, remove post-stage source/import
inconsistency and qualify a new release. [Verification evidence](tests/project-verify-fix-validation.json).

**Identity and protections.** Earlier mapped replacement changed region IDs.
Qualify required identity and saved-report preservation, compatibility admission,
drift rejection, ownership fencing and reviewed recovery before relying on them.

There is no demonstrated general incompatibility between PROJECT, Working Copies
and Git. Reevaluate E.1's break-glass authoring and broad reservations as project
policies. Keep one migration authority for each delivery stream.

## Decisions requested

1. **Accept E.2's assessment with its stated limits?** Recommended: yes. Retain G/H
   as protection gaps and I's reviewed-repair validation as unfinished. Acceptance
   does not certify a production release or close the sprint automatically.
2. **Keep PROJECT and Working Copies as supported options?** Recommended: yes.
   Maintain compatible repository conventions, Main team checkpoints and qualified
   lower-level alternatives. Do not mandate one tool for every journey.
3. **Prioritize stabilization and protection before pipeline adoption?** Recommended:
   yes. Use the existing backlog below, without creating duplicate work.
4. **Reevaluate E.1 authoring restrictions?** Recommended: yes, through native team
   collaboration evidence. Preserve required coordination and ownership outcomes.
5. **Keep complex Foundation upgrades in E.5?** Recommended: yes, after toolchain
   stabilization. No complex Foundation upgrade is delivered by E.2.

Record each decision as accepted, amended or deferred. Decisions remain pending.

## Proposed order of follow-up

1. **Stabilize capture and release qualification.** Pin the client, source/layout,
   target mapping and identity policy. PBI-028/029/037/038.
2. **Establish collaboration and component contracts.** One migration owner,
   Working Copy checkpoints and explicit major/minor/patch rules, including LOV
   return values and compatibility. PBI-020/039/042/052.
3. **Qualify delivery protections and reviewed recovery.** Reject incompatible or
   drifted targets, prove ownership fencing and demonstrate inspected partial-failure
   repair. PBI-021/022/023/024/045.
4. **Compose quality checks and pipelines.** Use utPLSQL/coverage, native audits and
   browser checks on the same candidate, then independently reproduce delivery.
   PBI-040/041/043/046. Complex Foundation evolution follows in E.5, PBI-048/049/050.

These are refinements of [existing backlog items](../../BACKLOG.md), not new
assignments or completed later-sprint work. E.1 historical evidence remains intact.

## Review package

The [editable diagram](model.drawio) retains the current diagram edits in E.2.

Read the [decision presentation](sprint_E.2_product_owner_handover.pptx) and
[concise gap analysis](oracle-gap-analysis.md). Use the
[native SQLcl walkthrough](cicd-walkthrough.md) to inspect demonstrated journeys.
The earlier increment presentation remains a separate exercise record.

Oracle basis: [lifecycle paper](../../refs/apex-lifecycle-management-v3.pdf),
[SQLcl PROJECT](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/project.html),
[APEX Working Copies](https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/about-working-copies.html),
[subscriptions](https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/using-shared-component-subscriptions.html).
Preparation receipts and screenshots identify rehearsal scope. Operator-reported
F completion is separate evidence. Neither establishes full production readiness.
