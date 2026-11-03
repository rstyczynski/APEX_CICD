# E.3 — Git-based pipeline prototype design

Repository setup update (2026-11-03): the Product Owner requested public access
and an operator-owned repository creation procedure. The
[final walkthrough](sprint_E.3_increment_demo.md#create-your-own-application-repository-once)
supersedes the private-repository setup proposal below. It preserves the native
baseline history/tags, configures each operator's repository and uses sibling
working checkouts under `~/projects`; no environment settings live in scratch.

## PBI-053 — Simple development-to-release journey

Status: Accepted

Prepared 2026-11-03. [Setup](sprint_E.3_setup.md) and
[analysis](sprint_E.3_analysis.md) explain the contract and actor goals;
[scope](sprint_E.3_pipeline_scope.md) defines the prototype boundary.
[SRS](../../docs/srs.md), [architecture](../../docs/architecture.md) and
[test profile](../../docs/test-profile.md) own shared product guidance.
The Product Owner approved implementation through handover on 2026-11-03,
including this design and its child decomposition. Routine implementation
choices proceed without further questions; actual results remain evidence-based.

### Requirement Summary

Show one Home-heading change from APEX Working Copy to reviewed Git source,
then a separately initiated release to a lab target. Keep it simple enough
to follow live. Git main supplies accepted source; integration feeds automated release preparation; merging the generated release
PR creates the version tag that the deployer explicitly selects. A PR is not a deployment request. Do not implement the former full E.3/E.4 delivery programme.

### Feasibility Analysis

Oracle documents [Working Copy comparison and selective Main merge](https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/about-working-copies.html).
E.2 [demonstrated that checkpoint](../E.2/tests/project-f1-working-copy-validation.json).
Use it rather than assume direct private-copy capture preserves identities.
Working Copies isolate metadata, not the schema, and native merges replace
selected components; inspect differences and exclude concurrent Main editing.

[SQLcl 25.4 PROJECT](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.4/sqcug/project.html)
provides export, stage, verify, gen-artifact and deploy. Pin **25.4.1.022.0618**
and the existing Java 21 installation, guided by the
[E.2 clean comparison](../E.2/tests/project-verify-fix-validation.json).
Use newly generated consistent source/distribution. Native verification errors
are release failures; never carry E.2's prerelease-assessment bypass forward.

[GitHub manual workflows](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)
support workflow_dispatch and explicit inputs. The workflow must exist on the
default branch. [Workflow events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)
allow PR checks without a deployment trigger. A [self-hosted runner](https://docs.github.com/en/actions/concepts/runners/self-hosted-runners)
can reach the local lab; connectivity, repository access and runner setup remain
unverified. Documentation was checked on 2026-11-03; documented support is not
an E.3 execution result.

### Design Overview

```mermaid
flowchart LR
  W[Working Copy: edit Home] --> A[APEX Main: reviewed DEV checkpoint]
  A --> C[PROJECT export and stage into feature branch]
  C --> P[Developer manually opens PR]
  P --> V[Hosted checks: no database access]
  V --> M[Reviewer squash merges classified PR]
  M --> B[Release Please updates version and CHANGELOG in release PR]
  B --> H[Reviewer merges release PR]
  H --> G[Workflow creates version tag and GitHub Release notes]
  G -. available for release .-> D[Deployer selects version tag and runs release]
  D --> R[Local runner: verify and package Git source]
  R --> T[Deploy archive to disposable lab target]
  T --> O[Check heading and retained history]
```

Recommend one small **private GitHub demonstration repository** containing the
native PROJECT application, generated distribution, three workflows and thin
scripts. It holds Foundation/Hello/World together, not one repository per
developer or component. Keep its working clone under ignored `.local-apex/e3/`.
Version its bootstrap recipe and reviewed seed source in this project so it is
reproducible. Keep E.1 source and migration/control history untouched. A separate
repository avoids configuring native PROJECT over the research/method monorepo;
it is a prototype packaging choice, not a general repository architecture mandate.
Creating/publishing the repository and registering a runner are subsequent
external setup actions, not performed by design approval or this document.

Reuse the current lab host and a prepared author application and disposable
integration target. Resolve actual schema/workspace/application identities
through the existing nonsecret environment definitions during preflight.
Do not use retained UAT, reset the whole lab or overwrite unexported DEV work.
Record and check the selected inventory before any setup mutation. One target
and one serial deployer suffice; no environment matrix or automatic provisioning
service is needed.

### Technical Specification

The proposed application repository contains native `.dbtools/`, `src/`,
`dist/` and `utils/` content; `version.txt` and `CHANGELOG.md`; thin
`scripts/capture.sh`, `scripts/check.sh`, `scripts/release.sh`; and workflows
`pr.yml`, `version.yml` and `release.yml` under `.github/workflows/`.
Generated ZIPs, tools, connection stores and run data stay outside Git.
These files are proposed interfaces, not currently executable deliverables.

Capture is manual developer work. Start a feature branch from accepted Git
main and confirm its source baseline matches the author application. Make the
heading edit in a Working Copy, selectively merge the reviewed change into APEX
Main, then run native `project export -list` and `project export`. The export
filter selects only the agreed Main application and required business objects,
excluding private copies, control/ledger objects, secrets and runtime data.
Review the diff, commit source, run `project stage -branch-name e3-base` against
a local branch pointing to the recorded release baseline, review/commit the
generated distribution and mapping hooks, then push and manually open the PR.
Use normal `codex/` feature branches; confirm slash-containing branch behavior
with 25.4.1 before relying on it. If that fails, report the limitation and propose
a simple explicit branch convention rather than silently rewriting stage paths.

The source baseline and distribution are fixed before review. A later source
edit requires a new export/stage/review cycle. The capture script prints the
actual base revision and inventory. It must not silently merge Main, push, open
a PR or export from a guessed application. For this one-change prototype the
reviewer confirms no unrelated Main changes were included.

### PR classification and automated version/changelog preparation

Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) and
[Release Please](https://github.com/googleapis/release-please-action) rather
than a custom version/changelog generator. This is an established tool-supported
pattern, not a claim that GitHub mandates a single release process. GitHub's
[native release notes](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes)
can categorize PRs by labels, but do not by themselves define our version-bump
policy or update a repository changelog.

Each ordinary change PR has exactly one of `patch`, `minor`, `major`. The author
sets a matching Conventional Commit title: `patch` requires `fix:`, `minor`
requires `feat:`, and `major` requires `feat!:` for this simple prototype.
For example, the heading correction is `patch` plus `fix: update Home heading`.
Scopes may be used consistently, such as `fix(home): ...`. Broader Conventional
Commit types and component-contract version policies remain later refinement;
this small mapping is intentionally explicit. Do not infer breaking behavior
from the size of a diff. The reviewer confirms the classification.

`pr.yml` runs on pull_request targeting main, including edited, labeled and
unlabeled events as well as new commits. Use a hosted runner, contents:read,
no deployment credentials and no lab access. Check exactly one change-level
label, its title mapping, shell/workflow syntax via actionlint and the native
source/distribution inventory. Missing/multiple labels or mismatched titles
fail validation. Configure squash merging to use the PR title, and verify that
message when merging. Release Please reads **merged Conventional Commit
messages**, not these labels directly; this validation preserves their meaning
in Git history. This check does not certify Oracle runtime behavior.

`version.yml` runs on pushes to main on a hosted runner. Use Release Please's
single-package `simple` strategy: it maintains `version.txt` and `CHANGELOG.md`.
Bootstrap an accepted version at or above 1.0.0 so patch/minor/major behavior is
unambiguous. Pin the action to a reviewed commit of a supported release during
implementation, rather than an unreviewed floating branch. Its documented
[configuration](https://github.com/googleapis/release-please/blob/main/docs/customizing.md)
and [simple strategy](https://github.com/googleapis/release-please/blob/main/src/strategies/simple.ts)
supply version and changelog updates without custom string editing.

After an ordinary squash merge, Release Please opens/updates a release PR with
the next version and accumulated CHANGELOG entry. `fix:` yields a patch,
`feat:` a minor, and `feat!:` a major; the highest required increment across
unreleased changes wins. Several feature PRs may accumulate in that release PR.
For the one heading change from 1.0.0, review the generated 1.0.1 proposal.
Merging the release PR commits the generated version/changelog and lets the
workflow create `v1.0.1` and a GitHub Release with matching version-specific
notes. The tag identifies the **release PR merge commit**, which includes the
accepted change plus generated metadata. This replaces the earlier manual
reviewer-tagging step. An ordinary feature merge prepares a release; it does
not by itself finalize a tag. Release-PR merge and deployment are separate decisions.

Both changelog outputs come from Release Please's same history/version data:
`CHANGELOG.md` is the cumulative repository record, and each GitHub Release
contains that version's notes. Do not independently hand-edit/regenerate a
second competing changelog. This is the prototype application/release version;
it does not automatically increment every Foundation/Hello/World contract.
Do not change generated APEX exports after stage just to stamp the new version.
Report the release tag in the receipt/UI evidence separately from any component
or APEX source display version until a qualified version-injection hook is chosen.

The release-preparation job has repository-scoped contents/pull-requests/issues
write permissions required by the action, and no lab credentials. Enable the
repository setting allowing Actions to create PRs. Use the built-in GITHUB_TOKEN
for the small supervised prototype. As the action's documentation explains,
bot-created PRs do not automatically trigger further workflows with that token.
Therefore also make hosted `pr.yml` manually dispatchable, and explicitly run
its checks on the generated release PR's current head before human review/merge.
The generated release PR is checked as release metadata (version/changelog and
bot-managed metadata), not forced to carry an ordinary change label or `fix:`
title. Recognize the actual tool-generated PR and inspect its limited diff;
an arbitrary `autorelease` label is not sufficient evidence of that status.
A scoped GitHub App token for fully automatic release-PR checks can be considered
later; it is not needed to demonstrate this path. Use the same read-only checks
locally first. No pull_request_target job or self-hosted PR runner is needed.

Neither ordinary PR merge, release PR merge, tag creation nor GitHub Release
publication can invoke the lab deployment job. `version.yml` has no deploy step.
This avoids relying on GITHUB_TOKEN event suppression as a deployment control.

`release.yml` runs **only** on workflow_dispatch from Git main. Require a
`version_tag` input such as `v1.0.1`; keep the target fixed to the configured
disposable integration role. The deployer selects a version, not a free-form
commit SHA. Fetch the exact `refs/tags/` reference, validate the `vMAJOR.MINOR.PATCH`
format and resolve it to a commit once. Require that commit to be reachable
from accepted remote main and that its `version.txt` equals the tag without `v` and the matching published GitHub
Release exists with that version's changelog entry.
Then check out the resolved commit in an isolated build directory and retain
both tag and resolved SHA. Do not substitute latest main if a tag is missing.
[Git revision resolution](https://git-scm.com/docs/git-rev-parse) supports
resolving a tag to its commit. Reject invocation from a feature branch.
For this supervised prototype the reviewer/deployer confirms the PR was
accepted; do not claim independent attestation or protected tag enforcement.
Pass inputs through environment variables and validate them before shell use,
rather than interpolating workflow expressions into commands.

Use a dedicated local runner label for the release job, contents:read and one
fixed concurrency group with cancel-in-progress:false. Do not send PR jobs to
that runner. The job rechecks the selected commit and pinned tool version,
establishes `e3-base` at the committed baseline SHA and runs
`project verify -cbn e3-base -verbose`. Require zero verification errors, not
just a successful process message. Then `project gen-artifact` creates one ZIP
named with the selected version and run ID. Do not run export/stage against live
DEV in the release job; do not mutate or commit release source there.

For this prototype, package the reviewed native next distribution. Do not add
`project release` freezing or release-job tagging/commit-back orchestration.
Release Please already assigned the Git version tag after release-PR merge;
the deployment job consumes it without incrementing a version.
If freezing changes the distribution later, the new bytes need new qualification.
Calculate SHA-256 and record version tag, resolved source SHA, base SHA, tool version, artifact hash,
run ID and fixed target in a small release receipt. This is traceability, not
cryptographic attestation. Retain the ZIP, redacted logs and receipt as run
artifacts. Never upload a connection store, credentials or business data.

Connect with a schema-scoped saved connection on the local runner; use the
reviewed native installer/defaults-file mapping, then `project deploy -file`
on that exact archive. Retain one migration authority: PROJECT's Liquibase
distribution. Do not invoke the E.1 custom installer/ledger around it. Run
explicit post-deploy SQL checks for the expected heading and unchanged prior
history/configuration, then inspect the target in the browser. Build/verify/check
failures stop downstream steps. A post-commit deployment failure is a failed
run requiring inspection; no destructive reset or automatic repair/retry occurs.

Preservation uses a private before/after baseline of the selected target, not
business rows in Git or downloadable CI logs. Restrict/publish the app through
the already exercised native gate as needed. This does not prove request draining,
stale-worker fencing, full identity preservation, drift rejection or safe recovery.
Do not reuse E.2 archives as a newly qualified baseline: bootstrap a reviewed
E.3 baseline, verify it with the pinned client and record its own installation
and target identity before the visible change.

### Selective future automation

Version tags are already part of the E.3 baseline; only deployment remains
manually triggered. Several PRs can be integrated and versioned without deploying
each one: the deployer selects the desired accumulated version. Creating a tag
or merging a PR must leave the release target unchanged.

Keep future automation design-only: an explicit promotion approval for an
existing version tag could invoke the same release path, require fresh candidate
checks and select an allowed target. This separates version assignment from
permission to deploy. Do not automatically deploy every PR or every version tag.
Version/changelog/tag generation is already automated in E.3; automatic
promotion and multi-target deployment remain later work.

### Implementation Approach and child outcomes

PBI-053.1, parent PBI-053: establish the reviewed E.3 baseline, tool/client and
Working Copy-to-Git checkpoint. Evidence is one intentional heading diff plus
consistent native source/distribution verification. No child dependency.

PBI-053.2, parent PBI-053: demonstrate manually opened PR, lightweight checks,
review and squash integration, followed by the generated release PR and its
reviewed merge. Evidence is the change label/title, both PRs, their check results,
version.txt/CHANGELOG updates, version tag and GitHub Release notes, with unchanged
deployment target. Depends on PBI-053.1.

PBI-053.3, parent PBI-053: demonstrate the manually triggered release, preserved
baseline and visible result, with a short reproducible walkthrough and explicit
limits. Evidence binds the selected version tag, resolved source, run, archive hash and target, including a required
check failure stopping deployment. Depends on PBI-053.2. The Product Owner approved these children with implementation authorization;
the board now tracks their tested outcomes.

### Testing Strategy

#### Recommended Sprint Parameters

Retain Test: smoke, integration and Regression: smoke. Smoke covers workflow
syntax and trigger separation without Oracle. Integration covers the one live
journey plus one required-check failure before deployment. Full existing smoke
regression remains the plan default; it uses the retained E.1 tool installation,
not the separate 25.4.1 E.3 client. No new unit suite or coverage target is needed.

#### Unit Test Targets

None: no new business logic is planned. Reassess only if implementation grows
nontrivial parsing/decision logic; prefer reducing that logic first.

#### Integration Test Scenarios

IT-1 is the supervised live actor journey with GitHub, the local runner and
Oracle/APEX. Expect the selected version tag's heading on the target, preserved
prior rows/configuration and attributable artifacts; allow roughly 10–20 minutes
for the human journey, an estimate to measure rather than a performance claim.
IT-2 uses an intentionally invalid candidate distribution on the disposable
fixture: native verification must fail before deploy, leaving the target
unchanged. Never introduce a test-only bypass of a real release gate.

#### Smoke Test Candidates

SM-1 runs actionlint, shell syntax checks and checks that PR workflow execution
cannot reach deployment, label/title classification is enforced, versioning
cannot access the lab and deployment has only a manual trigger. It needs only
the implementation source and local validation tools, normally under a minute.
Real remote trigger separation is confirmed during IT-1, not inferred solely
from a text assertion.

## Test Specification

Configuration: managed; Test smoke, integration; Regression smoke. Tests were specified before construction; executed results
are now in [the test record](sprint_E.3_tests.md). Original red skeletons were
registered under the delivery domain and are now implemented.

### SM-1 — Workflow contract

Target: `tests/smoke/test_pipeline.sh:test_SM1_pipeline_contract`.
Pass: valid proposed workflows/scripts, exactly one patch/minor/major label
matching the squash title, hosted release preparation on main pushes, deployment
only on manual dispatch with a version_tag input, no lab credentials in PR or
version-preparation jobs. Exercise missing/conflicting labels and title mismatch
with local metadata fixtures, without creating additional live change journeys. Depends on the
implementation workflows, not on a database. The original skeleton was red; current implementation passes as recorded in tests.

### IT-1 — Reviewed change to manual release

Target: `tests/integration/test_pipeline.sh:test_IT1_manual_release`.
Preconditions: authorized prepared demo repository and runner, qualified E.3
baseline, one fixed lab target and private preservation snapshot. Execute the
actor journey; record the patch label and matching title, squash merge, generated
release PR with patch version and CHANGELOG update, release-PR checks/merge and
automated tag/GitHub Release notes. All leave the target unchanged. Then manually
release the selected tag, changing its heading. Assert both changelog outputs
agree for the version, patch increment, tag/version.txt agreement and binding
between tag, release-PR merge SHA, receipt and archive,
successful runtime SQL/browser observation and retained baseline. The automated
assertion consumes attributable run evidence; a file's existence alone is not
a pass. Human steps and browser checks remain required and separately recorded.

### IT-2 — Required verification failure blocks deployment

Target: `tests/integration/test_pipeline.sh:test_IT2_verification_blocks_deploy`.
Preconditions: disposable invalid candidate with a missing stage include,
unchanged target snapshot and real pinned SQLcl client. Require native verification
failure, no deploy step and unchanged target. Keep the failed exercise separate
from the accepted source candidate. No post-deployment repair is tested.

### Traceability

PBI-053.1 maps to SM-1 and IT-1 capture/source observations; PBI-053.2 maps to
SM-1 and IT-1 PR/no-deploy observations; PBI-053.3 maps to IT-1 and IT-2.
The parent acceptance requires the complete live journey and explicit handover,
not merely passing smoke. Exact runnable commands and staged inputs belong in
the implementation walkthrough after execution; these interfaces are proposed.

## Approved design boundary

The Product Owner approved the small architecture, coordinated Main capture,
PR-check/version-preparation/manual-deployment split,
dedicated private demo repository/local release runner and three child outcomes.
The approval includes ordinary Working Copies and a manual authoring checkpoint for this E.3
prototype while retaining broader SRS protections/automation as unproven work.
No production adoption, complete FR-8/9/10/13 compliance or full toolchain
qualification is implied. Implementation was authorized through technical handover.

## Historical 1.0.1 implementation refinements — superseded

The Product Owner authorized completion without further questions. Native
verification confirmed the slash-containing branch limitation, so the separate
application demo uses explicit slashless e3-initial/e3-heading/e3-runtime-correction
branches. Native verification remains required. The mapping property file is
resolved from the selected checkout, since repository-level utils is not inside
the native artifact. A browser check found the inherited E1_CTRL session hook;
the bounded capture adapter converts that hook to LAB_RUNTIME.assert_ready in
reviewed source before staging. It preserves the retained UAT and original
controller. This correction entered a separate patch PR and accumulated in the
same generated 1.0.1 release PR, demonstrating release batching. No post-stage
source/archive modification or native verification bypass is used. See the
[implementation record](sprint_E.3_implementation.md) and
[test record](sprint_E.3_tests.md) for evidence and limits.

## Product Owner correction — native tools and GitHub control

Accepted by explicit Product Owner instruction on 2026-11-03: remove E.3 Python
code, inherit E.2 native APEX achievements and use GitHub Actions as controller.
This supersedes the recurring source adapter and Python helpers described in
the historical execution section. The assigned PBI and SM-1/IT-1/IT-2 criteria
remain unchanged.

Establish Main's native authoring baseline once through App Builder. Capture
then exports saved source without translation. SQLcl PROJECT owns export,
stage, verify, packaging and deployment. Native APEX availability handles
restriction/publication; inherited LAB_RUNTIME checks business readiness only.
GitHub Actions expresses the sequence as separate steps and blocks subsequent
steps on failure. Shell inside steps handles Git/CLI operations and output
checks; jq validates PR metadata. No standalone release or source controller
remains. Release Please and the approved manual version-tag selection remain.

SQL from accepted main and selected application source use separate checkouts.
Native verification precedes any target write. SQLcl can return success despite
verification errors, so the workflow explicitly requires Errors: 0. Existing
APEX import can restore source availability; reapply restriction after import
and disclose that this is not atomic fencing. Full fencing/recovery remains
deferred under the original scope.

See the [native correction record](sprint_E.3_native_correction.md),
[operator manual](user_manual.md), [E.2 native baseline](../E.2/cicd-walkthrough.md)
and [SQLcl PROJECT reference](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.4/sqcug/project.html).

## Product Owner correction — GitHub configuration ownership

Accepted by explicit instruction on 2026-11-03 after the linked native.env
discussion: no environment-specific settings in .local-apex; scratch is
temporary only. GitHub environment variables/secrets are authoritative.
The setup-native composite action selects Java, installs checksum-pinned SQLcl
on PATH and generates new native connection/mapping files under RUNNER_TEMP.
Job outputs/GITHUB_ENV pass those generated paths; cleanup runs on success and
failure. Runner registration moves to a persistent managed host directory
outside the checkout. No custom environment file is generated or sourced.

The existing IT-2 native rejection check moves into a separately manual
qualification workflow, using the same setup and lab concurrency, with no deploy
command. Parent integration checks fetch attributable GitHub evidence into fresh
OS temporary directories; platform smoke reads GitHub configuration and checks
live ORDS/APEX login. Historical five-schema identity evidence is not re-run
through retired local configuration. Assigned PBI criteria and test case IDs
remain unchanged. The [configuration record](sprint_E.3_github_configuration.md)
and [manual](user_manual.md) own setup details and results.
