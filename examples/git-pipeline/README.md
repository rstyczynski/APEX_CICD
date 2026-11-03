# E.3 Git pipeline prototype

This directory contains the small reusable pipeline scripts/workflows and the
complete reviewed application history in baseline.bundle. The private live
example is [APEX_CICD_E3](https://github.com/rstyczynski/APEX_CICD_E3).
Start with the [E.3 walkthrough](../../progress/E.3/sprint_E.3_increment_demo.md)
and [operator manual](../../progress/E.3/user_manual.md). The
[accepted design](../../progress/E.3/sprint_E.3_design.md) explains the boundary.

The ordinary path is Working Copy, agreed Main checkpoint, native source capture
and stage, patch/minor/major label plus matching Conventional Commit title,
squash merge, Release Please release PR, generated tag/changelogs, then manual
deployment of a selected tag. The deployment workflow is read from main; its
application source comes from the selected tag. No PR/tag/release event deploys.

baseline.bundle preserves the inspected Git history, native .dbtools/src/dist
and both 1.0.0/1.0.1 tags; the latter includes the corrected runtime source.
Its main also contains the reviewed workflow checkout correction. Use Git bundle
verify before cloning it. The [bundle receipt](../../progress/E.3/tests/bundle.json)
records identity. Do not copy runtime tools, connection stores or business data
into Git. scripts/lab.py reads only the private E3_LAB_CONFIG path. Native PROJECT
is the sole migration/packaging engine; the source adapter is explicit and runs
before stage. Existing broad production requirements remain unproven.
