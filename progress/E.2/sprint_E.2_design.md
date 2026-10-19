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
subsequently clarified the common-repository sequence, section-script interfaces
and experiment-based verification below; no independent recheck of those amendments or implementation
approval is claimed.

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
   Dependencies: PBI-051.1 and the PROJECT path established by .3. Capture the
   agreed Main outcome in that same repository and repeat its qualified path.
3. **PBI-051.3 — Assess PROJECT compatibility and retained admission controls.**
   Outcome: a native initial/change release slice, repository handoff assessment
   and declared-dependency admission evidence. Acceptance: PF findings identify
   actual captured scope, migration ownership, artifact identity, mapped-target
   outcomes, preservation and allowed/rejected declarations. An evidenced tool
   failure is a valid assessment outcome, not an equivalent-delivery claim.
   Dependency: .1. Establish PROJECT first; .2 then contributes a Working Copy
   checkpoint through this same path for the combined H-1/H-2 assessment.
4. **PBI-051.4 — Deliver the gap decision and reproducible handover.** Outcome:
   classified findings, reconciled follow-up and ordered roadmap plus presentation
   pair/manual/live demonstration. Acceptance: the Product Owner can inspect
   sources and results, repeat the selected exercises and assess recommendations;
   actual handover feedback is recorded. Dependencies: .1–.3 evidence/dispositions
   and the specified exercise/handover checks. No later-sprint PBI is claimed delivered.

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
2. Complete X1: establish PROJECT capture, staging, native artifacts and
   reconstruction, applying E.1 tools where appropriate and recording adaptations.
3. Complete X2: exercise Working Copies in APEX, integrate into Main, then
   export/review/commit those outcomes in the same PROJECT repository and repeat
   the established delivery path. A Working Copy remains an APEX authoring
   resource; its agreed result enters Git through Main.
4. Qualify declarations/admission, compare outcomes and deliver the gap decision.

X1 establishes the PROJECT path first. X2 then uses that same repository and
delivery path for Working Copy outcomes; neither exercise creates a competing
primary repository.

### Exercise X1 — PROJECT workflow and optional repository compatibility

Decision: is native workflow fit plausible with a bounded integration cost
(H-1 and combined H-1/H-2, EQ-2; PF-01–07/10–12; paper 18–20, 26–30)?

During preparation in the common Git repository, establish the comparison base
explicitly and initialize a filtered native project for the owned authoring schema
and Main app only. Establish and qualify this native path before the Working
Copy exercise. Inspect export inventory and exclude Working Copies, control fixtures, credentials and business
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

### Exercise X2 — Working Copies, team checkpoint and reconstruction

Decision: can ordinary native authoring feed the accepted Git contract with
usable coordination (H-2, EQ-1; AN-01/03/04/13; paper 12–14, 32)?

Start from X1's captured and qualified fixture baseline in the common PROJECT
repository, with a recorded synthetic history/config
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

Follow E.1's [thin launcher](../../scripts/cicd-walkthrough.sh) and
[individually runnable section scripts](../../scripts/cicd-walkthrough-F_hello_patch.sh).
Implement these proposed interfaces only after design approval:

- `scripts/cicd-oracle-lifecycle.sh`: thin launcher, ordered calls to sections
  A–E, selected mode and overall progress. Section operations stay in their scripts.
- `scripts/cicd-oracle-lifecycle-A_prepare.sh`: owned-resource preparation,
  version/source inventory and common PROJECT repository setup.
- `scripts/cicd-oracle-lifecycle-B_project.sh`: X1 PROJECT workflow, artifacts,
  mapped-target delivery and preservation observations.
- `scripts/cicd-oracle-lifecycle-C_working_copy.sh`: X2 authoring checkpoints,
  capture into B's repository and reconstruction through its established path.
- `scripts/cicd-oracle-lifecycle-D_admission.sh`: X3 declaration validation,
  allowed/rejected delivery and evidence inspection.
