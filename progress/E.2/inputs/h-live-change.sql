-- A native APEX attribute change, made outside PROJECT delivery.
set serveroutput on
begin
  if not ((user='E1_UAT' and :H_APP=810005) or
          (user='E1_INTEGRATION' and :H_APP=810004)) or :H_APP is null or :H_HISTORY is null then
    raise_application_error(-20901,'Missing matching H baseline');
  end if;
  apex_util.set_workspace(user);
  if apex_application_admin.get_global_notification(:H_APP) is not null then
    raise_application_error(-20902,'Notification changed since baseline; do not overwrite');
  end if;
  apex_application_admin.set_global_notification(
    p_application_id=>:H_APP,
    p_global_notification_message=>'H: live change outside release delivery');
  commit;
  if apex_application_admin.get_global_notification(:H_APP)<>'H: live change outside release delivery' then
    raise_application_error(-20904,'Native live change did not take effect');
  end if;
  dbms_output.put_line('OBSERVED native APEX live change: H: live change outside release delivery');
end;
/
