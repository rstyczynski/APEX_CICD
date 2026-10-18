# Control-flow tests: no Oracle or Podman operations.
_c_loop_setup() {
  source scripts/cicd-walkthrough-common.sh --preflight
  MODE=--live
  work="$(mktemp -d)"
}

test_C_loop_retries_missing_snapshot() (
  _c_loop_setup
  calls=0
  verify_runtime() { calls=$((calls+1)); }
  check_result() {
    if [ "$calls" -eq 1 ]; then echo 'C_VERIFICATION=WAITING' > "$work/output";
    else echo 'C_VERIFICATION=PASSED' > "$work/output"; fi
  }
  verify_c_runtime > "$work/transcript"
  [ "$calls" -eq 2 ]
  rg -q 'VERIFICATION NOT PASSED: Hello World assertion failed' "$work/transcript"
  rg -q 'PASS runtime assertion' "$work/transcript"
  rm "$work/transcript"
)

test_C_loop_quit_preserves_checkpoint() (
  _c_loop_setup
  verify_runtime() { exit 130; }
  check_result() { echo 'ERROR: must not run after quit' >&2; exit 99; }
  status=0
  ( verify_c_runtime ) || status=$?
  [ "$status" -eq 130 ]
)

test_C_loop_unexpected_sql_failure_stops() (
  _c_loop_setup
  verify_runtime() { :; }
  check_result() { exit 42; }
  status=0
  ( verify_c_runtime ) || status=$?
  [ "$status" -eq 42 ]
)


test_release_loop_retries_missing_snapshot() (
  _c_loop_setup
  calls=0
  verify_runtime() { calls=$((calls+1)); }
  check_result() {
    if [ "$calls" -eq 1 ]; then echo 'RELEASE_VERIFICATION=WAITING' > "$work/output";
    else echo 'RELEASE_VERIFICATION=PASSED' > "$work/output"; fi
  }
  verify_release_runtime user_acceptance_test E1_UAT 810005 > "$work/transcript"
  [ "$calls" -eq 2 ]
  rg -q 'VERIFICATION NOT PASSED: user_acceptance_test Hello World assertion failed' "$work/transcript"
  rg -q 'PASS runtime assertion' "$work/transcript"
  rm "$work/transcript"
)

test_release_loop_quit_preserves_checkpoint() (
  _c_loop_setup
  verify_runtime() { exit 130; }
  check_result() { exit 99; }
  status=0
  ( verify_release_runtime user_acceptance_test E1_UAT 810005 ) || status=$?
  [ "$status" -eq 130 ]
)

test_release_loop_unexpected_sql_failure_stops() (
  _c_loop_setup
  verify_runtime() { :; }
  check_result() { exit 42; }
  status=0
  ( verify_release_runtime user_acceptance_test E1_UAT 810005 ) || status=$?
  [ "$status" -eq 42 ]
)


test_initial_resume_rejects_published_checkpoint() (
  _c_loop_setup
  archive=/dev/null
  bash() { printf 'TARGET=E1_UAT APP=810005 EPOCH=1 PHASE=ready\n'; }
  check_result() { exit 99; }
  status=0
  ( resume_initial_verification user_acceptance_test E1_UAT 810005 ) > "$work/transcript" 2>&1 || status=$?
  [ "$status" -eq 1 ]
  rg -q 'not the retained verification checkpoint' "$work/transcript"
  rm "$work/transcript"
)

test_initial_resume_rejects_wrong_archive() (
  _c_loop_setup
  archive=/dev/null
  bash() { printf 'TARGET=E1_UAT APP=810005 EPOCH=1 PHASE=verifying\nARTIFACT=wrong\n'; }
  check_result() { exit 99; }
  status=0
  ( resume_initial_verification user_acceptance_test E1_UAT 810005 ) > "$work/transcript" 2>&1 || status=$?
  [ "$status" -eq 1 ]
  rg -q 'retained attempt archive differs' "$work/transcript"
  rm "$work/transcript"
)


test_examples_keep_existing_baseline() (
  _c_loop_setup
  touch "$work/baseline.json"
  python3() { printf '%s\n' "$*" >> "$work/calls"; }
  prepare_uat_upgrade_baseline "$work/baseline.json" > "$work/transcript"
  rg -q 'compare user_acceptance_test' "$work/calls"
  ! rg -q 'capture|apex_sql' "$work/calls"
  rm "$work/baseline.json" "$work/calls" "$work/transcript"
)

test_examples_capture_only_after_success() (
  _c_loop_setup
  python3() { printf '%s\n' "$*" >> "$work/calls"; }
  prepare_uat_upgrade_baseline "$work/baseline.json"
  [ "$(wc -l < "$work/calls" | tr -d ' ')" = 2 ]
  head -1 "$work/calls" | rg -q 'apex_sql.py user_acceptance_test'
  tail -1 "$work/calls" | rg -q 'capture user_acceptance_test'
  rm "$work/calls"
)

test_examples_failure_does_not_capture() (
  _c_loop_setup
  python3() { printf '%s\n' "$*" >> "$work/calls"; return 1; }
  status=0
  ( prepare_uat_upgrade_baseline "$work/baseline.json" ) > "$work/transcript" 2>&1 || status=$?
  [ "$status" -eq 1 ]
  ! rg -q 'capture' "$work/calls"
  rg -q -- '--resume-examples' "$work/transcript"
  rm "$work/calls" "$work/transcript"
)
