#!/usr/bin/env bash
# Thin A–I launcher; operations remain in individually runnable chapter scripts.
set -Eeuo pipefail
ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
cd "$ROOT"
MODE="${1:---live}"
case "$MODE" in
  --live|--preflight|--rehearse) ;;
  *) echo 'Usage: bash scripts/cicd-walkthrough.sh [--live|--preflight|--rehearse]' >&2; exit 2 ;;
esac
if [ "$#" -gt 1 ]; then echo 'Only one mode is accepted.' >&2; exit 2; fi
if [ "$MODE" = --live ] && [ ! -t 0 ]; then echo 'ERROR: use an interactive terminal for Product Owner checkpoints.' >&2; exit 2; fi
stages=(
  scripts/cicd-walkthrough-A_foundation.sh
  scripts/cicd-walkthrough-B_hello.sh
  scripts/cicd-walkthrough-C_world.sh
  scripts/cicd-walkthrough-D_integration_test.sh
  scripts/cicd-walkthrough-E_promotion.sh
  scripts/cicd-walkthrough-F_hello_patch.sh
  scripts/cicd-walkthrough-G_incompatible_upgrade.sh
  scripts/cicd-walkthrough-H_drift.sh
  scripts/cicd-walkthrough-I_repair.sh
)
# Check all chapter/file references first. Cleanup remains a separate operator action.
bash scripts/apex-destroy.sh --preflight
for stage in "${stages[@]}"; do bash "$stage" --preflight; done
if [ "$MODE" = --preflight ]; then exit 0; fi
echo 'PREREQUISITE: complete precheck, host preparation, destructive cleanup, infrastructure-only APEX installation and explicit project/area onboarding/readiness from the manual.'
for stage in "${stages[@]}"; do bash "$stage" "$MODE"; done
echo 'PASS selected fresh walkthrough: construction, initial integration_test/promotion, Hello patch, this-cycle preservation, incompatible proposal rejection, drift rejection/restoration and bounded additive-failure repair.'
echo 'OPEN E.1 WORK: broader concurrency, complete maintenance fencing, general schema-drift coverage and arbitrary-state repair. No sprint closure claimed.'
