# Sprint E.3 technical handover — external review prompt

**Round:** E.3, round 1, outbound expert prompt.

**Revision:** `b695ec9627f1453220a04032563f812242f7ac0f`, the published source
baseline on `main` at review preparation. No uncommitted source patch is
included. A subsequent publication commit adds this prompt and review-navigation
metadata; it does not change the reviewed implementation.

**Reviewer:** Independent external engineering reviewer; identity, model and
tools are not yet known. The Product Owner relays this prompt and returns the
review. No expert has been contacted by the coordinator.

**Scope:** Source/evidence review of the active Sprint E.3 technical handover,
an Elaboration architecture prototype. Coordination checks inspected the sprint
scope, design, implementation, walkthrough, test records and review inventory;
verified public repository/revision metadata and bundle refs/integrity. No fresh
pipeline, database, browser or full-walkthrough execution is claimed for this
review-preparation step. Runtime reproduction and production qualification are
excluded from the reviewer's authorized actions below.

**Inputs:** The pinned parent repository, application source bundle and public
application revision identified below, plus the linked context/evidence inventory.
There are no prior E.3 review findings. E.1/E.2 records are contextual evidence,
not earlier rounds of this E.3 handover review.

**Finding status:** No findings yet. Do not create placeholder findings.

## Copyable expert instruction

You are the independent external reviewer for APEX_CICD, Sprint E.3, handover
review round 1. Review the completed technical prototype and its explanations
critically; do not assume its declared test results establish every claim.

Git repository URL: **https://github.com/rstyczynski/APEX_CICD**.
Branch/ref: **main**. Exact review revision:
**b695ec9627f1453220a04032563f812242f7ac0f**.
The repository is public and `git ls-remote origin refs/heads/main` confirmed
that full SHA before preparing this prompt. Obtain that commit explicitly;
do not substitute whatever `main` points to later. The review subject and
necessary context are committed in that revision, not ignored local files.

The subject is **Sprint E.3 technical handover**. Use filename base
`sprint_E.3_handover` throughout this exchange. The expected returned review is:
**`progress/E.3/sprint_E.3_handover_review-1.md`**.

### Lifecycle objective and decision

E.3 is active in managed mode and remains in **Elaboration**. It demonstrates
one understandable development-to-release happy path: native APEX Working Copy
change, coordinated Main checkpoint, native SQLcl PROJECT capture/stage/verify,
manual developer PR, reviewed semantic squash merge, automated version and both
changelogs, then a deployer's separate manual selection/deployment of a published
tag. The target application visibly changes and prior captured business fields
remain. A separate experiment demonstrates missing-changeset rejection without
deployment. PBI-053 and its sprint children .1/.2/.3 define the bounded outcome.

The review supports a Product Owner handover decision: identify material defects
that invalidate this prototype, its evidence, its runnable explanation or its
safe experiment boundary. Distinguish those from work suitable for Construction
or a later risk-driven Elaboration experiment. Review does not accept/close the
sprint, activate another sprint or authorize production operation.

Use the whole project context as needed. Explain each finding's impact on E.3.
The broad SRS and E.1/E.2 history remain relevant, but apply the explicitly
approved E.3 scope and deferrals rather than treating every future production
requirement as a current prototype blocker. Conversely, a scope label does not
excuse misleading evidence, broken demonstrated commands or an unsafe current
operation.

### Accessible source and reading order

All parent paths below refer to the pinned parent commit above.

1. Read `progress/E.3/sprint_E.3_pipeline_scope.md`, the E.3 entry in `PLAN.md`,
   `BACKLOG.md` PBI-053 and `progress/E.3/sprint_E.3_design.md`, including its
   test specification. Use `progress/E.3/sprint_E.3_analysis.md` for actor and
   requirement reconciliation. Later configuration decisions explicitly
   supersede historical private-repository/local-file/adapter assumptions.
2. Read `progress/E.3/sprint_E.3_increment_demo.md` as the single operator
   starting point, `progress/E.3/sprint_E.3_implementation.md` for the current
   implementation and complete SQL source, `progress/E.3/user_manual.md`,
   `progress/E.3/sprint_E.3_github_configuration.md`, and
   `progress/E.3/sprint_E.3_handover.md`. Inspect the accompanying
   `progress/E.3/sprint_E.3_increment_demo.pptx` and screenshots if supported;
   disclose if you only inspect extracted text or cannot inspect the deck.
