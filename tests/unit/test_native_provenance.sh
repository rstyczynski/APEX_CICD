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
# Exercise both small validators on real files, without Oracle or SQLcl.
import subprocess
checks=Path('sprint-work/E.16').resolve()
with tempfile.TemporaryDirectory() as td:
 out=Path(td)/'output';out.write_text('SQLcl: Release 25.4.1.0 Production Build: 25.4.1.022.0618')
 def invoke(name):return subprocess.run([sys.executable,str(checks/name),str(out)],cwd=td,capture_output=True).returncode
 assert invoke('check_tool.py')==0
 out.write_text('SQLcl: Release 25.3.0.0 Production Build: 25.3.0.274.1210')
 assert invoke('check_tool.py')!=0
 out.write_text('SQLcl: Release 25.4.1.0 Production Build: 25.4.1.022.0618')
 config=Path(td)/'.dbtools/project.config.json';config.parent.mkdir();config.write_text('{"sqlcl":{"version":"25.3.0.0"}}')
 assert invoke('check_tool.py')!=0
 for text in ['ORA-01031: insufficient privileges','Errors: 1','Unknown Command','Expected a subcommand']:
  out.write_text(text);assert invoke('check_output.py')!=0
 out.write_text('Errors: 0\nOperation completed successfully.');assert invoke('check_output.py')==0
print('PASS provenance, measured tool/metadata and native-output checks; no Oracle mutation claimed')
PY
}
