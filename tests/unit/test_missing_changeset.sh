#!/usr/bin/env bash
# Offline review regression: exercise the actual native-log and receipt assertions.
test_missing_changeset_diagnostics() (
  set -euo pipefail
  root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)
  scratch=$(mktemp -d "${TMPDIR:-/tmp}/e3-missing-log.XXXXXX")
  trap 'rm -rf "$scratch"' EXIT
  parser="$root/examples/git-pipeline/.github/assert-missing-changeset.awk"
  receipt_filter="$root/examples/git-pipeline/.github/qualification-receipt.jq"
  expected=dist/releases/next/changes/e3-initial/e1_dev_c/package_bodies/lab_runtime.sql
  source=fbda57a0cbe4d32961ad826852bd04394a500c11
  count=0
  check_log() {
    local wanted=$1 name=$2 file=$3 result=reject
    if awk -v expected="$expected" -f "$parser" "$file" > "$scratch/output" 2>&1; then result=accept; fi
    test "$result" = "$wanted" || { printf 'FAIL %s: %s\n' "$name" "$result"; cat "$scratch/output"; return 1; }
    count=$((count+1)); printf 'PASS %s\n' "$name"
  }
  check_receipt() {
    local wanted=$1 name=$2 file=$3 run=$4 result=reject
    if jq -e --arg source "$source" --arg run "$run" --arg expected_missing "$expected" -f "$receipt_filter" "$file" > "$scratch/output" 2>&1; then result=accept; fi
    test "$result" = "$wanted" || { printf 'FAIL %s: %s\n' "$name" "$result"; cat "$scratch/output"; return 1; }
    count=$((count+1)); printf 'PASS %s\n' "$name"
  }
  check_log accept retained-missing-file "$root/progress/E.3/tests/github-native-rejection.log"
  check_log reject retained-positive "$root/progress/E.3/tests/github-native-verify.log"
  cat > "$scratch/valid" <<EOF
Errors: 1
  ERROR stage stagechangelogfilesvalid format: liquibase
    There is one missing file out of 26:
    Included in dist/releases/next/changes/e3-initial/stage.changelog.xml:
    $expected
  INFO stage stagechangelogcomplete No issues
EOF
  check_log accept bounded-format "$scratch/valid"
  sed 's/ERROR stage stagechangelogfilesvalid/ERROR project sqlclversion/' "$scratch/valid" > "$scratch/unrelated"
  printf 'INFO stage stagechangelogfilesvalid All scripts present\n' >> "$scratch/unrelated"
  check_log reject unrelated-error-with-INFO-rule "$scratch/unrelated"
  sed 's/lab_runtime.sql/lab_runtimeXsql/' "$scratch/valid" > "$scratch/wrong"
  check_log reject literal-wrong-path "$scratch/wrong"
  printf 'INFO other rule\n%s\n' "$expected" >> "$scratch/wrong"
  check_log reject expected-path-outside-error-block "$scratch/wrong"
  sed 's/Errors: 1/Errors: 0/' "$scratch/valid" > "$scratch/zero"
  check_log reject zero-error-summary "$scratch/zero"
  sed '/Errors:/d' "$scratch/valid" > "$scratch/incomplete"
  check_log reject missing-summary "$scratch/incomplete"
  printf 'Connection failed\nORA-01017\n' > "$scratch/connection"
  check_log reject connection-failure "$scratch/connection"
  sed 's/Errors: 1/Errors: 2/' "$scratch/valid" > "$scratch/count"
  check_log reject inconsistent-error-count "$scratch/count"
  printf 'Errors: 1\n' >> "$scratch/count"
  check_log reject conflicting-summaries "$scratch/count"
  sed '/There is one missing file/d' "$scratch/valid" > "$scratch/no-message"
  check_log reject missing-diagnostic-message "$scratch/no-message"
  sed 's/Errors: 1/Errors: 2/' "$scratch/valid" > "$scratch/two"
  printf 'ERROR project sqlclversion Wrong version\n' >> "$scratch/two"
  check_log reject additional-unrelated-error "$scratch/two"
  awk '{printf "\033[31m%s\033[0m    \n", $0}' "$scratch/valid" > "$scratch/ansi"
  check_log accept ANSI-and-padding "$scratch/ansi"
  sed 's@package_bodies/lab_runtime.sql@package_bodies/\
    lab_runtime.sql@' "$scratch/valid" > "$scratch/wrapped"
  check_log accept path-continuation "$scratch/wrapped"

  check_receipt accept pinned-legacy-receipt "$root/progress/E.3/tests/github-qualification.json" 41679432928
  check_receipt reject unrecognized-legacy-run "$root/progress/E.3/tests/github-qualification.json" 42
  jq --arg missing "$expected" --arg controller "$source" \
    '. + {verification_schema:2,missing_changeset:$missing,controller_sha:$controller,sqlcl_version_output:"SQLcl qualified fixture"}' \
    "$root/progress/E.3/tests/github-qualification.json" > "$scratch/receipt"
  check_receipt accept new-format-receipt "$scratch/receipt" 41679432928
  jq '.missing_changeset="dist/another.sql"' "$scratch/receipt" > "$scratch/wrong-receipt"
  check_receipt reject receipt-path-mismatch "$scratch/wrong-receipt" 41679432928
  jq 'del(.missing_changeset)' "$scratch/receipt" > "$scratch/incomplete-receipt"
  check_receipt reject new-format-missing-path "$scratch/incomplete-receipt" 41679432928
  jq 'del(.controller_sha)' "$scratch/receipt" > "$scratch/no-controller"
  check_receipt reject missing-controller-identity "$scratch/no-controller" 41679432928
  printf 'Checks: %s; failed: 0; offline only\n' "$count"
)
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then test_missing_changeset_diagnostics; fi
