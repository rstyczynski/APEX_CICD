# E.3 — GitHub configuration and local lab runner

The Product Owner directed removal of native.env-style configuration after
[the workflow discussion](codex://threads/01a1a231-79e2-7fe0-bf4c-73152c8364d9).
The subsequent direction is explicit: **use a local runner and provide a runnable
runner script in the laboratory repository**. This record supersedes the
prepared-local-files assumptions in the earlier
[native correction](sprint_E.3_native_correction.md). Native APEX/SQLcl and GitHub
Actions control remain unchanged. The [manual](user_manual.md) owns operating
steps; the [walkthrough](sprint_E.3_increment_demo.md),
[handover](sprint_E.3_handover.md), [design](sprint_E.3_design.md),
[architecture](../../docs/architecture.md), [requirements](../../docs/srs.md)
and [test profile](../../docs/test-profile.md) link this correction.

## Ownership and topology

GitHub stores the workflow configuration in environment **e3-lab**, with eight
nonsecret variables and two encrypted database-password secrets. Only main is
allowed by its environment branch policy. The manual lists every input.
GitHub-hosted jobs validate PRs and prepare versions/changelogs without database
credentials. The manually dispatched release and qualification jobs run on the
local self-hosted e3-lab runner, on the same Mac as the loopback lab endpoints.
SQLcl connects over Oracle TCP; ORDS exposes the APEX browser runtime over HTTP.
No workflow accesses the APEX installation directory.

The checked-in setup-native composite action explicitly selects Java 21 through
actions/setup-java and installs SQLcl 25.4.1.022.0618 from Oracle with a committed
SHA-256. It adds SQLcl to GITHUB_PATH, so commands invoke sql directly. GitHub
variables/secrets generate private native named connections and target mappings
under RUNNER_TEMP. Generated outputs feed later steps through GITHUB_ENV. Always-
run cleanup removes private material on success/failure, including partial setup.
No inherited native.env, SQLCL executable path, saved connection store or committed
target properties file is read. No .local-apex setting is used by current code.

The old E.3 native.env and lab.json and the temporary custom launch helper were
removed. The registered runner was relocated outside the checkout. .local-apex
is reserved for disposable checkouts, caches, build outputs and diagnostics;
it is not a configuration or credential authority. Historical E.1/E.2 evidence
retains its original paths and is not presented as current E.3 setup.

The Product Owner explicitly selected one temporary local exception on
2026-11-04: read the existing E.1/E.2 credential record for interactive logins
on this prepared host only. It must be retained while required, not treated as
disposable or copied elsewhere. Jobs never read it. The
[R1-L1 decision](sprint_E.3_handover_review-1-decisions.md#r1-l1--product-owner-policy-choice-required)
owns the ending/reconsideration trigger; NFR-4 is not declared satisfied.
The inherited VM-start fallback's scratch override is outside the supported
explicit-VM-start path until corrected.

References: [GitHub variables](https://docs.github.com/en/actions/concepts/workflows-and-actions/variables),
[deployment environments](https://docs.github.com/en/actions/concepts/workflows-and-actions/deployment-environments),
[runner temporary paths](https://docs.github.com/en/actions/reference/workflows-and-actions/variables),
[workflow path commands](https://docs.github.com/en/actions/reference/workflow-commands-for-github-actions#adding-a-system-path).

## Local runner as a lab component

The executable [scripts/e3-runner.sh](../../scripts/e3-runner.sh) provides setup,
run, preflight and status. Its setup installs the official 2.338.2 macOS ARM64
runner with SHA-256 verification and uses GitHub's native config.sh. Existing
matching registration is retained; unrelated/partial state is refused. Declared
repo/directory/name options avoid machine environment files. The native runner
registration defaults to ~/actions-runner-e3 and must stay outside the checkout
and scratch. Database secrets never enter the launcher.

The run command reads only nonsecret GitHub configuration, checks Oracle TCP and
ORDS HTTP reachability, clears retired inherited settings/operator tokens, and
executes GitHub's official runner. The lab operator starts it once for the lab
session; the deployer subsequently selects the version in GitHub. Per the Product
Owner's latest instruction this is a foreground local lab runner, not an installed
OS service. A GitHub-hosted runner would not reach localhost; the local runner
shares the lab host's exposed ports. It does not need filesystem access to APEX.

The launcher was syntax checked; help, preflight, existing-registration setup
and actual launch were exercised. Fresh setup on another operator's machine is
not claimed: [PBI-054](../../BACKLOG.md#pbi-054-generate-the-complete-local-environment-from-a-fresh-checkout)
retains the broader independent infrastructure/operator proof. Its wording and
SRS NFR-4 now require reproducible supported setup, not recreation of native.env.

## Verification scope

The existing SM-1/IT-1/IT-2 IDs remain. A separately manual qualification workflow
uses the same native setup, verifies valid source first, removes an included
changeset in a temporary checkout, requires native rejection and compares private
target snapshots. It contains no deployment command. It shares lab concurrency
with release. Parent integration checks query live GitHub PR/tag/run/release state,
for the fixed seed v1.0.4 journey (deployment 41679427616 and qualification
41679432928), download existing artifacts into new temporary directories and
verify hashes, changelogs, native result and cleanup. They do not create fresh
native runs or validate an operator's selected LAB. They need no local database
settings; platform smoke separately needs permission to read the seed environment
variables and probes that configured HTTP endpoint. Public source access does
not grant environment API access. See the current test profile for exact scope.

Platform smoke now obtains its endpoint/application from GitHub and checks live
ORDS plus the database-backed APEX login. The historical five-schema identity
proof is not re-executed through retired .local-apex configuration. This change
is explicit; a current login check is not represented as every historical
privilege/identity assertion.

The first explicit-setup trials, release 41677666720 and qualification 41677672274,
both succeeded with source v1.0.4. The repository launcher then started the local runner and executed the final
[deployment 41679427616](https://github.com/rstyczynski/APEX_CICD_E3/actions/runs/41679427616)
and [qualification 41679432928](https://github.com/rstyczynski/APEX_CICD_E3/actions/runs/41679432928),
both successfully. The [journey record](tests/github-environment-journey.json)
binds those runs to PR9, release PR10 and tag/source
fbda57a0cbe4d32961ad826852bd04394a500c11. The
[release receipt](tests/github-release-receipt.json) binds its native ZIP hash
 d66d6cb7a267e491fc20f6cfd48b62708128a40a4b9e4dc7ecbf60c3dff2cc8b.
The [qualification receipt](tests/github-qualification.json),
[positive verify](tests/github-native-verify.log) and
[rejection log](tests/github-native-rejection.log) prove the valid-source check,
expected missing-file failure and unchanged target. Both workflows' cleanup
steps passed. [Configuration metadata](tests/github-configuration.json) confirms
eight variables, two secret names, main-only branch policy and removal of the
retired E.3 configuration files; it contains no secret values.

Fresh gates passed: [A1 smoke](tests/github-A1-smoke.log) 1/1,
[A3 integration](tests/github-A3-integration.log) 2/2 and
[B1 full smoke](tests/github-B1-smoke.log) 2/2. The first new HTTP probe followed
redirects without retaining cookies and hit the redirect limit; its
[initial log](tests/github-B1-smoke-initial.log) is retained. An ephemeral cookie
jar fixed the test's session handling; the actual APEX login criterion remains.
No failure was waived. Unit/broader regression was not selected.

A fresh browser session authenticated as LAB_USER and showed the expected Home
heading and retained Hello World history row. [Observation](tests/github-browser.json),
[Home](tests/github-deployed-home.png) and [history](tests/github-deployed-history.png)
record it. The [regenerated bundle](tests/github-bundle.json) preserves accepted
main/tags through 1.0.4 with no moved tags. Broader saved-user-state or identity
preservation is not inferred from the retained row/business-field checks.

## Limits

This correction removes hidden workflow configuration; it does not provision all
Oracle/APEX/ORDS infrastructure or establish production operation. The lab must
be running and reachable from its local runner. APEX import/availability remains
non-atomic, complete drift/identity/fencing and general DDL recovery remain deferred,
and the inherited APEX display footer still says 1.0.0. Source tags and receipts
identify the pipeline release. Product Owner acceptance and sprint closure are
separate; no next sprint or broader PBI completion is inferred.

The [launcher check receipt](tests/github-runner-checks.json) records the exact
script hash and exercised commands. The [presentation check](tests/github-presentation-checks.json)
records the final 12-slide deck and passed package/layout/import checks. The
[document check](tests/github-document-checks.json) records source/link agreement.
