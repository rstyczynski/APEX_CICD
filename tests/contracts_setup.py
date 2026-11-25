"""Create only new isolated E.6 accounts/workspace and native application."""
from contracts_lab import *
import hashlib
from contract_manifest import qualified_toolchain
# Qualification precedes any native source generation/import.
env=os.environ.copy();env['JAVA_HOME']=str(ROOT/'.local-apex/tools/jdk-21.0.12.1+1/Contents/Home')
version=subprocess.check_output([str(ROOT/'.local-apex/tools/sqlcl-25.4.1.022.0618/sqlcl/bin/sql'),'-version'],env=env,text=True)
metadata=ROOT/'examples/secure-backend/.dbtools/project.config.json'
qualified_toolchain(json.loads(metadata.read_text())['sqlcl']['version'] if metadata.exists() else '25.4.1.0',version)
(OUT/'sqlcl-qualified.log').write_text(version)
if '--resume-application' not in sys.argv:
 execute('''create user E6_APP no authentication default tablespace users quota 100m on users;
 grant create session,create table,create procedure,create trigger to E6_APP;
 create user E6_TEST no authentication default tablespace users quota 20m on users;
 grant create session,create procedure,create table to E6_TEST;
create table e6_test.caller_markers(id number primary key);
 alter session set current_schema=E6_APP;
 '''+(SQL/'schema.sql').read_text()+'\n'+(SQL/'greeting_contract.sql').read_text()+'\n'+(SQL/'secure_greetings.sql').read_text()+'''
 insert into country_permissions values('ALICE','PL','Y');
 insert into country_permissions values('BOB','DE','Y');
 commit;
 alter session set current_schema=SYS;
 begin
  apex_instance_admin.add_workspace(p_workspace=>'E6_APP',p_primary_schema=>'E6_APP');
  apex_instance_admin.add_schema(p_workspace=>'E6_APP',p_schema=>'E6_TEST');
 end;
 /
 grant execute on E6_APP.greeting_contract to E6_TEST;
 grant execute on E6_APP.secure_greetings to E6_TEST;
 ''','schema-install.log')
 # Official, already pinned utPLSQL source is an input, not a credential authority.
 vendor=ROOT/'.local-apex/e5/download/utPLSQL.zip'
 assert hashlib.sha256(vendor.read_bytes()).hexdigest()=='6e650fc497bce02ae611e185e66c72204f0b984a024a41733b5452e7fb6db47a'
 cmd=BASE[:-1]+['cd /tmp/e5-utplsql/source && sqlplus -s / as sysdba']
 r=subprocess.run(cmd,input=PREFIX+'@create_grants.sql E5_UT E6_TEST\n@create_synonyms.sql E5_UT E6_TEST\nexit\n',text=True,capture_output=True,timeout=60)
 (OUT/'framework-grants.log').write_text(r.stdout+r.stderr)
 assert r.returncode==0 and not re.search(r'(?m)^\s*(ORA-|SP2-)',r.stdout+r.stderr)
 with access('E6_TEST') as pw:execute((ROOT/'tests/sql/contracts/test_contract.sql').read_text(),'unit-install.log','E6_TEST',pw)
source=(ROOT/'examples/testable-backend/apex/f810503.sql').read_text()
source=re.sub(r'(?m)^-- sqlcl_snapshot .*$', '',source)
for m in list(re.finditer(r'prompt --application/pages/page_(\d{5})\n.*?(?=prompt --application/|\Z)',source,re.S))[::-1]:
 if int(m[1]) not in (0,1,9999):source=source[:m.start()]+source[m.end():]
