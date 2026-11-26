test_hosted_source() {
  python3 -m py_compile sprint-work/E.15/validate.py sprint-work/E.15/controller.py
  actionlint sprint-work/E.15/.github/workflows/testing.yml
}
