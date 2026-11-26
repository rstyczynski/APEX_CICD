declare n number; begin
select count(*) into n from e12_app.history where id between 1000 and 1079 or id between 2000 and 2079;
if n<>160 then raise_application_error(-20122,'lost traffic'); end if;
select count(*) into n from e12_app.history h full outer join e12_app.details d on h.id=d.id where h.id is null or d.id is null or h.message<>case when d.template='literal' then d.person else 'Hello '||d.person end;
if n<>0 then raise_application_error(-20123,'visibility mismatch'); end if;
if e12_app.bridge.read_message(1000)<>'Hello Hello' or e12_app.bridge.read_message(2000)<>'Hello World' then raise_application_error(-20124,'shared visibility'); end if;
begin e12_app.bridge.retire; raise_application_error(-20125,'early retirement accepted'); exception when others then if sqlcode<>-20104 then raise; end if; end;
dbms_output.put_line('MIXED_READ_WRITE_AND_RETIREMENT_GUARD_PASS'); end;
/
update e12_app.callers set api=1 where component='Hello';
commit;
begin e12_app.hello(3000); e12_app.world(3001); commit; end;
/
declare n number; begin
if e12_app.bridge.read_message(1000)<>'Hello Hello' then raise_application_error(-20126,'new write lost on return'); end if;
select count(*) into n from e12_app.settings where k='language' and v='en'; if n<>1 then raise_application_error(-20127,'settings lost'); end if;
if e12_app.bridge.read_message(0)<>'retained greeting' then raise_application_error(-20128,'history lost'); end if;
dbms_output.put_line('RETURN_AFTER_NEW_WRITES_PRESERVATION_PASS'); end;
/
update e12_app.callers set api=2;
commit;
begin e12_app.bridge.retire; commit; end;
/
begin
begin e12_app.bridge.legacy_write(4000,'retired'); raise_application_error(-20129,'legacy accepted'); exception when others then if sqlcode<>-20102 then raise; end if; end;
e12_app.hello(4001); e12_app.world(4002); commit;
begin e12_app.bridge.template_write(4003,'unknown',sys.odcivarchar2list('x')); raise_application_error(-20130,'bad template accepted'); exception when others then if sqlcode<>-20103 then raise; end if; end;
dbms_output.put_line('RETIREMENT_AND_NEW_CONTRACT_PASS'); end;
/
