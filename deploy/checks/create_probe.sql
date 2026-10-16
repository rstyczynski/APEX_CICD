set serveroutput on
declare n number;
begin
  select count(*) into n from user_tables where table_name='E1_PRIVATE_PROBE';
  if n=0 then
    execute immediate 'create table e1_private_probe (id number primary key)';
    dbms_output.put_line('Created E1_PRIVATE_PROBE in current schema.');
  else
    dbms_output.put_line('Kept existing E1_PRIVATE_PROBE in current schema.');
  end if;
end;
/
