-- Read-only baseline for the selected owned application. No changes to UAT data.
set define on
set verify off
set serveroutput on
variable H_APP number
variable H_HISTORY clob
variable H_VERSION varchar2(255)
variable H_STATUS varchar2(100)
begin
  :H_APP:=&1;
  if (user='E1_UAT' and :H_APP=810005) or
     (user='E1_INTEGRATION' and :H_APP=810004) then null;
  else raise_application_error(-20901,'H requires the matching owned schema/application'); end if;
  apex_util.set_workspace(user);
  if apex_application_admin.get_global_notification(:H_APP) is not null then
    raise_application_error(-20902,'Expected no existing global notification; inspect before H');
  end if;
  select availability_status into :H_STATUS from apex_applications
    where application_id=:H_APP and owner=user;
  :H_VERSION:=apex_application_admin.get_application_version(:H_APP);
  if :H_VERSION<>'1.0.1' or :H_STATUS not in ('Available','Restricted Access') or
     (user='E1_UAT' and :H_STATUS<>'Available') then
    raise_application_error(-20903,'H requires the published F 1.0.1 application');
  end if;
  declare n number; begin
    select count(*) into n from lab_components where installed=1 and
      ((component in ('Foundation','World') and version='1.0.0') or (component='Hello' and version='1.0.1'));
    if n<>3 then raise_application_error(-20903,'H requires the F component triple'); end if;
  end;
  select json_arrayagg(json_object(*) order by orderexecuted returning clob)
    into :H_HISTORY from databasechangelog;
  dbms_output.put_line('PASS H baseline: '||user||' / '||:H_APP||' / '||:H_STATUS||' / 1.0.1 / no notification');
end;
/
