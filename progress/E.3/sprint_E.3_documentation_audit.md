# E.3 — Design preparation audit

2026-11-03. Scope: activation, analysis, proposed design and test specification
for PBI-053. This is not PBI completion or a runtime acceptance record.

## Reconciliation

[PLAN](../../PLAN.md) identifies E.3 as the sole Progress sprint; E.2 is already
Done. The [board](../../PROGRESS_BOARD.md) records PBI-053 under_design because
design approval is pending. No unapproved child rows were created. Broader
backlog definitions and E.1/E.2 historical evidence were not changed by this work.

The [scope](sprint_E.3_pipeline_scope.md), [setup](sprint_E.3_setup.md),
[analysis](sprint_E.3_analysis.md) and [design](sprint_E.3_design.md) agree on one
sequential happy path, manual PR and separate manual release. README/roadmap
reflect activation. SRS, architecture, research and test profile link the design
as Proposed while retaining wider requirements. Implementation and functional
results do not yet exist; their absence is explicit rather than recorded as a pass.

The accepted E.2 handover and clean verification receipt were inspected with
their limits. Official Oracle APEX 24.2/SQLcl 25.4 and GitHub documentation was
read and linked in the design. Documented support is not runtime evidence.
Read-only repository inspection found the existing repository public with main
as default branch. Tool inventory found actionlint, act, Podman and the retained
SQLcl client. Live runner/database connectivity was not verified.

## Verification

`bash -n tests/smoke/test_pipeline.sh tests/integration/test_pipeline.sh` passed.
The [check receipt](tests/design_checks_20261103_121830.json) records the sole
active sprint, PBI/board assignment and current local link-target checks.
`bash tests/run.sh --smoke --new-only progress/E.3/new_tests.manifest` and its
`--integration` counterpart returned expected nonzero results: one and two
explicit pending skeleton failures respectively. Their logs are linked in the
receipt. This verifies registration, not product behavior.

No live regression, workflow actionlint/act execution or deployment is claimed.
Implementation workflows do not yet exist. Design command interfaces are
proposed, not copyable tested walkthroughs. `git diff --check` passed and is
rechecked after adding this audit. This audit's link targets are also rechecked.

## Decision and commit boundary

Architecture, prototype policy exceptions, dedicated private demo repository/
local release runner and three-child decomposition await Product Owner design
approval. The Product Owner subsequently explicitly requested committing and
pushing this stage. That authorizes publication of the proposed analysis/design
checkpoint, without accepting the design or completing PBI-053. This scoped
stage commit includes the earlier E.3 planning changes and expected-red test
skeletons. Runner registration and deployment remain unperformed.

Before this checkpoint, shell syntax and current local link-target checks were
repeated successfully, the registered skeletons again returned their expected
pending failures, and git diff --check passed. No product-runtime gate is claimed.

## Version selection correction — 2026-11-03

The Product Owner clarified that merge introduces the version (a patch increment
for the heading-only change) and the deployer selects the version tag. Analysis,
design, scope, setup, README and test profile now reflect that sequence. The
design specifies reviewed version metadata, an explicit reviewer tagging step
on the accepted merge result, manual version_tag release input and tag-to-commit
resolution recorded with the archive. Tag creation does not trigger deployment;
future automation concerns explicit promotion of a selected version.

The existing user paragraph formatting in the analysis was preserved. This is
a proposed-design correction, not a live tag creation, workflow implementation,
acceptance or deployment. No new runtime tests are warranted for the prose edit;
local link targets and git diff --check are checked before reporting completion.

## Automated versioning and both changelogs — 2026-11-03

The Product Owner requested label-based workflow versioning and both changelog
outputs, then confirmed the label/Conventional Commit flow. The current design
supersedes manual tagging with Release Please: one patch/minor/major label,
matching squash title, automated version/changelog release PR, reviewed merge,
and automated tag/GitHub Release notes. Deployment still requires a manual
version_tag selection. Analysis, setup, scope, README and test profile agree.

GitHub release-note guidance, Release Drafter documentation and Release Please
upstream documentation/strategy source were inspected. Release Please was chosen
because it updates the committed changelog and release notes from one history.
Its input is Conventional Commits; label/title checks provide the explicit bridge,
not an unsupported claim that it directly consumes these PR labels. The simple
strategy uses version.txt. Built-in-token event suppression is documented, with
an explicit manual check of the generated release PR before merge. No personal
access token or extra runner service is introduced by this design amendment.

