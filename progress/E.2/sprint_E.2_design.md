# E.2 — Gap-analysis exercises and decision-package design

## PBI-051 — Evidence-backed evolution decision

Status: Proposed

Design approval: Awaiting Product Owner review. Analysis was explicitly approved
on 2026-10-19 after the [external analysis review](sprint_E.2_analysis_review-1.md)
found no required corrections. No exercise, provisioning, test
skeleton or runtime verification has been performed under this design.

The [external design review](sprint_E.2_design_review-1.md) raises no findings
and supports Product Owner acceptance, including the regression proposal.
The [engineering response](sprint_E.2_design_review-1-response.md) and
[assessment](sprint_E.2_assessment.md) record closure. The verdict applies to its pinned source. The Product Owner
subsequently clarified the common-repository sequence below; no independent
recheck of that clarification or implementation approval is claimed.

The [analysis](sprint_E.2_analysis.md) owns findings, H-1/H-2 and EQ-1–5;
[PROJECT fit assessment](project-fit-assessment.md) owns PF-01–12. The
[SRS](../../docs/srs.md) owns requirements, [architecture](../../docs/architecture.md)
the existing candidate, [test profile](../../docs/test-profile.md) verification,
[PLAN](../../PLAN.md#sprint-e2---assess-e1-against-oracle-lifecycle-guidance)
sprint assignment, and [board](../../PROGRESS_BOARD.md) execution status.
The [assessment](sprint_E.2_assessment.md) owns review closure; the
[setup](sprint_E.2_setup.md) owns contracting. This is an experimental design,
not a permanent replacement of those product contracts.

### Requirement summary

Give developers flexibility through stable, industry-standard tools and
techniques. Establish which combinations of Working Copies, PROJECT and useful
E.1 capabilities preserve accepted source, declared dependencies and delivery
outcomes at reasonable operating cost. Coexistence is a direction to test,
not a required successful result. Deliver source-backed classifications,
existing-backlog reconciliation, a dependency roadmap and a reproducible live
walkthrough. The experiment need not implement all later production outcomes.

### Feasibility and exact sources

The recorded baseline is APEX 24.2.0, SQLcl 25.3.0.274.1210 and Database
23.26.3.0.0. Current installed versions/readiness are unknown until preflight;
no upgrade or host rebuild is authorized by this design. The supplied
[Oracle paper](../../refs/apex-lifecycle-management-v3.pdf), version 3.2,
validates examples against 24.2/25.1.1, so exact-client behavior needs checking.

[SQLcl 25.3 PROJECT, section 6.2](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/project-command.html)
documents existing-repository initialization, capture, generated/custom staging,
release and deployment. [Its examples, section 6.5](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/project-command-usage-examples.html)
provide the branch/base workflow. [APEX 24.2 Working Copies, section 5.9.1](https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/about-working-copies.html)
documents the GUI operations and merge limits. These interfaces make a bounded
experiment feasible; they do not establish the desired outcomes in advance.
Documentation/help inspection precedes command adaptation. Supporting source
links and paper page mappings remain in AN-01–14, avoiding a second source
register with conflicting claims.

The implementation inspection reveals an important integration boundary:
[scripts/cicd-artifact.py](../../scripts/cicd-artifact.py) expects E.1's specific
tar layout, page inventory and E1_CTRL initialization hook. It cannot be called
an unchanged validator for a PROJECT ZIP. Conversely,
[scripts/cicd-compatibility.py](../../scripts/cicd-compatibility.py) exposes a
small validator for the declared component combinations. Reuse that rule in a
bounded bridge, explicitly labeling it custom; do not clone the E.1 controller.

### Scope decomposition

These are proposed sprint-scoped children of PBI-051 under local P6. They
remain in this design and the board, not new root backlog items. Acceptance of
the design approves this decomposition; none is complete now.

1. **PBI-051.1 — Establish safe inputs and evidence boundaries.** Outcome:
   pinned source/tool inventory, historical comparison, owned disposable
   resources, one PROJECT-initialized local Git repository and evidence ledger.
   Acceptance: the initial Main source is captured, retained E.1 state is identified,
   a foreign target is refused, and source/evidence levels are distinguishable.
   Dependencies: approved design and existing E.1 evidence.
2. **PBI-051.2 — Qualify Working Copy capture into Git.** Outcome: an observed
   authoring/checkpoint/reconstruction path with usability and failure limits.
   Acceptance: both intended changes survive reconstruction; stale/deletion
   handling and abandonment are observed or explicitly fail with evidence.
   Dependency: PBI-051.1. Capture the agreed Main outcome in that same
   PROJECT-initialized repository; .3 subsequently qualifies its native artifacts.
3. **PBI-051.3 — Assess PROJECT compatibility and retained admission controls.**
   Outcome: a native initial/change release slice, repository handoff assessment
   and declared-dependency admission evidence. Acceptance: PF findings identify
   actual captured scope, migration ownership, artifact identity, mapped-target
   outcomes, preservation and allowed/rejected declarations. An evidenced tool
   failure is a valid assessment outcome, not an equivalent-delivery claim.
   Dependency: .1 and .2; use their existing repository and accepted Main
   checkpoint to complete native staging/release and H-1/H-2 assessment.
4. **PBI-051.4 — Deliver the gap decision and reproducible handover.** Outcome:
   classified findings, reconciled follow-up and ordered roadmap plus presentation
   pair/manual/live demonstration. Acceptance: the Product Owner can inspect
   sources and results, repeat the selected exercises and assess recommendations;
   actual handover feedback is recorded. Dependencies: .1–.3 evidence/dispositions
   and applicable quality gates. No later-sprint PBI is claimed delivered.

### Design overview

- Preserve E.1 source, historical evidence and retained environments; verify
  versions and allocate owned disposable authoring and test resources.
- Create one local Git repository and initialize PROJECT for the authoring
  application and schema, with explicit capture scope and migration ownership.
- Develop in APEX Working Copies, integrate agreed changes into Main, then use
  PROJECT to export, review and commit the team checkpoint in that repository.
- Review staged migrations and intentional SQL changes, generate an identified
  native artifact and bind its component/dependency declarations.
- Reuse appropriate E.1 tools for validation and justified controls; qualify
  reconstruction, delivery and preservation in the owned test targets.
- Use lower-level exports/imports as labeled comparison paths from the same
  agreed checkpoint, without creating a second maintained source or migration
  authority. Compatibility remains an outcome to establish.
- Turn observed results into source-backed gap findings, existing-backlog
  reconciliation and an ordered roadmap, with a reproducible live walkthrough.
- Keep interfaces suitable for eventual pipelines; hosted pipeline delivery
  remains outside these bounded experiments.

### Preservation, fixtures and ownership

Before writes, record read-only DB/PDB/APEX identity, tools, schemas/workspaces,
application IDs, retained E.1 component metadata, source fingerprints and
history/configuration summaries. Preserve the current checkout and E.1 areas,
including E1_CTRL, E1_DEV_A/B/C, E1_INTEGRATION and E1_UAT. A missing runtime,
unexpected drift or wrong version stops preparation with a clear prerequisite
report; it never triggers a reset, destroy, restore or tool upgrade.

After approval allocate one authoring schema/workspace and two disposable target
schema/workspace pairs (fresh reconstruction and populated-baseline qualification).
Use an E2-owned run prefix, but check actual names and instance-wide app IDs;
record allocations rather than assume proposed names are unused. A run inventory
binds each resource to owner/run/DB/PDB and expected role. Administrator authority
is confined to provisioning; ordinary exercises use assigned schema credentials.
No secrets or business data enter source/evidence. Cleanup requires that inventory
and removes only positively identified owned resources; it is never automatic
on a failure and never touches retained E.1 state.

Use a reduced, real APEX greeting fixture with two visible pages and a shared
LOV over synthetic greeting data. Create it through documented App Builder
controls and export its generated source unchanged. Reuse E.1 business SQL and
component declarations where independently applicable; explicitly list any
adaptation or omitted E.1 behavior. The full E.1 exported application depends on
E1_CTRL and must not be imported as though it were self-contained. The reduced
fixture demonstrates transport/migration/metadata behavior, not full E.1 runtime
fencing, account security or availability equivalence. If an important conclusion
requires omitted behavior, leave that conclusion unproved and identify its
existing follow-up; do not silently enlarge the fixture.

Work under `.local-apex/e2/<run>/` in one primary scratch Git repository with
`codex/` branches. Initialize Git, initialize PROJECT in it and capture the
initial Main application/schema baseline before Working Copy exercises. Capture
agreed Main outcomes after Working Copy integration into this same repository
using PROJECT. Reuse E.1 tools when their contracts fit, including the existing
compatibility validator. Lower-level exports are comparison/reconstruction
outputs, not a second maintained source or migration authority. Any repository
layout trial uses a disposable branch/copy of the common baseline and never
becomes a competing primary repository. Pin source and imported file hashes.
Do not initialize PROJECT in this working checkout or restructure its product
sources. Create one repository compatibility trial containing a pinned E.1 source
layout plus an additive native project root; record which files are authoritative
and which are frozen comparison inputs. Try native configuration before writing
an adapter. Keep PROJECT-generated changelogs separate from E.1's migration
history; no changelog synchronization against an unverified baseline is permitted.

### Execution sequence in the common repository

1. Complete safe preparation, create the local Git repository, initialize
   PROJECT and record its filtered initial Main/schema capture.
2. Exercise Working Copies in APEX, integrate into Main, then export/review/
   commit those outcomes in that same PROJECT repository. A Working Copy itself
   remains an APEX authoring resource; its agreed result enters Git through Main.
3. Continue PROJECT staging, native artifacts and reconstruction from those
   commits, applying E.1 tools where appropriate and recording adaptations.
4. Qualify declarations/admission, compare outcomes and deliver the gap decision.

X1 and X2 below describe evidence responsibilities, not separate repository
implementations or a requirement to finish all of X1 before initializing PROJECT.

### Exercise X1 — Working Copies, team checkpoint and reconstruction

Decision: can ordinary native authoring feed the accepted Git contract with
usable coordination (H-2, EQ-1; AN-01/03/04/13; paper 12–14, 32)?

Start from the captured fixture baseline and a recorded synthetic history/config
sentinel. Create one Working Copy; change a visible page heading there and a
disjoint heading in Main. Compare, refresh and merge with actual App Builder
controls, recording selected changes and operator reasoning. Take one agreed
Main team checkpoint into the common repository through PROJECT export and
reviewed commit. The supplementary lower-level export uses the documented
split/original-ID/no-date profile; inspect the diff and full schema dependency
inventory. Reconstruct in the fresh owned target and verify both headings,
shared LOV behavior and the expected greeting. Compare with a Main-authored
checkpoint through the same capture path.

Use one expendable branch/copy to demonstrate stale same-page replacement and
its corrective refresh/reapply sequence; show a page deletion's explicit Main
handling and abandonment without Main changes. Observe actual page coordination
and record whether the UI protects the intended edit. Show a uniquely named
schema marker visible to Main and its Working Copy to expose shared-schema scope;
remove only that owned fixture after recording it. Capture number of operator
steps, required decisions, confusing diffs and recovery effort; no invented E.1
usability baseline. These bounded authoring alternatives test E.1-stage policies
without permanently changing the SRS or claiming component reservation equivalence.

Success means a correctly observed and explained outcome, with no missing edit
hidden. A failed native merge is an assessment result. Harness assertions must
still detect it. No browser automation of Working Copy management is presented
as a documented public API, and no undocumented APEX package is invoked.

### Exercise X2 — PROJECT workflow and optional repository compatibility

Decision: is native workflow fit plausible with a bounded integration cost
(H-1 and combined H-1/H-2, EQ-2; PF-01–07/10–12; paper 18–20, 26–30)?

During preparation in the common Git repository, establish the comparison base
explicitly and initialize a filtered native project for the owned authoring schema
and Main app only. Continue that same project after X1 captures its outcomes. Inspect export
inventory and exclude Working Copies, control fixtures, credentials and business
data. Review the exported source, commit it, stage against the recorded base,
review/install order and any custom SQL, then commit the distribution. Run native
verification and use an identified artifact for fresh/populated target tests
before freezing a release. Record the exact verified distribution revision;
if release creation changes distribution inputs, regenerate and requalify rather
than transferring stale evidence to different bytes.

Demonstrate one subsequent visible page correction, an additive schema change
and one intentional seed/configuration change represented as reviewed custom SQL.
Retain synthetic history and user settings through upgrade and repeat. The same
candidate artifact bytes must pass qualification before use in the second target.
Observe default, replacement and mapped identities; compare full relevant fields,
not row counts alone. A fresh target also receives the current release so that
baseline and upgrade paths are both assessed. An unexpected reinstall, checksum
failure or data difference becomes a finding; no automatic forced retry is allowed.

For optional use, compare lower-level reconstruction of the same checkpoint
with the PROJECT path. Try supported initialization/configuration with the E.1
layout retained as frozen inputs. Record direct compatibility, bounded adaptation,
one-time conversion or inability to establish a supported path. Do not hand-copy
parallel live source trees as the routine bridge. Inspect E.1 tool assumptions and
record which tools can consume the result unchanged; a new wrapper cannot make
an unchanged-tool claim true. Stop before generalizing the whole E.1 framework.
A migration to a generated history is a distinct reviewed handoff, never a second
writer to an active history. Native release command syntax/help, including version
handling, is capability discovery and does not require a general SemVer engine.

### Exercise X3 — Component declaration and validation admission

Decision: can native artifacts retain the explicit contract enforced in E.1
(PF-08/09, EQ-2/4; FR-5/7/9/10; existing PBI-021/038/045)?

First inspect whether native artifact/configuration facilities carry arbitrary
component declarations. Prefer a documented facility if adequate. Otherwise use
an explicit small assessment envelope binding the immutable native archive hash,
reviewed source/distribution revision, declaration hash, exact target identity,
observed installed component state and the check-result receipt. This is a custom
bridge under evaluation, not a native PROJECT feature. Record its limitations.

Invoke E.1's existing compatibility validator against copied declarations; do
not reimplement its rules. Accept the supported initial and Hello patch triples.
Reject proposed Foundation 2.0.0 with consumers still requiring 1.0.0, and reject
missing/unknown/inconsistent declarations. The proposed incompatible version is
metadata only: execute no breaking Foundation DDL. Bind any additional envelope
checks to this run and artifact. A changed archive/source/declaration/target state,
missing receipt or failed validation blocks the deploy call before target writes;
verify unchanged definitions/rows and show the deployment subprocess was not called.
The fixture's installed metadata must reconcile with the envelope after delivery.

Unit-injected rejection proves bridge control flow; successful real-target runs
and real negative admission observations are separately required. Neither proves
full E.1 drift fencing or partial-DDL recovery. Inspect native failure/transaction
behavior against existing E.1 receipts first. Do not inject an additional committed
DDL failure merely because it is possible. If an unproved safety behavior would
change the recommendation, propose a focused design amendment with exact failure,
target, observation and recovery boundary before executing it.

### Conditional evidence — EQ-3 and EQ-5

For branch identity, compare two no-edit captures and the owned mapped-target
reconstruction already produced by X1/X2. Explain original-ID, mapping and any
nonsemantic noise against paper page 34. This qualifies a shared-instance
alternative; it does not demonstrate a matched private branch instance. A full
clone/new instance needs a design amendment if the recommendation relies on it.

For audit/test integration, inspect available interfaces and map utPLSQL,
coverage, browser tests, native audits and dependency admission to candidate
identity, inputs, stage, evidence and failure effect. If a finding depends on
uncertain local Advisor behavior, use one controlled detectable finding and
correction in the owned fixture. Otherwise source evidence is enough for E.2's
gap classification. Do not install full utPLSQL/browser/optional commercial suites
merely to establish their absence. Their delivery remains E.3/E.4. Subscriptions
remain part of component interface/dependency analysis, not an extra exercise;
PBI-052 contract definition and E.5 upgrades stay outside implementation here.

### Proposed implementation interfaces

After design approval, implement only the needed domain helpers:
`scripts/cicd-oracle-lifecycle.sh` for run/preflight/GUI checkpoints and
`scripts/cicd-oracle-lifecycle.py` for inventory, hashing, receipt admission and
safe subprocess boundaries; SQL fixtures under `tests/sql/oracle_lifecycle/`.
Use the existing SQLcl/runtime and supported import/provisioning primitives,
without calling E.1 wrappers that silently select retained targets. Keep any
necessary interface adaptation explicit and bounded. Exact credential resolution
is local and role-scoped; logs redact connection secrets.

Proposed runner modes are `preflight`, `live`, `rehearsal`, and `inspect`, all
with an explicit run identifier. Preflight is read-only and returns ready or
blocked with diagnostics. Live pauses for actual GUI decisions. Rehearsal may
reuse previously captured GUI evidence only when it reports that limitation;
skipped observations cannot pass as fresh GUI checks. Inspect opens retained
results without mutations. A first-time run requires genuine authoring input.
No automatic deletion/rebuild is part of these modes.

Per-run evidence records contain case ID, source/target identities, exact versions,
input hashes, commands with secrets removed, exit status, expected/actual output,
selected GUI decisions, field-level preservation checks and timestamp. Distinguish
`demonstrated`, `observed limitation`, `blocked` and `not run`. Passing the harness
never changes a failed capability into a successful capability. Unknown cost or
missing historical measurements remain unknown.

### Testing Strategy

Test: smoke, unit, integration. Regression: smoke, unit, integration.
Proposed regression scope: `oracle_lifecycle` for E.2, pending explicit approval
and a subsequent PLAN/test-profile update before code/test skeletons. The scope
covers every E.2 helper and fixture plus reused compatibility behavior; production
E.1 code remains unchanged. The current PLAN still requests full registered
regression. Approval of this design must explicitly include the scope change or
retain that full gate with a separately safe disposable E.1 topology.

Reason: existing registered E.1 integration tests target retained E.1 state and
include unfinished acceptance, so blindly replaying them conflicts with preservation.
Record those limitations; do not modify the old tests, manufacture passes or call
E.2 scoped success full E.1 regression. If E.1 code must change, stop for a new
impact assessment and affected regression scope before implementing that change.

Smoke candidates check source hashes, resource/target identity, versions and
fixture ownership before writes; expected time is unmeasured. Unit targets isolate
inventory/admission/subprocess boundaries with temporary files and fake commands;
no Oracle mocks establish runtime equivalence. Integration scenarios run the real
owned fixture, capture/reconstruction, release upgrade/repeat and admission cases.
Required GUI observations remain explicit manual evidence. Record elapsed times
when executed instead of claiming estimates as measurements.

## Test Specification

All cases below belong to PBI-051 and proposed children .1–.4. They are specified,
not implemented or registered. Domain test files will be
`tests/smoke/test_oracle_lifecycle.sh`, `tests/unit/test_oracle_lifecycle.sh` and
`tests/integration/test_oracle_lifecycle.sh`. Function names below are proposed
runner identities, not commands claimed to work today.

1. **SM-E2-1 / test_SM1_oracle_lifecycle_preflight:** .1; FR-11/13, NFR-2,
   UC-1/6; EQ-1–5. Valid inventory yields ready; missing input, tool-version
   mismatch or foreign schema/app/PDB yields blocked before mutation. Preserve
   before/after retained-E.1 summaries. A live preflight never creates fixtures.
2. **UT-E2-1 / test_UT1_oracle_lifecycle_ownership:** .1; FR-11/13. With fake
   subprocesses test owned versus foreign/missing inventory, name collision and
   mismatched DB/PDB. All rejected cases invoke zero mutation commands.
3. **UT-E2-2 / test_UT2_oracle_lifecycle_admission:** .3; FR-5/7; EQ-2/4.
   Temporary valid/changed/missing envelope inputs and failed subprocesses prove
   exact binding and failure propagation. Exercise the reused validator with
   supported, incompatible, missing and unknown declarations. Rejection is a
   nonzero result with a specific diagnosis and no deploy invocation.
4. **IT-E2-1 / test_IT1_working_copy_capture:** .2; FR-8/11/12, UC-7–10/12;
   H-2/EQ-1. Real authoring target, GUI log and accepted source revision are
   prerequisites. Both intended headings and LOV/greeting behavior reconstruct;
   deletion/abandonment outcomes and shared-schema marker are accounted for.
   Stale-merge loss must be detected, its correction checked or reported blocked.
5. **IT-E2-2 / test_IT2_project_delivery:** .3; FR-5/6/11/12, UC-4/5/11;
   H-1/EQ-2/3. Native configured source scope and reviewed distribution produce
   identified artifacts. Fresh/baseline/repeat observations compare real schema/
   app identity, existing row fields, settings and migration history; artifact
   hashes agree across qualification/promotion. Generated/custom change ownership
   and alternate capture path differences are retained, not normalized away blindly.
6. **IT-E2-3 / test_IT3_native_contract_admission:** .3; FR-5/7/9/10,
   UC-4/5/11; PF-08/EQ-2/4. Against the owned target, allowed declarations pass;
   incompatible/missing/changed inputs reject before native deploy. Query unchanged
   target definitions and sentinel fields and retain no-deploy evidence. Installed
   metadata after a positive delivery matches the identified declaration. Injected
   unit failures alone cannot satisfy this integration case.
7. **IT-E2-4 / test_IT4_optional_native_audit:** conditional .3; FR-13,
   PBI-041 context/EQ-5. Only if local behavior is material: a controlled audit
   finding is observed and the corrected fixture rerun. Otherwise record why this
   case is not selected; do not register a permanently skipped passing test.
8. **Review-E2-1:** .4; PBI-051/UC-6. Every AN/PF disposition names exact
   sources, evidence level, remaining limitation, affected requirement and existing
   backlog destination. Recommendations do not infer absent measurements or
   complete later work. All executed cases, including failures, appear in handover.

After approval create `tests/manifests/component_oracle_lifecycle.manifest` and
`progress/E.2/new_tests.manifest` using actual `suite:script:function` entries.
Register only selected cases. The planned gate sequence is new-only smoke → unit
→ integration, then approved-scope regression smoke → unit → integration through
`tests/run.sh`; actual invocation requires both suite and manifest parameters.
Unrun/manual/blocked observations are separate from executable case success.
Skeletons and fixture resources are not created at this design gate.

### Findings and roadmap deliverables

Write the final experimental gap report as `oracle-gap-analysis.md`, linking
AN/PF IDs to fresh evidence and the approved analysis. For each custom mechanism
state retain, native replacement, bounded bridge, further validation or explicit
policy decision. Replacement requires the relevant outcome evidence; a valid
reduced-fixture experiment cannot prove all E.1 protections unnecessary.

Reconcile with PBI-017–047 and PBI-052 before proposing genuinely new outcomes.
Keep Proposed/unscheduled versus assigned and delivered status explicit. The
roadmap orders source/policy/identity → capture/staging/reconstruction → compatible
release and metadata admission → test/audit/pipeline integration → collaboration
qualification and comparison → stabilized toolchain → E.5 Foundation upgrades.
Each step needs prerequisites, exit evidence and an existing backlog owner;
no E.3–E.5 reassignment occurs through this design.

### Walkthrough and handover

Deliver `sprint_E.2_increment_demo.md` and matching editable `.pptx`,
`user_manual.md` and `sprint_E.2_handover.md`. They will link from README and this
sprint's assessment once real artifacts exist. Journey: inspect baseline and
read-only preflight → Working Copy authoring and team checkpoint → Git/source
review and reconstruction → PROJECT staged change/native artifact → declaration
admission failure and valid delivery → inspect evidence/findings/backlog/roadmap.
A failed capability is demonstrated honestly with its impact and follow-up.

The complete Markdown walkthrough supplies verified portable commands, actual
inputs, expected intermediate results, GUI decisions, recovery boundaries and
slide mapping. Provide a repeat path using fresh owned allocations, not a reset
of retained E.1. Rehearse and retain logs, render/inspect every slide, and record
live Product Owner questions/decision. Historical captures never stand in for
claimed live authoring. No current demo/rehearsal completion is asserted.

### Approval boundary

There are no unresolved product questions preventing review of this proposal.
Runtime readiness, export fidelity, native packaging metadata support and actual
operating effort remain experiment inputs. Unexpected resource requirements or
material interface substitutions return for amendment; no automatic upgrade,
undocumented API or full-controller rebuild is authorized.

Requested approval covers the four child outcomes, isolated reduced-fixture
X1–X3, conditional source-first EQ-3/EQ-5 handling, explicit custom-bridge trial,
and E.2-only regression scope. It does not permanently adopt PROJECT, change
E.1-stage product policies, implement PBI-052 or move E.5 work. Design acceptance
must be explicit before code, test skeletons, provisioning or runtime exercises.
