#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export CONTAINERS_CONF_OVERRIDE="$PWD/.local-apex/containers.conf"
podman --connection apex-cicd stop --time 120 apex-ords apex-db
podman machine stop apex-cicd
