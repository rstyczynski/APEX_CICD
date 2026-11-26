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

test_hosted_receipt() {
  python3 - <<'PYCODE'
import importlib.util
spec=importlib.util.spec_from_file_location('controller','sprint-work/E.15/controller.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
identity=dict(pr=1,head='a'*40,base='b'*40,trusted='c'*40,report_sha256='d'*64)
m.plan=lambda pr: identity.copy()
def unexpected(path):
 raise AssertionError('unbound receipt reached remote run lookup')
m.api=unexpected
for field in ('head','base','trusted','report_sha256'):
 receipt={**identity,'correlation':'different','run_id':1};receipt[field]='wrong'
 try:m.validate_receipt(receipt)
 except AssertionError as e:assert str(e)=='stale provenance', str(e)
 else:raise AssertionError('changed receipt accepted: '+field)
print('PASS receipt binding contract only; actual GitHub/Oracle evidence is separate')
PYCODE
}
