set serveroutput on
declare n number;
begin
  begin
    execute immediate 'select count(*) from {{other_schema}}.e1_private_probe' into n;
    raise_application_error(-20020,'Cross-area read was permitted');
  exception when others then
    if sqlcode not in (-942,-1031) then raise; end if;
    dbms_output.put_line('EXPECTED_DENIAL|'||sqlcode||'|'||substr(sqlerrm,12));
  end;
end;
/
