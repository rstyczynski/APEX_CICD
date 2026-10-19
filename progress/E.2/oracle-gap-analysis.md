# E.2 — Gap analysis and evolution decision

Status: prepared for Product Owner review. This report separates source support from actual
exercise observations; unexecuted capabilities and adoption decisions remain explicit. The motto is **Give
developers flexibility through stable, industry-standard tools and techniques.**

The [accepted analysis](sprint_E.2_analysis.md) owns the questions and requirement
trace; the [accepted design](sprint_E.2_design.md) owns the bounded exercises.
[Implementation](sprint_E.2_implementation.md) and [focused evidence](sprint_E.2_tests.md)
own actual execution. [PROJECT fit](project-fit-assessment.md) supplies the PF
criteria. [Backlog](../../BACKLOG.md) and [plan](../../PLAN.md) own priority and
scheduling; this report proposes dispositions without assigning later work.

Actual inputs and output are retained in the [run archive](tests/e2-20261019-01-evidence.zip) and [byte manifest](tests/e2-20261019-01-evidence-manifest.json). The [walkthrough](sprint_E.2_increment_demo.md), [manual](user_manual.md) and [handover](sprint_E.2_handover.md) provide inspection, reproduction and the pending live decision.

## Supported equivalences and coexistence

**Capture into Git is compatible with native authoring.** The Oracle paper
pages 12–14/29/32 describes Working Copies, Main integration and meaningful team
checkpoints exported to Git. These are stages of one collaboration journey.
Working Copies need not wait for Git acceptance. A team checkpoint is kept with
the Working Copy/Main flow, not introduced as a competing project mechanism.
Actual Compare identified the intended two page differences, selective Main-to-copy
refresh succeeded, and a transient ORA-08177 comparison failure recovered on a
read-only retry. Selected copy-to-Main merge succeeded. A controlled stale replacement was observed, recovered by restoring Main, selectively refreshing and explicitly reapplying the agreed edit. Deleting a page in the copy produced Missing differences; abandoning that unmerged copy left Main intact. Both edits survived native fresh/populated delivery and the lower-level fresh reconstruction from the same reviewed Main checkpoint.

**PROJECT can share a repository with retained project files.** An offline
initialization probe preserved all 56 frozen E.1 APEX/database input files.
A broader existing-Git probe preserved 117 of 118 frozen inputs but overwrote
README.md. Restoring its original bytes from Git succeeded; the generated README
was retained separately. Initialization therefore needs reviewed documentation
preservation as well as source-layout planning. This supports bounded physical coexistence. It does not make existing split APEX source
and hand-maintained migrations native PROJECT source/history. In the live owned
fixture, PROJECT generated monolithic importable APEX SQL plus readable YAML,
schema snapshots, staged Liquibase migrations and intentional custom SQL. Its
native path reconstructed an app in a mapped workspace/schema. One active
migration authority is required per delivery path; a conversion is a reviewed
handoff, not two tools writing the same live history. Oracle supports
[initialization in an existing repository and custom staged SQL](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/project-command.html).

**Shared-instance mapping is supported.** The paper pages 29–30 describes
properties and a defaults-file installer hook. The actual mapped candidate
installed Main's source as app 821789 in E2_0254C95F_F, preserving author Main
821788. Generated installation clears APEX session overrides, so pre-setting
session setters is insufficient for this path. The bounded defaults-file hook
is Oracle-recommended configuration, not evidence that mapping is incompatible.
Separate instances remain another topology; this exercise does not prove them.

**Useful E.1 controls can surround a native artifact.** Reusing the existing
explicit compatibility validator avoids duplicating its bounded rules. The native ZIP also carried the exact reviewed component declaration after placing its sole canonical source under dist. A separate custom declaration carrier is unnecessary for this qualified path. The
E.2 envelope binds archive/source/declaration/target state; it is a custom
assessment bridge, not native PROJECT component-dependency enforcement. Real patch-candidate negative observations rejected incompatible/missing/unknown
declarations, changed archive bytes and a missing receipt before native deploy,
with the real target unchanged. The combined candidate carried the exact declaration and passed fresh qualification before populated delivery; final rejection observations are recorded in the evidence ledger. E.1 capture/controller/archive
assumptions prevent an unchanged-tool claim for those helpers.

