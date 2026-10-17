#!/usr/bin/env bash
set -euo pipefail
cd "$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
p() { podman --connection apex-cicd "$@"; }
if ! p info >/dev/null 2>&1; then bash scripts/apex-vm-start.sh; fi
p start apex-db
ready=false
for ((attempt=0; attempt<180; attempt++)); do
  if p exec apex-db healthcheck.sh >/dev/null 2>&1; then ready=true; break; fi
  sleep 2
done
if [ "$ready" != true ]; then echo 'Database startup timed out.' >&2; exit 1; fi
p start apex-ords
for ((attempt=0; attempt<90; attempt++)); do
  if curl -fsS http://127.0.0.1:8080/ords/ >/dev/null 2>&1; then
    echo 'APEX available at http://127.0.0.1:8080/ords/'
    exit 0
  fi
  sleep 2
done
echo 'ORDS startup timed out; inspect podman logs apex-ords.' >&2
exit 1
