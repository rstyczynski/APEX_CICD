create or replace package secure_greetings authid definer as
 procedure submit_request(p_key varchar2,p_country varchar2,p_text varchar2);
end;
/
create or replace package body secure_greetings as
 procedure submit_request(p_key varchar2,p_country varchar2,p_text varchar2) is
  l_actor varchar2(255):=upper(apex_application.g_user);
  l_country varchar2(2);
  l_message varchar2(200);
  l_count number;
 begin
  savepoint greeting_operation;
  if apex_application.g_flow_id<>810603 or apex_application.g_flow_id is null
     or apex_application.g_instance is null or apex_application.g_instance=0
     or l_actor is null or l_actor in ('NOBODY','ANONYMOUS','APEX_PUBLIC_USER') then
   raise_application_error(-20400,'An authenticated application context is required.');
  end if;
  l_country:=apex_util.get_session_state('P1_COUNTRY');
  if l_country is null or p_country is null or p_country<>l_country then
   raise_application_error(-20401,'Country context mismatch.');
  end if;
  select count(*) into l_count from country_permissions
   where user_name=l_actor and country_code=p_country and enabled='Y';
  if l_count<>1 then raise_application_error(-20402,'Country access denied.'); end if;
  if trim(p_key) is null or length(p_key)>80 then
   raise_application_error(-20404,'A request key of 1 to 80 characters is required.');
  end if;
  l_message:=greeting_contract.render(p_text);
  insert into greeting_requests values(p_country,p_key,l_message,l_actor);
  insert into greeting_audit values(p_country,p_key,l_actor);
 exception
  when dup_val_on_index then
   rollback to greeting_operation;
   raise_application_error(-20403,'Duplicate request rejected.');
  when others then
   rollback to greeting_operation;
   raise;
 end;
end;
/
