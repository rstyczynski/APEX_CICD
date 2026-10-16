whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set define on verify off serveroutput on
set sqlformat csv
select user as connected_schema,sys_context('USERENV','CON_NAME') as pdb from dual;
select workspace_name,schema from apex_workspace_schemas
where workspace_name='&2' and schema='&1';
declare n number;
begin
  if user<>'&1' or sys_context('USERENV','CON_NAME')<>'FREEPDB1' then
    raise_application_error(-20010,'Wrong target schema or PDB');
  end if;
  select count(*) into n from apex_workspace_schemas where workspace_name='&2' and schema='&1';
  if n<>1 then raise_application_error(-20011,'Wrong workspace mapping'); end if;
  dbms_output.put_line('Target identity verified.');
end;
/
