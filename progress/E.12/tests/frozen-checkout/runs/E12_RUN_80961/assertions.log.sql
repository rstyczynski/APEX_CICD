declare n number; s varchar2(100); begin
select count(*) into n from e12_app.history h join e12_app.next_history t on t.id=h.id where h.id=0 and h.message='retained historical greeting' and t.message=h.message and h.language is null and t.language is null;
if n<>1 then raise_application_error(-20015,'original historical row changed'); end if;
select count(*) into n from e12_app.component_version where version='1.1.0';
if n<>1 then raise_application_error(-20016,'wrong component version'); end if;
dbms_output.put_line('RETAINED_HISTORY_PASS');
select count(*) into n from e12_app.history where id between 1001 and 1120 or id between 2001 and 2120;
if n<>240 then raise_application_error(-20004,'traffic lost'); end if;
select count(*) into n from e12_app.next_history where id=1 and message='newer accepted';
if n<>1 then raise_application_error(-20011,'target newer value lost'); end if;
select count(*) into n from e12_app.next_history where id=2;
if n<>0 then raise_application_error(-20012,'deleted ID resurrected'); end if;
select count(*) into n from e12_app.next_history where id=3 and message='concurrent insert' and language='pl';
if n<>1 then raise_application_error(-20013,'insert lost'); end if;
select message into s from e12_app.history where id=1; if s<>'newer accepted' then raise_application_error(-20005,'overwritten'); end if;
select count(distinct op) into n from e12_app.change_log where actor='E12_CONCURRENT'; if n<>3 then raise_application_error(-20006,'missing attribution'); end if;
select count(*) into n from e12_app.settings where k='language' and v='en'; if n<>1 then raise_application_error(-20007,'settings lost'); end if;
if e12_app.greet_language('Jan','pl')<>'Witaj Jan' or e12_app.greet_language('Jan')<>'Hello Jan' then raise_application_error(-20008,'language'); end if;
e12_app.hello(3001); e12_app.world(3002);
select count(*) into n from dba_objects where owner='E12_APP' and status<>'VALID'; if n<>0 then raise_application_error(-20009,'invalid objects'); end if;
dbms_output.put_line('ASSERTIONS_PASS'); end;
/