3. Inspect `scripts/e3-runner.sh`, `scripts/apex-start.sh`, relevant lab startup
   dependencies and the native implementation in `examples/git-pipeline/`,
   including hidden `.github/` action/workflow/policy files and `sql/*.sql`.
   The complete native application/project/source/distribution is available in
   the tracked `examples/git-pipeline/baseline.bundle`. Its main and v1.0.4 ref
   resolve to **fbda57a0cbe4d32961ad826852bd04394a500c11**. The bundle verifies
   and contains complete history. Inspect that revision for current native
   behavior; older tags preserve superseded code, including Python history.
4. A public alternative for that exact application snapshot is
   **https://github.com/rstyczynski/APEX_CICD_E3**, ref **v1.0.4**, commit
   **fbda57a0cbe4d32961ad826852bd04394a500c11**. GitHub's tag API confirmed its
   commit identity. Do not review unpinned later seed/LAB branches in place of
   this evidence snapshot. The walkthrough's operator-owned LAB repositories
   and later screenshots illustrate repeat use; they do not silently replace
   the recorded reference run's identity.
5. Inspect `progress/E.3/new_tests.manifest`,
   `tests/smoke/test_pipeline.sh`, `tests/integration/test_pipeline.sh`,
   `tests/unit/test_e3_runner.sh`, `progress/E.3/sprint_E.3_tests.md` and the
   evidence inventory below. Distinguish test source coverage, recorded runs
   and assertions about an external system's current state.
6. Use `README.md`, `docs/srs.md` (especially the E.3 scope disposition and
   NFR-4/NFR-5), `docs/architecture.md`, `docs/test-profile.md`,
   `RUP_patch.md`, `RUPStrikesBack.patch/RUP_patch.md` and
   `RUPStrikesBack.patch/USER_PREFERENCES.md` for shared context. Relevant prior
   evidence includes `progress/E.1/sprint_E.1_assessment.md`,
   `progress/E.2/sprint_E.2_assessment.md` and
   `progress/E.2/sprint_E.2_handover.md`. Oracle reference provenance is in
   `refs/apex-lifecycle-management-v3.pdf`; do not assume the lab implements
   every pattern described there.

No separately transmitted credentials, saved connection stores, private runner
files or business snapshots are necessary for this source review. Do not
request them. Required public inputs can be obtained from the pinned parent
checkout and its tracked bundle. If an input or external artifact is inaccessible,
identify it and explain the resulting evidence limitation rather than inventing
a passing result.

### Evidence inventory and applicability

Use the current configuration record to distinguish the final native run from
older v1.0.1 adapter-based and v1.0.2 initialization-failure evidence.

- `progress/E.3/tests/github-environment-journey.json` binds change PR9, release
  PR10, v1.0.4 and application source SHA to deployment **41679427616** and
  qualification **41679432928** in the public seed repository.
- `progress/E.3/tests/github-release-receipt.json` records archive SHA-256
  **d66d6cb7a267e491fc20f6cfd48b62708128a40a4b9e4dc7ecbf60c3dff2cc8b**.
  `github-qualification.json`, `github-native-verify.log` and
  `github-native-rejection.log` record the separate positive/negative check.
- `github-A1-smoke.log`, `github-A3-integration.log`, `github-B1-smoke.log`,
  `github-configuration.json`, `github-runner-checks.json`,
  `github-browser.json` and the associated Home/history images retain the
  reported smoke/integration, configuration, runner and browser observations.
  These are engineering-produced records, not an independent external recheck.
- `progress/E.3/tests/manual-native-rejection.log` records the later manual
  intact/rejected/restored CLI sequence against historical v1.0.4. It does not
  constitute another deployment or a clean-host reproduction.
- `native-sqlcl-version-compatibility.md` records the compatibility experiment.
  `github-public-repository.md` describes public seed/repository creation checks.
  `application-structure-presentation-checks.json` describes the current slide-2
  wording correction and its validation. Earlier presentation receipts apply
  to their recorded file hashes, not automatically to the current PPTX.
