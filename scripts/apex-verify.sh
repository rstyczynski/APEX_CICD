#!/usr/bin/env bash
set -euo pipefail
cd "$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
source .local-apex/credentials.env
p() { podman --connection apex-cicd "$@"; }
p exec -i apex-db sqlplus -s / as sysdba < scripts/apex-db-verify.sql
# Connect back through the published host port, rather than OS authentication.
{
  printf '%s\n' 'whenever oserror exit failure' 'whenever sqlerror exit sql.sqlcode'
  printf 'connect SYSTEM/%s@//host.containers.internal:1521/FREEPDB1\n' "$ORACLE_PASSWORD"
  printf '%s\n' "select user, sys_context('USERENV','CON_NAME') as pdb from dual;" 'exit'
} | p exec -i apex-db sqlplus -s /nolog
curl --fail --silent --show-error --location --output /dev/null \
  --write-out 'ORDS landing: HTTP %{http_code}\n' http://127.0.0.1:8080/ords/
# APEX needs a cookie jar when following its session redirects.
curl --fail --silent --show-error --location \
  --cookie-jar .local-apex/verify-cookies.txt --cookie .local-apex/verify-cookies.txt \
  --output .local-apex/apex-login.html --write-out 'APEX login: HTTP %{http_code}\n' \
  http://127.0.0.1:8080/ords/apex_admin
rg -q 'Oracle APEX Administration Services' .local-apex/apex-login.html
curl --fail --silent --show-error http://127.0.0.1:8080/i/apex_version.txt |
  tee .local-apex/apex-version.txt
rg -q '24\.2' .local-apex/apex-version.txt
echo
echo 'Database SQL, ORDS, APEX sign-in and static version checks passed.'
