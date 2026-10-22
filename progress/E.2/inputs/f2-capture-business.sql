-- Native SQLcl session baseline, before deployment. Keep this session connected.
set serveroutput on
variable F2_BEFORE clob
variable F2_OWNER varchar2(128)
begin
  if user not in ('E1_INTEGRATION','E1_UAT') then raise_application_error(-20888,'Wrong preservation target'); end if;
  select json_object('history' value (select coalesce(json_arrayagg(json_object(*) order by greeting_id returning clob),to_clob('[]')) from greeting_history) format json,
'hello_entries' value (select coalesce(json_arrayagg(json_object(*) order by entry_id returning clob),to_clob('[]')) from hello_entries) format json,
'world_entries' value (select coalesce(json_arrayagg(json_object(*) order by entry_id returning clob),to_clob('[]')) from world_entries) format json,
'hello_config' value (select coalesce(json_arrayagg(json_object(*) order by config_id returning clob),to_clob('[]')) from hello_config) format json,
'world_config' value (select coalesce(json_arrayagg(json_object(*) order by config_id returning clob),to_clob('[]')) from world_config) format json returning clob) into :F2_BEFORE from dual;
  :F2_OWNER:=user;
  dbms_output.put_line('PASS captured all business fields before deployment in '||user);
end;
/
