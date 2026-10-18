whenever oserror exit failure
whenever sqlerror exit failure
alter session set container=FREEPDB1;
set serveroutput on
declare n number;
begin
 select count(*) into n from dba_users where username in ('E1_CTRL','E1_DEV_A','E1_DEV_B','E1_DEV_C','E1_QUALIFY','E1_TEST');
 if n<>0 then raise_application_error(-20811,'Infrastructure must not create project schemas'); end if;
 select count(*) into n from apex_workspaces where workspace in ('E1_DEV_A','E1_DEV_B','E1_DEV_C','E1_QUALIFY','E1_TEST');
 if n<>0 then raise_application_error(-20812,'Infrastructure must not create project workspaces'); end if;
 dbms_output.put_line('PASS infrastructure only: zero project schemas and workspaces. Project onboarding is separate.');
end;
/
exit success
