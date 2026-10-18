#!/usr/bin/env bash
set -euo pipefail
cd "$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
source .local-apex/credentials.env
# Avoid SQL*Plus ACCEPT ... HIDE: it does not reliably read piped stdin.
# Generated passwords contain only letters, digits, underscore and # (no SQL quotes).
{
  printf '%s\n' 'whenever oserror exit failure rollback' 'whenever sqlerror exit failure rollback' \
    'set echo off verify off define off' 'alter session set container=FREEPDB1;'
  printf "begin apex_instance_admin.create_or_update_admin_user(p_username=>'ADMIN',p_email=>'admin@localhost',p_password=>'%s'); commit; end;\n/\n" "$APEX_ADMIN_PASSWORD"
  printf '@apex_rest_config_core.sql ./ %s %s\n' "$ORDS_PASSWORD" "$ORDS_PASSWORD"
  printf '%s\n' \
    'alter user ANONYMOUS account unlock;' \
    'alter user APEX_PUBLIC_USER account unlock;' 'exit'
} | podman --connection apex-cicd exec -i --workdir /tmp/apex apex-db sqlplus -s / as sysdba
