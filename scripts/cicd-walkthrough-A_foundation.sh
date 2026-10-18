#!/usr/bin/env bash
# Construct this checkpoint from reviewed source on fresh isolated areas.
source "$(dirname "${BASH_SOURCE[0]}")/cicd-walkthrough-common.sh"
prepare_stage '## A. Deliver Foundation' deploy/operator/import.sql scripts/cicd-artifact.py
pause 'Press any key to install A_foundation from reviewed source; q to quit.'
new_stage_source A_foundation
echo 'SOURCE: reviewed A_foundation snapshot e9a490f0582e768ad822a498453af69aedc9b1e9; unchanged native APEX and migrations.'
git archive e9a490f0582e768ad822a498453af69aedc9b1e9 apex db | tar -x -C "$stage_source"
check_result lab-dev "@\"$ROOT/deploy/operator/identity.sql\" E1_DEV_A E1_DEV_A
variable acquired_generation number
begin :acquired_generation:=E1_CTRL.e1_ownership.acquire('Foundation','walkthrough-A_foundation','e9a490f0582e768ad822a498453af69aedc9b1e9'); end;
/
column owned_generation new_value owned_generation noprint
select :acquired_generation owned_generation from dual;
cd \"$stage_source\"
lb validate -changelog-file db/changelog.xml
lb update -changelog-file db/changelog.xml
@\"$ROOT/deploy/operator/import.sql\" E1_DEV_A 810001 E1_DEV_A APEX-DELIVERY-LABORATORY \"$stage_source/apex/f810001\"
@\"$ROOT/deploy/operator/foundation_verify.sql\"
begin E1_CTRL.e1_ownership.release_task('walkthrough-A_foundation',to_number('&owned_generation')); end;
/"
touch .local-apex/walkthrough/current/A_foundation.done
echo 'DEPLOYED A_foundation: reviewed source installed in this fresh cycle.'
echo 'PRODUCT OWNER: open http://127.0.0.1:8080/ords/f?p=810001:1.'
pause 'View this chapter result at the runtime URL, then press any key to finish; q to quit.'
echo 'PASS result stage A_foundation.'
