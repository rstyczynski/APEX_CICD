test_SM1_platform() {
  python3 scripts/apex_sql.py --version | rg -q '25.3.0.274.1210'
  python3 scripts/cicd-platform.py check
  bash scripts/apex-verify.sh
}
