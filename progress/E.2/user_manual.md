# E.2 — Laboratory operating reference

The [native SQLcl use-case walkthrough](cicd-walkthrough.md) is the current
operating guide, aligned with E.1's A–I application journeys. It uses
preloaded development assemblies and direct PROJECT commands. A–E include
observed mapped integration and same-byte UAT promotion, with a transparent
[promotion wrapper prototype](../../scripts/cicd-project-promote.py). Its readiness
statement identifies the later release/control steps still awaiting implementation
and rehearsal. F1 provides exact native Working Copy, SQLcl PROJECT and Git
steps rehearsed on a separate Main copy; operator Main 810003 is ready for
verification. The Product Owner reported F completed. G now supplies exact operator steps;
its corrected G.2 uses a separate SQLcl 25.4.1 client and clean native verification
(Errors 0 / Warnings 0 / Info 15). F's preserved archives are not rebuilt or
recertified by this comparison. H–I remain pending. The section helpers below belong to the earlier exercise and
are not the operator interface for that replacement journey.

Status: prepared for live review. Commands below describe the bounded section helpers;
individual observations are in [focused evidence](sprint_E.2_tests.md). Selected retained-run preflight, inspection and completion-resume are rehearsed;
a second full new-run runner execution is not claimed. The [walkthrough](sprint_E.2_increment_demo.md)
is the end-to-end presentation entry point; the [design](sprint_E.2_design.md)
owns scope, [implementation](sprint_E.2_implementation.md) owns construction and
[gap analysis](oracle-gap-analysis.md) owns the evidenced recommendations.

## Starting state and scope

The Product Owner authorized fresh provisioning with the existing pinned
installation procedure after inspection found an empty VM. The resulting lab
has Database 23.26.3.0.0, APEX 24.2.0, SQLcl 25.3.0.274.1210 and Java 21.
Use the [pinned infrastructure procedure](../../docs/deploy.md) for explicit platform preparation;
its host/installer prerequisites are separate from ordinary application delivery.
Use loopback FREEPDB1 only. The Product Owner approved changing this fresh lab’s CDB/PDB scheduler limits
from 1 to 10 after observed queueing. This one-off platform change is recorded in
the accepted design and focused evidence; runners only inspect prerequisites.
No helper rebuilds infrastructure automatically or
restores E.1 application state. Preserve E.1 historical files and the unrelated
E.1 diagram backup edit.

Every new run has its own local SQLcl PROJECT Git repository, schema/workspace pairs,
application IDs, ownership markers and credentials. Local secrets live only in
`.local-apex/e2/RUN/private.json` with restricted file permissions. Do not copy
that file into evidence, screenshots, slides or commits. The lab developer is
E2DEV. Use the generated developer password when signing into a run workspace;
the workspace and application IDs are printed by inspect. Retrieve only the
Builder password with `python3 scripts/cicd-password.py E2DEV --run "$E2_RUN"`
after initializing `E2_RUN` in that terminal and creating the run through A.
As in E.1, keep the displayed password out of recorded output. Do not use production
connections or substitute an unregistered schema into commands.

## Section commands and modes

In one shell, position at the repository root using Git discovery:

```bash
cd "$(git rev-parse --show-toplevel)"
bash scripts/cicd-oracle-lifecycle.sh --preflight --run e2-20261019-01
bash scripts/cicd-oracle-lifecycle.sh --inspect --run e2-20261019-01
```

`--preflight` reads actual tool/runtime prerequisites. `--inspect` reads retained
local run evidence and requires an existing `inventory.json`. Preflight does
not initialize a run. For a new run, execute A with `--live` before inspection;
substituting a new ID into the retained inspection commands is insufficient.
`--live` uses an interactive terminal and pauses at real GUI
and review checkpoints. `--rehearse` executes only unattended-capable operations;
it stops at a required fresh GUI checkpoint and never claims a human observation.
Use a new run ID for an independent full exercise; the retained current run must
not be blindly replayed. A fresh run allocates additional owned lab resources.

The thin launcher calls separate A–E section scripts in order. Each section also
accepts the same modes independently:

