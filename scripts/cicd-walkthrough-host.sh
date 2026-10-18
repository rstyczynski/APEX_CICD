#!/usr/bin/env bash
# docs/deploy.md sections 2–3: initialize/reuse only the named host.
set -Eeuo pipefail
ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
cd "$ROOT"
[ "$#" -eq 0 ] || { echo 'Usage: bash scripts/cicd-walkthrough-host.sh' >&2; exit 2; }
export CONTAINERS_CONF_OVERRIDE="$ROOT/.local-apex/containers.conf"
if ! podman machine inspect apex-cicd >/dev/null 2>&1; then
  podman machine init --cpus 4 --memory 6144 --disk-size 30 apex-cicd
fi
if ! podman --connection apex-cicd info >/dev/null 2>&1; then bash scripts/apex-vm-start.sh; fi
podman --connection apex-cicd info
podman --connection apex-cicd ps -a
source scripts/apex-images.env
podman --connection apex-cicd pull "$DB_IMAGE"
podman --connection apex-cicd pull "$ORDS_IMAGE"
echo 'PASS host: named apex-cicd engine ready; pinned images available. Other VMs untouched.'
