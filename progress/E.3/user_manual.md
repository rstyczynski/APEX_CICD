# E.3 — Native pipeline operator manual

GitHub Actions owns configuration and setup. Native APEX/SQLcl owns authoring,
verification, migration and deployment. There is no Python pipeline, source
adapter, machine environment file or retained private connection-store dependency.
For a complete manual demonstration, start with the
[final walkthrough](sprint_E.3_increment_demo.md#run-it-yourself). It includes
the ordered setup and execution steps; this manual provides reference detail.
See also the
[configuration/evidence](sprint_E.3_github_configuration.md),
[design](sprint_E.3_design.md) and [handover](sprint_E.3_handover.md).

## Configuration ownership

The public [application repository](https://github.com/rstyczynski/APEX_CICD_E3)
is the seed. Every participant, including its owner, follows
the [repository creation procedure](sprint_E.3_increment_demo.md#create-your-own-application-repository-once)
to create their own writable `APEX_CICD_E3_LAB` with full history and tags.
Repeat demonstrations reuse that lab repository. In each terminal, select it:

```bash
e3_repo="$(gh api user --jq .login)/APEX_CICD_E3_LAB"
```

The commands below use this selected repository. Pass it explicitly to the
runner launcher as well.
The walkthrough's [lab setup](sprint_E.3_increment_demo.md#create-your-own-application-repository-once)
creates **e3-lab**, configures its main-only branch policy, sets the variables
and retains existing environment secrets, prompting only for missing ones.
Run that block as part of lab creation. Its nonsecret variables are:

| Variable | Demonstrated laboratory value |
|---|---|
| DB_CONNECT | 127.0.0.1:1521/FREEPDB1 |
| AUTHOR_SCHEMA | E1_DEV_C |
| SOURCE_APP_ID | 810003 |
| TARGET_SCHEMA | E3_TARGET |
| TARGET_WORKSPACE | E3_TARGET |
| TARGET_APP_ID | 810203 |
| TARGET_ALIAS | E3-LAB |
| ORDS_URL | http://127.0.0.1:8080/ords |

Supply **AUTHOR_PASSWORD** and **TARGET_PASSWORD** as environment secrets. Enter
the database schema passwords, not the APEX developer/end-user passwords. Never
commit them. For a different operator/lab, supply that operator's authorized
endpoint and credentials through GitHub; do not copy another operator's files.
The native project still describes the demonstrated E1_DEV_C/810003 source.

The following are reference commands for deliberately updating values after
the scripted setup has created the environment. Run each secret command
interactively and enter its existing authorized password when prompted:

```bash
gh variable set DB_CONNECT --repo "$e3_repo" --env e3-lab --body 127.0.0.1:1521/FREEPDB1
gh variable set AUTHOR_SCHEMA --repo "$e3_repo" --env e3-lab --body E1_DEV_C
gh variable set SOURCE_APP_ID --repo "$e3_repo" --env e3-lab --body 810003
gh variable set TARGET_SCHEMA --repo "$e3_repo" --env e3-lab --body E3_TARGET
gh variable set TARGET_WORKSPACE --repo "$e3_repo" --env e3-lab --body E3_TARGET
gh variable set TARGET_APP_ID --repo "$e3_repo" --env e3-lab --body 810203
gh variable set TARGET_ALIAS --repo "$e3_repo" --env e3-lab --body E3-LAB
gh variable set ORDS_URL --repo "$e3_repo" --env e3-lab --body http://127.0.0.1:8080/ords
gh secret set AUTHOR_PASSWORD --repo "$e3_repo" --env e3-lab
gh secret set TARGET_PASSWORD --repo "$e3_repo" --env e3-lab
```

## Runner infrastructure and workflow setup

The runner must reach the configured Oracle/ORDS endpoints. Loopback addresses
mean the runner shares the lab host. The demonstrated private runner is
**e3-lab-mac**, labels **self-hosted, macOS, ARM64, e3-lab**. The database/APEX/ORDS
lab and schema/workspace/application accounts are infrastructure prerequisites;
this workflow does not provision or reset them. Retained UAT is not the target.

The walkthrough includes [startup of Podman, Oracle Database, APEX and ORDS](sprint_E.3_increment_demo.md#start-podman-oracle-database-apex-and-ords)
before runner setup. It identifies the required software, checks the named VM,
starts the engine and existing containers, waits for database/HTTP readiness
and provides the log commands for failures. It uses the explicit `apex-cicd`
connection. Open [APEX workspace sign-in](http://127.0.0.1:8080/ords/r/apex/workspace-sign-in/oracle-apex-sign-in) and
sign in to E1_DEV_C as DEV_C; the target application is
[810203](http://127.0.0.1:8080/ords/f?p=810203:1).
The walkthrough's [APEX sign-in chapter](sprint_E.3_increment_demo.md#sign-in-to-apex-app-builder)
includes the CLI lookup of the DEV_C Builder password
from the prepared host's existing E.1/E.2 provisioning record. That password is
separate from the schema passwords in GitHub secrets.

The executable [lab launcher](../../scripts/e3-runner.sh) is versioned in the
parent laboratory repository. From that repository root, the lab operator runs:

```bash
./scripts/e3-runner.sh setup --repo "$e3_repo" --directory "$HOME/actions-runner-e3-lab"
./scripts/e3-runner.sh --repo "$e3_repo" --directory "$HOME/actions-runner-e3-lab"
```

Setup installs the official checksum-verified GitHub runner and registers it
using the operator's authenticated gh session with repository administration rights. It retains a matching existing
registration and refuses to overwrite partial/unrelated state. Its default
persistent host directory is `~/actions-runner-e3`, outside the checkout and
scratch. Options `--repo`, `--directory` and `--name` make the declared inputs
explicit; the installer supports this lab's macOS ARM64 host. No environment
file or Python helper is used. A registration token is short-lived and redacted.

The launch command checks registration, reads DB_CONNECT/ORDS_URL from GitHub,
checks local Oracle TCP and ORDS HTTP access, then invokes the official runner.
It clears inherited operator tokens and retired tool/connection variables;
workflows prepare their own configuration. Wait for **Listening for Jobs**.
This foreground lab runner stays open for the lab session; stop it with Control-C.
Use `./scripts/e3-runner.sh status --repo "$e3_repo" --directory "$HOME/actions-runner-e3-lab"` or
`./scripts/e3-runner.sh preflight --repo "$e3_repo" --directory "$HOME/actions-runner-e3-lab"` for read-only checks.
Do not start a second listener while this registration is already online.

The Product Owner explicitly selected a local runnable lab script. No OS service
is installed. Runner startup belongs to lab operation; once it is online, the
deployer only selects a version and dispatches the workflow. GitHub-hosted runners
cannot reach this loopback lab. This local runner runs on the lab Mac and uses
its exposed Oracle/ORDS ports, without needing the APEX installation files.

The checked-in composite GitHub action **setup-native** is shared by release and
qualification workflows. It uses `actions/setup-java` to select Java 21; downloads
SQLcl 25.4.1.022.0618 from Oracle, checks its committed SHA-256 and adds `sqlcl/bin`
to `GITHUB_PATH`. Later steps invoke **sql** directly. It maps GitHub variables
and secrets explicitly, generates private named connections and target mapping
properties under `RUNNER_TEMP`, and returns those generated paths as outputs.
`SQLCL_HOME` in the release job is defined from that output, not inherited from
the host. An always-run cleanup removes the private directory even if setup or
deployment fails. No target properties file is taken from a retained local folder.

`.local-apex/` may hold disposable downloads, build artifacts or diagnostics. It
must never supply environment settings, credentials, named connections or runner
registration. The former E.3 native.env, lab.json and custom launch helper were
removed. Their historical references describe retired implementations only.

## Native authoring and developer PR

Main 810003 uses the native baseline established through App Builder: the old
E1 initialization hook was cleared and native export now omits it. Old Working
Copies 100/102 predate that correction; refresh the application definition from
Main or create a new Working Copy before later work. Review native comparison
and merge the intended page into the coordinated Main checkpoint with a backup.
See the [saved baseline](tests/native-author-baseline.png).

Follow [Prepare Java 21 and SQLcl](sprint_E.3_increment_demo.md#prepare-java-21-and-sqlcl)
to discover an installed SQLcl before downloading it,
and set PATH to its actual location in each developer terminal. Record the build
printed by `sql -version`. The author
uses their own native SQLcl profile outside the checkout. At its prompt, connect and
save the logical author connection, entering the authorized password when asked:

```sql
connect -save lab-dev-c -savepwd -replace E1_DEV_C@//127.0.0.1:1521/FREEPDB1
connect -name lab-dev-c
select user from dual;
```

Require E1_DEV_C from the query. The saved name must be exactly `lab-dev-c`,
without the Git branch/demo suffix, in the same default native connection store
used by capture. Starting the client with `-name lab-dev-c -L` makes a missing
saved profile fail before the SQL script is executed.
Before capture, step D selects an installed SQLcl matching the project's
`.sqlcl.version` value. Native PROJECT rejects a mismatched client even when
its connection succeeds; generic tool discovery alone is not that compatibility
check. The walkthrough reads the required value from project metadata.
This logical alias matches the project's native configuration; the workflow
creates its own separate, temporary alias from GitHub secrets. It does not read
an author's profile. In the application checkout, use a slashless feature branch
because the pinned native comparison has a known slash-path issue:

```bash
git switch -c e3-next-change
git branch -f e3-base "$(jq -r .baseline_sha pipeline.json)"
sql -nohistory -noupdates -S -L -name lab-dev-c @sql/capture.sql
git diff -- src
```

Capture connects to lab-dev-c and runs native PROJECT export. Inspect and commit
the source before native staging; then run:

```bash
sql -nohistory -noupdates -S -L -name lab-dev-c @sql/stage.sql
sql -nohistory -noupdates -S -L -name lab-dev-c @sql/verify.sql
git diff -- dist
```

Require **Errors: 0**; native verification can report errors while returning
process success. Review and commit generated dist, push the feature branch,
then manually open a PR. Exactly one patch/minor/major label must match its
Conventional Commit title: `fix:`, `feat:` or `feat!:`; scoped titles are supported.
Hosted checks have no database credentials. The reviewer checks the diff and
checks, then squash merges. No exported SQL/YAML or packaged archive is rewritten.

## Version and explicit deployment

Release Please prepares version.txt, CHANGELOG.md and its release manifest.
Review its generated release PR. If checks are absent on the bot PR, manually
run PR checks using the release PR number in your own lab repository:

```bash
read -r -p "Current release PR number: " release_pr
gh workflow run pr.yml --repo "$e3_repo" --ref main -f "pr_number=$release_pr"
```

After checks pass on its latest head, merge the release PR. The version workflow
creates its tag and matching GitHub Release notes. None of these events deploys.
The deployer separately chooses a published tag in **Deploy selected version**,
main, Run workflow. Select the tag generated in your lab repository:

```bash
read -r -p "Published tag to deploy: " version_tag
gh workflow run release.yml --repo "$e3_repo" --ref main -f "version_tag=$version_tag"
```

Inspect the ordered job steps: resolve source → explicit tools/connections setup
→ native verify before writes → package one native ZIP → private data snapshot
→ native APEX restriction → PROJECT deployment with generated mapping → restore
restriction and compare fields → native APEX session/heading/readiness validation
and publication → receipt/artifacts → private-material cleanup. Required failure
stops later operations. Accepted-main control SQL and selected-tag application
source use separate checkouts; no live DEV recapture occurs during release.

## Qualification, inspection and failure

A separate manually dispatched **Qualify native verification gate** workflow
exercises the existing IT-2 criterion without deployment:

```bash
gh workflow run qualification.yml --repo "$e3_repo" --ref main -f "version_tag=$version_tag"
```

It uses the same explicit setup, first verifies valid source, snapshots the target,
removes one included native changeset from its temporary checkout, requires
native rejection and confirms the target is unchanged. No deploy command is
called. Its native logs and receipt support the test; private snapshots and
connections are removed afterward. It shares deployment concurrency to avoid
racing the lab demonstration. PR/version workflows remain separate.

The parent repository's smoke/integration checks require gh, Git, jq, Node, curl,
shasum and authenticated API access to the selected repository. They download
fresh attributable workflow evidence into OS temporary directories and remove
it afterward; they need no local database passwords or retained source clone.
Platform smoke reads its endpoint from GitHub and checks the live ORDS/APEX login.
Earlier five-schema identity evidence remains historical E.1 evidence.

Open the configured APEX target as LAB_USER with its existing authorized end-user
credential. Inspect the Home heading and retained greeting history. Password
browser authentication remains a separate observation from native session API
validation. The APEX footer remains 1.0.0, distinct from the Git release version.

Native import may restore source availability; reapplying restriction afterward
is not atomic maintenance fencing. A later failure needs operator inspection,
not automatic reset, retagging, DDL rollback or a fabricated repair claim. Wider
concurrency, drift/identity and independent infrastructure provisioning remain
registered work. [PBI-054](../../BACKLOG.md#pbi-054-generate-the-complete-local-environment-from-a-fresh-checkout)
retains the broader new-operator/clean-lab proof; it does not require a machine
specific environment file or turn scratch into a configuration store.
