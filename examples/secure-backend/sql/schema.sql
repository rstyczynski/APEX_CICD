create table country_permissions (
 user_name varchar2(255) not null,
 country_code varchar2(2) not null check (country_code in ('PL','DE')),
 enabled char(1) default 'Y' not null check (enabled in ('Y','N')),
 primary key (user_name,country_code)
);
create table greeting_requests (
 country_code varchar2(2) not null,
 request_key varchar2(80) not null,
 greeting_text varchar2(200) not null,
 actor varchar2(255) not null,
 primary key (country_code,request_key)
);
create table greeting_audit (
 country_code varchar2(2) not null,
 request_key varchar2(80) not null,
 actor varchar2(255) not null,
 primary key (country_code,request_key),
 foreign key (country_code,request_key) references greeting_requests(country_code,request_key)
);
