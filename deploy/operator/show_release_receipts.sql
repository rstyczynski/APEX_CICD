whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set sqlformat csv
select schema_name,epoch,phase,artifact_hash,source_commit,config_hash,fingerprint,owner_name from e1_release_targets order by schema_name;
select schema_name,epoch,starting_state,outcome,artifact_hash,started_at,finished_at from e1_release_attempts order by schema_name,epoch;
select * from e1_qualified_artifacts order by qualified_at;
