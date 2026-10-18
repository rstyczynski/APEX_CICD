#!/usr/bin/env bash
# docs/deploy.md section 12: discard ALL database/APEX state in the owned lab.
set -Eeuo pipefail
ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
cd "$ROOT"
MODE="${1:---run}"
case "$MODE" in --run|--preflight) ;; *) echo 'Usage: bash scripts/apex-destroy.sh [--run|--preflight]' >&2; exit 2 ;; esac
[ "$#" -le 1 ]
command -v podman >/dev/null
command -v python3 >/dev/null
test -r scripts/cicd-lab-inventory.py
if [ "$MODE" = --preflight ]; then echo 'OK: APEX destruction files/tools found; no database or Podman mutation.'; exit 0; fi
# Never treat an unreachable engine as an absent installation.
podman --connection apex-cicd info >/dev/null
python3 scripts/cicd-lab-inventory.py
p() { printf 'OPERATION: podman --connection apex-cicd'; printf ' %q' "$@"; printf '\n'; podman --connection apex-cicd "$@"; }
echo 'DESTROY: deleting ALL A/B/C, qualification and TEST applications, entries, settings, greeting history and database control receipts.'
for container in apex-ords apex-db; do
  if podman --connection apex-cicd container exists "$container"; then
    p stop --time 120 "$container"
    p rm "$container"
  fi
done
for volume in apex-data apex-ords-config apex-images; do
  if podman --connection apex-cicd volume exists "$volume"; then p volume rm "$volume"; fi
done
if podman --connection apex-cicd network exists apex-net; then p network rm apex-net; fi
if podman --connection apex-cicd secret inspect apex-db-password >/dev/null 2>&1; then p secret rm apex-db-password; fi
# Host evidence is historical, never a substitute for fresh database receipts.
umask 077
mkdir -p .local-apex/walkthrough
previous="$(mktemp -d "$ROOT/.local-apex/walkthrough/previous.XXXXXX")"
for file in drift-active.json test-initial-preservation.json qualification-initial-preservation.json; do
  if [ -e ".local-apex/releases/$file" ]; then mv ".local-apex/releases/$file" "$previous/"; fi
done
if [ -e .local-apex/walkthrough/current ]; then mv .local-apex/walkthrough/current "$previous/cycle"; fi
for container in apex-db apex-ords; do
  if podman --connection apex-cicd container exists "$container"; then echo "ERROR: $container remains" >&2; exit 1; fi
done
for volume in apex-data apex-ords-config apex-images; do
  if podman --connection apex-cicd volume exists "$volume"; then echo "ERROR: $volume remains" >&2; exit 1; fi
done
echo 'PASS destroy: owned database/APEX/ORDS data removed; no greeting history or applications survive in the lab.'
echo 'Retained on host: credentials, tools, installers, source archives and historical evidence. VM/images and unrelated resources retained.'
