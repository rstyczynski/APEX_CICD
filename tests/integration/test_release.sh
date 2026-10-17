test_IT1_release() {
  # Full IT-1 includes additive upgrade and reconstruction beyond the initial subcase.
  echo 'IT-1 full upgrade/reconstruction acceptance pending; initial result uses initial_release.manifest' >&2
  return 1
}
test_IT2_patch() {
  local archive
  archive="$(cat .local-apex/releases/patch-selected.txt)"
  bash scripts/cicd-patch-result.sh lab-qualify
  bash scripts/cicd-patch-result.sh lab-test
  python3 scripts/cicd-preservation.py compare lab-qualify .local-apex/releases/qualification-initial-preservation.json
  python3 scripts/cicd-preservation.py compare lab-test .local-apex/releases/test-initial-preservation.json
  python3 scripts/apex_sql.py lab-test tests/sql/hello_patch.sql
  python3 scripts/apex_sql.py lab-control tests/sql/patch_receipts.sql
  echo 'PASS IT-2: same patch qualified fresh/from initial, promoted, repeat checked without writes; retained fields and behavior verified.'
}

# Bounded IT-1 initial-install evidence; full upgrade/reconstruction remains pending above.
test_IT1_initial_result() {
  local archive work hash
  archive="$(cat .local-apex/releases/initial-selected.txt)"
  work="$(mktemp -d .local-apex/releases/initial-check.XXXXXX)"
  hash="$(shasum -a 256 "$archive" | awk '{print $1}')"
  python3 scripts/apex_sql.py lab-test tests/sql/initial_preservation_snapshot.sql > "$work/before.txt"
  bash scripts/cicd-qualify.sh "$archive" > "$work/qualify.log" 2>&1
  bash scripts/cicd-promote.sh "$archive" lab-test > "$work/test.log" 2>&1
  rg -q 'ALREADY DELIVERED' "$work/qualify.log"
  rg -q 'ALREADY DELIVERED' "$work/test.log"
  python3 scripts/apex_sql.py lab-test tests/sql/prepare_history_sentinels.sql > "$work/fixture-repeat.log"
  python3 scripts/apex_sql.py lab-test tests/sql/initial_preservation_snapshot.sql > "$work/after.txt"
  cmp "$work/before.txt" "$work/after.txt"
  cat > "$work/receipts.sql" <<SQL
set serveroutput on
declare n number; begin
 select count(*) into n from e1_release_targets where schema_name in ('E1_QUALIFY','E1_TEST') and phase='ready' and owner_name is null and artifact_hash='$hash';
 if n<>2 then raise_application_error(-20760,'Both targets must publish the same archive'); end if;
 select count(*) into n from e1_release_attempts where artifact_hash='$hash' and outcome='succeeded';
 if n<>2 then raise_application_error(-20761,'Two successful receipts required'); end if;
 select count(*) into n from e1_qualified_artifacts where artifact_hash='$hash';
 if n<>1 then raise_application_error(-20762,'Qualification receipt required'); end if;
 dbms_output.put_line('PASS initial same-artifact receipts');
end;
/
SQL
  python3 scripts/apex_sql.py lab-control "$work/receipts.sql" > "$work/receipts.log"
  echo "PASS initial receipts, live fingerprints, repeat no-op and all retained history/configuration fields. Evidence: $work"
}
