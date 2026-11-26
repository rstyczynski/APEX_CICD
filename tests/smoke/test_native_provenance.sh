test_native_source() {
 python3 -m py_compile sprint-work/E.16/check_tool.py sprint-work/E.16/check_output.py sprint-work/E.16/provenance.py
 bash -n sprint-work/E.16/sql.sh
 test ! -e sprint-work/E.16/lifecycle.py
 python3 - <<'PYCODE'
import ast
from pathlib import Path
for name in ['check_tool.py','check_output.py','provenance.py']:
 tree=ast.parse((Path('sprint-work/E.16')/name).read_text())
 assert not any(isinstance(n,ast.Import) and any(a.name=='subprocess' for a in n.names) for n in ast.walk(tree))
print('PASS small Python checks do not launch lifecycle operations')
PYCODE
 actionlint sprint-work/E.16/.github/workflows/native.yml
}
