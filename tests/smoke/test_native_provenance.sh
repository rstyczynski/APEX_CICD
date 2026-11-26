test_native_source() {
 python3 -m py_compile sprint-work/E.16/lifecycle.py sprint-work/E.16/provenance.py
 actionlint sprint-work/E.16/.github/workflows/native.yml
}