This remains Proposed and unimplemented. Checks are limited to current local
link targets, textual reconciliation and git diff --check; no new application
or GitHub workflow execution occurred. Earlier manual-tagging statements in this
audit describe superseded proposals, not current operating instructions.

## Completed implementation and technical handover — 2026-11-03

The Product Owner approved implementation through handover without further
questions. The design is Accepted and its three children were assigned on the
board. This supersedes earlier Proposed/commit-boundary statements in this
historical audit. No Product Owner post-execution acceptance or closure is
inferred. PLAN stays Progress; board execution outcomes are tested.

Reconciled README, PLAN/board, roadmap, SRS, architecture, research and test
profile with accepted prototype scope and observed results. Shared E.1
requirements remain broader than the E.3 evidence. Setup, analysis, accepted
design, implementation, tests, bugs, walkthrough, manual, presentation and
handover link one another. The accepted instructions authorize sequential role
execution and routine corrections without new approval stops. Historical
E.1/E.2 sprint evidence is unchanged. E.4/E.5 are not activated.

The private demonstration repository contains actual classified PRs, generated
version/changelog metadata, tags and remote execution. The native stage branch,
mapping path, inherited runtime hook and detached-HEAD failures have explicit
corrections. Runtime conversion is pre-stage source adaptation, not an archive
edit or a claim of full E.1 protection replacement. Workflow main SHA and selected
application tag SHA are separate identities. Source/release evidence records
are linked from tests and the handover. The later 1.0.2 release proposal remains
unmerged/undeployed by design. The source Git bundle retains both tags and final
main; its receipt identifies its bytes and commit.

Actual checks: new smoke 1/1; new integration 2/2; full smoke regression 2/2,
all with timestamped logs. IT-1 verifies actual downloaded archive SHA-256,
remote PR/tag/run state, both changelogs and live field preservation; IT-2 runs
real missing-changeset rejection against a throwaway clone. Browser Home/history
were inspected after deployment. A separate throwaway source-clone rehearsal
ran the actual capture.sh/pre-stage adapter/stage/native verify successfully.
The canonical native artifact used in the remote run was not repacked afterward.
Configured credential values were scanned against tracked demonstration source;
private configuration, connection stores, runner credentials and runtime rows
remain outside the delivered Git/CI artifacts.

The 12-slide PPTX was built with the presentation skill's bundled Artifact Tool,
rendered and individually reviewed. Package integrity, layout/font checks and
first-party reimport passed with no findings/warnings. Initial narrow historical
captures were retained, while the readable Working Copy inspection was labeled
as later evidence; the final deck crop was rechecked. No native PowerPoint
application inspection is claimed. [Presentation receipt](tests/presentation-checks.json)
records exact output identity. The Markdown slide map matches all 12 slides.

Local link/anchor consistency, Python/shell syntax, bundle integrity, source
scope and git diff --check are rechecked before the completion commit. No test
or runtime repetition is used to disguise the earlier observations. The
[completion report](sprint_E.3_completion.md) identifies delivered phases,
parameters, evidence and deferred work. A single scoped completion commit groups
the coherent three-child prototype, shared tooling, test evidence and handover;
the final response identifies its hash. No sprint completion is inferred.

Final current-document checks passed: 324 local link targets and 36 anchors,
sole active sprint/board/decomposition consistency, bundle integrity and the
canonical PPTX hash. [Receipt](tests/final-document-checks.json) records scope.
The preparation entry point was also rerun against the retained lab and correctly
refused overwrite before mutation. Final Python syntax and diff-whitespace checks
passed. Earlier design-stage pending/red statements were reconciled with their
current results while preserving the historical receipts.

## Staged-log formatting correction

Completion commit a106ccc was created after the staged whitespace check reported
SQLcl table padding in the newly staged rejection log. This was a check-handling
error, not a product-test failure. Raw bytes are preserved in the original commit
and privately under .local-apex/e3/logs/native-verification-rejection-raw.log.
The maintained readable log now removes trailing spaces/blank end lines only;
the evidence exporter applies that same deterministic formatting on future runs.
No error text, source/target identity or test criterion changes. The correction
is checked before a follow-up commit; no prior commit or release tag is rewritten.

## Native correction audit — 2026-11-03

