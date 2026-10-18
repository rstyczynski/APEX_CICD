#!/usr/bin/env bash
# docs/deploy.md sections 4–9: fresh database, APEX, ORDS, empty application areas.
set -Eeuo pipefail
ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
cd "$ROOT"
[ "$#" -eq 0 ] || { echo 'Usage: bash scripts/cicd-walkthrough-apex-init.sh' >&2; exit 2; }
p() { printf 'OPERATION: podman --connection apex-cicd'; printf ' %q' "$@"; printf '\n'; podman --connection apex-cicd "$@"; }
podman --connection apex-cicd info >/dev/null
for resource in apex-data apex-ords-config apex-images; do
 if podman --connection apex-cicd volume exists "$resource"; then echo "ERROR: $resource exists; complete explicit cleanup first." >&2; exit 1; fi
done
for container in apex-db apex-ords; do
 if podman --connection apex-cicd container exists "$container"; then echo "ERROR: $container exists; complete explicit cleanup first." >&2; exit 1; fi
done
umask 077
if [ ! -f .local-apex/credentials.env ]; then
 printf 'ORACLE_PASSWORD=Aa1_%s\nAPEX_ADMIN_PASSWORD=Aa1#%s\nORDS_PASSWORD=Aa1_%s\n' "$(openssl rand -hex 16)" "$(openssl rand -hex 16)" "$(openssl rand -hex 16)" > .local-apex/credentials.env
fi
chmod 600 .local-apex/credentials.env
printf '%s  %s\n' a7ad0ba94f70b2d581f7dde97fe27cd07afc98c32ecc146d89fd70cce9b76456 .local-apex/apex_24.2.zip | shasum -a 256 -c -
bash scripts/apex-db-start.sh
p cp .local-apex/apex_24.2.zip apex-db:/tmp/apex_24.2.zip
p exec --user root apex-db bash -c 'cd /tmp && unzip -q apex_24.2.zip && chown -R oracle:oinstall /tmp/apex'
echo 'OPERATION: install APEX using scripts/apex-db-install.sql; full output in .local-apex/apex-install.log'
podman --connection apex-cicd exec -i --workdir /tmp/apex apex-db sqlplus -s / as sysdba < scripts/apex-db-install.sql > .local-apex/apex-install.log 2>&1
if rg -n '^ORA-[0-9]+:|^SP2-[0-9]+:' .local-apex/apex-install.log; then echo 'ERROR: inspect APEX installation log.' >&2; exit 1; fi
bash scripts/apex-configure.sh
bash scripts/apex-ords-install.sh > .local-apex/ords-install.log 2>&1
bash scripts/apex-start.sh
bash scripts/apex-verify.sh
python3 scripts/cicd-platform.py bootstrap
python3 scripts/apex_sql.py lab-control deploy/control.sql
python3 scripts/apex_sql.py lab-control deploy/release_control.sql
python3 scripts/cicd-platform.py check
# Probe rows are explicit infrastructure isolation tests, not greeting/business data.
python3 scripts/cicd-platform.py isolation
python3 scripts/cicd-platform.py check-empty
mkdir -p .local-apex/walkthrough
mkdir .local-apex/walkthrough/current
echo 'PASS APEX init: fresh verified runtime, isolated empty areas and control authority. No lab application or greeting history installed. Ready for A.'
