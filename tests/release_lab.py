"""Prepared-host isolated upgrade experiment; never writes prior sprint evidence."""
from pathlib import Path
import sys,subprocess,re,os,json,hashlib
sys.path.insert(0,'scripts')
from release_validation import build,verify,digest
from contract_manifest import qualified_toolchain
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'progress/E.7/tests';OUT.mkdir(exist_ok=True)
BASE=['podman','--connection','apex-cicd','exec','-i','--user','oracle','apex-db','bash','-lc','sqlplus -s / as sysdba']
def sql(body,name,expected=None):
 prefix='whenever sqlerror exit failure rollback\nwhenever oserror exit failure rollback\nset define off\nset sqlblanklines on\nset pagesize 0\nset feedback off\nset serveroutput on\nalter session set container=FREEPDB1;\n'
 r=subprocess.run(BASE,input=prefix+body+'\nprompt E7_COMPLETE\nexit\n',capture_output=True,text=True,timeout=90);out=r.stdout+r.stderr;(OUT/name).write_text(out)
 bad=r.returncode or re.search(r'(?m)^\s*(ORA-|PLS-|SP2-|Warning:)',out) or 'E7_COMPLETE' not in out
 if expected:
  assert bad and 'STATE:'+expected in out,out
 elif bad:raise RuntimeError(out[-2000:])
 return out

