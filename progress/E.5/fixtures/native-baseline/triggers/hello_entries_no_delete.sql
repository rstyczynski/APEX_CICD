create or replace editionable trigger hello_entries_no_delete before
    delete on hello_entries
begin
    raise_application_error(-20311, 'Deactivate Hello entries instead of deleting');
end;
/

alter trigger hello_entries_no_delete enable;


-- sqlcl_snapshot {"hash":"1b13cbe7b26186df3bd80826c42ffd18bb9f0098","type":"TRIGGER","name":"HELLO_ENTRIES_NO_DELETE","schemaName":"E1_DEV_C","sxml":""}