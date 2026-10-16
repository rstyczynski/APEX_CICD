set serveroutput on
begin
  begin
    execute immediate 'insert into {{other_schema}}.e1_private_probe values (1)';
    rollback;
    raise_application_error(-20021,'Cross-area write was permitted');
  exception when others then
    if sqlcode not in (-942,-1031) then raise; end if;
    dbms_output.put_line('EXPECTED_DENIAL|'||sqlcode||'|'||substr(sqlerrm,12));
  end;
end;
/
