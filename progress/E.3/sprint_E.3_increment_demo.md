# E.3 — Native Git pipeline walkthrough

**Start here to run the E.3 demonstration manually.** Follow steps A–G below
in order, using the [editable deck](sprint_E.3_increment_demo.pptx) alongside them.
The commands, setup and expected results are included here. The
[operator manual](user_manual.md) is a reference for additional detail, not a
second starting point. Chapter H separately demonstrates rejection of incomplete
source; it is an architecture experiment rather than deployment verification.
The recorded run after chapter H is historical evidence.

APEX/SQLcl provide native capabilities; GitHub Actions controls execution.
The [current implementation record](sprint_E.3_implementation.md#current-native-implementation--2026-11-04)
explains the implemented mechanisms and complete SQL source by backlog outcome;
this walkthrough presents them in operator execution order.

## Application structure and terminology

Foundation, Hello and World are **project-defined logical components within one
APEX application**. In APEX, Hello and World are separate sets of pages for
entries, editing and configuration, backed by their tables and logic. Foundation
provides shared PL/SQL, greeting history and component version/readiness records.
These project groupings are not native APEX entities or independent deployment
units. Native APEX pages, regions and Shared Components remain the actual
application definitions.

Main **810003** and target **810203** are development and deployment copies of
the same assembled application. Capture exports the configured application and
included schema definitions; Git identifies the files changed by your edit.
The E.3 workflow packages and deploys the assembled application rather than
releasing Hello and World as separate applications. This is the structure shown
on **slide 4** and detailed in the
[implementation record](sprint_E.3_implementation.md#current-native-implementation--2026-11-04).

**Oracle mini-app best-practice note.** For larger solutions, Oracle's lifecycle
guidance describes modularizing into multiple smaller APEX applications, with
common/library components reused through subscriptions and shared authentication
for seamless navigation. Separate database schemas are optional. The paper
explicitly says smaller solutions do not require this split. Our three logical
components are therefore not three mini apps. See the
[Oracle APEX lifecycle paper, version 3.2, pages 7 and 15–16](https://www.oracle.com/a/tech/docs/apex-lifecycle-management-v3.pdf#page=15).
The separate mini-app reuse scenario remains proposed in
[PBI-044](../../BACKLOG.md#pbi-044-demonstrate-native-mini-app-component-reuse);
it is not delivered by this walkthrough.

## Table of contents

- [Application structure and terminology](#application-structure-and-terminology)
- [Run it yourself](#run-it-yourself)
  - [A. Check access and prepare the two checkouts](#a-check-access-and-prepare-the-two-checkouts--slides-14)
  - [B. Confirm GitHub settings and start the local runner](#b-confirm-github-settings-and-start-the-local-runner--slide-4)
  - [C. Make a fresh native APEX change](#c-make-a-fresh-native-apex-change--slides-56)
  - [D. Capture, commit and stage using native SQLcl](#d-capture-commit-and-stage-using-native-sqlcl--slide-7)
  - [E. Open the PR, review and let the workflow version it](#e-open-the-pr-review-and-let-the-workflow-version-it--slides-89)
  - [F. Manually deploy the published tag](#f-manually-deploy-the-published-tag--slide-10)
  - [G. Verify the deployed application in the browser](#g-verify-the-deployed-application-in-the-browser--slides-1112)
  - [H. Demonstrate rejection of incomplete source](#h-demonstrate-rejection-of-incomplete-source)
- [Recorded run and supporting evidence](#recorded-run-and-supporting-evidence)
  - [Goal and inherited foundation](#goal-and-inherited-foundation)
  - [1. Working Copy and Main checkpoint](#1-working-copy-and-main-checkpoint)
  - [2. Native capture, review, staging and verification](#2-native-capture-review-staging-and-verification)
  - [3. Manual PR and automated release preparation](#3-manual-pr-and-automated-release-preparation)
  - [4. GitHub configuration and explicit setup](#4-github-configuration-and-explicit-setup)
  - [5. Deployer selects the version](#5-deployer-selects-the-version)
  - [6. Application and rejection evidence](#6-application-and-rejection-evidence)
- [Slide map and handover boundary](#slide-map-and-handover-boundary)

## Run it yourself

### A. Check access and prepare the two checkouts — slides 1–6

This demonstration uses the **existing E.2/E.3 lab**, not a newly provisioned
database. Use its macOS ARM64 host. The startup sequence below brings Oracle up
at `127.0.0.1:1521/FREEPDB1` and ORDS at `http://127.0.0.1:8080/ords`.
You need the existing APEX developer credential for Main 810003 in E1_DEV_C,
the E1_DEV_C and E3_TARGET database passwords, and LAB_USER's target application
password. These are different credentials. The target is E3_TARGET / 810203;
retained UAT is not used.

**Temporary credential accommodation approved on 2026-11-04:** on this already
prepared E.2/E.3 host, the existing `.local-apex/e1-secrets.json` record remains
the read-only source for the three interactive password lookups below. It is
a retained dependency until replaced, not disposable scratch. Do not create new
settings there, copy the record to another host, move/delete it or use it in
GitHub jobs. Jobs use GitHub environment secrets; author profiles live outside
the checkout. The exception ends when a compliant source remedy is selected and
must be reconsidered before new-host reproduction, scratch cleanup or expansion.
It is an explicit [R1-L1 deferral](sprint_E.3_handover_review-1-decisions.md#r1-l1--product-owner-policy-choice-required),
not a claim that NFR-4 is satisfied. Another host needs its own assigned credentials.

Install Podman, Git, GitHub CLI (`gh`), jq, curl, nc, tar, unzip and shasum on this host.
For developer capture, Java 21 and SQLcl **25.4.1.022.0618** must also be on
your ordinary PATH. Release jobs install their own Java/SQLcl. Authenticate
`gh` with your GitHub account. The public source is readable by everyone;
creating your own repository and configuring its runner requires your own
repository administration permission.

The software runs in these locations; starting the GitHub runner does not start
the database or web server:

| Location | Required software / resource | Purpose |
|---|---|---|
| macOS host | Podman CLI (demonstrated: 6.0.0) | Starts the Linux VM and its containers |
| macOS host | Git, gh, jq, curl, nc, tar, unzip, shasum | Repository setup, connectivity and runner setup |
| macOS author terminal | Java 21 and SQLcl 25.4.1.022.0618 | Native PROJECT capture, staging and verification |
| Podman VM `apex-cicd` | Prepared Linux container engine; demonstrated sizing: 4 CPUs, 6 GiB RAM, 30 GiB disk | Hosts the two containers |
| Container `apex-db` | Oracle Database Free 23.26.3, with APEX 24.2 installed in FREEPDB1 | Database, APEX definitions and existing lab data |
| Container `apex-ords` | ORDS 25.3 and APEX static assets | Serves App Builder and application HTTP URLs |

If Podman is missing, install the macOS package from the
[official Podman installer](https://podman.io/docs/installation), then reopen
Terminal and check `podman --version`. The CLI is sufficient; Podman Desktop
does not have to be open. Oracle Database, APEX and ORDS are already installed
inside the prepared lab; they do not need separate macOS installations.
Image versions/digests are retained in [apex-images.env](../../scripts/apex-images.env).

#### Prepare Java 21 and SQLcl

Run this setup before the first `sql` command. GitHub's workflow tool setup
applies to its jobs; your developer terminal needs its own installation.
The discovery block below can reuse the earlier sprint's Java 21 as well.
If Java 21 is missing, install it with [Homebrew](https://brew.sh/):

```bash
brew install openjdk@21
```

Select Java 21 in this terminal, then **discover the installed SQLcl**.
The Java selection also checks for the earlier sprint's downloaded JDK if the
Homebrew location is absent.
Discovery first uses `sql` if it is already on PATH. Otherwise it searches your
earlier lab tool cache, Applications, Downloads and tools for a SQLcl executable, adds its
actual directory to PATH and prints the installed version:

```bash
echo "Selecting Java 21..."
export JAVA_HOME="$(brew --prefix openjdk@21)/libexec/openjdk.jdk/Contents/Home"
if [ ! -x "$JAVA_HOME/bin/java" ]; then
  e3_java=$(find "$HOME/projects/APEX_CICD/.local-apex/tools" "$HOME/Applications" "$HOME/tools" -type f -path '*/jdk-21*/Contents/Home/bin/java' -print -quit 2>/dev/null)
  if [ -n "$e3_java" ]; then export JAVA_HOME="${e3_java%/bin/java}"; fi
fi
e3_sqlcl=$(command -v sql || true)
if [ -z "$e3_sqlcl" ]; then
  e3_sqlcl=$(find "$HOME/projects/APEX_CICD/.local-apex/tools" "$HOME/Applications" "$HOME/Downloads" "$HOME/tools" -type f -path '*/sqlcl*/bin/sql' -print -quit 2>/dev/null)
fi
if [ -n "$e3_sqlcl" ] && [ -x "$e3_sqlcl" ]; then
  export PATH="$(dirname "$e3_sqlcl"):$PATH"
  hash -r
  command -v sql
  sql -version
else
  echo 'SQLcl was not found. Install SQLcl before continuing.' >&2
fi
```

If SQLcl is found, **skip installation**. The earlier sprint's tool cache can
supply the executable. Discovery reads tool binaries and creates no settings or
credentials. Record the version printed by `sql -version`; discovery does not
filter by a fixed version string.

**Only if discovery finds no SQLcl installation**, install the same pinned
SQLcl version used by the workflows. This block downloads
the Oracle archive, checks its SHA-256 and extracts it under your Applications
directory. Run it once; repeat it if that tool directory has been removed:

```bash
(
set -euo pipefail
mkdir -p "$HOME/Downloads" "$HOME/Applications/apex-cicd/sqlcl-25.4.1.022.0618"
curl --fail --location --retry 3 https://download.oracle.com/otn_software/java/sqldeveloper/sqlcl-25.4.1.022.0618.zip -o "$HOME/Downloads/sqlcl-25.4.1.022.0618.zip"
printf '%s  %s\n' b717d83aa1a7ada2ca38e7c8be5b369ea6a2f9f50c5fdb55e18d263b471ecab9 "$HOME/Downloads/sqlcl-25.4.1.022.0618.zip" | shasum -a 256 -c -
unzip -q -o "$HOME/Downloads/sqlcl-25.4.1.022.0618.zip" -d "$HOME/Applications/apex-cicd/sqlcl-25.4.1.022.0618"
chmod +x "$HOME/Applications/apex-cicd/sqlcl-25.4.1.022.0618/sqlcl/bin/sql"
)
```

After installation, rerun the discovery block above. In **each new authoring
terminal**, select Java 21 and run discovery again. Expect `command -v sql` to
show the **discovered path**, and `sql -version` to report its actual build. PATH changes
affect that terminal only. A `command not found` error requires discovery or
installation, rather than exporting an assumed directory.
See [Oracle's SQLcl environment requirements](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.4/sqcug/preparing-your-environment.html).

Start in your home directory; no checkout is required yet. Check the installed
tools and GitHub access:

```bash
cd ~
gh auth status
git --version
jq --version
sql -version
gh repo view rstyczynski/APEX_CICD
gh repo view rstyczynski/APEX_CICD_E3
```

On the first run, create a working directory and clone the parent repository
and public seed as siblings. Name the seed's local checkout `APEX_CICD_E3_LAB`
to distinguish your working lab from the shared seed:

```bash
mkdir -p "$HOME/projects"
cd "$HOME/projects"
gh repo clone rstyczynski/APEX_CICD APEX_CICD
gh repo clone rstyczynski/APEX_CICD_E3 APEX_CICD_E3_LAB
```

The **parent lab checkout**, `~/projects/APEX_CICD`, contains this walkthrough
and `scripts/e3-runner.sh`. The **application checkout**,
`~/projects/APEX_CICD_E3_LAB`, contains the source, native project and workflows.
Everyone, including the seed owner, uses their own
`<operator>/APEX_CICD_E3_LAB` GitHub repository for this walkthrough. The public
`rstyczynski/APEX_CICD_E3` repository supplies the seed only. Cloning downloads
its history to your computer; the creation step below makes your writable
GitHub repository and changes this checkout's origin to it.

On later runs, skip both cloning and repository creation. Reuse your existing
lab checkout/repository, whose origin already points to your own lab. If the
local checkout is missing but your lab repository already exists, clone
`<operator>/APEX_CICD_E3_LAB` instead of cloning the seed again.

If a checkout already exists, reuse it only after reviewing/committing any local
work; do not clone over it. Open the **parent lab terminal** and prepare it:

```bash
cd "$HOME/projects/APEX_CICD"
git status --short
git switch main
git pull --ff-only
```

#### Start Podman, Oracle Database, APEX and ORDS

Run this sequence at the beginning of each lab session, from the parent checkout.
Already running resources are retained. The order is **VM → database/APEX →
ORDS → browser → GitHub runner**.

**1. Check the prepared machine and its connection.**

```bash
podman --version
podman machine list
podman system connection list
```

Expect a machine and connection named **apex-cicd**. On macOS, Podman containers
run inside this Linux VM. Use the explicit connection below even if another
connection is marked as default. If `apex-cicd` is absent, stop: this is not the
prepared earlier-sprint host. Creating an empty VM would not restore its database,
APEX applications or data. This session-start sequence reuses that prepared lab.

**2. Start the VM if it is stopped, then check the engine.**

```bash
if ! podman --connection apex-cicd info > /dev/null 2>&1; then
  podman machine start apex-cicd
fi
podman --connection apex-cicd info
podman --connection apex-cicd ps -a --format '{{.Names}}\t{{.Status}}\t{{.Ports}}'
```

Expect engine information and containers **apex-db** and **apex-ords**, which may
still be stopped. If startup reports another VM already running, inspect
`podman machine list` and finish that VM's work before stopping it; do not remove
it. See [Podman's machine-start reference](https://docs.podman.io/en/stable/markdown/podman-machine-start.1.html).
Stop on engine errors or missing lab containers before proceeding.

**3. Start the database/APEX, wait for readiness, then start ORDS.**

##### Script introduction: `apex-start.sh`

This script addresses the named Podman connection `apex-cicd` explicitly,
avoiding whichever unrelated VM is the host default. It starts `apex-db` and
polls the image's `healthcheck.sh` before starting `apex-ords`, then polls the
ORDS HTTP endpoint. Database and HTTP readiness have separate bounded waits;
either timeout stops the script. It starts retained containers rather than
recreating their data. If the engine is unavailable, it delegates VM startup
to `apex-vm-start.sh`, whose macOS `launchd` launch keeps the VM independent of
the invoking terminal. The preceding VM check should already have established
engine access for this walkthrough.

The inherited fallback reads a retained `.local-apex/containers.conf` override
without generating it. It is outside this walkthrough's supported startup path:
complete the explicit VM-start/check step above first. Stop on failure rather
than relying on that fallback or treating its configuration as optional scratch.

Run the startup script:

```bash
bash scripts/apex-start.sh
```

It runs `podman --connection apex-cicd start apex-db`, waits for
`podman --connection apex-cicd exec apex-db healthcheck.sh` to succeed, starts
`apex-ords`, then waits for the ORDS HTTP endpoint. APEX runs inside Oracle
Database; there is no separate APEX container or APEX start command. Expect:

```text
APEX available at http://127.0.0.1:8080/ords/
```

**4. Check both containers and the browser endpoint before continuing.**

```bash
podman --connection apex-cicd ps --format '{{.Names}}\t{{.Status}}\t{{.Ports}}'
podman --connection apex-cicd exec apex-db healthcheck.sh
nc -z -w 3 127.0.0.1 1521
curl --fail --silent --show-error --location --output /dev/null --write-out 'APEX HTTP %{http_code}\n' http://127.0.0.1:8080/ords/
```

Expect both containers **Up**, database port **127.0.0.1:1521**, ORDS port
**127.0.0.1:8080**, successful database/TCP checks and **APEX HTTP 200** after
redirects. If startup or readiness fails, inspect the relevant logs and resolve
the error before starting the GitHub runner:

```bash
podman --connection apex-cicd logs --tail 80 apex-db
podman --connection apex-cicd logs --tail 80 apex-ords
```

Starting the prepared containers retains schemas, applications and history.
Do not run the earlier sprint's destroy/reinstall commands for an E.3 replay.

When all four checks pass, continue to [Sign in to APEX App Builder](#sign-in-to-apex-app-builder).

#### Sign in to APEX App Builder

Open [APEX workspace sign-in](http://127.0.0.1:8080/ords/r/apex/workspace-sign-in/oracle-apex-sign-in).
This direct URL opens the login form. The shorter `/ords/` URL opens the ORDS
landing page; its **Oracle APEX → Go** button leads to the same form.

| Sign-in field | Value |
|---|---|
| Workspace | E1_DEV_C |
| Username | DEV_C |
| Password | DEV_C Builder password from the prepared lab's provisioning record |

Retrieve **only the DEV_C Builder password** in the parent lab terminal:

```bash
jq -er '.DEV_C | select(type == "string" and length > 0)' "$HOME/projects/APEX_CICD/.local-apex/e1-secrets.json"
```

This reads the existing E.1/E.2 provisioning record on the prepared host. It
does not create or modify it. Treat it as a legacy credential lookup for this
retained lab; E.3 configuration continues to live in GitHub. A different host
needs its own assigned Builder credential from its lab provisioning.
The value is printed in your terminal for entry in the login form; keep it out
of screenshots and Git. It differs from the E1_DEV_C database password used by
GitHub workflows. After signing in, choose **App Builder**.

![APEX workspace sign-in with workspace E1_DEV_C and username DEV_C](tests/walkthrough/00-builder-sign-in.jpg)

**Checkpoint:** the APEX workspace home shows **DEV_C / E1_DEV_C** and provides
the **App Builder** link. Continue to the application terminal setup below.

#### Prepare the application terminal

Open a second, **application terminal**, and prepare that checkout:

```bash
cd "$HOME/projects/APEX_CICD_E3_LAB"
git status --short
git switch main
git pull --ff-only
```

#### Create your own application repository once

Run the following setup from the prepared application checkout in an interactive
Bash terminal. It creates your public lab repository, publishes the seed history
and tags, configures Actions and labels, imports the seed release, and sets up
`e3-lab` with its main-only rule and eight variables. Existing environment secrets
are retained. For each missing secret, enter the existing **E1_DEV_C** or
**E3_TARGET database password** when prompted. These credentials belong to the
local Oracle schemas; they are not GitHub account passwords. GitHub does not
allow stored secret values to be read back or copied from the public seed.
See [GitHub's secrets API](https://docs.github.com/en/rest/actions/secrets).

The setup retains an existing repository, release and main branch rule, so it
can complete an interrupted run. Git pushes are ordinary fast-forward pushes.
On later demonstrations, reuse the configured lab and skip this setup.

Keep the complete seed history: `pipeline.json` refers to an earlier commit
needed by native PROJECT comparison. The existing Oracle/APEX/ORDS lab remains
a prerequisite.

```bash
(
set -euo pipefail
cd "$HOME/projects/APEX_CICD_E3_LAB"
e3_repo="$(gh api user --jq .login)/APEX_CICD_E3_LAB"

if ! gh repo view "$e3_repo" > /dev/null 2>&1; then
  gh repo create "$e3_repo" --public --description "Native APEX E.3 Git pipeline lab"
fi
gh api --method PUT "repos/$e3_repo/actions/permissions/workflow" -f default_workflow_permissions=read -F can_approve_pull_request_reviews=true
gh api --method PUT "repos/$e3_repo/actions/permissions/fork-pr-contributor-approval" -f approval_policy=all_external_contributors
git remote set-url origin "https://github.com/$e3_repo.git"
git push -u origin main
git push origin --tags
gh repo edit "$e3_repo" --default-branch main --enable-squash-merge --squash-merge-commit-message pr-title
gh label create patch --repo "$e3_repo" --color 0E8A16 --description "Patch release" --force
gh label create minor --repo "$e3_repo" --color 1D76DB --description "Minor release" --force
gh label create major --repo "$e3_repo" --color B60205 --description "Major release" --force

gh api --method PUT "repos/$e3_repo/environments/e3-lab" --input - <<'JSON'
{"deployment_branch_policy":{"protected_branches":false,"custom_branch_policies":true}}
JSON

branch_rules=$(gh api "repos/$e3_repo/environments/e3-lab/deployment-branch-policies")
if ! jq -e 'any(.branch_policies[]; .name == "main" and .type == "branch")' <<< "$branch_rules" > /dev/null; then
  gh api --method POST "repos/$e3_repo/environments/e3-lab/deployment-branch-policies" -f name=main -f type=branch
fi

gh variable set DB_CONNECT --repo "$e3_repo" --env e3-lab --body 127.0.0.1:1521/FREEPDB1
gh variable set AUTHOR_SCHEMA --repo "$e3_repo" --env e3-lab --body E1_DEV_C
gh variable set SOURCE_APP_ID --repo "$e3_repo" --env e3-lab --body 810003
gh variable set TARGET_SCHEMA --repo "$e3_repo" --env e3-lab --body E3_TARGET
gh variable set TARGET_WORKSPACE --repo "$e3_repo" --env e3-lab --body E3_TARGET
gh variable set TARGET_APP_ID --repo "$e3_repo" --env e3-lab --body 810203
gh variable set TARGET_ALIAS --repo "$e3_repo" --env e3-lab --body E3-LAB
gh variable set ORDS_URL --repo "$e3_repo" --env e3-lab --body http://127.0.0.1:8080/ords
configured_secrets=$(gh secret list --repo "$e3_repo" --env e3-lab --json name)
if ! jq -e 'any(.[]; .name == "AUTHOR_PASSWORD")' <<< "$configured_secrets" > /dev/null; then
  printf '%s\n' 'Enter the existing E1_DEV_C database password:'
  gh secret set AUTHOR_PASSWORD --repo "$e3_repo" --env e3-lab
fi
if ! jq -e 'any(.[]; .name == "TARGET_PASSWORD")' <<< "$configured_secrets" > /dev/null; then
  printf '%s\n' 'Enter the existing E3_TARGET database password:'
  gh secret set TARGET_PASSWORD --repo "$e3_repo" --env e3-lab
fi

seed_tag="v$(cat version.txt)"
if ! gh release view "$seed_tag" --repo "$e3_repo" > /dev/null 2>&1; then
  seed_notes=$(mktemp)
  gh release view "$seed_tag" --repo rstyczynski/APEX_CICD_E3 --json body --jq .body > "$seed_notes"
  gh release create "$seed_tag" --repo "$e3_repo" --verify-tag --title "$seed_tag" --notes-file "$seed_notes"
  rm -f "$seed_notes"
fi
)
```

Expect the repository, its release and the `e3-lab` environment to be present
when setup finishes. Subsequent version bumps are generated by the workflow.
Step B checks the configuration before runner startup.

#### Select the repository for this session

In **each terminal**, select your own lab repository:

```bash
e3_repo="$(gh api user --jq .login)/APEX_CICD_E3_LAB"
gh repo view "$e3_repo"
```

For the seed owner this resolves to `rstyczynski/APEX_CICD_E3_LAB`, following
the same procedure as every other participant. This shell variable is a
nonsecret command input for this terminal session; it is not a machine
configuration file.

**Checkpoint:** your selected repository is writable, its main and tags are
present, the baseline commit resolves, SQLcl reports the pinned version, and the
application checkout is clean and current:

```bash
git cat-file -t "$(jq -r .baseline_sha pipeline.json)"
git remote -v
git status --short
```

Expect `commit`, the selected origin URL, and no uncommitted changes.

### B. Confirm GitHub settings and start the local runner — slide 6

The creation script above has already configured **your lab repository's**
`e3-lab` environment. Verify it from the terminal before starting the runner:

```bash
gh api "repos/$e3_repo/environments/e3-lab" --jq .deployment_branch_policy
gh api "repos/$e3_repo/environments/e3-lab/deployment-branch-policies" | jq -e '.total_count == 1 and .branch_policies[0].name == "main" and .branch_policies[0].type == "branch"'
gh variable list --repo "$e3_repo" --env e3-lab
gh secret list --repo "$e3_repo" --env e3-lab
```

Expect custom branch policies enabled, the sole rule `main` / `branch`, the
following eight variables, and both secret names. Secret values are never read
back. The Settings → Environments UI is an optional inspection view; no manual
UI configuration is required.

| Variable | Lab value |
|---|---|
| DB_CONNECT | 127.0.0.1:1521/FREEPDB1 |
| AUTHOR_SCHEMA | E1_DEV_C |
| SOURCE_APP_ID | 810003 |
| TARGET_SCHEMA | E3_TARGET |
| TARGET_WORKSPACE | E3_TARGET |
| TARGET_APP_ID | 810203 |
| TARGET_ALIAS | E3-LAB |
| ORDS_URL | http://127.0.0.1:8080/ords |

Environment secrets **AUTHOR_PASSWORD** and **TARGET_PASSWORD** hold the
respective database schema passwords. If configuration is missing, return to
the lab setup above before starting the runner. No environment
settings or credentials belong in `.local-apex`.

That rule governs workflow configuration. The explicitly approved prepared-host
interactive credential accommodation in step A is the narrow temporary exception.

#### Script introduction: runner setup and status

`e3-runner.sh setup` validates the selected repository and persistent runner
directory. For a new installation it downloads the pinned official macOS ARM64
runner, verifies its SHA-256 and obtains a short-lived GitHub registration token
through `gh`; the token registers the runner with label `e3-lab`. A matching
existing registration is retained, while a mismatched registration is rejected.
Its preflight reads `DB_CONNECT` and `ORDS_URL` from the selected GitHub
environment and checks TCP/HTTP access; it does not authenticate to Oracle.
`status` checks that registration and queries GitHub for matching runners'
online/offline and busy state. Neither command starts a listener.

In the **parent lab terminal**:

```bash
cd "$HOME/projects/APEX_CICD"
./scripts/e3-runner.sh setup --repo "$e3_repo" --directory "$HOME/actions-runner-e3-lab"
./scripts/e3-runner.sh status --repo "$e3_repo" --directory "$HOME/actions-runner-e3-lab"
```

Setup retains a matching registration or installs/registers the official runner
in `~/actions-runner-e3-lab`, selected explicitly by these commands so an older
seed runner in `~/actions-runner-e3` can be retained. Use the same directory on
setup, status and run; the launcher refuses to replace an unrelated registration. Expect
**Setup complete** and successful Oracle TCP /
ORDS HTTP checks. If status already reports this runner online, use that listener.
Otherwise start it in this terminal:

#### Script introduction: foreground runner listener

With no subcommand, `e3-runner.sh` selects `run`. It validates the same
registration and connectivity, removes inherited GitHub tokens and retired
tool/connection overrides from the child environment, then replaces itself
with the installed runner's `run.sh`. That listener receives GitHub jobs; the
job's workflow supplies its own tools and environment secrets. Control-C stops
the listener while preserving registration for the next session.

```bash
./scripts/e3-runner.sh --repo "$e3_repo" --directory "$HOME/actions-runner-e3-lab"
```

Wait for **Listening for Jobs** and leave the terminal open. Use a second
terminal for the remaining commands. Stop here if prerequisites fail; runner
setup does not provision Oracle/APEX/ORDS. The runner uses their network ports;
GitHub workflows prepare job-private tools/connections and clean them afterward.

### C. Make a fresh native APEX change — slides 8–9

In the signed-in Builder session, choose
**App Builder → APEX Delivery Laboratory (810003)**. If your session has expired,
follow [Sign in to APEX App Builder](#sign-in-to-apex-app-builder), which contains
the direct URL, credentials and password lookup command.

**Create the Working Copy.** In the first screenshot, **①** identifies Main
810003 and **②** points to **Create Working Copy** in the right sidebar.

![Main 810003 and Create Working Copy, numbered pointers 1 and 2](tests/walkthrough/01-main-annotated.png)

[Original capture](tests/walkthrough/01-main.jpg).

Enter a unique Working Copy Name and click **Create Working Copy**. Create it
from current Main; old copies 100/102 predate the baseline correction. The
screenshots use the separate documentation copy **103**, “E3 screenshot guide”;
your newly assigned copy ID will differ.

![Create Working Copy dialog with Main application 810003 and a copy name](tests/walkthrough/02-create-working-copy.jpg)

**Change the page title.** In your Working Copy, open **1 – Home**. In Page
Designer, select the **Page 1: Home** tree root (**①**), then change
**Identification → Title** in the right property panel (**②**) to
`Hello World demo 2`. Use a different suffix on each replay. Click **Save**
(**③**), wait for **Changes saved**, then run the page and check the browser
tab title. The field to change is the page Title, not the page Name or the
region Name. Keep the `Hello World - Git pipeline` region heading unchanged;
the existing acceptance SQL checks that exact region name.

![Page Designer: select page root, edit Title, and Save, numbered pointers 1 to 3](tests/walkthrough/04-page-title-annotated.png)

[Original capture](tests/walkthrough/04-page-title.jpg).

**Compare with Main.** Return to the Working Copy's application home using
the **Application** breadcrumb. Under **Working Copy Tasks**, choose
**Compare Changes** to review, or **Merge into Main** to enter the comparison
and merge wizard shown below. Expect **1 Changed**, with only **Home / PAGE:1**
selected. Review its difference before clicking **Next**. Keep unrelated
concurrent authoring out of this checkpoint.

![Working Copy home with Compare Changes and Merge into Main links](tests/walkthrough/03-working-copy.jpg)

![Native comparison showing one changed Home page](tests/walkthrough/05-compare.jpg)

**Merge the reviewed page.** At confirmation, check that the selected component
is **Home / PAGE:1** (**①**). Keep **Backup target app first** selected (**②**).
Leave **Delete Working Copy after merge** unchecked if retaining it for the
demo. Click **Confirm Merge** (**③**). Open Main **810003**, run Home, and check
that its browser tab title now matches your change.

![Confirm merge: Home page, native backup, and Confirm Merge, numbered pointers 1 to 3](tests/walkthrough/06-confirm-merge-annotated.png)

[Original capture](tests/walkthrough/06-confirm-merge.jpg).

These screenshots show the confirmation controls; the documentation copy was
not merged into Main while capturing them. Perform the merge for your own demo.

**Checkpoint:** Main contains your intended page title; its inherited initialization
remains blank. Do not insert the retired E1 controller hook.

### D. Capture, commit and stage using native SQLcl — slide 10

In the **application terminal**, use the project's recorded SQLcl version to
select an installed tool. SQLcl PROJECT enforces `.sqlcl.version` from
`.dbtools/project.config.json`; a newer executable can be installed successfully
and still be rejected by this project. Read that value rather than hard-coding
a version or changing the project to match whichever tool was found first:

A newer SQLcl can be adopted as a reviewed toolchain upgrade: update the project
configuration and the workflow's SQLcl setup together, then verify export,
stage, native verification, packaging and deployment with that version.
Multiple SQLcl installations can coexist on the host. For this demonstration,
select the version already recorded by the project and exercised by its pipeline.
This is a project-wide production requirement:
[NFR-5 — SQLcl PROJECT toolchain compatibility](../../docs/srs.md#quality-requirements-and-initial-release).

```bash
echo "Selecting Java 21..."
export JAVA_HOME="$(brew --prefix openjdk@21)/libexec/openjdk.jdk/Contents/Home"
if [ ! -x "$JAVA_HOME/bin/java" ]; then
  e3_java=$(find "$HOME/projects/APEX_CICD/.local-apex/tools" "$HOME/Applications" "$HOME/tools" -type f -path '*/jdk-21*/Contents/Home/bin/java' -print -quit 2>/dev/null)
  if [ -n "$e3_java" ]; then export JAVA_HOME="${e3_java%/bin/java}"; fi
fi
echo "Selecting SQLcl for this project..."
e3_project_version=$(jq -er '.sqlcl.version' .dbtools/project.config.json)
e3_sqlcl=''
while IFS= read -r e3_candidate; do
  printf 'Checking SQLcl: %s\n' "$e3_candidate"
  e3_candidate_version=$("$e3_candidate" -nohistory -noupdates -version </dev/null 2>&1) || { echo 'Version probe failed; continuing.' >&2; continue; }
  if [[ "$e3_candidate_version" == *"Release $e3_project_version "* ]]; then
    e3_sqlcl="$e3_candidate"
    break
  fi
done < <(find "$HOME/projects/APEX_CICD/.local-apex/tools" "$HOME/Applications" "$HOME/Downloads" "$HOME/tools" \( -name .git -o -name node_modules -o -name .venv \) -prune -o -type f -path '*/sqlcl*/bin/sql' -print 2>/dev/null)
if [ -n "$e3_sqlcl" ]; then
  export PATH="$(dirname "$e3_sqlcl"):$PATH"
  hash -r
  command -v sql
  sql -version
else
  echo 'No compatible SQLcl was selected. Review the probe messages before continuing.' >&2
fi
```

Search is limited to the earlier lab tool cache and the named application/tool
directories; it does not traverse every project checkout. Each probe prints its
executable path and runs with closed standard input so
SQLcl cannot consume the discovery loop's path list or wait for terminal input.
If you cancel discovery, the final message means selection did not complete;
it does not establish that the required installation is absent.

**1. Get the E1_DEV_C database password in the Bash terminal.** Run this before
opening SQLcl, and copy the printed value:

```bash
jq -er '.E1_DEV_C | select(type == "string" and length > 0)' "$HOME/projects/APEX_CICD/.local-apex/e1-secrets.json"
```

This reads the prepared host's existing provisioning record. Select the
**E1_DEV_C** key for the database login; the **DEV_C** key is the different
Builder password used for browser sign-in.

**2. Start SQLcl interactively:**

```bash
sql -nohistory -noupdates /nolog
```

**3. At the SQL prompt, save the author connection as lab-dev-c.** Paste the
password retrieved in step 1 at the password prompt. This name is the
project's configured connection name; do not append your Git branch or demo ID.
`-replace` repairs an existing definition under that same name:

```sql
connect -save lab-dev-c -savepwd -replace E1_DEV_C@//127.0.0.1:1521/FREEPDB1
```

When the password is provided you may continue.

```sql
connect -name lab-dev-c
select user from dual;
exit
```

Require a successful connection and **E1_DEV_C** from the query before capture.
If Oracle reports ORA-01017, stop and retrieve the E1_DEV_C value again; do not
continue to export while disconnected or substitute the DEV_C Builder password.

Use the same SQLcl home for profile setup and capture: the commands here use
the default native connection store. A profile saved with another `-home`
is not automatically available in this default store.

This is your native author profile outside the checkout; workflows create
separate temporary connections from GitHub secrets.

#### Script introduction: capture the authoring checkpoint

**Complete source — `sql/capture.sql`:**

```sql
set echo off verify off define off
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name lab-dev-c
project export -list
project export
exit success
```

`sql/capture.sql` reconnects to **lab-dev-c**, runs `project export -list` to
show the export scope, then `project export` to capture the configured schema
and APEX definitions into `src`. It reads the authoring database and writes
repository files; it does not stage a release or deploy to the target. The
project's export settings determine which definitions are captured.

The SQL prologue disables command echo, substitution verification and `&`
substitution (`set echo off verify off define off`). `whenever sqlerror` and
`whenever oserror` request failure exit and rollback for SQL/OS errors; they
do not guarantee every PROJECT diagnostic becomes a failing process status.
`exit success` therefore needs the visible output checks described below.
The same prologue and named author connection are used by stage/verify.

In the launcher, `-name lab-dev-c` establishes the saved connection before
the file executes, so a missing profile fails at startup. `-L` avoids repeated
login attempts, `-S` suppresses startup noise, and `-nohistory -noupdates`
avoids statement-history persistence and update checks. The script's own
`connect -name lab-dev-c` makes its connection context explicit as well.

Back at the shell, create
one **slashless** feature branch per change. If already on that feature branch,
continue with the baseline/capture commands rather than creating another branch:

```bash
git switch -c "e3-demo-$(date +%Y%m%d%H%M%S)"
git branch -f e3-base "$(jq -r .baseline_sha pipeline.json)"
sql -nohistory -noupdates -S -L -name lab-dev-c @sql/capture.sql
git diff -- src
git status --short
```

Review the export for the page title you just changed. If there is no intended
diff, resolve the authoring/connection issue before continuing. Commit reviewed
source **before** staging:

```bash
git add src
git commit -m "fix: update demo page title"
```

#### Script introduction: stage the committed source change

**Complete source — `sql/stage.sql`:**

```sql
set echo off verify off define off
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name lab-dev-c
project stage -branch-name e3-base
exit success
```

`sql/stage.sql` connects to **lab-dev-c** and runs
`project stage -branch-name e3-base`. `e3-base` identifies the accepted baseline
from `pipeline.json`; SQLcl compares it with the current named feature branch
and creates the native distribution and Liquibase changelogs in `dist`.
Committing source first makes that branch comparison meaningful. This builds
deployment inputs without applying them to the target database.

```bash
sql -nohistory -noupdates -S -L -name lab-dev-c @sql/stage.sql
```

#### Script introduction: verify source and staged distribution

**Complete source — `sql/verify.sql`:**

```sql
set echo off verify off define off
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name lab-dev-c
project verify -cbn e3-base -verbose
exit success
```

`sql/verify.sql` connects to **lab-dev-c** and runs
`project verify -cbn e3-base -verbose`. It checks source/distribution agreement,
changelog references, APEX exports and project/tool configuration against the
same baseline. It does not execute the staged installation. Read the native
summary and require **Errors: 0**, even if the SQLcl process exits successfully.
[Chapter H](#how-native-verification-detects-an-incomplete-distribution)
explains the individual rules and demonstrates a missing-file failure.

```bash
sql -nohistory -noupdates -S -L -name lab-dev-c @sql/verify.sql
git diff -- dist
git status --short
```

**Checkpoint:** read verification output and require **Errors: 0**; process exit
success alone is insufficient. Review generated distribution and project metadata
shown by `git status`. Commit only the generated changes you have reviewed:

```bash
git add dist
git diff --cached --stat
git commit -m "chore: stage native demo distribution"
git status --short
```

If native tools changed additional tracked project metadata, review and include
that metadata before pushing. Do not edit exported source or archives to make
verification pass. Finish with a clean working tree.

### E. Open the PR, review and let the workflow version it — slides 12–13

Push the feature branch and explicitly create its PR:

```bash
git push -u origin HEAD
gh pr create --repo "$e3_repo" --base main --title "fix: update demo page title" --label patch --body "Update the Home page title through native APEX Working Copy/Main and SQLcl PROJECT. Native verification reports Errors: 0."
```

Open the returned PR URL. The reviewer checks source/distribution diffs and
successful **PR checks**. Follow the screens below in your own lab repository;
PR numbers and branch names vary on each replay.

**① Confirm the change PR title and classification.** The example is
[lab PR #1](https://github.com/rstyczynski/APEX_CICD_E3_LAB/pull/1).
Exactly one classification label is allowed:
`patch` matches `fix:`, `minor` matches `feat:`, and `major` matches `feat!:`.

![Change PR with semantic title and patch label](tests/walkthrough/github/01-change-pr.jpg)

**② Open Files changed.** Review both `src` and `dist` in the left file tree.
Expand the page changes and confirm the intended title appears in both source
and staged distribution; review any generated metadata changes as well.

![Files changed showing source and distribution in the file tree](tests/walkthrough/github/02-files-changed.jpg)

**③ Open Checks.** Require successful **PR checks** for the latest head commit.
The example below shows the successful check for `2c28802`.

The two **PR checks** entries are separate runs of the same workflow for this
commit: PR events such as opening the PR and adding its label can each trigger
a run. Both validate the classification label against the semantic PR title,
check the required native project/source/distribution files and absence of
Python files, and lint the GitHub workflows with `actionlint`. They do not
connect to APEX or deploy; native verification is performed during staging and
again in the deployment workflow.

![Successful PR checks for the latest change PR head](tests/walkthrough/github/03-pr-checks.jpg)

Return to **Conversation**. While signed in with merge permission, use the
merge button's dropdown to select **Squash and merge**. In the confirmation
form, set the squash title to `fix: update demo page title`, then confirm.
The squash commit's semantic history drives automated versioning.

**④ In Actions, wait for Prepare version and changelog to complete.** Open
the run triggered by your merged change and require **Success**.

The remaining screenshots are **historical examples from the public seed
repository `rstyczynski/APEX_CICD_E3`**. They show the completed v1.0.4 run,
including an already merged release PR. Use your own lab's current release PR
and generated version when following these steps.

![Historical successful Prepare version and changelog run](tests/walkthrough/github/08-prepare-version.jpg)

**⑤ Open the generated Release Please PR.** Its bot-authored description
contains the proposed version and release notes. This historical example is
[release PR #10](https://github.com/rstyczynski/APEX_CICD_E3/pull/10).

![Historical bot-generated release PR with proposed changelog](tests/walkthrough/github/04-release-pr.jpg)

Open **Files changed** and review `CHANGELOG.md`, `version.txt` and
`.release-please-manifest.json`. Confirm the same proposed version in all three.

![Historical release PR file tree and generated version and changelog diffs](tests/walkthrough/github/05-release-files.jpg)

**⑥ Check the release PR before merging.** If checks are absent on this
bot-created PR, open **Actions → PR checks → Run workflow**, choose **main**,
enter the **current release PR number**, and click **Run workflow**. These
controls require a signed-in account with workflow permission. Wait for the
run to finish successfully and inspect its `check` job to confirm it validated
your release PR's latest head. The run summary displays `main` because that is
the workflow dispatch branch; the PR number selects the PR being checked.

![Historical successful manually triggered PR checks run](tests/walkthrough/github/06-release-pr-check-run.jpg)

**⑦ Merge the generated release PR** and wait for **Prepare version and changelog**
again. In Releases, confirm the generated tag and matching release notes. Record
that tag for step F. **Do not type a new version or create a tag yourself.**
No PR merge, release PR merge or tag publication deploys the application.

![Historical GitHub Release published by github-actions with tag and release notes](tests/walkthrough/github/07-published-release.jpg)

**Checkpoint:** the workflow has generated the version and both changelogs.
For this display-only change, expect the next patch after the current accepted
release, rather than a hard-coded replay of historical v1.0.4.

### F. Manually deploy the published tag — slide 15

The deployer opens Actions → **Deploy selected version** → Run workflow, chooses
**main**, and enters the exact **published tag from step E** as `version_tag`.
Before starting it, read the SQL sequence below so each workflow step has a
visible meaning. Alternatively, use the authenticated application terminal
after reviewing this introduction.

#### Workflow introduction: tool setup and isolated connections

`release.yml` checks out control scripts from `main` in `controller` and the
selected tagged application in `application`. The controller runs the accepted
automation while the tag identifies the application content being packaged.
The workflow verifies that the tag is a published release, its commit belongs
to accepted history, and `version.txt` agrees with the selected tag.

The shared `setup-native` action selects Java and verifies the downloaded
SQLcl archive checksum. It sends generated `connect -save ... -savepwd`
commands to SQLcl through standard input using GitHub environment secrets.
`-home` isolates the saved **lab-dev-c** and **e3-target** profiles in a private
job directory rather than the operator's default SQLcl store. It also creates
the native APEX deployment mapping for workspace, application ID, schema and
alias. `GITHUB_PATH` supplies the tool executable, action outputs expose generated
paths, and `GITHUB_ENV` makes those paths available to subsequent steps.
Private connection material and snapshots are excluded from published artifacts
and removed by an always-run cleanup step.

#### SQL introduction: verify and package before target writes

First, `sql/verify.sql` performs the native check explained in
[step D](#script-introduction-verify-source-and-staged-distribution), using the
job's isolated author profile. The workflow requires **Errors: 0** and rejects
the Oracle/client diagnostic patterns it checks before proceeding.

**Complete source — `sql/package.sql`:**

```sql
set echo off verify off define on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
project gen-artifact -name e3 -version &1 -format zip
exit success
```

Next, `sql/package.sql` runs
`project gen-artifact -name e3 -version &1 -format zip`. `&1` receives the selected
tag's numeric version. Its `define on` enables this positional substitution;
the workflow restricts the tag to the expected semantic-version format first.
The command packages the selected Git state as `artifact/e3-<version>.zip`.
It does not recapture live DEV or install the archive.

#### SQL introduction: preserve a target baseline and restrict access

**Complete source — `sql/snapshot.sql`:**

```sql
set echo off verify off define on serveroutput off
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name e3-target
begin
  if user <> '&2' then raise_application_error(-20931,'Unexpected target'); end if;
end;
/
set heading off pagesize 0 feedback off linesize 32767 long 1000000 longchunksize 32767 trimspool on
spool "&1"
select 'greeting_history|'||json_object(*) from greeting_history order by greeting_id;
select 'hello_entries|'||json_object(*) from hello_entries order by entry_id;
select 'world_entries|'||json_object(*) from world_entries order by entry_id;
select 'hello_config|'||json_object(*) from hello_config order by config_id;
select 'world_config|'||json_object(*) from world_config order by config_id;
select 'lab_components|'||json_object(*) from lab_components order by component;
select 'lab_state|'||json_object(*) from lab_state order by state_key;
spool off
exit success
```

`sql/snapshot.sql` connects to **e3-target**, checks `user` against its expected
schema argument and spools ordered `json_object(*)` rows from greeting history,
Hello/World entries and configuration, component metadata and lab state.
`&1` is the private output path and `&2` the expected schema. Stable ordering
and disabled report headings/feedback let `cmp` compare captured business
fields before and after deployment. This is not a complete schema snapshot.

**Complete source — `sql/restrict.sql`:**

```sql
set echo off verify off define on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name e3-target
begin
  if user <> '&1' then raise_application_error(-20931,'Unexpected target'); end if;
  apex_util.set_security_group_id(apex_util.find_security_group_id('&2'));
  apex_application_admin.set_application_status(
    p_application_id => &3, p_application_status => apex_application_admin.c_app_restricted_access,
    p_allowed_users_list => apex_t_varchar2('VERIFIER'));
  commit;
end;
/
exit success
```

`sql/restrict.sql` also checks the target schema, selects the APEX workspace
security group with `apex_util.set_security_group_id`, then calls
`apex_application_admin.set_application_status` with restricted access and
**VERIFIER** as the allowed user. It commits that availability change.
Its three arguments identify schema, workspace and application; this is an
APEX availability control, not an exclusive database deployment lock.

#### SQL introduction: deploy the archive and compare retained data

**Complete source — `sql/deploy.sql`:**

```sql
set echo off verify off define on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name e3-target
begin
  if user <> '&3' then raise_application_error(-20931,'Unexpected target'); end if;
end;
/
define DEFAULTS_FILE = '&2'
project deploy -file &1
exit success
```

`sql/deploy.sql` connects to **e3-target** and checks the expected schema (`&3`).
It defines `DEFAULTS_FILE` from `&2`, making the generated APEX target mapping
available to the native installer, then runs `project deploy -file &1` on the
packaged archive. SQLcl PROJECT executes its native installation through
Liquibase. SQL/OS errors request failure exit; the workflow additionally scans
the deployment log for its configured error patterns. Oracle DDL can commit
implicitly, so the prologue's rollback is not an all-or-nothing deployment
guarantee.

Import can restore source application availability, so the workflow runs
`restrict.sql` again with the same target arguments before its checks. It then
runs `snapshot.sql` again into a second private file and uses `cmp` to require
the captured rows and fields to match. Reapplying restriction does not prove
atomic fencing throughout the import.

#### SQL introduction: check readiness and publish availability

**Complete source — `sql/accept.sql`:**

```sql
set echo off verify off define on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name e3-target
-- Read-only behavior checks precede publication.
declare n number;
begin
  if user <> '&1' then raise_application_error(-20931,'Unexpected target'); end if;
  lab_runtime.assert_ready;
  select count(*) into n from apex_application_page_regions
   where application_id=&3 and page_id=1 and region_name='Hello World - Git pipeline';
  if n <> 1 then raise_application_error(-20932,'Expected Home heading missing'); end if;
  apex_util.set_security_group_id(apex_util.find_security_group_id('&2'));
  -- Native APEX executes the application's Initialization PL/SQL Code.
  apex_session.create_session(p_app_id=>&3,p_page_id=>1,p_username=>'VERIFIER');
  apex_session.delete_session;
end;
/
-- APEX availability is inherited from the E.2 native approach.
begin
  apex_util.set_security_group_id(apex_util.find_security_group_id('&1'));
  apex_application_admin.set_application_status(
    p_application_id => &3, p_application_status => apex_application_admin.c_app_available);
  commit;
end;
/
prompt PASS native readiness, heading and APEX publication
exit success
```

`sql/accept.sql` connects to **e3-target**, checks the schema and calls
`lab_runtime.assert_ready`. It requires exactly one page-1 region named
`Hello World - Git pipeline`. After selecting the workspace security group,
it creates and deletes an APEX session as **VERIFIER**; session creation
executes native application initialization and can expose errors that a metadata
query alone misses. Only after those checks does it set the application status
to available and commit. This is native runtime acceptance, while step G checks
the actual browser page title and history. A successful workflow also writes
a receipt binding the tag, source commit and archive SHA-256.

In `accept.sql`, `&1`, `&2` and `&3` receive target schema, workspace and
application ID respectively. The publication block looks up the workspace
using `&1`; this works for this lab because schema and workspace are both
`E3_TARGET`. It must not be assumed to support different schema/workspace names
without a reviewed correction. The source is shown as executed, including this
lab-specific assumption.

#### Start the reviewed deployment workflow

```bash
read -r -p "Published tag to deploy (for example v1.0.5): " version_tag
```

```bash
gh release view "$version_tag" --repo "$e3_repo"
gh workflow run release.yml --repo "$e3_repo" --ref main -f "version_tag=$version_tag"
```

Open the newly dispatched run in Actions and follow its steps through completion.
Require successful native verification, packaging, deployment, retained-data
comparison, native session/heading/readiness checks and cleanup. Inspect the
uploaded receipt for the selected tag, source commit and archive hash.

The **Set up native tools and job-scoped connections** step selects Java 21
through `setup-java` and downloads, checksum-verifies and extracts SQLcl on
every deployment or qualification run. Java may reuse the runner's tool cache;
SQLcl currently has no reuse step. This does not install Oracle Database, APEX
or ORDS, which must already be running. Connections are generated privately
for each job and removed afterward.

Reducing this repeated setup is proposed in
[PBI-055](../../BACKLOG.md#pbi-055-reduce-repeated-pipeline-toolchain-setup),
without adding optimization to the E.3 happy-path prototype. Evaluate a verified
tool cache or a provisioned runner toolchain first; a versioned custom image
is another candidate if its platform, database connectivity and maintenance
cost are justified. Keep secrets and connection stores out of reusable caches
or images. GitHub documents [dependency caching](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching)
and [container jobs](https://docs.github.com/en/actions/how-tos/write-workflows/choose-where-workflows-run/run-jobs-in-a-container).

**Checkpoint:** the run succeeds for the tag you selected. If it fails, inspect
the failed step before continuing; do not claim a successful deployment or
automatically reset/redeploy the target.

### G. Verify the deployed application in the browser — slides 16–17

Retrieve **only LAB_USER's application password** in the terminal, using the
same retained lab provisioning record as the earlier credential lookups:

```bash
jq -er '.LAB_USER | select(type == "string" and length > 0)' "$HOME/projects/APEX_CICD/.local-apex/e1-secrets.json"
```

Copy the displayed value into the application login form. This is the
**LAB_USER application password**, distinct from the DEV_C Builder and
E3_TARGET database passwords. The command only reads the existing record;
keep the displayed password out of screenshots and Git. On another host, use
that lab's assigned LAB_USER credential.

Open [target application 810203](http://127.0.0.1:8080/ords/f?p=810203:1), sign
in as **LAB_USER** using its existing application password, and check the **new
page title from step C** in the browser tab, and the retained
`Hello World - Git pipeline` region heading. Inspect the greeting history and confirm the existing
rows remain. The inherited APEX footer stays 1.0.0; the pipeline release identity
is the generated Git tag and deployment receipt.

Record the source PR, release PR, generated tag, deployment run URL, receipt and
browser observation for your run.

**Checkpoint:** deployment verification is complete when the selected release
is deployed, the new page title is visible and prior history is retained.

### H. Demonstrate rejection of incomplete source

**Purpose:** test whether native SQLcl PROJECT verification detects an
incomplete staged distribution before deployment. This is a separate negative
test of the architecture's verification gate; it does not verify the application
deployed in steps F–G.

#### How native verification detects an incomplete distribution

The workflow runs `project verify -cbn e3-base -verbose` through `sql/verify.sql`.
SQLcl uses the project configuration, staged Liquibase changelogs, exported
source and comparison branch. `e3-base` points to the baseline commit recorded
in `pipeline.json`. These are native SQLcl rules, not checks inferred from PR
labels or semantic commit messages. Oracle documents the command and branch
comparison in the [SQLcl 25.4 PROJECT reference](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.4/sqcug/project.html).

The [successful verification log](tests/github-native-verify.log) records these
relevant rules for the qualified tool version:

1. **Referenced scripts must exist and be readable.**
   `stagechangelogfilesvalid` checks included scripts and cross-references.
   `stagechangelogcomplete` separately validates the stage changelog structure.
2. **Source changes and staged changes must correspond.** `stagesourcediff`
   compares against the selected baseline and checks that modified source is
   represented in `dist` and distribution changes are represented in `src`.
3. **Staged APEX exports must be complete and match source.**
   `apexchangelogcomplete`, `apexchangelogfilesvalid` and `apexinsrcmatchesdist`
   check APEX changelog entries, staged files and source/distribution agreement.
4. **Project structure must be consistent.** Additional checks cover duplicate
   changelog entries, configured soft-object placement, SQLcl version,
   export filters/formatting configuration and snapshot validity.

In this experiment, the deleted SQL file remains referenced by its stage
changelog. SQLcl therefore reports **ERROR `stagechangelogfilesvalid`** and
**Errors: 1**. The [recorded rejection log](tests/github-native-rejection.log)
identifies the missing `e1_dev_c/package_bodies/lab_runtime.sql` file and the
changelog that includes it. Other rules can still pass: this example's
`stagechangelogcomplete` result remains successful.

The deployment workflow requires an explicit **Errors: 0** summary and rejects
the Oracle/client error patterns it checks before packaging or target writes;
it does not rely solely on SQLcl's process exit code. The corrected qualification
requires the intact copy to report zero errors. For the damaged copy it requires
a positive error count, ERROR rows only for the intended stage rule, and the
literal selected missing path inside that rule's diagnostic. The historical
workflow used a weaker rule-name check; its retained log nevertheless shows the
genuine missing-file failure.
This establishes structural/source consistency for the exercised case. It does
not prove business correctness, complete dependency capture or target-schema
drift protection.

#### First demonstrate the native check manually

Use the **application terminal from step D**, with the project-compatible
SQLcl on PATH and the saved `lab-dev-c` connection working. Keep Oracle running.
Use the published `version_tag` selected in step F. This exercise makes a
temporary clone, so your application checkout and published tag stay intact.
It runs verification only; it does not package or deploy anything.
The clone uses a named branch because this SQLcl PROJECT version requires one
for its branch comparison.

##### Script introduction: the three `verify.sql` calls

**Complete source — `sql/verify.sql`:**

```sql
set echo off verify off define off
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name lab-dev-c
project verify -cbn e3-base -verbose
exit success
```

Each call executes the same `connect -name lab-dev-c` and
`project verify -cbn e3-base -verbose` explained in
[step D](#script-introduction-verify-source-and-staged-distribution). The first
checks the intact tagged distribution; the second checks a local copy with a
referenced SQL file moved aside; the third checks it after restoration.
The changelog is deliberately left untouched, so its reference becomes dangling
in the second call. No custom SQL validation replaces the native rule.

The subshell limits directory/variable changes to this exercise. Cloning with
`--no-hardlinks` separates its files from the application checkout. `tee`
retains visible SQLcl output; `pipefail` preserves command failure through the
pipeline. The negative call allows an expected nonzero exit so its diagnostic
can be inspected. The shared `assert-missing-changeset.awk` assertion requires
the positive error count, intended **ERROR** rule and literal selected path in
that same rule's message. It strips ANSI/table padding and joins only fragments
forming the exact expected path; unrelated errors or paths under another rule
cannot establish success. It asserts native output rather than replacing PROJECT
verification. Load it from the parent checkout so old tags need not contain it.
The positive/restored calls require **Errors: 0**. These assertions matter
because PROJECT diagnostics are not reliably represented by process status
alone. Moving the script outside the clone's application tree preserves it
for restoration without editing the changelog or published source.

Run this Bash block from the application repository. Read the output at each
numbered marker: the first verification must pass, the second must identify
the missing file, and the final verification must pass after restoration.

```bash
(
  set -euo pipefail
  cd "$(git rev-parse --show-toplevel)"
  : "${version_tag:?Set version_tag to the published tag used in step F}"
  e3_controls="$(git -C ../APEX_CICD rev-parse --show-toplevel)/examples/git-pipeline/.github"
  test -f "$e3_controls/assert-missing-changeset.awk"
  git fetch origin "refs/tags/$version_tag:refs/tags/$version_tag"
  e3_demo=$(mktemp -d "${TMPDIR:-/tmp}/e3-native-rejection.XXXXXX")
  printf 'Disposable exercise and logs: %s\n' "$e3_demo"
  git clone --no-hardlinks --no-checkout . "$e3_demo/application"
  cd "$e3_demo/application"
  git checkout -B e3-manual-qualification "$version_tag"
  git branch -f e3-base "$(jq -er .baseline_sha pipeline.json)"

  printf '\n① Intact distribution: expect Errors: 0\n'
  # Native PROJECT verification of the unmodified tagged distribution.
  sql -nohistory -noupdates -S -L -name lab-dev-c @sql/verify.sql \
    | tee "$e3_demo/positive.log"
  grep -Eq 'Errors:[[:space:]]*0([^0-9]|$)' "$e3_demo/positive.log"

  e3_missing=$(find dist/releases/next/changes -type f -name '*.sql' -print -quit)
  test -n "$e3_missing"
  printf '\n② Remove this staged script, leaving its changelog reference: %s\n' "$e3_missing"
  find dist/releases/next/changes -name '*.xml' \
    -exec grep -nHF "$(basename "$e3_missing")" {} +
  mv "$e3_missing" "$e3_demo/removed-changeset.sql"

  printf '\n③ Incomplete distribution: expect a missing-file ERROR\n'
  # The same verification now follows a changelog reference to a missing file.
  if sql -nohistory -noupdates -S -L -name lab-dev-c @sql/verify.sql \
    | tee "$e3_demo/negative.log"; then :; fi
  awk -v expected="$e3_missing" -f "$e3_controls/assert-missing-changeset.awk" "$e3_demo/negative.log"

  printf '\n④ Restore the script: expect Errors: 0 again\n'
  mv "$e3_demo/removed-changeset.sql" "$e3_missing"
  # The same verification must pass again after restoring the referenced file.
  sql -nohistory -noupdates -S -L -name lab-dev-c @sql/verify.sql \
    | tee "$e3_demo/restored.log"
  grep -Eq 'Errors:[[:space:]]*0([^0-9]|$)' "$e3_demo/restored.log"
  git status --short
  printf '\nPASS: intact → rejected → restored. Logs retained in %s\n' "$e3_demo"
)
```

Inspect the **ERROR** row in the second result. Its changelog path and missing
script path explain the failure directly. The final `git status --short`
should be empty. The subshell returns you to your original application
checkout; the disposable clone and logs remain at the printed temporary path.

The [manual rehearsal log](tests/manual-native-rejection.log) records the earlier
sequence on 2026-11-04 using historical tag v1.0.4 and SQLcl 25.4.1.022.0618:
zero errors, one missing-file error, then zero errors after restoration.
The corrected assertion has offline fixture coverage; this review correction
does not claim a fresh SQLcl rehearsal or qualification run.

#### Then demonstrate the same check automated by GitHub Actions

##### Workflow introduction: `qualification.yml`

The workflow selects the tag on a named qualification branch and reuses the
private connection setup described in step F. Its first `verify.sql` call
requires zero errors. Before disturbing the runner's files, `snapshot.sql`
records the captured target rows using the target-schema guard described in
step F. It then removes one staged SQL file locally and calls `verify.sql`
again, requiring the error-count/rule/path assertion described above. The path
comes from the actual selected file before removal. A second `snapshot.sql`
call captures the same target fields and
`cmp` requires them unchanged. It writes `qualification.json`, uploads only
public result logs/receipt and removes private job material. No packaging,
restriction, deployment or publication SQL is called in this workflow.

Keep the local runner running. Open **Actions → Qualify native verification
gate → Run workflow**, choose **main** and the same published tag, then run it.
The workflow first verifies the intact source. It then deletes one changeset
SQL file from its disposable runner checkout and requires native verification
to reject the incomplete distribution. The repository and published tag remain
unchanged. It compares target snapshots before and after the experiment and
never calls deployment.

The workflow automates the intact-versus-missing-file comparison you just ran
manually, adding private job connections, target snapshots and an archived
receipt. It uses its own disposable checkout rather than the CLI exercise's
temporary clone.

New receipts use `verification_schema: 2` and record `missing_changeset`,
`controller_sha` and `sqlcl_version_output`, separately from the application SHA.
The receipt path must match the selected path used by the diagnostic assertion.
Historical v1.0.4 receipts remain unchanged and are supported only with their
pinned original run/source/path context; absent fields do not establish a
new-format pass. An existing LAB must adopt the reviewed controller/helper
revision before claiming this corrected qualification behavior. Offline tests
do not establish a fresh native workflow run.

Require **Success** for the workflow: success here means the deliberate defect
was rejected, not that the broken distribution passed. Download its
`e3-qualification-<run ID>` artifact and inspect `positive.log`, `negative.log`
and `qualification.json`. The receipt must report `positive_native_verify`,
`missing_changeset_rejected` and `target_unchanged` as `true`, and
`deployment_called` as `false`. The target comparison covers the fields captured
by the workflow's snapshots; it is not a full database drift check.

**Checkpoint:** intact source passes, incomplete source is rejected and the
captured target state is unchanged. Record the qualification run URL separately
from the deployment run.

When the lab is finished, stop the foreground runner with Control-C.
The Product Owner accepted this increment and closed E.3 on 2026-11-05.

## Recorded run and supporting evidence

The sections below describe the performed handover run. Their PR numbers, tags,
screenshots and results are historical references, not inputs for a new replay.

### Goal and inherited foundation

E.2 established native Working Copy collaboration, PROJECT capture/staging and
native APEX availability. E.3 adds classified Git review, generated version and
both changelogs, then manual release by a selected tag. This is an Elaboration
architecture prototype, with broader construction work deferred.

The initial E.3 run used the uncorrected E1 authoring definition and a Python
adapter; that was an implementation mistake. On Product Owner correction,
Main's legacy initialization code was cleared **in App Builder**, once, before
native export. The [saved native baseline](tests/native-author-baseline.png)
and corrected source prove the change. No exported source/archive is rewritten.
Native APEX availability is used; business-schema readiness stays in LAB_RUNTIME.

### 1. Working Copy and Main checkpoint

The original performed authoring change remains valid evidence: Working Copy
100, “E3 heading patch”, changed Home's heading to “Hello World - Git pipeline”.
Native comparison showed one changed page, none added or missing. Page 1 was
merged to Main 810003 with a backup; the Working Copy was retained.
Inspect the [native comparison](tests/working-copy-diff.png) and
[readable Working Copy screen](tests/working-copy-inspection.png).

The retained old Working Copies predate the baseline correction. Refresh their
application definition from Main or create a new Working Copy before later work.
Do not merge the old E1 initialization hook back into Main.

### 2. Native capture, review, staging and verification

In the prepared private application checkout, use SQLcl on the author's ordinary PATH and the native author profile described
in the [manual](user_manual.md#native-authoring-and-developer-pr). The
correction was performed on slashless branch e3-native-only. The actual commands
are SQLcl calls, with small SQL files that expose the native operations:

#### Historical script introduction: capture

As explained in [step D](#script-introduction-capture-the-authoring-checkpoint),
`capture.sql` selects `lab-dev-c`, lists configured export objects and exports
them into `src`. The historical invocation below used `/nolog` and relied on
the connection inside the script; the current walkthrough establishes the
named connection at startup as well.

```bash
git branch -f e3-base "$(jq -r .baseline_sha pipeline.json)"
sql -nohistory -noupdates -S -L /nolog @sql/capture.sql
git diff -- src
```

Inside `capture.sql`: `connect -name lab-dev-c`, `project export -list`,
`project export`. The native source now has a blank initialization setting;
it contains neither E1_CTRL's controller hook nor an adapter-inserted hook.
Review and commit the source before native staging:

#### Historical script introduction: staging and verification

`stage.sql` connects as the author and runs
`project stage -branch-name e3-base` to generate the native distribution from
committed changes. `verify.sql` then runs
`project verify -cbn e3-base -verbose` against the same baseline without applying
the installation. These are the operations explained before their current
invocations in step D; the historical run below also relied on the scripts'
internal connection selection.

```bash
sql -nohistory -noupdates -S -L /nolog @sql/stage.sql
sql -nohistory -noupdates -S -L /nolog @sql/verify.sql
git diff -- dist
```

Those files run `project stage -branch-name e3-base` and
`project verify -cbn e3-base -verbose`. The performed correction reported
**Errors: 0, Warnings: 0**. Review/commit the native distribution. Capture does
not transform source; release does not recapture live DEV.

### 3. Manual PR and automated release preparation

The original heading PR1 and native-baseline corrections PRs6/7 remain historical
source evidence. The current configuration correction is
[PR9](https://github.com/rstyczynski/APEX_CICD_E3/pull/9), title
`fix: configure native workflows through GitHub environments`, label patch.
Its hosted checks passed; the reviewed diff was squash merged. The policy
requires exactly one patch/minor/major label matching its Conventional Commit
squash title. Hosted PR jobs receive no database credentials.

Release Please prepared
[release PR10](https://github.com/rstyczynski/APEX_CICD_E3/pull/10) for 1.0.4.
Only version.txt, CHANGELOG.md and its manifest changed in that release PR.
Its latest head passed the manually dispatched
[hosted check 41676987381](https://github.com/rstyczynski/APEX_CICD_E3/actions/runs/41676987381).
Merging it published v1.0.4 and matching GitHub Release notes. None of these
events deploys. Roles were exercised sequentially by Codex under the Product
Owner's instruction; independent human review is not claimed.

### 4. GitHub configuration and explicit setup

The GitHub **e3-lab** environment is the configuration authority: eight nonsecret
variables and two database-password secrets, restricted to main. The
[configuration guide](sprint_E.3_github_configuration.md) records the correction
requested after the native.env discussion. The old file and E.3 lab.json were
removed; the runner registration moved outside disposable scratch.

The workflow runs the shared setup-native action: actions/setup-java selects
Java 21; pinned SQLcl is downloaded and checksum verified, then added to
GITHUB_PATH. GitHub inputs generate new private connections/mappings under
RUNNER_TEMP. Output paths feed later steps through GITHUB_ENV. Always-run cleanup
removes private material. No runner-inherited tool paths or saved connection
files are read. The manual contains the complete configuration matrix.

### 5. Deployer selects the version

The lab operator uses the versioned [runner launcher](../../scripts/e3-runner.sh)
in the parent lab repository. On a new macOS ARM64 host, with authenticated `gh`,
the documented command dependencies and the existing Oracle/APEX/ORDS lab ready,
run this sequence from the repository root (presentation slide 6):

#### Historical script introduction: runner setup and listening

The setup command below registers or retains the runner, verifies the downloaded
runner archive and checks Oracle/ORDS connectivity. The second invocation
starts its foreground job listener; the two commands have the distinct effects
explained in step B. These historical commands use the seed repository and
default runner directory. For a fresh replay, use step B's explicit lab
repository and directory instead.

```bash
./scripts/e3-runner.sh setup  # Once per host: install and register with GitHub
./scripts/e3-runner.sh        # Each lab session: start the foreground listener
```

Setup downloads and checksum-verifies the official GitHub runner, registers it
using a short-lived token, and checks Oracle/ORDS access. It retains a matching
existing registration. Expect **Setup complete**; setup alone does not start the
listener. The second command must reach **Listening for Jobs**. Keep that terminal
open and perform the dispatch below in another authenticated terminal or GitHub's
UI; stop the listener with Control-C after the lab session. The default persistent
installation is `~/actions-runner-e3`, outside the checkout. Setup does not provision
the database/APEX lab; workflow steps prepare Java, SQLcl and temporary connections.
If registration or connectivity fails, correct the reported prerequisite before
dispatching. See the [manual](user_manual.md#runner-infrastructure-and-workflow-setup)
for dependencies and options, and the [implementation record](sprint_E.3_implementation.md#current-runner-installation-and-launch)
for setup behavior. Once the local runner is online, the deployer only selects
the tag. In GitHub Actions choose
**Deploy selected version**, main, **v1.0.4**, then Run workflow. The same
explicit manual selection is available through gh:

#### Historical workflow introduction: selected-tag deployment

The dispatch below requests the historical seed release v1.0.4. The SQL scripts
execute the verify, package, snapshot, restrict, deploy, compare and publish
sequence explained before dispatch in step F. It is a historical example,
not a request to redeploy that tag when following the current walkthrough.

```bash
gh workflow run release.yml --repo rstyczynski/APEX_CICD_E3 --ref main -f version_tag=v1.0.4
```

Inspect each workflow step. GitHub Actions checks out control SQL from accepted
main separately from the tagged application. It verifies the selected state
before writes, builds one native archive, records private business fields,
uses native APEX restriction, deploys with PROJECT, reapplies restriction,
compares every field, checks native readiness/heading and publishes availability.
A later step cannot run after an earlier required failure. The receipt binds
tag, source and ZIP hash; full business snapshots remain private.

APEX import can restore source availability during import. Reapplying restriction
does not establish atomic fencing; that broader risk remains deferred. No
custom controller is added to conceal this native boundary.

### 6. Application and rejection evidence

Open [application 810203](http://127.0.0.1:8080/ords/f?p=810203:1), sign in as
LAB_USER with the existing credential, inspect the Home heading and greeting
history. The inherited APEX footer still says 1.0.0; repository versions identify
the pipeline release and do not claim automatic display stamping.

The latest [GitHub setup record](sprint_E.3_github_configuration.md) links the actual deployment run, source/ZIP identity,
browser observation and fresh test results. IT-2 now uses a separately manual qualification workflow with the same explicit
setup. It first verifies valid source, then removes an included native changeset
in the temporary checkout. PROJECT must reject it and the private target snapshot
must remain unchanged; the workflow contains no deployment command. Parent tests
read fresh GitHub evidence, not a retained local source/data snapshot.

## Slide map and handover boundary

| Slide | Topic |
|---|---|
| 1 | E.3 goal and architecture prototype |
| 2 | Agenda |
| 3 | Section 1: Architecture and setup |
| 4 | Application structure and walkthrough |
| 5 | E.2 native foundation and GitHub responsibilities |
| 6 | GitHub configuration and generated job setup |
| 7 | Section 2: Native authoring and capture |
| 8 | Retained Working Copy heading change |
| 9 | Native comparison and Main checkpoint |
| 10 | Direct SQLcl capture, stage and verify |
| 11 | Section 3: Review and release preparation |
| 12 | PR labels and Conventional Commit titles |
| 13 | Release Please version and both changelogs |
| 14 | Section 4: Deployment and results |
| 15 | Manual selected-tag native deployment |
| 16 | Deployed application and retained history |
| 17 | Assigned outcomes and next acceptance decision |
| 18 | Section 5: Oracle lifecycle mapping |
| 19 | Oracle lifecycle mapping: native authoring, Git capture and review |
| 20 | Oracle lifecycle mapping: GitHub automation, releases and deployment |
| 21 | Oracle lifecycle mapping: adaptations, accepted LC-1 and backlog follow-up |
| 22 | Thank you / Q&A closing |

Slides 19–21 map the demonstrated journey to the foundation
[Oracle lifecycle paper](../../refs/apex-lifecycle-management-v3.pdf), with
printed page references on slides and implementation/evidence pointers in
speaker notes. The Product Owner accepted
[LC-1 and its gap dispositions](sprint_E.3_pipeline_scope.md#lc-1--oracle-apex-lifecycle-alignment-validation)
on 2026-11-05. The gaps have backlog owners; full feature-centric and production
qualification remain outside the demonstrated slice.

PBI-053.1/.2/.3 retain their original criteria and SM-1/IT-1/IT-2 tests.
Construction completeness, full fencing/drift/identity coverage and general DDL
recovery remain deferred. The [handover](sprint_E.3_handover.md) records the final
outcome. The Product Owner accepted the increment and closed E.3 on 2026-11-05; see the
[closure record](sprint_E.3_handover.md#sprint-closure).

The native correction initially published 1.0.2. Its workflow passed, but the
browser exposed whitespace left in the initialization field. That version is
historical failed browser evidence. The final 1.0.3 correction clears the field
without inserting editor indentation and adds native APEX_SESSION.CREATE_SESSION
plus DELETE_SESSION before publication. This executes initialization and would
reject that observed failure; it does not replace real authentication/browser
validation. See the [correction record](sprint_E.3_native_correction.md).

The final PPTX omits internal implementation-fix history at the Product Owner's
request. Detailed corrections remain in the engineering records; the 22-slide
deck presents the delivered pipeline, operator journey, results and next steps.
