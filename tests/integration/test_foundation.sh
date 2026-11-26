test_foundation_live() (
 set -euo pipefail
 python3 tests/foundation_lab.py integration
)
test_bridge_live() (
 python3 tests/foundation_bridge.py integration
)

test_windows_integration() (
 python3 tests/foundation_windows.py integration
)
