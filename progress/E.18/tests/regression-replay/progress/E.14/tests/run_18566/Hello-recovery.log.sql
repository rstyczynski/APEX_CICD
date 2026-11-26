declare n number; begin select api into n from e12_app.callers where component='Hello'; if n<>1 then raise_application_error(-20204,'route leaked'); end if; select count(*) into n from e12_app.migrations where component='Hello'; if n<>0 then raise_application_error(-20205,'journal leaked'); end if; dbms_output.put_line('RECOVERY_PASS'); end;
/
begin dbms_session.sleep(1); end;
/