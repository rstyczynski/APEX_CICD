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
