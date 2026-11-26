test_native_guard() {
 python3 - <<'PY'
import sys,tempfile,hashlib
from pathlib import Path
sys.path.insert(0,'sprint-work/E.16')
from provenance import guard,BUILD
with tempfile.TemporaryDirectory() as td:
 a=Path(td)/'archive';a.write_bytes(b'qualified')
 r=dict(source='a'*40,build=BUILD,sha256=hashlib.sha256(a.read_bytes()).hexdigest())
 guard(a,r,'a'*40,BUILD)
 for key,value in [('source','b'*40),('build','wrong'),('sha256','0'*64)]:
  wrong={**r,key:value}
  try:guard(a,wrong,'a'*40,BUILD)
  except AssertionError:pass
  else:raise AssertionError('accepted '+key)
 a.write_bytes(b'substituted')
 try:guard(a,r,'a'*40,BUILD)
 except AssertionError:pass
 else:raise AssertionError('substitution accepted')
print('PASS provenance contract; no Oracle mutation claimed')
PY
}
