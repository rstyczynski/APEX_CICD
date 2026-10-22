-- Observe the native repeat deployment, without imposing a custom drift gate.
set serveroutput on
declare
  history_after clob;
  status_after varchar2(100);
  equal_history number;
  n number;
begin
  if not ((user='E1_UAT' and :H_APP=810005) or
          (user='E1_INTEGRATION' and :H_APP=810004)) or :H_APP is null or :H_HISTORY is null then
    raise_application_error(-20901,'Missing matching H baseline');
  end if;
  apex_util.set_workspace(user);
  if nvl(apex_application_admin.get_global_notification(:H_APP),'NULL')<>'H: live change outside release delivery' then
    raise_application_error(-20905,'Unexpected live definition after deployment; inspect');
  end if;
  select json_arrayagg(json_object(*) order by orderexecuted returning clob)
    into history_after from databasechangelog;
  select case when json_equal(:H_HISTORY,history_after error on error) then 1 else 0 end into equal_history from dual;
  if equal_history<>1 then raise_application_error(-20906,'Changeset history changed unexpectedly'); end if;
  select availability_status into status_after from apex_applications where application_id=:H_APP and owner=user;
  if status_after<>:H_STATUS or apex_application_admin.get_application_version(:H_APP)<>:H_VERSION then
    raise_application_error(-20906,'Publication/version changed unexpectedly');
  end if;
  select count(*) into n from lab_components where installed=1 and
    ((component in ('Foundation','World') and version='1.0.0') or (component='Hello' and version='1.0.1'));
  if n<>3 then raise_application_error(-20906,'Installed components changed'); end if;
  dbms_output.put_line('OBSERVED live change remains after native repeat deployment');
  dbms_output.put_line('PASS component versions, publication and changeset history unchanged');
end;
/
