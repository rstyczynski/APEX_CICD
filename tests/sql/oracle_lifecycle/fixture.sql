create table e2_components (
  component varchar2(30) primary key,
  version varchar2(30) not null
);
create table e2_settings (
  setting_key varchar2(30) primary key,
  setting_value varchar2(100) not null
);
create table e2_history (
  history_id number generated always as identity primary key,
  greeting_text varchar2(261) not null,
  recorded_at timestamp default systimestamp not null
);
create or replace package e2_greeting authid definer as
  function greeting return varchar2;
end;
/
create or replace package body e2_greeting as
  function greeting return varchar2 is
    h varchar2(100); w varchar2(100);
  begin
    select setting_value into h from e2_settings where setting_key='HELLO';
    select setting_value into w from e2_settings where setting_key='WORLD';
    return h||' '||w;
  end;
end;
/
