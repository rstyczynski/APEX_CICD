test_foundation_live() (
 set -euo pipefail
 python3 tests/foundation_lab.py integration
)
test_bridge_live() (
 python3 tests/foundation_bridge.py integration
)
