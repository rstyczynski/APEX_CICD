create or replace editionable trigger world_entries_no_delete before
    delete on world_entries
begin
    raise_application_error(-20321, 'Deactivate World entries instead of deleting');
end;
/

alter trigger world_entries_no_delete enable;


-- sqlcl_snapshot {"hash":"2ac1d3a81ab1260f7ee60282b59ab0ba034beacc","type":"TRIGGER","name":"WORLD_ENTRIES_NO_DELETE","schemaName":"E1_DEV_C","sxml":""}