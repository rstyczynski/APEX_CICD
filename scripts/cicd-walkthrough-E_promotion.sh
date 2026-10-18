#!/usr/bin/env bash
source "$(dirname "${BASH_SOURCE[0]}")/cicd-walkthrough-common.sh"
prepare_stage '## E. Promote the same initial artifact to user_acceptance_test' scripts/cicd-release-step.sh scripts/cicd-release-result.sh tests/sql/prepare_history_sentinels.sql
test -f .local-apex/walkthrough/current/D_qualification.done
new_stage_source E_promotion
archive="$(cat .local-apex/releases/initial-selected.txt)"
initial_hash="$(shasum -a 256 "$archive" | awk '{print $1}')"
python3 scripts/cicd-artifact.py inspect "$archive"
initial_install user_acceptance_test E1_UAT 810005
check_result lab-control "@\"$ROOT/deploy/operator/show_initial_proof.sql\" $initial_hash"
echo 'PRODUCT OWNER: open http://127.0.0.1:8080/ords/f?p=810005:1 as LAB_USER. This NEW TEST application runs 1.0.0.'
pause 'Create a greeting and view its NEW history; press any key to prepare explicit upgrade test examples.'
python3 scripts/apex_sql.py user_acceptance_test tests/sql/prepare_history_sentinels.sql
python3 scripts/cicd-preservation.py capture user_acceptance_test .local-apex/releases/test-initial-preservation.json
touch .local-apex/walkthrough/current/E_promotion.done
echo 'PASS result stage E_promotion: identical qualified/promoted archive; NEW field baseline captured for F.'
