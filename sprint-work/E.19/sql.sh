#!/usr/bin/env bash
# One SQLcl invocation; Actions owns sequencing and all lifecycle decisions.
set -euo pipefail
connection=$1
label=$2
mkdir -p "$GITHUB_WORKSPACE/result"
"$SQL_EXE" -version > "$GITHUB_WORKSPACE/result/tool.txt" 2>&1
config=.dbtools/project.config.json
if [[ ! -f "$config" ]]; then config="$GITHUB_WORKSPACE/toolchain.json"; fi
INPUT_LOG="$GITHUB_WORKSPACE/result/tool.txt" INPUT_CONFIG="$config" node "$GITHUB_WORKSPACE/actions/checks.cjs" tool
input=$(mktemp "$RUNNER_TEMP/native-input.XXXXXX")
trap 'rm -f "$input"' EXIT
{
  printf '%s\n' 'whenever sqlerror exit failure rollback' 'whenever oserror exit failure rollback'
  if [[ "$connection" != - ]]; then printf 'connect -name %s\n' "$connection"; fi
  cat
  printf '\nexit\n'
} > "$input"
timeout 240 "$SQL_EXE" -home "$RUNNER_TEMP/private-sqlcl" -nohistory -noupdates -S -L /nolog < "$input" 2>&1 | tee "$GITHUB_WORKSPACE/result/$label.log"
INPUT_LOG="$GITHUB_WORKSPACE/result/$label.log" node "$GITHUB_WORKSPACE/actions/checks.cjs" output