def run():
 env=os.environ.copy();env['JAVA_HOME']=str(ROOT/'.local-apex/tools/jdk-21.0.12.1+1/Contents/Home')
 tool=subprocess.check_output([str(ROOT/'.local-apex/tools/sqlcl-25.4.1.022.0618/sqlcl/bin/sql'),'-version'],env=env,text=True)
 qualified_toolchain('25.4.1.0',tool);(OUT/'sqlcl-qualified.log').write_text(tool)
 # Refuse unrelated pre-existing owners. Rehearsal is resumable only with our exact marker.
 existing=sql("select 'OWNER:'||count(*) from dba_users where username='E7_APP';",'preflight.log')
 if 'OWNER:0' in existing:
  sql("create user E7_APP no authentication default tablespace users quota 50m on users;\ngrant create session,create table,create procedure to E7_APP;\ncreate user E7_CONSUMER no authentication;\nbegin apex_instance_admin.add_workspace(p_workspace=>'E7_APP',p_primary_schema=>'E7_APP'); end;\n/",'setup.log')
  sql((ROOT/'examples/release-validation/sql/baseline.sql').read_text()+"\ninsert into e7_app.greetings values(7,'E7 retained synthetic greeting');\ncommit;",'baseline.log')
 else:
  sql("merge into e7_app.greetings d using(select 7 id, 'E7 retained synthetic greeting' message from dual) s on(d.id=s.id) when not matched then insert(id,message) values(s.id,s.message);\ncommit;",'resume-seed.log')
  out=sql("select 'MARKER:'||message from e7_app.greetings where id=7;",'owner-marker.log');assert 'MARKER:E7 retained synthetic greeting' in out
 source=(ROOT/'examples/secure-backend/apex/f810603.sql').read_text()
 source=source.replace('E6 Secure Greeting Laboratory','E7 Release Laboratory').replace("p_alias=>", "p_alias=>",1)
 source=source.replace("p_flow_version=>'1.0.0'","p_flow_version=>'@RELEASE@'")
 a=source.index('prompt --application/pages/page_00001\n');b=source.index('prompt --application/',a+10)
 page="""prompt --application/pages/page_00001
begin
wwv_flow_imp_page.create_page(p_id=>1,p_name=>'Release identity',p_alias=>'HOME',p_step_title=>'Release identity',p_autocomplete_on_off=>'OFF',p_page_template_options=>'#DEFAULT#',p_protection_level=>'C',p_page_is_public_y_n=>'Y');
wwv_flow_imp_page.create_page_plug(p_id=>wwv_flow_imp.id(970000001),p_plug_name=>'Installed release',p_plug_template=>2674017834225413037,p_plug_display_sequence=>10,p_plug_display_point=>'BODY',p_plug_source=>'Application release @RELEASE@ | Greeting contract 1.1.0',p_plug_source_type=>'NATIVE_STATIC');
end;
/
"""
 source=source[:a]+page+source[b:]
 source=source.replace("p_restrict_to_user_list=>'ALICE,BOB'","p_restrict_to_user_list=>null")
 source=source.replace("p_authentication=>'PLUGIN'","p_authentication=>'PUBLIC'")
 # Public release information; other pages remain unused fixture material.
 prefix="begin apex_application_install.set_workspace('E7_APP'); apex_application_install.set_application_id(810703); apex_application_install.generate_offset; apex_application_install.set_schema('E7_APP'); apex_application_install.set_application_alias('E7-RELEASE'); end;\n/\n"
 commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
 contracts=(ROOT/'examples/secure-backend/contracts.json').read_bytes()
 receipts=[]
 for index,release in enumerate(['1.0.0','1.1.0','1.1.0']):
  app=source.replace('@RELEASE@',release)
  migration=(ROOT/'examples/release-validation/sql'/('baseline.sql' if index==0 else 'upgrade.sql')).read_bytes()
  files={'migration.sql':migration,'application.sql':(prefix+app).encode(),'contracts.json':contracts,'configuration.json':json.dumps({'schema':'E7_APP','app_id':810703,'sqlcl':'25.4.1.0','build':'25.4.1.022.0618'}).encode(),'evidence.txt':(ROOT/'progress/E.7/tests/unit-integrity.log').read_bytes()}
  files['source/release_lab.py']=Path(__file__).read_bytes()
  files['source/release_validation.py']=(ROOT/'scripts/release_validation.py').read_bytes()
  archive,pin=build(files,commit,release,json.loads(contracts));name='release-'+release+'-'+pin[:16]+'.zip'
  if index<2:
   target=OUT/name
   if target.exists():assert target.read_bytes()==archive,'Released contents changed under same identity'
   else:target.write_bytes(archive)
   (OUT/(name+'.sha256')).write_text(pin+'\n')
  else:
   name=receipts[-1]['archive'];archive=(OUT/name).read_bytes();pin=(OUT/(name+'.sha256')).read_text().strip()
  manifest=verify(archive,pin)
  import zipfile,io
  with zipfile.ZipFile(io.BytesIO(archive)) as verified:
   migration=verified.read('migration.sql');application=verified.read('application.sql').decode()
  if index:sql(migration.decode(),'upgrade-'+str(index)+'.log')
  sql(application,'apex-'+str(index)+'.log')
  observed=sql("select 'VERSION:'||version from apex_applications where application_id=810703;\nselect 'PRESERVED:'||message from e7_app.greetings where id=7;",'observed-'+str(index)+'.log')
  assert 'VERSION:'+release in observed and 'PRESERVED:E7 retained synthetic greeting' in observed,observed
  import urllib.request
  html=urllib.request.urlopen('http://127.0.0.1:8080/ords/f?p=810703:1',timeout=30).read().decode()
  (OUT/('rendered-'+str(index)+'.html')).write_text(html)
  assert 'Application release '+release+' | Greeting contract 1.1.0' in html,'Rendered release mismatch'
  if index:sql((ROOT/'examples/release-validation/sql/assert_state.sql').read_text(),'state-'+str(index)+'.log')
  receipts.append({'release':release,'archive':name,'source_base_commit':commit,'manifest_sha256':pin,'archive_sha256':digest(archive),'preserved':True,'metadata':release,'repeat':index==2})
 checks=(ROOT/'examples/release-validation/sql/assert_state.sql').read_text()
 faults=[('COLUMN',"alter table e7_app.greetings modify language_code varchar2(3);","alter table e7_app.greetings modify language_code varchar2(2);"),('CONSTRAINT','alter table e7_app.greetings disable constraint e7_language_ck;','alter table e7_app.greetings enable validate constraint e7_language_ck;'),('GRANT','revoke execute on e7_app.greeting_api from e7_consumer;','grant execute on e7_app.greeting_api to e7_consumer;'),('INVALID_OBJECT','create or replace procedure e7_app.invalid_probe as begin nonexistent_call; end;\n/','drop procedure e7_app.invalid_probe;'),('REFERENCE',"update e7_app.release_reference set value='wrong' where code='LANGUAGE';\ncommit;","update e7_app.release_reference set value='en' where code='LANGUAGE';\ncommit;")]
 for label,inject,restore in faults:
  try:
   # Invalid compilation deliberately emits a warning; retain it and require our state error next.
   if label=='INVALID_OBJECT':
    try:sql(inject,'inject-'+label+'.log')
    except RuntimeError as e:
     assert 'created with compilation errors' in str(e),str(e)
   else:sql(inject,'inject-'+label+'.log')
   sql(checks,'detected-'+label+'.log',label)
  finally:sql(restore,'restore-'+label+'.log')
 sql(checks,'final-state.log')
 (OUT/'deployment-receipts.json').write_text(json.dumps({'deployments':receipts,'detected_states':[f[0] for f in faults],'sqlcl':tool.strip()},indent=2)+'\n')
 print('PASS upgrade, preservation, contracts, five wrong states, repeat and APEX metadata')
if __name__=='__main__':run()
