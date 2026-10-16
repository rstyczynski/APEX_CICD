test_IT11_isolation() {
  python3 scripts/cicd-platform.py check
  python3 scripts/cicd-platform.py isolation
  python3 scripts/cicd-platform.py preservation-check
}
test_IT4_assembly() {
  python3 scripts/apex_sql.py lab-dev deploy/operator/foundation_verify.sql
  python3 scripts/apex_sql.py lab-dev deploy/checks/foundation_contract.sql
  local cookie_file
  cookie_file="$(mktemp)"
  curl -fsSL -b "$cookie_file" -c "$cookie_file" 'http://127.0.0.1:8080/ords/f?p=810001:1' | rg -q 'Foundation assembly: Hello and World are not installed.'
  local result=$?
  rm -f "$cookie_file"
  return "$result"
}
