test_IT1_manual_release() (
  set -euo pipefail
  local evidence=progress/E.3/tests/github-environment-journey.json repository=rstyczynski/APEX_CICD_E3
  local scratch tag run source hash pr ref
  scratch=$(mktemp -d "${TMPDIR:-/tmp}/apex-e3-release.XXXXXX")
  trap 'rm -rf "$scratch"' EXIT
  tag=$(jq -er .version_tag "$evidence")
  run=$(jq -er .deploy_run "$evidence")
  source=$(jq -er .source_sha "$evidence")
  [[ "$tag" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ && "$run" =~ ^[0-9]+$ ]]
  for pr in $(jq -r '.change_pr,.release_pr' "$evidence"); do
    gh api "repos/$repository/pulls/$pr" | jq -e '.merged == true and .base.ref == "main"' > /dev/null
  done
  gh api "repos/$repository/actions/runs/$run" | jq -e '.conclusion == "success" and .event == "workflow_dispatch"' > /dev/null
  gh api "repos/$repository/actions/runs/$run/jobs" | jq -e '
    [.jobs[].steps[] | select(.name == "Set up native tools and job-scoped connections" or .name == "Check retained business data before publication" or .name == "Remove private job material") | .conclusion] == ["success","success","success"]' > /dev/null
  ref=$(gh api "repos/$repository/git/ref/tags/$tag" --jq .object.sha)
  test "$ref" = "$source"
  gh run download "$run" --repo "$repository" --name "e3-release-$run" --dir "$scratch"
  hash=$(shasum -a 256 "$scratch/artifact/e3-${tag#v}.zip" | cut -d ' ' -f1)
  jq -e --arg hash "$hash" --arg source "$source" '.artifact_sha256 == $hash and .source_sha == $source and .history_configuration_preserved == true and .controller == "GitHub Actions"' "$scratch/result/receipt.json" > /dev/null
  gh release view "$tag" --repo "$repository" --json body --jq .body > "$scratch/notes.txt"
  gh api "repos/$repository/contents/CHANGELOG.md?ref=$tag" -H 'Accept: application/vnd.github.raw+json' > "$scratch/changelog.txt"
  node -e 'const f=require("fs");if(!f.readFileSync(process.argv[1],"utf8").includes(f.readFileSync(process.argv[2],"utf8").trim()))process.exit(1)' "$scratch/changelog.txt" "$scratch/notes.txt"
  gh api "repos/$repository/git/trees/$source?recursive=1" | jq -e 'all(.tree[]; (.path | endswith(".py") | not))' > /dev/null
  echo 'PASS fresh GitHub evidence: explicit tool setup, selected tag/archive, changelogs, preservation and cleanup'
)

test_IT2_verification_blocks_deploy() (
  set -euo pipefail
  local scratch run repository=rstyczynski/APEX_CICD_E3 source
  scratch=$(mktemp -d "${TMPDIR:-/tmp}/apex-e3-qualification.XXXXXX")
  trap 'rm -rf "$scratch"' EXIT
  run=$(jq -er .qualification_run progress/E.3/tests/github-environment-journey.json)
  source=$(jq -er .source_sha progress/E.3/tests/github-environment-journey.json)
  [[ "$run" =~ ^[0-9]+$ ]]
  gh api "repos/$repository/actions/runs/$run" | jq -e '.conclusion == "success" and .event == "workflow_dispatch"' > /dev/null
  gh api "repos/$repository/actions/runs/$run/jobs" | jq -e '[.jobs[].steps[] | select(.name == "Remove private job material") | .conclusion] == ["success"]' > /dev/null
  gh run download "$run" --repo "$repository" --name "e3-qualification-$run" --dir "$scratch"
  jq -e --arg source "$source" '.source_sha == $source and .positive_native_verify == true and .missing_changeset_rejected == true and .target_unchanged == true and .deployment_called == false' "$scratch/qualification.json" > /dev/null
  grep -Eq 'Errors:[[:space:]]*0([^0-9]|$)' "$scratch/positive.log"
  if grep -Eq 'Errors:[[:space:]]*0([^0-9]|$)' "$scratch/negative.log"; then return 1; fi
  grep -Eq 'stagechangelogfilesvalid|stagechangelogcomplete' "$scratch/negative.log"
  echo 'PASS real native missing-changeset rejection in GitHub; target unchanged; no deployment'
)
