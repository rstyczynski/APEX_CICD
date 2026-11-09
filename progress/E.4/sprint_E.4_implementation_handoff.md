# E.4 — Approved implementation handoff

## Product Owner authorization — 2026-11-09

The Product Owner approved the current analysis/design in the E.4 design chat and
instructed implementation in a new chat named **E.4 implementation**, continuing
through Product Owner handover preparation without intermediate approval stops.
At the end, conduct an independent Astra review in a separate new chat named
**E.4 handover review**, then supply the Product Owner handover document and PPTX.
The earlier waiver applied to another design review, not to this newly requested
handover review. Final handover acceptance and sprint closure remain Product Owner
rights; do not invent a live demonstration or their satisfaction/acceptance.

## Approved scenario

The [analysis](sprint_E.4_setup.md#analysis) and
[design/test specification](sprint_E.4_design.md) in the current working checkout
are the approved inputs, including uncommitted revisions after the older published
Astra design checkpoint. Do not implement the obsolete serial design from HEAD.

Developers independently work, test, capture and stage on separate author fixtures
and feature branches. Later the Release Manager creates a release branch from current
accepted main, announces its name and invites submissions. Its starting commit may
be newer than the developers' starts. Developers choose whether to participate:
A/C submit PRs targeting that announced branch; B chooses to postpone. The manager
separately reviews readiness/checks/dependencies and admits A/C. Preserve B's source,
branch and staged work for a later normal release. No developer must wait for another
PR merge to begin or first-stage their change. The candidate contains its inherited
main baseline plus A/C; prove B absent from source/distribution/artifact and central
DEV. Reconcile source and generated snapshot/changelog conflicts and freshly validate
the resolved candidate before native numbered release and deliberate synchronization.
Exercise PBI-042's stale-candidate/pending-edit refusals, trusted initial baseline,
actual status/checksum lifecycle, data preservation and safe repeat.

## Implementation responsibility

Use the RUP entry skill, local patch/preferences, relevant artifact adapters and
canonical construction/test/documentor procedures. Record the explicit approval in
design and reconcile setup, assessment, README and board before execution. This
approval also accepts the stated PBI-060 refinement from three-in-one-release to
selective A/C delivery with B retained: route concise backlog wording alignment
through rup-backlog, preserving the assigned parent ID/priority and scope. Do not
leave the old criterion as a hidden ambiguity or claim it passed unchanged.

Scope is PBI-042/PBI-060, APEX/SQLcl native and GitHub native. PBI-056 provisioning
service, broader production fencing/security and unrelated Construction work remain
excluded. Prepare only the necessary fixed experiment fixtures using supported native
interfaces; qualify actual identity/source-path equivalence and host capacity. Never
replace missing independence with serial resets/shared-author capture, fake parallel
evidence or a silent toolchain upgrade. Record actual participants versus role simulation.

Follow NFR-5 before native operations: the executable release/build must match the
selected Git state's project metadata, including historical states. Use GitHub
variables/secrets and temporary private connections; scratch is not authoritative.
Preserve the narrow prepared-host credential exception without expanding/copying it.
The inherited fresh-install guard is a known issue to handle explicitly, not bypass
by editing an old released changeset. Preserve retained data and other lab targets.

Resolve routine implementation issues and bounded corrections within the approved
scope without asking again. Use tool permission requests when technically required;
do not circumvent them. If a genuinely unavailable prerequisite or material change
blocks the approved scenario, report the exact evidence and required decision rather
than claim completion. Ordinary GitHub work needed for the approved lab journey and
existing review-publication authorization follows repository policy; no force pushes,
secret disclosure or unrelated publication is authorized.

## Workspace preservation

At dispatch, current E.4 records, README and docs contain approved working design
changes. BACKLOG has a pre-existing PBI-059 addition; retain it without absorbing it
into unrelated completion claims. Pre-existing modified E.3 model.drawio, final gap
analysis and increment_demo.pptx, plus editor backup files, are unrelated. Do not
revert, overwrite, delete or stage them with E.4 work. No new worktree is requested.
Use the current checkout and scoped commits/audits; avoid concurrent writers to the
same artifacts. The design chat coordinator will not edit while implementation runs.

## Handover and independent review

Produce implementation and test evidence, user_manual.md,
sprint_E.4_increment_demo.md with runnable end-to-end steps,
sprint_E.4_increment_demo.pptx (same basename), and sprint_E.4_handover.md.
Use the presentations skill and bundled runtime; preserve editable content, render
and visually inspect all slides. Follow current preferences: agenda/section dividers,
closing slide, readable desktop captures, Courier for trees/commands, editable native
bullets, complete SQL source and explanation before invocation. Rehearse/preflight
the actual walkthrough and distinguish browser observations from API fixtures and
historical evidence. The handover doc must make delivered/unfinished outcomes and
all limitations clear without assembling raw logs.

Only when the implementation, tests and handover package are concrete, use
rup-external-review to prepare an exact-revision prompt and create the new dedicated
**E.4 handover review** chat with model gpt-6-astra. The Product Owner explicitly
requested that new chat and reviewer contact. Do not reuse E.3 review or E.4 design
review chats. Give the reviewer read-only source/evidence and report-only write scope;
no target mutation. Wait for their report, answer findings, make in-scope corrections
and obtain focused recheck where needed. Preserve original expert text. Do not stop
with a relay prompt or an unfinished reviewer request; carry through the review and
handover deliverables. Do not create review placeholders before evidence exists.

Return a self-contained final handover with artifact links, actual gate outcomes,
source/release/artifact provenance, review verdict, remaining limits and the exact
live Product Owner demonstration/acceptance still required. Emit created-thread
directives for chats you create. The design coordinator will monitor this chat using
compact wait snapshots; no cross-chat reply is required to report completion.
