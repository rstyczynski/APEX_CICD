test_clean_host_receipt() {
 python3 - <<'PY'
import sys,tempfile,json,hashlib
from pathlib import Path
sys.path.insert(0,'tests')
from clean_host import validate
with tempfile.TemporaryDirectory() as d:
 root=Path(d)
 try:validate(root,'1','a'*40)
 except FileNotFoundError:pass
 else:raise AssertionError('missing observations accepted')
 fixtures={'host.json':dict(run='1',source='a'*40,host='contract-host',identity='contract-operator',database_containers=['one','two'],fresh_inputs='new random per-run'), 'application-access.json':dict(status=200,login=True),'success.json':dict(preserved=True)}
 for name,data in fixtures.items():(root/name).write_text(json.dumps(data))
 for name,text in {'application.html':'APEX Delivery Laboratory','cleanup.txt':'PASS private inputs removed','assert-upgrade.log':'retained across upgrade','assert-repeat.log':'retained across upgrade'}.items():(root/name).write_text(text)
 for v in ['1.0.0','1.1.0']:
  (root/f'native16-{v}.zip').write_bytes(b'contract bytes')
  (root/f'receipt-{v}.json').write_text(json.dumps(dict(workflow_source='a'*40,workflow_run='1',build='25.4.1.022.0618',sha256=hashlib.sha256(b'contract bytes').hexdigest())))
 validate(root,'1','a'*40)
 for name,bad in [('host.json',{**fixtures['host.json'],'run':'2'}),('application-access.json',dict(status=503,login=False)),('success.json',dict(preserved=False))]:
  (root/name).write_text(json.dumps(bad))
  try:validate(root,'1','a'*40)
  except AssertionError:pass
  else:raise AssertionError('accepted invalid '+name)
  (root/name).write_text(json.dumps(fixtures[name]))
 (root/'native16-1.1.0.zip').write_bytes(b'substituted')
 try:validate(root,'1','a'*40)
 except AssertionError:pass
 else:raise AssertionError('accepted substituted archive')
print('PASS synthetic reader contracts: missing, stale, failed access, lost data and substituted archive rejected; no platform behavior claimed')
PY
}
