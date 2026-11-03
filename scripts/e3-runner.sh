#!/usr/bin/env bash
# Local lab infrastructure only. GitHub workflows own tools, settings and secrets.
# Operating guide: progress/E.3/user_manual.md
set -euo pipefail
command_name=run
repository=rstyczynski/APEX_CICD_E3
runner_dir="$HOME/actions-runner-e3"
runner_name="e3-lab-$(hostname -s)"
project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)
if (($#)) && [[ "$1" != --* ]]; then command_name=$1; shift; fi
while (($#)); do
  case "$1" in
    --repo) repository=${2:?Missing repository}; shift 2 ;;
    --directory) runner_dir=${2:?Missing directory}; shift 2 ;;
    --name) runner_name=${2:?Missing name}; shift 2 ;;
    --help) printf '%s\n' 'Usage: scripts/e3-runner.sh [setup|run|preflight|status] [--repo OWNER/REPO] [--directory ABSOLUTE_PATH] [--name NAME]'; exit 0 ;;
    *) printf 'Unknown option: %s\n' "$1" >&2; exit 2 ;;
  esac
done
[[ "$repository" =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ ]]
case "$runner_dir/" in
  "$project_root/"*|*/.local-apex/*) echo 'Runner registration must be outside the checkout and .local-apex.' >&2; exit 2 ;;
  /*) ;;
  *) echo 'Use an absolute runner directory.' >&2; exit 2 ;;
esac
for dependency in gh jq; do command -v "$dependency" >/dev/null; done
check_registration() {
  test -f "$runner_dir/.runner" || { echo 'Runner is not configured. Run scripts/e3-runner.sh setup first.' >&2; return 1; }
  jq -e --arg url "https://github.com/$repository" '.gitHubUrl == $url' "$runner_dir/.runner" >/dev/null
}
preflight() {
  command -v curl >/dev/null
  command -v nc >/dev/null
  local connect endpoint authority host port
  connect=$(gh api "repos/$repository/environments/e3-lab/variables/DB_CONNECT" --jq .value)
  endpoint=$(gh api "repos/$repository/environments/e3-lab/variables/ORDS_URL" --jq .value)
  [[ "$connect" =~ ^[A-Za-z0-9.:-]+/[A-Za-z0-9._-]+$ && "$endpoint" =~ ^https?:// ]]
  authority=${connect%%/*}; host=${authority%:*}; port=${authority##*:}
  [[ "$port" =~ ^[0-9]+$ ]]
  nc -z -w 3 "$host" "$port"
  curl --fail --silent --show-error --max-time 10 --location "$endpoint/" >/dev/null
  echo 'PASS local Oracle TCP and ORDS HTTP access; settings read from GitHub e3-lab.'
}
case "$command_name" in
  setup)
    if [[ -f "$runner_dir/.runner" ]]; then
      check_registration
      echo 'Existing matching runner registration retained.'
    else
      [[ "$(uname -s)/$(uname -m)" == Darwin/arm64 ]] || { echo 'This lab installer supports macOS ARM64.' >&2; exit 2; }
      for dependency in curl tar shasum; do command -v "$dependency" >/dev/null; done
      gh api "repos/$repository" --jq .private | jq -e '. == true' >/dev/null
      if [[ -d "$runner_dir" && -n "$(ls -A "$runner_dir")" ]]; then
        echo 'Unregistered runner directory is not empty; inspect it before setup.' >&2; exit 2
      fi
      temporary=$(mktemp -d "${TMPDIR:-/tmp}/apex-runner-setup.XXXXXX")
      trap 'rm -rf "$temporary"' EXIT
      curl --fail --location --retry 3 https://github.com/actions/runner/releases/download/v2.338.2/actions-runner-osx-arm64-2.338.2.tar.gz -o "$temporary/runner.tar.gz"
      echo "25a065af409ffa317ab4d5a3b614dd15fc9c40f2172bc1b35a1b1258e919a388  $temporary/runner.tar.gz" | shasum -a 256 -c -
      mkdir -p "$runner_dir"
      chmod 700 "$runner_dir"
      tar -xzf "$temporary/runner.tar.gz" -C "$runner_dir"
      registration_token=$(gh api -X POST "repos/$repository/actions/runners/registration-token" --jq .token)
      result=0
      output=$(cd "$runner_dir" && ./config.sh --url "https://github.com/$repository" --token "$registration_token" --name "$runner_name" --labels e3-lab --work _work --unattended 2>&1) || result=$?
      printf '%s\n' "${output//"$registration_token"/[REDACTED]}"
      unset registration_token output
      ((result == 0)) || exit "$result"
      check_registration
    fi
    preflight
    echo 'Setup complete. Start with scripts/e3-runner.sh.'
    ;;
  preflight) preflight ;;
  status)
    check_registration
    gh api "repos/$repository/actions/runners" --jq '.runners[] | select(any(.labels[]; .name == "e3-lab")) | {name,status,busy}'
    ;;
  run)
    check_registration
    preflight
    # No operator token or retired tool/connection configuration enters the runner.
    unset GH_TOKEN GITHUB_TOKEN SQLCL SQLCL_HOME JAVA_HOME E3_LAB_CONFIG
    cd "$runner_dir"
    exec ./run.sh
    ;;
  *) echo 'Use setup, run, preflight or status.' >&2; exit 2 ;;
esac
