#!/usr/bin/env bash
source "$(dirname "$0")/cicd-oracle-lifecycle-common.sh"
section_options E "$@"
need_section D
resume_completed
helper checkpoint --run "$RUN_ID" --section E --status in-progress --value 'Findings, roadmap and reproducible live inspection'
helper inspect --run "$RUN_ID"
pause_for 'Open progress/E.2/sprint_E.2_increment_demo.md and the matching PPTX. Inspect classified findings, source/evidence links, reconciled backlog and dependency-ordered roadmap. Walk through the actual retained results and a repeatable failure. Record Product Owner feedback in the handover document; runner completion cannot accept or close the sprint.'
record_complete 'Walkthrough inspection performed; Product Owner handover decision remains in the handover document'
