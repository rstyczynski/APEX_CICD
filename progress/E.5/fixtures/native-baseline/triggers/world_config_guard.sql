create or replace editionable trigger world_config_guard before
    insert or update on world_config
    for each row
declare
    n number;
begin
    lab_runtime.assert_ready;
    select
        count(*)
    into n
    from
        world_entries
    where
            entry_id = :new.default_entry_id
        and active = 'Y';

    if n <> 1 then
        raise_application_error(-20322, 'World default must be an active World entry');
    end if;
end;
/

alter trigger world_config_guard enable;


-- sqlcl_snapshot {"hash":"9659a7dc6d2eff2051199f00d9ed0a88861825fe","type":"TRIGGER","name":"WORLD_CONFIG_GUARD","schemaName":"E1_DEV_C","sxml":""}