set serveroutput on
declare n number;
begin
  select count(*) into n from user_errors where name in
    ('LAB_RUNTIME','GREETING_HISTORY_IMMUTABLE','GREETING_HISTORY_INSERT_GUARD');
  if n<>0 then raise_application_error(-20400,'Foundation runtime has compile errors'); end if;
  begin
    lab_runtime.assert_ready;
    raise_application_error(-20401,'Incomplete assembly accepted work');
  exception when others then
    if sqlcode<>-20300 then raise; end if;
  end;
  select count(*) into n from greeting_history;
  if n<>0 then raise_application_error(-20402,'Unexpected history in Foundation-only target'); end if;
  dbms_output.put_line('PASS Foundation contract: compiled; incomplete runtime blocked; history empty.');
end;
/