## Observed gaps and tool constraints

**Native verification is a current release blocker.** Pinned SQLcl
25.3.0.274.1210 stages slash-containing branch names into a sanitized directory,
while verification searches an unsanitized path. A slashless branch removes
that error. Initial full verification claims the APEX source is missing from
stage.changelog, although native staging includes it through the separate APEX
changelog in main.changelog. The later Working Copy comparison reports all six source SQL files missing from stage.changelog while other checks report source/distribution correspondence and 13 readable included scripts. These are retained observations requiring diagnosis; the precise defect or configuration cause is not established. All observed archives are prerelease candidates;
no formal release is claimed. The documented
[release prerequisites](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/project-command.html)
require successful verification and build/data qualification. A failed verify
must never be hidden by its success process status; the helper checks its
Errors summary. This is scoped evidence from one client/fixture, not a claim
that all versions fail.

**The retained native-import failure is not a universal incompatibility.** E.1's
historical import evidence remains unchanged. A fresh pinned lab now successfully
imports the bounded generated app through native delivery. This supports a
runtime/state-specific interpretation of that historical blocker; it does not
establish its exact historical root cause or qualify the entire E.1 app under
native import.

**Version labels are not component contracts.** The paper page 27 explicitly
permits arbitrary artifact name/version values. A 1.0.1 label does not determine
whether a changed LOV return value, package signature, data meaning or shared
component behavior is breaking. PROJECT-generated object ordering and
Liquibase execution history address different dependencies from the declared
Foundation/Hello/World compatibility contract. Keep explicit declarations known
to the toolchain; PBI-052 already owns contract/SemVer mapping. Automatic change
classification is a later question, not an Elaboration exit condition.

