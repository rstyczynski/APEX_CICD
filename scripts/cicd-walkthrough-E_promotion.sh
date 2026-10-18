#!/usr/bin/env bash
# Result stage paired with progress/E.1/cicd-walkthrough.md.
source "$(dirname "${BASH_SOURCE[0]}")/cicd-walkthrough-common.sh"
prepare_stage '## E. Promote the same initial artifact to TEST' \
  'scripts/cicd-artifact.py' \
  'deploy/operator/show_initial_proof.sql'
archive="$(cat .local-apex/releases/initial-selected.txt)"
initial_hash="$(shasum -a 256 "$archive" | awk '{print $1}')"
pause 'Press any key to verify the retained initial TEST promotion receipt; q to quit.'
python3 scripts/cicd-artifact.py inspect "$archive"
check_result lab-control "@\"$ROOT/deploy/operator/show_initial_proof.sql\" $initial_hash"
echo 'VERIFIED HISTORICAL RESULT: the verified TEST epoch-1 receipt has the same initial archive hash.'
echo 'PRODUCT OWNER: open http://127.0.0.1:8080/ords/f?p=810005:1 as LAB_USER; it now runs 1.0.1.'
pause 'View TEST, then press any key for current patch verification; q to quit.'
echo 'PASS result stage E_promotion.'
