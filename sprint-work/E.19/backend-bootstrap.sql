-- Run as SYS in FREEPDB1 only. Existing users are rejected, never replaced.
create user e5_test no authentication default tablespace users quota 20m on users;
grant create session, create table, create procedure to e5_test;
create table e5_test.hello_entries (
  entry_id number generated always as identity primary key,
  entry_text varchar2(100 char) not null,
  active char(1) default 'Y' not null check (active in ('Y','N')),
  constraint e5_hello_text_valid check (length(trim(entry_text)) between 1 and 100)
);
insert into e5_test.hello_entries(entry_text,active) values ('E5 unrelated sentinel','Y');
commit;
