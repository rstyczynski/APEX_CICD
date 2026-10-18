# Local policy checks only; this test never starts, stops or deletes a runtime.
test_lab_cleanup_boundary() {
  python3 tests/unit/test_lab_inventory.py
}
