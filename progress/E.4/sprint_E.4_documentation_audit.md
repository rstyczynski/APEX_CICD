# E.4 — Documentation audit

Earlier entries below are revision-specific snapshots. The current working-draft
check is [Handover preparation checkpoint](#handover-preparation-checkpoint).

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


## Current parallel-scenario correction — direct Product Owner review

2026-11-09. The Product Owner rejected the sequential authoring protocol and
explicitly waived another Astra review. The current working design requires all
three branches from one S0, separate prepared author fixtures, independent native
capture/stage with overlapping work, and retention of all three staged original
heads before any integration. Setup/analysis, IT-1, architecture diagram, README
and product-document scope links are reconciled. PBI-042's reviewed trusted-baseline
and availability corrections remain; previous expert approval applies only to the
superseded serial scenario. Original expert artifacts are preserved unchanged.

The author fixtures are an unqualified execution prerequisite, not existing proven
infrastructure or a new PBI-056 service. Identity/path equivalence, native combined
source/distribution reconciliation and simultaneous host capacity must be qualified
before execution. Unavailable prerequisites block execution without serial fallback.
No new reviewer chat/message, test skeleton, implementation, fixture preparation,
native operation or workflow is initiated. Both selected items remain under_design.

Validation for this working draft: all local Markdown file targets from changed
E.4 records exist; all three e4-a/e4-b/e4-c branches explicitly start at S0 and
stage against e4-base=S0; IT-1 rejects serial initial work and requires the common-base
staged checkpoint. git diff --check passes. SQLcl 25.4 PROJECT command/reference
and native export filter documentation were rechecked; no SQLcl capability is
claimed runtime-qualified by reading documentation. No completion commit or new
review-publication push is made for this unapproved working design correction.


## A/C selection and B postponement — working design

The current design and tests now select A/C only for the first release while
retaining independent B on an unmerged branch. Archive/source/snapshot and browser
checks must prove B's absence and A/C preservation. Later B update/revalidation is
specified without duplicating old changesets or weakening accepted history. Oracle
25.4 PROJECT and 26.1 release-change documentation were checked: stage is not a
feature selector; 26.1's release selectors are outside the approved toolchain.

Setup, assessment and proposed-change record explain that the root PBI-060 still
requires three contributions in one release and needs explicit criterion alignment
at design approval. No root backlog, plan or board is modified by this correction.
No further reviewer contact or native/runtime execution occurs. Markdown link targets
and git diff --check pass. This is an unapproved working design, not a completion commit.


## Release announcement and developer participation

2026-11-09. This is a documentation-only correction for direct Product Owner
review. Analysis in setup now defines the developer, Release Manager, operator and
GitHub responsibilities, an actor-led release journey and authoritative sources.
It separates independent development, later release announcement, developer opt-in,
manager admission and candidate validation. A/C participate and B waits; no developer
needs the release branch name to start, and a release does not depend on a nonparticipant
finishing. Main at branch creation can be newer than developer starting commits.

Design/diagram and IT-1 now target feature PRs to the announced RELEASE BRANCH.
Main receives a separate candidate promotion PR; selected native release preparation
remains subject to source-equivalence checks. Branch/source changes require fresh
checks, and later mainline changes cannot silently redefine the selected release.
B retains source/staging evidence and can submit to a future announced candidate.
Assessment and appended accepted proposal are reconciled to this flow. Only current
E.4 narrative records are edited for this request. Root managed artifacts, historical
expert messages and other sprint records are not changed by this correction.

GitHub Flow, Creating a pull request, Keeping a PR in sync, and Microsoft's Git
branching guidance were checked on their official documentation sites. The analysis
states exactly which mechanisms each supports and distinguishes the project's direct
feature-to-release opt-in policy from their complete published workflows. No formal
industry standard is claimed to mandate this exact sequence. Source links are retained
at the relevant claims rather than offered as unsupported general endorsements.

The local checks verify Markdown file targets/anchors, the new analysis-to-design
references, branch-role/participation requirements and pending approval status.
Git diff --check validates whitespace. These document checks do not qualify native
commands, PR automation or runtime behavior. No new test framework/skeleton, reviewer
message, release announcement, database access, code change, commit or push is made;
the current design is a working draft awaiting Product Owner approval.

Check result: the first anchor check identified one pre-existing obsolete PLAN
section anchor in the historical, append-only part of proposedchanges. It is retained
as history, with an appended working link to the current PLAN section. All current
working-record links/anchors and all newly added references pass; that one historical
anchor is the explicit exception. Expert report/feedback diffs remain empty. Whitespace
and the release-timing/participation consistency assertions pass. No native/runtime
check was run for these documentation edits.


## Approved construction entry

2026-11-09. The explicit Product Owner approval is retained in the implementation
handoff. Backlog, progress and execution adapters were read before changes. PBI-060
now expresses three independent staged contributions, A/C participation/admission
and numbered delivery, and B preservation/deferral. Its ID, ordering and assignment
are unchanged; the unrelated PBI-059 addition is preserved. Design status, setup,
README, assessment and board now reflect authorized construction. Earlier audit and
expert messages remain historical. No native/runtime success is asserted at entry.
The initial working-tree inventory includes unrelated E.3 edits and editor backups;
they are excluded from E.4 writes and future staging.


## Handover preparation checkpoint

2026-11-09. The approved implementation and its narrow counter-only recovery
amendment are reconciled across design, setup, implementation, tests, manual,
walkthrough, handover, assessment, README, SRS, architecture and test profile.
PBI-042/PBI-060 now have `tested` execution rows after required gates; PLAN remains
Progress and backlog completion/PO acceptance are not inferred. New traceability
links under progress/backlog/PBI-042 and PBI-060 point to the actual E.4 artifacts.
Pre-existing PBI-059 and E.3 working edits remain outside the checkpoint.

The native author/PR/release/refusal/sync/repeat/browser sequence was executed on
2026-11-09. Final evidence-reader gates ran A1 then A3 then B1 with results 1/1,
3/3 and 2/2 (timestamp 20261109_152509). These do not replay Oracle. The walkthrough's
current read-only blocks were executed, including SQLcl version, Git history,
GitHub issue/PR/release/B-branch reads, archive checksum/listing and VS Code viewing.
Historical write recipes are clearly separated and were not rerun over the delivered
state after central access removal. SQL fenced bodies match their executable helpers.

The editable 41-slide presentation passed package, geometry and first-party import
checks. Every slide was rendered and inspected full size; missing screenshots and
text/code overlaps found in the first draft were corrected, then affected slides
rechecked. The slide-19 caption warning was visually checked: its two lines fit.
Agenda, section dividers, Courier commands, native bullets, closing slide and the
walkthrough slide map agree. Native PowerPoint rendering was not performed.
[The validation receipt](tests/presentation-validation.json) binds the final bytes.

Known generated temporary secrets were scanned against 244 shared files and archive/
PPTX members without matches. Raw source/business snapshots and credentials are not
published. Markdown file targets and current anchors pass; the append-only historical
proposed-change link to the retired E.4 PLAN title remains the documented exception.
Stale E.3 links in maintained README/PLAN were corrected without editing E.3 artifacts.
Changed maintained prose/scripts pass whitespace checks; raw native output retains its
original bytes. Independent Astra handover review is the next gate, not yet a verdict.


## Independent review correction R1-L1

The original Astra report is preserved byte-for-byte. It found no high/medium issue
and one low-severity measurement-label error. Overall author-worker overlap includes
non-native work; individual native receipts establish 14.757295 seconds of capture
and 4.155229 seconds of stage/verify overlap. Implementation, tests, walkthrough and
slide 13 now identify each interval correctly. Historical receipts are untouched.
The existing evidence reader additionally checks distinct successful native PIDs,
author/home correspondence and three-way overlap separately for both native phases.
The derived calculation is retained in tests/native-overlap-calculation.json.

A1/A3/B1 were rerun in order and passed 1/1, 3/3 and 2/2 after this bounded correction.
The deck was re-exported, package/layout/import checked and rerendered; changed slide
13 and the closing slide were re-inspected. Displayed SQL remains unchanged and its
full helper comparison passed earlier. Current Markdown targets/anchors and changed
prose whitespace were rechecked. No native or target operation was repeated. The
corrected checkpoint is prepared for focused independent recheck, not claimed as
independently verified before feedback arrives.
