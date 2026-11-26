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
print('PASS every named E17 native validation step retained')
PY
}
