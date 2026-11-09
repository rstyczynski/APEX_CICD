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
  ! rg -n '\.local-apex|native\.env|\$SQLCL"' "$example/.github" "$example/sql"
  rg -q 'environment: e3-lab' "$example/.github/workflows/release.yml"
  rg -q 'actions/setup-java@' "$example/.github/actions/setup-native/action.yml"
  rg -q 'GITHUB_PATH' "$example/.github/actions/setup-native/action.yml"
  rg -q 'secrets.TARGET_PASSWORD' "$example/.github/workflows/release.yml"
  ! rg 'project deploy|sql/deploy.sql' "$example/.github/workflows/qualification.yml"
  test "$(rg -c '^  workflow_dispatch:' "$example/.github/workflows/release.yml")" = 1
  ! rg '^  (push|pull_request|release):' "$example/.github/workflows/release.yml"
  rg -q 'project export' "$example/sql/capture.sql"
  rg -q 'project stage' "$example/sql/stage.sql"
  rg -q 'project verify' "$example/sql/verify.sql"
  rg -q 'project gen-artifact' "$example/sql/package.sql"
  rg -q 'project deploy' "$example/sql/deploy.sql"
  echo 'PASS native workflow boundary and 9 PR classification cases'
}


test_SM58_native_release_boundary() {
  local scratch original=$PWD
  scratch=$(mktemp -d "${TMPDIR:-/tmp}/apex-native-release.XXXXXX")
  (
    set -e
    . "$original/examples/git-pipeline/.github/assert-native-release.sh"
    cd "$scratch"
    git init -q
    mkdir -p .dbtools dist/releases/1.0.5
    printf '1.0.5\n' > version.txt
    printf '{"lastReleaseVersion":""}\n' > .dbtools/project.config.json
    printf '<databaseChangeLog/>\n' > dist/releases/1.0.5/release.changelog.xml
    git add .
    git -c user.name=Test -c user.email=test@example.invalid commit -qm fixture
    if assert_native_release 1.0.5; then echo 'Unfrozen release accepted'; exit 1; fi
    printf '{"lastReleaseVersion":"1.0.5"}\n' > .dbtools/project.config.json
    git add .
    git -c user.name=Test -c user.email=test@example.invalid commit -qm frozen
    assert_native_release 1.0.5
    if assert_native_release 1.0.6; then echo 'Wrong version accepted'; exit 1; fi
    if assert_native_release '../next'; then echo 'Unsafe version accepted'; exit 1; fi
    rm dist/releases/1.0.5/release.changelog.xml
    if assert_native_release 1.0.5; then echo 'Missing distribution accepted'; exit 1; fi
    git restore .
    printf 'dirty\n' >> version.txt
    if assert_native_release 1.0.5; then echo 'Dirty release accepted'; exit 1; fi
  )
  local result=$?
  rm -rf -- "$scratch"
  ((result == 0)) || return "$result"
  rg -q 'skip-github-release: true' examples/git-pipeline/.github/workflows/version.yml
  rg -q 'project release -version &1' examples/git-pipeline/sql/release.sql
  rg -q 'assert_native_release' examples/git-pipeline/.github/workflows/release.yml
  echo 'PASS frozen release accepted; unfrozen, mismatched, unsafe, missing and dirty inputs rejected'
}

test_E4_SM1_native_artifact() {
  local evidence=progress/E.4/tests expected actual
  expected=$(jq -er .archive_sha256 "$evidence/release-artifact.json")
  actual=$(shasum -a 256 "$evidence/e3-1.0.7.zip" | cut -d ' ' -f1)
  test "$actual" = "$expected"
  unzip -p "$evidence/e3-1.0.7.zip" releases/apex/f810003/f810003.sql |
    node -e 'let s="";process.stdin.on("data",x=>s+=x);process.stdin.on("end",()=>{for(const x of ["E4 A: Select Hello and World values, then record the greeting.","World entries - selected C","Hello World - Git pipeline no.2"])if(!s.includes(x))throw Error(x);if(s.includes("Hello entries - deferred B"))throw Error("B leaked");})'
  ! unzip -Z1 "$evidence/e3-1.0.7.zip" | grep -q '/e4-b/'
  for log in author-a-stage-verify.log author-b-stage-verify.log author-c-stage-verify.log integration-restage-verify.log frozen-native-verify.log; do
    test -s "$evidence/$log"
    grep -q '25.4.1.022.0618' "$evidence/$log"
    grep -Eq 'Errors:[[:space:]]*0([^0-9]|$)' "$evidence/$log"
  done
  echo 'PASS E4 archive bytes, selected content and native verification transcripts; evidence reader, no target operation'
}
