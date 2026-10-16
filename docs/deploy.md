# Local Oracle APEX with Podman (Apple Silicon)

## Preliminary work status

The Product Owner recognized this setup as completed preliminary work on
2026-10-16. It is available for potential reuse by the APEX CI/CD laboratory;
adoption will depend on the research and candidate architecture. The
verification record below describes the earlier setup work, not a new Sprint 0
execution. Commands run from the project root, although this runbook now lives
in `docs/`. No setup or cleanup commands were rerun when relocating it.

This runbook adapts [Raoul Mangoensentono's recipe](https://www.linkedin.com/pulse/simple-way-run-oracle-apex-apple-silicon-raoul-mangoensentono-5rrde/) to Podman. It installs APEX in `FREEPDB1` on `gvenzl/oracle-free`, with a separate Oracle ORDS container. All runtime resources belong to the dedicated `apex-cicd` VM. Existing Podman machines are preserved. Run commands in Bash from this directory.

Versions selected for this deployment: Oracle AI Database Free 23.26.3, APEX 24.2, and ORDS 25.3. Native ARM64 database and ORDS images are locked by digest.

## Prepare the VM and local files

Prerequisites: macOS Apple Silicon, Podman installed, `curl`, `openssl`, and internet access. Only one Podman machine can run at a time with this provider. If an unrelated VM is running, stop it deliberately before proceeding. Do not delete it.

```bash
cd /Users/rstyczynski/projects/APEX_CICD
podman machine list
podman system connection list
df -h .
mkdir -p .local-apex
chmod 700 .local-apex
```

This Mac has Podman 6.0.0 and krunkit 1.1.1. That combination fails because Podman passes `--timesync`, which krunkit 1.1.1 does not accept. Use the project-local krunkit 1.3.2 helper (including its libraries) instead of modifying Homebrew packages. Xcode command line tools (`install_name_tool`, `codesign`) are needed. The script adds a relative library search path and signs the local binaries for the hypervisor entitlement.

```bash
bash scripts/apex-helper-setup.sh
export CONTAINERS_CONF_OVERRIDE="$PWD/.local-apex/containers.conf"
podman machine init --cpus 4 --memory 6144 --disk-size 30 apex-cicd
bash scripts/apex-vm-start.sh
```

Set `CONTAINERS_CONF_OVERRIDE` again in every new terminal before starting this VM. It applies only to the current command environment; no global Podman configuration is edited.

`apex-vm-start.sh` uses a removable user LaunchAgent (`local.apex-cicd.vm-start`) to launch the VM independently of the automation terminal. This avoids losing its background processes when a tool session ends. The plist and log stay under `.local-apex/`; nothing is installed in `~/Library/LaunchAgents`. The job runs once, without KeepAlive or automatic login startup. This helper is for this repository's current path (no XML special characters in the path).

Downloaded archive checksums on 2026-10-16:

```text
a7ad0ba94f70b2d581f7dde97fe27cd07afc98c32ecc146d89fd70cce9b76456  apex_24.2.zip
de9ab62dd90461cd1df1e37b78e780690d75490f4bab1674cbb4a1f75b90c227  krunkit-1.3.2.tgz
```

Create new passwords once per fresh deployment. Do not regenerate them for an existing database. The file is deliberately local and ignored by Git.

```bash
umask 077
printf 'ORACLE_PASSWORD=Aa1_%s\nAPEX_ADMIN_PASSWORD=Aa1#%s\nORDS_PASSWORD=Aa1_%s\n' \
  "$(openssl rand -hex 16)" "$(openssl rand -hex 16)" "$(openssl rand -hex 16)" \
  > .local-apex/credentials.env
chmod 600 .local-apex/credentials.env
curl -fL --retry 3 -o .local-apex/apex_24.2.zip \
  https://download.oracle.com/otn_software/apex/apex_24.2.zip
shasum -a 256 .local-apex/apex_24.2.zip
printf '%s  %s\n' a7ad0ba94f70b2d581f7dde97fe27cd07afc98c32ecc146d89fd70cce9b76456 \
  .local-apex/apex_24.2.zip | shasum -a 256 -c -
```

## Database and APEX installation

Run these steps once on an empty environment. Setup refuses to overwrite an existing `apex-db`. To repeat a clean install, remove this environment using the cleanup section, then start from the beginning. APEX installation itself is not an idempotent migration; do not rerun it on a partially installed database.

```bash
source scripts/apex-images.env
podman --connection apex-cicd pull "$DB_IMAGE"
podman --connection apex-cicd pull "$ORDS_IMAGE"
bash scripts/apex-db-start.sh
podman --connection apex-cicd logs --tail 40 apex-db
podman --connection apex-cicd cp .local-apex/apex_24.2.zip apex-db:/tmp/apex.zip
podman --connection apex-cicd exec apex-db bash -c 'cd /tmp && unzip -q apex.zip'
podman --connection apex-cicd exec -i --workdir /tmp/apex apex-db \
  sqlplus -s / as sysdba < scripts/apex-db-install.sql \
  > .local-apex/apex-install.log 2>&1
tail -n 60 .local-apex/apex-install.log
bash scripts/apex-configure.sh > .local-apex/apex-configure.log 2>&1
podman --connection apex-cicd exec -i apex-db sqlplus -s / as sysdba \
  < scripts/apex-db-verify.sql
```

Expect APEX registry status `VALID` and zero invalid APEX objects. Allow up to an hour for APEX installation. In another terminal, `tail -f .local-apex/apex-install.log` shows progress; interrupting `tail` does not stop installation. If installation fails, preserve the log and reset the dedicated environment before a fresh attempt.

The database script uses a Podman secret for the initial SYS/SYSTEM password. It creates no application schema. The APEX administrator is `ADMIN` in workspace `INTERNAL`, with the password in `.local-apex/credentials.env`. For unattended setup, `apex-configure.sh` uses the same administrator API as `apxchpwd.sql` and the parameterized core of `apex_rest_config.sql`. SQL*Plus `ACCEPT ... HIDE` failed with piped stdin on this installation, so the script avoids those interactive prompts. Do not enable shell tracing (`set -x`) around credential handling.

Image tags used to select these releases were `gvenzl/oracle-free:23.26.3` and `database/ords:25.3.0`. The checked-in `scripts/apex-images.env` pins their digests so a later tag change does not silently change a repeat deployment.

## Install ORDS and publish APEX

```bash
bash scripts/apex-ords-install.sh > .local-apex/ords-install.log 2>&1
tail -n 50 .local-apex/ords-install.log
podman --connection apex-cicd logs --tail 60 apex-ords
```

The script copies APEX's matching images to a VM-local named volume, installs ORDS non-interactively, enables its proxied PL/SQL gateway and the recipe's Database Actions/REST features, then starts the web server. It uses the image's `oracle` user for both installation and serving, so the configuration wallet has consistent ownership. No SYS password is supplied to the long-running ORDS container. The static files are mounted read-only in ORDS. Shared volumes use `:z` for a shared SELinux label; omitting it can produce permission errors and static-file 404 responses even when Unix file permissions allow reading.

The serving container runs the image's Java launcher directly with `ords.war --config /etc/ords/config serve`. This preserves the image's ORDS installation and user while allowing Java to receive termination signals as PID 1. The image's default shell entrypoint delayed shutdown until Podman's timeout during testing.

Open <http://127.0.0.1:8080/ords/>. To administer APEX, use <http://127.0.0.1:8080/ords/apex_admin> (workspace `INTERNAL`, user `ADMIN`). To retrieve your locally generated passwords, run:

```bash
cat .local-apex/credentials.env
```

Oracle SQL connection details: host `127.0.0.1`, port `1521`, service `FREEPDB1`, user `SYSTEM` (password `ORACLE_PASSWORD` in the file). SYS connections require the SYSDBA role. This is a local HTTP development environment; both published ports bind only to loopback.

## Verify, stop and restart

```bash
bash scripts/apex-verify.sh | tee .local-apex/access-verification.log
bash scripts/apex-stop.sh
bash scripts/apex-start.sh
bash scripts/apex-verify.sh | tee .local-apex/restart-verification.log
```

Verification checks APEX's database registry status and invalid objects, authenticates SQL as SYSTEM through the published host port (via `host.containers.internal`), and fetches the ORDS landing page, APEX sign-in page, and matching static version file. APEX redirects require cookies; the script handles them using a local cookie jar. A separate browser login as `ADMIN` verifies the administrator password.

Stopping keeps all data and configuration. Starting waits for Oracle readiness before starting ORDS. Use these commands after a Mac reboot too; the environment does not start automatically at login. Allow up to 120 seconds per container for shutdown; Podman terminates a container if it has not exited within that window.

## Interrupted ORDS installation recovery

The initial tool-launched VM exited during ORDS setup. The durable LaunchAgent start method above replaces that launch method. A partial ORDS setup can leave a corrupt wallet or an incomplete procedure allowlist even when the landing page works. This recovery was used on this deployment; it is unnecessary for an uninterrupted fresh installation.

If `Wallet Version Not Supported` appears, recreate only the ORDS config volume (the database stays intact):

```bash
podman --connection apex-cicd rm --force apex-ords  # only if this container exists
podman --connection apex-cicd volume rm apex-ords-config
podman --connection apex-cicd volume create apex-ords-config
bash scripts/apex-ords-install.sh > .local-apex/ords-install.log 2>&1
```

To repair incomplete ORDS database metadata after an interruption:

```bash
source .local-apex/credentials.env
source scripts/apex-images.env
podman --connection apex-cicd stop --time 120 apex-ords
printf '%s\n' "$ORACLE_PASSWORD" | podman --connection apex-cicd run --rm -i \
  --network apex-net -v apex-ords-config:/etc/ords/config:z \
  -v apex-images:/opt/oracle/apex/images:ro,z "$ORDS_IMAGE" \
  install repair --admin-user SYS --password-stdin \
  > .local-apex/ords-repair.log 2>&1
podman --connection apex-cicd start apex-ords
bash scripts/apex-verify.sh
```

## Resource boundary

- VM: `apex-cicd`, 4 CPUs, 6144 MiB RAM, 30 GiB sparse disk.
- Connection: always specify `podman --connection apex-cicd`; do not rely on the default connection.
- Containers: `apex-db`, `apex-ords` (and temporary `apex-ords-install`).
- Network: `apex-net`; volumes: `apex-data`, `apex-ords-config`, `apex-images`.
- VM-local secret: `apex-db-password`; user LaunchAgent: `local.apex-cicd.vm-start`.
- Host ports: `127.0.0.1:1521` (Oracle), `127.0.0.1:8080` (ORDS/APEX).
- Host downloads, passwords and logs: `.local-apex/`, excluded from Git.
- APEX archive: version 24.2, rather than the recipe's moving `apex-latest.zip`.

Keep sufficient disk space for image downloads, Oracle datafiles, and APEX installation. A sparse disk's configured capacity is not reserved host space.

## Remove the runtime completely

These commands destroy this environment's database and configuration. Leave the source files and runbook in place for another deployment.

```bash
cd /Users/rstyczynski/projects/APEX_CICD
export CONTAINERS_CONF_OVERRIDE="$PWD/.local-apex/containers.conf"
bash scripts/apex-stop.sh
launchctl bootout "gui/$(id -u)/local.apex-cicd.vm-start"
podman machine rm --force apex-cicd
rm -rf -- .local-apex
unset CONTAINERS_CONF_OVERRIDE
podman machine list
podman system connection list
```

Removing the dedicated VM removes its containers, volumes, networks and downloaded container images. It does not remove `podman-machine-default`. No global prune or reset is needed.

If the VM is already stopped, skip the stop command. If it is stuck during its very first boot, preserve its log before removal (`$(getconf DARWIN_USER_TEMP_DIR)/podman/apex-cicd.log`). A force removal of this dedicated VM is the reset boundary; do not delete or reset another machine.

To undo the documentation/source changes too, run the following after runtime cleanup. All listed files were created by this task; the original PDF is preserved.

```bash
rm -f -- scripts/apex-helper-setup.sh scripts/apex-vm-start.sh \
  scripts/apex-images.env scripts/apex-db-start.sh scripts/apex-db-install.sql \
  scripts/apex-configure.sh scripts/apex-db-verify.sql scripts/apex-ords-install.sh \
  scripts/apex-verify.sh scripts/apex-start.sh scripts/apex-stop.sh
# Remove these only if you have not added your own content to them:
rm -f -- .gitignore docs/deploy.md
```

References: [database image documentation](https://github.com/gvenzl/oci-oracle-free), [Oracle ORDS installation guide](https://docs.oracle.com/en/database/oracle/oracle-rest-data-services/25.3/ordig/installing-and-configuring-oracle-rest-data-services.html), and [krunkit releases](https://github.com/libkrun/krunkit/releases/tag/v1.3.2).

## Verification record (2026-10-16)

| Check | Observed result |
| --- | --- |
| Native image architecture | Database and ORDS: ARM64 |
| APEX in FREEPDB1 | 24.2.0, registry `VALID`, zero invalid APEX objects |
| Oracle host-port authentication | SYSTEM connected through host port 1521 to FREEPDB1 |
| ORDS landing page | HTTP 200 |
| APEX administration sign-in | HTTP 200 with session cookies |
| Static assets | `/i/apex_version.txt`: HTTP 200, version 24.2 |
| Administrator authentication | Browser login reached Welcome to Oracle APEX; admin / internal |
| Full VM stop and restart | SQL and HTTP access checks passed afterward |

Local evidence: `.local-apex/access-verification.log`, `.local-apex/restart-verification.log`, `.local-apex/db-verification.log`, `.local-apex/ords-repair.log`, and `.local-apex/apex-admin-verified.png`. Credentials and session cookies stay in the ignored directory. Full cleanup of the working database has intentionally not been executed; the environment is left running for use and can be removed with the commands above. Empty failed VM attempts were removed during setup without changing the original VM.
