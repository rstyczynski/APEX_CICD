test_IT11_isolation() {
  python3 scripts/cicd-platform.py check
  python3 scripts/cicd-platform.py isolation
  python3 scripts/cicd-platform.py preservation-check
}
test_IT4_assembly() {
  # TODO: implement — assert Foundation-only then complete assembly.
  echo 'IT-4 assembly implementation pending' >&2
  return 1
}
