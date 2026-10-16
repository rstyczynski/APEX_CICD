#!/usr/bin/env bash
set -uo pipefail
cd "$(dirname "$0")/.."
suite=''
manifest=tests/manifests/component_delivery.manifest
while (($#)); do
  case "$1" in
    --smoke|--unit|--integration) suite=${1#--}; shift ;;
    --new-only) manifest=$2; shift 2 ;;
    --component) manifest="tests/manifests/component_$2.manifest"; shift 2 ;;
    *) echo "Unknown test option: $1" >&2; exit 2 ;;
  esac
done
[[ -n "$suite" && -f "$manifest" ]] || { echo 'Specify a suite and an existing manifest.' >&2; exit 2; }
count=0
failed=0
while IFS=: read -r level script function; do
  [[ "$level" == "$suite" ]] || continue
  [[ "$script" =~ ^test_[a-z_]+\.sh$ && "$function" =~ ^test_[A-Za-z0-9_]+$ ]] || { echo 'Invalid manifest entry' >&2; exit 2; }
  count=$((count+1))
  echo "RUN $level:$script:$function"
  ( set -e; source "tests/$level/$script"; "$function" )
  result=$?
  if ((result==0)); then
    echo "PASS $function"
  else
    echo "FAIL $function"
    failed=$((failed+1))
  fi
done < "$manifest"
echo "Tests: $count; failed: $failed"
((count>0 && failed==0))
