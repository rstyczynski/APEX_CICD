test_SM1_pipeline_contract() {
  local example=examples/git-pipeline label title labels
  actionlint -config-file "$example/.github/actionlint.yaml" "$example"/.github/workflows/*.yml
  while IFS='|' read -r label title; do
    jq -n --arg label "$label" --arg title "$title" '{labels:[{name:$label}],title:$title,user:{login:"developer"},head:{ref:"change"}}' |
      jq -er -f "$example/.github/pr-policy.jq" > /dev/null
  done <<'CASES'
patch|fix: update Home heading
minor|feat: add greeting
major|feat!: replace contract
patch|fix(home): title
CASES
  while IFS='|' read -r labels title; do
    if jq -n --arg labels "$labels" --arg title "$title" '{labels:($labels|split(",")|map({name:.})),title:$title,user:{login:"developer"},head:{ref:"change"}}' |
      jq -er -f "$example/.github/pr-policy.jq" > /dev/null 2>&1; then
      echo 'FAIL invalid PR classification accepted'; return 1
    fi
  done <<'CASES'
|fix: title
patch,minor|fix: title
patch|feat: title
major|feat: title
minor|feat!: title
CASES
  test -z "$(find "$example" -name '*.py' -print -quit)"
  ! rg -n 'python|scripts/(lab|release|capture)' "$example/.github" "$example/sql"
  test "$(rg -c '^  workflow_dispatch:' "$example/.github/workflows/release.yml")" = 1
  ! rg '^  (push|pull_request|release):' "$example/.github/workflows/release.yml"
  rg -q 'project export' "$example/sql/capture.sql"
  rg -q 'project stage' "$example/sql/stage.sql"
  rg -q 'project verify' "$example/sql/verify.sql"
  rg -q 'project gen-artifact' "$example/sql/package.sql"
  rg -q 'project deploy' "$example/sql/deploy.sql"
  echo 'PASS native workflow boundary and 9 PR classification cases'
}
