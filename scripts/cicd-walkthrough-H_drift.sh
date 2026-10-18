#!/usr/bin/env bash
# Result stage paired with progress/E.1/cicd-walkthrough.md.
source "$(dirname "${BASH_SOURCE[0]}")/cicd-walkthrough-common.sh"
prepare_stage '## H. Reject deployment over unexpected live change' \
  'scripts/cicd-drift-demo.py' \
  'scripts/cicd-protection-check.sh' \
  'scripts/cicd-patch-result.sh' \
  'scripts/cicd-patch-step.sh'
echo 'This script runs H.2, the optional automated replay. For the guided App Builder demonstration, follow H.1 separately.'
test -f .local-apex/walkthrough/current/F_hello_patch.done
bash scripts/cicd-protection-check.sh drift --expect-clean
pause 'Press any key to save TEST and install the controlled page-drift fixture; q to quit.'
python3 scripts/cicd-drift-demo.py inject
echo 'PRODUCT OWNER: open http://127.0.0.1:8080/ords/f?p=810005:1 and re-login if needed; see DIRECT CHANGE - deployment must stop.'
pause 'View the changed page, then press any key to attempt redeployment preflight; q leaves the fixture active for explicit restoration.'
bash scripts/cicd-protection-check.sh drift --expect-drift
pause 'Reopen TEST to see the changed page/history retained, then press any key for the separate RESTORE operation; q leaves the fixture active.'
python3 scripts/cicd-drift-demo.py restore
bash scripts/cicd-protection-check.sh drift --expect-clean
echo 'PRODUCT OWNER: reopen http://127.0.0.1:8080/ords/f?p=810005:1; re-login if needed. The banner is gone and history remains.'
pause 'View the restored application, then press any key to finish; q to quit.'
echo 'PASS result stage H_drift.'
