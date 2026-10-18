#!/usr/bin/env bash
source "$(dirname "${BASH_SOURCE[0]}")/cicd-walkthrough-common.sh"
prepare_stage '## F. Deliver the compatible Hello patch' scripts/cicd-patch-step.sh scripts/cicd-preservation.py tests/sql/prepare_integration_test_fixture.sql
test -f .local-apex/walkthrough/current/E_promotion.done
new_stage_source F_hello_patch
archive="$(cat .local-apex/releases/patch-selected.txt)"
python3 scripts/cicd-artifact.py inspect "$archive"
pause 'Press any key to recreate ONLY disposable integration_test for fresh patch testing; q to quit.'
python3 scripts/cicd-platform.py reset-integration-test
patch_install integration_test E1_INTEGRATION 810004 empty
pause 'Press any key to recreate ONLY integration_test and reconstruct the initial upgrade baseline; q to quit.'
python3 scripts/cicd-platform.py reset-integration-test
archive="$(cat .local-apex/releases/initial-selected.txt)"
initial_install integration_test E1_INTEGRATION 810004 sentinels
python3 scripts/cicd-preservation.py capture integration_test .local-apex/releases/integration_test-initial-preservation.json
archive="$(cat .local-apex/releases/patch-selected.txt)"
patch_install integration_test E1_INTEGRATION 810004 1.0.0
python3 scripts/cicd-preservation.py compare integration_test .local-apex/releases/integration_test-initial-preservation.json
pause 'Both integration_test starts passed. Press any key to upgrade user_acceptance_test using those SAME bytes; q to quit.'
patch_install user_acceptance_test E1_UAT 810005 1.0.0
python3 scripts/cicd-preservation.py compare user_acceptance_test .local-apex/releases/test-initial-preservation.json
python3 scripts/apex_sql.py user_acceptance_test tests/sql/hello_patch.sql
touch .local-apex/walkthrough/current/F_hello_patch.done
echo 'PRODUCT OWNER: open http://127.0.0.1:8080/ords/f?p=810005:1 as LAB_USER; see Hello 1.0.1 and THIS cycle history retained.'
pause 'Create a greeting, refresh history and view Installed components; press any key to finish.'
echo 'PASS result stage F_hello_patch.'