# Replace just page 1, retaining the native shared theme/authentication and login page.
a=source.index('prompt --application/pages/page_00001\n');b=source.index('prompt --application/',a+10)
page="""prompt --application/pages/page_00001
begin
wwv_flow_imp_page.create_page(p_id=>1,p_name=>'Secure greetings',p_alias=>'HOME',p_step_title=>'Secure greetings',p_autocomplete_on_off=>'OFF',p_page_template_options=>'#DEFAULT#',p_protection_level=>'C');
wwv_flow_imp_page.create_page_plug(p_id=>wwv_flow_imp.id(900000001),p_plug_name=>'Country-scoped greeting request',p_plug_template=>2674017834225413037,p_plug_display_sequence=>10,p_plug_display_point=>'BODY',p_location=>null);
"""
for i,(name,prompt,default,size) in enumerate([('P1_COUNTRY','Country code (PL or DE)','PL',2),('P1_REQUEST_KEY','Request key',None,80),('P1_TEXT','Greeting text','World',100)]):
 page+="wwv_flow_imp_page.create_page_item(p_id=>wwv_flow_imp.id("+str(900000010+i)+"),p_name=>'"+name+"',p_item_sequence=>"+str((i+1)*10)+",p_item_plug_id=>wwv_flow_imp.id(900000001),p_prompt=>'"+prompt+"',p_display_as=>'NATIVE_TEXT_FIELD',p_cMaxlength=>"+str(size)+",p_field_template=>1609122147107268652,p_item_template_options=>'#DEFAULT#'"+(",p_item_default=>'"+default+"'" if default else '')+");\n"
page+="""wwv_flow_imp_page.create_page_button(p_id=>wwv_flow_imp.id(900000020),p_button_sequence=>10,p_button_plug_id=>wwv_flow_imp.id(900000001),p_button_name=>'SUBMIT_REQUEST',p_button_action=>'SUBMIT',p_button_template_id=>4072362960822175091,p_button_image_alt=>'Submit greeting');
wwv_flow_imp_page.create_page_process(p_id=>wwv_flow_imp.id(900000021),p_process_sequence=>10,p_process_point=>'AFTER_SUBMIT',p_process_type=>'NATIVE_PLSQL',p_process_name=>'Submit country greeting',p_process_sql_clob=>'begin secure_greetings.submit_request(:P1_REQUEST_KEY,:P1_COUNTRY,:P1_TEXT); end;',p_process_clob_language=>'PLSQL',p_process_when=>'SUBMIT_REQUEST',p_process_when_type=>'REQUEST_EQUALS_CONDITION',p_error_display_location=>'INLINE_IN_NOTIFICATION',p_process_success_message=>'Greeting request saved.');
end;
/
"""
source=source[:a]+page+source[b:]
source=re.sub(r'wwv_flow_imp_shared.create_list_item\(.*?\n\);',lambda m:'' if re.search(r'f\?p=&APP_ID\.:(10|20|100|110|200|210):',m[0]) else m[0],source,flags=re.S)
source=source.replace("p_restrict_to_user_list=>'VERIFIER'","p_restrict_to_user_list=>'ALICE,BOB'").replace('APEX Delivery Laboratory','E6 Secure Greeting Laboratory')
source=source.replace(",p_flow_version=>'1.0.0'",",p_vpd=>'begin if upper(apex_application.g_user) = ''INIT_FAIL'' then raise_application_error(-20450,''E6 initialization failed''); end if; end;'\n,p_flow_version=>'1.0.0'")
out=ROOT/'examples/secure-backend/apex/f810603.sql';out.parent.mkdir(exist_ok=True);out.write_text(source)
password=secrets.token_urlsafe(24)
body="begin apex_util.set_security_group_id(apex_util.find_security_group_id('E6_APP'));\nif apex_util.get_user_id('ALICE') is null then apex_util.create_user(p_user_name=>'ALICE',p_web_password=>'"+password+"',p_change_password_on_first_use=>'N'); else apex_util.edit_user(p_user_id=>apex_util.get_user_id('ALICE'),p_user_name=>'ALICE',p_web_password=>'"+password+"',p_new_password=>'"+password+"',p_change_password_on_first_use=>'N'); end if;\nend;\n/\n"
body+='''begin
 apex_application_install.set_workspace('E6_APP');
 apex_application_install.set_application_id(810603);
 apex_application_install.generate_offset;
 apex_application_install.set_schema('E6_APP');
 apex_application_install.set_application_alias('E6-CONTRACTS');
end;
/
'''+source
execute(body,'application-install.log',redactions=(password,))
private=Path('/tmp/e6-demo-login.json');private.write_text(json.dumps({'username':'ALICE','password':password}));private.chmod(0o600)
print('Installed isolated E6_APP / 810603 and E6_TEST; no public grants or stored database passwords.')
