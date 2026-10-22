#!/usr/bin/env bash
source "$(dirname "$0")/cicd-oracle-lifecycle-common.sh"
section_options A "$@"
if [[ ! -f "$RUN_PATH/inventory.json" ]]; then
  [[ -z "$RETRY" && -z "$CONTINUE" ]] || { echo 'No existing run to continue.' >&2; exit 1; }
  helper preflight
  helper init --run "$RUN_ID"
fi
resume_completed
helper checkpoint --run "$RUN_ID" --section A --status in-progress --value 'Own resources, fixture and PROJECT repository'
helper provision --run "$RUN_ID"
helper fixture --run "$RUN_ID"
helper inspect --run "$RUN_ID" --section A
pause_for 'Open App Builder in this run author workspace as E2DEV. Create E2 Lifecycle with Home (page 1) and an interactive report E2 History (page 2) over E2_HISTORY. Add shared LOV E2 Greeting Words using SELECT SETTING_VALUE d, SETTING_KEY r FROM E2_SETTINGS WHERE SETTING_KEY IN (HELLO,WORLD); use quoted SQL string values. Do not include supporting objects. Password stays in the private run file.'
read -r -p 'Enter the actual Main application ID just created: ' MAIN_APP_ID
[[ "$MAIN_APP_ID" =~ ^[0-9]+$ ]] || { echo 'Invalid app ID' >&2; exit 2; }
helper app --run "$RUN_ID" --value "$MAIN_APP_ID"
helper project --run "$RUN_ID" --value export
helper project --run "$RUN_ID" --value 'commit:feat: reviewed initial Main and schema checkpoint'
record_complete 'Owned fixture and initial PROJECT capture; GUI creation explicitly observed'
