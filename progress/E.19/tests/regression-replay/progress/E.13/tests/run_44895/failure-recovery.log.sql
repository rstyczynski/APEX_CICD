begin
begin e12_app.bridge.template_write(99,'greeting',sys.odcivarchar2list('Failure'),true); raise_application_error(-20120,'failure not injected');
exception when others then if sqlcode<>-20101 then raise; end if; end;
commit;
end;
/
declare n number; begin select count(*) into n from e12_app.history where id=99; if n<>0 then raise_application_error(-20121,'partial history'); end if;
select count(*) into n from e12_app.details where id=99; if n<>0 then raise_application_error(-20121,'partial details'); end if;
dbms_output.put_line('CAUGHT_FAILURE_COMMIT_ATOMIC'); end;
/
update e12_app.callers set api=2 where component='Hello';
commit;
