test_SM2_compatibility() {
  bash scripts/cicd-protection-check.sh compatibility
}
test_IT7_drift() {
  # Error-code text inside structured evidence must not mask or impersonate SQL failures.
  python3 - <<'BOUNDARY'
import sys
sys.path.insert(0,'scripts')
from apex_sql import run
assert 'ORA-20998' in run("set sqlformat csv\nselect 'ORA-20998: retained diagnostic' as failure_reason from dual;",connection='user_acceptance_test')
try:
    run("begin raise_application_error(-20998,'Boundary assertion'); end;\n/",connection='user_acceptance_test')
except RuntimeError as exc:
    assert 'ORA-20998' in str(exc)
else:
    raise AssertionError('Real Oracle failure did not stop SQL execution')
print('PASS IT-7 SQL boundary: stored diagnostics readable, real Oracle exceptions fail.')
BOUNDARY
  python3 scripts/cicd-drift-demo.py inject
  bash scripts/cicd-protection-check.sh drift
  python3 scripts/cicd-drift-demo.py restore
  bash scripts/cicd-patch-result.sh user_acceptance_test
}
