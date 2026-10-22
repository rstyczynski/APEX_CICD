#!/usr/bin/env bash
# Thin E.2 launcher; the same section files also run independently.
set -Eeuo pipefail
ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
cd "$ROOT"
for section in A_prepare B_project C_working_copy D_admission E_findings; do
  bash "scripts/cicd-oracle-lifecycle-$section.sh" "$@"
done
