#!/usr/bin/env bash
source "$(dirname "${BASH_SOURCE[0]}")/cicd-walkthrough-common.sh"
prepare_stage '## F. Deliver the compatible Hello patch' scripts/cicd-patch-step.sh scripts/cicd-preservation.py tests/sql/prepare_qualification_fixture.sql
test -f .local-apex/walkthrough/current/E_promotion.done
new_stage_source F_hello_patch
archive="$(cat .local-apex/releases/patch-selected.txt)"
python3 scripts/cicd-artifact.py inspect "$archive"
pause 'Press any key to recreate ONLY disposable qualification for fresh patch qualification; q to quit.'
python3 scripts/cicd-platform.py reset-qualify
python3 scripts/apex_sql.py lab-control deploy/release_control.sql
patch_install lab-qualify E1_QUALIFY 810004 empty
pause 'Press any key to recreate ONLY qualification and reconstruct the initial upgrade baseline; q to quit.'
python3 scripts/cicd-platform.py reset-qualify
python3 scripts/apex_sql.py lab-control deploy/release_control.sql
archive="$(cat .local-apex/releases/initial-selected.txt)"
initial_install lab-qualify E1_QUALIFY 810004 sentinels
python3 scripts/cicd-preservation.py capture lab-qualify .local-apex/releases/qualification-initial-preservation.json
archive="$(cat .local-apex/releases/patch-selected.txt)"
patch_install lab-qualify E1_QUALIFY 810004 1.0.0
python3 scripts/cicd-preservation.py compare lab-qualify .local-apex/releases/qualification-initial-preservation.json
pause 'Both qualification starts passed. Press any key to upgrade TEST using those SAME bytes; q to quit.'
patch_install lab-test E1_TEST 810005 1.0.0
python3 scripts/cicd-preservation.py compare lab-test .local-apex/releases/test-initial-preservation.json
python3 scripts/apex_sql.py lab-test tests/sql/hello_patch.sql
touch .local-apex/walkthrough/current/F_hello_patch.done
echo 'PRODUCT OWNER: open http://127.0.0.1:8080/ords/f?p=810005:1 as LAB_USER; see Hello 1.0.1 and THIS cycle history retained.'
pause 'Create a greeting, refresh history and view Installed components; press any key to finish.'
echo 'PASS result stage F_hello_patch.'
