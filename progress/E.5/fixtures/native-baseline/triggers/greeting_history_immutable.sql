create or replace editionable trigger greeting_history_immutable before
    update or delete on greeting_history
begin
    raise_application_error(-20305, 'Greeting history is immutable');
end;
/

alter trigger greeting_history_immutable enable;


-- sqlcl_snapshot {"hash":"bf6ba43dd5e754dcc4acb5d7f0d0e8fea449aa68","type":"TRIGGER","name":"GREETING_HISTORY_IMMUTABLE","schemaName":"E1_DEV_C","sxml":""}