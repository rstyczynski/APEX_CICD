#!/usr/bin/env bash
source "$(dirname "$0")/cicd-oracle-lifecycle-common.sh"
section_options C "$@"
need_section B
if [[ "$RETRY" = verify ]]; then
  helper titles --run "$RUN_ID" --role author --value 'E2 Hello working copy|E2 History Main'
  exit
fi
if [[ "$RETRY" = capture ]]; then
  helper project --run "$RUN_ID" --value export
  echo 'Capture changed; downstream artifacts/qualification must be regenerated after review.'
  exit
fi
if [[ "$RETRY" = gui ]]; then
  pause_for 'Inspect the retained Working Copy observation ledger and reopen Compare/Refresh/Merge in Builder. Record actual new observations before any mutation.'
  exit
fi
resume_completed
helper checkpoint --run "$RUN_ID" --section C --status in-progress --value 'X2 Working Copies into the common PROJECT repository'
git -C "$RUN_PATH/repo" branch e2-before-working-copy
git -C "$RUN_PATH/repo" checkout -b e2-working-copy
helper shared-probe --run "$RUN_ID"
pause_for 'Follow the Working Copies chapter in progress/E.2/user_manual.md. Create the owned Working Copy and record its real assigned application ID.'
read -r -p 'Working Copy application ID: ' WORKING_COPY_ID
[[ "$WORKING_COPY_ID" =~ ^[0-9]+$ ]] || { echo 'Invalid Working Copy ID' >&2; exit 2; }
helper shared-scope --run "$RUN_ID" --value "$WORKING_COPY_ID"
pause_for 'Observe shared-schema results; change page 1 title in the copy and page 2 title in Main; compare, refresh and merge selected changes. Record screenshots, selections, operator actions and reasoning. Also exercise stale same-page replacement/recovery, deletion handling and abandonment in the expendable copy.'
helper titles --run "$RUN_ID" --role author --value 'E2 Hello working copy|E2 History Main'
helper shared-probe --run "$RUN_ID" --value remove
helper stable-capture --run "$RUN_ID"
helper project --run "$RUN_ID" --value 'commit:feat: reviewed Working Copy team checkpoint from Main'
helper project --run "$RUN_ID" --value stage:e2-before-working-copy
pause_for 'Review native staging and confirm only Main, not a private Working Copy, is in the captured application inventory.'
helper project --run "$RUN_ID" --value 'commit:feat: reviewed native Working Copy checkpoint distribution'
if ! helper project --run "$RUN_ID" --value verify:e2-before-working-copy; then
  helper checkpoint --run "$RUN_ID" --section C --status observation --value 'Full native verify failed: prerelease assessment only, no formal release'
fi
helper project --run "$RUN_ID" --value artifact:1.0.1-working-copy-candidate
ARCHIVE="$(helper artifact-path --run "$RUN_ID")"
helper new-fresh --run "$RUN_ID"
helper bind --run "$RUN_ID" --role fresh --file "$ARCHIVE"
helper deploy --run "$RUN_ID" --role fresh --file "$ARCHIVE"
helper qualify --run "$RUN_ID" --file "$ARCHIVE"
helper titles --run "$RUN_ID" --role fresh --value 'E2 Hello working copy|E2 History Main'
helper behavior --run "$RUN_ID" --role fresh
helper identities --run "$RUN_ID" --role upgrade --value before
helper bind --run "$RUN_ID" --role upgrade --file "$ARCHIVE"
helper deploy --run "$RUN_ID" --role upgrade --file "$ARCHIVE"
helper preservation --run "$RUN_ID" --role upgrade
helper behavior --run "$RUN_ID" --role upgrade
helper identities --run "$RUN_ID" --role upgrade --value after
helper lower-compare --run "$RUN_ID"
helper titles --run "$RUN_ID" --role fresh --value 'E2 Hello working copy|E2 History Main'
helper behavior --run "$RUN_ID" --role fresh
pause_for 'Inspect both reconstructed headings and shared LOV/greeting behavior. Record any missing edit or failure explicitly; compare the native and lower-level paths from the same accepted Main state.'
record_complete 'Working Copy/Main observations, checkpoint captures and bounded reconstructions; read the ledger for actual limits'
