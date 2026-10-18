# Provision and operate the local APEX runtime

## Purpose and current state

- E.1 owns this procedure.
- It provisions the infrastructure used by the [architecture](architecture.md): one Oracle database, APEX and ORDS on the dedicated apex-cicd Podman VM.
- Application authoring and releases use the private areas inside that database; an application deployment does not recreate the VM or database.

- The current environment is running.
- Inventory checked on 2026-10-16: apex-cicd has 4 CPUs, 6144 MiB RAM and a 30 GiB sparse disk; apex-db and apex-ords are running; apex-data, apex-ords-config and apex-images exist.
- The unrelated podman-machine-default is stopped and must be preserved.
- Database version is 23.26.3.0.0, APEX is 24.2.0 and ORDS is 25.3.0.r2671248.
- Image digests are pinned in [apex-images.env](../scripts/apex-images.env).

- Use the inspection section on an existing installation.
- Use fresh provisioning only after confirming that the named runtime does not exist, or after the scoped recreation procedure.
- Steps below are operator actions, performed separately with inspection between stages.
- Lifecycle scripts remain conveniences whose bounded operations are explained here.

## Maintain procedures and guided scripts together

- An operating chapter and its guided execution script form one artifact: **always update both together**.
- Preserve the numbered steps/bullets and expose each operation, its target, expected result and stop condition.
- The detailed application operator walkthrough pair is [the E.1 manual](../progress/E.1/user_manual.md) and [cicd-operator-walkthrough.sh](../scripts/cicd-operator-walkthrough.sh). The [results guide](../progress/E.1/cicd-walkthrough.md) pairs [cicd-walkthrough.sh](../scripts/cicd-walkthrough.sh) with independently runnable A–H chapter scripts. Maintain these guides, scripts and cleanup instructions together.
- The detailed operator runner uses an existing runtime. The new separate infrastructure walkthrough commands below execute bounded parts of this lifecycle procedure; A–H application chapters remain separate.
- If an infrastructure walkthrough is added, it must reference these chapters and preserve the same visible operations and data-preservation boundaries.

## Fresh walkthrough infrastructure sequence

This is the entry point before the [A–H application walkthrough](../progress/E.1/cicd-walkthrough.md). Use one operation at a time and wait for PASS. The Product Owner explicitly requested a completely disposable lab on 2026-10-18: **all current lab database data, including user_acceptance_test and greeting history, may be discarded for this fresh-start demonstration**. This exception does not apply to an ordinary release, upgrade, restart or unrelated resources.

1. Position at the repository root:

   ```bash
   cd "$(git rev-parse --show-toplevel)"
   ```

2. **Precheck** host tools, pinned SQLcl/Java, helper, APEX archive, reviewed source/release inputs and disk space. This does not require a database. An existing healthy named database is inspected for actual APEX registry version/status; absent/stopped/partial runtime is reported explicitly. Missing inputs/checksum errors stop before deletion. Acquire missing prerequisites with sections 1–4 and `bash scripts/cicd-tools.sh`, then rerun:

   ```bash
   bash scripts/cicd-walkthrough-prerequisites.sh
   ```

3. **Initialize/reuse the named Podman host** using sections 2–4. It creates apex-cicd only if absent, starts it if required and pulls pinned images. It leaves other VMs untouched:

   ```bash
   bash scripts/cicd-walkthrough-host.sh
   ```

4. **Cleanup if the lab is present**, following the scoped operations in section 12. This removes all lab database/APEX/ORDS state; absent resources are skipped. An unreachable engine is an error, not evidence of absence:

   ```bash
   bash scripts/apex-destroy.sh
   ```

5. **Install** the fresh database and APEX/ORDS only using sections 5–8. Existing containers/volumes cause refusal; do not install over partial data:

   ```bash
   bash scripts/cicd-walkthrough-apex-init.sh
   ```

