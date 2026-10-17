#!/usr/bin/env bash
set -euo pipefail
cd "$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
export CONTAINERS_CONF_OVERRIDE="$PWD/.local-apex/containers.conf"
podman --connection apex-cicd stop --time 120 apex-ords apex-db
podman machine stop apex-cicd
