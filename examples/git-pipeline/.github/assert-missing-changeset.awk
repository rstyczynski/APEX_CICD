# Assert the qualified SQLcl table diagnostic for one deliberately removed file.
# expected is a literal project-relative path selected before removing the file.
function finish_rule() {
    if (in_rule && (!missing_message || !matched_path)) invalid = 1
    in_rule = 0
}
{
    gsub(/\033\[[0-9;]*[A-Za-z]/, "")
    sub(/[[:space:]]+$/, "")
    text = $0
    sub(/^[[:space:]]+/, "", text)
    if (text ~ /^Errors:[[:space:]]*[0-9]+$/) {
        summaries++
        sub(/^Errors:[[:space:]]*/, "", text)
        reported_errors = text + 0
        next
    }
    if (text ~ /^(INFO|WARNING|WARN|ERROR)[[:space:]]/) {
        finish_rule()
        split(text, fields, /[[:space:]]+/)
        if (fields[1] == "ERROR") {
            error_rows++
            if (fields[2] != "stage" || fields[3] != "stagechangelogfilesvalid") {
                invalid = 1
            } else {
                in_rule = 1
                missing_message = matched_path = 0
                path_prefix = ""
            }
        }
    }
    if (in_rule) {
        if (text ~ /missing file/) missing_message = 1
        # Only continuation lines forming the exact expected path may join.
        if (text != "" && text !~ /^(INFO|WARNING|WARN|ERROR)[[:space:]]/) {
            candidate = path_prefix text
            if (substr(expected, 1, length(candidate)) == candidate) {
                path_prefix = candidate
            } else if (substr(expected, 1, length(text)) == text) {
                path_prefix = text
            } else {
                path_prefix = ""
            }
            if (path_prefix == expected) matched_path = 1
        }
    }
}
END {
    finish_rule()
    if (expected == "" || summaries != 1 || reported_errors < 1 ||
        error_rows != reported_errors || invalid || !matched_path) {
        print "FAIL: expected missing-changeset ERROR/count/path not established" > "/dev/stderr"
        exit 1
    }
    print "PASS native missing-changeset diagnostic: " expected
}
