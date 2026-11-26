test_pipeline_capacity_arithmetic() {
 python3 - <<'PY'
import sys
from pathlib import Path
sys.path.insert(0,'tests')
from pipeline_capacity import distribution,seconds,summarize
assert distribution([10,20])==dict(n=2,median=15,p95=20)
assert seconds('2026-11-26T00:00:02Z')-seconds('2026-11-26T00:00:00Z')==2
for values in [[],[-1],[float('nan')]]:
 try:distribution(values)
 except ValueError:pass
 else:raise AssertionError('invalid samples accepted')
try:summarize(dict(conclusion='failure'),[],Path('.'))
except ValueError:pass
else:raise AssertionError('failed run accepted')
print('PASS synthetic arithmetic and failed-run refusal; no performance claim')
PY
}
