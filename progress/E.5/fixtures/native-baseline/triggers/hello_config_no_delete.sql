create or replace editionable trigger hello_config_no_delete before
    delete on hello_config
begin
    raise_application_error(-20313, 'Hello configuration cannot be deleted');
end;
/

alter trigger hello_config_no_delete enable;


-- sqlcl_snapshot {"hash":"f0fcd091339157f957706955c05525d5a648839b","type":"TRIGGER","name":"HELLO_CONFIG_NO_DELETE","schemaName":"E1_DEV_C","sxml":""}