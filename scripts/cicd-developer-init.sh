#!/usr/bin/env bash
# Developer workstation setup: own password/connection only, no SYS access or DDL.
set -Eeuo pipefail
cd "$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
exec python3 scripts/cicd-developer-configure.py "$@"
