# E.2 — Focused exercise evidence

Separate automated tests/regression: not applicable by Product Owner direction.
This record reports actual observations against the
[accepted design](sprint_E.2_design.md#exercise-verification) and
[implementation](sprint_E.2_implementation.md). It does not declare runtime
success from file existence or unit-injected outcomes.

## Initial read-only runtime inventory — 2026-10-19

`podman machine list` reports apex-cicd running. Both
`podman --connection apex-cicd ps -a` and the apex-cicd-root equivalent have
no containers; both connections' volume inventories are empty. A loopback
ORDS HTTP request fails to connect. No provisioning/rebuild/reset was attempted during this read-only inventory.
Pinned local SQLcl and Java executable paths exist; runtime versions have not
yet been observed. Outcome at inventory time: blocked runtime prerequisite. The Product Owner then
authorized fresh lab provisioning with the pinned installation procedure; the
following observations supersede that initial prerequisite status.

## Preparation and actual capture

The pinned database/APEX/ORDS procedure completed successfully. Observed database
23.26.3.0.0 and APEX 24.2.0 VALID, zero invalid APEX objects, HTTP 200 from ORDS.
Local run `e2-20261019-01` binds database ID 1514744599, FREEPDB1, three owned
schema/workspace pairs and an isolated PROJECT Git repository. Native Builder
created Main 821788 with pages 0/1/2/9999, E2 History interactive report and
E2 GREETING WORDS dynamic LOV. [Actual LOV screen](tests/e2_main_lov_created.png).

PROJECT export inventory: three tables, one package spec, one package body and
one Main application. No ownership marker or business rows in source capture.
The SQLcl defaults produce an importable monolithic APEX SQL source and readable
YAML; this is different from E.1's split SQL profile and is not unchanged-layout
compatibility. Original IDs are explicitly enabled. Source checkpoint in the
local experiment Git repository: `1bdeb727c7c1ca53293138c783401d78b79046c3`.

## Native staging and verification findings

`project stage -branch-name e2-empty-base` first rejected a tag-only checkpoint.
An actual branch at that exact retained commit allowed native staging. A sandbox
restriction also blocked JGit's normal external configuration write; approved
escalation allowed it. These causes are distinct from an Oracle product failure.

With branch `codex/e2-initial`, stage wrote `changes/codexe2-initial`, whereas
verify expected `changes/codex/e2-initial`. Selecting a slashless branch removed
that error. Verification still reports one error: the APEX SQL file is absent
from stage.changelog, although the native generator places it in a separate
`dist/releases/apex` changelog included by main.changelog. Formal release is
blocked; no passing full verification is claimed. Native verification initially
returned a success process status despite its nonzero Errors summary; the helper
now rejects that summary explicitly.

The first generated archive was not deployed. Inspection found that generated
APEX installation clears prior session overrides. The Oracle paper pages 29–30
provides the appropriate defaults-file mapping hook. The disposable installer
uses it, enables DEFINE for the hook, and supplies exact `appId` spelling used
by this pinned generator. Candidate mapping/deployment is under observation;
no release qualification is inferred from archive generation.

### Existing-repository initialization probe

The first scoped probe preserved 56 APEX/database files. A broader probe in an
existing local Git repository included 118 frozen README/APEX/database/deploy/
configuration/release files. Native PROJECT init changed README.md and preserved
the other 117. The generated README was retained separately and the original
README restored byte-for-byte from the frozen Git commit. Only the disposable
probe was modified. This is a bounded adoption hazard and a demonstrated Git
recovery, not unchanged full-repository compatibility or a change to E.1 history.
An unsupported `-config-only` syntax probe was rejected before the successful
plain-init probe; only exact-client documented syntax is used in the recipe.

### PROJECT additive patch and repeat

The saved Builder page 1 title E2 Hello patch and app version 1.0.1 were captured.
A field-fill attempt initially did not update the Page Designer model; the saved
database-title assertion failed. Keyboard typing produced the named Undo change,
Save persisted it, and the assertion/export then captured the intended title.
This was an operator automation correction, not evidence of an Oracle merge bug.

Native stage generated ALTER TABLE E2_SETTINGS ADD RELEASE_NOTE and a separate
reviewed custom changeset for Hello 1.0.1 metadata/LANGUAGE=en. Source revision
`37a796cf8a0281b1aa7a61df314d3e71bd9b1f54`; distribution revision
`786ad443ec23c685311b58d178ca29f522c2cf70`. Candidate SHA-256
`bf02e280dea9091f94f5bb2f9894cc41ad2fded0b689a35f4c2a43182501fe91`
installed from empty in a newly allocated owned F2 target, keeping F intact.
It also upgraded U using 3 changed changesets, with 6 previously run. Repeat
ran 0 with 9 previously run. Both upgrade and repeat preserved USER_PREFIX and
all recorded history fields, including timestamp 2026-10-19 16:16:11.821787.
Greeting remains Hello World and Foundation/World remain 1.0.0. Full native verify
still reports one error. These are prerelease candidate outcomes, not a frozen
release. Section B records that assessment explicitly; Working Copies follow it.

### Working Copy observations in progress

Native Builder created Working Copy 101, E2 coordinated edit, from Main 821788
after X1 candidate qualification. Public APEX_SESSION/APEX_EXEC contexts for
both applications returned the unique e2-20261019-01 marker from author schema
E2_0254C95F_A; the result is retained in shared-schema.json. Page 1 Title was
saved as E2 Hello working copy in the copy; Main page 2 Title was saved as
E2 History Main. Compare Changes completed with 2 Changed, 0 Added, 0 Missing.
Its page 1 YAML viewer shows exactly E2 Hello patch versus E2 Hello working copy.
Screens: [comparison](tests/e2_working_copy_two_changes.png),
[title diff](tests/e2_working_copy_title_diff.png). The initial background-loading
view temporarily said zero differences while its progressbar was active; the
operator waited for the completed result before deciding. Selective refresh and
merge remain in progress; no successful combined checkpoint is yet claimed.

### Working Copy background-job capacity

Compare completed with two intended page differences. Refresh is waiting with
its progressbar active. Read-only inspection found JOB_QUEUE_PROCESSES=1 in both
CDB$ROOT and FREEPDB1. APEX's earlier APEX$DIFF job completed with ERROR# 0; an
APEX background process occupied the PDB worker, and a root scheduler session
was also observed. This supports a capacity/queueing hypothesis, not an intrinsic
Working Copy incompatibility. The 24.2 Working Copies reference requires enabled
background jobs and checking the CDB setting. The Database 23 administration
guide explains that the root caps total scheduler workers and PDB limits also
apply. A proposed fresh-lab adjustment to 10/10 is awaiting explicit managed
approval; it has not been executed. Current selected resources and edits remain
retained. The proposed SQL is local preparation only.

### Approved scheduler adjustment and selection review

The Product Owner approved 10/10 fresh-lab scheduler limits. The existing Refresh
comparison had already completed with 2 Changed before adjustment; no improvement
is attributed retroactively. A DBID-checked SQL session changed CDB root from 1
to 10; FREEPDB1 then inherited 10 and was explicitly set to 10. The saved
[before/after output](tests/scheduler_capacity_20261019.txt) records the sequence.
The accepted design has the narrowly approved addendum. No pinned E.1 installer
or historical evidence changed. Later comparisons use the adjusted lab.

The Refresh selection initially defaulted to both changed pages. Confirmation
review caught this before applying. Returned to Previous, deselected page Home,
and verified the confirmation listed only PAGE:2 with Backup target app first
checked. [Selection proof](tests/e2_working_copy_selective_refresh.png). Confirm
Refresh has been submitted; final success/combined headings remain to verify.

### Selective refresh succeeded; comparison retry

Builder confirmed Your changes have been successfully refreshed. Saved-state
inspection shows copy page 1 still E2 Hello working copy, copy page 2 now
E2 History Main; Main page 1 remains E2 Hello patch and Main page 2 remains
E2 History Main. The subsequent Merge comparison displayed ORA-08177 before
selection/confirmation; [failure screen](tests/e2_working_copy_compare_ora08177.png)
is retained. Oracle's [error guidance](https://docs.oracle.com/en/error-help/db/ora-08177/)
says to retry the intended operation/transaction. Reopened copy home and retried
only the comparison. This does not prove the scheduler adjustment caused the
serialization conflict, and no successful merge is claimed yet.

The separate patch-candidate negative admission exercise rejected incompatible
Foundation metadata, a missing dependency, an unknown version, changed archive
bytes in a temporary copy and an absent receipt. Original archive/receipt were
restored/preserved and the real populated target's observed definitions/data
were unchanged. Native deploy was not reached. This is observed bridge behavior,
not native component-contract enforcement. It will be bound again to the final
Working Copy checkpoint if that combined path succeeds.

### First combined Main outcome

The comparison retry completed with one changed page (Home/PAGE:1). Confirmation
listed only that page, Backup target app first checked and Delete Working Copy
after merge unchecked. Builder confirmed the selected merge succeeded. Main's
saved page titles now include both E2 Hello working copy and E2 History Main.
This is the first successful combined authoring result; stale-edit recovery,
deletion/abandonment and capture/reconstruction still follow. The first failed
comparison remains evidence and is not counted as a successful merge.

### Deliberate stale same-page replacement

Saved Main page 1 as E2 Main retained edit and the copy's page 1 as
E2 stale copy replacement. The [native two-way diff](tests/e2_working_copy_stale_diff.png)
showed both values, but selection still classified the page simply as Changed.
Selected PAGE:1 with a target backup and confirmed the controlled stale merge.
Builder reported success; the saved-state assertion observed Main's title changed
to E2 stale copy replacement while page 2 remained E2 History Main. This is the
documented replacement behavior and an observed lost Main edit, not an automatic
three-way conflict resolution. No component-reservation equivalence is inferred.

Recovery restored the reviewed Main value through Builder, then selected only
PAGE:1 for Refresh Working Copy. The refresh is being verified before explicitly
reapplying the agreed final title. Same-field conflict resolution requires a
deliberate chosen value; both conflicting titles cannot coexist in one field.
This is one operator using separate authoring contexts, not measured concurrent
user/page-lock contention.

### Completed Working Copy recovery, deletion and abandonment

Restored the controlled stale Main edit, refreshed only page 1, explicitly
reapplied the agreed Working Copy title and merged only that page with native
backup selected. Saved Main titles were verified as E2 Hello working copy and
E2 History Main. Deleted page 2 only in disposable Working Copy 101. The completed
Compare report showed 1 Changed (Navigation Menu) and 3 Missing (page, list entry,
breadcrumb entry). This was not a Main deletion instruction. Main retained page 2.
Abandoned the unmerged deletion using native Delete Working Copy; Builder
confirmed copy 101 deleted and returned to Main with pages 1 and 2 present.
Screenshots: [missing components](tests/e2_working_copy_missing_page.png) and
[abandoned copy, Main retained](tests/e2_working_copy_abandoned.png).
The removed shared-schema probe is excluded from the next capture. No concurrent
second developer or native page-lock contention is claimed.

### Combined candidate reconstruction and identity result

Native candidate 938c468b70c017d98780064e4b4d9de3b46d19fcee85de3a12c32d2e4a80ce38
installed nine changesets in new F3/app 3821789. Fresh qualification and both
expected page titles passed before promoting the exact same bytes to U/app
821790. U ran one changed APEX changeset/eight previous. Exact retained history
fields and USER_PREFIX survived. Public LOV SQL executed with HELLO→Hello and
WORLD→World and the actual greeting returned Hello World on both targets.
Browser inspection of U confirmed both page document titles and displayed the
retained history row. The runtime region heading remains E2 Lifecycle/History;
page Title is the document title, not a changed region heading.

Replacement identities did NOT survive: page 1 region
7776626377022974→8976622650248833; page 2 History region
7959627147038641→9159623420264500. The other observed regions also changed.
Generated XML clears installation context and generates an offset for mapped
app/alias overrides. No offset property is present in that inspected wrapper.
This demonstrates a gap for this mapped replacement path; it does not establish
private saved-report loss or universal Oracle incompatibility. The unchanged
E.1 identity test remains evidence for its own public-API importer only.

Lower-level comparison exported the same Main as native split/original-ID/no-date
source and reconstructed its five schema SQL files plus intentional seed/patch
in new F4/app 4821789. Both expected titles, LOV return/display values and greeting
passed. Fixed owned offset 40111007300000 was applied through public
APEX_APPLICATION_INSTALL setters. This is one fresh reconstruction, not proof of
changed-import identity preservation, native migration-history equivalence or
complete E.1 controller behavior. No parallel live source authority was created.

## Retained evidence and rehearsal receipt

[Run archive](tests/e2-20261019-01-evidence.zip) and
[byte manifest](tests/e2-20261019-01-evidence-manifest.json) retain 505 files: native
candidates, redacted SQLcl logs, source Git bundle, comparison export, receipts
and screenshots. Known generated secrets were scanned and absent; private.json
is excluded. Final combined-candidate negative admission passed all five stated
rejections and exact observed target state remained unchanged.

An unregistered target role was refused before connection; see
[scope refusal](tests/foreign_scope_refusal_20261019.txt). Retained-run preflight,
launcher inspection and C/D completion-resume passed. E rehearsal stopped at its
actual human review checkpoint with exit 3. No fresh GUI observation, second
full new-run runner execution or Product Owner acceptance is claimed.
Bash syntax and Python compilation passed. Native verification remains a
retained expected failure; mapped replacement identities changed. These are
assessment findings with follow-up, not a false all-green product result.

## Desktop presentation repeat — 2026-10-19

At Product Owner request, repeated the screenshot views with a desktop viewport
requested at 1440×1000. The browser capture returned 1107×769 full images;
focused crops retain the relevant application identity, controls and values.
Created a separate disposable Working Copy named E2 desktop walkthrough
(APEX reused ID 101 after the original copy had been deleted). Changed its
page 1 Title, captured the two-column YAML comparison and selected PAGE:1
merge confirmation, but did not apply Confirm Merge. Deleted page 2 only in
that repeat copy and captured 2 Changed / 3 Missing (including its unmerged
page 1 change). Then abandoned/deleted the repeat copy through native controls.

[Main preservation receipt](tests/desktop_repeat_main_preservation.json) shows
identical observed Main definitions and rows before/after the repeat. The
original exercise captures, run ZIP, manifest and historical results remain
unchanged. New screenshots are labeled desktop walkthrough repeats rather
than contemporaneous evidence of the earlier stale merge/recovery.
The current deck uses [merge selection](tests/e2_desktop_repeat_merge_full.jpg),
[two-column comparison](tests/e2_desktop_repeat_diff.jpg) and
[missing components](tests/e2_desktop_repeat_missing_full.jpg). Corresponding full
images retain surrounding context. The temporary viewport override was reset.

### B recovery validation — user run e2-20261019-02

The user-driven new run completed initial delivery/repeat and preservation,
then stopped before patch SQL because the persisted Main page 1 title was
E2 Lifecycle rather than E2 Hello patch. Main is app 101 in E2_A9CF4097_A.
The application repository was clean on e2-patch at initial baseline 713b299.

Executed the new read-only `patch-resume` admission against the actual run.
Result: PRESERVED upgrade (exact recorded history fields and user setting),
then PATCH RESUME READY. Initial target definitions/rows matched the deployed
receipt; no initial deployment, patch DDL or app authoring was executed by this
validation. Three isolated guard exercises substituted wrong-branch,
dirty-source and started-DDL inputs and observed the intended refusals; these
were synthetic guard checks, not additional Oracle mutations. Shell/Python
syntax and git diff whitespace checks passed. The user's resumed interactive
patch execution is not claimed by these checks.

## Full-application mapped integration observation — 2026-10-20

The [mapped candidate receipt](tests/project-integration-mapped-validation.json)
records the exact ZIP, source/distribution commit and snapshot digest. Native
deployment passed with 23 initial changesets; application 810004 is owned by
E1_INTEGRATION, all three component versions are 1.0.0 and business packages/
triggers compile. VERIFIER browser login, greeting and history passed; native
restricted access blocked LAB_USER. Native APEX publication then allowed
LAB_USER greeting/history, preserving the verifier row. Identical-artifact repeat
ran zero changesets and retained every history/configuration field. Exact guide
restriction/publication SQL blocks passed as written.

Native verification is not all-pass: one `stagechangelogcomplete` APEX completeness
error remains. The generated DATABASECHANGELOG_DETAILS view is also invalid;
business objects are valid. These observations do not qualify a formal release,
UAT promotion or later upgrade. Native transcripts and 1280×720 screenshots are
retained under tests/project-integration-*; no new automated test suite was added.

## Same-byte UAT promotion prototype observation

Observed all five prototype actions against the prepared lab. First UAT install
ran 23 changesets from D's exact ZIP, mapped to 810005 / E1_UAT. VERIFIER browser
greeting/history, LAB_USER restriction, native publication and LAB_USER greeting
passed. The retained `UAT:` prefix affected a new greeting while two earlier
Hello World snapshots kept their original fields. Captured and compared all
fields of the three histories, both entries and both configuration rows.
Repeat deployment ran zero changesets; repeated baseline capture preserved file
bytes. Hash mismatch, missing explicit assessment mode, changed prior history and
changed settings were rejected by focused prototype checks; added history was
allowed. These are Elaboration exercises, not a new test suite or formal release
pass. [Receipt](tests/project-uat-promotion-validation.json) and
`tests/project-uat-prototype-*.txt` retain results; desktop browser captures are
`tests/project-uat-*.jpg`.

## F1 focused native authoring/capture rehearsal — 2026-10-20

Passed on separate Main 810103 / Working Copy 101: native create; two saved
disjoint page edits; completed comparison (pages 1 and 10); refresh only page 10
with backup; merge only page 1 with backup and retained copy; both headings
present in Main/copy metadata; native Main backup visible. PROJECT list/export
with the original filter selected only operator Main 810003, left Git clean
and excluded the private copy. A rehearsal-only filter selected 810103 and
captured both intended headings in SQL/readable YAML, excluding 101; the capture
was committed in the isolated rehearsal repository.

The browser automation initially populated editor fields without updating the
Page Designer model. Read-only metadata detected the unsaved edits; entering
through keyboard events, leaving the field and saving corrected the rehearsal.
Only the later persisted edits are counted. The operator steps explicitly
require Tab, Save, completion and metadata/export checks. A queued comparison
at scheduler capacity 1 completed after the previously approved capacity 10
was reapplied. No automated test suite was added.

[Receipt and limits](tests/project-f1-working-copy-validation.json),
[metadata](tests/project-f1-main-copy-metadata.txt),
[native export](tests/project-f1-export-rehearsal-main.txt),
[Main after merge](tests/project-f1-merge.jpg) and
[backup screenshot](tests/project-f1-backup.jpg) retain evidence. The Product
Owner's runtime checks on Main 810003 after its future merge are not claimed
executed. F2 component upgrade/delivery remains pending.

## F.2 focused native compatible-upgrade exercises — 2026-10-20

The [F.2 receipt](tests/project-f2-upgrade-validation.json) records the exact
candidate SHA-256 and source commit, target identity and limits. Native runtime
results passed on E1_INTEGRATION/application 810004:

- Fresh cumulative candidate: 26 executed, none previously applied; Foundation
  1.0.0 / Hello 1.0.1 / World 1.0.0; tab/newline normalization and whitespace-only
  rejection passed with rolled-back verification inserts.
- Original initial reconstruction: 23 executions. New literal QUAL: prefix and
  QUAL:Hello World history were created through a native APEX VERIFIER session;
  these are synthetic qualification fixtures, not restored business snapshots.
- Populated upgrade of the identical candidate: 4 executions / 22 previously
  applied. Exact-field JSON comparison passed across native project deploy,
  retaining the prefix, default, entries and every history field.
- Actual browser checks on both starts: VERIFIER greeting/history, ordinary-user
  denial with the explicit message, native publication, and ordinary-user greeting.
- Completed-deployment repeat: 0 executions / 26 previously applied; Available
  and complete business-field equality retained.
- Negative probes: the native comparator rejected an uncommitted changed prefix
  with ORA-20890, followed by SQLcl failure rollback. The integration reset refused
  the author identity with ORA-20896 before destructive statements. Final checks
  confirmed the probe did not persist and UAT stayed unchanged.

Native verify remains Errors 1 / Warnings 0 / Info 7. The failed completeness
check lists initial files now in frozen release 1.0.0 and separate APEX source;
this is not recorded as a native release-gate pass. A discovery clone initially
lacked a local e2-world branch; stage reported an error despite a later generic
completion message. Creating that local ref fixed staging. The operator repo's
final stage succeeded against its existing local e2-world branch.

Exact relative @paths and author-input repeat/export were exercised. Native
business snapshot/assertion scripts were tested in one SQLcl session, including
across deployment. They require comparison before browser writes and do not
replace E6's durable baseline. No new automated smoke/unit/integration suite was
introduced. UAT promotion remains for operator execution; no such pass is claimed.

### Operator candidate: empty custom changeset detected

F.2.3's component check rejected execution-r1: Hello remained 1.0.0.
Inspection confirmed its packaged hello_1_0_1_version.sql contained only the
generated Liquibase header. The working file was populated with the reviewed
release-data SQL; exactly one generated header and version update were verified.
The regular walkthrough now checks that content before generating execution-r2
and qualifies r2 from the explicitly reset integration target. The r1 archive
is retained as failed-candidate evidence. No target version was patched by hand,
and this correction does not establish that r2 has passed runtime qualification.

### Product Owner execution report — F

On 2026-10-20 the Product Owner reported “F completed.” This records operator
completion of the Working Copy and compatible Hello patch journey, including
fresh/populated qualification, same-artifact UAT delivery, preservation and
repeat checks. It does not replace execution transcripts or close the unresolved
native PROJECT verification finding. G–I and final acceptance remain separate.

### G — focused rehearsal before operator execution

Evidence: tests/project-g-incompatible-validation.json and the two
project-g-native-*.txt transcripts. Native supported/incompatible verification
outputs were identical: Errors 1 / Warnings 0 / Info 7, with the retained stage
completeness finding. There was no new component-dependency diagnostic.

Three real-target rejection rehearsals used the existing validator and each
reported zero PROJECT deploy invocations. Exact UAT business rows, component
state, changeset history, schema DDL, APEX export and availability matched before
and after. Retained-baseline check and prepare repeat also passed. The supported
declaration passed; missing dependency, unknown version, inconsistent dependency
and changed archive binding were refused. All G shell blocks passed bash syntax
checking; fixture paths and branch references were exercised. Browser inspection
is provided as an operator step, not claimed as an observed rehearsal. This is
focused prototype evidence, not a new automated regression suite.

### Native verification correction — supersedes accepting the G baseline error

See tests/project-verify-fix-validation.json and project-g-25.4.1-*.txt. The
corrected comparison clone passed native verification for both supported and
incompatible metadata: Errors 0 / Warnings 0 / Info 15. Two isolated negative
controls failed as required: removing a real Hello trigger changeset include,
and changing generated APEX status after staging. Both were restored afterward.
This demonstrates that the new pass did not result from disabling verification.

The older 25.3 outputs remain historical evidence. The 26.3 trial removed the
original completeness finding but required additional configuration migration;
it was not adopted. The qualified 25.4.1 path and separate connection store are
documented. Hash comparison confirmed both completed F archive bytes unchanged.
UAT definitions/data are checked independently by G's retained snapshot. This
read-only comparison work is not a new application deployment or Foundation
upgrade. Operator completion of the corrected G steps remains pending.

### H — focused pre-operator qualification

Receipt: tests/project-h-drift-validation.json. Final native transcript:
tests/project-h-native-rehearsal.txt. A controlled integration banner edit was
visible in native exports and the browser. An unchanged F artifact replay
succeeded with Run 0 / Previously run 26 and left the edit present. The selected
attribute was restored with the native API; every exported YAML definition
matched the accepted baseline after the explicit internal-revision exclusion.
Business rows/fields and changeset history matched exactly. Publication and
installed components were unchanged. Separate desktop browser captures record
the banner before/after the native repeat and its absence after restoration.

Exploratory raw checksum equality after restoration failed: source SQL differed
in p_version_scn/checksum and readable YAML differed only in root subscription
version-number. This finding motivated the narrowly stated comparison policy;
raw equality was not falsely recorded as passing. Final documented sequence
passed with that explicit policy. Missing/different expected outcomes and an
additional unexpected attribute caused the file comparison to fail. Wrong
schema/application ownership was refused before any edit. Actual UAT preflight,
business snapshot equality and 24-file native export passed read-only. Rendered
Bash blocks passed bash -n without heredoc warnings. No automated test suite
was added, and operator H completion is not claimed.
