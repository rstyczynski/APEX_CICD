create table lab_components (
  component varchar2(20) primary key,
  installed number(1) not null check (installed in (0,1)),
  version varchar2(30),
  constraint lab_component_presence check ((installed=0 and version is null) or (installed=1 and version is not null))
);
insert into lab_components values ('Foundation',1,'1.0.0');
insert into lab_components values ('Hello',0,null);
insert into lab_components values ('World',0,null);
create table greeting_history (
  greeting_id number generated always as identity primary key,
  hello_entry_id number not null,
  world_entry_id number not null,
  hello_text varchar2(100 char) not null,
  world_text varchar2(100 char) not null,
  hello_prefix varchar2(30 char),
  world_prefix varchar2(30 char),
  greeting_text varchar2(261 char) not null,
  created_at timestamp with time zone default systimestamp not null,
  actor varchar2(255 char) not null
);
create table lab_state (
  state_key varchar2(30) primary key,
  parent_key varchar2(30),
  state varchar2(20) check (state in ('ready','maintenance','failed')),
  reason varchar2(1000)
);
insert into lab_state values ('Application',null,'maintenance','Initial assembly incomplete');
insert into lab_state values ('Foundation','Application','ready','Foundation installed');
insert into lab_state values ('Hello','Application','maintenance','Not installed');
insert into lab_state values ('World','Application','maintenance','Not installed');
