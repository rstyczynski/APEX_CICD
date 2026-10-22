# E.2 — Oracle lifecycle gap-analysis walkthrough

Status: prepared for live Product Owner review; actual feedback and acceptance remain pending. This is the
single handover entry point. The [manual](user_manual.md) supplies operating and
recovery detail; [gap analysis](oracle-gap-analysis.md) supplies recommendations,
[implementation](sprint_E.2_implementation.md) and [focused evidence](sprint_E.2_tests.md)
supply actual outcomes. [Handover](sprint_E.2_handover.md) records the live review
and Product Owner decision. The matching [editable presentation](sprint_E.2_increment_demo.pptx) follows the slide map below.

## Goal and starting state

Give developers flexibility through stable, industry-standard tools and
techniques. Inspect how SQLcl PROJECT, Working Copies, Git and useful E.1 controls can
coexist, which requirements still need controls, and what genuinely blocks the
pinned path. This is a disposable Elaboration laboratory, not a production
rollout or delivery of E.3/E.4/E.5 items.

Use the authorized fresh pinned lab and retained run e2-20261019-01. Start from
its actual committed local source/distribution and owned targets. Do not reset
it to demonstrate a clean installation. Use a new named run for independent
reproduction, following A–E in the manual; the provisioning prerequisite remains
the existing installation procedure, not an automatic fallback.

## 1. Inspect source, versions and owned resources

For the retained-run inspection, use the existing run below in one terminal
session. Its inventory and repository already exist. `--preflight` checks
prerequisites without creating a run; `--inspect` requires that run's inventory.

```bash
cd "$(git rev-parse --show-toplevel)"
E2_RUN=e2-20261019-01
bash scripts/cicd-oracle-lifecycle-A_prepare.sh --preflight --run "$E2_RUN"
bash scripts/cicd-oracle-lifecycle-A_prepare.sh --inspect --run "$E2_RUN"
git -C ".local-apex/e2/$E2_RUN/repo" log --all --oneline --decorate -12
```

Expected: loopback FREEPDB1, observed APEX/Database identity, owned resource
inventory and native repository checkpoints. The private credentials file is
not part of inspection output. Relevant outcome: PBI-051.1; design A.

Open the [Git repository layout](repository-layout.md) during the handover.
Show the directory tree and follow its read-only inspection sequence. Trace
Working Copy outcomes through Main into source and distribution, and identify
the added component declaration and retained E.1 controls.

Inspect the actual exported source and generated native install hierarchy:

```bash
find ".local-apex/e2/$E2_RUN/repo/src" -type f
find ".local-apex/e2/$E2_RUN/repo/dist" -type f
cat ".local-apex/e2/$E2_RUN/repo/dist/component-contract.json"
```

Expected: Main APEX SQL plus readable YAML, bounded schema source, generated
migrations/custom SQL and explicit component declarations. No ownership marker,
private Working Copy export or runtime-history replacement data belongs there.

## 2. Inspect SQLcl PROJECT reconstruction and preservation

```bash
python3 scripts/cicd-oracle-lifecycle.py snapshot --run "$E2_RUN" --role upgrade
python3 scripts/cicd-oracle-lifecycle.py preservation --run "$E2_RUN" --role upgrade
```

Expected: declared component versions, Hello World, the retained user setting
and exact synthetic history fields. Open the candidate receipts and native
migration output described in the focused evidence. Compare the initial and
patch checkpoints: generated RELEASE_NOTE addition and intentional LANGUAGE seed
are different responsibilities. Relevant outcome: PBI-051.3; design X1.

Inspect the actual archive/source/declaration binding before any deployment.
A full live mutation sequence uses B in a new owned run, with review pauses and
fresh qualification before populated deployment. A repeat of a retained result
is not a second fresh install claim.

## 3. Inspect the native release blocker

```bash
bash scripts/cicd-oracle-lifecycle-B_project.sh --rehearse --run "$E2_RUN" --retry verify
```

This command is expected to fail on the pinned native verification finding;
it performs no deployment. Read the Errors summary and the retained verbose
finding in focused evidence. Explain the separate APEX changelog and branch-name
workaround. A successful candidate install does not waive full verification or
permit a formal release. Relevant outcome: PBI-051.3; PF verification fit.

## 4. Inspect Working Copies and agreed Main checkpoint

In App Builder inspect owned Main 821788. Working Copy 101 was deliberately
abandoned after its unmerged page deletion; use the retained screenshots and
operator ledger for that completed copy. Inspect the selected pages,
refresh/merge direction, stale-edit recovery and explicit deletion handling. Show that Main and copy
share a schema. Follow the manual's exact controls and the recorded operator
ledger; do not recreate an earlier failure over the agreed Main checkpoint.

Then inspect the team checkpoint in this same SQLcl PROJECT repository and both
reconstructed page document titles, LOV values and greeting. A lower-level split export/import is a
labeled comparison from the same Main state, not another maintained live source.
Relevant outcome: PBI-051.2; design X2.

