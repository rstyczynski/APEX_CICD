create or replace trigger e6_app.e6_test_audit_failure
before insert on e6_app.greeting_audit for each row
begin
 if :new.request_key='FAIL-AUDIT' then
  raise_application_error(-20499,'Selected second-write failure');
 end if;
end;
/
