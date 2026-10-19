# E.2 — Analysis review

Analysis approved by the Product Owner on 2026-10-19; revised exercise design
and test specification are Proposed. PBI-051 remains unfinished.
The [full analysis](sprint_E.2_analysis.md) owns the conclusions, exact source
links, actor/use-case relationships, existing-PBI reconciliation and evidence
questions. [Setup](sprint_E.2_setup.md) owns contracting. The
[board](../../PROGRESS_BOARD.md) records E.2/PBI-051 and its proposed children
under_design; [PLAN](../../PLAN.md) keeps the sprint active/managed.

## Goal of the gap analysis

**Give developers flexibility through stable, industry-standard tools and techniques.**

Assess which supported combinations let developers author, review, test and
deliver changes safely with understandable effort. The preferred direction is
coexistence of PROJECT, Working Copies and useful E.1 capabilities, where
evidence supports it. Identify the common contracts that make these choices
practical, the boundaries that prevent conflicting authorities and the custom
mechanisms that can be simplified. Retaining every E.1 mechanism is not an
acceptance condition; replacing E.1 wholesale is not the analysis objective.

The [full analysis](sprint_E.2_analysis.md#goals-and-further-coexistence-opportunities)
explains two further opportunities: generated and explicit migrations;
and combined testing/compatibility/release checks.
They are supported patterns or hypotheses,
not two newly approved implementations. Assess representative journeys and
their costs rather than promise every possible combination.

Topology flexibility is already covered; retain the documented qualification
questions without proposing another flexibility workstream. Validation analysis
must combine utPLSQL, E.1 assertions, semantic-version and component dependency
checks, audits and browser tests around the same candidate, explaining what each
proves, when it runs and how failures block delivery. APEX subscriptions are an
optional master/copy mechanism for specified shared components across applications
in one workspace; [AN-11](sprint_E.2_analysis.md#an-11--mini-apps-are-optional-modularity)
explains their scope. Treat subscribed/shared LOVs as part of the component's
declared interface where consumers depend on them, with changes classified
under its major/minor/patch compatibility contract. Subscription propagation
and stale copies are specific dependency-state concerns, not a separate
coexistence workstream or an assumed component release/version manager.

Pipelines are the intended delivery destination. Local commands support
development, focused exercises and reproducibility. Comparing local execution
with hosted CI is not a current coexistence objective; pipeline suitability
remains relevant to tool recommendations, with full delivery allocated through
the existing backlog.

## Component-contract criticality decision

E.1's component/version/dependency manifest and selected-combination checks
are a valid bounded starting point. Elaboration must establish that proposed
tool choices preserve that declaration in source/artifacts, reject unsupported
combinations and reconcile installed state. It need not infer compatibility
from arbitrary code changes or introduce a general dependency resolver.

The [criticality decision](sprint_E.2_analysis.md#elaboration-criticality-decision--component-contracts)
separates essential evidence from later delivery. Broad consumer-test suites
remain with existing test items; actual compatible/breaking evolution remains
in E.5. Subscription propagation remains within PBI-044, becoming an E.2
exercise obligation only if the selected recommendation depends on it.
Automatic semantic change classification is a deferred, unregistered
enhancement direction, not a present acceptance requirement. Existing items
cover required delivery work. The subsequently requested
[PBI-052](../../BACKLOG.md#pbi-052-define-semantic-versioning-rules-for-component-contracts)
defines component contracts and major/minor/patch classification rules. It is
Proposed and unscheduled, separate from automatic inference and E.5 upgrade
delivery, and adds no E.2 completion gate.

## Conclusions for review

E.1 combines supported Oracle export/import and Liquibase primitives with
custom orchestration. Lower-level exports are a documented alternative, so
absence of PROJECT alone is not nonconformance. E.2 must assess Oracle SQLcl
PROJECT as a way of developing and delivering changes: authoring in APEX/the
database, exporting project sources, staging reviewed distribution changes,
integrating through Git and producing deployable releases. Assess the native
workflow itself before deciding which E.1 mechanisms it replaces or still needs.
Its availability does not prove E.1's validation, identity, preservation or
repair contracts.

Working Copies can conceptually precede Git acceptance; the paper explicitly
describes team checkpoints exported to Git. Break-glass-only authoring and
component-wide reservations were E.1-stage policies. E.2 must reevaluate the
usability of Working Copies for ordinary development, including coordination,
comparison, refresh, merge, abandonment and capture into the Git pipeline.
Keep periodic team checkpoints within this assessment: integrate into Main,
export the agreed team state and commit it to Git. This appears compatible
with E.1's capture-to-Git approach; completeness, attribution and reconstruction
still need evidence. It is not a separate feature or coexistence workstream.
Those earlier policies do not predetermine the result or constrain the target
approach. Native page locks have a different scope; assess their practical
adequacy against the developer journey and observed risks.

The feature-centric branch-instance approach is a separate issue: page 34
requires matching workspace name/ID and APEX patch level. E.1's distinct
workspaces in one PDB do not demonstrate that contract. Existing identity
evidence is useful but narrower. Capture noise, reconstruction and any proposed
topology deviation need explicit evidence and disposition.

PL/SQL coverage, automated browser checks, native audits, hosted pipeline
operation and central DEV synchronization remain implementation/evidence gaps
already covered by existing PBIs. Mini apps are an optional modularity pattern,
not an implicit replacement for logical component versioning or Foundation
coexistence. Cloud-specific connection constraints do not block this local lab.

No genuine technology blocker is established and no entire custom mechanism
is yet proved unnecessary by execution. The analysis separates documented
limits, source differences, policy conflicts and untested hypotheses. All
fourteen findings have an existing backlog destination. PBI-052 additionally
records the requested component-contract/version-classification definition.
No later item is reassigned or marked complete.

## Optional-tool compatibility hypotheses

Guiding principle: **Give developers flexibility through stable,
industry-standard tools and techniques.** PROJECT adoption and Working Copy adoption are
optional decisions to assess separately from compatibility. The
[full analysis](sprint_E.2_analysis.md#optional-tool-compatibility-hypotheses)
owns H-1/H-2, their source evidence and falsification criteria.

For PROJECT, test whether a native project root or a bounded adaptation can
coexist with the repository's source, component metadata and migration contract
without duplicate authorities or routine manual copying. For Working Copies,
test the authoring → Main checkpoint → Git → reconstructed application journey;
this is an APEX workflow compatibility question rather than a folder convention.
Then assess their combined use and the developer effort of switching routes.

Desk evidence makes both hypotheses plausible. Current repository compatibility
and practical usability remain unverified. No repository layout, mandatory tool
or exercise implementation is approved by this refinement.

## Evidence needed next

### PROJECT fit decision

The primary question is **whether PROJECT is the proper tool for our
requirements**, not whether we can execute its subcommands. The
[requirements-fit assessment](project-fit-assessment.md) enumerates twelve
possible design assumptions, weaknesses/boundaries and validation obligations:

1. Object snapshots do not by themselves establish business-change intent.
2. Export scope and a coherent team checkpoint need explicit control.
3. The Git comparison base, source and staged distribution must remain aligned.
4. Generated DDL needs qualification against populated targets.
5. Automatic generation has version-specific object/change limitations.
6. Existing-target baseline adoption needs proof before migration-history sync.
7. Target mapping must also preserve supported application/component identity.
8. Semantic-version handling and component dependency enforcement need explicit
   validation; release labels and migration ordering are insufficient evidence.
9. Migration tracking alone does not establish drift, fencing or safe repair.
10. Project verification does not replace application acceptance tests.
11. Archive generation does not establish accepted-source/validation provenance.
12. Native operation must be usable, reproducible and worth its integration cost.

Each entry names its evidence, affected FR/NFR requirements, validation needed
and provisional fit verdict. Possible designer assumptions are explicitly
inferences, not attributed intentions. The supplied
[Pretius article](https://pretius.com/pl/blog/project-oracle-sqlcl) is a useful
24.3.2 worked example; official 25.3 documentation controls the current technical
assessment. A tutorial's successful workflow does not establish our fit.

Current verdict: conditional fit for the source/distribution/release core,
with configuration, testing and justified integration still required. Adoption
is unvalidated; there is no automatic preference based on Oracle branding or
CLI breadth. Compare native adoption, adoption with supplements and the
lower-level Oracle approach under the same requirements. Do not relax those
requirements solely to accommodate PROJECT. E.1-stage policies remain open
to the reevaluation already directed by the Product Owner.

### Questions about the SQLcl PROJECT way of working

1. **Authoring and source authority:** Can developers work naturally in APEX
   and the database, then use PROJECT to capture, review and accept changes in
   Git? Which E.1 assumptions about manually authored migrations or early
   component reservations should change for that workflow?
2. **Project scope and initial adoption:** How do we establish a PROJECT
   baseline from E.1, and configure capture of the intended Main application,
   schema objects and dependencies while excluding Working Copies, lab controls,
   test fixtures, credentials and runtime business data?
3. **Export and stage:** What do developers review and commit after `project
   export` and `project stage`? Are generated changes complete, understandable
   and correctly ordered, and how are intentional data changes, deletions and
   unsupported changes represented without a second migration authority?
4. **Git integration:** How does PROJECT staging work for coordinated team
   checkpoints and for feature branches? Which comparison base is authoritative,
   and what must be refreshed or regenerated when the branch or integration
   baseline changes before acceptance?
5. **Working Copies:** When a Working Copy is merged into Main, how does its
   application change and any related database change enter the PROJECT/Git
   workflow consistently? Who coordinates capture, and how do we avoid admitting
   unrelated or unfinished team changes?
6. **Qualification and delivery:** Can `project release`, `project gen-artifact`
   and `project deploy` supply the initial and compatible Hello releases with
   reviewed source identity, mapped targets, the same qualified artifact,
   preserved user data and safe repeat deployment?
7. **Validation and failures:** What does `project verify` establish, what still
   needs application tests or pipeline gates, and how are failed staging,
   installation or partially committed changes detected and handled?
8. **Usability and simplification:** Is the native PROJECT workflow practical
   and reproducible for our developers and operator? What effort, confusing
   steps and justified custom controls remain compared with E.1, without
   recreating E.1's custom framework around PROJECT?
9. **Semantic versions and component dependencies:** does PROJECT interpret
   semantic versions and support separately versioned Foundation/Hello/World
   components with declared compatibility? Can it accept a supported combination
   and reject incompatible, unknown or inconsistent combinations before
   deployment writes? Which behavior is native, bundled, configured or custom?
   The [PF-08 validation](project-fit-assessment.md#pf-08--semantic-versioning-and-component-dependencies-require-validation)
   distinguishes version labels, migration ordering and semantic dependency
   enforcement without assuming support or incompatibility.

These are analysis questions to investigate, not implementation choices the
Product Owner must supply. [EQ-2 in the full analysis](sprint_E.2_analysis.md#prioritized-evidence-questions-for-design)
owns their evidence boundary and connections to the other questions. Evaluate
the native workflow before accepting or rejecting it; use focused exercises
for the unresolved parts and preserve E.1 as the historical comparison.

### Selecting focused evidence

Design should derive the smallest discriminating observations for: native
PROJECT authoring/capture/staging → accepted Git source → reconstruction;
native release on fresh,
compatible-upgrade and repeat starts with preserved data/identities; the
branch-source identity deviation; safety/validation gaps around native deploy;
and any locally uncertain native audit capability. The full test frameworks,
collaboration environments and pipeline products remain later implementation
outcomes. These questions replace the earlier broad exercise selection as the
input to design.

The dependency direction is source/policy/identity → native capture and initial
release → compatible delivery/preservation/safety → tests, audits and pipelines
→ collaboration comparison and safe central DEV synchronization → stabilized
toolchain acceptance → Foundation upgrades in E.5. PBI-048–050 stay in E.5.

## Review boundary and verification

External analysis review round 1 is complete: the
[original expert report](sprint_E.2_analysis_review-1.md) reviews published commit
`cb766e5f6a3bd3a06454afb62fae275cb27c1e8d`, raises no findings and concludes
ready for exercise design. The [engineering response](sprint_E.2_analysis_review-1-response.md)
assesses that verdict and its limits; the
[interim assessment](sprint_E.2_assessment.md) records round closure and the
remaining gates. No additional feedback exchange is needed. This does not
approve exercise implementation, establish runtime compatibility or close E.2.

The Product Owner subsequently approved analysis and directed design. The
[revised exercise design](sprint_E.2_design.md) is awaiting its own approval.
No exercise or test skeleton was
implemented. No database/app mutation, full regression, live demonstration or
completion commit is claimed. Source inspection and historical evidence are
distinguished from fresh execution; measured savings and current runtime
readiness remain unknown. Phase token counts are unavailable.

The [source inventory](tests/analysis_sources_20261019.json) records inspected
input hashes and Oracle URLs. The
[analysis checks](tests/analysis_review_checks_20261019.txt) record local-link,
anchor, status, preservation and whitespace verification. The
[audit](sprint_E.2_documentation_audit.md) records the current phase and remaining
dependencies. The analyst recommends proceeding to evidence-led design after
review of this baseline; it is not an implementation approval request.
