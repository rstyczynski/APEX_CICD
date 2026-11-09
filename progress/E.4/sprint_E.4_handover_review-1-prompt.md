# E.4 handover review — round 1 prompt

Round: E.4 handover, 1, outbound prompt.
Revision: e32ae318df3c999712d724f73e1bee0ad2977f98, published source checkpoint;
no working implementation patch included. Repository: https://github.com/rstyczynski/APEX_CICD.git,
branch main. `git ls-remote origin refs/heads/main` verified this full SHA before
this prompt-only follow-up. Reviewer: independent Codex chat, gpt-6-astra.
Status: No findings yet.

## Objective and authority

Review the concrete Elaboration PBI-042/PBI-060 handover, including its completeness,
evidence, reproducibility, accuracy and experiment limits. The Product Owner explicitly
requested a NEW dedicated chat named E.4 handover review with Astra and authorized
reviewer contact, overriding the external-review skill's normal relay-only routing.
This is not the earlier E.4 design review or E.3 review. Final PO acceptance and sprint
closure remain pending. Implementation through handover and bounded corrections are
authorized; review itself does not authorize target mutation or broader scope.

Read AGENTS.md, the local patch/preferences and the approved implementation handoff.
Use the pinned revision, even if main advances. The source is available in this shared
local checkout and at the verified remote. Pre-existing unstaged PBI-059 and E.3 changes/
editor backups are excluded: use `git show <SHA>:<path>` for those contextual files,
not their unrelated working bytes. Do not reset/checkout/change the shared Git state.

## Inputs

Start with progress/E.4/sprint_E.4_handover.md, sprint_E.4_increment_demo.md and its
same-basename PPTX, then user_manual.md, sprint_E.4_design.md, sprint_E.4_setup.md,
sprint_E.4_implementation.md, sprint_E.4_tests.md, sprint_E.4_documentation_audit.md,
implementation_handoff.md (actual filename sprint_E.4_implementation_handoff.md),
and tests/ receipts/transcripts. Use root SRS, architecture, README, PLAN, BACKLOG and
PROGRESS_BOARD context as needed. Prior E.4 design reviews are historical scope;
there are no prior findings in this handover-review subject.

Application source is in https://github.com/rstyczynski/APEX_CICD_E3_LAB at release
v1.0.7 / e0f60ff5efc6905c3b6a4c0e7a7a79a6b0134b0c. The committed archive hash is
27541bed6550c9f2dcfb36aeabd5e903bfe09a475fda0b0ec1972aa8ad9a1535.
The new handover PPTX hash is c5d35a89505f5ffd64548e4040711108077ca1b694e318ac3017df026d28f1d9.
The exact final rendered slides may also be inspected read-only at /tmp/e4-pptx/render/
(slide-01.png through slide-41.png); these are a supplied convenience, not a substitute
for the committed PPTX. No credentials or raw business snapshots are review inputs.

## Review focus

Assess the complete independent A/B/C start/capture/stage story, later release start
from newer main, announcement, separate developer opt-in and manager admission,
A/C conflict resolution and fresh validation, native freeze/commit/tag/archive binding,
B absence and preserved original work. Distinguish one-operator role simulation from
real process concurrency. Inspect actual evidence rather than merely trusting summaries.

Assess initial full-source trust, pre/post-baseline pending edits, stale refusal,
availability/checksum lifecycle, full-field preservation, final receipt and repeat.
The Product Owner explicitly approved temporary central developer/proxy access and
reservation, then explicitly approved reviewed counter-only recovery when title
restoration changed only p_version_scn. These narrow approvals are retained in records;
do not judge them as an unauthorized general drift normalizer. Both temporary central
users were removed. First import restored Available; the operational exclusion interval,
not continuous technical restriction, covered it. Production fencing, PBI-056 provisioning,
arbitrary fresh installation and three-human concurrency are outside this experiment.

Assess whether the walkthrough and editable slides explain the journey and current
starting state sufficiently for PO handover. The delivered state is already 1.0.7;
current inspection commands are distinct from historical writes/newly authorized replay.
No live PO demonstration or acceptance has occurred. Evidence-reader gates are not
fresh Oracle execution. Missing material prerequisites or broken commands matter;
production hardening unrelated to this Elaboration boundary should be a deferral.

## Allowed checks and output

Read-only source/evidence, Git history, archive/PPTX inspection and read-only GitHub
queries are allowed. You may run the three documented E.4 manifest gates (local
assertions plus GitHub reads) and syntax/link checks. Rendering/extracting the PPTX
into your own OS temporary directory is allowed. Do not run SQLcl connections,
Oracle/Podman/ORDS commands, deployment, native capture/stage/release, GUI edits,
Git mutations, pushes, API mutations, secret lookup or cleanup. Do not inspect private
credential directories or raw business snapshots. Do not message other chats.

Write ONLY progress/E.4/sprint_E.4_handover_review-1.md in the repository. Preserve
all existing reports/source. Return a concise verdict and report path in your chat.
Start the report with round, full revision, reviewer, scope/exclusions and inputs.
Use narrative per-finding status paragraphs (the local no-table preference applies).
Use stable IDs R1-H1/M1/L1 etc.; each finding needs location, impact, observed vs inferred
evidence, correction and acceptance check. Say what you ran and what you only inspected.
State whether the package is ready for the live Product Owner handover, ready with
nonblocking limitations, or requires correction. Be candid and independently test claims.
