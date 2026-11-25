create or replace editionable trigger world_entries_guard before
    insert or update on world_entries
    for each row
declare
    n number;
begin
    lab_runtime.assert_ready;
    :new.entry_text := trim(:new.entry_text);
    if :new.active = 'N' then
        select
            count(*)
        into n
        from
            world_config
        where
            default_entry_id = :new.entry_id;

        if n > 0 then
            raise_application_error(-20320, 'Choose another active World default before deactivation');
        end if;
    end if;

end;
/

alter trigger world_entries_guard enable;


-- sqlcl_snapshot {"hash":"4caf7023604fa5198b4c688ee9842baf64caff7f","type":"TRIGGER","name":"WORLD_ENTRIES_GUARD","schemaName":"E1_DEV_C","sxml":""}