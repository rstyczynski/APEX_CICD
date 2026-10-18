#!/usr/bin/env bash
RESUME_VERIFICATION=0
RESUME_EXAMPLES=0
case "${1:-}" in
  --resume-verification) RESUME_VERIFICATION=1; shift ;;
  --resume-examples) RESUME_EXAMPLES=1; shift ;;
esac
source "$(dirname "${BASH_SOURCE[0]}")/cicd-walkthrough-common.sh"
prepare_stage '## E. Promote the same initial artifact to user_acceptance_test' scripts/cicd-release-step.sh scripts/cicd-release-result.sh tests/sql/prepare_history_sentinels.sql
test -f .local-apex/walkthrough/current/D_integration_test.done
if [ "$RESUME_VERIFICATION" -eq 0 ] && [ "$RESUME_EXAMPLES" -eq 0 ]; then
  if [ -d .local-apex/walkthrough/current/E_promotion ]; then
    echo 'Existing E attempt: use --resume-verification before publication, or --resume-examples after successful publication.' >&2
  fi
  new_stage_source E_promotion
fi
archive="$(cat .local-apex/releases/initial-selected.txt)"
initial_hash="$(shasum -a 256 "$archive" | awk '{print $1}')"
python3 scripts/cicd-artifact.py inspect "$archive"
if [ "$RESUME_EXAMPLES" -eq 1 ]; then
  [ "$MODE" = --live ] || { echo 'ERROR: resume requires an interactive terminal.' >&2; exit 2; }
  test -d .local-apex/walkthrough/current/E_promotion
  test ! -e .local-apex/walkthrough/current/E_promotion.done
  bash scripts/cicd-release-result.sh "$archive" user_acceptance_test
  echo 'RESUME: published initial UAT release verified; continue only browser result and upgrade examples.'
elif [ "$RESUME_VERIFICATION" -eq 1 ]; then
  [ "$MODE" = --live ] || { echo 'ERROR: resume requires interactive verification.' >&2; exit 2; }
  test -d .local-apex/walkthrough/current/E_promotion
  test ! -e .local-apex/walkthrough/current/E_promotion.done
  resume_initial_verification user_acceptance_test E1_UAT 810005
  verify_release_runtime user_acceptance_test E1_UAT 810005
  bash scripts/cicd-release-step.sh "$archive" user_acceptance_test publish "$release_epoch"
  bash scripts/cicd-release-result.sh "$archive" user_acceptance_test
else
  initial_install user_acceptance_test E1_UAT 810005
fi
check_result lab-control "@\"$ROOT/deploy/operator/show_initial_proof.sql\" $initial_hash"
echo 'PRODUCT OWNER: open http://127.0.0.1:8080/ords/f?p=810005:1 as LAB_USER. This user_acceptance_test application runs 1.0.0.'
pause 'View LAB_USER greeting history; create a greeting only if none exists. Press any key to prepare explicit upgrade test examples; q to quit.'
prepare_uat_upgrade_baseline
touch .local-apex/walkthrough/current/E_promotion.done
echo 'PASS result stage E_promotion: identical qualified/promoted archive; NEW field baseline captured for F.'
