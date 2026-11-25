test_IT1_compatibility() (
  set -euo pipefail
  python3 tests/contracts_lab.py compatibility
)
test_IT2_sessions_transactions() (
  set -euo pipefail
  python3 tests/contracts_lab.py integration
)
test_IT4_page_release() (
  set -euo pipefail
  python3 - <<'PY'
import sys,json,zipfile,re,hashlib
from pathlib import Path
sys.path.insert(0,'tests');from contracts_lab import execute,OUT
out=execute("select 'BROWSER_ALLOWED:'||count(*) from e6_app.greeting_requests where request_key='BROWSER-ALLOW-1' and country_code='PL' and actor='ALICE';\nselect 'BROWSER_DENIED:'||count(*) from e6_app.greeting_requests where request_key='BROWSER-DENIED-1';\nselect 'TEST_TRIGGER:'||count(*) from dba_triggers where owner='E6_APP' and trigger_name='E6_TEST_AUDIT_FAILURE';",'page-business-check.log')
assert 'BROWSER_ALLOWED:1' in out and 'BROWSER_DENIED:0' in out and 'TEST_TRIGGER:0' in out,out
receipt=json.loads((OUT/'native-release.json').read_text());archive=OUT/receipt['archive']
assert hashlib.sha256(archive.read_bytes()).hexdigest()==receipt['sha256']
assert hashlib.sha256(Path('examples/secure-backend/contracts.json').read_bytes()).hexdigest()==receipt['component_declarations_sha256']
with zipfile.ZipFile(archive) as z:
 names=z.namelist();assert any('apex' in n.lower() for n in names)
 assert any('secure_greetings' in n.lower() for n in names)
 assert not any(re.search(r'e6_test|test_contract|e6_test_audit_failure',n,re.I) for n in names)
observed=json.loads((OUT/'browser-observations.json').read_text());assert observed['wrong_password_rejected'] and observed['allowed_page_submit'] and observed['denied_country_submit']
print('PASS separate browser evidence, live business invariants and native whole-application artifact')
PY
)