6. Wait for **PASS APEX init**, including database validity and matching web/static assets. The separate boundary test confirms **zero project schemas/workspaces**; it is not project configuration inside the installer. Then follow [separate project control and onboarding](../progress/E.1/cicd-walkthrough.md#initialize-project-delivery-control): control initialization, one-area provisioning, each developer's private configuration and project readiness. Only then start A–H.
7. To **destroy** the demonstration afterward, use the same scoped cleanup operation. To repeat, run precheck, host preparation, cleanup and fresh installation again. Never substitute a global prune or system reset.

- Credentials, local tools/installers, reviewed archives and historical host evidence remain. They contain no restored business history. Stale preservation/drift journals are moved out of the active cycle.
- `.local-apex/apex-install.log` contains full APEX installation output; use `tail -f .local-apex/apex-install.log` in another terminal. ORDS installation output is `.local-apex/ords-install.log`. A failed install does not qualify a release.
- The precheck, host, cleanup and install scripts and this chapter are **one artifact** with the main walkthrough. All commands discover the repository through Git.

## 1. Open the operator terminal and inspect resources

- Prerequisites are macOS Apple Silicon, installed Podman, curl, openssl, unzip and Xcode command line tools.
- The local helper setup also uses install_name_tool and codesign.
- In Bash:

  ```bash
  cd "$(git rev-parse --show-toplevel)"
  podman --version
  podman machine list
  podman system connection list
  df -h .
  ```

- Start from any directory inside the checkout; Git selects its root. Do not copy a developer-specific home path into commands.
- A sparse VM disk consumes host space as it grows; its configured 30 GiB is not reserved host space.
- Current free host space is approximately 61 GiB, not a minimum sizing guarantee.

- If apex-cicd is running, inspect its resources:

  ```bash
  podman --connection apex-cicd ps -a
  podman --connection apex-cicd volume ls
  podman --connection apex-cicd network ls
  podman --connection apex-cicd secret ls
  ```

- Expected containers are apex-db and apex-ords, network apex-net, volumes apex-data/apex-ords-config/apex-images, and secret apex-db-password.
- A built-in podman network may also appear.
- These commands list secret metadata only.
- Do not use a default connection for mutations.
- Do not initialize an already existing VM or rerun initial database installation on its data.

- Only one machine can run at a time with this provider. If another VM is running, stop it deliberately before starting this one; never remove it to resolve that conflict.

## 2. Prepare the local helper — fresh setup only

```bash
mkdir -p .local-apex
chmod 700 .local-apex
```

- On this Mac, Podman 6.0.0 passes --timesync, which the installed krunkit 1.1.1 does not accept.
- The project uses krunkit 1.3.2 locally rather than changing the system installation:

  ```bash
  bash scripts/apex-helper-setup.sh
  ```

- [apex-helper-setup.sh](../scripts/apex-helper-setup.sh) downloads the pinned helper archive, checks its SHA-256, extracts its binaries/libraries into .local-apex/helper, adds a relative library search path, signs those local files with the hypervisor entitlement and writes .local-apex/containers.conf.
- Expected output ends with helper version 1.3.2.
- No global Podman configuration is edited.
- This setup is for the current checkout path, which must not contain XML special characters for the launch helper below.

- If the helper is already configured, inspect and reuse it rather than rerunning binary patching:

  ```bash
  .local-apex/helper/bin/krunkit --version
  cat .local-apex/containers.conf
  export CONTAINERS_CONF_OVERRIDE="$PWD/.local-apex/containers.conf"
  ```

- Set CONTAINERS_CONF_OVERRIDE in each new lifecycle terminal.
- It selects this checkout's helper.
- The archive SHA-256 is de9ab62dd90461cd1df1e37b78e780690d75490f4bab1674cbb4a1f75b90c227.

## 3. Create and start the VM — fresh setup only

- Only when apex-cicd is absent:

  ```bash
  podman machine init --cpus 4 --memory 6144 --disk-size 30 apex-cicd
  ```

- Start the newly created VM:

  ```bash
  bash scripts/apex-vm-start.sh
  podman machine list
  podman --connection apex-cicd info
  ```

- Expected: apex-cicd is running and info returns its engine information. Stop here if startup fails; inspect .local-apex/vm-start.log before provisioning containers.

- [apex-vm-start.sh](../scripts/apex-vm-start.sh) writes a project-local plist and submits a one-shot user LaunchAgent named local.apex-cicd.vm-start.
- The job executes podman machine start apex-cicd with the local helper configuration and waits for the engine.
- This keeps the VM independent of an automation terminal's lifetime.
- Its plist/log stay in .local-apex; nothing is installed in ~/Library/LaunchAgents, and there is no automatic login startup or KeepAlive loop.
- This macOS-specific launch workaround is the only VM-start wrapper used below.

## 4. Retain or generate credentials, then acquire installers

- Credentials belong to the runtime.
- Reuse .local-apex/credentials.env if it exists, including after an authorized fresh reconstruction.
- Do not overwrite it during restart.
- This fresh-setup block refuses to replace the file:

  ```bash
  umask 077
  if [ -e .local-apex/credentials.env ]; then
    echo 'Existing credentials retained.'
  else
    printf 'ORACLE_PASSWORD=Aa1_%s\nAPEX_ADMIN_PASSWORD=Aa1#%s\nORDS_PASSWORD=Aa1_%s\n' \
      "$(openssl rand -hex 16)" "$(openssl rand -hex 16)" "$(openssl rand -hex 16)" \
      > .local-apex/credentials.env
  fi
  chmod 600 .local-apex/credentials.env
  ```

- Do not enable shell tracing around credentials.
- They are ignored by Git.
- The scripts expect the generated quote-free password format; do not substitute arbitrary shell/SQL characters without changing and reviewing that handling.

- Download the APEX installer and verify it before extraction:

  ```bash
  curl -fL --retry 3 -o .local-apex/apex_24.2.zip \
    https://download.oracle.com/otn_software/apex/apex_24.2.zip
  printf '%s  %s\n' a7ad0ba94f70b2d581f7dde97fe27cd07afc98c32ecc146d89fd70cce9b76456 \
    .local-apex/apex_24.2.zip | shasum -a 256 -c -
  ```

- Expected: OK. Do not continue on a checksum mismatch. An already downloaded archive can be checked with the second command alone.

- Load the image pins and pull each image separately:

  ```bash
  source scripts/apex-images.env
  podman --connection apex-cicd pull "$DB_IMAGE"
  podman --connection apex-cicd pull "$ORDS_IMAGE"
  podman --connection apex-cicd image inspect "$DB_IMAGE" --format '{{.Architecture}} {{.Digest}}'
  podman --connection apex-cicd image inspect "$ORDS_IMAGE" --format '{{.Architecture}} {{.Digest}}'
  ```

- Expected architecture is arm64 and digests match the environment file.
- Selected releases are gvenzl/oracle-free:23.26.3 and Oracle database/ords:25.3.0; digest references prevent a moving tag changing the installation silently.

## 5. Create the network, volumes and database — fresh setup only

- First inspect the inventory from section 1.
- Stop on unexpected existing resources and identify their origin.
- These commands are the individual operations performed by [apex-db-start.sh](../scripts/apex-db-start.sh); use this sequence or that script, never both for the same fresh installation.

```bash
podman --connection apex-cicd network create apex-net
podman --connection apex-cicd volume create apex-data
podman --connection apex-cicd volume create apex-ords-config
podman --connection apex-cicd volume create apex-images
```

- apex-data holds the database and all private application areas. apex-ords-config holds ORDS configuration/wallet. apex-images holds APEX's matching static assets.
- These volumes persist across container/VM stop and start, but disappear when the VM is removed.

- Create the initial database secret without putting its password in process arguments:

  ```bash
  source .local-apex/credentials.env
  printf '%s' "$ORACLE_PASSWORD" | podman --connection apex-cicd secret create apex-db-password -
  ```

- Start the database container:

  ```bash
  podman --connection apex-cicd run -d --name apex-db --network apex-net \
    -p 127.0.0.1:1521:1521 \
    --secret apex-db-password \
    -e ORACLE_PASSWORD_FILE=/run/secrets/apex-db-password \
    -v apex-data:/opt/oracle/oradata \
    -v apex-images:/opt/apex-images:z "$DB_IMAGE"
  ```

- Inspect startup and then check readiness:

  ```bash
  podman --connection apex-cicd logs --tail 40 apex-db
  podman --connection apex-cicd exec apex-db healthcheck.sh
  ```

- Repeat the readiness operation until it succeeds; initial startup may take several minutes.
- The existing convenience script allows up to 15 minutes.
- Do not install APEX before readiness.
- The database port binds only to loopback.
- No application schema is created by this container-start step.

## 6. Install and configure APEX — fresh database only

- Copy and extract the verified installer:

  ```bash
  podman --connection apex-cicd cp .local-apex/apex_24.2.zip apex-db:/tmp/apex.zip
  podman --connection apex-cicd exec apex-db bash -c 'cd /tmp && unzip -q apex.zip'
  ```

- Run the APEX installation in FREEPDB1:

  ```bash
  podman --connection apex-cicd exec -i --workdir /tmp/apex apex-db \
    sqlplus -s / as sysdba < scripts/apex-db-install.sql \
    > .local-apex/apex-install.log 2>&1
  ```

- [apex-db-install.sql](../scripts/apex-db-install.sql) selects FREEPDB1 and executes Oracle's apexins.sql with SYSAUX/SYSAUX/TEMP and the /i/ image prefix.
- Allow up to an hour.
- In another terminal, tail -f .local-apex/apex-install.log shows progress; Ctrl+C on tail does not stop installation.
- After installation:

  ```bash
  tail -n 60 .local-apex/apex-install.log
  ```

- Stop on installer errors.
- APEX installation is not an idempotent application migration; do not rerun it blindly against a partial installation.
- Preserve logs and use the scoped recreation procedure when a clean installation is required.

- Configure the instance administrator and REST accounts:

  ```bash
  bash scripts/apex-configure.sh > .local-apex/apex-configure.log 2>&1
  tail -n 40 .local-apex/apex-configure.log
  ```

- [apex-configure.sh](../scripts/apex-configure.sh) selects FREEPDB1, calls APEX_INSTANCE_ADMIN.CREATE_OR_UPDATE_ADMIN_USER for INTERNAL/ADMIN, runs Oracle's apex_rest_config_core.sql with the REST password and unlocks ANONYMOUS/APEX_PUBLIC_USER.
- Passwords are supplied through standard input.
- The local script avoids SQL*Plus ACCEPT HIDE, which did not work reliably with piped input in the preliminary installation.

- Verify the database before installing the web tier:

  ```bash
  podman --connection apex-cicd exec -i apex-db sqlplus -s / as sysdba \
    < scripts/apex-db-verify.sql
  ```

- Expected: FREEPDB1, APEX 24.2.0 with registry status VALID, and zero invalid APEX objects.
- The SQL file fails when registry/object checks fail.
- It also displays relevant gateway account status.
- This is a database/APEX check, not proof of browser access.

## 7. Install ORDS and expose the web endpoint — fresh setup only

- These are the individual operations in [apex-ords-install.sh](../scripts/apex-ords-install.sh).
- Use this sequence or that script, not both.
- First load the retained credentials and image pins in this terminal:

  ```bash
  source .local-apex/credentials.env
  source scripts/apex-images.env
  ```

- Populate matching static assets from the installed APEX archive:

  ```bash
  podman --connection apex-cicd exec --user root apex-db \
    bash -c 'cp -r /tmp/apex/images/. /opt/apex-images/ && chmod -R a+rX /opt/apex-images'
  ```

- Run the temporary ORDS installer, passing its two passwords over stdin:

  ```bash
  printf '%s\n%s\n' "$ORACLE_PASSWORD" "$ORDS_PASSWORD" | \
    podman --connection apex-cicd run --rm -i --name apex-ords-install --network apex-net \
      -v apex-ords-config:/etc/ords/config:z \
      -v apex-images:/opt/oracle/apex/images:ro,z \
      "$ORDS_IMAGE" install --admin-user SYS --proxy-user \
      --db-hostname apex-db --db-port 1521 --db-servicename FREEPDB1 \
      --gateway-mode proxied --gateway-user APEX_PUBLIC_USER \
      --feature-sdw true --feature-rest-enabled-sql true --feature-db-api true \
      --password-stdin > .local-apex/ords-install.log 2>&1
  tail -n 50 .local-apex/ords-install.log
  ```

- Stop on installation errors.
- Expected: successful ORDS installation and creation of its configuration/wallet.
- The temporary container is removed after exit.
- This profile enables Database Actions, REST-enabled SQL and database API features as well as the APEX gateway.
- The installer and server both use the image's oracle user so wallet ownership matches.

- Configure static assets and the gateway as separate operations:

  ```bash
  podman --connection apex-cicd run --rm \
    -v apex-ords-config:/etc/ords/config:z "$ORDS_IMAGE" \
    config set standalone.static.path /opt/oracle/apex/images
  podman --connection apex-cicd run --rm \
    -v apex-ords-config:/etc/ords/config:z "$ORDS_IMAGE" \
    config set plsql.gateway.mode proxied
  ```

- Start the serving container:

  ```bash
  podman --connection apex-cicd run -d --name apex-ords --network apex-net \
    -p 127.0.0.1:8080:8080 \
    -v apex-ords-config:/etc/ords/config:z \
    -v apex-images:/opt/oracle/apex/images:ro,z \
    --entrypoint /opt/graalvm-ee-java17/bin/java "$ORDS_IMAGE" \
    -jar /opt/oracle/ords/ords.war --config /etc/ords/config serve
  podman --connection apex-cicd logs --tail 60 apex-ords
  ```

- The direct Java entrypoint receives termination signals as PID 1; the image's default shell entrypoint delayed shutdown during preliminary testing.
- Static assets are read-only in the server.
- The shared :z SELinux label is needed for cross-container volume access.
- No SYS password is supplied to the long-running server.
- Only loopback port 8080 is published.

## 8. Verify access as an operator

Follow the numbered [post-install verification steps and account guide](../progress/E.1/cicd-walkthrough.md#verify-the-installation-before-project-setup). They cover repeatable automated checks, ADMIN browser sign-in, static assets, optional SYSTEM/SQLcl login and log inspection.

1. Run the infrastructure verifier:

   ```bash
   bash scripts/apex-verify.sh
   ```

   To inspect the individual layers directly instead of the combined check:

   ```bash
   podman --connection apex-cicd exec apex-db healthcheck.sh
   podman --connection apex-cicd exec -i apex-db sqlplus -s / as sysdba < scripts/apex-db-verify.sql
   curl --fail --silent --show-error --location --output /dev/null --write-out 'ORDS landing: HTTP %{http_code}\n' http://127.0.0.1:8080/ords/
   curl --fail --silent --show-error http://127.0.0.1:8080/i/apex_version.txt
   ```

2. Expect APEX **24.2 VALID**, zero invalid APEX objects, SYSTEM authenticated through the published host port to **FREEPDB1**, ORDS/login-page **HTTP 200**, matching static assets and the final passed message.
3. Retrieve the locally generated administrator password and open [Administration Services](http://127.0.0.1:8080/ords/apex_admin):

   ```bash
   python3 scripts/cicd-password.py APEX_ADMIN_PASSWORD
   ```

4. Sign in as **ADMIN**, administration workspace **INTERNAL**. Confirm the administration home and styling, then sign out. HTTP 200 alone does not verify credentials.
5. There are no fixed default passwords. The installer generates passwords once in protected `.local-apex/credentials.env` and retains them across lab destruction. SYSTEM/SYS use **ORACLE_PASSWORD**; SYS requires SYSDBA. **ORDS_PASSWORD** is installation/service configuration, not a browser login. Do not publish password values.
6. Project schemas, private workspaces and developer/runtime accounts are created only by the separate onboarding commands below.

## 9. Provisioning boundary for application areas

Current deployment areas are **integration_test / E1_INTEGRATION / 810004** and **user_acceptance_test / E1_UAT / 810005**. These replace the former lab-qualify/E1_QUALIFY and lab-test/E1_TEST identities. They remain separate workspaces/schemas in the same Oracle/APEX installation. Script aliases normalize old connection tokens; use the new saved connection names for direct SQLcl.

The authorized one-time transition on 2026-10-18 stopped the paused D process, preserved native APEX export plus table/control rows under protected `.local-apex/environment-rename-20261018/`, retired its uncompleted attempt with a reason, and recreated only those two disposable areas. Control attempt history and A/B/C work were retained. Target epochs remain monotonic; the integration target's prior epoch is not reset to zero. New source/configuration identities require newly built archives and fresh qualification. The old immutable archives and historical evidence remain; do not edit them or treat them as evidence for the renamed mappings. Do not rerun the transition over unrelated or completed work.

The [repository and pipeline draft](../progress/E.1/repo_layout.md#private-areas-and-assembled-applications) explains how these areas relate to shared source and release delivery. Keep its mappings consistent with this procedure and areas.json.

Infrastructure installation stops at a working Oracle Database/APEX/ORDS runtime. `cicd-walkthrough-apex-init.sh` must not create **any project schemas**, workspaces, developer accounts or delivery-control tables. Project-specific verification is an external test, not part of the generic installer. It checks that all six E1 schemas and five project workspaces are absent after installation.

1. **Project operator:** `bash scripts/cicd-control-init.sh` creates only E1_CTRL and installs control packages. There are no grants to not-yet-provisioned areas.
2. **Privileged provisioning operator:** `bash scripts/cicd-area-provision.sh TARGET` provisions exactly one of lab-dev, lab-dev-b, lab-dev-c, integration_test or user_acceptance_test, using [areas.json](../config/areas.json). It creates that schema/workspace/accounts, grants its delivery interfaces and saves its central operator automation connection. Other areas remain unchanged.
3. **Local walkthrough operator:** `(set -o pipefail; python3 scripts/cicd-password.py E1_DEV_A | bash scripts/cicd-developer-init.sh A --password-stdin)` configures A's private SQLcl profile; use the matching B/C commands in the walkthrough. The password helper reads the protected operator store and pipes only the assigned schema password into setup. Setup checks identity/workspace and performs no project DDL or SYS login.
4. **Walkthrough operator:** `bash scripts/cicd-walkthrough-ready.sh` checks identities/isolation and the empty fresh state, then enables entry to A. This is separate from infrastructure initialization.

The [onboarding walkthrough](../progress/E.1/cicd-walkthrough.md#provision-each-assigned-area) supplies the exact commands, actors, password distinctions and expected outcomes. The operator's protected .local-apex/e1-secrets.json remains separate from developer connection profiles. Normal developer setup never runs the privileged provisioning helper. This single-host lab's role separation does not establish separate OS-user security boundaries.

Qualification reset reprovisions **only integration_test** and restores only its grants. It must not silently rerun every developer/target's onboarding. Reapplying control packages preserves existing grants; target-specific grants belong to area provisioning. Infrastructure lifecycle, project control, developer onboarding and application migrations are distinct operations.

## 10. Stop and restart without deleting data

- For an ordinary stop, shut down the web tier first, then the database, then the VM:

  ```bash
  export CONTAINERS_CONF_OVERRIDE="$PWD/.local-apex/containers.conf"
  podman --connection apex-cicd stop --time 120 apex-ords
  podman --connection apex-cicd stop --time 120 apex-db
  podman machine stop apex-cicd
  podman machine list
  ```

- Expected: apex-cicd is stopped; all volumes, credentials and applications remain.
- Allow up to 120 seconds for each container; Podman terminates a container after its timeout. [apex-stop.sh](../scripts/apex-stop.sh) is the convenience equivalent, stopping both containers before the VM.
- Skip commands for resources already stopped.

- To restart, including after a Mac reboot:

  ```bash
  export CONTAINERS_CONF_OVERRIDE="$PWD/.local-apex/containers.conf"
  bash scripts/apex-vm-start.sh
  podman --connection apex-cicd start apex-db
  podman --connection apex-cicd exec apex-db healthcheck.sh
  ```

- Repeat healthcheck until it succeeds before starting ORDS:

  ```bash
  podman --connection apex-cicd start apex-ords
  podman --connection apex-cicd logs --tail 40 apex-ords
  bash scripts/apex-verify.sh | tee .local-apex/restart-verification.log
  ```

- If the VM is already running, skip its start operation.
- Repeat the HTTP check if ORDS is still initializing. [apex-start.sh](../scripts/apex-start.sh) automates the same ordered start and readiness waits.
- Nothing is configured to start automatically at login.
- A normal restart does not rerun APEX installation, recreate areas or generate passwords.

## 11. Recover an interrupted ORDS installation

- Use this only for a diagnosed interrupted setup, not routine releases.
- A partial setup previously left a corrupt wallet or incomplete procedure allowlist.
- Inspect .local-apex/ords-install.log and container logs first.

- If Wallet Version Not Supported identifies a disposable broken ORDS configuration, retain the logs and any configuration customizations, then remove only that web-tier configuration:

  ```bash
  podman --connection apex-cicd rm --force apex-ords
  podman --connection apex-cicd volume rm apex-ords-config
  podman --connection apex-cicd volume create apex-ords-config
  ```

- Skip container removal if it does not exist.
- Rebuild ORDS with section 7 or the bounded apex-ords-install.sh script. apex-data and the database remain intact.
- This operation replaces the wallet/configuration; preserve custom configuration first.

- For incomplete ORDS database metadata instead, stop ORDS and run the supported repair operation:

  ```bash
  source .local-apex/credentials.env
  source scripts/apex-images.env
  podman --connection apex-cicd stop --time 120 apex-ords
  printf '%s\n' "$ORACLE_PASSWORD" | podman --connection apex-cicd run --rm -i \
    --network apex-net -v apex-ords-config:/etc/ords/config:z \
    -v apex-images:/opt/oracle/apex/images:ro,z "$ORDS_IMAGE" \
    install repair --admin-user SYS --password-stdin \
    > .local-apex/ords-repair.log 2>&1
  tail -n 50 .local-apex/ords-repair.log
  ```

- Only after repair succeeds:

  ```bash
  podman --connection apex-cicd start apex-ords
  bash scripts/apex-verify.sh
  ```

- This infrastructure recovery is separate from the planned application failed-deployment/repair experiment.

## 12. Scoped destruction and fresh reconstruction

### Fresh-demo cleanup while retaining the Podman VM

The requested fresh walkthrough discards all lab data. The destructive command is named `apex-destroy.sh` (formerly `cicd-walkthrough-cleanup.sh`) to make its scope explicit. `bash scripts/apex-destroy.sh` first checks the effective inventory with `python3 scripts/cicd-lab-inventory.py`, refuses unrelated containers sharing lab resources, then performs these named operations only when the resource exists:

1. Stop `apex-ords`, then `apex-db` with `podman --connection apex-cicd stop --time 120 NAME`.
2. Remove each stopped container with `podman --connection apex-cicd rm NAME`.
3. Remove each of `apex-data`, `apex-ords-config`, `apex-images` with `podman --connection apex-cicd volume rm NAME`.
4. Remove `apex-net` with `podman --connection apex-cicd network rm apex-net`.
5. Remove the Podman secret `apex-db-password`; its original credential remains in the protected host file for reconstruction.
6. Verify both containers and all three volumes are absent. Move active drift/preservation pointers and the previous cycle directory into a separate private historical directory; retain the source archives and credentials.

**PASS cleanup** means no database or APEX application/history survives in this lab. The VM and cached images remain available to reduce installation time, and unrelated resources remain untouched. `bash scripts/cicd-walkthrough-apex-init.sh` then performs the fresh installation sequence above. This is a deliberate demo restart; it is not a data-preserving migration or failed-deployment repair.

### Optional removal of the entire named VM


- The Product Owner authorized recreation of the current apex-cicd prototype runtime.
- Removing the VM destroys its database, every private area, retained user_acceptance_test data, control reservations/events, ORDS wallet/configuration and VM-local images.
- Host credentials alone cannot recover that data.

- Before removal, identify what must survive.
- Preserve retained database data and history, APEX source, control records and configuration outside the VM, and establish a usable restore path.
- Application exports exclude business data; a Git checkout alone cannot restore greeting history.
- A validated database backup/restore procedure is not implemented in this prototype yet.
- If retained data must survive and no verified backup exists, stop before removal.
- Use ordinary stop/start instead.
- Disposable fresh-install experiments can proceed when no required data depends on the discarded database.

- Keep .local-apex on the host: it holds credentials, tools, installers, local connection configuration, captures and evidence.
- Inspect the resources in section 1 once more, then perform the scoped teardown:

  ```bash
  export CONTAINERS_CONF_OVERRIDE="$PWD/.local-apex/containers.conf"
  podman --connection apex-cicd stop --time 120 apex-ords
  podman --connection apex-cicd stop --time 120 apex-db
  podman machine stop apex-cicd
  ```

- Skip already stopped or absent resources. Remove the one-shot launch job if it is registered:

  ```bash
  launchctl print "gui/$(id -u)/local.apex-cicd.vm-start"
  launchctl bootout "gui/$(id -u)/local.apex-cicd.vm-start"
  ```

- If print reports no service, there is no job to boot out. Remove only the named VM:

  ```bash
  podman machine rm --force apex-cicd
  podman machine list
  podman system connection list
  ```

- Expected: apex-cicd and its associated connections are gone; podman-machine-default remains. No global prune, system reset or deletion of other VMs is part of this procedure.

- For reconstruction, retain the existing host credentials/helper and repeat sections 3–8.
- Reprovision the declared application areas, reinstall control/application source and restore any retained data using its verified restore path before claiming preservation.
- Existing saved SQLcl connections will only work after their schemas and matching credentials are restored.
- An empty replacement database proves fresh installation, not a data-preserving upgrade.

- Whole-VM removal remains optional and was not needed for the fresh walkthrough. The current fresh-start test uses named container/volume removal and database/APEX reconstruction; its observed results are recorded in E.1 test evidence.

## Repeatable application demonstrations

1. For a **fresh-start demonstration**, use the explicit infrastructure sequence near the top of this document, then the [A–H guide](../progress/E.1/cicd-walkthrough.md). Cleanup deletes every lab application and greeting history; infrastructure installation creates no project areas; explicit onboarding creates the empty areas before A.
2. For **settings-only preparation of an existing C application**, use `bash scripts/cicd-demo-defaults.sh`. This is the former nondestructive preparation operation: it restores Hello/World defaults, backs up configuration and preserves every existing history row. It does not prepare a fresh run.
3. For a **normal retained deployment/upgrade**, do not run fresh-start cleanup. Use the operator release stages and preserve data as required.

## Verification scope and references

- The preliminary deployment established ARM64 images, APEX 24.2.0 VALID with zero invalid objects, SYSTEM authentication through port 1521, ORDS/login HTTP 200, static assets 24.2, an ADMIN browser login and access after full VM stop/restart.
- Historical local evidence is in .local-apex/access-verification.log, restart-verification.log, db-verification.log, ords-repair.log and apex-admin-verified.png.
- These private files may contain session material and are not committed.

- E.1 reused that environment and passed its platform smoke checks.
- For this procedure update, rechecked the resource inventory, both pinned ARM64 image digests, helper version 1.3.2 and database health.
- Reran apex-verify.sh successfully: APEX VALID, zero invalid objects, SYSTEM/FREEPDB1 authentication, ORDS and APEX login HTTP 200, and static assets 24.2.
- Browser authentication was not repeated during this documentation update.
- Fresh installation, ORDS repair and stop/restart commands above are expanded from the adopted lifecycle scripts.
- Their earlier evidence does not constitute a new reconstruction rehearsal.
- New results belong in the current sprint's construction/test records.

- References: [database image documentation](https://github.com/gvenzl/oci-oracle-free), [Oracle ORDS installation guide](https://docs.oracle.com/en/database/oracle/oracle-rest-data-services/25.3/ordig/installing-and-configuring-oracle-rest-data-services.html), [krunkit 1.3.2 release](https://github.com/libkrun/krunkit/releases/tag/v1.3.2), and the [initial technical assessment](cicd-research.md).

## Disposable qualification lifecycle

1. Discover the repository root with `cd "$(git rev-parse --show-toplevel)"`.
2. Inspect release receipts and require idle ownership before resetting qualification:

   ```bash
   python3 scripts/apex_sql.py lab-control deploy/operator/show_release_receipts.sql
   python3 scripts/apex_sql.py lab-control deploy/operator/walkthrough_idle.sql
   ```

3. If an initial experiment failed, inspect its attempt and transcripts first. Only the bound `E1_CTRL.e1_release.retire_disposable_qualification(epoch,hash,reason)` procedure may retire its active qualification attempt. It retains failure/history. There is no automatic user_acceptance_test retirement or recovery.
4. Only when a new empty integration_test area is required, run `python3 scripts/cicd-platform.py reset-integration-test`. This checks the local ownership receipt, removes E1_INTEGRATION through public APEX_INSTANCE_ADMIN and reprovisions only that schema/workspace, its accounts and grants. Other areas are not reprovisioned. The reset helper does not itself acquire deployment ownership; the explicit idle check and operator sequencing are required.
5. Project control is installed separately with `bash scripts/cicd-control-init.sh`. Qualification reset restores only the new integration_test schema's grants through its targeted provisioning operation; no global package/grant bootstrap is needed. Existing control records/epochs remain retained.
6. Continue with the [initial-release operator chapter](../progress/E.1/user_manual.md#initial-release-build-qualify-and-promote). A normal rerun verifies the already qualified result. The current control package also supports an explicitly requested initial reconstruction for patch-baseline qualification: it retains the first qualification receipt and records the reconstruction under a new attempt epoch.

- This procedure preserves retained user_acceptance_test, credentials, release history and unrelated Podman resources. It does not recreate the VM or containers.
- Do not use this disposable-area procedure as a retained-target upgrade or repair mechanism.
