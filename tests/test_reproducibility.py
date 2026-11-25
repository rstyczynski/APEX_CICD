import sys,tempfile,hashlib
from pathlib import Path
sys.path.insert(0,'scripts')
from reproducible_delivery import validate, summary
with tempfile.TemporaryDirectory() as d:
 p=Path(d)/'cache';p.write_bytes(b'qualified')
 digest=hashlib.sha256(p.read_bytes()).hexdigest()
 validate(p,'3.23.0',digest)
 for version,sha in [('3.22.0',digest),('3.23.0','0'*64)]:
  try:validate(p,version,sha)
  except ValueError:pass
  else:raise AssertionError('invalid tool accepted')
 assert summary([3,1,2])=={'n':3,'median':2,'p95':3}
print('PASS wrong version, corrupt cache, valid cache and nearest-rank statistics')
