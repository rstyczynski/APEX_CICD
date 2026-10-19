#!/usr/bin/env bash
# Shared options/checkpoints only. Section operations stay in A–E scripts.
set -Eeuo pipefail
ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
cd "$ROOT"
helper() { python3 "$ROOT/scripts/cicd-oracle-lifecycle.py" "$@"; }
section_options() {
  SECTION="$1"; shift
  MODE=--live RUN_ID='' CONTINUE='' RETRY=''
  while (($#)); do
    case "$1" in
      --preflight|--live|--rehearse|--inspect) MODE="$1"; shift ;;
      --run) [[ $# -ge 2 ]] || return 2; RUN_ID="$2"; shift 2 ;;
      --resume) CONTINUE=resume; shift ;;
      --retry) [[ $# -ge 2 ]] || return 2; RETRY="$2"; shift 2 ;;
      *) echo "Unknown option: $1" >&2; return 2 ;;
    esac
  done
  [[ "$RUN_ID" =~ ^[a-z][a-z0-9-]{2,40}$ ]] || { echo 'Specify --run with a lowercase run identifier.' >&2; return 2; }
  [[ -z "$RETRY" || "$RETRY" = verify || "$RETRY" = capture || "$RETRY" = gui ]] || { echo 'Supported retry steps: verify, capture, gui; mutation replay is refused.' >&2; return 2; }
  if [[ -n "$RETRY" ]]; then
    case "$SECTION:$RETRY" in
      B:verify|B:capture|C:verify|C:capture|C:gui) ;;
      *) echo "Section $SECTION does not support retry $RETRY; inspect its checkpoint." >&2; return 2 ;;
    esac
  fi
  if [[ "$MODE" = --preflight || "$MODE" = --inspect ]]; then
    [[ -z "$RETRY" && -z "$CONTINUE" ]] || { echo 'Continuation options require live/rehearse mode.' >&2; return 2; }
  fi
  RUN_PATH="$ROOT/.local-apex/e2/$RUN_ID"
  if [[ "$MODE" = --inspect ]]; then helper inspect --run "$RUN_ID" --section "$SECTION"; exit; fi
  if [[ "$MODE" = --preflight ]]; then helper preflight --run "$RUN_ID"; exit; fi
  if [[ "$MODE" = --live && ! -t 0 ]]; then echo 'Live mode requires an interactive terminal; use --rehearse for unattended-capable actions.' >&2; return 2; fi
}
need_section() {
  local previous="$1"
  [[ -f "$RUN_PATH/$previous.complete.json" ]] || { echo "BLOCKED: section $previous must complete first." >&2; return 1; }
  helper guard --run "$RUN_ID" --role author
}
pause_for() {
  local reply
  printf '\n%s\n' "$1"
  if [[ "$MODE" = --rehearse ]]; then
    echo 'BLOCKED: a real GUI observation is required here; no fresh human observation claimed.' >&2
    helper checkpoint --run "$RUN_ID" --section "$SECTION" --status blocked --value "$1"
    return 3
  fi
  read -r -p 'Complete the action; Enter to verify, q to stop: ' reply
  [[ "$reply" != q && "$reply" != Q ]] || return 130
}
record_complete() {
  helper checkpoint --run "$RUN_ID" --section "$SECTION" --status complete --value "$1"
  helper finish --run "$RUN_ID" --section "$SECTION"
}
resume_completed() {
  if [[ -f "$RUN_PATH/$SECTION.complete.json" ]]; then
    [[ "$CONTINUE" = resume || -n "$RETRY" ]] || { echo 'Section already completed; use --resume to verify it or --inspect to read evidence.' >&2; exit 1; }
    helper verify-complete --run "$RUN_ID" --section "$SECTION"
    echo 'Verified existing completion; no operation replayed and no fresh execution claimed.'
    exit
  fi
  if [[ "$CONTINUE" = resume && -f "$RUN_PATH/journal.jsonl" && "$SECTION" != A ]]; then
    echo 'A partial section is not blindly replayed. Use --retry verify/capture/gui as documented, or inspect the failed operation.' >&2
    exit 1
  fi
}
