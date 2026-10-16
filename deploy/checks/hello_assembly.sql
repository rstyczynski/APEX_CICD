set serveroutput on
declare n number;
begin
  select count(*) into n from user_errors;
  if n<>0 then raise_application_error(-20410,'Schema has compilation errors'); end if;
  select count(*) into n from lab_components where installed=1 and version='1.0.0' and component in ('Foundation','Hello');
  if n<>2 then raise_application_error(-20411,'Foundation/Hello versions not verified'); end if;
  select count(*) into n from lab_components where component='World' and installed=0 and version is null;
  if n<>1 then raise_application_error(-20412,'World must remain absent'); end if;
  select count(*) into n from hello_entries;
  if n<>0 then raise_application_error(-20413,'Unexpected seeded Hello business entries'); end if;
  begin lab_runtime.assert_ready; raise_application_error(-20414,'Incomplete assembly admitted mutation');
  exception when others then if sqlcode<>-20300 then raise; end if; end;
  dbms_output.put_line('PASS Hello assembly: compiled; Foundation/Hello 1.0.0; World absent; runtime blocked.');
end;
/
