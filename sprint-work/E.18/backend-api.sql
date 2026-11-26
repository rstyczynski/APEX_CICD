create or replace package hello_entry_api authid definer as
  function validation_error(p_text varchar2) return varchar2;
  procedure create_entry(p_text varchar2, p_active varchar2 default 'Y', p_id out number);
end hello_entry_api;
/
create or replace package body hello_entry_api as
  function validation_error(p_text varchar2) return varchar2 is
  begin
    if trim(p_text) is null then
      return 'Entry Text must have some value.';
    elsif length(trim(p_text)) > 100 then
      return 'Entry Text must not exceed 100 characters.';
    end if;
    return null;
  end;
  procedure create_entry(p_text varchar2, p_active varchar2 default 'Y', p_id out number) is
    l_error varchar2(200);
  begin
    l_error := validation_error(p_text);
    if l_error is not null then
      raise_application_error(-20320, l_error);
    end if;
    if p_active is null or p_active not in ('Y', 'N') then
      raise_application_error(-20321, 'Active must be Y or N.');
    end if;
    insert into hello_entries(entry_text, active)
      values (trim(p_text), p_active) returning entry_id into p_id;
  end;
end hello_entry_api;
/
