# E.3 — Git-based pipeline prototype design

## PBI-053 — Simple development-to-release journey

Status: Proposed

Prepared 2026-11-03. [Setup](sprint_E.3_setup.md) and
[analysis](sprint_E.3_analysis.md) explain the contract and actor goals;
[scope](sprint_E.3_pipeline_scope.md) defines the prototype boundary.
[SRS](../../docs/srs.md), [architecture](../../docs/architecture.md) and
[test profile](../../docs/test-profile.md) own shared product guidance.
This design and its child decomposition require Product Owner approval.

### Requirement Summary

Show one Home-heading change from APEX Working Copy to reviewed Git source,
then a separately initiated release to a lab target. Keep it simple enough
to follow live. Git main supplies accepted source; a PR is not a deployment
request. Do not implement the former full E.3/E.4 delivery programme.

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
  V --> M[Reviewer accepts merge to Git main]
  M -. available for release .-> D[Deployer selects commit and runs release]
  D --> R[Local runner: verify and package Git source]
  R --> T[Deploy archive to disposable lab target]
  T --> O[Check heading and retained history]
```

Recommend one small **private GitHub demonstration repository** containing the
native PROJECT application, generated distribution, two workflows and thin
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
`dist/` and `utils/` content; thin `scripts/capture.sh`, `scripts/check.sh`,
`scripts/release.sh`; and `.github/workflows/pr.yml` and `release.yml`.
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

`pr.yml` runs on pull_request targeting main, on a GitHub-hosted runner, with
contents:read, no deployment credentials and no lab access. Check shell syntax,
workflow syntax via actionlint, required native layout/configuration and the
reviewable source/distribution inventory. These checks do not certify Oracle
runtime behavior or replace review. No pull_request_target workflow is needed.
Merging a PR has no automatic release/deploy successor.

`release.yml` runs **only** on workflow_dispatch from Git main. Require a
full accepted `source_sha`; keep the target fixed to the configured disposable
integration role. Validate the SHA syntax and that it is an ancestor of current
remote main, then check it out in an isolated build directory. Reject invocation
from a feature branch. For this supervised prototype the reviewer/deployer
confirms the PR was accepted; do not claim independent attestation or protected
branch enforcement. Pass inputs through environment variables and validate them
before shell use, rather than interpolating workflow expressions into commands.

Use a dedicated local runner label for the release job, contents:read and one
fixed concurrency group with cancel-in-progress:false. Do not send PR jobs to
that runner. The job rechecks the selected commit and pinned tool version,
establishes `e3-base` at the committed baseline SHA and runs
`project verify -cbn e3-base -verbose`. Require zero verification errors, not
just a successful process message. Then `project gen-artifact` creates one ZIP
named from the selected commit and run ID. Do not run export/stage against live
DEV in the release job; do not mutate or commit release source there.

For this prototype, package the reviewed native next distribution. Do not add
`project release` freezing, automatic Git tagging or commit-back orchestration.
If freezing changes the distribution later, the new bytes need new qualification.
Calculate SHA-256 and record source SHA, base SHA, tool version, artifact hash,
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

Keep this design-only: after several accepted PRs, a deployer could approve a
release tag pointing to a selected main commit. That explicit event would invoke
the same release path, require fresh candidate checks and select an allowed
target. A PR label alone is insufficient to identify an integrated release;
workflow_run after every PR check would accidentally couple validation and
deployment. E.3 implements the manual trigger only. Release approval policy,
tag authorization and multi-target promotion remain later work.

### Implementation Approach and child outcomes

PBI-053.1, parent PBI-053: establish the reviewed E.3 baseline, tool/client and
Working Copy-to-Git checkpoint. Evidence is one intentional heading diff plus
consistent native source/distribution verification. No child dependency.

PBI-053.2, parent PBI-053: demonstrate manually opened PR, lightweight checks,
review and accepted integration. Evidence is the PR URL, check result and
accepted commit, with unchanged deployment target. Depends on PBI-053.1.

PBI-053.3, parent PBI-053: demonstrate the manually triggered release, preserved
baseline and visible result, with a short reproducible walkthrough and explicit
limits. Evidence binds source, run, archive hash and target, including a required
check failure stopping deployment. Depends on PBI-053.2. All children and their
board rows remain subject to design/decomposition approval before construction.

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
Oracle/APEX. Expect the selected commit's heading on the target, preserved
prior rows/configuration and attributable artifacts; allow roughly 10–20 minutes
for the human journey, an estimate to measure rather than a performance claim.
IT-2 uses an intentionally invalid candidate distribution on the disposable
fixture: native verification must fail before deploy, leaving the target
unchanged. Never introduce a test-only bypass of a real release gate.

#### Smoke Test Candidates

SM-1 runs actionlint, shell syntax checks and checks that PR workflow execution
cannot reach deployment and release has only a manual trigger. It needs only
the implementation source and local validation tools, normally under a minute.
Real remote trigger separation is confirmed during IT-1, not inferred solely
from a text assertion.

## Test Specification

Configuration: managed; Test smoke, integration; Regression smoke. All tests
and runtime results are pending. Runnable red skeletons are registered under
the delivery domain, not a new per-sprint test domain.

### SM-1 — Workflow contract

Target: `tests/smoke/test_pipeline.sh:test_SM1_pipeline_contract`.
Pass: valid proposed workflows/scripts, only PR checks on pull_request, release
only on manual dispatch, no deployment credentials in PR jobs. Depends on the
implementation workflows, not on a database. Skeleton currently fails explicitly.

### IT-1 — Reviewed change to manual release

Target: `tests/integration/test_pipeline.sh:test_IT1_manual_release`.
Preconditions: authorized prepared demo repository and runner, qualified E.3
baseline, one fixed lab target and private preservation snapshot. Execute the
actor journey; record the PR/update/merge leaving the target unchanged, then
the manual run changing its heading. Assert accepted SHA/receipt/archive binding,
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

## Review decision requested

Approve the small architecture, coordinated Main capture, two-workflow split,
dedicated private demo repository/local release runner and three child outcomes.
Approve ordinary Working Copies and a manual authoring checkpoint for this E.3
prototype while retaining broader SRS protections/automation as unproven work.
No production adoption, complete FR-8/9/10/13 compliance or full toolchain
qualification is implied. Implementation begins only after explicit approval.
