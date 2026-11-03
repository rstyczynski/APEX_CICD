test_IT1_manual_release() (
  set -euo pipefail
  local evidence=progress/E.3/tests/native-journey.json repository=rstyczynski/APEX_CICD_E3
  local tag run source archive hash pr notes
  tag=$(jq -er .version_tag "$evidence")
  run=$(jq -er .deploy_run "$evidence")
  source=$(jq -er .source_sha "$evidence")
  for pr in $(jq -r '.change_pr,.release_pr' "$evidence"); do
    gh api "repos/$repository/pulls/$pr" | jq -e '.merged == true and .base.ref == "main"' > /dev/null
  done
  gh api "repos/$repository/actions/runs/$run" | jq -e '.conclusion == "success" and .event == "workflow_dispatch"' > /dev/null
  test "$(git -C .local-apex/e3/repo rev-parse "$tag^{commit}")" = "$source"
  archive=".local-apex/e3/native-download/artifact/e3-${tag#v}.zip"
  hash=$(shasum -a 256 "$archive" | cut -d ' ' -f1)
  jq -e --arg hash "$hash" --arg source "$source" '.artifact_sha256 == $hash and .source_sha == $source and .history_configuration_preserved == true and .controller == "GitHub Actions"' .local-apex/e3/native-download/result/receipt.json > /dev/null
  gh release view "$tag" --repo "$repository" --json body --jq .body > .local-apex/e3/native-release-notes.txt
  git -C .local-apex/e3/repo show "$tag:CHANGELOG.md" > .local-apex/e3/native-changelog.txt
  node -e 'const f=require("fs");if(!f.readFileSync(process.argv[1],"utf8").includes(f.readFileSync(process.argv[2],"utf8").trim()))process.exit(1)' .local-apex/e3/native-changelog.txt .local-apex/e3/native-release-notes.txt
  test -z "$(git -C .local-apex/e3/repo ls-tree -r --name-only "$tag" | rg '\.py$' || true)"
  source .local-apex/e3/native.env
  "$SQLCL" -nohistory -noupdates -home "$SQLCL_HOME" -S -L /nolog @examples/git-pipeline/sql/snapshot.sql "$PWD/.local-apex/e3/native-current.txt" > .local-apex/e3/logs/native-current.log 2>&1
  cmp .local-apex/e3/native-preservation-before.txt .local-apex/e3/native-current.txt
  echo 'PASS native selected-tag workflow, release notes/changelog, archive identity and current preservation'
)

test_IT2_verification_blocks_deploy() (
  set -euo pipefail
  local scratch tag log missing code=0
  source .local-apex/e3/native.env
  tag=$(jq -er .version_tag progress/E.3/tests/native-journey.json)
  scratch=$(mktemp -d "$PWD/.local-apex/e3/native-rejection.XXXXXX")
  log="$scratch/verify.log"
  "$SQLCL" -nohistory -noupdates -home "$SQLCL_HOME" -S -L /nolog @examples/git-pipeline/sql/snapshot.sql "$scratch/before.txt" > "$scratch/before.log" 2>&1
  git clone --quiet --no-hardlinks .local-apex/e3/repo "$scratch/repo"
  git -C "$scratch/repo" checkout --quiet -b e3-rejection "$tag"
  missing=$(find "$scratch/repo/dist/releases/next/changes" -name '*.sql' -type f -print -quit)
  test -n "$missing"
  rm "$missing"
  (
    cd "$scratch/repo"
    git branch -f e3-base "$(jq -er .baseline_sha pipeline.json)"
    "$SQLCL" -nohistory -noupdates -home "$SQLCL_HOME" -S -L /nolog @sql/verify.sql > "$log" 2>&1
    grep -Eq 'Errors:[[:space:]]*0([^0-9]|$)' "$log"
  ) || code=$?
  test "$code" -ne 0
  grep -Eq 'stagechangelogfilesvalid|stagechangelogcomplete' "$log"
  "$SQLCL" -nohistory -noupdates -home "$SQLCL_HOME" -S -L /nolog @examples/git-pipeline/sql/snapshot.sql "$scratch/after.txt" > "$scratch/after.log" 2>&1
  cmp "$scratch/before.txt" "$scratch/after.txt"
  sed -E $'s/\033\\[[0-9;]*m//g; s/[[:space:]]+$//' "$log" | sed '${/^$/d;}' > progress/E.3/tests/native-only-rejection.log
  jq -n '{native_verification_failed:true,target_unchanged:true,deployment_called:false,engine:"SQLcl PROJECT"}' > progress/E.3/tests/native-only-rejection.json
  echo 'PASS native verification blocks missing changeset; no deployment; target unchanged'
)