The Product Owner explicitly rejected Python/source adaptation. The
[native correction record](sprint_E.3_native_correction.md), design refinement,
manual, walkthrough, handover, deck and shared orientation now reflect native
APEX/SQLcl with GitHub Actions control. Earlier 1.0.1 implementation records are
marked historical. No E.1/E.2 source history was rewritten. The baseline bundle
was regenerated and separately hashed with current main/tags; older identity
receipts remain historical. Removed Python helpers/caches and shell controllers.

Hosted patch/release checks and manual v1.0.3 execution passed. A1 1/1, A3 2/2,
B1 2/2 passed freshly. Native APEX_SESSION reproduced the failed 1.0.2
initialization, then validated corrected 1.0.3 before publication. Actual browser
authentication, heading and retained history were checked again. The source
export omits the initialization property; no source translation is used.

The first documentation build lacked the runtime-module environment for import
verification. That environment was supplied; final native-v2 package/layout/font
and first-party import checks passed with zero findings/warnings. All twelve
final slide renders were individually inspected. No native PowerPoint run is
claimed. The final PPTX is copied unchanged from that validated output.

Independent clean-checkout provisioning remains outside this correction; the
manual explicitly requires prepared private lab state. Existing unrelated
Product Owner edits to fresh-setup requirements/backlog are preserved.
Final local link, source, whitespace and credential-value checks are recorded
in the native correction checks receipt before the scoped completion commit.

## GitHub configuration and local-runner correction

The Product Owner rejected machine environment files and confirmed that the lab
uses a local runner with a runnable repository script. The
[configuration record](sprint_E.3_github_configuration.md), manual, walkthrough,
design, README, SRS, test profile, PLAN and AGENTS policy now state GitHub
configuration ownership and temporary-only scratch. PBI-054's wording was
corrected without assigning/closing it or claiming a new-operator infrastructure
proof. The retired E.3 native.env/lab.json/custom launch helper were deleted;
native runner registration moved outside the checkout. No OS service was
installed; the latest Product Owner direction is the foreground lab launcher.

The executable scripts/e3-runner.sh was checked with bash -n; help, preflight,
status, existing-registration setup and real launch were exercised. It reached
Oracle TCP and ORDS HTTP, then executed the final 1.0.4 release and qualification
through the official runner. Bootstrap on a different machine was not claimed.

A1 1/1, A3 2/2 and B1 2/2 passed. The updated platform smoke checks actual
ORDS/APEX login using GitHub configuration; it does not re-run the historical
five-schema identity checks through retired local configuration. The first
HTTP probe lacked cookie persistence and failed on redirects; this test issue
was corrected with an OS-temporary cookie jar and rechecked successfully.
Native missing-changeset rejection and private cleanup passed on GitHub. Browser
authentication, heading and retained history were observed again. Downloaded
artifacts/evidence use OS temporary directories; no environment state is read
from .local-apex. Its remaining presentation build/cache usage is disposable.

The deck adds a configuration/topology slide and updates the walkthrough map
to 13 slides. Final package/layout/import checks, individual slide inspection,
local links, source matching and executable checks are recorded in the GitHub
configuration evidence receipts before the scoped completion commit.

### Runner setup explanation correction — 2026-11-03

The Product Owner requested explicit setup documentation in the implementation record and presentation pair. The manual already contained the setup and launch commands; the implementation record and walkthrough only linked to the launcher, and slide 4 omitted setup. The [implementation record](sprint_E.3_implementation.md#current-runner-installation-and-launch), [walkthrough stage 5](sprint_E.3_increment_demo.md#5-deployer-selects-the-version) and PPTX slide 4 now distinguish one-time installation/registration from starting the foreground listener each lab session. They state the persistent directory, expected output, GitHub authentication and connectivity prerequisites, retained matching registration and the boundary between runner setup, existing lab infrastructure and workflow tool setup.

This documentation correction was checked against the actual launcher source. Script syntax, local links/anchors, PPTX package/layout and first-party import passed. Slide 4 was visually inspected; the other 12 rendered PNGs are byte-identical to the previous inspected revision. One density warning on slide 4 was reviewed and accepted with readable, unclipped text. The [presentation receipt](tests/github-presentation-checks.json) now identifies the revised canonical deck; [documentation checks](tests/runner-setup-document-checks.json) record this scope. Setup and live runner execution were not repeated for this text-only change; prior operational evidence remains historical. No sprint or PBI status was changed.
