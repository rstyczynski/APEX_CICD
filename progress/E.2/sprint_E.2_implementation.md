# E.2 — Implementation record

Status: under_construction

The Product Owner accepted the [design](sprint_E.2_design.md) on 2026-10-19
and directed implementation using the project RUP method. PBI-051 is active;
its [child outcomes](sprint_E.2_design.md#scope-decomposition) and
[board](../../PROGRESS_BOARD.md) own scope/progress. The
[elaboration summary](sprint_E.2_elaboration.md) records design acceptance.
[PLAN](../../PLAN.md) sets Test: none and Regression: none: section observations,
failure evidence and reproducible handover replace separate test suites.

## Construction baseline and preservation

Construction started at commit `3cbc3e5fef64388f33ffddc91831945499899a39`.
The unrelated E.1 diagram backup working edit is preserved and excluded.
No E.1 application/controller source is changed. Only owned E.2 resources may
be provisioned; missing infrastructure is not silently rebuilt.

## PBI-051.1 — Preparation and safe inputs

In progress. Read-only inventory found the apex-cicd VM running, with no
containers or volumes on either apex-cicd or apex-cicd-root. ORDS on loopback
8080 refused connection. Local pinned SQLcl/Java files exist. This establishes
a missing runtime prerequisite, not an Oracle lifecycle blocker. Asked the
Product Owner to choose fresh pinned provisioning or an existing restore path;
the Product Owner selected fresh pinned provisioning. Database startup completed
using the existing pinned procedure. Verified the APEX installer SHA-256. The
copied ZIP initially had unreadable permissions for the Oracle image user;
changed only that fresh installer file to readable and extraction completed.
APEX installation/configuration and ORDS installation completed. Database verification
reports APEX 24.2.0 VALID, no invalid APEX objects, and open gateway accounts;
ORDS responds with HTTP 200. This is a fresh runtime, not restored E.1 state.
Run `e2-20261019-01` owns three isolated schema/workspace pairs. Native App Builder
created Main 821788, its E2 History report and E2 GREETING WORDS dynamic LOV.

## PBI-051.3 — PROJECT first

Under construction. Build separate B section using the A-owned common
repository; consult exact-client help and official documentation before capture,
staging, generated/custom migration and deployment operations. Record direct
support versus bounded adaptation without assuming compatibility.

## PBI-051.2 — Working Copies after PROJECT

Designed, not executed. C will use B's repository and qualified capture path.
GUI evidence must come from actual compare/refresh/merge and reconstruction;
an unattended script may not manufacture those observations.

## PBI-051.4 — Findings and live handover

Designed. Final report, roadmap, presentation pair, manual, rehearsal and live
handover remain outstanding. No runtime equivalence or sprint completion claim.

## Implementation updates and evidence

This record is updated with concrete files, actions, failures, corrections and
remaining limits as construction proceeds. [Functional evidence](sprint_E.2_tests.md)
records focused observations rather than a separate automated test suite.
The following updates supersede the initial construction checkpoint; no child
is claimed complete until its exercise and documentation audit are finished.

### First implemented artifacts

Added the narrow Python utilities and disposable fixture SQL under
`tests/sql/oracle_lifecycle/`. PROJECT initialization was also exercised offline
with the pinned client: generated project configuration succeeds without a DB
connection. Its default expOriginalIds is false and generated git.defaultBranch
is main; the exercise sets identity/base choices explicitly. Exact-client help
is retained, including unsupported -help probes; these are syntax observations,
not successful export/deploy evidence. The implementation is still being completed;
no section or child is marked implemented.

### Owned fixture and preparation corrections

The first local helper initialization reached the PROJECT scaffold, then failed
on a nonexistent E.1 initial-manifest path. Recovery was confined to the
unprovisioned local scaffold; the declaration now derives the bounded initial
triple from the existing E.1 manifest. Historical E.1 publication/runtime fields
are removed rather than attributed to the E.2 native path. Section A/B scripts
and shared ownership/admission helpers exist but remain under construction.
The private run file contains generated lab credentials and is excluded from
tracked evidence. Native export is the next observation.

### Native PROJECT capture, staging and first reconstruction

Native capture produced Main application SQL/readable YAML plus three tables
and package spec/body, with the intended ownership/data exclusions. The initial
source and distribution are committed in the local experiment repository.
Stage requires a branch checkpoint rather than a tag alone. A slash-containing
branch exposed a stage/verify directory mismatch; selecting a slashless branch
removed that one error. Full verification still reports missing APEX source in
stage.changelog although native main.changelog includes its separate APEX path.
The helper now rejects native nonzero Errors summaries even when the process
returns success. Formal release remains blocked; no gate is waived.

The paper pages 29–30 mapping hook replaces ineffective session setters because
the generated APEX changeset calls clear_all. The bounded installer modification
uses defaults-file and exact appId spelling from the pinned generator. A first
archive-inspection helper incorrectly expected a dist/ archive prefix; inspection
showed install.sql at archive root and that guard was corrected before deployment.
The original unmapped archive was never deployed. Mapped candidate archive
SHA-256 `534d4e56ab18bb97127f5312ee29fe3b4154fc15aa9f6a6a842416228906774e`
installed successfully in fresh schema/workspace E2_0254C95F_F, app 821789.
Observed components are all 1.0.0 and greeting Hello World. SYS inventory confirms
Main 821788 remains in author workspace and the mapped application is distinct.
Fresh qualification records actual database checks, not GUI success. Populated
baseline/repeat, patch and Working Copies remain under execution. Native
prerelease assessment follows the documented gen-artifact path; formal release
cannot be called unless full native verification passes.

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

### Stale merge and recovery exercise

Observed the intended stale-page failure: native merge replaced the newer Main
Title with the stale copy Title. Main page 2 remained correct. The two-way YAML
diff made the values inspectable; the operator deliberately applied the controlled
replacement with backup retained, then restored Main and refreshed only page 1.
An explicit reapply of the agreed final value follows. This is evidence for
coordination policy, not native component-reservation or three-way merge proof.

The config-list verbose probe returned Unable to render the settings rather
than a configuration table. Its failure text is retained; no successful command
capability inventory is claimed. The helper now rejects that message. Static
tracked native configuration remains inspectable. A native declaration-carrier
trial is prepared: one canonical contract under dist for gen-artifact, with
legacy-path reading only for earlier candidates and rejection of dual authorities.
Native inclusion has not yet been observed, so no carrier support is claimed.

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

### Stable common-repository checkpoint

Two consecutive no-edit native PROJECT exports produced identical hashes for
every captured source file (capture-stability.json, zero changed paths). The
reviewed diff contains both intended page titles in Main SQL/readable YAML;
no Working Copy or ownership-probe capture is present. Scratch Git checkpoint
`d49bc94221777237845b55b8595ea0d56e42266d` also moves the sole canonical
component declaration into dist. Native ZIP inclusion remains an experiment
until generated bytes are inspected. The previous candidate checkpoints and
archives remain retained.

Full verification of combined distribution d5c3334486cac6300a0939a4d84bfcfe70627df9
again failed stagechangelogcomplete (1 error group). Against e2-before-working-copy
it listed all six source SQL objects as absent from stage.changelog, although
stagesourcediff reported that source/dist changes corresponded and all 13 included
scripts were present/readable. Preserve this distinct result; it is broader than
the initial candidate's APEX-only missing-source result. No formal release follows.

### Native declaration-carrier result

Native gen-artifact included dist/component-contract.json as ZIP-root
component-contract.json. Its bytes exactly match the reviewed declaration:
SHA256 a67bb9a2e471ce927031dd74d272877ea5290b471a3bc5466d55e19f481fe745.
Combined candidate archive SHA256
938c468b70c017d98780064e4b4d9de3b46d19fcee85de3a12c32d2e4a80ce38.
This removes the need for a separate custom declaration carrier for this path.
Native packaging does not enforce semantic dependency admission: reuse of E.1's
validator and candidate/target evidence binding remains explicit.

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

### Final negative observation and reproducibility

Final combined candidate negatives rejected incompatible Foundation, missing
dependency, unknown component version, altered copied archive bytes and absent
receipt before native deploy. The exact observed real-target definitions and
rows remained unchanged; original bytes and receipt were restored/preserved.
The public evidence bundle excludes private credentials and passed a scan for
known generated lab/platform secrets, including native ZIP entries and scratch
Git history. It retains failures as well as successful receipts.

A–D local checkpoints now record actual bounded outcomes. E remains at its real
Product Owner review checkpoint. Read-only preflight/inspection and C/D resume
were rehearsed without replay; E unattended rehearsal stopped with exit 3. A
second full new-run launcher execution is not claimed. The helpers are retained
as disposable lab/reproduction tools, not a production framework. No new
automated suite or generic regression claim was introduced.

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

## Independent operator walkthrough — 2026-10-19

The [new use-case walkthrough](cicd-walkthrough.md) supplies the E.1-style
operating journey separately from the retained-results presentation guide,
which the Product Owner instructed us to leave unchanged. It maps each existing
A–E pause to commands, explicit Builder operations, expected observations and
stop/recovery boundaries. It also describes a separate isolated existing-repo
PROJECT initialization experiment. No runner behavior was changed for this
addition. Static snippet/link checks passed; independent full new-run runner
execution and the new adoption recipe remain pending rehearsal. The document
is not evidence that those executions have occurred.

### Run-specific Builder credential retrieval

Extended the existing E.1 `cicd-password.py` single-credential helper with
`E2DEV --run RUN_ID`. It reads only that run's developer password and leaves
existing platform-key retrieval unchanged. The new walkthrough gives workspace,
username and the exact retrieval command at the Builder login step; manual
editing of the private store is no longer required. The helper rejects invalid
run IDs, unsupported run/account combinations and missing credentials.

### B pre-patch continuation correction

Product Owner authorized providing recovery rather than requiring manual script
steps or deleting the run. Added B `--retry patch`, narrowly scoped to the
failed pre-patch title/version boundary. It skips initial staging/delivery and
branch creation, validates the retained clean initial baseline, absence of
RELEASE_NOTE patch DDL, matching qualification/deployment receipts and unchanged
populated target, then repeats the normal Builder checkpoint. A repeated failed
title assertion prints the exact recovery command. Arbitrary partially applied
patches remain refused. Walkthrough B2 and the operating manual now provide the
supported command; the presentation guide is unchanged.

## Fresh full-application preload for the native SQLcl walkthrough

Recreated the explicitly reset apex-cicd machine with the pinned host/runtime
procedure. Database/APEX/ORDS health, sign-in and static-version checks passed.
Reinstalled the existing E1_CTRL packages and declared E.1 logical areas; loaded
reviewed Foundation, Hello and complete World snapshots using unchanged native
APEX exports and their original database changes. Private input provenance is
recorded and summarized in tests/project-preload-validation.json. The complete
application retains its E1_CTRL runtime dependency; no gate was stripped.

Prepared initial Hello/World entries/defaults and complete-assembly state, then
verified LAB_USER browser login, actual Hello World creation, the saved history
row and the three 1.0.0 component versions. Apps 810001/810002/810003 and native
saved connections are supplied; a restricted local login card supplies account
credentials without committing them. The operating guide's preparation-task list
was replaced by actual runtime URLs and connection commands.

Rehearsed native PROJECT init/configuration/export in a separate repository.
The exact client rejects the -type option shown in its configuration help
examples; -name/-value alone successfully preserves native Boolean types.
A first capture-filter attempt had a duplicate predicate separator; corrected
it, retained the failed private log, and verified capture of 24 objects including
Main and seven business tables. These checks do not qualify a native deployment,
upgrade, component-by-component PROJECT assembly, or replacement handover.

## E.1 journey alignment and explicit PROJECT capture

Aligned the native walkthrough's A–I chapter names and application outcomes with
E.1. Replaced the undefined checkpoint-selection actions with explicit saved
connections, schema/application checks, PROJECT configuration, capture filters
and Git operations. A/B/C are independent preloaded development assemblies;
comparing their different physical schemas as successive target migrations would
misrepresent E.1. The single application repository therefore retains separate
capture branches, while World supplies initial qualification/promotion and patch
lineage. No authoring application is rebuilt by these documentation changes.

An isolated private Git rehearsal executed the three native init/config/export
sequences against the existing owned sources. All passed; each branch captured
only its designated Main application. Native World staging against its configured
empty baseline also passed. The nonsecret receipt is
[project-component-capture-validation.json](tests/project-component-capture-validation.json).
No release target was written. Qualification, mappings/admission, promotion,
patch/protection and repair replays remain incomplete; capture/staging does not
close those gaps. E.1 artifacts and presentation Markdown were not edited.

## Explicit initial release-data input

Added `inputs/initial-release-data.sql` as a candidate payload for the native
custom changeset. It inserts fixed initial component/state declarations and new
Hello/World examples/defaults, with no history copying or existing-setting
updates. A schema allowlist and all-seven-tables-empty precondition reject use
on an authoring or populated target. The operator guide now gives exact append,
include-order and staged-diff checks while preserving PROJECT's generated header.

Oracle DBMS_SQL parsed the anonymous block against the existing author schema
without executing it; compilation passed. Shell syntax, header preservation and
repeat-append checks passed. No initialization data was applied. Fresh-target
initialization, target mapping/admission and complete delivery remain pending;
the guide identifies those as implementation work, not operator improvisation.

## Completed mapped initial integration exercise

Implemented and exercised the Oracle page-30 defaults-file installer hook with
packaged integration/UAT properties. The approved candidate-only adaptation
replaces the source fixture's E1_CTRL initialization call with native restricted
APEX availability and excludes external source-grant replay. Author application
810003, its capture and the earlier unmapped ZIP remain intact. The two excluded
grant scripts remain unreferenced frozen files in the native distribution; they
are not executed or claimed as required target grants.

Native `project deploy` installed 23 changesets into E1_INTEGRATION, application
810004, alias E2-INTEGRATION. All components report 1.0.0; business packages and
triggers are valid. Browser checks passed: VERIFIER created/saw Hello World in
history; LAB_USER was blocked while restricted; public APEX publication enabled
LAB_USER, whose new greeting retained the verifier row. Repeating identical ZIP
bytes executed zero changesets and preserved the full history/configuration
snapshot. Documented restriction/publication SQL blocks were also run directly.

The application repository commit is
`87fa1dccd6464a2123e9c425630aa11e4e7afec6`; every archive member matches its
committed distribution file. Mapped ZIP SHA-256 is
`0377604203edf3674ae5a2b3735da11f108de6f576c879266ea1325d4bf6e0d0`.
The [receipt](tests/project-integration-mapped-validation.json), native transcripts
and desktop browser captures retain results. No project-root commit/push or UAT
deployment was performed.

SQLcl 25.3 `project verify` still reports one `stagechangelogcomplete` APEX
missing-source error; other seven verification results report INFO/pass. Native
Liquibase's generated DATABASECHANGELOG_DETAILS view is invalid in this run,
separately from valid application code. These are recorded tool/configuration
findings. This is a working runtime assessment candidate, not a formal native
verification pass. D1/D2 now give actual preparation, deployment, restriction,
publication and inspection commands rather than unimplemented placeholders.

## Exact UAT promotion and transparent wrapper prototype

Added `scripts/cicd-project-promote.py` for the requested narrow automation
prototype: inspect, deploy, publish, baseline and check-baseline. It reuses the
SQLcl named-connection/error-redaction boundary, prints actual commands, checks
the D-tested archive identity and packaged UAT mapping, and validates the live
integration/UAT state. Deployment/publication require explicit assessment mode;
no formal native verification pass is claimed. SQLcl CLOB JSON queries set LONG/
LONGCHUNKSIZE explicitly to avoid truncation, and separate their output from the
server completion marker. Local receipts/baselines are private files, not a new
database controller or production provenance system.

The same SHA-256 archive installed 23 changesets into E1_UAT / application 810005.
Actual browser checks passed: VERIFIER greeting/history, LAB_USER restriction,
native publication and LAB_USER greeting/history. LAB_USER edited the Hello
configuration via the normal application dialog to prefix `UAT:`; the next
greeting became `UAT:Hello World` while earlier snapshots remained unchanged.
Captured three complete history rows, both entries/configuration rows and initial
component declarations. Identical-archive repeat executed zero changesets and
matched every business field; baseline repeat retained the exact file bytes.

Focused negative checks rejected a different archive hash, deployment without
assessment mode, changed history and changed configuration; a new history row
was permitted without altering prior rows. No new automated test suite was added.
The [UAT receipt](tests/project-uat-promotion-validation.json), visible native
transcripts and desktop screenshots retain evidence. E now supplies exact shell,
SQLcl and browser operations, including separate publication and immutable
baseline stages. The current fixture is already published and has a baseline;
repeat instructions inspect/compare rather than reset it. Initial source apps,
D's target and all archive bytes remain intact. Later patch/protection execution
and production trust/concurrency controls remain separate work.

## F1 native Working Copy checkpoint preparation — 2026-10-20

Replaced the F1 outline with exact operator steps: Git branch preparation,
DEV_C Builder login, private Working Copy creation, page 1 Hero region Name,
independent Main page 10 Title, selected-page Refresh and Merge with native
backups, source metadata inspection, native PROJECT list/export and reviewed
Git commit. The direct SQLcl interface remains visible; no F wrapper was added.
F1 does not change component versions or deliver Hello 1.0.1.

Rehearsed on a separate native Copy Application of 810003: Main 810103 and
Working Copy 101, in E1_DEV_C. Native comparison reported two changed pages;
refresh selected only page 10, merge selected only page 1. Both final metadata
values and the retained native backup were inspected. Reapplied the existing
Product Owner approval for scheduler capacity 10 in CDB/FREEPDB1 after the
recreated lab was found at 1 with comparison queued behind an APEX job.

In an isolated clone of the application repository, the original PROJECT filter
listed/exported only 810003 and left Git clean despite the additional apps.
Changing only that rehearsal clone's filter to Main 810103 exported both merged
headings, excluded Working Copy 101 and produced local checkpoint fba9327.
The operator repository remains clean at 87fa1dc; Main 810003, integration,
UAT, historical E.1 evidence and original artifacts were not changed.

The [focused receipt](tests/project-f1-working-copy-validation.json) distinguishes
GUI/metadata/export observations from runtime verification still to be performed
on operator Main after its merge. No runtime qualification of the rehearsal
copy is claimed: it inherits the source fixture's ID-bound E1_CTRL gate.
F2 patch inputs, staging, packaging and upgrade qualification remain incomplete.

## F authoring-workflow clarification

The Product Owner selected two Working Copies instead of the direct-Main
shortcut for simulating the independent edit. F's introduction now states the
end-to-end goal and separates F1's authoring/Git checkpoint from F2's component
release and preservation proof. F1c gives exact second-copy create/edit/reviewed
merge operations; Main's page properties are not edited directly. A continuation
route preserves any page 10 edit already made under the previous instructions.
The existing F1 rehearsal receipt retains its original direct-Main simulation;
the revised two-copy combined execution remains for operator verification.
No additional runtime or release pass is claimed for this documentation change.

## F.2 native Hello 1.0.1 preparation and qualification — 2026-10-20

Prepared the established compatible whitespace correction from
`db/changes/005-hello-1.0.1.sql` as a reviewed native authoring input, without
using its old migration-history stream. The authoring schema now has the
nonblank constraint, whitespace-normalizing Hello guard and installed Hello
1.0.1 declaration. All prior author business fields were checked unchanged.
The F.1 commit c79fe9d is preserved; its page 10 Name differs from its unchanged
Title, so F.2 documents actual runtime text rather than silently editing Main.

Executed native PROJECT release 1.0.0, export, stage against local e2-world,
add-custom, verify and gen-artifact on the operator application repository.
Preparation commits are 8f6d66f (freeze initial history), 58affef (source correction)
and 3916ec6 (reviewed mapped distribution). Initial migration SQL/logical IDs
remain intact: 24 initial SQL files are byte-identical after the native release
move. The new stage orders constraint, trigger and explicit installed-version
SQL. Candidate APEX metadata retains approved native restricted verification,
clears the inherited runtime hook and declares assembly version 1.0.1. The
packaged component declaration is project-authored, not inferred by PROJECT.

Fixed candidate: `artifact/e2-1.0.1-assessment-r1.zip`, SHA-256
`e1063f78aab39ec4315d12eda6871286762df36e1a3711f5bd6ba874e9174a46`.
Native verification still reports one stagechangelogcomplete error / seven INFO,
now listing frozen initial files and separately included APEX. Formal release
verification remains blocked; successful runtime qualification is separate.

Explicitly reconstructed only disposable E1_INTEGRATION/application 810004,
with its workspace/accounts retained and ownership/table guards checked. Fresh
candidate installation ran 26 changesets. Reconstructed the original initial
archive (23 changesets), created literal QUAL: configuration/history examples,
then applied the identical candidate: 4 executions / 22 previously applied.
Native SQLcl CLOB binds and Oracle JSON_EQUAL compared all business fields across
actual deployment in the same connected session. New behavior, component triple,
native VERIFIER access, LAB_USER denial, publication and ordinary-user greetings
passed on both starts. Repeating the candidate ran 0 / 26 and preserved Available
status and every business field.

The reviewed @files are SQL/PLSQL inputs and focused assertions, not a deployment
orchestration wrapper. Wrong-identity reset refusal and changed-configuration
comparison rejection were exercised; the latter probe rolled back. Relative
operator paths and an unchanged repeat PROJECT export passed. Detailed native
outputs, scope and screenshots are bound by the
[F.2 receipt](tests/project-f2-upgrade-validation.json).

UAT was not upgraded in preparation. Every UAT business/component field matched
its pre-preparation snapshot, with Hello 1.0.0 and UAT: retained. Its first
1.0.1 promotion/publication is deliberately reserved for Product Owner execution.
No Foundation upgrade, hosted pipeline, recovery/concurrency guarantee, formal
verification pass or handover acceptance is claimed.

### G — native verification and bounded compatibility rejection

Implemented the accepted X3 metadata-only negative case in the native A–I
walkthrough. The comparison clone holds supported/incompatible declarations;
PROJECT verify is run visibly against each. The project-authored
`scripts/cicd-project-incompatible.py` reuses `cicd-compatibility.py` and binds
the immutable F execution-r2 archive, source commit/tracked worktree, declaration
hashes, validator and exact UAT snapshot before its deployment dispatch point.
The incompatible case rejects before `project deploy`; native Oracle metadata/
APEX export primitives capture the before/after target. No Foundation DDL,
publication change or business insertion is part of G. Private state stays under
.local-apex; public evidence contains hashes/results only.

Disposition: retain the helper as an Elaboration assessment prototype, not a
production admission controller. Snapshot/check/dispatch has no concurrency fence
and no general semantic-version policy. Existing admission/pipeline work owns
productionization; complex Foundation implementations remain E.5.

### Correct native verification instead of accepting an error

The SQLcl 25.3 StageChangeLogComplete implementation scans exported SQL sources
against the current branch stage file, producing false missing-file reports for
released objects and separately staged APEX. Binary inspection was diagnostic;
no client JAR was modified. Official clients 25.4.1 and 26.3 were downloaded
side-by-side and checked against Oracle-published ZIP hashes. SQLcl 25.4.1 was
the smaller qualified correction for G; 26.3 remains an investigated alternative.

The G comparison clone now uses version 25.4.1.0, explicit autoConnect=false,
current APEX IDs (expOriginalIds=false), native export, committed capture and
native stage. Current identities avoid the inherited 810001/E1_DEV_A export
identity when the application actually belongs to 810003/E1_DEV_C. Native APEX
source and distribution must match; the clone does not reproduce F's post-stage
version/status/hook edits. Both G declarations verify with Errors 0 / Warnings 0 /
Info 15. The original F repository, immutable artifacts and UAT remain unchanged.
This fixes G's structural baseline without certifying or rebuilding F's old ZIP.
No verifier, test service or native check was disabled.

### H — native live-definition capture, repeat and explicit restoration

Added the H.1–H.5 operator procedure. The selected definition change is the
APEX global notification, applied/restored with the documented native API.
Native SQLcl exports application SQL and READABLE_YAML before the change, after
the change, after the unchanged F artifact repeat, and after restoration.
Native PROJECT repeat ran 0 / previously run 26 and did not reject the live edit.
No custom admission controller is inserted in that path. SQL assertions compare
publication, component versions, full changeset history and all business fields.

The small file-only comparison helper excludes only the root application YAML
subscription.version-number, an internal revision that advances even on restoration.
All other YAML values/files must match for restoration. This is an explicit
project comparison policy, not an Oracle deployment feature. Native raw exports
and failed raw-checksum restoration diagnostics are retained privately.

Rehearsal used integration 810004 and preserved its Restricted Access status.
A read-only check confirmed UAT 810005 is Available / 1.0.1 with no notification
and produces 24 YAML files. UAT was not changed during preparation. Browser
verification used VERIFIER on integration and confirmed the live banner survives
the native repeat, then disappears after restoration. Retain these helpers only
as Elaboration inspection/assertion prototypes; do not adopt as production drift
control. Existing PBI-023/045 and pipeline work own production decisions.

## Decision handover package

The current Product Owner brief and separate 11-slide decision deck summarize
demonstrated delivery, native protection gaps, release blockers and five decisions.
The deck retains editable tables/listings, a scoped desktop screenshot and source
notes. README links this package. The earlier increment deck and E.1 evidence
remain separate. Publication checks do not change sprint status or certify the
retained F artifacts. See the [audit](sprint_E.2_documentation_audit.md#product-owner-handover-publication--2026-10-22).
