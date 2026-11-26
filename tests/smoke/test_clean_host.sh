test_clean_host_source() {
 python3 -m py_compile tests/clean_host.py sprint-work/E.17/provision_host.py
 bash -n sprint-work/E.17/sql.sh
 actionlint sprint-work/E.17/.github/workflows/native.yml
}
