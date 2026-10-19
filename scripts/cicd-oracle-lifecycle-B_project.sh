#!/usr/bin/env bash
source "$(dirname "$0")/cicd-oracle-lifecycle-common.sh"
section_options B "$@"
need_section A
if [[ "$RETRY" = verify ]]; then
  helper project --run "$RUN_ID" --value verify
  exit
fi
if [[ "$RETRY" = capture ]]; then
  helper project --run "$RUN_ID" --value export
  echo 'New capture is unaccepted; review/commit and regenerate downstream evidence explicitly.'
  exit
fi
resume_completed
helper checkpoint --run "$RUN_ID" --section B --status in-progress --value 'X1 native PROJECT lifecycle'
# SQLcl 25.3 stage/verify disagree on slash-containing branch directories.
# This local experiment uses a recorded slashless branch; the product checkout
# retains its normal codex/ branch convention.
git -C "$RUN_PATH/repo" checkout -b e2-initial
helper project --run "$RUN_ID" --value stage:e2-empty-base
helper project --run "$RUN_ID" --value custom:seed
helper project --run "$RUN_ID" --value mapping-hook
pause_for 'Review exported inventory, native generated distribution, mapping hook and intentional seed SQL. Confirm no private Working Copies, ownership tables or runtime business rows were captured.'
helper project --run "$RUN_ID" --value 'commit:feat: reviewed initial native distribution'
assess_candidate() {
  local version="$1" base="$2" native_verify=passed
  if ! helper project --run "$RUN_ID" --value "verify:$base"; then
    native_verify=failed
    helper checkpoint --run "$RUN_ID" --section B --status observation --value "Native verify failed for $version: formal release remains blocked. Assessing a prerelease artifact is not a verification waiver."
  fi
  helper project --run "$RUN_ID" --value "artifact:$version-candidate"
  ARCHIVE="$(helper artifact-path --run "$RUN_ID")"
  helper bind --run "$RUN_ID" --role fresh --file "$ARCHIVE"
  helper deploy --run "$RUN_ID" --role fresh --file "$ARCHIVE"
  helper qualify --run "$RUN_ID" --file "$ARCHIVE"
  helper bind --run "$RUN_ID" --role upgrade --file "$ARCHIVE"
  helper deploy --run "$RUN_ID" --role upgrade --file "$ARCHIVE"
  if [[ "$version" = 1.0.0 ]]; then helper sentinel --run "$RUN_ID" --role upgrade; fi
  helper preservation --run "$RUN_ID" --role upgrade
  helper bind --run "$RUN_ID" --role upgrade --file "$ARCHIVE"
  helper deploy --run "$RUN_ID" --role upgrade --file "$ARCHIVE"
  helper preservation --run "$RUN_ID" --role upgrade
  if [[ "$native_verify" = passed ]]; then
    helper project --run "$RUN_ID" --value "release:$version"
    helper project --run "$RUN_ID" --value "commit:chore: freeze qualified native release $version"
    helper project --run "$RUN_ID" --value "artifact:$version"
    ARCHIVE="$(helper artifact-path --run "$RUN_ID")"
    # Release changes paths/bytes: never transfer qualification to new bytes.
    helper new-fresh --run "$RUN_ID"
    helper bind --run "$RUN_ID" --role fresh --file "$ARCHIVE"
    helper deploy --run "$RUN_ID" --role fresh --file "$ARCHIVE"
    helper qualify --run "$RUN_ID" --file "$ARCHIVE"
    helper bind --run "$RUN_ID" --role upgrade --file "$ARCHIVE"
    helper deploy --run "$RUN_ID" --role upgrade --file "$ARCHIVE"
    helper preservation --run "$RUN_ID" --role upgrade
  fi
}
assess_candidate 1.0.0 e2-empty-base
git -C "$RUN_PATH/repo" branch e2-initial-baseline
git -C "$RUN_PATH/repo" checkout -b e2-patch
pause_for 'In Main App Builder change page 1 title to E2 Hello patch and application version to 1.0.1. Save.'
helper titles --run "$RUN_ID" --role author --value 'E2 Hello patch'
helper sql --run "$RUN_ID" --role author --file tests/sql/oracle_lifecycle/author_patch.sql
helper contract-patch --run "$RUN_ID"
helper project --run "$RUN_ID" --value export
helper project --run "$RUN_ID" --value 'commit:fix: reviewed application and additive schema change'
helper project --run "$RUN_ID" --value stage:e2-initial-baseline
helper project --run "$RUN_ID" --value custom:patch
pause_for 'Review patch source/distribution and intentional data change. Confirm retained history and user settings are not replacement data.'
helper project --run "$RUN_ID" --value 'commit:fix: reviewed native patch distribution'
helper new-fresh --run "$RUN_ID"
assess_candidate 1.0.1 e2-initial-baseline
record_complete 'Initial/patch candidate observations. Native release is qualified only if the retained full verify and freeze receipts pass; a failed verify is an explicit assessment finding.'
