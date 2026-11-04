# Sprint E.3 technical handover — round 2 correction recheck

**Round:** E.3, round 2, outbound independent recheck prompt, 2026-11-04.

**Revision:** Corrected parent source
**d37b461e23bf459ba34d5e5298a7f47af0306750**, published on `main` in
**https://github.com/rstyczynski/APEX_CICD** and verified with `git ls-remote`.
Corrected public seed controller:
**eac24dedab3f611ef09b0196623cfabf674e7e1c**, `main` in
**https://github.com/rstyczynski/APEX_CICD_E3**, also present as main in the
parent's tracked baseline bundle. Historical application tag v1.0.4 remains
**fbda57a0cbe4d32961ad826852bd04394a500c11**. No tag moved. The subsequent
prompt/status publication changes coordination metadata only. No implementation
working patch is included. Unrelated local `progress/E.3/model.drawio` is
untracked, excluded and was not read, modified or committed by the coordinator.

**Reviewer:** Independent external engineering reviewer; identity/model/tool
to be supplied. The Product Owner relays this prompt; no reviewer has been
contacted by the coordinator and no independent recheck is yet claimed.

**Scope:** Recheck R1-M1/M2/L2 corrections and the approved R1-L1 deferral for
the bounded Elaboration handover. Source, presentation and offline evidence;
no fresh native qualification or deployment is supplied or claimed.

**Inputs:** [Original review](sprint_E.3_handover_review-1.md),
[engineering response](sprint_E.3_handover_review-1-response.md),
[expert feedback](sprint_E.3_handover_review-1-feedback.md),
[selected decisions](sprint_E.3_handover_review-1-decisions.md),
[correction receipt](tests/review-1-correction-checks.json),
[offline cases](tests/review-1-offline-diagnostics.log),
[static smoke](tests/review-1-static-smoke.log),
[walkthrough](sprint_E.3_increment_demo.md),
[implementation](sprint_E.3_implementation.md) and
[audit](sprint_E.3_documentation_audit.md). All source/evidence inputs are
committed in the exact corrected parent revision above.

## Status entering recheck

| Finding | Status | Scope / disposition |
|---|---|---|
| R1-M1 | fixed@d37b461 | Actual PPTX/notes/source corrected and rendered; independent recheck pending. |
| R1-M2 | fixed@d37b461 | Fixed reference readers distinguished from new-LAB acceptance; no parameterization claim. |
| R1-L1 | deferred | Product Owner-approved temporary read-only prepared-host lookup, with ending/reconsideration trigger; not NFR-4 compliance. |
| R1-L2 | fixed@d37b461 | Shared assertions pass 21 offline diagnostic/receipt cases; native workflow not rerun. |

Retain the R1 IDs. Correction-commit statuses precede this later publication of
that commit's identity; no label establishes independent runtime verification.

## Copyable expert instruction

Act as independent reviewer for APEX_CICD Sprint E.3 technical handover, round 2.
Repository: **https://github.com/rstyczynski/APEX_CICD**; branch/ref: **main**;
exact review revision: **d37b461e23bf459ba34d5e5298a7f47af0306750**.
Use that commit, not an arbitrary later main. The corrected application controller
is **eac24dedab3f611ef09b0196623cfabf674e7e1c** in the public seed and tracked
bundle. Historical v1.0.4 and its receipts remain unchanged.

The Product Owner approved: **“Approve fixes; allow temporary lookup on this
prepared host.”** This selects M1's focused PPTX correction, M2's documentation-only
option, L2's assertion correction with offline validation, and L1's temporary
prepared-host accommodation. No fresh native workflow or deployment was selected.

Recheck the round-1 closing conditions against the correction, using the input
inventory above and the original prompt for wider context:

1. **M1:** Inspect actual PPTX slides 4/10 and notes plus
   `progress/E.3/presentation-handover/build.mjs`, against walkthrough B/F.
   Check variable provenance in each terminal, explicit matching LAB/directory,
   published-tag selection and historical-result labels. The receipt records
   four changed slide/notes parts and 75 preserved parts. State whether you
   rendered the slides or inspected only text/package evidence.
2. **M2:** Compare test inputs with the manual, test profile/record,
   configuration, implementation and handover. Fixed seed evidence readers,
   current seed HTTP probing, access permissions and new-LAB acceptance must
   be distinct. No selected-replay parameterization is claimed or required.
3. **L1:** Check AGENTS' explicit exception and linked SRS/current guidance.
   The existing record is retained only for this prepared host; no new store,
   copying or deletion is authorized. Jobs use GitHub secrets independently.
   End it when a compliant remedy is selected; reconsider before new-host
   reproduction, scratch cleanup or expansion. The inherited scratch-configured
   VM-start fallback is outside the supported explicit-VM-start sequence.
   Assess the approved deferral, not NFR-4 compliance or PBI-054 completion.
4. **L2:** Inspect `examples/git-pipeline/.github/assert-missing-changeset.awk`,
   `qualification-receipt.jq`, qualification workflow, manual exercise and
   `tests/integration/test_pipeline.sh`. A consistent positive error count,
   expected ERROR rule and literal selected path must belong to the same
   diagnostic. ANSI/padding/wrapping must preserve that association. Inspect
   `tests/unit/test_missing_changeset.sh` and its 21-case log. Check schema-2
   receipt path/controller/tool-output fields and explicit pinned legacy
   compatibility. No new native workflow success is claimed by offline tests.

Allowed actions: pinned source/public evidence inspection and PPTX extraction/
rendering in disposable storage. If dependencies are already available, the
following bounded offline checks are also authorized in an isolated checkout:

```bash
bash tests/unit/test_missing_changeset.sh
bash tests/run.sh --smoke --new-only progress/E.3/new_tests.manifest
```

The second needs installed actionlint. Report unavailable/unrun checks rather
than installing tools or claiming success. Do not run broader integration or
platform tests, SQLcl, setup scripts, the presentation build script, database/
browser logins, runner/container operations, workflow dispatch, PR merges,
tagging, GitHub setting changes or deployment. Do not request/read credentials
or private snapshots, change source or push. Offline fixtures are the selected
validation level; production qualification remains outside E.3.

For each R1 ID, state whether its closing condition is met, partly met or not
met, with exact source/evidence and actual checks performed. Assess the L1
deferral's reason and trigger. Re-raised findings keep R1 IDs; identify regressions
explicitly. New findings material to E.3 use R2-H/M/L IDs and explain their
impact on the bounded handover. Do not turn deferred production work into a
blocker without a concrete conflicting E.3 claim.

Return complete Markdown as **`progress/E.3/sprint_E.3_handover_review-2.md`**.
Begin with subject/round/type, exact parent/controller/application revisions,
reviewer identity/model/tool, actual scope/checks/exclusions, inputs and a
per-finding status table. Give evidence and remaining closing conditions.
Finish with whether this bounded review can close with the approved deferral
or which corrections remain. Sprint acceptance remains the Product Owner's
separate decision. If file writing is unavailable, return Markdown for the
Product Owner to save at that exact path.
