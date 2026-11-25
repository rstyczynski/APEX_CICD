test_runner_final_record() {
  python3 - <<'PY'
import tempfile,subprocess
from pathlib import Path
with tempfile.TemporaryDirectory() as td:
 manifest=Path(td)/'case.manifest'
 for ending in ['', '\n']:
  manifest.write_text('unit:test_foundation.sh:test_foundation_unit'+ending)
  result=subprocess.run(['bash','tests/run.sh','--unit','--new-only',str(manifest)],text=True,capture_output=True)
  assert result.returncode==0,result.stdout+result.stderr
  assert result.stdout.count('RUN unit:')==1,result.stdout
  assert 'Tests: 1; failed: 0' in result.stdout,result.stdout
import shutil
with tempfile.TemporaryDirectory() as td:
 root=Path(td);(root/'tests/unit').mkdir(parents=True);(root/'tests/manifests').mkdir()
 shutil.copyfile('tests/run.sh',root/'tests/run.sh')
 (root/'tests/unit/test_probe.sh').write_text('test_sink() { cat >/dev/null; }\ntest_after() { echo FOLLOWING_CASE_EXECUTED; }\n')
 (root/'tests/manifests/component_delivery.manifest').write_text('unit:test_probe.sh:test_sink\nunit:test_probe.sh:test_after\n')
 result=subprocess.run(['bash',str(root/'tests/run.sh'),'--unit'],text=True,capture_output=True)
 assert result.returncode==0,result.stdout+result.stderr
 assert 'FOLLOWING_CASE_EXECUTED' in result.stdout,result.stdout
 assert 'Tests: 2; failed: 0' in result.stdout,result.stdout
print('PASS actual runner final record with/without newline and manifest protected from stdin-draining child')
PY
}

test_private_sql_binding() {
  python3 - <<'UNIT'
import os,sys,tempfile
from pathlib import Path
sys.path.insert(0,'scripts')
import apex_sql
with tempfile.TemporaryDirectory() as td:
 apex_sql.LOCAL=Path(td) # No credential files exist here: validation must precede reading them.
 for descriptor in ['localhost:1521/FREEPDB1\nselect 1 from dual;', 'localhost:99999/FREEPDB1', 'localhost:1521/FREEPDB1 as sysdba']:
  os.environ['APEX_CICD_SERVICE']=descriptor
  try:apex_sql.run('select 1 from dual;')
  except ValueError:pass
  else:raise AssertionError('Unsafe descriptor reached connection processing')
 os.environ.pop('APEX_CICD_SERVICE')
 before=apex_sql.command()[0]
 os.environ['APEX_CICD_CONNECTIONS']=td
 command=apex_sql.command()
 assert command[command.index('-home')+1]==td
 assert command[0]==before
print('PASS invalid descriptors rejected before credential access; private profile keeps pinned tool path')
UNIT
}
