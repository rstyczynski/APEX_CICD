# E.3 — Corrected native technical handover

The Product Owner rejected the recurring E1 source adaptation and instructed:
remove E.3 Python, inherit E.2 native achievements and use GitHub Actions as
controller. That direction governs this handover. See the
[native correction record](sprint_E.3_native_correction.md),
[walkthrough](sprint_E.3_increment_demo.md), [operator manual](user_manual.md),
[editable deck](sprint_E.3_increment_demo.pptx) and
[accepted design refinement](sprint_E.3_design.md#product-owner-correction--native-tools-and-github-control).
[PLAN](../../PLAN.md) retains E.3 as Progress; final acceptance is separate.

## Delivered path

APEX Working Copy → native compare/merge to agreed Main → native SQLcl PROJECT
export/stage/verify → manually opened classified Git PR → squash merge → Release
Please release PR with version.txt/CHANGELOG.md → tag/GitHub Release notes →
deployer explicitly selects the version → GitHub Actions runs native verify,
packaging, deployment and APEX acceptance/publication steps.

Main's native baseline is established in App Builder. Capture no longer modifies
exported SQL/YAML. SQLcl PROJECT is the migration/package engine, native APEX
availability controls restriction/publication and APEX_SESSION validates
initialization. GitHub Actions provides the controller. PR metadata validation
uses jq; command steps use standard Git/CLI operations. There are no Python
pipeline, preparation, runner or evidence helpers, nor shell release controllers.

The original heading change and Working Copy/Main comparison remain valid
historical authoring evidence. PRs6/7 correct the implementation; release PR8
prepares 1.0.3. The correction record identifies the final source, manual run,
archive identity, browser results and fresh gates. It also preserves the failed
1.0.2 browser check instead of equating a green workflow with working software.

## Reuse and operation

[examples/git-pipeline](../../examples/git-pipeline/README.md) contains the
workflow/SQL configuration and bundled native application history. Use the
existing prepared target E3_TARGET/810203 and official runner e3-lab-mac. Start
it with its own `./run.sh`, using the private SQLcl/Java environment. Saved SQLcl
connections supply credentials; they are not committed or included in artifacts.
The manual explains the native commands and release selection. Old Working
Copies must refresh Main's application definition before later merges.

Only the explicitly selected version is deployed. PR merges, tags and GitHub
Release publication do not trigger deployment. Separate accepted-main control
and selected-tag application checkouts preserve those identities. Business
snapshots remain private; artifacts contain native archives/logs and a receipt.
Retained UAT and historical E.1/E.2 evidence remain intact.

## Scope and acceptance boundary

PBI-053 and children .1/.2/.3 retain their approved prototype criteria and the
SM-1/IT-1/IT-2 checks. The correction does not expand the sprint into a complete
solution. Native import can restore source availability; reapplying restriction
after import does not prove atomic fencing. Full concurrency, drift/identity
coverage, production privileges and general DDL recovery remain deferred.
Native session validation does not replace actual password authentication.
The APEX footer remains 1.0.0, distinct from the repository release version.

The earlier handover was corrected following Product Owner feedback. Technical
verification and Product Owner acceptance remain distinct. No final acceptance,
sprint closure or next sprint activation is inferred. The
[documentation audit](sprint_E.3_documentation_audit.md) records the revision.
