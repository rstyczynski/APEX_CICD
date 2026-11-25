test_foundation_smoke() (
 set -euo pipefail
 python3 -c "import ast; ast.parse(open('tests/foundation_lab.py').read())"
)
