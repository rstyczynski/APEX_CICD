test_foundation_smoke() (
 set -euo pipefail
 python3 -c "import ast; ast.parse(open('tests/foundation_lab.py').read())"
)
test_bridge_smoke() (
 python3 -c "import ast,pathlib; ast.parse(pathlib.Path('tests/foundation_bridge.py').read_text())"
)

test_windows_smoke() (
 python3 -c "import ast; ast.parse(open('tests/foundation_windows.py').read())"
)