- `progress/E.3/sprint_E.3_documentation_audit.md` records later documentation
  corrections. Test-run success does not imply every maintained document is
  consistent; assess that consistency independently.

Recorded results are historical. Live run metadata may be read, but unavailable
or expired downloadable artifacts must be reported as such. Private target
snapshots are not in the review packet; assess public preservation claims
against the code/receipts and state what cannot be independently established.

### Review questions

Assess whether an experienced engineer can understand and follow the declared
supported journey, including prerequisites, GitHub repository/environment setup,
runner lifecycle, SQLcl selection/profile setup, explicit capture scope and
reviewed Main checkpoint. Examine any dependence on retained E.1/E.2 local
credential records against the stated configuration/scratch policy and the
bounded prepared-lab prerequisite. Decide whether limitations are honest and
adequate for E.3, not whether clean-host provisioning is already complete.

Check whether executable workflows/SQL and their displayed explanations agree:
whole configured APEX export versus Git diff, stage comparison, semantic
classification/version creation, bot release-PR checks, tag/source/controller
identity, runtime acceptance versus PROJECT verification, retained-field
comparison and publication. Foundation/Hello/World are project-defined logical
components in one APEX application, not delivered mini apps; mini-app reuse is
proposed work. The lab's custom checks and fixed component-version assumptions
must not be mistaken for native APEX component management or general validation.

Assess error handling and the distinction between a native diagnostic and SQLcl
process success. Check the scope of the deliberate missing-file experiment,
private connection/secret handling, cleanup, tool-version/checksum expectations,
wrong-target guards and preservation evidence. Treat a concrete error affecting
the current lab differently from a correctly disclosed limitation on more
general workspace/schema mappings, fencing, concurrency or DDL recovery.

Evaluate the evidence's provenance, exact revisions and claimed coverage,
including whether tests merely inspect receipts or actually exercise behavior.
Assess source/deployment identity without presuming a qualified immutable
promotion service has been delivered. Wider production hardening, full identity/
drift/fencing/recovery, broad test coverage, independent clean-lab provisioning
and pipeline setup optimization remain follow-up work unless a demonstrated
E.3 claim depends on them. Relevant proposals include PBI-054 and PBI-055.

### Allowed actions and required report

Allowed actions are read-only source/evidence inspection, downloading/reading
public repository inputs and recorded public run metadata, and local checkout
or extraction of the pinned sources into an isolated review directory. Do not
run project test/setup scripts, start/stop runners or containers, connect to the
database, reset/provision any lab, trigger workflows, create/merge PRs, change
GitHub settings, push, contact others or modify project source. Do not request
or disclose credentials or private business data. Local static inspection does
not authorize executing the reviewed application or workflow code.

There are no prior E.3 findings to recheck. Use stable IDs **R1-H1**, **R1-M1**,
**R1-L1**, etc., with severity appropriate to this Elaboration scope. For every
finding, give source path and line/location at the pinned revision, observed
facts, impact on E.3, proposed correction and a concrete acceptance check.
Separate source-inspected risks from reproduced failures, and classify wider
enhancements as conditional follow-up. Be candid, including disagreement with
the engineering claims where evidence warrants it.

Save the complete Markdown as
**`progress/E.3/sprint_E.3_handover_review-1.md`**. Begin with subject and round,
full reviewed revision(s), reviewer identity/model/tool if known, actual scope,
checks/exclusions and inputs. Include a per-finding status table with new
findings `open`, followed by detailed evidence. If there are no findings, state
that explicitly without invented rows. End with a decision-ready recommendation:
ready for this bounded handover, corrections required, or insufficient evidence,
with reasons and explicitly deferred production concerns. State what you did
not inspect/run. Do not claim sprint acceptance or independent runtime validation.

If file writing is unavailable, return the complete Markdown for the Product
Owner to save at that exact path. Do not create an engineering response or
decisions on the team's behalf. The Product Owner returns your original report;
the coordinator will then assess each claim and prepare the engineering reply.
