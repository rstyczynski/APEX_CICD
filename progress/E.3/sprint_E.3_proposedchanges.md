# E.3 APEX-native team-centric lifecycle: backlog review and exercise plan

## Decision and status

This planned exercise was renumbered from E.2 to E.3 on 2026-10-19 when
the Product Owner inserted an additional Elaboration iteration. The
[E.2 gap analysis](../E.2/sprint_E.2_proposedchanges.md) now assesses E.1 and
informs later refinement; [complex upgrades](../E.5/sprint_E.5_proposedchanges.md)
are deferred to E.5 after toolchain stabilization.
References in this scope record use the new numbering; assignments and
acceptance criteria remain unchanged by the renumbering.

On 2026-10-19 the Product Owner requested an Oracle-style repeat of the delivered
scenarios, extended by the supplied paper, then split the exercise into E.3
and E.4. E.3 owns the native-APEX path and common foundation; E.4 owns the
Git-based path and final comparison. E.3 is **Planned**, in managed
mode. This is the explicitly requested pre-sprint planning artifact, not a
setup/design approval, execution record or claim that any new test passed.
No application, database, runner or infrastructure is changed by this plan.

The [Product Backlog](../../BACKLOG.md) owns item definitions and priority;
the [Sprint Plan](../../PLAN.md#sprint-e3---validate-apex-native-team-centric-development)
owns assignments and lifecycle status; the [progress board](../../PROGRESS_BOARD.md)
contains the assigned Planned rows. The [SRS](../../docs/srs.md) owns current
actor goals and acceptance requirements. The [architecture](../../docs/architecture.md)
and [test profile](../../docs/test-profile.md) retain the E.1 baseline pending
E.3 refinement. The [research](../../docs/cicd-research.md) records the earlier
tooling choice; the [roadmap](../../ROADMAP.md) places E.3 in Elaboration.
The [E.1 assessment](../E.1/sprint_E.1_assessment.md) and
[clean-checkout evidence](../E.1/tests/clean_checkout_20261018.txt) define
what E.1 actually demonstrated, rather than what its full specification hoped
to demonstrate. The [README](../../README.md) remains the project orientation.

## Split decision and assignment ownership — 2026-10-19

The Product Owner subsequently requested separate E.3 and E.4 iterations.
E.3 now owns APEX-native team-centric development: page locks, Working Copies,
APEX Main integration and coordinated team exports into Git. E.4 owns the
[Git-based feature-centric exercise](../E.4/sprint_E.4_proposedchanges.md):
private branch environments, feature branches, PR review, Git conflict
integration and post-merge central DEV synchronization. Both remain Planned.
APEX Main and Git main are separate integration points; neither merge
implicitly performs the other. No native-only claim removes Git from release
history or source-controlled distribution files.

E.3 retains PBI-036/037/035/039/040/034/041/027/038/021/029/045/044/043
and adds PBI-047 for the mandatory E.1 comparison (15 items). PBI-019/020/042/017/046 move to E.4 (five items), without changed
backlog definitions or duplicate assignments. E.3 owns the native release,
quality and two-pipeline foundation; E.4 reuses it and records fresh regression
for feature-integrated artifacts. PBI-036 defines the coverage of both paths,
while each sprint accepts only its own assigned outcomes. PBI-017's final
consolidated guide and PBI-046's full comparison/reproduction complete in E.4;
E.3 delivers its own runnable operating instructions, reproduction, E.1
comparison and live-review evidence under the sprint's handover requirements.

The full paper coverage below is retained as context. Feature-centric sections
and final cross-approach comparison are E.4 scope, not E.3 exit criteria.
The original planning validation at the end describes the pre-split snapshot.

## Strict Oracle traceability and comparison contract

The Product Owner made this a strict acceptance requirement on 2026-10-19
for both E.3 and E.4. Oracle-style means demonstrated alignment with the
supplied paper and applicable official Oracle documentation, not merely use
of an Oracle command or the absence of custom scripts. This contract applies
to every assigned item, actor journey, material alternative/failure flow,
inherited capability and handover claim in each sprint. PBI-036 establishes
the common map; each sprint maintains and validates its own evidence against
it. Unmapped or unsupported claims block the affected acceptance decision.

Before implementation, create a traceability record for every scenario with
its stable scenario/use-case ID, actor and goal, PBI/sprint owner, exact paper
page and section, official Oracle documentation URL and section, documented
product version, selected runtime/tool version and planned acceptance test.
Read and verify the cited guidance; a generic documentation landing page or
search snippet is insufficient. Record the reference revision/access date
and resolve differences between the paper's APEX 24.2/SQLcl 25.1.1 examples
and the selected executable versions. Third-party tool documentation can
explain usage but cannot substitute for evidence of Oracle's recommendation.

Maintain the reverse view from every paper workflow to its owning scenario,
sprint and acceptance evidence, including cross-sprint dependencies, optional
examples and explicit exclusions. A project-specific scenario absent from
the paper must be marked as an extension, state that there is no direct paper
equivalent, and map each underlying Oracle operation to its official contract.
Do not fabricate a paper recommendation for stronger ownership, compatibility
or recovery policies. An excluded cloud or optional commercial-tool example
must be visible in the map with its approved scope disposition; exclusion
is never a passing execution result.

After execution, extend each record with source commit, artifact identity,
actual target/tool versions, test/run IDs, expected and observed outcomes,
links to retained logs/reports and relevant browser or manual observations.
Separate document conformity, execution success and complete use-case
acceptance. Record supported, partial, failed, unrun or excluded outcomes
with the actual denominator so a high-level coverage statement is auditable.
E.4 must recheck inherited evidence against its changed inputs and versions;
E.3's pass does not automatically qualify a new feature-integrated artifact.

Use the documented native path first. A deviation record must identify the
Oracle guidance, reproducible limitation, affected scenario, proposed
alternative and its tradeoff and receive an explicit Product Owner disposition
before the deviation is treated as accepted. Recording an assumption or a
preference for custom code does not establish a limitation. Material conflicts
with existing SRS criteria remain managed requirement decisions, not silent
relaxations for the sake of claiming native-tool coverage.

### Required E.1 comparison at each handover

[PBI-047](../../BACKLOG.md#pbi-047-compare-apex-native-delivery-with-the-earlier-prototype)
owns the E.3-versus-E.1 evidence package. E.3 cannot defer that comparison to
E.4. [PBI-046](../../BACKLOG.md#pbi-046-compare-and-independently-reproduce-the-oracle-style-laboratory)
owns E.4-versus-E.1 and the final three-approach comparison, incorporating
E.3 evidence with its provenance and applicability stated.

Before running comparisons, define matched scenario inputs, starting states,
expected behaviors, data-preservation checks, version/resource conditions and
the measurement method. Include initial assembly/release, compatible upgrade,
incompatible proposal, drift and bounded committed-DDL repair from E.1's
demonstrated A–I outcomes, plus the newly covered Oracle journeys. Show new
capabilities separately from common-scenario parity; an unimplemented E.1
workflow is not an invented failed run. Preserve E.1 historical artifacts and
identify their exact source/date. If fresh E.1 measurements are necessary,
replay the identified baseline in an isolated fixture and label the new run
without rewriting historical sprint results.

For each approach, compare use-case and Oracle-guidance coverage, actual
success/failure and preservation results, concurrency/isolation/conflict
behavior, provenance and repeatability, setup effort, operator actions and
manual interventions, elapsed runtimes, resource use and custom maintenance
responsibilities. State units, trial counts and coverage denominators; identify
changed conditions and noncomparable measurements. Historical missing values
remain unavailable unless newly measured. Neither more scripts nor fewer
scripts alone establish a better outcome.

Each sprint ends with a readable comparison report and its walkthrough/slides,
linked to reproducible evidence rather than raw logs alone. Explain material
benefits, regressions, limitations, remaining risks and custom extensions.
Present options and an evidence-supported recommendation against the agreed
decision criteria, including the option to run another experiment when evidence
is insufficient. Record the Product Owner's actual decision or explicit
deferral; never infer the preferred approach from tool choice, silence or
sprint closure. The E.4 package supports selection among E.1 custom delivery,
E.3 APEX-native team-centric and E.4 Git-based feature-centric development.

Design approval requires the complete applicable source map and comparison
protocol. Handover acceptance requires the executed evidence map, deviation
dispositions and the sprint's E.1 comparison package. Missing evidence remains
an open criterion even if individual functional tests pass. These gates do
not change either sprint from Planned or assert that the final approach has
already been selected.

## Source and meaning of Oracle-style

The source is [Understanding the Oracle APEX Application Development Lifecycle](../../refs/apex-lifecycle-management-v3.pdf),
June 2025, version 3.2, 47 pages. Page references here are PDF page numbers.
Its validated examples use APEX 24.2 and SQLcl 25.1.1; the existing lab uses
SQLcl 25.3. E.3 setup must select and record exact compatible tool versions,
checksums, API/command differences and the resource budget before execution.
Do not assume that a later version or E.1's configuration passes this exercise.

Use the native SQLcl PROJECT lifecycle for source export, distribution staging,
release creation, artifact generation and deployment. Use APEX page locking
and Working Copies for E.3’s team-centric path. E.4 separately validates Git
feature branches with private APEX branch environments. Use utPLSQL
for database tests and measured coverage, Cypress for browser regression,
and the built-in Advisor and SQLcl code scanning for the core audit exercise.
Jenkins is the planning default for the paper's two automation pipelines;
another paper-listed runner requires an explicit design rationale and the
same evidence. Local prototype execution is preferred; remote publication,
runner registration and repository changes are separate external actions.

The paper allows alternative scripts and lower-level interfaces (pp. 45, 47).
That permission does not justify carrying the custom E.1 packager into the
new native path. Thin scripts may expose native operations, add checks and
retain evidence. They must not recreate a competing release format, migration
ledger or installer. Authored data transformations belong in supported custom
changesets. The [SQLcl 25.3 PROJECT reference](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/project.html)
documents these lifecycle commands and custom staging; the
[PROJECT introduction](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/introduction.html)
explains supported export/staging objects. A suspected native limitation must
be reproduced and recorded before a replacement mechanism is proposed.

## Existing backlog review and reuse

[PBI-017](../../BACKLOG.md#pbi-017-deliver-a-repository-and-pipeline-reference-guide)
already owns the consolidated reference guide. Schedule it in E.4 for the consolidated Oracle
reference rather than creating a second documentation item. Keep E.1 operating
guidance as historical, version-specific evidence.

[PBI-019](../../BACKLOG.md#pbi-019-prove-parallel-component-collaboration-and-integration),
[PBI-020](../../BACKLOG.md#pbi-020-complete-apex-capture-and-reconstruction-validation)
and [PBI-035](../../BACKLOG.md#pbi-035-validate-adoption-of-an-existing-apex-application)
already cover genuine parallel integration, stable capture/reconstruction and
existing-application adoption. PBI-019/020 are assigned to E.4 and PBI-035
to E.3; use native tools to satisfy their existing observable criteria. Identity normalization, deletion, shared
source conflicts, dependencies and supported saved-user state remain real
tests, not assumptions established by choosing PROJECT.

[PBI-021](../../BACKLOG.md#pbi-021-complete-release-admission-and-promotion-negative-coverage),
[PBI-027](../../BACKLOG.md#pbi-027-unify-delivery-environment-configuration)
and [PBI-029](../../BACKLOG.md#pbi-029-strengthen-automation-failure-diagnostics)
already cover invalid promotion, consistent target mappings and dependable
failure outcomes. Schedule them around native artifacts and execution;
do not add duplicate native-only definitions. Environment banners extend the
operating exercise without weakening mapping checks.

[PBI-034](../../BACKLOG.md#pbi-034-automate-application-browser-acceptance-checks)
already owns browser acceptance. Schedule it using Cypress, including a
controlled broken behavior that the browser suite detects. SQL/API fixtures
must not stand in for browser evidence.

The earlier full acceptance scope remains recorded under PBI-011–016 in E.1.
Do not reopen or rewrite that sprint. E.3's new baseline and comparison items
must reconcile its findings with those unfinished outcomes rather than claim
their retrospective completion.

## Missing outcomes added to the backlog

[PBI-036](../../BACKLOG.md#pbi-036-define-oracle-lifecycle-use-case-coverage)
owns actor-led coverage refinement, including QA/test-author and automation
operator responsibilities. It must model the paper's additional goals at
appropriate depth, preserve UC-1–12 identity and explain altered alternatives.

[PBI-037](../../BACKLOG.md#pbi-037-establish-native-oracle-source-capture-and-staging)
and [PBI-038](../../BACKLOG.md#pbi-038-deliver-native-oracle-release-artifacts)
fill the native source/staging and release/deployment gaps. They complement
the existing capture and promotion negative tests rather than replace them.

[PBI-039](../../BACKLOG.md#pbi-039-demonstrate-native-team-centric-apex-collaboration)
adds the missing ordinary shared-DEV journey with page locks and Working
Copies. [PBI-042](../../BACKLOG.md#pbi-042-synchronize-central-development-after-accepted-merges)
adds explicit post-merge central DEV synchronization.

[PBI-040](../../BACKLOG.md#pbi-040-measure-plsql-regression-coverage-with-utplsql)
adds measured database regression coverage and test improvement.
[PBI-041](../../BACKLOG.md#pbi-041-demonstrate-oracle-recommended-application-quality-audits)
adds repeatable audit, finding investigation and correction.
[PBI-043](../../BACKLOG.md#pbi-043-operate-the-oracle-lifecycle-automation-pipelines)
adds both operational pipelines and archived artifacts/results, which are
broader than PBI-030's hosted database-independent source checks.

[PBI-044](../../BACKLOG.md#pbi-044-demonstrate-native-mini-app-component-reuse)
adds a bounded optional-pattern demonstration of native subscriptions and
shared authentication. It is scheduled; the architecture pattern is optional
for the main greeting application, not optional acceptance of this item.

[PBI-045](../../BACKLOG.md#pbi-045-preserve-scenario-protections-around-native-oracle-delivery)
owns re-proving the three demonstrated E.1 protection scenarios around native
delivery. [PBI-046](../../BACKLOG.md#pbi-046-compare-and-independently-reproduce-the-oracle-style-laboratory)
owns the independent reproduction, comparison and architecture recommendation.

## Exercise coverage and acceptance evidence

### Planning and source adoption — paper pp. 9–11, 16–21

PBI-036/035/037 cover UC-8/12 and the source-control portions of UC-10.
Create an issue and milestone using native APEX Team Development for the
small-team exercise, assign and complete a change, and trace it to source
history. Demonstrate native project configuration/filters, initial application
and schema capture, a subsequent change, distribution staging and review.
Reconstruct an adopted application in a controlled empty target; missing
dependencies, inconsistent capture or unsafe populated-target adoption block
acceptance. Inspect a historical revision and explain a source difference.

### Shared team development — paper pp. 12–14, 32

PBI-039 covers the native alternative to UC-9/10 and its coordination goal.
Two developer identities must observe page lock ownership and blocked editing.
Create a Working Copy, compare it, pick up a nonconflicting Main change,
complete a fix, merge it and verify Main. Discard a separate experiment and
verify no unintended Main change. Explain that Working Copies isolate APEX
definitions, not the parsing schema's business data or database changes.

### Feature-centric development — paper pp. 32–39

This section is assigned to E.4 under PBI-019/020/042, reusing the
PBI-037 capture foundation from E.3. It covers UC-7/8/9/10/11. B and C make actual overlapping-in-time
Hello and World contributions on independent feature branches/private areas.
Update a feature with newer main changes, resolve a controlled shared-source
conflict, run the combined checks, address peer feedback and integrate both
intentions. Update central DEV from accepted source, preserving uncaptured
work. A sequential snapshot replay does not pass parallel collaboration.

The paper's branch-instance setup requires matching workspace name/ID and
APEX patch level (p. 34). E.1's distinct workspaces in one instance are not
automatically equivalent. Design must validate a resource-bounded arrangement
of matching branch environments, or present a measured limitation and seek a
scope decision before substituting a topology. Simultaneous tests require
simultaneous resources; sequential allocation cannot prove concurrency.

### Logic, browser and quality checks — paper pp. 22–26, 30–31

PBI-040/034/041 cover the testing gaps around UC-2/3/7/10/11. Author and run
utPLSQL tests for greeting validation, composition and immutable history;
retain machine-readable results and an HTML coverage report. State included
program units and covered/total executable lines, show an uncovered path,
add a test and compare measured coverage. A test count is not code coverage.

Cypress must exercise supported user roles, invalid input, escaping, greeting
submission, history navigation and behavior before/after upgrade. Include
at least one deliberately broken behavior caught by the suite. Run Advisor,
export embedded SQL/JavaScript and execute SQLcl code scanning on a controlled
finding; preserve audit results, triage and correction evidence. Evaluate
SonarQube/ApexSec applicability and document any license/access limitation;
an evaluation is not an executed third-party scan. These optional products
must not be reported as passed when unavailable.

### Release, deployment and environments — paper pp. 26–30, 39

PBI-027/038/021/029 cover UC-1/4/11. Reproduce Foundation-first assembly,
complete initial release, same-artifact integration-to-UAT promotion and
Hello 1.0.1 upgrade with Foundation/World unchanged. Use project release,
gen-artifact and deploy on reviewed distribution files; enforce accepted-main
provenance and record source, tool versions, artifact hash and target outcome.
Validate empty and supported upgrade starts, safe repeat, rejected wrong
targets, altered artifacts, stale/missing validation and surfaced client/server
failure. Check every prior history/configuration field rather than row counts
alone. No developer runtime business data travels in the release.

Show separate development, validation and retained UAT roles with distinct
environment banners. Explain same-instance target mapping and the paper's
separate-instance alternative. Production deployment is an explained analogue,
not evidence of operating a production service.

### E.1 protections through native delivery — UC-5 and A–I parity

PBI-045 preserves known incompatible Foundation proposal rejection before
writes, unexpected Page Designer drift capture/rejection with explicit
restoration or reviewed reconciliation, and failure after committed additive
DDL followed by inspected forward repair. Use separately reviewed native
artifacts for changed repair code, retain failed/successful history and prior
business data, reject an observation changed after inspection, and prove an
unchanged repair repeat makes no new changes. The ordinary runtime remains
restricted during the demonstrated partial failure. Map each check to native
capability or a justified thin extension; do not present these extra policies
as capabilities supplied by the paper.

### Mini-app reuse — paper pp. 15–16

PBI-044 demonstrates a common/library application and two minimal consuming
applications. Show subscription to a common component, deliberate publish
and individual refresh behavior, plus single-login navigation using native
session sharing. Explain the optional separate-schema pattern and its grants.
Keep this teaching fixture distinct from Foundation/Hello/World page-group
version labels. This is not an instruction to split the main application.

### Automation and reproduction — paper pp. 40–44

PBI-043 in E.3 establishes automation around UC-4/6/7/11.
PBI-017/046 in E.4 consolidate the guide and cross-approach reproduction. Execute an on-demand
export/stage/reviewed-merge/release/artifact journey and a build/deploy-to-test/
utPLSQL/Cypress/qualified-deployment journey. Preserve the review boundary
instead of allowing automation to bypass it. Show trigger identity, checkout
revision, credentials boundary, failure gating, run logs, downloadable artifact,
test reports and coverage. Local triggers are acceptable for the prototype
if their actual invocation is explicit; document a repository-event trigger
as unproved unless exercised. Stop promotion after a controlled test failure.

For E.3 handover, an independent clean checkout must execute its team-centric
and common native-release scenarios with new
target state and credentials, without copied private archives or receipts.
Browser evidence remains explicit. In E.4 under PBI-046, compare both
development approaches and the same supported scenarios with
E.1 using actual outcomes, elapsed runtime, setup/operating steps, resource
use and maintained custom responsibilities; record missing historical
measurements as unavailable, not estimated facts. Deliver a runnable guide,
live demonstration, comparison and evidence-based Lifecycle Architecture
recommendation. No production-readiness conclusion follows from parity alone.

## Existing requirements and deliberately unscheduled work

E.3 does not silently remove the accepted same-component reservation,
ownership, compatibility or preservation requirements. Native page locking
is narrower than UC-9's atomic multi-component pre-edit reservation. PBI-036
must expose this difference; retain a justified extension or obtain a specific
Product Owner requirement change during managed design. Merely using native
locks cannot satisfy the stronger criterion.

PBI-018, PBI-022, PBI-023 and PBI-024 remain unscheduled: comprehensive
reservation contention, full request/verifier/stale-worker fencing, schema
drift and additional recovery states go beyond E.1's demonstrated A–I parity.
They remain obligations and prevent full acceptance claims where applicable.
E.3/E.4's selected parallel/negative tests do not automatically complete them.

PBI-025/026/028/030/031/032/033 also remain unscheduled: shared-service
privileges/gateway exposure, additional release profiles, hosted source CI,
independent attestations, licensing/distribution and another host platform.
PBI-043's local pipeline does not complete PBI-030 or PBI-031. Licensing remains
an open distribution constraint; this exercise does not authorize new external
distribution of the paper or third-party software.

OCI deployment, bastion/private-subnet access and the HTTPS-only service
alternative (p. 46) are documented as scope boundaries, not silently omitted
or represented as tested. The additional export mechanisms in Appendix B
(p. 47) are explained alternatives; native PROJECT is the selected primary
path. Commercial audit products and production service operation are not
hidden prerequisites for the local exercise.

## Execution order and entry/exit gates

First refine coverage/actors and approve requirements deltas and the resource
and native-tool design under PBI-036. Then establish capture/adoption and
baseline reconstruction and the shared-team journey. Parallel-feature work,
complete private-target reconstruction and central DEV synchronization follow
in E.4. Add test/coverage/audit evidence before qualifying native
initial/upgrade releases and re-proving the three protections. The bounded
mini-app fixture can follow the stable capture baseline; automate the proven
team-centric journeys and independently reproduce E.3. E.4 finalizes the
consolidated reference and cross-approach comparison.

No duration or team capacity has been supplied. This is a broad Elaboration
exercise, not a measured single-timebox commitment. At activation, estimate
the selected work and present any necessary split for Product Owner decision;
do not silently drop paper scenarios or transfer scheduled items. Refine broad
parents into approved sprint children only during setup/design, following the
local method. Planned board rows do not assert design approval.

Before code-bearing work, update exact native build/test/regression commands
and evidence locations in the test profile. Existing E.1 commands cannot be
relabeled as native PROJECT tests. Run new smoke/unit/integration gates and
applicable regression against the native workflow, including business-data
preservation; preserve the retained E.1 reference lab and historical evidence.
Any intentionally superseded test must retain its behavioral requirement
mapping and receive an explicit disposition.

Exit review requires an outcome and evidence for every assigned item and
paper workflow assigned to E.3 above, documented native-tool limitations, explicit remaining
requirements, reproducible operating instructions and a live Product Owner
review. An experiment may establish a limitation, but that does not fulfill
the affected product criterion or authorize a custom replacement. Sprint
closure and Lifecycle Architecture acceptance remain distinct decisions.

## Original planning validation — 2026-10-19 (before split)

Reviewed all 35 existing root PBIs against the paper workflows and E.1's
assessment and clean-checkout evidence. Added PBI-036–046 and scheduled eight
existing items plus those eleven new items. Existing backlog ordering and
definitions and all E.1 plan/board/evidence entries are preserved. Shared
README, roadmap, SRS, architecture, research and test-profile navigation now
identify the planned successor and distinguish existing behavior from E.3.

Executed a structural check confirming 46 unique sequential root IDs, all
eleven new titles within 80 characters, two-to-four-sentence descriptions,
single-line verb-led test criteria and the existing Proposed definition
format. Confirmed 19 unique E.3 assignments with matching backlog titles and
19 Planned board rows, required managed/test/regression fields and zero
Progress sprints. Checked 40 planning-related local link targets and applicable
anchors. The whitespace check passed. No code, database or browser tests were
run for this planning change, and no execution/design approval is inferred.

## Split validation — 2026-10-19

Reassigned five items to E.4 and retained fourteen in E.3. Checked that all
19 original assignments remain exactly once, every title matches the unchanged
backlog and each board row matches its planned sprint. Both iterations retain
managed mode and smoke/unit/integration test and regression gates; neither
is active. Checked 62 planning links and applicable anchors and passed the
whitespace check. Shared orientation, requirements, architecture, research
and test-profile references now distinguish the two paths. No runtime tests,
deployment, requirement acceptance or historical E.1 status changes occurred.

## Strict requirement validation — 2026-10-19

Strengthened PBI-036's two-sprint Oracle traceability criterion and PBI-046's
three-approach decision evidence criterion. Added and assigned PBI-047 to E.3
so its E.1 comparison is independently required at that handover. The earlier
14-item split snapshot above is historical; the current plan has 15 E.3 items
and five E.4 items, all Planned. No earlier acceptance or execution result was
changed. The strict source/evidence contract is linked from both sprint plans,
the E.4 record, README, roadmap, SRS, architecture, research and test profile.

Executed checks confirming 47 sequential root PBIs, canonical changed item
formats, all 20 unique assignments with matching Planned board rows, required
test/regression fields and no active sprint. Validated 72 planning links and
applicable anchors; the whitespace check passed. This validates the planning
change only: the scenario source maps, executions and comparisons themselves
remain required future deliverables, not completed evidence.
