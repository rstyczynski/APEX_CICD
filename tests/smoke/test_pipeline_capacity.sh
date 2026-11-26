test_pipeline_capacity_source() {
 actionlint sprint-work/E.18/.github/workflows/native.yml
 bash -n sprint-work/E.18/sql.sh
 python3 -m py_compile tests/pipeline_capacity.py sprint-work/E.18/sample_resources.py sprint-work/E.18/provision_host.py
 python3 - <<'PY'
from pathlib import Path
old=Path('sprint-work/E.17/.github/workflows/native.yml').read_text()
new=Path('sprint-work/E.18/.github/workflows/native.yml').read_text()
for line in old.splitlines():
 if '- name:' in line:assert line in new,line
for source,target in [('tests/sql/backend/bootstrap.sql','backend-bootstrap.sql'),('tests/sql/backend/test_hello_entry_api.sql','backend-tests.sql'),('examples/testable-backend/sql/hello_entry_api.sql','backend-api.sql')]:
 assert Path(source).read_bytes()==Path('sprint-work/E.18',target).read_bytes(),target
assert "5 tests, 0 failed, 0 errored" in new
print('PASS every named E17 native validation step retained')
PY
}
