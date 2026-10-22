#!/usr/bin/env bash
source "$(dirname "$0")/cicd-oracle-lifecycle-common.sh"
section_options D "$@"
need_section C
resume_completed
helper checkpoint --run "$RUN_ID" --section D --status in-progress --value 'X3 retained explicit-declaration admission'
ARCHIVE="$(helper artifact-path --run "$RUN_ID")"
# Rebind after observed successful delivery; the old pre-deploy target state is stale.
helper bind --run "$RUN_ID" --role upgrade --file "$ARCHIVE"
helper admit --run "$RUN_ID" --role upgrade --file "$ARCHIVE"
helper negative --run "$RUN_ID" --file "$ARCHIVE"
pause_for 'Inspect the unchanged-target negative receipt, native artifact hash and declaration. Explain what E.1 validator reuse proves and what native dependency/drift/recovery controls remain unqualified.'
record_complete 'Allowed declaration and real-target negative admission; explicit custom bridge, not native dependency enforcement'
