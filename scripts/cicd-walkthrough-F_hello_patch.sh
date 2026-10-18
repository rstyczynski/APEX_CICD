#!/usr/bin/env bash
# Result stage paired with progress/E.1/cicd-walkthrough.md.
source "$(dirname "${BASH_SOURCE[0]}")/cicd-walkthrough-common.sh"
prepare_stage '## F. Deliver the compatible Hello patch' \
  'scripts/cicd-patch-result.sh' \
  'scripts/cicd-patch-step.sh' \
  'scripts/cicd-preservation.py' \
  'scripts/apex_sql.py' \
  'tests/sql/hello_patch.sql'
pause 'Press any key to verify the existing qualified/promoted patch and retained fields; q to quit.'
bash scripts/cicd-patch-result.sh lab-qualify
bash scripts/cicd-patch-result.sh lab-test
python3 scripts/cicd-preservation.py compare lab-test .local-apex/releases/test-initial-preservation.json
python3 scripts/apex_sql.py lab-test tests/sql/hello_patch.sql
echo 'PRODUCT OWNER: open http://127.0.0.1:8080/ords/f?p=810005:1; create a greeting, refresh history and inspect Installed components.'
pause 'Use TEST and see Foundation 1.0.0 / Hello 1.0.1 / World 1.0.0, then press any key; q to quit.'
echo 'PASS result stage F_hello_patch.'
