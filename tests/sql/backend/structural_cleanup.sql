-- Isolated test schema only. A preexisting E5_TEST_DDL must fail creation;
-- never adopt or drop an object after a failed CREATE.
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
create table e5_test_ddl (id number primary key);
rollback;
declare l_count number;
begin
  select count(*) into l_count from user_tables where table_name='E5_TEST_DDL';
  if l_count <> 1 then raise_application_error(-20325,'DDL unexpectedly rolled back'); end if;
end;
/
drop table e5_test_ddl purge;
declare l_count number;
begin
  select count(*) into l_count from user_tables where table_name='E5_TEST_DDL';
  if l_count <> 0 then raise_application_error(-20326,'DDL cleanup failed'); end if;
end;
/
