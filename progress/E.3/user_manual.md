# E.3 — Native pipeline operator manual

This manual implements the Product Owner's correction: inherit E.2's native
APEX approach, remove E.3 Python, and let GitHub Actions control the pipeline.
See the [walkthrough](sprint_E.3_increment_demo.md),
[design](sprint_E.3_design.md), [tests](sprint_E.3_tests.md) and
[handover](sprint_E.3_handover.md). Earlier 1.0.1 receipts are historical.

## Prepared laboratory

**Fresh-checkout setup gap:** These instructions currently assume a retained lab and private local files. The Product Owner requires generation of every required `.local-apex/` file from a fresh checkout, including `native.env`, tool and connection setup, and runner configuration, using documented commands and the new operator's authorized inputs. [SRS NFR-4](../../docs/srs.md#quality-requirements-and-initial-release) owns this requirement; [PBI-054](../../BACKLOG.md#pbi-054-generate-the-complete-local-environment-from-a-fresh-checkout) tracks delivery, with the gap also exposed in the [project orientation](../../README.md). No complete generator or independent clean-checkout proof is currently provided for this E.3 setup.

Use the existing Oracle/APEX/ORDS lab, Java 21 and SQLcl 25.4.1.022.0618.
DEV Main is E1_DEV_C/810003; the separate target is E3_TARGET/810203. Retained
E1_UAT is not a target. The dedicated runner e3-lab-mac belongs only to the
private [application repository](https://github.com/rstyczynski/APEX_CICD_E3).
Git, gh, jq and shasum are required. Hosted checks use actionlint 1.7.7.

The private file `.local-apex/e3/native.env` exports SQLCL (executable),
SQLCL_HOME (connection store) and JAVA_HOME (Java 21). It contains paths only;
credentials are saved by SQLcl. Load it in an operator terminal:

```bash
source .local-apex/e3/native.env
```

The saved connections are `lab-dev-c` and `e3-target`. If configuring a different
operator's private SQLcl store, start the same client with `/nolog` and use its
native prompt, entering the existing assigned credential when requested:

```sql
connect -save e3-target -savepwd E3_TARGET@//127.0.0.1:1521/FREEPDB1
```

Do not commit the store, passwords, runner registration or business snapshots.
This manual uses retained prepared resources; it does not promise a fresh lab
provisioner. E.3's Python provisioning and runner helpers have been removed.
The existing runner was installed from GitHub's official checksum-verified
2.338.2 distribution. Use GitHub's Settings → Actions → Runners instructions and
its native `config.sh` for a new registration; do not overwrite the retained one.

## Native authoring baseline

The one-time baseline correction was performed through App Builder: application
810003 → Edit Application Definition → Security → Database Session → clear the
E1_CTRL initialization code → Apply Changes. This follows E.2's native APEX
availability approach. Export now captures the actual saved application; nothing
rewrites exported SQL or YAML. LAB_RUNTIME remains an inherited business-schema
readiness check, not a deployment controller or application initialization hook.
The [saved screen](tests/native-author-baseline.png) records the result.

Old Working Copies 100/102 predate that baseline correction. Before later work,
refresh the relevant application definition from Main using native Working Copy
comparison, or create a new Working Copy. Review every native merge; do not merge
an obsolete application definition back into Main. Historical E.2 evidence and
retained UAT remain unchanged; Main's baseline change is explicit.

## Developer capture and PR

In the application repository, create a slashless feature branch. Slash-containing
stage paths remain a known SQLcl comparison limitation. Establish the comparison
branch from the committed pipeline baseline:

```bash
git switch -c e3-next-change
git branch -f e3-base "$(jq -r .baseline_sha pipeline.json)"
"$SQLCL" -nohistory -noupdates -home "$SQLCL_HOME" -S -L /nolog @sql/capture.sql
git diff -- src
```

`capture.sql` connects to lab-dev-c and runs `project export -list` and
`project export`. Inspect the real source diff, then commit it before staging:

```bash
git add src
git commit -m 'fix: describe the reviewed application change'
"$SQLCL" -nohistory -noupdates -home "$SQLCL_HOME" -S -L /nolog @sql/stage.sql
"$SQLCL" -nohistory -noupdates -home "$SQLCL_HOME" -S -L /nolog @sql/verify.sql
git diff -- dist
```

Require **Errors: 0**; SQLcl can report verification failures without a nonzero
process exit, so read the summary. GitHub's workflow checks it explicitly.
Review/commit the generated distribution, push the feature branch, then manually
open its PR. Classify patch with `fix:`, minor with `feat:`, major with `feat!:`;
scopes such as `fix(home):` are accepted. Missing/conflicting labels and mismatched
titles fail the hosted policy. The reviewer inspects the diff/checks, then squash
merges. These sample Git commits are instructions for a real next change, not a
reason to create an empty demonstration change.

## Version and both changelogs

The version workflow runs on main and uses Release Please. Review its generated
release PR, including version.txt and CHANGELOG.md. If the bot PR has no checks,
manually run PR checks with that PR's number:

```bash
gh workflow run pr.yml --repo rstyczynski/APEX_CICD_E3 --ref main -f pr_number=8
```

After a successful run on the latest head, merge the release PR. The version
workflow publishes its tag and GitHub Release notes. PR8 is the performed 1.0.3
release PR; choose the actual current number for a later release. Reviewers retain
control of integration and release-PR merge. Neither operation deploys.

## Manual deployment and runner

In a separate terminal at the parent project root, start the official runner
in the foreground. Stop any earlier foreground runner first with Control-C;
only one listener may use this registration.

```bash
source .local-apex/e3/native.env
cd .local-apex/e3/runner
./run.sh
```

Wait for **Listening for Jobs**. The runner inherits the SQLcl/Java paths and
private connection store. No OS service or Python runner helper is needed.
In GitHub Actions, select **Deploy selected version**, branch **main**, enter the
published tag and Run workflow. The CLI equivalent is:

```bash
gh workflow run release.yml --repo rstyczynski/APEX_CICD_E3 --ref main -f version_tag=v1.0.3
```

Read each visible job step: resolve the published tag; native verification before
writes; native packaging; private baseline; native restriction; native deployment;
reapply restriction and compare data; verify heading/readiness and publish; receipt.
Workflow SQL comes from accepted main; application/configuration comes from the
selected tag. Their identities are distinct. No export from DEV occurs during
release. The immutable tag is attached to a local named branch for SQLcl verify.

The artifact uses the committed target mapping by absolute checkout path because
repository-level utils is outside the native ZIP. Data snapshots stay private in
runner temporary files; uploaded artifacts contain the native ZIP, native logs and
nonsecret receipt. Inspect the application as LAB_USER and its retained history.
The repository version is distinct from the inherited 1.0.0 APEX footer.

## Failure and recovery

A failed verification prevents packaging and target writes. Later failures stop
publication and require inspection of the failed step/native log; do not
automatically reset, repair, retag or overwrite the target. APEX import can restore
source availability, so restriction is reapplied immediately after import. This
is a happy-path demonstration, not atomic maintenance fencing or general DDL
rollback. Browser verification follows the successful workflow; SQL checks alone
do not qualify every application behavior. Use the existing backlog for broader
recovery, concurrency, drift and identity proof.

The native correction initially published 1.0.2. Its workflow passed, but the
browser exposed whitespace left in the initialization field. That version is
historical failed browser evidence. The final 1.0.3 correction clears the field
without inserting editor indentation and adds native APEX_SESSION.CREATE_SESSION
plus DELETE_SESSION before publication. This executes initialization and would
reject that observed failure; it does not replace real authentication/browser
validation. See the [correction record](sprint_E.3_native_correction.md).
