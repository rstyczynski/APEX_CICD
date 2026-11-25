test_IT1_backend_runtime() (
  set -euo pipefail
  python3 tests/backend_runner.py integration
)

test_IT4_backend_page_and_release() (
  set -euo pipefail
  python3 - <<'PY'
import sys,json,re,zipfile,hashlib
from pathlib import Path
sys.path.insert(0,'tests')
import backend_admin as b
b.sql((b.ROOT/'tests/sql/backend/page_assertions.sql').read_text(),'page-assertions.log')
base=Path('progress/E.5/tests')
receipt=json.loads((base/'native-release.json').read_text())
archive=base/receipt['archive']
assert hashlib.sha256(archive.read_bytes()).hexdigest()==receipt['sha256']
with zipfile.ZipFile(archive) as z:
 assert len(z.namelist())==receipt['entries']
 assert not any(re.search(r'e5_test|e5_ut|test_hello_entry|e5_test_ddl',n,re.I) for n in z.namelist())
 for n in z.namelist():
  if n.endswith(('.sql','.xml')):
   assert not re.search(r'create\s+(?:or\s+replace\s+)?(?:package|table)\s+(?:e5_test|test_hello_entry|e5_test_ddl)',z.read(n).decode(),re.I), n
observed=json.loads((base/'browser-observations.json').read_text())
assert observed['baseline']['empty_input']==observed['package_backed']['empty_input']
assert observed['package_backed']['visible_saved_value']=='E5 after'
print('PASS live page mapping, invalid API rejection and native artifact exclusion; browser observations separately recorded')
PY
)
