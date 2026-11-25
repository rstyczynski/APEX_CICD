create or replace package greeting_contract authid definer as
 function render(p_text varchar2, p_suffix varchar2 default null) return varchar2;
 -- Deprecated in 1.1; callable for all 1.x consumers, removal requires 2.0.
 function hello(p_name varchar2) return varchar2;
 function render_v2(p_text varchar2) return varchar2;
end;
/
create or replace package body greeting_contract as
 function render(p_text varchar2, p_suffix varchar2 default null) return varchar2 is
 begin
  if trim(p_text) is null or length(trim(p_text))>100 then
   raise_application_error(-20410,'Greeting text must contain 1 to 100 characters.');
  end if;
  return 'Hello '||trim(p_text)||p_suffix;
 end;
 function hello(p_name varchar2) return varchar2 is
 begin
  return render(p_text=>p_name);
 end;
 function render_v2(p_text varchar2) return varchar2 is
 begin
  return json_object('message' value render(p_text) returning varchar2);
 end;
end;
/
