# E.3 native Git pipeline prototype

APEX Working Copies and SQLcl PROJECT provide the native development and
migration path inherited from E.2. GitHub Actions controls PR checks, release
preparation and the separately dispatched deployment. There is no Python
pipeline, source adapter or custom migration controller.

Start with the [walkthrough](../../progress/E.3/sprint_E.3_increment_demo.md),
[operator manual](../../progress/E.3/user_manual.md) and
[design](../../progress/E.3/sprint_E.3_design.md). The live private example is
[APEX_CICD_E3](https://github.com/rstyczynski/APEX_CICD_E3).

Developer: Working Copy → compare/merge to agreed Main → `project export` →
review/commit source → `project stage` → `project verify` → review/commit dist →
manual PR. Exactly one patch/minor/major label matches its Conventional Commit
title. Squash merge preserves that classification. Release Please prepares
version.txt, CHANGELOG.md and matching GitHub Release notes/tag.

Deployer: explicitly select a published version tag in the manual release
workflow. Its visible steps resolve the source, verify, package one native ZIP,
record private business fields, use native APEX availability, deploy with
PROJECT, compare fields and publish. A failed required step stops later steps.
An APEX import can restore source availability; the workflow reapplies restriction
after import. This bounded gate does not prove atomic maintenance fencing.

The SQL files contain native commands and small lab assertions. Shell snippets
inside the workflow perform Git/CLI operations and compare outputs; jq validates
PR metadata and writes the nonsecret receipt. No standalone orchestration script
is used. SQLcl saved connections and private runner environment stay outside Git.

baseline.bundle retains the reviewed native source/distribution and release
history. Its current main and latest release contain no Python. Earlier commits
and older tags preserve the superseded implementation as historical evidence;
no history is rewritten. Use `git bundle verify` before cloning. Native
verification is mandatory; the E.2 assessment waiver is not reused.
