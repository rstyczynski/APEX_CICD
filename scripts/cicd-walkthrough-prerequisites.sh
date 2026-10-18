#!/usr/bin/env bash
# docs/deploy.md sections 1–4: check host tools and verified installers before cleanup.
set -Eeuo pipefail
command -v git >/dev/null || { echo 'MISSING prerequisite: git' >&2; exit 1; }
ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
cd "$ROOT"
[ "$#" -eq 0 ] || { echo 'Usage: bash scripts/cicd-walkthrough-prerequisites.sh' >&2; exit 2; }
[ "$(uname -s)" = Darwin ] && [ "$(uname -m)" = arm64 ] || { echo 'ERROR: this lab requires macOS Apple Silicon.' >&2; exit 1; }
for tool in git podman python3 curl openssl unzip shasum tar rg launchctl codesign install_name_tool; do
  command -v "$tool" >/dev/null || { echo "MISSING prerequisite: $tool" >&2; exit 1; }
  echo "OK tool: $tool"
done
podman --version
podman machine list
if podman --connection apex-cicd info >/dev/null 2>&1; then
  echo 'Existing named engine inventory:'
  podman --connection apex-cicd ps -a
  python3 scripts/cicd-lab-inventory.py
else
  echo 'Named engine is stopped/absent: initialize it in the next explicit host step.'
fi
# Read-only prerequisite validation. Install missing tools through docs/deploy.md first.
for file in .local-apex/tools/sqlcl/bin/sql .local-apex/tools/jdk-21.0.12.1+1/Contents/Home/bin/java .local-apex/helper/bin/krunkit .local-apex/containers.conf .local-apex/apex_24.2.zip; do
  test -r "$file" || { echo "MISSING prerequisite: $file; follow docs/deploy.md before cleanup." >&2; exit 1; }
done
printf '%s  %s\n' 4ce293bc11685050ea37baa3abac986018746df4baea492cdb8deaebee7e8ba7 .local-apex/tools/sqlcl-25.3.0.274.1210.zip | shasum -a 256 -c -
printf '%s  %s\n' 3623232f33a9c3baadf304480b2535f9a3cba8a58d42ecbb438ba267315d9998 .local-apex/tools/java21.tar.gz | shasum -a 256 -c -
source scripts/cicd-env.sh
sql_version="$(sql -version)"
printf '%s\n' "$sql_version"
printf '%s\n' "$sql_version" | rg -Fq '25.3.0.274.1210'
java_version="$("$JAVA_HOME/bin/java" -version 2>&1)"
printf '%s\n' "$java_version"
printf '%s\n' "$java_version" | rg -Fq '21.0.12.1+1'
helper_version="$(.local-apex/helper/bin/krunkit --version)"
printf '%s\n' "$helper_version"
printf '%s\n' "$helper_version" | rg -Fq '1.3.2'
printf '%s  %s\n' a7ad0ba94f70b2d581f7dde97fe27cd07afc98c32ecc146d89fd70cce9b76456 .local-apex/apex_24.2.zip | shasum -a 256 -c -
# Both reviewed releases must be available before discarding the current database.
for pointer in initial-selected patch-selected; do
  archive="$(cat ".local-apex/releases/$pointer.txt")"
  python3 scripts/cicd-artifact.py inspect "$archive"
done
for revision in e9a490f f511ab8; do git cat-file -e "$revision:apex/f810001/install.sql"; done
df -h .
# Inspect APEX only when an existing named database is healthy. Absence is valid before install.
if podman --connection apex-cicd info >/dev/null 2>&1 && podman --connection apex-cicd container exists apex-db; then
  if podman --connection apex-cicd exec apex-db healthcheck.sh >/dev/null 2>&1; then
    echo 'OPERATION: inspect existing APEX registry through the named database (read-only).'
    installed="$(podman --connection apex-cicd exec -i apex-db sqlplus -s / as sysdba < deploy/operator/walkthrough_infrastructure.sql)"
    printf '%s\n' "$installed"
    printf '%s\n' "$installed" | rg -q '^PRECHECK_APEX_INFO_COMPLETE\r?$'
  else
    echo 'Existing named database is stopped/unhealthy; SQL inspection skipped. Treat as partial runtime for explicit cleanup.'
  fi
else
  echo 'No running named database to inspect. Fresh installation follows host preparation/cleanup.'
fi
echo 'PASS prerequisites: host tools, pinned SQLcl/Java, helper, APEX installer and reviewed release inputs.'