- `scripts/cicd-oracle-lifecycle-E_findings.sh`: inspect the actual findings,
  comparisons, backlog reconciliation and roadmap during handover. This script
  does not invent conclusions or automatically change managed backlog items.
- `scripts/cicd-oracle-lifecycle-common.sh`: shared option parsing, pauses,
  logging and checkpoint verification; no hidden section orchestration.
- `scripts/cicd-oracle-lifecycle.py`: narrow inventory/hash/receipt/admission
  utilities where appropriate, reusing E.1 rules. SQL fixtures belong under
  `tests/sql/oracle_lifecycle/`.

Use existing SQLcl/runtime and supported import/provisioning primitives without
calling E.1 wrappers that silently select retained targets. Record bounded
adaptations. Credential resolution is local/role-scoped and logs redact secrets.

#### Modes apply to each section

Every section script accepts one of `--preflight`, `--live`, `--rehearse` or
`--inspect`, plus an explicit `--run RUN_ID`. These options are shared across
sections; do not build four separate implementations of each section. The
launcher invokes the same scripts in order and forwards the chosen mode/run.
A section can also be invoked directly with its verified prerequisites.

- `--preflight`: inspect requirements without target mutation. Whole-walkthrough
  preflight checks the plan/tool/source requirements, identifying resources that
  A will create; it does not demand that all later checkpoints already exist.
  A section's execution-entry check additionally requires its actual predecessor
  evidence and current target state. A missing dependency blocks execution.
- `--live`: execute the selected section with inspection pauses and real GUI
  decisions; require an interactive terminal for human checkpoints.
- `--rehearse`: execute unattended-capable steps and report human checks as
  skipped or historical evidence. It cannot create a fresh Working Copy merge
  observation without an operator. Missing required GUI evidence is incomplete,
  not a successful end-to-end result.
- `--inspect`: read saved outputs/checkpoints without deployment or authoring
  actions. It can inspect an existing run offline without a live database.

#### Resume and retry are continuation options

`--resume` and section-local `--retry STEP` modify `--live`/`--rehearse`; they
are not modes and are invalid with `--preflight`/`--inspect`. The launcher can
resume at the first incomplete section after checking predecessor evidence.
Direct section execution resumes/retries only that section's named steps.

Before continuation, verify run/resource ownership, source/artifact/declaration
hashes, prerequisite results and observed target state. Completion markers alone
are insufficient. Skip completed mutations only after their postconditions are
revalidated; do not present a skipped operation as a new execution observation.
A retry creates a new attempt record and preserves the earlier failure/output.

Offer retry where semantics are known: repeat read-only verification, return to
a failed GUI observation, or recapture corrected source as a new candidate with
fresh downstream validation. Never blindly repeat migration/import, destructive
setup or an uncertain partial-DDL operation. Unknown partial state blocks and
reports the required inspection/recovery; no force retry, reset or automatic
cleanup is provided. Changed inputs invalidate affected downstream checkpoints.
A complete repeat demonstration uses new owned allocations rather than replaying
setup against retained resources.

The manual has one matching chapter per section, its direct invocation, modes,
prerequisites, expected output and supported continuation steps. A failed section
prints the precise next safe command when one exists, otherwise a blocked-state
diagnosis. All CLI examples remain proposed until implemented and verified.

Per-run evidence records contain case ID, source/target identities, exact versions,
input hashes, commands with secrets removed, exit status, expected/actual output,
selected GUI decisions, field-level preservation checks and timestamp. Distinguish
`demonstrated`, `observed limitation`, `blocked` and `not run`. Passing the harness
never changes a failed capability into a successful capability. Unknown cost or
missing historical measurements remain unknown.

### Testing Strategy

