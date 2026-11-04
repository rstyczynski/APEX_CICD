# E.3 — Native pipeline and local runner handover

**Start with the [final walkthrough](sprint_E.3_increment_demo.md#run-it-yourself).**
It is the single manual execution entry point: prerequisites, configuration,
runner startup, native authoring, PR/versioning, deployment and browser checks
are presented in order alongside the slide numbers.

The application repository is now a public seed. The walkthrough includes
[creation of an operator-owned repository](sprint_E.3_increment_demo.md#create-your-own-application-repository-once)
with native baseline history/tags, release metadata, PR labels and Actions
permissions. Each participant supplies their own GitHub environment and runner;
the procedure creates the repository and assumes the existing native lab.
The shared `rstyczynski/APEX_CICD_E3` is the seed; every participant, including
its owner, runs demonstrations in `<operator>/APEX_CICD_E3_LAB`. Create that
repository once, then reuse it on later runs.
The [lab setup](sprint_E.3_increment_demo.md#create-your-own-application-repository-once)
configures the repository and its e3-lab environment, main branch policy, eight
variables and the two encrypted secrets in one command block. Existing secrets
are retained; missing values are requested through secure interactive prompts.
The [publication and creation check](tests/github-public-repository.md) records
visibility verification, secret-scan scope and local baseline-clone validation.

The executable runner entry point is
[scripts/e3-runner.sh](../../scripts/e3-runner.sh). From the laboratory repository
root, the lab operator can retain/configure the official local runner and start it:

```bash
e3_repo="$(gh api user --jq .login)/APEX_CICD_E3_LAB"
./scripts/e3-runner.sh setup --repo "$e3_repo" --directory "$HOME/actions-runner-e3-lab"
./scripts/e3-runner.sh --repo "$e3_repo" --directory "$HOME/actions-runner-e3-lab"
```

The launcher was exercised, reached local Oracle/ORDS and ran both the selected-tag
deployment and native rejection check. It remains a foreground local lab runner,
as explicitly requested; no OS service was installed. Once it is online, the
deployer only selects a published version tag and dispatches the release workflow.

The [manual](user_manual.md) defines configuration, setup and operation. The
[configuration record](sprint_E.3_github_configuration.md),
[walkthrough](sprint_E.3_increment_demo.md),
[editable deck](sprint_E.3_increment_demo.pptx),
[design](sprint_E.3_design.md) and [audit](sprint_E.3_documentation_audit.md)
connect implementation, evidence and limits.

## Current delivered boundary

GitHub environment e3-lab owns eight nonsecret variables and two encrypted
schema-password secrets, restricted to main. Workflow setup explicitly installs
Java and pinned SQLcl, adds sql to PATH, generates private native connections
and target mappings under RUNNER_TEMP, and cleans them afterward. No machine
native.env, retained local SQLcl store, committed target properties or .local-apex
settings are used. .local-apex is disposable scratch only. Runner registration
is persistent host infrastructure outside the checkout. AGENTS and NFR-4 now
record that boundary; PBI-054 retains the broader independent-operator/lab proof.

Native APEX Working Copies/Main and SQLcl PROJECT provide the inherited source,
verification, packaging and migration path. GitHub Actions controls ordered steps.
The versioned Bash launcher manages local runner infrastructure; it is not a
migration/release controller. There is no Python implementation or recurring
source adapter in the E.3 pipeline.

## Executed result

[Version 1.0.4](https://github.com/rstyczynski/APEX_CICD_E3/releases/tag/v1.0.4)
was explicitly selected in
[deployment 41679427616](https://github.com/rstyczynski/APEX_CICD_E3/actions/runs/41679427616).
It passed explicit tool/connection setup, native verification, packaging,
deployment, retained-field comparison, native APEX session validation and cleanup.
The [receipt](tests/github-release-receipt.json) binds source and native ZIP hash.
The separate [qualification 41679432928](https://github.com/rstyczynski/APEX_CICD_E3/actions/runs/41679432928)
proved a missing included changeset is rejected with target unchanged, without
calling deployment. These jobs ran through the repository's local launcher.

New smoke passed 1/1, integration 2/2 and full smoke 2/2. Browser sign-in as
LAB_USER showed the expected Home heading and the original Hello World history
row. [Browser observation](tests/github-browser.json) and
[gate evidence](sprint_E.3_github_configuration.md#verification-scope) retain the
results, including the initial HTTP-test cookie correction. Configuration/private
connection files and raw business snapshots are absent from uploaded artifacts.
GitHub-hosted runners do not access this localhost lab; the local runner uses
its published Oracle/ORDS network ports and needs no APEX installation files.

## Scope and acceptance

PBI-053 and children .1/.2/.3 retain the approved bounded architecture-prototype
criteria and remain tested. Ordinary PR integration, automated version/changelog
preparation and manual deployment remain separate. Both CHANGELOG.md and GitHub
Release notes are generated; no PR merge/tag publication triggers deployment.

This does not complete independent clean-lab provisioning, full drift/identity/
fencing, general DDL recovery or production operation. Native import may restore
source availability; status gating is not atomic fencing. The inherited APEX
footer remains 1.0.0, distinct from the Git release version. Historical E.1/E.2
and earlier E.3 evidence remains attributable to its original revision.

Technical handover is delivered. PLAN remains Progress pending separate Product
Owner acceptance/closure; no next sprint or unscheduled PBI completion is inferred.

## External technical handover review

Round 1 is prepared against published parent revision
`b695ec9627f1453220a04032563f812242f7ac0f`. The
[expert prompt](sprint_E.3_handover_review-1-prompt.md) identifies the exact
application snapshot, accessible source/evidence and Elaboration review boundary.
The [original expert report](sprint_E.3_handover_review-1.md) has arrived and is
preserved unchanged. It recommends corrections for the bounded handover: two
medium and two low findings, with no high-severity finding invalidating the
recorded prototype result. The
[engineering response](sprint_E.3_handover_review-1-response.md) agrees with
R1-M1, R1-M2 and R1-L2, and partly agrees with R1-L1 while identifying the
Product Owner's explicit credential-lookup direction. These are engineering
positions, not selected or implemented corrections. Expert feedback on the
response is the next exchange. No round closure or sprint acceptance is claimed.
