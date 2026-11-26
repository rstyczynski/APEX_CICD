test_javascript_actions_source() {
 node --check sprint-work/E.19/actions/checks.cjs
 node --check sprint-work/E.19/host.cjs
 bash -n sprint-work/E.19/sql.sh
 actionlint sprint-work/E.19/native.yml sprint-work/E.19/acceptance.yml sprint-work/E.19/testing.yml sprint-work/E.19/benchmark.yml
 if rg -n 'python|\.py' sprint-work/E.19/native.yml sprint-work/E.19/acceptance.yml; then return 1; fi
}
