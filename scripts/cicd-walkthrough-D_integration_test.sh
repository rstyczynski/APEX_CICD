#!/usr/bin/env bash
source "$(dirname "${BASH_SOURCE[0]}")/cicd-walkthrough-common.sh"
prepare_stage '## D. Qualify the initial release' scripts/cicd-release-step.sh scripts/cicd-release-result.sh deploy/operator/walkthrough_runtime.sql
# 1. Require completed C and create a new D attempt.
test -f .local-apex/walkthrough/current/C_world.done
new_stage_source D_integration_test
# 2. Select and inspect the retained reviewed initial archive.
archive="$(cat .local-apex/releases/initial-selected.txt)"
python3 scripts/cicd-artifact.py inspect "$archive"
# 3-12. Status -> admit -> migrate -> import -> units -> verify -> browser VERIFIER
# -> publish -> result/receipt/fingerprint. Each controller operation remains visible.
initial_install integration_test E1_INTEGRATION 810004
touch .local-apex/walkthrough/current/D_integration_test.done
echo 'DEPLOYED AND INTEGRATION_TEST PASSED initial release 1.0.0 from the verified archive in this cycle.'
# 13-15. Retrieve LAB_USER password, check ordinary runtime, finish D.
echo '1. In another terminal: python3 scripts/cicd-password.py LAB_USER'
echo '2. Sign out of VERIFIER; open http://127.0.0.1:8080/ords/f?p=810004:1 and sign in as LAB_USER.'
echo '3. Create a greeting and refresh Greeting history; return here to finish D.'
pause 'Use the NEW integration_test application and history; then press any key to finish.'
echo 'PASS result stage D_integration_test.'
