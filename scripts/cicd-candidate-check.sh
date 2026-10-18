#!/usr/bin/env bash
# Read-only source validation plus transactional unit fixtures in private developer C.
set -Eeuo pipefail
ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
cd "$ROOT"
if [ -n "$(git status --porcelain --untracked-files=all -- apex db deploy config release scripts tests/sql)" ]; then
  echo 'ERROR: commit the reviewed candidate source before validation.' >&2; exit 1
fi
revision="$(git rev-parse HEAD)"
umask 077
mkdir -p .local-apex/releases/candidates
log=".local-apex/releases/candidates/$revision.log"
receipt=".local-apex/releases/candidates/$revision.json"
if [ -e "$receipt" ]; then echo 'ERROR: candidate receipt already exists; retain it and inspect before repeating.' >&2; exit 1; fi
{
  echo "CANDIDATE SOURCE: $revision"
  python3 scripts/apex_sql.py lab-dev-c deploy/checks/published_development.sql
  bash tests/run.sh --unit
  manifest=release/manifest.json
  [ -f "$manifest" ] || manifest=release/initial.json
  if rg -q '"stage": "complete-patch"' "$manifest"; then
    python3 scripts/apex_sql.py lab-dev-c deploy/checks/patch_development.sql
    python3 scripts/apex_sql.py lab-dev-c tests/sql/hello_patch.sql
  fi
} 2>&1 | tee "$log"
python3 - "$revision" "$log" "$receipt" <<'PY'
import hashlib,json,sys
from pathlib import Path
revision,log,receipt=sys.argv[1:]
Path(receipt).write_text(json.dumps({'source_commit':revision,'status':'passed','scope':'development integrity and transactional UT-1/UT-2; separate from fresh archive integration_test','log_sha256':hashlib.sha256(Path(log).read_bytes()).hexdigest()},indent=2)+'\n')
PY
echo "CANDIDATE PASSED: $receipt. Integrate locally before building the release."
