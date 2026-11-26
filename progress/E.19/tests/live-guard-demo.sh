#!/usr/bin/env bash
set -euo pipefail
node fixtures.cjs provenance valid
out=$(mktemp)
trap 'rm -f "$out"' EXIT
export GITHUB_OUTPUT="$out"
export INPUT_ARCHIVE=fixtures/archive INPUT_RECEIPT=fixtures/receipt
export INPUT_SOURCE=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa INPUT_BUILD=25.4.1.022.0618
printf '%s\n' 'DEMO valid receipt binds expected source/build and exact archive bytes'
node actions/provenance/index.cjs
cat "$out"
printf '%s\n' 'DEMO substitute archive bytes; rejected guard must prevent the next step'
printf 'substituted' >> fixtures/archive
if node actions/provenance/index.cjs && touch fixtures/forbidden-demo-mutation; then
  printf '%s\n' 'FAIL rejection absent'; exit 1
fi
test ! -e fixtures/forbidden-demo-mutation
printf '%s\n' 'PASS substituted archive refused and mutation absent'
printf '%s\n' 'DEMO restore correct producer output and retry'
node fixtures.cjs provenance valid
node actions/provenance/index.cjs
printf '%s\n' 'PASS recovery with original validated evidence'
