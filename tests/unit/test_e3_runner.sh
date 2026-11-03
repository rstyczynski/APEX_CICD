#!/usr/bin/env bash
# Offline regression checks for actionable runner diagnostics.
set -euo pipefail
root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)
temporary=$(mktemp -d "${TMPDIR:-/tmp}/e3-runner-check.XXXXXX")
trap 'rm -rf "$temporary"' EXIT
mkdir -p "$temporary/bin" "$temporary/runner"
cat > "$temporary/bin/gh" <<'SH'
#!/usr/bin/env bash
case "$*" in
  *variables/DB_CONNECT*) echo '127.0.0.1:1521/FREEPDB1' ;;
  *variables/ORDS_URL*) echo 'http://127.0.0.1:8080/ords' ;;
  *actions/runners*) echo '[]' ;;
  *) exit 99 ;;
esac
SH
cat > "$temporary/bin/nc" <<'SH'
#!/usr/bin/env bash
exit 1
SH
chmod +x "$temporary/bin/gh" "$temporary/bin/nc"
export PATH="$temporary/bin:$PATH"
launcher="$root/scripts/e3-runner.sh"
repository=example/APEX_CICD_E3_LAB

if bash "$launcher" status --repo invalid --directory "$temporary/runner" > "$temporary/result" 2>&1; then
  echo 'FAIL: invalid repository accepted'; exit 1
fi
grep -q 'Use --repo OWNER/REPO' "$temporary/result"

echo '{"gitHubUrl":"https://github.com/example/SEED"}' > "$temporary/runner/.runner"
if bash "$launcher" setup --repo "$repository" --directory "$temporary/runner" > "$temporary/result" 2>&1; then
  echo 'FAIL: unrelated registration accepted'; exit 1
fi
grep -q 'does not match example/APEX_CICD_E3_LAB' "$temporary/result"
grep -q 'separate --directory' "$temporary/result"

printf '{"gitHubUrl":"https://github.com/%s"}\n' "$repository" > "$temporary/runner/.runner"
bash "$launcher" status --repo "$repository" --directory "$temporary/runner" > "$temporary/result" 2>&1
grep -q 'GitHub runners for example/APEX_CICD_E3_LAB' "$temporary/result"
grep -q '\[\]' "$temporary/result"

if bash "$launcher" setup --repo "$repository" --directory "$temporary/runner" > "$temporary/result" 2>&1; then
  echo 'FAIL: failed Oracle connection accepted'; exit 1
fi
grep -q 'Oracle TCP connection failed: 127.0.0.1:1521' "$temporary/result"
echo 'PASS: invalid repository, mismatched registration, empty status and Oracle failure diagnostics.'
