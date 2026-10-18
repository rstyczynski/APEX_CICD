set serveroutput on
declare q e1_release_targets%rowtype; t e1_release_targets%rowtype; n number;
begin
 select * into q from e1_release_targets where schema_name='E1_INTEGRATION';
 select * into t from e1_release_targets where schema_name='E1_UAT';
 if q.phase<>'ready' or t.phase<>'ready' or q.artifact_hash<>t.artifact_hash or q.source_commit<>t.source_commit or q.config_hash<>t.config_hash then
  raise_application_error(-20785,'Qualification/TEST patch identity differs');
 end if;
 select count(*) into n from e1_patch_qualifications where artifact_hash=t.artifact_hash and source_commit=t.source_commit and config_hash=t.config_hash and starting_state in ('empty','1.0.0');
 if n<>2 then raise_application_error(-20786,'Fresh and baseline-upgrade qualification required'); end if;
 select count(*) into n from e1_release_attempts where schema_name='E1_UAT' and epoch=t.epoch and artifact_hash=t.artifact_hash and outcome='succeeded' and starting_state='1.0.0';
 if n<>1 then raise_application_error(-20787,'Retained TEST upgrade receipt missing'); end if;
 dbms_output.put_line('PASS two patch qualification starts and successful same-artifact TEST upgrade receipt.');
end;
/
