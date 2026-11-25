-- CREATE fragment. The full native application in ../apex/f810503.sql
-- owns the installed, browser-verified validation/process mapping.
-- Condition: request CREATE. Retain native DML for SAVE/DELETE only.
-- Add a function-body-returning-error-text validation on P101_ENTRY_TEXT:
-- return hello_entry_api.validation_error(:P101_ENTRY_TEXT);
begin
  hello_entry_api.create_entry(
    p_text => :P101_ENTRY_TEXT,
    p_active => :P101_ACTIVE,
    p_id => :P101_ENTRY_ID);
end;
/
