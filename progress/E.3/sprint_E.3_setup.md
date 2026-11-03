# E.3 — Contract and analysis

SPRINT E.3 | MODE: managed | Test: smoke, integration | Regression: smoke

## Contract

The Product Owner explicitly requested E.3 activation and preparation of its
design on 2026-11-03. E.2 is already Done in [PLAN](../../PLAN.md), with an
[accepted handover](../E.2/sprint_E.2_handover.md). E.3 is the sole active sprint.
Only [PBI-053](../../BACKLOG.md#pbi-053-prove-a-simple-git-based-development-to-release-journey)
is assigned. The [scope](sprint_E.3_pipeline_scope.md) bounds the work to an
architectural prototype of one Git-based happy path.

Codex performs the manager, analyst, designer and test-architect responsibilities
serially. The canonical manager and role procedures, generic cooperation/Git/
test rules, GitHub Actions rules and local patch/preferences have been reviewed.
The local patch and explicit request take precedence over generic instructions
to execute all phases or push at each phase. The present authorization ends at
design preparation. No implementation, deployment, repository creation, runner
registration or remote publication is performed in this increment.

Keep E.1/E.2 evidence and their tool installations intact. Preserve existing
uncommitted planning edits. Do not weaken broader backlog criteria or turn
deferred production protections into prerequisites for the entire prototype.
Requirements/design changes must be explicit and remain Proposed until review.
Do not claim design checks or failing skeletons establish runtime success.

## Analysis

The full [analysis](sprint_E.3_analysis.md) identifies the actors, happy path,
policy changes, evidence and risks. The selected design recommendation is a
coordinated Working Copy-to-APEX-Main checkpoint captured into a feature branch;
a manually opened/reviewed PR integrates it into Git main. A separate manual
release workflow builds from an accepted commit and deploys to one lab target.

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
