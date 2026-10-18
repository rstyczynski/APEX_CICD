#!/usr/bin/env bash
# Construct this checkpoint from reviewed source on fresh isolated areas.
source "$(dirname "${BASH_SOURCE[0]}")/cicd-walkthrough-common.sh"
prepare_stage '## B. Deliver Hello' deploy/operator/import.sql scripts/cicd-artifact.py
test -f .local-apex/walkthrough/current/A_foundation.done
pause 'Press any key to install B_hello from reviewed source; q to quit.'
new_stage_source B_hello
echo 'SOURCE: reviewed B_hello snapshot f511ab8c8e1f723b70e4293f4488693a42b35532; unchanged native APEX and migrations.'
git archive f511ab8c8e1f723b70e4293f4488693a42b35532 apex db | tar -x -C "$stage_source"
check_result lab-dev-b "@\"$ROOT/deploy/operator/identity.sql\" E1_DEV_B E1_DEV_B
variable acquired_generation number
begin :acquired_generation:=E1_CTRL.e1_ownership.acquire('Hello','walkthrough-B_hello','f511ab8c8e1f723b70e4293f4488693a42b35532'); end;
/
column owned_generation new_value owned_generation noprint
select :acquired_generation owned_generation from dual;
cd \"$stage_source\"
lb validate -changelog-file db/changelog.xml
lb update -changelog-file db/changelog.xml
@\"$ROOT/deploy/operator/import.sql\" E1_DEV_B 810002 E1_DEV_B APEX-DELIVERY-LABORATORY-B \"$stage_source/apex/f810001\"
@\"$ROOT/deploy/operator/../checks/hello_assembly.sql\"
begin E1_CTRL.e1_ownership.release_task('walkthrough-B_hello',to_number('&owned_generation')); end;
/"
touch .local-apex/walkthrough/current/B_hello.done
echo 'DEPLOYED B_hello: reviewed source installed in this fresh cycle.'
echo 'PRODUCT OWNER: open http://127.0.0.1:8080/ords/f?p=810002:1.'
pause 'View this chapter result at the runtime URL, then press any key to finish; q to quit.'
echo 'PASS result stage B_hello.'
