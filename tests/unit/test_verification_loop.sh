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
