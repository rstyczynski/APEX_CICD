create or replace editionable trigger world_config_no_delete before
    delete on world_config
begin
    raise_application_error(-20323, 'World configuration cannot be deleted');
end;
/

alter trigger world_config_no_delete enable;


-- sqlcl_snapshot {"hash":"29ff6d340e0dd32c9dd1427f58b1681968132740","type":"TRIGGER","name":"WORLD_CONFIG_NO_DELETE","schemaName":"E1_DEV_C","sxml":""}