#!/usr/bin/env bash
source "$(dirname "${BASH_SOURCE[0]}")/cicd-walkthrough-common.sh"
prepare_stage '## D. Qualify the initial release' scripts/cicd-release-step.sh scripts/cicd-release-result.sh deploy/operator/walkthrough_runtime.sql
test -f .local-apex/walkthrough/current/C_world.done
new_stage_source D_qualification
archive="$(cat .local-apex/releases/initial-selected.txt)"
python3 scripts/cicd-artifact.py inspect "$archive"
initial_install lab-qualify E1_QUALIFY 810004
touch .local-apex/walkthrough/current/D_qualification.done
echo 'DEPLOYED AND QUALIFIED initial release 1.0.0 from the verified archive in this cycle.'
echo 'PRODUCT OWNER: open http://127.0.0.1:8080/ords/f?p=810004:1 as LAB_USER.'
pause 'Use the NEW qualification application and history; then press any key to finish.'
echo 'PASS result stage D_qualification.'
