set serveroutput on
begin
  E1_CTRL.e1_ownership.assert_owned('Foundation','foundation-initial',1);
end;
/
lb validate -changelog-file db/changelog.xml
lb update -changelog-file db/changelog.xml
declare n number; begin
  select count(*) into n from lab_components where component='Foundation' and installed=1 and version='1.0.0';
  if n<>1 then raise_application_error(-20201,'Foundation verification failed'); end if;
  select count(*) into n from lab_components where component in ('Hello','World') and installed=0 and version is null;
  if n<>2 then raise_application_error(-20202,'Foundation assembly presence metadata failed'); end if;
  select count(*) into n from lab_state where state_key='Application' and state='maintenance';
  if n<>1 then raise_application_error(-20203,'Incomplete application is not blocked'); end if;
  dbms_output.put_line('Foundation 1.0.0 verified; Hello/World not installed; application maintenance.');
end;
/