For this disposable Elaboration prototype, propose `Test: none` and
`Regression: none` for separate automated suites. No smoke/unit/integration
harness, test skeletons, new-tests manifest or component test manifest is needed.
Use the focused experiments and their observable checks below instead, as
permitted by local P1 for proportionate Elaboration evidence. This replaces the
previous proposed domain regression suite; PLAN parameters change only upon
explicit acceptance of this revised design/verification approach.

This is not a proposal to remove the experiments that answer the analysis.
Section scripts still check actual prerequisites, fail on unexpected errors,
validate expected outcomes and retain logs/receipts. Real GUI decisions remain
visible. Record whether a capability works, fails, is blocked or was not run;
do not invent a passing result from a script exit alone. Safety checks are part
of operating the exercise, not a separate test framework built around helpers.

Do not replay E.1 integration tests against retained targets. Production E.1
code remains unchanged; E.1's unfinished acceptance remains documented. If a
helper becomes shared product code, a production source change is needed, or
an observation cannot establish a material safety property, reassess the affected
verification before extending implementation. Disposable status does not justify
writing to an unverified target or claiming an unsupported capability.

## Exercise Verification

These observations are the evidence specification for PBI-051 and its children,
not new registered automated test cases. Implement checks directly in the
relevant A–E section scripts and walkthrough; record expected/actual results.

- **A — Preparation:** verify source/tool/DB/PDB identity, owned allocation and
  initial state. Refuse foreign targets and unmet prerequisites before writes.
  Record retained E.1 state for the final preservation comparison.
- **B — PROJECT / X1:** inspect exact exported inventory and Git/distribution
  diffs; demonstrate fresh, populated-baseline and repeat outcomes with identified
  artifact bytes. Compare relevant schema/app identities, existing row fields,
  settings and migration history. Account for generated and intentional changes.
- **C — Working Copies / X2:** observe actual compare/refresh/merge; verify both
  intended headings and LOV/greeting behavior after capture and reconstruction
  through B's path. Record stale-edit/deletion handling, abandonment and shared
  schema exposure. A failed capability remains a documented finding.
- **D — Admission / X3:** show an allowed declaration and rejection of incompatible,
  missing or changed inputs before deployment. Verify unchanged target definitions/
  sentinel data and absence of a deploy invocation for rejected attempts. Reconcile
  installed metadata after positive delivery with the identified artifact.
- **Continuation:** demonstrate one needed retry/resume during the walkthrough.
  Preserve the earlier attempt and recheck state. Changed inputs invalidate
  downstream evidence; unknown partial mutations block rather than replay.
- **Conditional native audit:** if its local behavior affects a recommendation,
  observe one controlled finding and corrected result. Otherwise use documented
  availability and label runtime behavior unexecuted; no framework installation
  or permanently skipped passing test is required.
- **E — Findings and handover:** trace every AN/PF disposition to exact sources,
  evidence level, limitation, requirement and existing backlog destination.
  Show all material failures, relevant corrections and unresolved outcomes.
  Rehearse the actual manual/section sequence and demonstrate it live for the
  Product Owner; review links, commands, slides and evidence for correctness.

If a required observation cannot run, record the blocker and its impact on the
recommendation. It may establish a gap; it does not automatically establish that
Oracle technology cannot meet the requirement. There is no separate regression
pass/fail claim and no generic test gate masquerading as prototype completion.

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
read-only preflight → PROJECT capture/staged change/native artifact and
reconstruction → Working Copy authoring and Main checkpoint in that same
repository → repeated capture/delivery → declaration
admission failure and valid delivery → inspect evidence/findings/backlog/roadmap.
A failed capability is demonstrated honestly with its impact and follow-up.

The launcher and A–E section scripts follow the same manual chapters. Direct
section, continuation and rehearsal limitations are demonstrated explicitly.
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
and experiment-based verification without separate automated/regression suites.
It does not permanently adopt PROJECT, change
E.1-stage product policies, implement PBI-052 or move E.5 work. Design acceptance
must be explicit before code, provisioning or runtime exercises.
