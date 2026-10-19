# E.2 — Oracle lifecycle assessment and exercise design

## Design

### Sprint E.2 — Assess E.1 against Oracle lifecycle guidance

#### PBI-051 — Evidence-backed evolution decision

Status: Proposed

Review state: held pending the separate
[analysis](sprint_E.2_analysis.md). The previous design approval request is
withdrawn. This premature draft is retained for reassessment after analysis;
its proposed exercises and test specification are not an agreed scope.
It authorizes no runtime writes or test skeletons. The
[setup](sprint_E.2_setup.md) supplies contract/analysis; the
[scope record](sprint_E.2_proposedchanges.md), [SRS](../../docs/srs.md),
[architecture](../../docs/architecture.md), [test profile](../../docs/test-profile.md),
[PLAN](../../PLAN.md#sprint-e2---assess-e1-against-oracle-lifecycle-guidance)
and [board](../../PROGRESS_BOARD.md) own their respective decisions and status.

### Requirement summary and feasibility

Assess technology and delivery against the supplied
[Oracle paper](../../refs/apex-lifecycle-management-v3.pdf), using its printed
page numbers (matching PDF page numbers), and applicable version-specific
Oracle guidance. Establish equivalence, missing implementation, avoidable
custom mechanisms, policy conflicts and genuine blockers separately. For each
finding retain observation date, versions, source/provenance, evidence path,
confidence, affected actor/use case/requirement, attempted alternatives and
retain/replace/investigate recommendation.

Oracle documents the required baseline primitives: APEX 24.2 split source
export, Working Copy compare/refresh/merge in App Builder, and SQLcl 25.3
PROJECT export/stage/release/gen-artifact/deploy. Availability is established
in documentation; local runtime behavior is not yet tested. Use Oracle public
APIs and generated installers, not hand-authored internal APEX calls. Do not
assume a documented GUI authoring action has an automation API. Investigate
the FR-13 boundary explicitly before claiming fully automated native working
copy operations. GitHub API feasibility is not a dependency: hosted changes
and publication are outside these bounded experiments.

Read-only research may continue before approval. Experiment implementation,
test skeletons and fixture provisioning follow acceptance. If exact-version
help or a supported interface contradicts this design, record the result and
return for approval of any material alternative rather than upgrade tools or
silently change a requirement.

### Sources and coverage

Use the entire paper as the coverage checklist. Record a justified applicable,
optional, deferred or out-of-scope disposition for each recommendation family:
architecture and mini apps (6–8, 15–16), issue planning (9–11), collaboration
(12–14, 32–39), source history/capture/staging (16–21, 47), logic/coverage/UI
testing (22–25), release/deployment/environment mapping (26–30), quality
inspection (30–31), both automation journeys (40–45), and connection constraints
(46). The supplied copy is version 3.2, validated on 24.2/25.1.1 (page 2).
Do not transfer example Java or latest-download settings to the pinned lab
without checking SQLcl 25.3 requirements.

The initial version-specific source register is:

1. [APEX 24.2 export options and split source](https://docs.oracle.com/en/database/oracle/apex/24.2/aeadm/exporting-one-or-more-applications.html),
   sections 3.12.11.1.6.3–6: source granularity, original IDs, export dates and
   importable versus readable output. Verify the complete dependency scope.
2. [APEX 24.2 Working Copies](https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/about-working-copies.html),
   section 5.9.1 and its creation/edit/merge/refresh procedures: compare and
   merge boundaries. Check public API documentation separately for automation.
3. [SQLcl 25.3 PROJECT](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/project.html),
   section 11.16, and [CI/CD introduction](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/introduction.html),
   section 6.1: generated migration/release responsibilities and supported
   object types; custom changes can supplement generated staging.
4. [SQLcl 25.3 project examples](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/project-command-usage-examples.html),
   section 6.5: baseline/change branches and installable artifacts.

Extend the register with version-specific installation mapping, Liquibase,
APEX Advisor and database semantics for every final technical claim. Record
retrieval date and page/section, distinguish Oracle recommendation from an
inference, and retain only short necessary excerpts. No claim is supported
solely by a search-result snippet or newer product documentation.

### Design overview and preservation boundary

Data flow: E.1 source/evidence plus Oracle sources → traceable questions →
bounded isolated exercises → classified findings → existing-PBI reconciliation
→ dependency roadmap → reproducible walkthrough and live review.

Retain the existing Podman/database/APEX/ORDS environment as the starting
point. Before mutation, inventory runtime versions, workspaces, applications,
schema mappings, current source revision, credentials availability and
unexpected edits. Record retained E.1 history/configuration and content
fingerprints read-only. A missing runtime or pending manual UAT drift is a
preflight condition, not permission to reset/rebuild/restore that target.

Create only an explicitly recorded disposable E.2 inventory, separate from
E1_CTRL, E1_DEV_A/B/C, E1_INTEGRATION and E1_UAT. Proposed logical roles are
E2_ANALYSIS (authoring), E2_REBUILD (fresh reconstruction) and E2_UPGRADE
(baseline upgrade). Collision-check schema/workspace names and instance-wide
application IDs, recording the actual allocations; never overwrite collisions.
Use the existing PDB and supported provisioning/import interfaces. Keep
generated credentials local and out of artifacts/logs. Provisioning uses
administrator authority; experiments use their assigned schema credentials.

Use a separate local scratch Git repository for native generated source and
distribution scripts, preserving this checkout's dirty work. Any experimental
branches use the `codex/` prefix. No remote creation, push or PR is part of
these exercises. Record baseline source revisions and hashes without claiming
the current dirty checkout is an accepted release. Capture environment state
before and after each exercise. Cleanup can remove only this run's recorded
disposable resources and refuses foreign objects or missing ownership evidence.
No automatic cleanup of retained E.1 state is permitted.

### Exercise X1 — Establish the relevant E.1 behavior

Question: which Oracle lifecycle outcomes already exist, and which depend on
custom code? Inspect the initial and Hello patch artifacts reconstructed from
the established pinned release recipes, source commit, migration files,
candidate and qualification receipts. Run read-only current-state checks
against retained areas; inspect any recorded drift without restoring it.
Reproduce necessary native SQLcl/APEX import and transactional greeting/history
checks in E.2 disposable targets from the pinned source. Do not replay E.1's
whole A–I runner against retained targets as a hidden precondition.

Observe a fresh initial installation, compatible Hello correction and safe
repeat where required for comparison; preserve field-level synthetic history
and settings. Record what runs through an unchanged E.1 controller versus what
is only a native-interface comparison. If the controller is hard-coded to
E.1 target identities, document that constraint and use public imports in E.2
areas rather than changing the existing controller without a design amendment.
Do not call a native-interface run a full E.1 controller reproduction.

Inspect custom source packaging, candidate/provenance receipts, artifact hashes,
ordered migrations, live fingerprints, version triples, reservations,
maintenance/verifier and repair controls. Separate code inspection, historical
observations and fresh results. Use the selected E.1 failure records to identify
which protections X3 must challenge; avoid duplicating broad E.1 concurrency
proofs or complex upgrades. Outcome: a defensible comparison baseline with
unmeasured historical costs explicitly unknown.

### Exercise X2 — Working Copies through accepted Git source

Question: can native application authoring feed the Git-authoritative release
boundary, and which limitations require coordination or policy changes?
Import the pinned baseline into E2_ANALYSIS. Through documented App Builder
controls create a Working Copy, make one visible page correction, compare,
refresh a disjoint Main change and merge selected changes. Retain the comparison
and both intended changes. Demonstrate a second developer's locked-page view
and distinguish page locking from E.1's component-wide reservation rule.

In disposable copies, demonstrate a same-page stale-merge/overwrite case and
one page deletion requiring explicit handling. Keep before/after source and
show the corrective refresh/coordination or explicit deletion sequence. Delete
an abandoned experimental Working Copy and verify Main is unchanged. Show that
a disposable schema-object change is shared by Main and its Working Copy;
rollback DML where appropriate, remove only the owned DDL fixture afterwards.
Do not infer database isolation from an isolated application page edit.

Capture the resulting Main into a scratch Git change using the documented
stable export profile. Review the complete source diff, dependency scope and
identity metadata; accept a local exact revision; reconstruct that revision
in E2_REBUILD and verify both page changes and greeting/history behavior.
Cross-check PROJECT capture in X3 without adopting two source authorities.
Distinguish APEX Main merge, local Git integration and later artifact
promotion. A team checkpoint may include multiple authors and does not prove
per-feature provenance or private schema isolation.

Routine Working Copy authoring/merge in this disposable experiment is an
explicit experimental exception to the SRS break-glass restriction. Design
acceptance approves testing that alternative, not changing production policy.
Human authoring/review stays visible. Assess whether automated operational
steps can use supported interfaces; if unavailable, record an FR-13 policy
decision or alternative automated Git reconstruction boundary. Do not
manufacture an undocumented automation interface.

### Exercise X3 — Native lifecycle as a replacement candidate

Question: which custom release responsibilities does SQLcl PROJECT cover on
the pinned client, and what remains project-specific? In the scratch repository,
initialize a filtered project with E2_ANALYSIS's baseline app/schema. Exclude
control/test infrastructure, credentials and runtime business data. Inspect
generated filters/configuration and actual client help before using them;
do not paste 25.1.1 properties into 25.3 without checking. Capture initial
definitions and stage against an identified baseline branch. Review generated
APEX/schema distribution scripts, dependencies and any custom intentional data
change. Use one source/migration authority for this experimental track.

Create an initial release/artifact, deploy its exact bytes to E2_REBUILD and
E2_UPGRADE, and record source identity, client/server versions and checksums.
Author the bounded compatible Hello correction, export/stage/review it, release
and qualify the same native artifact on fresh and baseline starts. Repeat it
and compare all retained synthetic history/settings fields. Test documented
same-instance workspace/schema/application-ID mapping; verify that source IDs
remain traceable across remapping. Recheck actual generated installers and
deployment errors rather than assume success from a returned process status.

Introduce one controlled failing validation between qualification and the next
disposable-target deployment; require that failure to stop progression. Then
change candidate source and require renewed validation. This is a local pipeline
boundary exercise, not delivery of hosted pipelines/run dashboards under
PBI-043. Inspect whether native staging/deploy supplies incompatible-start,
drift and partial-DDL protections; exercise one minimal drift or committed-DDL
failure where documentation/inspection cannot answer. Retain partial-state
evidence and demonstrate a bounded forward correction or explain why the target
must remain blocked. Never imply PROJECT is inherently an all-or-nothing
database deployment or a replacement for every E.1 safety requirement.

Stop after the observation needed for a finding. Broad repair/state machines,
full automation, utPLSQL installation/coverage, browser suites, optional external
audits and mini-app delivery remain later PBIs unless a material finding needs
a separately approved focused addition. No Foundation 1.1/2.0 coexistence,
dual-write migration or component maintenance-window exercise is included.

### Testing Strategy

Keep PLAN's Test and Regression values: smoke, unit, integration. No regression
scope reduction is proposed. Use manual evidence for source/GUI findings;
document review is not a passing runtime test. Create executable skeletons and
register the actual selected cases only after approval. Do not manufacture unit
tests for prose or mirror native Oracle implementation details.

Smoke checks verify pinned tools, actual DB/APEX identity, allowed fixture
inventory, source/artifact inputs and retained-state baselines before mutation.
They must reject a wrong target or collision. For any new runner, unit checks
cover fail-closed target ownership, missing/changed validation, and external
command failure propagation with mocked process boundaries; they prove local
control flow, not Oracle runtime behavior. Existing business-logic unit checks
remain in regression.

Integration checks bind X1–X3 to real disposable database/APEX instances and
exact source/artifact identities. GUI checkpoints cover actual compare/refresh/
merge, page locks, abandonment and visible behavior. CLI or injected runtime
fixtures cannot substitute for these checkpoints. Record duration, commands,
exit status, expected/actual output and preservation results. Runtime/resource
comparisons use the same input and comparable starting states; missing E.1
measurements remain unknown, without invented savings.

Run Phase A smoke → unit → integration for the registered new exercise-control
tests, followed by Phase B full registered smoke → unit → integration. Current
`tests/integration/test_release.sh:test_IT1_release` explicitly fails because
full E.1 acceptance is pending. Preserve that failure if observed; selected
manifest success cannot be reported as full regression success. If the full
gate remains blocked by historical incomplete acceptance, bring its exact
result and an evidence-based proposed scope decision to the Product Owner.
Do not change PLAN or mark a failed gate passed to close this sprint.

## Test Specification

SM-E2-1, proposed target `tests/smoke/test_oracle_lifecycle.sh`, verifies the
preflight/preservation boundary for all exercises. Missing fixture ownership,
wrong mappings, unavailable tools or source inputs block before mutation.

UT-E2-1, proposed target `tests/unit/test_oracle_lifecycle.sh`, tests any new
runner's mutation allowlist: foreign schema/application or E.1 retained-target
requests reject without invoking the mutation command. UT-E2-2 tests missing
validation, changed artifact/source and failed subprocess: no downstream
deployment and nonzero status. Use temporary files and stubbed commands only.
If no new control code is needed, record these targets as not applicable by
design refinement rather than create empty passing tests.

IT-E2-1, proposed target `tests/integration/test_oracle_lifecycle.sh`, checks X1
fresh/compatible-patch/repeat behavior in disposable targets, exact archive and
source provenance, visible greeting and field-level synthetic data retention.
Identify any controller-vs-native-interface difference explicitly.

IT-E2-2 uses the same integration domain file for X2 source/Git reconstruction:
both intended page edits survive, original identities remain explainable,
deletion/abandonment are explicit, and a shared-schema marker is visible from
both apps. Supplement it with required manual page-lock and Working Copy
checkpoints. An observed unsafe stale merge is the negative demonstration;
successful assessment requires the documented corrective path or an explicit
unresolved finding, not hiding the unsafe outcome.

IT-E2-3 covers X3 generated initial/change distribution, fresh and baseline
deploys using the same qualified artifact, repeat preservation, target mapping
and failed/stale-validation rejection. IT-E2-4 records the selected native
drift/partial-failure question with before/after evidence and bounded correction
or retained blocked state. A capability failure is a finding; harness integrity,
preservation and correct outcome reporting still must pass.

All cases trace to PBI-051: X1/X3 cover UC-4/5/11 and FR-5–10/13; X2 covers
UC-7–10/12 and FR-8/11–13; preservation/visible greeting cover UC-2/3 and FR-1–4.
Source coverage and backlog reconciliation are reviewed under UC-6/PBI-051.
After approval register actual function entries in
`tests/manifests/component_oracle_lifecycle.manifest` and
`progress/E.2/new_tests.manifest`; these files do not exist yet. Exact copyable
exercise commands will be published only after execution verifies them.

### Findings, backlog reconciliation and roadmap

Write the completed analysis as `progress/E.2/oracle-gap-analysis.md`, linked
from maintained research/architecture guidance. Each finding has a stable
identifier, source page/section, observed E.1 mechanism, requirement, evidence,
classification and disposition. Distinguish supported outcome equivalence
from an identical mechanism. Call a custom mechanism unnecessary only after
showing that a native replacement meets its relevant contract. A genuine
blocker needs a reproducible supported-version failure or documented hard
constraint, impact, attempted alternatives and decision sought. A policy
restriction, unrun scenario or unavailable optional commercial tool has its
own classification.

Reconcile follow-up with PBI-036/037 (coverage/capture), 038/021 (release and
admission), 039/018/019 (collaboration and policy), 020/035 (reconstruction and
adoption), 040/034/041 (tests/coverage/audits), 042 (central DEV), 027/029
(configuration/diagnostics), 043/030/031 (automation/provenance), 044 (mini apps),
045/022/023/024 (protections), 046/047 (comparison), and 017 (operating guide).
Assess conditional 025/026/028/032/033 separately. Do not duplicate these
outcomes or claim completion of later PBIs. Any genuinely new proposal remains
in the E.2 proposal record with value and acceptance signal until promotion
through the backlog skill and Product Owner decision.

Proposed dependency order to validate from findings: settle source/policy and
capture identities → reproducible native initial release → compatible change,
preservation and safety gates → tests/audits and pipeline integration →
team-centric and feature-centric comparison with central DEV synchronization
→ accept stabilized technology/toolchain → E.5 complex Foundation upgrades.
Map each stage to existing assignments, prerequisites, exit evidence and
decisions. This is an assessment roadmap, not automatic rescheduling of E.3–E.5.

### Walkthrough, handover and documentation

Prepare `sprint_E.2_increment_demo.md` and its matching editable `.pptx`,
`user_manual.md` and `sprint_E.2_handover.md`. The walkthrough starts with the
retained baseline and preflight, inspects X1, performs X2, inspects/repeats X3
including failures/corrections, then opens finding sources, existing backlog
coverage and dependency decisions. Explain expected intermediate output,
restoration boundaries, copied source versus real authoring and pending checks.
Use portable Git-root discovery in verified commands.

If a guided runner is built, expose one entry with preflight, paused live and
unattended rehearsal modes and the same stages as the manual. GUI actions
require real operator input; rehearsal labels skipped human observations.
Store logs, outputs, screenshots and rehearsal receipts in `progress/E.2/tests/`.
Render and inspect all final slides, verify commands/links and reconcile README,
manual, deck, sources and findings. Demonstrate actual artifacts and runtime
actions to the Product Owner; record questions and an explicit decision before
handover acceptance or closure. No live-demo completion is claimed at this gate.

### Design decisions and remaining approvals

Use bounded native capabilities to test replacement hypotheses without
adopting a new production toolchain. Preserve retained E.1 evidence/data and
its existing uncommitted diagrams. Keep native authoring and Git acceptance
as separate boundaries; assess the policy choice rather than presuppose a
blocker. Resource estimates and savings remain unmeasured until evidence exists.

No design decision is currently requested. X1–X3 and their test scope are held
for reassessment against the separate analysis. Neither exercise selection nor
an experimental policy exception is approved. Any revised design must follow
the analysis conclusions and the managed approval gate before implementation.