```bash
bash scripts/cicd-oracle-lifecycle-A_prepare.sh --live --run e2-demo-02
bash scripts/cicd-oracle-lifecycle-B_project.sh --live --run e2-demo-02
bash scripts/cicd-oracle-lifecycle-C_working_copy.sh --live --run e2-demo-02
bash scripts/cicd-oracle-lifecycle-D_admission.sh --live --run e2-demo-02
bash scripts/cicd-oracle-lifecycle-E_findings.sh --live --run e2-demo-02
```

The full new-run sequence remains pending execution as a runner; do not treat the
example as proof of a completed second run. The current run was exercised through
its underlying helpers and actual Builder controls as recorded in the evidence.

## A — Prepare owned inputs

A initializes SQLcl PROJECT in a private Git repository, provisions collision-checked
owned resources and installs the small schema fixture. Sign into the printed
author workspace as E2DEV. Create E2 Lifecycle with the allocated Main ID, Home
page 1 and an interactive report E2 History page 2 over E2_HISTORY. Add a dynamic
shared LOV E2 GREETING WORDS with this query and map Return Column R, Display D:

```sql
select setting_value d, setting_key r
from e2_settings
where setting_key in ('HELLO','WORLD')
```

Enter the real Main application ID at A's prompt. A verifies workspace/schema
ownership, scopes SQLcl PROJECT filters to Main, captures schema/application source
and commits the reviewed source. Inspect that no private Working Copy,
ownership table, credentials or runtime history/settings rows were captured.

## B — SQLcl PROJECT capture and candidate qualification

Inspect the generated staging hierarchy and custom seed SQL before accepting the
prompt. Native stage requires a branch reference; a tag alone was rejected.
The bounded workflow uses slashless experiment branch names because pinned
SQLcl stage and verify disagree on slash-containing directory names. This is a
local experiment constraint, not a change to the product checkout convention.

The generated APEX installation clears session setters. The installer therefore
uses the Oracle paper page 30 defaults-file hook. Target property files use the
exact `appId` spelling generated by this client and a unique target alias. A
candidate must contain the reviewed hook before deployment. Its archive hash,
source revision, declaration and exact observed target state are bound first.
A fresh successful candidate qualifies the same bytes before populated delivery.

Inspect empty-target reconstruction, installed component versions and greeting.
A synthetic retained-history row and user setting are then added to the populated
target. Repeat the same archive and inspect exact retained fields. Change Main's
page 1 Title to E2 Hello patch and application Version to 1.0.1; add the fixture's
RELEASE_NOTE column and intentional LANGUAGE setting through the section helper.
Review the generated additive migration and custom SQL. Qualify the patch from
empty and from the baseline, including repeat and preservation.

In Page Designer, make the edit through keyboard typing and leave the field;
verify the Undo control names the changed property before Save. The initial
programmatic fill did not update the Builder model, and the database title check
correctly rejected it. After Save, check the persisted title through the helper;
an editor field alone does not prove a saved change.

A full native verify failure is retained as an assessment finding. The helper
rejects its nonzero Errors summary even if the process returns success. Prerelease
candidate exercises may establish delivery behavior; **formal release stays
blocked**. No generic force option bypasses that gate. If verification passes,
the section tests before freezing, then regenerates and requalifies changed
release bytes instead of transferring stale evidence.

## C — Working Copies and team checkpoint

Start from B's qualified fixture and recorded Main/Git baseline. In Main's
application home choose Create Working Copy and give the copy an E2-specific
name. Record its assigned application ID. In SQL Workshop inspect
E2_RUN_SHARED_PROBE from the author schema: Main and its Working Copy use this
same schema. A Working Copy does not isolate database-object changes.

In the Working Copy, edit page 1 Title to E2 Hello working copy and Save. In Main,
edit page 2 Title to E2 History Main and Save. Use Compare Changes, Refresh from
Main and Merge into Main controls, recording which direction and components you
select. Refresh the disjoint Main page into the copy before merging the intended
copy page into Main. Check both saved titles. A merge replaces selected pages or
shared components; it does not perform a Git text merge within one page.

