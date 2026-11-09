# E.4 — Design checkpoint audit

## Scope and decision

2026-11-09. [PLAN](../../PLAN.md) records explicit E.3 acceptance/closure and E.4
activation with only PBI-042/PBI-060. [Setup](sprint_E.4_setup.md) and
[design](sprint_E.4_design.md) are the current review inputs. This is a draft
review-publication checkpoint under the external-review skill, not a completed
PBI increment or accepted design. No implementation/test skeletons are authorized.

## Consistency review

Root SRS: actor/use-case/FR-8/13 obligations inspected; bounded procedural checks
are not reported as complete automation, isolation or concurrency coverage.
Architecture: native capture/import/fingerprint interfaces and shared/private
semantics inspected; proposed experiment backlink added, existing production
requirements retained. Test profile: E.3 reference-run limitations inspected;
E.4 cases require new actual observations. README: E.3 closure and E.4 Proposed
entry points reconciled. PLAN and board: only selected E.4 parents remain assigned,
under_design; E.3 closes under the explicit Product Owner instruction. Backlog
criteria are unchanged. Existing PBI-060 definition is necessary review context.

Setup/design: approval remains pending, explicit preflight and no-edit interval,
known initial-install restriction, coordinated rather than parallel capture,
manual admission limits and target identity are visible. Implementation record,
functional test results, manual and presentation do not exist for this new scope;
creation is deferred until design approval and execution. Old E.4 scope record
is retained with an appended accepted superseding decision. Historical E.3
artifacts and unrelated working edits are excluded from this checkpoint.

## Checks

Native command signatures and checksum capability were checked against Oracle
SQLcl 25.4 PROJECT documentation and APEX 24.2 GET_APPLICATION documentation,
linked from the design. Oracle paper pp.20 and 26–27 were text-inspected with the
bundled Python/pypdf runtime. No current SQLcl invocation, database access,
workflow dispatch or runtime test was performed. Generated operating commands
and SQL source will require rehearsal after approval; design prose is not a
verified runnable walkthrough.

Local Markdown file-target and whitespace checks run before checkpoint commit;
results are recorded below. The review prompt pins the resulting source commit;
the review response will identify any further corrections and their checks.

Design checkpoint checks passed: all local Markdown file targets in PLAN, README
and E.4 records exist; git diff --check reported no whitespace errors. Anchor
semantics and native runtime behavior remain subject to review/execution.


## Review routing correction

The Product Owner explicitly requires a dedicated local Astra chat for E.4
design review. The earlier E.3-chat request was cancelled and supplies no E.4
acceptance evidence. Setup/design now name the dedicated review boundary.
The original issued prompt is preserved; a clarification supersedes its routing.


## R1-M1/R1-M2 design corrections

The original dedicated Astra report is preserved without edits. Design corrections
specify read-only first-run source reconciliation, two-read baseline qualification,
pre-existing-edit rejection, explicit availability observations across import and
receipt finalization after restoration. Existing accept.sql/restrict.sql/deploy.sql
and the retained E.3 receipt were inspected; no runtime execution occurred. Planned
IT-3/IT-4 now cover the two issues. Source corrections remain Proposed and require
independent textual recheck, then Product Owner approval. Runtime acceptance remains
pending. Relative file targets, scope/state assertions and git diff --check pass for
the correction checkpoint; no implementation files were changed.

## Final design-review handoff

Dedicated Astra feedback independently verifies both design-level corrections at
0ad508b6e872ca500c5ac92c6b60d555fc154cb4 and recommends Product Owner approval.
Review report/feedback are preserved. Assessment/dispositions link the findings,
corrections and pending runtime checks. Both PBIs stay under_design; no acceptance
token is changed. All E.4 Markdown file-target checks and git diff --check pass
again. This final checkpoint publishes review evidence only, not a completed PBI.
