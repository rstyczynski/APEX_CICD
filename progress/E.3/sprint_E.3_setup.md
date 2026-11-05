# E.3 — Contract and analysis

Configuration update: the [GitHub-owned setup](sprint_E.3_github_configuration.md) supersedes every retained-local-file/tool-path assumption below. Earlier run results remain historical evidence for their original revisions.

Current correction — 2026-11-03: the Product Owner required native APEX/SQLcl
and GitHub Actions control, with all E.3 Python removed. The
[native correction record](sprint_E.3_native_correction.md) supersedes the earlier
1.0.1 implementation described below. Historical evidence is retained.

SPRINT E.3 | MODE: managed | Test: smoke, integration | Regression: smoke

## Contract

The Product Owner explicitly requested E.3 activation and preparation of its
design on 2026-11-03. E.2 is already Done in [PLAN](../../PLAN.md), with an
[accepted handover](../E.2/sprint_E.2_handover.md). E.3 was the sole active sprint at activation. The Product Owner subsequently
accepted and closed it on 2026-11-05; the
[closure record](sprint_E.3_handover.md#sprint-closure) owns the final status.
Only [PBI-053](../../BACKLOG.md#pbi-053-prove-a-simple-git-based-development-to-release-journey)
is assigned. The [scope](sprint_E.3_pipeline_scope.md) bounds the work to an
architectural prototype of one Git-based happy path.

Codex performs the manager, analyst, designer and test-architect responsibilities
serially. The canonical manager and role procedures, generic cooperation/Git/
test rules, GitHub Actions rules and local patch/preferences have been reviewed.
The local patch and explicit request take precedence over generic instructions
to execute all phases or push at each phase. The initial authorization ended at design preparation; at that checkpoint no
implementation, deployment, repository creation or runner registration was
performed. The subsequent authorization and executed outcomes are recorded below.

Keep E.1/E.2 evidence and their tool installations intact. Preserve existing
uncommitted planning edits. Do not weaken broader backlog criteria or turn
deferred production protections into prerequisites for the entire prototype.
Requirements/design changes must be explicit and remain Proposed until review.
Do not claim design checks or failing skeletons establish runtime success.

## Analysis

The full [analysis](sprint_E.3_analysis.md) identifies the actors, happy path,
policy changes, evidence and risks. The selected design recommendation is a
coordinated Working Copy-to-APEX-Main checkpoint captured into a feature branch;
a manually opened/reviewed PR supplies a patch/minor/major label and matching
Conventional Commit squash title. Release Please prepares a release PR with the
version/changelog update; merging it creates the tag and GitHub Release notes. The deployer selects that version tag for a separate manual
release workflow, which builds its resolved accepted commit and deploys to one
lab target. Version assignment does not trigger deployment.

Recommend GitHub Actions: hosted PR checks without lab credentials, and a
manual release job on the local Mac with access to the loopback lab. A small
dedicated private application repository avoids mixing E.1's custom source and
ledger with the native PROJECT prototype. These are design proposals; remote
setup and runner access remain implementation prerequisites requiring concrete
authorization. Existing APEX_CICD is public, as observed by read-only repository
inspection; do not attach an unrestricted lab runner to public PR execution.

The [design and test specification](sprint_E.3_design.md) is ready for Product
Owner review. No scope clarification is needed to prepare it. Repository/runner
selection and prototype policy exceptions are included in that decision, rather
than silently treated as accepted. Runtime/toolchain qualification is pending.
Token accounting is not exposed per phase by this environment; no count is invented.

## Implementation authorization and outcome

The Product Owner approved the flow and explicitly directed implementation
through the end of handover without further questions on 2026-11-03. The
[design](sprint_E.3_design.md) is Accepted, the prototype and required gates
are complete, and the [technical handover](sprint_E.3_handover.md) links the
executed journey and evidence. Final acceptance/closure is not inferred.
Earlier preparation-only authorization statements above describe that stage.