Use the expendable copy for a stale same-page scenario: save distinguishable
changes in Main and the copy, inspect Compare and the replacement warning, and
observe the stale merge outcome. Recover by refreshing the needed Main state
and deliberately reapplying the intended copy change. Preserve the initial
failure and correction notes. Record every selected page and Main value before
and after; do not call a lost edit a successful merge.

Delete an expendable page only in that owned copy and inspect the Missing
comparison entry. Main deletion requires an explicit separate action; keep it
out of the agreed checkpoint unless deliberately selected and recorded. Finally,
make an unmerged expendable copy edit and abandon/delete that owned disposable
copy, confirming Main is unchanged. No historical application is involved.
Record actual operator actions/decisions, confusing differences and recovery
effort in the exercise evidence; there is no measured E.1 usability baseline.

C removes only its owned shared-schema marker, captures the agreed Main team
checkpoint through SQLcl PROJECT in the same repository, compares two no-edit exports
and commits the reviewed result. Inspect that private Working Copies were
excluded. Reconstruct through the established native candidate path and a
separately labeled lower-level split/original-ID/no-date comparison. The latter
is temporary evidence, not a second maintained migration history. Check both
page document titles and the shared LOV definition/data and greeting in reconstructed targets. Native mapping regenerated region IDs on changed import: this gap must remain visible even when functional checks pass.

## D — Declaration admission

D reuses the E.1 explicit validator; it does not infer compatibility from diffs
or parse general semantic version ranges. Inspect allowed initial/patch triples,
incompatible Foundation metadata, missing dependency, unknown version and stale
artifact rejection. Breaking Foundation DDL is never executed. Compare the real
target definitions and rows before/after rejected inputs and verify native deploy
was not reached. The envelope is a custom bridge under assessment; full E.1
fencing and partial-DDL recovery remain unqualified here.

## E — Findings and handover

Open the walkthrough and editable presentation. Inspect source/evidence references,
classified findings, backlog reconciliation and ordered roadmap. Repeat a retained
read-only verification failure and a safe inspection step. Record actual Product
Owner feedback in [handover](sprint_E.2_handover.md). Runner completion is not
sprint acceptance, and earlier screenshots/logs do not substitute for a live demo.

## Resume, retry and recovery

Use `--resume` for a completed section to verify its retained checkpoint and owned
runtime without replay. Later sections may legitimately advance Git HEAD; the
older checkpoint must still exist and the current source must be clean. For a
partial mutating section, inspect its logs and target state first; the helper
refuses blind replay. `--retry verify` repeats a section's read-only verification;
`--retry capture` refreshes source but invalidates downstream artifact/qualification
claims until reviewed and regenerated. C's `--retry gui` returns to a real GUI
inspection checkpoint and records no fresh automatic usability result.

For B's failed pre-patch title check, save the requested Main title/version and
run `bash scripts/cicd-oracle-lifecycle-B_project.sh --live --run "$E2_RUN" --retry patch`.
This validates the retained initial baseline and upgrade state, refuses started
patch DDL, and returns to the patch-authoring pause without repeating initial
delivery. It does not recover arbitrary later partial failures.

An unexpected reinstall, checksum error, partial DDL, unknown target, missing
receipt or changed binding stops the affected operation. Retain the failed
attempt, inspect actual state, and choose a bounded recovery or a new owned run.
Do not reset a target, rewrite migration history, force checksums or recreate a
foreign resource to make an exercise pass. Infrastructure failures require a
separate explicit provisioning/restoration decision, as recorded for this run.

## Retained current outcome and prototype retention

The walkthrough identifies native F3, populated U and comparison F4 explicitly;
inspect inventory and receipts rather than assuming the current fresh pointer
still names the qualified native target. Native artifacts carry the canonical
component declaration from dist/component-contract.json; semantic admission is
separate. Never deploy an archive lacking the reviewed target-mapping hook.

The scripts are retained as disposable, reproducible Elaboration laboratory
helpers. They are not adopted as a production framework. Production retention,
API hardening, provenance and operational protections require the reconciled
follow-up backlog. Preserve run inputs and evidence until review; no general
cleanup command is provided that could erase E.1 or another run.
