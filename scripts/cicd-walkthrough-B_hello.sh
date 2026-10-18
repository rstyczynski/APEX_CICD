#!/usr/bin/env bash
# Result stage paired with progress/E.1/cicd-walkthrough.md.
source "$(dirname "${BASH_SOURCE[0]}")/cicd-walkthrough-common.sh"
prepare_stage '## B. Deliver Hello' \
  'deploy/operator/identity.sql' \
  'deploy/operator/component_inventory.sql' \
  'deploy/checks/hello_assembly.sql'
pause 'Press any key to verify the existing Hello assembly; q to quit.'
check_result lab-dev-b "@\"$ROOT/deploy/operator/identity.sql\" E1_DEV_B E1_DEV_B
@\"$ROOT/deploy/operator/component_inventory.sql\"
@\"$ROOT/deploy/checks/hello_assembly.sql\""
echo 'VERIFIED EXISTING RESULT: B remains blocked while World is missing.'
echo 'PRODUCT OWNER: open http://127.0.0.1:8080/ords/f?p=810002:1'
pause 'See the World-not-installed message, then press any key; q to quit.'
echo 'PASS result stage B_hello.'