**Background-job capacity affects usability.** Working Copy Compare succeeded;
Refresh initially waited in a fresh lab with a single job worker in both CDB/PDB.
Read-only inspection found other scheduler work occupying capacity. Treat the cause as a queueing hypothesis; completion alone does not establish causality. [APEX 24.2](https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/about-working-copies.html)
requires enabled jobs and checking CDB limits; the
[Database 26ai scheduler guidance](https://docs.oracle.com/en/database/oracle/oracle-database/26/admin/oracle-scheduler-concepts.html)
explains root/PDB worker limits. The Product Owner approved raising CDB/PDB limits to 10; both are now 10.
The pending comparison completed before that adjustment, so it cannot establish
a before/after performance improvement. Later operations are observed separately. Do not turn this observation into a general incompatibility.

**Mapped replacement changed physical identities.** Before/after observations
on U/app 821790 show every observed region ID changed on the combined candidate
import. For example, page 2 History changed from 7959627147038641 to
9159623420264500. The generated wrapper clears installation context and generates
an offset for mapped app/alias overrides. Stable runtime component identity is
therefore unfulfilled by this observed path, even though exact retained rows,
LOV values, greeting and both page document titles passed. No private saved-report
loss was measured. Existing E.1 public-API fixed-offset evidence suggests a
solution direction; adapting/qualifying a native wrapper or a different topology
remains follow-up under PBI-020/029/037/038. A fixed-offset fresh lower-level
reconstruction succeeded using the documented [SET_OFFSET API](https://docs.oracle.com/en/database/oracle/apex/24.2/aeapi/SET_OFFSET-Procedure.html), but does not prove changed-import preservation.

## Policy conflicts and avoidable custom work

Break-glass-only Builder authoring and component-wide reservations were E.1-stage
project policies. They do not establish an Oracle prohibition on ordinary
Working Copy authoring. [Page locks](https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/locking-and-unlocking-a-page.html)
coordinate page edits; they do not provide
schema isolation or prove component-level reservation equivalence. Reevaluate
policy with observed usability and recovery, without removing proven controls
before a replacement meets the same requirement.

Prefer native capture/staging/custom SQL and mapped deployment where qualified.
Avoid wrapping PROJECT in an imitation of every E.1 controller operation, a
second source tree maintained by hand, a second dependency validator or a custom
SemVer parser merely to label this fixture. Preserve custom controls only for
requirements the native path has not established: ownership, admission,
provenance, drift/failure recovery and scenario-specific runtime protection.

## Component interfaces and complementary validation

[APEX 24.2 subscriptions](https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/using-shared-component-subscriptions.html)
are one scoped dependency mechanism within the component
contract. The contract must state producer/consumer, source-of-truth and refresh
policy, consumed return values/types and observable behavior. A LOV label change
may be compatible while a changed return code or narrowing of permitted values
may break a consumer. A subscription's refresh state is operational metadata;
it does not prove compatibility or advance a component version automatically.
PBI-052 defines major/minor/patch policy for these changes. Component dependency
admission must know which contract version a consumer requires.

Combine checks around the same candidate identity: PL/SQL assertions and
utPLSQL for database behavior; coverage to identify unexercised code; native
application audits for detectable metadata issues; browser acceptance for
observable journeys; dependency admission for declared contracts. Coverage is
not correctness, an audit is not compatibility, and a successful import is not
a complete user journey. Retain inputs, tool versions, result/evidence and the
failure effect for each check. Pipeline placement is the eventual destination,
not a separate local-versus-hosted feature. Full suites remain E.3/E.4 work.

## Backlog reconciliation and dependency-ordered roadmap

1. Stabilize source/policy/identity decisions and reproduce the native verification
   finding under PBI-028/029/037. Qualify any toolchain fix or selected replacement
   version on this retained fixture. Do not create duplicate backlog items for
   the same toolchain stabilization outcome.
2. Complete capture/staging/reconstruction and immutable artifact handoff under
   PBI-020/037/038. Decide the single migration owner and any one-time E.1 conversion;
   retain lower-level export/import as a qualified alternative where appropriate.
3. Qualify Working Copy coordination/checkpoint capture and central synchronization
   under PBI-019/039/042. Replace E.1 authoring policies only after evaluating the
   same collaboration and protection requirements.
4. Carry admission, ownership, drift, recovery and independent provenance through
   PBI-021/022/023/024/031/045. The assessment envelope does not complete these
   production protections. PBI-052 supplies explicit component-contract SemVer
   rules; it remains Proposed and unscheduled.
5. Compose utPLSQL/coverage, native audits and browser checks under PBI-034/040/041,
   then operate the accepted contracts in pipelines under PBI-030/043. PBI-017/046/047
   cover operating guidance, independent reproduction and comparison.
6. Address compatible/breaking/in-place Foundation upgrades under PBI-048/049/050
   in E.5 after toolchain stabilization. No complex Foundation change is delivered
   by this sprint.

These are proposed refinements of existing items, not new root items or new
sprint assignments. The acceptance refinements and exit criteria below apply the retained exercise evidence; Product Owner prioritization remains separate.

## Analysis and fit dispositions

This is an assessment outcome, not adoption approval. The reduced fixture proves
the observed combinations only. Sources in the accepted analysis remain the
version-specific basis for findings handled without a new runtime exercise.

- **AN-01/02; PF-01–05:** supported SQLcl/export/Git primitives coexist. The
  observed native slice captures six intended objects, stages generated DDL and
  explicit DML, delivers initial/patch/combined candidates, and preserves bounded
  user data. Two no-edit source captures were stable. Full native verification
  blocks a formal release on this client. Unsupported object coverage and
  general semantic migration generation are not established by these six objects.
- **AN-03/13; PF-02/12; H-2/EQ-1:** native authoring, selective refresh/merge,
  recovered stale replacement, missing-page interpretation and abandonment were
  observed. Both agreed edits reached Git and reconstructed by both paths.
  Builder actions remain human authoring/review. No unsupported internal
  Working Copy management API was invoked and no unattended merge API is claimed.
- **AN-04:** page coordination remains distinct from schema isolation and
  component reservation. One operator exercised both edit directions; concurrent
  locking was not tested. Treat E.1 policy replacement as an explicit follow-up
  decision, not an achieved capability equivalence.
- **AN-05/09; PF-07; EQ-3:** shared-instance mapped deployment worked and avoids
  assuming separate-instance necessity for every goal. Stable no-edit source
  is observed; a matched private branch instance is not. Shared schema visibility
  is observed through actual Main/copy public query contexts. Changed mapped
  import regenerated region IDs; shared-instance delivery still needs an
  identity-preserving procedure.
- **AN-06/10; PF-10; EQ-5:** documented audits, utPLSQL/coverage and browser checks
  are complementary. No recommendation here depends on a new local Advisor
  defect, so no synthetic audit exercise or framework installation was needed.
  Full integration stays with existing validation backlog items.
- **AN-07/08; PF-09/11; EQ-4:** pipeline placement is future work. Actual
  candidate/target admission observations establish the bounded bridge only;
  production provenance, concurrent fencing and partial-DDL recovery remain
  gaps. E.1 receipts/code remain historical comparison, not newly reproduced
  controls. Do not remove safety requirements merely because native migration
  tracking exists.
- **AN-11; PF-08:** subscriptions/component groups are scoped optional reuse,
  under PBI-044. They are dependencies within the component interface contract.
  Native packaging carried the exact contract; the E.1 validator enforces
  explicitly supported combinations. No native general SemVer/range resolver or
  automatic change classification was established. Oracle's arbitrary artifact
  version label is insufficient evidence of either. PBI-052 owns the mapping.
- **AN-12:** RUP files provide comparable milestone/issue-planning purpose.
  Oracle Team Development's full journey was not demonstrated. PBI-036 owns
  whether to demonstrate or deliberately exclude it; a second tracker adds no
  proven value here.
- **AN-14; PF-06/12; H-1/EQ-2:** existing-Git initialization and native lifecycle
  are viable bounded routes, with README preservation and version-specific
  diagnosis required. This is not a verified brownfield baseline adoption of
  the full E.1 database/history. Keep PROJECT optional and qualify a reviewed
  one-time handoff before changing the product's migration authority.

## Follow-up acceptance refinements and exits

These refine existing outcomes and are proposals for Product Owner assessment.
They create no new root backlog item or assignment. PBI-052 is already Proposed
and unscheduled; none of the later items is delivered by this sprint.

1. **Toolchain and identity — PBI-028/029/037, with 020/038.** Retain this exact
   fixture and client diagnostics. Exit: successful full verify on the selected
   pinned route, explained branch handling and stable required IDs across a
   changed populated import, or an explicitly accepted qualified alternative.
2. **Capture/adoption/artifacts — PBI-020/037/038.** Prerequisite: selected route
   and identity policy. Exit: reviewed baseline conversion, Main-only scope,
   README/source preservation, one migration owner and immutable qualified
   bytes. Prefer native declaration carriage already observed over another
   custom archive layer.
3. **Coordination — PBI-019/039/042.** Prerequisite: agreed authoring and capture
   boundaries. Exit: evaluate multi-developer contention, stale replacement,
   unsupported/deleted metadata and abandoned work against the required
   protection goals; decide whether page/native coordination replaces any
   component-wide reservation policy. Keep team checkpoints with this journey.
4. **Admission and recovery — PBI-021/022/023/024/031/045; PBI-052 policy.**
   Prerequisite: stable component contract, artifact and target identities. Exit:
   native-carried declarations, installed-state reconciliation and independent
   admission/provenance plus required drift, interruption and repair evidence.
   The current bridge is a disposable prototype, not the production answer.
5. **Combined validation and pipelines — PBI-034/040/041/030/043.** Prerequisite:
   stable candidate/admission contracts. Exit: each selected check consumes the
   same candidate identity, retains results and blocks promotion on failure or
   stale evidence. PBI-017/046/047 cover guidance, independent reproduction and
   comparison. Their exit includes an independently repeatable actor journey.
6. **Foundation evolution — PBI-048/049/050 in E.5.** Prerequisite: stabilized
   toolchain, artifact/contract admission and recovery controls. Exit: compatible,
   breaking and in-place Foundation scenarios with their own preservation and
   availability evidence. No complex upgrade is pulled into E.2.
