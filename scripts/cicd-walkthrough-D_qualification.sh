#!/usr/bin/env bash
# Result stage paired with progress/E.1/cicd-walkthrough.md.
source "$(dirname "${BASH_SOURCE[0]}")/cicd-walkthrough-common.sh"
prepare_stage '## D. Qualify the initial release' \
  'scripts/cicd-artifact.py' \
  'deploy/operator/show_initial_proof.sql'
archive="$(cat .local-apex/releases/initial-selected.txt)"
initial_hash="$(shasum -a 256 "$archive" | awk '{print $1}')"
pause 'Press any key to verify the retained initial archive/receipts; q to quit.'
python3 scripts/cicd-artifact.py inspect "$archive"
check_result lab-control "@\"$ROOT/deploy/operator/show_initial_proof.sql\" $initial_hash"
echo 'PRODUCT OWNER: open http://127.0.0.1:8080/ords/f?p=810004:1 as LAB_USER. The live area now runs the later patch.'
pause 'View the current application; initial delivery is evidenced by the retained receipts, then press any key; q to quit.'
echo 'PASS result stage D_qualification.'
