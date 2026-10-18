#!/usr/bin/env bash
# Result stage paired with progress/E.1/cicd-walkthrough.md.
source "$(dirname "${BASH_SOURCE[0]}")/cicd-walkthrough-common.sh"
prepare_stage '## C. Deliver World and complete the assembly' \
  'deploy/operator/identity.sql' \
  'deploy/operator/component_inventory.sql' \
  'deploy/checks/published_development.sql'
pause 'Press any key to verify the published development assembly; q to quit.'
check_result lab-dev-c "@\"$ROOT/deploy/operator/identity.sql\" E1_DEV_C E1_DEV_C
@\"$ROOT/deploy/operator/component_inventory.sql\"
@\"$ROOT/deploy/checks/published_development.sql\""
echo 'VERIFIED EXISTING RESULT: C development application, supported 1.0.0 / 1.0.1 / 1.0.0 components.'
echo 'PRODUCT OWNER: open http://127.0.0.1:8080/ords/f?p=810003:1 and sign in as LAB_USER.'
echo 'Select Hello/World, Create greeting, reopen Greeting history and Installed components.'
pause 'Use the application to see its result, then press any key; q to quit.'
echo 'PASS result stage C_world.'
