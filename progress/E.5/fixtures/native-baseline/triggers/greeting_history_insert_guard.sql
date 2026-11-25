create or replace editionable trigger greeting_history_insert_guard before
    insert on greeting_history
begin
    lab_runtime.assert_ready;
end;
/

alter trigger greeting_history_insert_guard enable;


-- sqlcl_snapshot {"hash":"1a947b32033ff56f13421fd9b8a6b4f3779584df","type":"TRIGGER","name":"GREETING_HISTORY_INSERT_GUARD","schemaName":"E1_DEV_C","sxml":""}