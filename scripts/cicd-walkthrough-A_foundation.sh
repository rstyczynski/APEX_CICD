#!/usr/bin/env bash
# Result stage paired with progress/E.1/cicd-walkthrough.md.
source "$(dirname "${BASH_SOURCE[0]}")/cicd-walkthrough-common.sh"
prepare_stage '## A. Deliver Foundation' \
  'deploy/operator/identity.sql' \
  'deploy/operator/application_inventory.sql' \
  'deploy/operator/component_inventory.sql' \
  'deploy/operator/foundation_verify.sql' \
  'deploy/operator/show_reservations.sql'
pause 'Press any key to check the existing Foundation result; q to quit.'
check_result lab-dev "@\"$ROOT/deploy/operator/identity.sql\" E1_DEV_A E1_DEV_A
@\"$ROOT/deploy/operator/application_inventory.sql\"
@\"$ROOT/deploy/operator/component_inventory.sql\"
@\"$ROOT/deploy/operator/foundation_verify.sql\""
check_result lab-control "@\"$ROOT/deploy/operator/show_reservations.sql\""
echo 'PRODUCT OWNER: open http://127.0.0.1:8080/ords/f?p=810001:1'
echo 'Expected: Foundation assembly: Hello and World are not installed.'
pause 'Open that runtime URL to see the blocked incomplete application, then press any key; q to quit.'
echo 'PASS result stage A_foundation.'
