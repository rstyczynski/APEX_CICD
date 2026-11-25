create or replace editionable trigger hello_config_guard before
    insert or update on hello_config
    for each row
declare
    n number;
begin
    lab_runtime.assert_ready;
    select
        count(*)
    into n
    from
        hello_entries
    where
            entry_id = :new.default_entry_id
        and active = 'Y';

    if n <> 1 then
        raise_application_error(-20312, 'Hello default must be an active Hello entry');
    end if;
end;
/

alter trigger hello_config_guard enable;


-- sqlcl_snapshot {"hash":"e81c39016d9af392a7c529d7a43aaa94dc847b78","type":"TRIGGER","name":"HELLO_CONFIG_GUARD","schemaName":"E1_DEV_C","sxml":""}