whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set serveroutput on
declare n number;
begin
  if user<>'E1_CTRL' then raise_application_error(-20700,'Control connection required'); end if;
  select count(*) into n from e1_reservations where owner_name is not null;
  if n<>0 then raise_application_error(-20701,'Active developer task: finish it before walkthrough cleanup'); end if;
  select count(*) into n from user_tables where table_name='E1_RELEASE_TARGETS';
  if n=1 then
    execute immediate 'select count(*) from e1_release_targets where owner_name is not null or phase not in (''new'',''ready'')' into n;
    if n<>0 then raise_application_error(-20702,'Active or interrupted release: inspect it before walkthrough cleanup'); end if;
  end if;
  dbms_output.put_line('PASS walkthrough idle: no active authoring or deployment owner.');
end;
/
