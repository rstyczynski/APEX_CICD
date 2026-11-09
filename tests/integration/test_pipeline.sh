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
  echo 'PASS reference seed evidence: recorded tag/archive, changelogs, preservation and cleanup; not a new LAB deployment'
)

test_IT2_verification_blocks_deploy() (
  set -euo pipefail
  local scratch run repository=rstyczynski/APEX_CICD_E3 source expected_missing
  scratch=$(mktemp -d "${TMPDIR:-/tmp}/apex-e3-qualification.XXXXXX")
  trap 'rm -rf "$scratch"' EXIT
  run=$(jq -er .qualification_run progress/E.3/tests/github-environment-journey.json)
  source=$(jq -er .source_sha progress/E.3/tests/github-environment-journey.json)
  [[ "$run" =~ ^[0-9]+$ ]]
  gh api "repos/$repository/actions/runs/$run" | jq -e '.conclusion == "success" and .event == "workflow_dispatch"' > /dev/null
  gh api "repos/$repository/actions/runs/$run/jobs" | jq -e '[.jobs[].steps[] | select(.name == "Remove private job material") | .conclusion] == ["success"]' > /dev/null
  gh run download "$run" --repo "$repository" --name "e3-qualification-$run" --dir "$scratch"
  # This reader is pinned to the unchanged legacy v1.0.4 experiment, not a replay.
  expected_missing=dist/releases/next/changes/e3-initial/e1_dev_c/package_bodies/lab_runtime.sql
  jq -e --arg source "$source" --arg run "$run" --arg expected_missing "$expected_missing" \
    -f examples/git-pipeline/.github/qualification-receipt.jq "$scratch/qualification.json" > /dev/null
  grep -Eq 'Errors:[[:space:]]*0([^0-9]|$)' "$scratch/positive.log"
  awk -v expected="$expected_missing" -f examples/git-pipeline/.github/assert-missing-changeset.awk "$scratch/negative.log"
  echo 'PASS legacy reference qualification evidence; no new defect injection, LAB qualification or deployment'
)

# Evidence reader for the freshly executed local native qualification.
# It does not claim to dispatch GitHub or repeat target writes.
test_IT58_native_release_evidence() {
  local evidence=progress/E.3/tests/release-correction receipt hash expected
  receipt="$evidence/integration.json"
  jq -e '.native_release == "1.0.5" and .native_verify_errors == 0 and .native_verify_warnings == 0 and .legacy_next_upgrade and .repeat_deployments == 1 and .history_configuration_preserved and .missing_changeset_rejected and .temporary_proxy_removed' "$receipt" > /dev/null
  expected=$(jq -er .archive_sha256 "$receipt")
  hash=$(shasum -a 256 "$evidence/e3-1.0.5.zip" | cut -d ' ' -f1)
  test "$hash" = "$expected"
  expected=$(jq -er .bundle_sha256 "$receipt")
  hash=$(shasum -a 256 examples/git-pipeline/baseline.bundle | cut -d ' ' -f1)
  test "$hash" = "$expected"
  grep -Eq 'Errors:[[:space:]]*0([^0-9]|$)' "$evidence/verify.log"
  grep -q 'Process completed successfully' "$evidence/release.log"
  grep -q 'PASS native readiness' "$evidence/supported-upgrade-accept.log"
  grep -q 'PASS native readiness' "$evidence/supported-repeat-accept.log"
  awk -v expected='dist/releases/1.0.5/changes/e3-initial/e1_dev_c/package_bodies/lab_runtime.sql' \
    -f examples/git-pipeline/.github/assert-missing-changeset.awk "$evidence/missing-changeset.log"
  echo 'PASS native release qualification evidence and archive/bundle bindings (local evidence reader)'
}

