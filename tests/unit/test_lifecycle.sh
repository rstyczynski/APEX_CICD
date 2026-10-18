# Local policy checks only; this test never starts, stops or deletes a runtime.
test_lab_cleanup_boundary() {
  python3 tests/unit/test_lab_inventory.py
}

test_onboarding_boundaries() {
  python3 tests/unit/test_onboarding.py
}

test_environment_name_boundary() {
  python3 tests/unit/test_environment_names.py
}
