#!/usr/bin/env bash
# Result stage paired with progress/E.1/cicd-walkthrough.md.
source "$(dirname "${BASH_SOURCE[0]}")/cicd-walkthrough-common.sh"
prepare_stage '## G. Reject an incompatible database upgrade' \
  'scripts/cicd-protection-check.sh'
test -f .local-apex/walkthrough/current/F_hello_patch.done
pause 'Press any key to submit the incompatible Foundation-major proposal; q to quit.'
bash scripts/cicd-protection-check.sh compatibility
echo 'PRODUCT OWNER: open http://127.0.0.1:8080/ords/f?p=810005:1; the existing greeting/history application still works.'
pause 'See the retained application after rejection, then press any key; q to quit.'
echo 'PASS result stage G_incompatible_upgrade.'
