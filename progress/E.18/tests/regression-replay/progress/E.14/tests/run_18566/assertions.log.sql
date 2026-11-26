declare n number; begin
select count(*) into n from e12_app.callers where api=2 and maintenance=0; if n<>2 then raise_application_error(-20206,'routes incomplete'); end if;
select count(*) into n from e12_app.history; if n<>163 then raise_application_error(-20207,'history lost'); end if;
select count(*) into n from e12_app.history h full outer join e12_app.details d on h.id=d.id where h.id is null or d.id is null or h.message<>case when d.template='literal' then d.person else 'Hello '||d.person end; if n<>0 then raise_application_error(-20208,'representation mismatch'); end if;
select count(*) into n from e12_app.settings where k='language' and v='en'; if n<>1 then raise_application_error(-20209,'configuration lost'); end if;
if e12_app.bridge.read_message(0)<>'retained greeting' then raise_application_error(-20210,'baseline lost'); end if;
dbms_output.put_line('COMPONENT_WINDOWS_PRESERVATION_PASS'); end;
/
