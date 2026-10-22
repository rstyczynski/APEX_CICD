-- Append once below PROJECT's generated custom changeset header.
-- Declare the installed Hello version after its schema correction is applied.
-- Existing business rows and configuration are deliberately not updated.
declare
  l_count number;
begin
  if user not in ('E1_INTEGRATION','E1_UAT') then
    raise_application_error(-20884,'Hello release data requires an owned delivery target');
  end if;
  select count(*) into l_count from lab_components where installed=1 and
    ((component in ('Foundation','World') and version='1.0.0') or
     (component='Hello' and version='1.0.0'));
  if l_count<>3 then raise_application_error(-20885,'Expected complete 1.0.0 baseline'); end if;
  select count(*) into l_count from user_constraints
    where table_name='HELLO_ENTRIES' and constraint_name='HELLO_TEXT_NONBLANK'
      and status='ENABLED' and validated='VALIDATED';
  if l_count<>1 then raise_application_error(-20886,'Hello schema correction is missing'); end if;
  select count(*) into l_count from user_objects
    where object_name='HELLO_ENTRIES_GUARD' and object_type='TRIGGER' and status='VALID';
  if l_count<>1 then raise_application_error(-20887,'Hello guard is invalid'); end if;
  update lab_components set version='1.0.1' where component='Hello';
end;
/
