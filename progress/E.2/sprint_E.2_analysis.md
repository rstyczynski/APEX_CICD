# E.2 — Analysis

Status: Complete — desk analysis approved by the Product Owner on 2026-10-19

The external analysis review found no required corrections; the Product Owner
explicitly approved analysis and directed design. The
[revised exercise design](sprint_E.2_design.md) is Proposed, not accepted.

This completes the analyst's problem/requirements assessment, not PBI-051 or
the final experimentally supported gap report. The evidence questions below
are inputs to design. No exercise or new runtime verification has run.

## Purpose and authority

This document owns E.2's analysis of the problem, required outcomes, actor
journeys, evidence and unresolved questions. [Setup](sprint_E.2_setup.md)
records contracting and preliminary scoping. Contracting establishes working
rules and responsibilities; it does not establish the adequacy of a solution
or replace analysis. The earlier premature declaration and exercise approval
request were withdrawn. The [revised exercise design](sprint_E.2_design.md)
now has its own approval request following explicit analysis acceptance.

[PBI-051](../../BACKLOG.md#pbi-051-assess-the-e1-delivery-approach-against-oracle-lifecycle-guidance)
owns the intended outcome. [PLAN](../../PLAN.md#sprint-e2---assess-e1-against-oracle-lifecycle-guidance)
keeps E.2 active in managed mode; the [board](../../PROGRESS_BOARD.md) keeps
the sprint/PBI under_design after analysis approval. Proposed sprint-scoped
children are defined in the exercise design, without changing root assignment.
The [SRS](../../docs/srs.md) owns requirements and actor
definitions; [architecture](../../docs/architecture.md) and
[research](../../docs/cicd-research.md) own earlier mechanisms and rationale.
The [test profile](../../docs/test-profile.md) owns verification expectations.
Analysis may challenge those decisions but does not silently amend them.

## Problem and required outcome

E.1 demonstrated a selected delivery/protection slice using Oracle primitives
and substantial project orchestration. The decision now needed is which
responsibilities should remain custom, which Oracle capabilities can replace
them, and which missing outcomes or policy constraints prevent adoption.
Preference for native tooling alone is insufficient evidence for replacement.
Similarly, unfinished E.1 tests do not prove a limitation of Oracle technology.

PBI-051 requires a source-backed gap analysis, justified follow-up proposals,
a dependency-ordered roadmap and a reproducible demonstration. Focused exercises
serve specific unresolved questions; they are selected after those questions
are understood. E.2 must not become delivery of the full E.3/E.4 workflows or
the complex Foundation changes assigned to E.5.

## Goals and further coexistence opportunities

**Give developers flexibility through stable, industry-standard tools and techniques.**
The gap analysis should establish supported choices and their practical limits.
The Product Owner favors coexistence of PROJECT, Working Copies and useful
E.1 capabilities. These operate across several responsibilities; coexistence
may mean using them together or choosing an alternative at a defined boundary.
It does not mean maintaining duplicate authorities for one source or migration.

The desired outcomes are a small set of understandable developer journeys,
explicit contracts for source/identity, dependencies, migration ownership,
validation and artifact promotion, and evidence about correctness, usability,
operating effort and version stability. Identify avoidable custom work while
retaining justified project protections. Recommend a default journey and a
bounded set of qualified alternatives; optionality must have a visible support
cost. Exact-version support, reproducibility and documented interfaces are
evidence to establish, rather than properties implied by the motto.

Pipelines are the intended delivery destination. Local commands support
development, focused exercises and reproducibility; local versus hosted
execution is not a coexistence goal or tool-selection decision for E.2.
Assess pipeline suitability where it affects recommendations, while retaining
the existing later-sprint allocation of full pipeline delivery.

Further opportunities already visible in AN-01–14 are:

1. **Generated changes and explicit migration intent can coexist.** PROJECT
   documents generated staging plus custom SQL changesets
   ([SQLcl 25.3, section 6.2](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/project-command.html)).
   Evaluate generated structural changes with reviewed data/unsupported changes
   in one changelog authority. E.1 migrations may inform adoption, but existing
   history cannot simply be replayed or silently marked applied. This is a
   documented extension model; compatibility with our history remains unproved.
   AN-02/PF-01/06 and PBI-037/038 cover it.
2. **Combine testing, compatibility checks and release evidence.**
   [Advisor](https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/running-advisor-to-check-application-integrity.html)
   supplies application-integrity checks; the paper separately discusses
   PL/SQL tests/coverage and browser journeys (pages 22–25, 30–31). Retain useful
   E.1 assertions while identifying missing outcomes. Test runners can vary
   where they satisfy the same defined check; static audits, coverage and
   user-visible acceptance are distinct evidence. AN-06/10 and PBI-034/040/041
   cover this without requiring one framework for every responsibility.
   Explicitly analyse how utPLSQL tests/coverage, E.1 assertions, semantic-version
   interpretation, component dependency admission, native audits and browser
   checks combine around the same identified candidate. Semantic-version labels
   alone do not prove compatibility, and passing unit tests does not establish
   dependency correctness. Identify each check's owner, inputs, applicable stage,
   expected evidence, failure effect and invalidation when source, dependencies
   or target state changes. Reject unsupported combinations before target writes;
   distinguish those checks from tests that require an installed test target.
   Relate PF-08/EQ-2 and AN-08/EQ-4 to AN-06/10/EQ-5 so the recommendation is a
   coherent validation approach suitable for pipelines. Discover native/bundled
   support and only then justify missing integration. Existing version/dependency
   and safety items retain ownership; E.2 analyses and exercises selected gaps,
   rather than implementing all test suites or complex E.5 upgrades.

APEX subscriptions belong within component interface/dependency analysis, not
as another coexistence opportunity. AN-11 explains the native propagation
mechanism; PF-08/EQ-2 cover the component version and compatibility contract.

Environment-topology flexibility is already covered by the project approach;
it is not an additional coexistence proposal. Retain AN-05/09's qualification
of the supported arrangements and branch-instance identity conditions within
PBI-019/020/027/046. This clarification does not imply that all topologies have
already been demonstrated or satisfy identical isolation guarantees.

For each opportunity, report whether it is documented, locally demonstrated,
conditional or unsupported; identify the common contract, extra maintenance
and evidence that could reject it. Coexistence is a preferred direction, not a
predetermined successful result. The [review summary](sprint_E.2_inception.md#goal-of-the-gap-analysis)
presents this goal. H-1/H-2 and EQ-1–5 remain the bounded evidence framework;
these observations add no PBI, exercise approval or later-sprint implementation.

## Elaboration criticality decision — component contracts

The component contract must be a project/artifact input understood by the
toolchain. E.1 already provides a bounded starting implementation:
[release metadata](../../release/manifest.json) declares component versions,
exact dependencies and supported starts, while the
[artifact inspector](../../scripts/cicd-artifact.py) checks the selected
combinations and the APEX release version. FR-7 expressly distinguishes
declared compatibility from proof based on version numbers. E.1's design
excluded a generic dependency resolver and SQL semantic parser. This inspection
supports retaining the bounded model; it is not a fresh runtime verification
or evidence of automatic interface-change analysis.

**Critical now: preserve and enforce the declared contract across tool choices.**
EQ-2/PF-08 must establish whether component/dependency metadata can accompany
accepted source and the native artifact, whether it can be read by admission
checks, and whether observed installed state is reconciled with that artifact.
Select the smallest missing positive/negative observation after reusing E.1
evidence. Exact approved combinations are sufficient for the current bounded
requirement. Discover PROJECT's version syntax/ordering/range capabilities from
documentation or help first; a general SemVer engine or resolver is not an
Elaboration prerequisite. PBI-037/038/045 already cover native integration and
retained protections; do not add a duplicate PBI.

**Critical now: qualify the source path we actually recommend.** Working Copy
changes must reach accepted Git source and reconstruction without unexplained
loss or inclusion. A changed candidate must not retain stale validation
authority. These are existing EQ-1/2/4 obligations, not a mandate to implement
all hypothetical subscription or consumer scenarios. A remaining inability to
preserve declared dependencies or reject an unsupported combination would be
a material architecture gap, not an optional improvement.

**Describe now, deliver through existing follow-up:** document a representative
consumer-facing contract and the responsibilities of provider tests, consumer
checks, data-preservation tests and UI tests. Broad consumer-contract suites,
LOV evolution cases and coverage expansion do not block E.2's toolchain decision
unless that decision relies on an unproved behavior. PBI-034/040/041 cover
test/audit delivery; PBI-048–050 cover actual compatible/breaking Foundation
evolution and retained-data behavior in E.5. E.2 does not expand those items or
move them earlier. A representative contract may remain reviewed prose linked
to metadata; a machine-readable inventory of every interface is not required.

**Conditional, not a current blocker: subscription propagation.** Record how
publish/refresh could change consumer copies, and qualify any assumption used
in a recommendation. Since subscriptions are not required by the selected
single-application delivery slice, do not construct a subscription experiment
just to prove the general risk. PBI-044 already explicitly includes controlled
propagation and publish/refresh; PBI-020/045 cover relevant reconstruction/drift
outcomes. If E.2 recommends subscriptions as essential to its chosen path,
the previously deferred uncertainty becomes a required evidence question.

**Not critical for Elaboration: infer compatibility from arbitrary changes.**
Automatic discovery of all consumer dependencies, semantic comparison of LOV/
SQL/APEX behavior, and automatic selection of major/minor/patch changes are a
separate product capability. They are not required by FR-7's explicit
declarations and are not prerequisites for using standard tools. Retain this
as a deferred, unregistered enhancement direction; do not create a PBI without
an independently justified product need. Human classification backed by bounded
tests is sufficient for the current architecture. Existing PBI-048–050 already
exercise the meaning of compatible/breaking changes without requiring such an
analyser. No automated semantic-analysis PBI or sprint assignment is warranted now.

By subsequent Product Owner direction,
[PBI-052](../../BACKLOG.md#pbi-052-define-semantic-versioning-rules-for-component-contracts)
records the distinct follow-up to define component interfaces and map actual
changes to major/minor/patch classifications. This formalizes the human-facing
contract/classification rules; it does not implement automatic inference or
duplicate the upgrade demonstrations in PBI-048–050. It is Proposed and
unscheduled, with no additional E.2 completion gate.

This decision narrows the earlier discussion of possibilities into the
Elaboration evidence needed. The [review summary](sprint_E.2_inception.md#component-contract-criticality-decision)
states the current boundary. Exercise selection and implementation remain
subject to managed design approval.

## Actors and end-to-end outcomes

The [SRS actor model](../../docs/srs.md#actors) supplies five actors. A second
operator reproducing the lab is another A-03 participant, not a new actor.
The Product Owner accepts product/process decisions but is not an additional
runtime actor. SQLcl, APEX and the project pipeline are system components.

**A-01 Developer, supported by A-02 Reviewer and A-03 Operator:** obtains a
known development baseline, authors an application/database change, compares
and captures it, addresses review and verifies the integrated outcome. The
success criterion is preservation of intended changes and attributable source,
not simply a successful export. Alternatives include shared DEV with Working
Copies and private task environments. Relevant cases are UC-7–12. Analysis
must explain the different meanings of native Main integration, Git integration
and schema isolation before recommending either collaboration method.

**A-02 Reviewer / Packager, supported by A-05 Git hosting:** identifies the
exact candidate/base, reviews complete dependencies and validation results,
accepts integration and releases a reproducible artifact. Changed source or
base invalidates earlier evidence. Team checkpoints and feature-specific PRs
offer different attribution granularity. Local Git evidence cannot establish
hosted PR enforcement or pipeline history. Relevant cases are UC-4/7/10/12.

**A-03 Delivery operator:** qualifies and deploys an identified artifact to a
known target, checks installed definitions and retained data, and handles drift
or committed partial failure. Success requires an observed verified outcome
with traceable receipts; an installer exit alone is insufficient. Unsupported
starts, changed live content and unsafe repair states must remain visible.
Independent reproduction is part of this role. Relevant cases are UC-1/4/5/6/11.

**A-04 Application user:** configures Hello/World entries, records greetings
and reads earlier history across a compatible delivery. The user-visible
outcome supplies the preservation oracle for delivery comparisons. Runtime
availability and retained history must be distinguished from application source
reconstruction. Relevant cases are UC-2/3 and the verification part of UC-11.

## Analysis model and evidence boundaries

There are three distinct states to trace: mutable authoring state in APEX and
its parsing schema; reviewed source and migrations at an accepted Git revision;
and installed definitions plus user data in a target. An APEX Working Copy
changes the authoring workflow. It does not, by itself, decide which Git
revision is accepted or which artifact may be deployed. Likewise, a Git branch
does not create an isolated database merely by existing.

For every proposed equivalence, identify the responsibility being compared.
Source capture, change generation, packaging, qualification, promotion,
concurrency, application access and recovery are different responsibilities.
A native package command can replace packaging while leaving application
compatibility or deployment authorization as project concerns. Conversely,
retaining one project-specific check does not justify retaining the entire
custom release framework.

Use four evidence levels: official version-specific documented behavior;
inspected implementation; historical executed evidence with its date/scope;
and fresh exercise results. Keep an unresolved hypothesis explicit. No runtime
exercise has been implemented or executed in E.2. Current runtime readiness
and reproduction costs are unknown.

## Source and implementation comparison

Analysis date: 2026-10-19. The supplied paper is version 3.2, June 2025;
its page 2 names APEX 24.2 and SQLcl 25.1.1 as the validated example versions.
Page references below are printed PDF pages. The applicable baseline is E.1's
recorded APEX 24.2.0 / SQLcl 25.3.0.274.1210 / Database 23.26.3.0.0; those
historical runtime observations have not been refreshed. Official sources were
opened for the named versions. The
[source inventory](tests/analysis_sources_20261019.json) records exact local
input hashes and reference URLs. A dirty documentation checkout is not
relabeled a released E.1 revision.

### AN-01 — E.1 already uses supported source-control primitives

The paper's Appendix B, page 47, discusses lower-level exports alongside
SQLcl PROJECT. [APEX 24.2 export documentation](https://docs.oracle.com/en/database/oracle/apex/24.2/aeadm/exporting-one-or-more-applications.html),
sections 3.12.11.1.6.3–6, documents split exports and identity/date options.
[E.1 capture](../../deploy/operator/capture.sql) uses these options and excludes
Supporting Objects while [the changelog](../../db/changelog.xml) separately
owns database changes. Classification: supported primitive equivalence,
with an independently maintained source/migration boundary. This is not evidence
of complete dependency capture or reconstruction. PBI-020/035/037 already cover
those outcomes; do not propose another capture item.

### AN-02 — PROJECT requires evaluation as a complete way of working

Paper pages 18–20 and 26–27 describe PROJECT capture, staging and release.
[SQLcl 25.3 PROJECT](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/project.html),
section 11.16, documents corresponding commands. E.1 instead uses reviewed
SQL migrations and [a custom archive implementation](../../scripts/cicd-artifact.py)
that packages Git files and validation receipts. Classification: mechanism
divergence and potential avoidable custom work, not an established blocker or
proven unnecessary mechanism. Determine which generated artifacts preserve
source identity, installation order, mapped targets, validation binding and
data. PBI-037/038/043 own the likely follow-up; PBI-021/045 own retained safety
questions. A second independent migration authority would create a new problem.

Evaluate the native developer/operator workflow before reducing PROJECT to a
replacement packager. The key change from E.1 may be database/APEX authoring
followed by exported source snapshots and generated, reviewed distribution
scripts, rather than manually maintaining the whole migration/package path.
Git acceptance still supplies release authority; authoring in a database does
not contradict that boundary. Reevaluate E.1-stage policies where necessary
instead of forcing PROJECT into the old controller's operating model.

Paper pages 18–20, 26–30 and 32–44 connect project setup, filtered capture,
staging, team/feature integration and release/deploy. The
[SQLcl 25.3 project examples](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/project-command-usage-examples.html),
section 6.5, provide the version-specific workflow reference. Compare that
operating model with the current sources, not only the availability of each
command. EQ-2 and the [review questions](sprint_E.2_inception.md#questions-about-the-sqlcl-project-way-of-working)
identify the missing evidence.

The [PROJECT fit assessment](project-fit-assessment.md) now makes the adoption
decision explicit. It enumerates PF-01–12 with possible design assumptions,
documented limitations or unproved guarantees, requirement impact, validation
obligations and provisional verdicts. Evaluate native fit and necessary
supplements against the SRS, not against command count or the ability to wrap
PROJECT in E.1's controller. The Pretius example supplied by the Product Owner
is an input to these questions, not proof that the selected version or full
requirements passed. EQ-2 remains the exercise-selection group for this
expanded assessment; PF identifiers refine AN-02 rather than adding new PBIs.

### AN-03 — Working Copies and accepted Git authority are distinct questions

Paper pages 14 and 32 describe native Working Copies and coordinated team
exports to Git. [APEX 24.2 Working Copies](https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/about-working-copies.html),
section 5.9.1, explains comparison and replacement-based merge, plus unsupported
types and manual deletion handling. The Product Owner clarified that the
break-glass restriction and component-wide reservations were policies for the
E.1 stage. They describe the comparison baseline; they do not constrain E.2's
reevaluation or predetermine the future workflow. Classification: E.1 policy
differences to reassess, alongside documented merge limitations; no established
Working Copy/Git incompatibility.

The open question is whether a change can travel from native authoring through
reviewed Git source to reconstruction without lost edits or ambiguous source
identity. The analysis must also establish what team-level checkpoint attribution
does and does not satisfy. PBI-039 covers native collaboration; PBI-020/037 cover
capture/reconstruction; PBI-036 covers policy reconciliation.

Keep periodic team checkpoints within this Working Copy workflow assessment,
not as a separate coexistence opportunity. Here “checkpoint” means exporting
the agreed Main state and committing the team's accumulated progress to Git,
as described on paper page 32; it is not an additional APEX feature. This
appears conceptually compatible with E.1's capture-to-Git approach. Validate
checkpoint completeness, task attribution, treatment of unrelated/unaccepted
work and reconstruction rather than presume that E.1 capture must be replaced.
H-2/EQ-1 own this evidence, with EQ-2 checking any PROJECT capture route.
Feature-branch/private-instance differences remain in AN-09/EQ-3; they do not
require a separate team-checkpoint workstream.

Reevaluate usability as well as technical transport: can developers understand
what is isolated, coordinate work, inspect differences, refresh and merge
without losing intent, abandon experiments safely and get accepted changes
into the Git pipeline? Record actual operator steps, confusing decisions,
conflicts and recovery effort. A successful export alone cannot establish a
usable collaboration workflow. The recommendation may replace the E.1 policies
with native coordination if evidence supports that choice.

### AN-04 — Page coordination is not the component reservation requirement

Paper pages 12–14 describe native page coordination. The E.1 FR-8/UC-9 baseline requires
an atomic component-wide decision before managed editing, including tasks on
different pages of the same component. The requirement's scope is broader than
a page lock. Classification: different coordination scopes, not proof that
native collaboration is defective. Reevaluate whether the broader E.1 exclusion
is still needed; do not require native page locking to reproduce that policy
as a condition of being usable. Assess the actor goal and observed risk, then
recommend native coordination, justified supplemental controls or a revised
policy. PBI-018/019/039 already expose these concerns.
The [24.2 page-lock reference](https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/locking-and-unlocking-a-page.html),
section 6.9, permits administrator unlocking. Page coordination is not a
durable deployment-ownership or runtime-fencing mechanism.

### AN-05 — One instance is not inherently contrary to the paper

Paper pages 28–30 describe separate workspaces/schemas in one APEX instance
and the target mapping needed there, as well as separate instances. E.1's
[area configuration](../../config/areas.json) uses distinct schemas/workspaces
and application IDs. Classification: a supported topology option with shared
failure/administrative boundaries, rather than physical isolation. Mapping,
stable IDs and repeat replacement remain validation questions. E.1's
[patch import](../../deploy/operator/import_patch.sql) contains explicit offset
reuse; native replacement behavior must be compared against that observed
identity problem. PBI-020/027/038 cover the follow-up.

### AN-06 — Test execution does not establish the paper's coverage outcome

Paper pages 22–25 distinguish PL/SQL regression/coverage from browser journeys.
E.1's [unit entry points](../../tests/unit/test_greeting.sh) call transactional
SQL checks; the [assessment](../E.1/sprint_E.1_assessment.md) distinguishes
selected browser observations from unfinished full acceptance. Classification:
useful existing checks with missing coverage measurement and broader automated
browser evidence. PBI-040/034 already cover those gaps. No new testing framework
is justified until the required observable results are specified.

### AN-07 — Local automation is not the full pipeline operating journey

Paper pages 40–45 cover source-to-release and build/test/deploy journeys with
run history and retained results. E.1's
[candidate check](../../scripts/cicd-candidate-check.sh) and archive builder bind
selected local evidence to source, while its
[assessment](../E.1/sprint_E.1_assessment.md) retains hosted execution and
independent attestation as later concerns. Classification: partial outcome
coverage and delivery gap. PBI-043/030/031 cover the distinct outcomes. Determine
what needs a native command, a thin adapter or a runner capability before
assigning replacement work.

### AN-08 — Safety requirements need their own equivalence assessment

E.1 checks a bounded component combination in its
[manifest](../../release/manifest.json) and artifact inspector; its
[fingerprint query](../../deploy/operator/fingerprint.sql) uses a native APEX
export checksum. The [handover](../E.1/sprint_E.1_handover.md) preserves a manual
drift decision and bounded forward-repair evidence. Neither native capability
availability nor absence from a lifecycle example establishes equivalence for
FR-7/9/10. Classification: explicit project obligations with incomplete broader
proofs. PBI-021–024/045 cover admission, fencing, schema drift and recovery.
Assess those obligations separately before recommending deletion of controls.

### AN-09 — E.1 private areas differ from the paper's branch instances

Paper pages 33–34 pair a feature branch with a private APEX installation; page
34 requires matching workspace name, workspace ID and APEX version including
patch level. It offers PDB cloning or a matching workspace in another database
followed by installation of the current build. E.1's
[mapping](../../config/areas.json) instead uses E1_DEV_A/B/C and distinct
application IDs in one PDB. Classification: a documented topology/identity
deviation. The DEV/TEST workspace arrangement on pages 28–30 does not prove
equivalence for this branch-authoring topology.

The historical [identity experiment](../E.1/tests/apex_identity_20261018.txt)
establishes bounded replacement-offset and saved-report behavior, not the full
branch-instance criterion. Determine which differences are harmless and which
pollute reviewed source. A retained single-instance alternative needs explicit
deviation acceptance with capture/reconstruction evidence. PBI-019/020/046
already cover the outcome. This is not a product blocker, nor authority to
implement the full E.4 environment now.

### AN-10 — Native code audits are an unexecuted gap

Paper pages 30–31 describe Advisor, embedded-code extraction, SQLcl code
scanning and optional external products. [APEX 24.2 Advisor](https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/running-advisor-to-check-application-integrity.html),
section 24.6, documents metadata checks before deployment. The
[25.3 SQL performance appendix](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/sql-peformance-issues.html)
lists relevant patterns; [24.2 GET_APPLICATION](https://docs.oracle.com/en/database/oracle/apex/24.2/aeapi/GET_APPLICATION_Function.html),
section 28.1, documents EMBEDDED_CODE output. Inspected E.1 evidence does not
establish those audits or measured scan coverage. Compilation and greeting
tests are not equivalent. Classification: implementation/evidence gap under
PBI-041. Unavailable external products remain optional/unexecuted, not blockers
for native delivery. Executing extracted application SQL is not a safe substitute
for static analysis.

### AN-11 — Mini apps are optional modularity

Paper pages 7 and 15–16 describe library/mini-app reuse, subscriptions and shared
authentication. [APEX 24.2 Component Groups](https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/using-component-groups.html),
section 16.11, and [subscriptions](https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/using-shared-component-subscriptions.html),
section 16.3, cover specified shared-component types. E.1's Hello and World are
logical components in one application. Classification: optional capability
absent from E.1, not a defect in the small-app topology. A component group does
not bundle arbitrary pages, schema migrations and independent semantic versions.
PBI-044 already owns the separate reuse outcome; it is not an assumed solution
for Foundation coexistence or independent maintenance in E.5.

In concrete terms, a subscription copies a supported shared component from a
master application into another application in the same workspace and retains
a link to that master. The subscribed copy is read-only; changes are made at
the master and propagated by publish or refresh. For example, applications can
reuse a master List of Values. This is development-time shared-component reuse,
not a reference to commercial subscriptions or a general package/version
manager. Its documented dependency handling copies/reuses specific APEX shared
components; it does not establish version constraints for our Foundation/Hello/
World components. Keep it as a bounded optional reuse finding, not an adopted
release mechanism or a new workstream.

For the project's component model, an exposed LOV or other shared component
is part of the owning component's declared interface wherever consumers depend
on its behavior. Internal implementation details do not automatically become
public interfaces. A subscription is one way to materialize that dependency;
apply the same compatibility rules used for other APEX/database interfaces.
Under [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html), classify
changes against the declared contract: incompatible public behavior is major,
backward-compatible functionality is minor, and backward-compatible bug fixes
are patch. An LOV label correction, new value or removed return value cannot
be classified from its edit type alone: assess promised display behavior,
accepted/returned values, consumer assumptions and existing stored data.

The subscription-specific concern is propagation and installed state. Analyse
how the exact master definition and consumer copy are captured/versioned, how
publish/refresh is controlled, and how source/artifact/installed-state checks
detect a stale copy or an unqualified update. A native subscription reference
or “up to date” status is not evidence of the project's semantic-version
compatibility. Resolve these within the existing dependency/validation analysis;
no separate subscription framework or runtime exercise is presumed necessary.

### AN-12 — Milestone tracking uses a different mechanism

Paper pages 9–11 present issue/milestone tracking alternatives; page 45 recommends
Team Development for the small-team path. BACKLOG, PLAN, the board and the
[E.1 bug record](../E.1/sprint_E.1_bugs.md) retain scope, scheduling and defects
under RUP. Classification: comparable planning purpose, different mechanism,
without evidence of the native issue journey. PBI-036 should record whether
that journey is demonstrated or intentionally excluded. Two competing trackers
are not required; no new product tracker or RUP replacement is proposed.

### AN-13 — Native authoring automation needs an explicit boundary

The inspected [24.2 API index](https://docs.oracle.com/en/database/oracle/apex/24.2/aeapi/toc.htm)
and [APEX_APPLICATION_ADMIN](https://docs.oracle.com/en/database/oracle/apex/24.2/aeapi/APEX_APPLICATION_ADMIN.html)
reference do not supply a Working Copy create/refresh/merge interface in their
listed routines. App Builder documents UI actions. This is a bounded search
result, not proof that every supported automation alternative is impossible.
Classification: unconfirmed operational interface and an FR-13 policy boundary.

The viable hypothesis is human native authoring/merge in DEV, then automated
capture, reviewed Git acceptance, reconstruction and artifact qualification.
Evaluate that workflow on its merits; do not use the earlier break-glass or
reservation rules as a veto. The authoring/automation boundary is also subject
to evidence-led policy reevaluation, rather than inherited by default from E.1.
The unresolved policy question is whether native merge/refresh are authoring
or must themselves be automated under FR-13. If strict automation includes
them, identify a supported path or retain an alternative Git integration
boundary. PBI-036/039/043 cover this. A browser test can repeat documented UI
actions without establishing a public unattended delivery API. Do not invoke
undocumented packages to manufacture conformance.

### AN-14 — Version-specific qualification matters

[SQLcl 25.3 release notes](https://www.oracle.com/tools/sqlcl/sqlcl-relnotes-25.3.0.html)
identify the pinned build, Java 17/21 requirements and fixes in export, staging
and diagnostics. Fixed bugs are reasons to verify the chosen version, not
evidence of a remaining defect. E.1's [installer](../../scripts/cicd-tools.sh)
pins Temurin Java 21; Oracle's supported runtime list names Oracle Java/GraalVM.
Functional lab evidence is not a vendor-support determination for that
distribution. Classification: qualification/support clarification, not an
observed technical blocker; use existing PBI-028/032 if a profile decision follows.

[25.3 filters](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/refining-exports-filters.html),
section 6.4, support scoped exports. Its export-type list and APEX example use
different singular/plural spellings. Resolve that detail against generated
client configuration and observed inventory, rather than invent a limitation.
The [25.3 concepts](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/introduction.html),
section 6.1, distinguish supported objects, snapshot/diff generation and specific
staging limitations; custom SQL remains available. Generated DDL does not prove
correct business-data migration or safe Foundation coexistence. Those remain
E.5 concerns after stabilization.

## Responsibility-level disposition

**Retain required outcomes:** accepted source identity, dependency completeness,
review, exact-artifact qualification/promotion, target identity, preserved user
data, observable failures and explicit repair decisions. Component compatibility
and availability obligations remain unless requirements change. Retaining an
outcome does not mandate retaining its E.1 implementation.

**Investigate native replacement:** shared export configuration, schema
snapshot/diff generation, changelog scaffolding, release-directory management
and archive generation/deployment. [PROJECT 25.3](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/project.html),
section 11.16, covers these responsibilities. Another general custom framework
would be unjustified where the native path meets the scoped contract. E.1's
archive inspector also enforces project-specific assertions; retain or relocate
those before accepting replacement. No complete custom mechanism is yet
experimentally proved unnecessary.

**Justify thin integration separately:** review/test binding, fail-stop pipeline
behavior, preservation assertions and relevant compatibility/drift/repair guards.
PROJECT verify does not establish all business and operating rules.
[Oracle COMMIT semantics](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqlrf/COMMIT.html)
include implicit DDL commits; replacing a controller does not make deployment
transactional. The [E.1 failure record](../E.1/tests/recovery_proof_20261018.txt)
shows why inspected partial state matters.

Similarly named APIs are not automatic replacements:
[GET_OFFSET](https://docs.oracle.com/en/database/oracle/apex/24.2/aeapi/GET_OFFSET-Function.html)
reads import package context, not an identified installed application's saved
offset; [GET_INFO](https://docs.oracle.com/en/database/oracle/apex/24.2/aeapi/GET_INFO-Function.html)
parses source install information. Neither reference alone justifies deleting
E.1's observed-target offset extraction. Compare native replacement against
saved-report/component identity evidence before deciding it is avoidable.

## Coverage of the Oracle paper

Pages 1–5 establish provenance and navigation. Architecture/source history
(6–9) maps to AN-01/05/11; issue planning (9–11) to AN-12; shared authoring,
conflicts and Working Copies (12–14) to AN-03/04/13; optional modularity
(7, 15–16) to AN-11; source control, capture and distribution (16–21) to
AN-01/02/14; logic testing, coverage and UI checks (22–26) to AN-06.

Release, deployment and environments (26–30) map to AN-02/05/08; native/external
audits (30–31) to AN-10; both collaboration models, branch instances, conflict
review and central DEV update (32–39) to AN-03/04/07/09/13. Central synchronization
is already PBI-042. The two pipeline journeys and archived results (40–45) map
to AN-07/14. Page 45 chooses different emphases for small and larger teams;
it does not require combining every mechanism in one workflow.

Cloud connections/bastions (46) are conditional and outside the loopback lab;
they create no local blocker. SQLcl's local database connection requirement is
relevant, with historical E.1 platform evidence rather than a fresh check.
Alternative exports (47) support AN-01. Paper snippets and older helper-script
names are examples, not verified lab entry points. Every recommendation family
has a disposition; coverage is not a claim of executed capability.

## Optional-tool compatibility hypotheses

The Product Owner's direction is to give developers flexibility through stable,
industry-standard tools and techniques. Compatibility and adoption are separate decisions:
PROJECT and Working Copies may remain optional alternatives. A compatible
repository must preserve an understandable route into a supported workflow;
it need not make every tool mandatory or promise cost-free switching. The
[review summary](sprint_E.2_inception.md#optional-tool-compatibility-hypotheses)
and [PROJECT fit assessment](project-fit-assessment.md#optional-use-and-repository-compatibility)
carry this distinction into the adoption decision. This is an evaluation aim,
not a claim that the current toolchain has already met it.

**H-1 — Optional PROJECT use is feasible without compromising the repository's
delivery contract.** Oracle documents initialization in an existing Git
repository, committed `.dbtools` configuration and `src`/`dist` conventions
([SQLcl 25.3, section 6.2](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/project-command.html)).
That supports feasibility investigation, but does not establish compatibility
with E.1's current layout or migration history. Compare a native PROJECT root
inside the repository with a documented adaptation, measuring extra generation,
review and maintenance work. Do not restructure the repository merely to
resemble an example.

EQ-2 must identify authoritative files, source scope, stable identities, Git
base/configuration, migration ownership and a verified initial baseline. From
the same accepted revision, demonstrate native export/stage/artifact/deploy
and a supported alternative entry path with equivalent required outcomes.
Require reviewable diffs, component/version metadata and retained history;
reject silent omissions, double application, parallel independently maintained
migration histories or manual copying as the routine bridge. Report whether
compatibility is direct, requires a bounded maintained adapter, or only supports
a one-time migration. An expensive or lossy adapter can disprove the hypothesis.
Optionality does not authorize two tools to write the same generated files
concurrently; any switch needs a clear ownership and baseline procedure.

**H-2 — Optional Working Copy authoring can feed the same accepted Git and
delivery contract.** Oracle describes an APEX application copy with compare,
refresh and merge operations, using original IDs for comparison
([APEX 24.2, section 5.9.1](https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/about-working-copies.html)).
Our inference is that compatibility concerns authoring, capture and restoration,
rather than a special Working Copy Git directory layout. The supplied paper's
team-checkpoint-to-Git flow (page 32) supports this hypothesis. It does not
establish a fully automated Working Copy management API.

EQ-1 must reconstruct Main from accepted Git, create a Working Copy, develop
and integrate a bounded change, capture the agreed Main checkpoint and rebuild
its accepted revision. Compare ordinary Main authoring through the same capture
contract. Check identity stability, schema dependencies, unintended inclusion
of private copies, stale edits, deletions and unsupported merge components.
Record explicit manual steps and developer usability. Loss of accepted intent,
uncontrolled private changes or an impractical recovery path can disprove fit.
Neither Main-first capture nor direct Working Copy export is declared the only
supported route before investigation; direct capture requires its own identity
and reconstruction evidence if proposed.

Evaluate H-1 and H-2 independently, then their combined path. Their tools act
at different layers, so failure of one does not establish failure of the other.
The current verdict is **plausible, unverified compatibility**. Record exact
supported versions and requalification needs; do not imply universal future
compatibility. Reconcile resulting recommendations through PBI-037/039 and
the existing source/pipeline items before proposing a new PBI. E.1 evidence,
E.5 upgrade allocation and managed exercise approval gates remain intact.

## Prioritized evidence questions for design

**EQ-1 — Native authoring to accepted Git source (AN-01/03/13).** Highest
priority: determine whether one Working Copy change plus a disjoint Main change
survives compare/refresh/merge, capture and reconstruction of a reviewed Git
revision. A lost change, unexplained identity difference or unavailable required
interface would change the recommendation. Retain source diffs, selected merge
decisions and reconstructed visible output. A bounded stale-page or deletion
case should expose the documented limitation and corrective procedure.
Include developer usability: clear Main/Working Copy identity, coordination
signals, understandable comparison and refresh/merge decisions, safe
abandonment, and the effort to recover and capture accepted changes. Separate
an observed usability problem from a policy preference inherited from E.1.

**EQ-2 — PROJECT authoring-to-delivery workflow (AN-01/02/03/05/07/08/14).**
Determine whether the native workflow is usable and reconstructible from initial
project adoption through a subsequent application/database change: author →
filtered export → reviewed source commit → stage against the declared Git base
→ reviewed distribution commit → integration → release/artifact → validation
and deployment. The [nine review questions](sprint_E.2_inception.md#questions-about-the-sqlcl-project-way-of-working)
make the actor decisions and unknowns explicit.

Evidence must distinguish development object definitions from staged deployment
changes, show the actual captured inventory and dependencies, and establish one
migration authority. Include the treatment of intentional data changes,
deletions and unsupported generation; a custom changeset is not automatically a
reason to abandon PROJECT. Relate Working Copy Main integration to coordinated
capture and keep unrelated/unaccepted work visible. For branch integration,
record the comparison base and how accepted source and staged changes are kept
consistent after it moves. Do not presume a successful text merge establishes
a valid installation.

The delivery slice must qualify the same native artifact on fresh/baseline
starts, preserve prior settings/history and supported identities, and repeat
safely in mapped targets. Distinguish PROJECT's structural verification from
business/browser tests and release admission. Inspect generated changes,
diagnostics and partial-failure behavior. Record developer/operator steps,
review effort, confusing decisions, reproducibility and remaining justified
custom responsibilities. An empty install or invocation of every command alone
does not establish the native way of working. Existing E.1 receipts are the
historical comparison, not fresh full-controller reproduction.

Explicitly validate [semantic-version and component dependency support](project-fit-assessment.md#pf-08--semantic-versioning-and-component-dependencies-require-validation):
version parsing/ordering versus labels, separate component identities and
declarations, pre-write acceptance/rejection of combinations, and consistency
between artifact declarations and observed installed versions. Distinguish
native/bundled support from configuration or a custom admission check. General
dependency resolution is not required by the bounded approved combinations;
complex Foundation upgrades are not needed to test metadata admission.

**EQ-3 — Feature-source identity (AN-09).** Compare the actual E.1 logical-area
capture contract with the paper's matched branch-instance requirement. Use
existing identity/export evidence first; select only the missing observation
needed to explain nonsemantic differences or demonstrate the matched approach.
Full PDB cloning, multi-developer concurrency and E.4 delivery are not automatic
E.2 scope. An explicitly accepted topology deviation remains a possible outcome.

**EQ-4 — Native deployment protections (AN-07/08).** Determine which guards are
native, need thin integration, or require a policy decision. Inspect generated
artifacts first; propose the smallest failed/stale-validation, drift or
committed-DDL observation that could change the recommendation. Failed validation
must stop downstream deployment. Preserve partial-state evidence. Do not copy
E.1's whole authority/control schema merely to make a native experiment pass.

**EQ-5 — Audit/test availability versus full delivery (AN-06/10).** Coverage,
browser and audit gaps are already identified; installing full test frameworks
is unnecessary merely to establish those missing outcomes. If a recommendation
depends on local native audit behavior, choose one controlled finding and its
corrected result. Full suites, measured coverage improvement and operating
pipelines remain E.3/E.4 outcomes.

Each proposed exercise must identify the decision it could change, existing
evidence, smallest discriminating observation, preservation boundary and stop
condition. Omit runtime exercises when documentation/source settles the finding.
The earlier X1–X3 draft must be reassessed against EQ-1–5, not treated as selected
work. No retained-environment rebuild is justified just to make analysis appear
reproducible. Current runtime readiness will be an approved exercise prerequisite.

## Feasibility, risks and readiness

Desk analysis is feasible from the available code and references. Focused
runtime evidence is conditional on verified tool versions, supported interfaces,
owned disposable resources and managed design approval. Complexity is moderate
to high because comparison spans multiple responsibilities and existing policy
requirements; no measured engineering-cost estimate is available.

Principal risks are premature selection of a replacement toolchain, confusing
policy with product limits, overclaiming historical evidence, designing a full
later sprint as an E.2 experiment, and losing retained state during repetition.
The full registered E.1 release test deliberately reports unfinished acceptance;
it is a known verification constraint to analyze rather than silently narrow.

No genuine technology blocker is established. Documented Working Copy
limitations, the different branch topology, missing tests and unconfirmed
automation are distinct findings. A blocker assertion requires the exact
supported-version constraint or reproducible failure, impact, attempted
alternatives and why the relevant requirement cannot be met. Optional cloud
or external services and unknown performance must not become blocker claims.

There is enough evidence to derive a focused design after analysis review.
Runtime questions are identified rather than hidden in a blanket feasibility
claim. The implementor remains responsible for the technical recommendation;
the Product Owner need not choose implementation details on the implementor's
behalf. Permanent policy changes and later sprint changes require decisions
after evidence exists.

## Backlog reconciliation and dependency direction

AN-01/02/05/09/14 map to PBI-020/035/037/038 and configuration PBI-027.
Native team authoring/policy differences map to PBI-036/039 with PBI-018/019.
AN-06/10 map to PBI-034/040/041. AN-07 maps to PBI-030/031/042/043. AN-08 and
EQ-4 map to PBI-021/022/023/024/045. Mini-app reuse is PBI-044; comparative
evidence/reproduction is PBI-046/047, with the operating guide in PBI-017.
PBI-025/026/028/032/033 remain conditional on selected access, hosting, version,
distribution and platform profiles. These reference existing outcomes without
changing assignment or claiming later work complete.

PBI-052 is the Product Owner-requested follow-up for explicit component-contract
and version-classification rules. No other new PBI is currently justified.
Working Copy/Git compatibility,
native packaging, source identity, audits and central DEV synchronization are
already covered. Their existing descriptions can absorb evidence-led acceptance
clarifications through managed refinement. If execution reveals a genuinely
uncovered outcome, propose its finding, value and test before backlog promotion.

The dependency direction is: resolve source-acceptance/policy and identity
boundaries → establish native capture/staging and reconstructible initial
release → prove compatible Hello delivery, repeat/data preservation and relevant
safety/validation → integrate tests/audits and both pipeline journeys → compare
team-centric and feature-centric work including safe central DEV synchronization
→ accept the stabilized toolchain → complex Foundation upgrades in E.5.
PBI-036/037/038 precede PBI-043; PBI-042 needs a reconstructed accepted artifact
and a safe authoring boundary. This informs the existing E.3/E.4 order without
editing their scope/status. PBI-048–050 remain assigned to E.5.

## Analysis review and next phase

The analyst deliverable identifies the problem, actors, complete journey
outcomes, inspected implementation, version constraints, recommendation
coverage, classified findings, dependencies and evidence questions. The
[analysis summary](sprint_E.2_inception.md) is the review entry point.
The [PROJECT fit register](project-fit-assessment.md) separately distinguishes
documentation/source validation from configuration/integration needs and
pending runtime proofs for each applicable requirement.
Analysis has now been explicitly accepted; the revised design is Proposed. PBI-051
remains unfinished until approved exercises, final findings/roadmap and the
reproducible live handover satisfy its criterion. No construction, skeleton,
permanent policy change or implementation approval is claimed here.
