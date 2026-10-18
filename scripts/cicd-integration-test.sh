#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
[ "$#" -eq 1 ] || { echo 'Usage: bash scripts/cicd-integration-test.sh ARCHIVE' >&2; exit 2; }
exec bash "$ROOT/scripts/cicd-deliver-initial.sh" "$1" integration_test
