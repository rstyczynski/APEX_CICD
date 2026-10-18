# No Oracle/Podman calls: classify captured preflight outcomes only.
_protection_case() (
  source scripts/cicd-protection-check.sh
  log="$(mktemp)"
  trap 'rm -f "$log"' EXIT
  printf '%s\n' "$1" > "$log"
  status=0
  observed="$(protection_outcome "$2" "$3" "$log" "$4")" || status=$?
  [ "$status" -eq "$5" ]
  [ "$observed" = "$6" ]
)

test_clean_drift_check_passes() {
  _protection_case 'ALREADY DELIVERED: patch versions and live APEX fingerprint match; no writes.' drift 0 any 0 clean
}
test_changed_drift_check_passes() {
  _protection_case 'REJECTED DRIFT: live APEX fingerprint differs.' drift 1 any 0 drift
}
test_unexpected_error_is_not_drift() {
  _protection_case 'ORA-01017: invalid credentials' drift 1 any 1 ''
}
test_silent_failure_is_not_drift() {
  _protection_case '' drift 1 any 1 ''
}
test_fixture_requires_actual_drift() {
  _protection_case 'ALREADY DELIVERED: patch versions and live APEX fingerprint match; no writes.' drift 0 --expect-drift 1 ''
}
test_baseline_requires_clean_target() {
  _protection_case 'REJECTED DRIFT: live APEX fingerprint differs.' drift 1 --expect-clean 1 ''
}
test_compatibility_still_requires_specific_rejection() {
  _protection_case 'REJECTED INCOMPATIBLE: Hello requires Foundation 1.0.0; proposed Foundation 2.0.0' compatibility 1 any 0 incompatible
}
