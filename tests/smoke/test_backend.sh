test_SM1_backend_source() (
  set -euo pipefail
  python3 - <<'PY'
from pathlib import Path
import re
api=Path('examples/testable-backend/sql/hello_entry_api.sql').read_text()
assert not re.search(r'\b(commit|rollback)\b',api,re.I)
assert api.index('raise_application_error(-20321') < api.index('insert into')
assert not list(Path('examples/testable-backend').rglob('test_*.sql'))
assert 'P101_ENTRY_TEXT' in Path('examples/testable-backend/sql/page_create_adapter.sql').read_text()
print('PASS backend source boundaries; runtime/page evidence is checked separately')
PY
)
