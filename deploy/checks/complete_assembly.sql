set serveroutput on
declare n number;
begin
  select count(*) into n from user_errors;
  if n<>0 then raise_application_error(-20420,'Compilation errors block assembly'); end if;
  select count(*) into n from lab_components where installed=1 and version='1.0.0' and component in ('Foundation','Hello','World');
  if n<>3 then raise_application_error(-20421,'Complete 1.0.0 triple required'); end if;
  select count(*) into n from lab_state where state_key in ('Foundation','Hello','World') and state='ready';
  if n<>3 then raise_application_error(-20422,'Components are not ready'); end if;
  select count(*) into n from apex_application_pages where application_id=810003 and page_id in (0,1,10,20,100,101,110,111,200,201,210,211,9999);
  if n<>13 then raise_application_error(-20423,'Required application pages are missing'); end if;
  dbms_output.put_line('PASS complete development assembly: compiled, three 1.0.0 components and thirteen required pages.');
end;
/
