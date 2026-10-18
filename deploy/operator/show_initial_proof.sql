-- Historical initial proof remains available after upgrading the live targets.
set define on verify off serveroutput on sqlformat csv
declare n number;
begin
 select count(*) into n from e1_qualified_artifacts where artifact_hash='&1' and starting_state='empty';
 if n<>1 then raise_application_error(-20780,'Initial qualification receipt missing'); end if;
 select count(*) into n from e1_release_attempts where schema_name='E1_UAT' and artifact_hash='&1' and outcome='succeeded' and starting_state='empty';
 if n<>1 then raise_application_error(-20781,'Initial TEST receipt missing'); end if;
 dbms_output.put_line('VERIFIED HISTORICAL INITIAL RELEASE: same qualified/promoted bytes; current targets may be upgraded.');
end;
/
select schema_name,epoch,starting_state,outcome,artifact_hash from e1_release_attempts where artifact_hash='&1' order by schema_name,epoch;
