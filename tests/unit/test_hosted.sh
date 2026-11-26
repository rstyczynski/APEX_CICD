test_hosted_input() {
  python3 - <<'PY'
import importlib.util, tempfile
from pathlib import Path
spec=importlib.util.spec_from_file_location('validator','sprint-work/E.15/validate.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
with tempfile.TemporaryDirectory() as td:
 p=Path(td)/'candidate.sql'
 for data in ['', ' ' * 8193]:
  p.write_text(data)
  try:m.load(p)
  except ValueError:pass
  else:raise AssertionError('invalid input accepted')
 p.write_text("select 'Hello World' from dual")
 assert m.load(p)==p.read_text()
 q=Path(td)/'other.sql';q.write_text('select 1 from dual')
 try:m.load(q)
 except ValueError:pass
 else:raise AssertionError('wrong path accepted')
print('PASS bounded SQL input contract; no Oracle execution claimed')
PY
}
