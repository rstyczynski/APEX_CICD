test_SM1_platform() (
  set -euo pipefail
  local repository=rstyczynski/APEX_CICD_E3 base app scratch
  base=$(gh api "repos/$repository/environments/e3-lab/variables/ORDS_URL" --jq .value)
  app=$(gh api "repos/$repository/environments/e3-lab/variables/TARGET_APP_ID" --jq .value)
  [[ "$base" =~ ^https?:// && "$app" =~ ^[0-9]+$ ]]
  scratch=$(mktemp -d "${TMPDIR:-/tmp}/apex-platform.XXXXXX")
  trap 'rm -rf "$scratch"' EXIT
  curl --fail --silent --show-error --location --cookie-jar "$scratch/cookies" --cookie "$scratch/cookies" "$base/" > "$scratch/ords.html"
  curl --fail --silent --show-error --location --cookie-jar "$scratch/cookies" --cookie "$scratch/cookies" "$base/f?p=$app:1" > "$scratch/login.html"
  grep -q 'P9999_USERNAME' "$scratch/login.html"
  grep -q 'P9999_PASSWORD' "$scratch/login.html"
  if grep -q 'Error processing database session setup code' "$scratch/login.html"; then return 1; fi
  echo 'PASS live ORDS and database-backed APEX login; configuration read from GitHub environment'
)
