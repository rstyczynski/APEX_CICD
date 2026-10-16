# Sprint 0 — Documentation audit

## Increment and decision evidence

PBI-001 is complete on the document-review criterion: the Product Owner
accepted the README vision on 2026-10-16 and subsequently stated approval of
the README. The Product Owner also directed that the earlier local setup be
recorded as completed preliminary work, the PDF be moved to `refs/`, and the
deployment runbook be moved to `docs/` for potential reuse. These are recorded
decisions, not new claims that the runtime was tested during Sprint 0.

The shared setup, plan context, and draft roadmap support PBI-002. Including
these proposed planning artifacts with the vision increment does not mark
PBI-002 complete: roadmap acceptance, planned label/context changes, and final
Sprint 0 handover remain pending. No push is authorized.

## Reconciliation

README.md records the accepted vision, preliminary assets, current planning
state and relocated references. PLAN.md records the explicitly accepted
preliminary work without inventing a historical sprint or marking future
application work complete. ROADMAP.md and sprint_0_proposedchanges.md label
the I.1/E.1 sequence as proposed; current sprint assignments are unchanged.
The setup record now reflects the acceptance and remaining planning decision.

PROGRESS_BOARD.md retains four columns and only Sprint 0's assigned items.
PBI-001 is tested through Product Owner review; PBI-002 remains under_design.
This does not close Sprint 0 or substitute for the P9 final handover.

The root SRS and candidate architecture do not yet exist; these are later
Inception deliverables. The test profile remains pending candidate
architecture. No accepted technical design, implementation record, functional
test record, or automated test specification is needed to claim the vision
document complete. No application code or runtime configuration changed.
Executable build and regression checks are not applicable to this increment.

docs/deploy.md preserves the earlier instructions and verification record,
adds the preliminary-work context, and corrects its own optional removal path.
Its setup, operating, recovery and destructive cleanup examples were not rerun
or newly certified. The scripts, local credentials and runtime data remain
untouched; scripts and the existing .gitignore remain local untracked assets.
Future work must assess suitability before adopting this pre-work.

The external PDF is unchanged. SHA-256 before and after relocation:
`6f41b2f4511bfc3e3e4bbe28f3240c897a56006a42e46177d62a06d493cc4425`.
No research conclusion is asserted from its unread contents.

## Checks performed

`git diff --check` passed. `shasum -a 256` on the original PDF and on
`refs/apex-lifecycle-management-v3.pdf` returned the identical hash above.
A Python pathlib/re check of Markdown links in README.md, PLAN.md,
ROADMAP.md, docs/deploy.md, sprint_0_setup.md and sprint_0_proposedchanges.md
passed for all 17 local links. The same check confirmed the old root PDF and
runbook paths are absent. Remote documentation links were not revalidated
during this relocation increment.

Stage only the vision, planning/evidence documents, moved runbook, and external
PDF. Leave .DS_Store, .gitignore, scripts and ignored runtime files outside
this increment. The completion commit will identify PBI-001; record its hash
in the next audit or sprint wrap-up.
