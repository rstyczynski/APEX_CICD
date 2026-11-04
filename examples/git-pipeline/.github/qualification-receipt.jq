# expected_missing comes from the caller's selected file or pinned legacy case.
.source_sha == $source and (.run_id | tostring) == $run and
.positive_native_verify == true and .missing_changeset_rejected == true and
.target_unchanged == true and .deployment_called == false and
if .verification_schema == 2 then
  .missing_changeset == $expected_missing and
  (.controller_sha | type == "string") and
  (.controller_sha | test("^[0-9a-f]{40}$")) and
  (.sqlcl_version_output | type == "string" and length > 0)
else
  # Explicit compatibility only for the unchanged, recorded v1.0.4 receipt.
  (has("verification_schema") | not) and (has("missing_changeset") | not) and
  $source == "fbda57a0cbe4d32961ad826852bd04394a500c11" and
  $run == "41679432928" and
  $expected_missing == "dist/releases/next/changes/e3-initial/e1_dev_c/package_bodies/lab_runtime.sql"
end
