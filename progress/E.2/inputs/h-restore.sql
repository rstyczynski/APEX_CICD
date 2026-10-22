-- Explicitly restore only the one demonstration attribute, not an entire app.
set serveroutput on
begin
  if not ((user='E1_UAT' and :H_APP=810005) or
          (user='E1_INTEGRATION' and :H_APP=810004)) or :H_APP is null or :H_HISTORY is null then
    raise_application_error(-20901,'Missing matching H baseline');
  end if;
  apex_util.set_workspace(user);
  if nvl(apex_application_admin.get_global_notification(:H_APP),'NULL')<>'H: live change outside release delivery' then
    raise_application_error(-20907,'Unexpected notification; refuse blind restoration');
  end if;
  apex_application_admin.set_global_notification(:H_APP,null);
  commit;
  if apex_application_admin.get_global_notification(:H_APP) is not null then
    raise_application_error(-20908,'Notification restoration failed');
  end if;
  dbms_output.put_line('PASS original notification restored through native APEX API');
end;
/
