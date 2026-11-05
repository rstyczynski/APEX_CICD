# E.3 native Git pipeline prototype

APEX Working Copies and SQLcl PROJECT provide the native development and
migration path inherited from E.2. GitHub Actions controls PR checks, release
preparation and the separately dispatched deployment. There is no Python
pipeline, source adapter or custom migration controller.

Start with the [walkthrough](../../progress/E.3/sprint_E.3_increment_demo.md),
[operator manual](../../progress/E.3/user_manual.md) and
[design](../../progress/E.3/sprint_E.3_design.md). The live private example is
[APEX_CICD_E3](https://github.com/rstyczynski/APEX_CICD_E3).

The application repository is a public seed. Every participant, including its
owner, creates `<operator>/APEX_CICD_E3_LAB` once and reuses it for demonstrations.
Use the walkthrough's
[creation procedure](../../progress/E.3/sprint_E.3_increment_demo.md#create-your-own-application-repository-once).
It preserves native baseline history/tags, creates your own public repository
and imports the seed release. Configure your own environment secrets and runner;
those are not transferred by cloning. This creates the GitHub repository, not
the prerequisite Oracle/APEX/ORDS lab.

Developer: Working Copy → compare/merge to agreed Main → `project export` →
review/commit source → `project stage` → `project verify` → review/commit dist →
manual PR. Exactly one patch/minor/major label matches its Conventional Commit
title. Squash merge preserves that classification. Release Please prepares
version.txt and CHANGELOG.md in a proposal PR; automatic tag/publication is disabled.
After that PR merges, run native `project release` on main, review/commit its
metadata and numbered distribution, then tag/publish that accepted commit.
See walkthrough step E for the complete native sequence.

Deployer: explicitly select a published version tag in the manual release
workflow. Its visible steps reject unfrozen/mismatched source, verify, package one native ZIP,
record private business fields, use native APEX availability, deploy with
PROJECT, compare fields and publish. A failed required step stops later steps.
An APEX import can restore source availability; the workflow reapplies restriction
after import. This bounded gate does not prove atomic maintenance fencing.

The SQL files contain native commands and small lab assertions. Shell snippets
inside the workflow perform Git/CLI operations and compare outputs; jq validates
PR metadata and writes the nonsecret receipt. No standalone orchestration script
is used. GitHub environment variables/secrets supply configuration; the setup-native
action installs Java/SQLcl and generates new job-scoped SQLcl connections and
mapping properties under RUNNER_TEMP. Always-run cleanup removes them. No
machine environment file or retained connection store is used. The official
runner registration belongs outside the checkout; .local-apex is scratch only.

baseline.bundle retains the reviewed native source/distribution and release
history. Its current main and latest release contain no Python. Earlier commits
and older tags preserve the superseded implementation as historical evidence;
no history is rewritten. Use `git bundle verify` before cloning. Native
verification is mandatory; the E.2 assessment waiver is not reused.

Review R1-L2 adds a shared AWK missing-file diagnostic assertion and schema-2
receipt checks. Current bundle main contains that corrected controller; v1.0.4
and its original receipt/logs remain unchanged historical application evidence.
The [correction receipt](../../progress/E.3/tests/review-1-correction-checks.json)
records the new seed/bundle identities and offline validation. No new native
qualification or deployment is claimed for this correction.

The manual-only qualification workflow exercises native missing-changeset
rejection without deployment. It shares the setup action and lab concurrency.
See the [GitHub configuration guide](../../progress/E.3/sprint_E.3_github_configuration.md)
for configuration ownership, exact fields and actual run evidence.

The parent lab includes an executable [local runner launcher](../../scripts/e3-runner.sh).
It installs/registers the official runner and checks local Oracle/ORDS reachability
using GitHub variables. It stores runner registration outside the checkout,
clears retired inherited settings and starts the foreground lab runner.
