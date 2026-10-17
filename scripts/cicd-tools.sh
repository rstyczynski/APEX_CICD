#!/usr/bin/env bash
set -euo pipefail
cd "$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
mkdir -p .local-apex/tools
fetch() {
  local name=$1 url=$2 sha=$3
  if [[ ! -f ".local-apex/tools/$name" ]]; then
    curl -fL --retry 3 -o ".local-apex/tools/$name" "$url"
  fi
  printf '%s  %s\n' "$sha" ".local-apex/tools/$name" | shasum -a 256 -c -
}
fetch sqlcl-25.3.0.274.1210.zip \
  https://download.oracle.com/otn_software/java/sqldeveloper/sqlcl-25.3.0.274.1210.zip \
  4ce293bc11685050ea37baa3abac986018746df4baea492cdb8deaebee7e8ba7
fetch java21.tar.gz \
  'https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.12.1%2B1/OpenJDK21U-jdk_aarch64_mac_hotspot_21.0.12.1_1.tar.gz' \
  3623232f33a9c3baadf304480b2535f9a3cba8a58d42ecbb438ba267315d9998
python3 - <<'PY'
from pathlib import Path
import tarfile, zipfile
p=Path('.local-apex/tools')
if not (p/'sqlcl/bin/sql').exists():
    with zipfile.ZipFile(p/'sqlcl-25.3.0.274.1210.zip') as z: z.extractall(p)
if not (p/'jdk-21.0.12.1+1/Contents/Home/bin/java').exists():
    with tarfile.open(p/'java21.tar.gz') as t: t.extractall(p,filter='data')
(p/'sqlcl/bin/sql').chmod(0o755)
(p/'sqlcl-home').mkdir(mode=0o700,exist_ok=True)
PY
python3 scripts/apex_sql.py --version
