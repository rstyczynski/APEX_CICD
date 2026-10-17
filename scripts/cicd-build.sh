#!/usr/bin/env bash
# One operation: package reviewed Git source. No live export or database write.
set -Eeuo pipefail
cd "$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
python3 scripts/cicd-artifact.py build
