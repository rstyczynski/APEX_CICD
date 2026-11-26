test_foundation_unit() (
 set -euo pipefail
 python3 tests/foundation_lab.py unit
)
test_bridge_unit() (
 python3 tests/foundation_bridge.py unit
)

test_windows_unit() (
 python3 tests/foundation_windows.py unit
)
