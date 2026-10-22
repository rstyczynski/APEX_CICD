-- Compare every business field before browser checks create any new rows.
set serveroutput on
declare
  l_after clob;
  l_equal number;
begin
  if user not in ('E1_INTEGRATION','E1_UAT') then raise_application_error(-20888,'Wrong preservation target'); end if;
  if :F2_BEFORE is null or :F2_OWNER is null or :F2_OWNER<>user then
    raise_application_error(-20889,'Missing same-session target baseline; do not recapture after deployment');
  end if;
  select json_object('history' value (select coalesce(json_arrayagg(json_object(*) order by greeting_id returning clob),to_clob('[]')) from greeting_history) format json,
'hello_entries' value (select coalesce(json_arrayagg(json_object(*) order by entry_id returning clob),to_clob('[]')) from hello_entries) format json,
'world_entries' value (select coalesce(json_arrayagg(json_object(*) order by entry_id returning clob),to_clob('[]')) from world_entries) format json,
'hello_config' value (select coalesce(json_arrayagg(json_object(*) order by config_id returning clob),to_clob('[]')) from hello_config) format json,
'world_config' value (select coalesce(json_arrayagg(json_object(*) order by config_id returning clob),to_clob('[]')) from world_config) format json returning clob) into l_after from dual;
  select case when json_equal(:F2_BEFORE,l_after error on error) then 1 else 0 end into l_equal from dual;
  if l_equal<>1 then raise_application_error(-20890,'Business fields changed during deployment; inspect'); end if;
  dbms_output.put_line('PASS exact business fields unchanged by deployment in '||user);
end;
/
