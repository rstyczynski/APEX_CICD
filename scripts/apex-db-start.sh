#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
source .local-apex/credentials.env
source scripts/apex-images.env
p() { podman --connection apex-cicd "$@"; }
if p container exists apex-db; then
  echo 'apex-db already exists. Use podman start for a restart, or the documented full reset.' >&2
  exit 1
fi
p network create apex-net
p volume create apex-data
p volume create apex-ords-config
p volume create apex-images
printf '%s' "$ORACLE_PASSWORD" | p secret create apex-db-password -
p run -d --name apex-db --network apex-net \
  -p 127.0.0.1:1521:1521 \
  --secret apex-db-password \
  -e ORACLE_PASSWORD_FILE=/run/secrets/apex-db-password \
  -v apex-data:/opt/oracle/oradata \
  -v apex-images:/opt/apex-images:z "$DB_IMAGE"
for ((attempt=0; attempt<180; attempt++)); do
  if p exec apex-db healthcheck.sh >/dev/null 2>&1; then
    echo 'Database ready.'
    exit 0
  fi
  sleep 5
done
p logs --tail 80 apex-db
echo 'Database was not ready within 15 minutes.' >&2
exit 1