The retained checkpoint is d5c3334486cac6300a0939a4d84bfcfe70627df9. Inspect
its page-title diffs against e2-before-working-copy. Native fresh F3/app 3821789
and upgrade U/app 821790 use the same combined candidate bytes; lower-level
comparison is F4/app 4821789. The current fresh-role pointer denotes F4 after
comparison; the native qualification receipt retains F3 explicitly.

```bash
python3 scripts/cicd-oracle-lifecycle.py titles --run "$E2_RUN" --role upgrade \
  --value 'E2 Hello working copy|E2 History Main'
python3 scripts/cicd-oracle-lifecycle.py behavior --run "$E2_RUN" --role upgrade
cat ".local-apex/e2/$E2_RUN/identities-upgrade-before.json"
cat ".local-apex/e2/$E2_RUN/identities-upgrade-after.json"
cat ".local-apex/e2/$E2_RUN/native-declaration-carrier.json"
```

Expected: both page titles; HELLO/Hello and WORLD/World; Hello World; changed
physical region IDs; exact native-carried declaration hash. Page Title is the
browser document title. The runtime region heading retains its original name.
Open U through ORDS application 821790 as the generated E2DEV lab user: Home
document title is E2 Hello working copy; E2 History document title is
E2 History Main and its report displays E2 retained history. F4 renders the same
titles with an empty history report, as expected for a fresh reconstruction.
Use the source-linked screenshots/ledger for abandoned Working Copy 101. A new
copy for a live repeat must use the manual's disposable scope and recover Main
to the agreed state; do not pretend the deleted copy is still present.

## 5. Inspect admission and one rejection

The final combined-candidate negative exercise has run. Inspect the allowed declaration, archive
hash and real-target before/after receipt. Repeat D's read-only admission
inspection, and show one safe stale-binding rejection before native deploy.
A retained read-only inspection can use:

```bash
cat ".local-apex/e2/$E2_RUN/negative-admission.json"
python3 scripts/cicd-oracle-lifecycle.py admit --run "$E2_RUN" --role upgrade \
  --file ".local-apex/e2/$E2_RUN/repo/artifact/e2-1.0.1-working-copy-candidate.zip"
```

The actual negative routine can be repeated with D's helper after inspecting
its receipt; it temporarily changes copied archive bytes and withholds/restores
the admission receipt. It never invokes native deploy after rejection. Explain
that E.1's existing validator is reused; the envelope is custom and
bounded. It does not complete E.1 drift/failure fencing. Relevant outcome:
PBI-051.3; design X3.

## 6. Assess recommendations together

Open the gap analysis and reconciled roadmap. Compare supported equivalences,
observed gaps, avoidable custom mechanisms, project-policy conflicts and current
blockers. Existing PBIs own the follow-up work; PBI-052 defines contract/SemVer
mapping and remains unscheduled. Complex Foundation upgrades stay E.5, after
toolchain stabilization. No pipeline or later-sprint completion is claimed.

Record the Product Owner's questions, repeat requests, assessment and explicit
handover decision in the handover record. Earlier reviews and current exercise
results do not substitute for the live review.

## Presentation map and reproduction limits

Slides 1–4 establish goal, agenda, responsibilities and scope. Slide 5 maps to
walkthrough 1. Slide 6 introduces the native journey; slide 7 shows the actual
repository layout. Slides 8–10 map to 2–3 (mapping, verification and existing
repository probe). Slides 11–16 map to Working Copies in 4; slide 12 traces the
checkpoint into Git and supplies read-only inspection commands. Slides 17–18
cover reconstruction and the identity gap. Slide 19 maps to admission in 5.
Slides 20–22 cover component contracts, roadmap and decisions in 6. Repository
and command listings use Courier; paths remain on individual lines.

[Public run evidence](tests/e2-20261019-01-evidence.zip) retains native candidates,
logs, receipts, comparison source and a scratch Git bundle. Its
[manifest](tests/e2-20261019-01-evidence-manifest.json) binds all retained bytes.
Inspect that evidence without a live database. Extract into a new directory;
clone scratch-repository.bundle into another empty directory to inspect all
source/distribution commits. This does not provision a runtime or reconstruct
secret credentials. The manual's A–E sequence creates a new independent owned
run. The observed run used the same domain helpers and actual Builder actions;
a second full new-run launcher execution has not been performed or claimed.

Read-only preflight/inspection and C/D completion-resume are rehearsed. E
rehearsal stops at the real review checkpoint, without fabricating a fresh
human observation. Expected native verification failure is retained. Actual
Product Owner feedback/acceptance is required in the handover record.

## Presentation formatting and desktop captures

The current deck uses SQLcl PROJECT consistently and the title Scope and evidence.
Parallel items have editable native bullets; the numbered agenda and ordered
roadmap keep their numbering. Slides 13–15 show desktop walkthrough repeats
from the separate E2 desktop walkthrough copy, labeled on the slides and in
notes. These views illustrate the recorded workflow; the original exercise
ZIP and captures remain unchanged. The repeat stopped before Confirm Merge
and was abandoned. Main's observed definitions and rows remained identical;
see the [repeat ledger](sprint_E.2_tests.md#desktop-presentation-repeat--2026-10-19).
