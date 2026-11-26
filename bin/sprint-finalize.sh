#!/usr/bin/env bash
# Run explicitly from this checkout, even when invoked from another directory.

sprint=""
extra_prompt=""

usage() {
    cat <<'USAGE'
Usage: sprint-finalize.sh --sprint ID [--extra-prompt TEXT]

  --sprint ID          Sprint to complete (required).
  --extra-prompt TEXT  Additional instructions for this sprint; may be repeated.
  -h, --help          Show this help.
USAGE
}

while [ "$#" -gt 0 ]; do
    case "$1" in
        --sprint|--extra-prompt)
            if [ "$#" -lt 2 ] || [ -z "$2" ]; then
                printf 'Option %s requires a nonempty value.\n' "$1" >&2
                exit 2
            fi
            case "$1" in
                --sprint) sprint="$2" ;;
                --extra-prompt)
                    if [ -n "$extra_prompt" ]; then
                        extra_prompt+=$'\n\n'
                    fi
                    extra_prompt+="$2"
                    ;;
            esac
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            printf 'Unknown option: %s\n' "$1" >&2
            usage >&2
            exit 2
            ;;
    esac
done

if [ -z "$sprint" ]; then
    printf 'Option --sprint is required.\n' >&2
    usage >&2
    exit 2
fi

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd) || exit 1
cd "$project_root" || exit 1

# Templates are plain text. Replace only the supported placeholders; never eval.
master_file="$project_root/etc/sprint-finalize-master.prompt"
retry_file="$project_root/etc/sprint-finalize-retry.prompt"
for template_file in "$master_file" "$retry_file"; do
    if [ ! -r "$template_file" ] || [ ! -s "$template_file" ]; then
        printf 'Prompt template is unreadable or empty: %s\n' "$template_file" >&2
        exit 1
    fi
done
master_template=$(cat "$master_file") || exit 1
retry_template=$(cat "$retry_file") || exit 1
prompt=${master_template//'${sprint}'/"$sprint"}

if [ -n "$extra_prompt" ]; then
    prompt+="

Additional instructions for Sprint ${sprint}:
${extra_prompt}"
fi

for command_name in codex-cli tee awk; do
    if ! command -v "$command_name" >/dev/null 2>&1; then
        printf 'Required command not found: %s\n' "$command_name" >&2
        exit 1
    fi
done

# release codex threads / chat session
codex-cli --broker stop

run_dir=$(mktemp -d "${TMPDIR:-/tmp}/sprint-finalize.XXXXXX") || exit 1
state_file="$run_dir/thread.json"
max_attempts=10

next_prompt="$prompt"
new_chat=(--new)

printf 'Logs: %s\n' "$run_dir" >&2

for ((attempt = 1; attempt <= max_attempts; attempt++)); do
    output_file="$run_dir/attempt-$attempt.txt"
    answer_file="$run_dir/attempt-$attempt-last-answer.txt"

    printf '\nAttempt %s/%s\n\n' "$attempt" "$max_attempts" >&2

    # Use codex-cli directly: hiai forces agentic output mode.
    # stdin remains attached to the terminal.
    # stderr remains live; stdout is displayed live and saved.
    if codex-cli --broker \
        "${new_chat[@]}" \
        --state "$state_file" \
        --interactive false \
        --approval accept \
        --approval-command accept \
        --approval-file accept \
        --approval-permissions accept \
        --json false \
        --agentic-error-code false \
        --debug false \
        --interim true \
        --progress true \
        --timeout 86400 \
        --prompt "$next_prompt" |
        tee "$output_file"
    then
        statuses=("${PIPESTATUS[@]}")
    else
        statuses=("${PIPESTATUS[@]}")
    fi

    rc=${statuses[0]}
    log_rc=${statuses[1]}

    if [ "$log_rc" -ne 0 ]; then
        printf '\nCould not save output. Logs: %s\n' "$run_dir" >&2
        exit "$log_rc"
    fi

    # Extract the final answer, excluding earlier progress messages.
    awk '
        {
            sub(/\r$/, "")
        }
        /^Sprint result:[[:space:]]*$/ {
            answer = ""
            found = 1
        }
        found {
            answer = answer $0 ORS
        }
        END {
            if (found) printf "%s", answer
        }
    ' "$output_file" > "$answer_file"

    final_line=$(awk '
        NF {
            sub(/\r$/, "")
            last = $0
        }
        END {
            print last
        }
    ' "$answer_file")

    if [ "$rc" -eq 0 ] &&
       [ "$final_line" = "Sprint status: COMPLETE" ]; then
        printf '\nSprint %s completed. Logs: %s\n' \
            "$sprint" "$run_dir" >&2
        exit 0
    fi

    printf '\nLast answer (process exit %s):\n\n' "$rc" >&2

    if [ -s "$answer_file" ]; then
        cat "$answer_file" >&2
    elif [ -s "$output_file" ]; then
        printf 'No marked final answer received. Last assistant output:\n' >&2
        tail -n 40 "$output_file" >&2
    else
        printf 'No assistant answer received; see terminal diagnostics.\n' >&2
    fi

    # Do not retry after interruption.
    case "$rc" in
        130|143)
            printf '\nInterrupted. Logs: %s\n' "$run_dir" >&2
            exit "$rc"
            ;;
    esac

    if [ "$attempt" -ge "$max_attempts" ]; then
        break
    fi

    # Resume the same chat once its saved state exists.
    if [ -s "$state_file" ]; then
        new_chat=()
    fi

    next_prompt=${retry_template//'${sprint}'/"$sprint"}
    next_prompt=${next_prompt//'${rc}'/"$rc"}
    next_prompt=${next_prompt//'${prompt}'/"$prompt"}

    printf '\nRetrying in the same chat...\n' >&2
done

printf '\nStopped after %s unsuccessful attempts. Logs: %s\n' \
    "$max_attempts" "$run_dir" >&2
exit 1