test_E4_IT1_parallel_selection_evidence() {
  local evidence=progress/E.4/tests
  node - "$evidence" <<'JS'
const fs=require('fs'),p=process.argv[2],rows=JSON.parse(fs.readFileSync(p+'/parallel-contributions.json'));
if(rows.length!==3||new Set(rows.map(x=>x.service)).size!==3)throw Error('Independent services missing');
if(Math.max(...rows.map(x=>Date.parse(x.start)))>=Math.min(...rows.map(x=>Date.parse(x.finish))))throw Error('No overlap');
if(!rows.every(x=>x.clean&&x.independent_native_processes&&x.actual_operator==='Codex role simulation'))throw Error('Provenance missing');
const release=JSON.parse(fs.readFileSync(p+'/release-branch.json'));
if(release.starting_main===release.developer_base||!rows.every(x=>x.base===release.developer_base))throw Error('Baseline scenario missing');
JS
  gh api repos/rstyczynski/APEX_CICD_E3_LAB/pulls/9 | jq -e '.merged and .base.ref=="release-e4-candidate"' > /dev/null
  gh api repos/rstyczynski/APEX_CICD_E3_LAB/pulls/10 | jq -e '.merged and .base.ref=="release-e4-candidate" and .head.sha=="8485f8149f30e2add49b8f5501755b3d80a13842"' > /dev/null
  gh api repos/rstyczynski/APEX_CICD_E3_LAB/pulls/11 | jq -e '.merged and .base.ref=="main"' > /dev/null
  gh api repos/rstyczynski/APEX_CICD_E3_LAB/git/ref/heads/e4-b | jq -e '.object.sha=="ed9fe37bbebe30306ce91e981da9b5565b44c5c5"' > /dev/null
  echo 'PASS E4 actual concurrent-process receipts, admitted PRs and preserved B remote; no replay'
}

test_E4_IT2_IT3_refusal_evidence() {
  local evidence=progress/E.4/tests
  jq -e '.decision=="REFUSE_STALE_SOURCE" and (.selected_source!=.attempted_source) and (.deploy_invoked|not) and .all_business_fields_unchanged and (.receipt_sha256_before==.receipt_sha256_after)' "$evidence/it2-refusal.json" > /dev/null
  jq -e '.decision=="REFUSE_INITIAL_BASELINE" and (.trusted_baseline_created|not) and (.deploy_invoked|not) and .all_business_fields_unchanged' "$evidence/it3a-refusal.json" > /dev/null
  jq -e '.decision=="REFUSE_DEPLOY" and (.baseline_checksum!=.live_checksum) and (.deploy_invoked|not) and .pending_title_retained and .all_business_fields_unchanged and .prior_receipt_unchanged and (.original_checksum_restored|not)' "$evidence/it3b-refusal.json" > /dev/null
  jq -e '.two_equal_reads and .business_fields_preserved and (.recovery_authorization|contains("Approve reviewed counter-only recovery"))' "$evidence/trusted-recovered-baseline.json" > /dev/null
  echo 'PASS refusal evidence; checksum restoration failed and explicitly approved narrow recovery is retained'
}

test_E4_IT4_sync_repeat_evidence() {
  node - <<'JS'
const fs=require('fs'),dir='progress/E.4/tests/',read=n=>JSON.parse(fs.readFileSync(dir+n));
const release=read('release-artifact.json'),first=read('sync-receipt.json'),repeat=read('repeat-receipt.json');
for(const [name,r] of [['sync',first],['repeat',repeat]]){
 if(r.source_sha!==release.source_sha||r.archive_sha256!==release.archive_sha256||r.status!=='Available'||!r.all_business_fields_preserved||!r.selected_A_C_verified||!r.deferred_B_absent||!r.two_equal_final_reads)throw Error(name+' receipt');
 const states=read(name+'-lifecycle.json');
 if(states.map(x=>x.stage).join(',')!=='admission,restricted-before,after-import,restricted-after,published-1,published-2')throw Error('Lifecycle missing');
 if(states[1].status!=='Restricted Access'||states[3].status!=='Restricted Access'||states[4].status!=='Available'||states[4].checksum!==states[5].checksum||r.checksum!==states[5].checksum)throw Error('Invalid final baseline');
}
if(repeat.previous_checksum!==first.checksum)throw Error('Repeat did not admit finalized baseline');
JS
  grep -q 'Operation completed successfully' progress/E.4/tests/sync-deploy.log
  grep -q 'Operation completed successfully' progress/E.4/tests/repeat-deploy.log
  echo 'PASS E4 synchronization/repeat receipts and status lifecycle; local evidence reader, no deployment replay'
}
