test_IT11_isolation() {
  python3 scripts/cicd-platform.py check
  python3 scripts/cicd-platform.py isolation
  python3 scripts/cicd-platform.py preservation-check
}
test_IT4_assembly() {
  python3 tests/legacy_release.py assembly
}
