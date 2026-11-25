test_SM1_contract_sources() (
  set -euo pipefail
  python3 - <<'PY'
import sys,json,copy,re
from pathlib import Path
sys.path.insert(0,'tests');from contract_manifest import validate,qualified_toolchain
source=Path('examples/secure-backend/sql/secure_greetings.sql').read_text()
assert not re.search(r'\bcommit\b',source,re.I)
assert 'savepoint greeting_operation' in source and 'rollback to greeting_operation' in source
manifest=json.loads(Path('examples/secure-backend/contracts.json').read_text());validate(manifest)
bad=copy.deepcopy(manifest);bad['components']['Greeting']['version']='2.0.0'
try:validate(bad)
except ValueError:pass
else:raise AssertionError('Incompatible declaration was not rejected')
actual='SQLcl: Release 25.4.1.0 Production Build: 25.4.1.022.0618'
qualified_toolchain('25.4.1.0',actual)
for pin,version in [('26.3.0.0',actual),('25.4.1.0',actual.replace('25.4.1.022.0618','25.4.1.999.9999'))]:
 try:qualified_toolchain(pin,version)
 except ValueError:pass
 else:raise AssertionError('Toolchain mismatch was not rejected')
print('PASS explicit version/dependency declarations and caller-owned transaction boundary')
PY
)
