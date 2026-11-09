-- &1: connection; &2: schema; &3: workspace; &4: application.
-- Read-only acceptance checks; publication is a separate explicit operation.
set echo off verify off define on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name &1
declare n number;
begin
  if user <> '&2' then raise_application_error(-20931,'Unexpected target'); end if;
  apex_util.set_workspace(p_workspace=>'&3');
  lab_runtime.assert_ready;
  select count(*) into n from apex_application_pages
   where application_id=&4 and page_id=1
     and header_text='<p>E4 A: Select Hello and World values, then record the greeting.</p>';
  if n <> 1 then raise_application_error(-20932,'Selected A header missing'); end if;
  select count(*) into n from apex_application_page_regions
   where application_id=&4 and page_id=200 and region_name='World entries - selected C';
  if n <> 1 then raise_application_error(-20933,'Selected C region missing'); end if;
  select count(*) into n from apex_application_page_regions
   where application_id=&4 and page_id=100 and region_name='Hello entries';
  if n <> 1 then raise_application_error(-20934,'Baseline Hello region missing'); end if;
  select count(*) into n from apex_application_page_regions
   where application_id=&4 and region_name='Hello entries - deferred B';
  if n <> 0 then raise_application_error(-20935,'Deferred B is present'); end if;
  apex_session.create_session(p_app_id=>&4,p_page_id=>1,p_username=>'VERIFIER');
  apex_session.delete_session;
end;
/
prompt PASS selected A/C, excluded B, native readiness and verifier session
exit success
