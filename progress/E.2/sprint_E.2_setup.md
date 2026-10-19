# E.2 — Contract and analysis

## Contract

Sprint E.2 was activated on 2026-10-19 at the Product Owner's explicit request.
Mode: managed. Current Test: none. Current Regression: none, by Product Owner
direction for the disposable E.2 prototype. Focused exercise verification and
live handover remain required. PBI-051 is the only root assigned item.
[PLAN](../../PLAN.md#sprint-e2---assess-e1-against-oracle-lifecycle-guidance)
owns assignment and lifecycle; the [board](../../PROGRESS_BOARD.md) owns
execution status. The [scope record](sprint_E.2_proposedchanges.md) is the
planning baseline; the current request additionally makes explicit that bounded
exercises may use Oracle-recommended capabilities outside E.1's mechanisms.

The implementor owns analysis, design, bounded experiments, evidence,
recommendations and the runnable handover. The Product Owner approves material
design and policy changes, backlog promotion, handover and closure. Activation
does not approve experiment implementation. No critical scope ambiguity prevents
design. Exact experiment outcomes and current runtime readiness remain unknown.

Apply the [RUP entry skill](../../.agents/skills/rup-strikes-back/SKILL.md), its
manager, contract/analysis and design/test adapters, the canonical manager and
role procedures, and [local policy](../../RUPStrikesBack.patch/RUP_patch.md).
The sprint and progress adapters govern the activation/board edits. Generic
cooperation, Git, backlog/sprint definitions, testing, failure and bug rules
were reviewed. GitHub Actions rules apply if a workflow is later selected;
no hosted workflow is being implemented here. No Ansible/Terraform rules apply.

Local P1 permits proportional Elaboration experiments. P7 requires narrative
paragraphs, portable instructions and current-sprint scope. P8 defers a
completion commit until the increment and audit pass; it overrides generic
per-phase commits. No remote push is authorized. P9 requires a rehearsed
presentation pair, complete manual walkthrough and actual live review. The
manager requires explicit design approval; local P8 extends that gate to test
skeletons. Perform the RUP role responsibilities serially.

Existing uncommitted changes were present in BACKLOG, PLAN, board, README,
ROADMAP, shared docs, E.1 diagrams and E.2–E.5 planning directories. Preserve
them without treating them as work performed in this execution. Do not rewrite
E.1 records or change E.3–E.5 artifacts. Complex Foundation PBI-048–050 stays
assigned to E.5, after accepted technology/toolchain stabilization. Do not
modify the method submodule, retained user data or unexpected live edits.
Token accounting by phase is unavailable; no synthetic counts are reported.

## Analysis

### PBI-051 outcome and actors

Deliver a source-backed retain/replace/investigate decision for E.1 against the
Oracle paper and documentation applicable to the tested versions. The
[SRS](../../docs/srs.md#actors) supplies developer, reviewer, operator and
laboratory-reproducer roles and Git hosting as an external system. Follow the
developer's author/capture/review journey (UC-7–10), operator release and repair
journey (UC-4/5/11), and reproducer journey (UC-6/12). Assess greeting/history
behavior (UC-2/3) to check that delivery preserves useful outcomes. Oracle
APEX/SQLcl and the local database are the execution boundary; a local Git
review does not establish hosted PR automation.

Acceptance requires each material finding to connect an exact source section,
E.1 implementation/evidence, relevant requirement, classification, evidence
strength, alternative and disposition. Required exercises resolve uncertainty;
an observed limitation can satisfy an analysis question without delivering the
missing product capability. Reconcile proposals with existing PBIs before
requesting additions. A roadmap must order dependencies and name decisions
needed to revise current requirements or later sprint scope.

### Baseline and compatibility

The [E.1 assessment](../E.1/sprint_E.1_assessment.md) records APEX 24.2.0,
SQLcl 25.3.0.274.1210, Java 21.0.12.1+1 and Database 23.26.3.0.0. These are
historical version observations until an E.2 preflight records the runtime.
Its [design](../E.1/sprint_E.1_design.md),
[implementation](../E.1/sprint_E.1_implementation.md),
[tests](../E.1/sprint_E.1_tests.md) and
[handover](../E.1/sprint_E.1_handover.md) establish selected initial release,
compatible Hello patch, incompatibility rejection, live APEX drift rejection
and bounded additive-failure repair. Wider acceptance remained incomplete at
closure. Keep that distinction in all comparisons.

Source inspection confirms that `scripts/cicd-build.sh` delegates to the
custom `cicd-artifact.py` archive builder; `cicd-candidate-check.sh` binds a
candidate receipt to a Git commit and selected development checks. Release
scripts call SQLcl Liquibase and native APEX installers. Thus E.1 is Oracle
delivery primitives with project orchestration, not a wholly non-native
technology. The [architecture](../../docs/architecture.md) owns the mechanism
description; this analysis does not reaccept it.

### Initial source observations, not experiment conclusions

The supplied [paper](../../refs/apex-lifecycle-management-v3.pdf) is June 2025,
version 3.2 despite its filename; page 2 says its examples were validated with
APEX 24.2 and SQLcl 25.1.1. Extraction used pypdf over all 47 pages and page
32 was rendered and visually inspected. pypdf reported malformed pointer
warnings but completed extraction. Confirm exact claims visually as findings
are authored; no replacement copy of the supplied reference is produced.

Pages 14 and 32 describe Working Copies, team progress exported to Git and a
separate feature-centric approach. Pages 18–20 describe SQLcl PROJECT capture
and staging; pages 26–30 cover release and mapped workspaces. Appendix B,
page 47, explicitly discusses lower-level export alternatives. These make
mechanism-by-mechanism assessment more useful than a binary conformance label.

The [APEX 24.2 Working Copy reference](https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/about-working-copies.html)
documents replacement-based merge behavior, manual deletions, unsupported
types and a background-job prerequisite. These are bounded limitations to
exercise, not evidence that Git integration is impossible. The
[SQLcl 25.3 PROJECT reference](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/project.html)
documents capture, staging, release and artifact deployment. Its availability
does not establish this lab's reconstruction or migration correctness.

The SRS FR-8 break-glass restriction and component-wide reservations, and
FR-13 automated-operation rule, may conflict with a routine native authoring
workflow. Separate these policy questions from retention of Git as accepted
release authority. Do not use undocumented repository writes to force an
automation result. Lack of an API found in an initial search is an unknown,
not proof of product incompatibility.

### Feasibility, dependencies and next gate

Analysis is feasible with existing source, Oracle references and bounded
disposable experiments. Resource use, identities, privileges, supported APIs
and native artifact behavior require preflight/execution. The current plan's
E.3/E.4 scopes are hypotheses for later implementation, not prerequisites
requiring E.2 to deliver them. Existing PBI-018–047 cover most likely follow-up
outcomes; PBI-048–050 remain E.5 work. No new backlog item is registered now.

The material above is preliminary scoping, not completed analysis. The separate
[analysis record](sprint_E.2_analysis.md) owns the requirements, actor journeys,
comparison findings and unresolved evidence needed before exercise design.
That desk-analysis baseline is now complete and presented in the
[analysis review summary](sprint_E.2_inception.md); PBI-051's experiment-backed
outcome remains unfinished.
The earlier premature design request remains withdrawn. Following external
review and explicit Product Owner analysis approval on 2026-10-19, the
[revised exercise design](sprint_E.2_design.md) is Proposed for its own managed
approval. The Product Owner subsequently directed Test: none and Regression: none;
those values replace the original full-suite parameters in PLAN. The
[documentation audit](sprint_E.2_documentation_audit.md) records the transition.
No exercise, test skeleton, runtime test, live demonstration or completion
commit is claimed.

## Current construction interpretation

The preceding scoping/approval statements are retained stage snapshots. The
Product Owner accepted the revised design and authorized construction, fresh
pinned provisioning and the recorded scheduler adjustment. The
[implementation](sprint_E.2_implementation.md), [actual evidence](sprint_E.2_tests.md)
and [gap decision](oracle-gap-analysis.md) now own executed findings. The
[walkthrough](sprint_E.2_increment_demo.md) is prepared; actual
[Product Owner live review/acceptance](sprint_E.2_handover.md) remains pending.
