set serveroutput on
set sqlformat csv
select user as connected_schema, sys_context('USERENV','CON_NAME') as pdb from dual;
select workspace_name, schema from apex_workspace_schemas
where workspace_name='{{workspace}}' and schema='{{schema}}';
declare n number;
begin
  if user<>'{{schema}}' or sys_context('USERENV','CON_NAME')<>'FREEPDB1' then
    raise_application_error(-20010,'Wrong effective target');
  end if;
  select count(*) into n from apex_workspace_schemas
    where workspace_name='{{workspace}}' and schema='{{schema}}';
  if n<>1 then raise_application_error(-20011,'Wrong workspace/schema association'); end if;
end;
/
