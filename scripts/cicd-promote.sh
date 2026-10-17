#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
[ "$#" -eq 2 ] && [ "$2" = lab-test ] || { echo 'Usage: bash scripts/cicd-promote.sh ARCHIVE lab-test' >&2; exit 2; }
exec bash "$ROOT/scripts/cicd-deliver-initial.sh" "$1" "$2"
