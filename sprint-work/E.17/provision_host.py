"""Fresh hosted platform provisioning. Private values never enter retained evidence."""
import hashlib,json,os,re,secrets,subprocess,sys,time,urllib.request,zipfile
from pathlib import Path
OUT=Path('result');OUT.mkdir(exist_ok=True)
TMP=Path(os.environ['RUNNER_TEMP']);PRIVATE=TMP/'e17-private'
APEX_SHA='a7ad0ba94f70b2d581f7dde97fe27cd07afc98c32ecc146d89fd70cce9b76456'
ORDS='container-registry.oracle.com/database/ords@sha256:1551b5c51faf47a1e961ddbacf7d75262e686108b165d96c42542f0bae79e6de'
passwords=[v for v in [os.environ.get('NATIVE_PASSWORD'),os.environ.get('APEX_ADMIN_PASSWORD')] if v]
def run(args,body=None,label=None):
 p=subprocess.run(args,input=body,text=True,capture_output=True,timeout=1800)
 output=p.stdout+p.stderr
 for secret in passwords:output=output.replace(secret,'[REDACTED]')
 if label:(OUT/(label+'.log')).write_text(output)
 if label=='apex-install' and re.search(r'(?m)^\s*(ORA-|SP2-|PLS-)',output):raise RuntimeError('APEX native installation reported errors: '+output[-3000:])
 if p.returncode:raise RuntimeError(f'{label or args[0]} failed ({p.returncode}): '+output[-3000:])
 return output

def sql(container,body,label):
 out=run(['docker','exec','-i',container,'sqlplus','-s','/ as sysdba'],"whenever sqlerror exit failure\nset echo off verify off define off\nalter session set container=FREEPDB1;\n"+body+'\nexit\n',label)
 assert not re.search(r'(?m)^\s*(ORA-|SP2-|PLS-)',out),out[-2000:]
 return out

def verify():
 url='http://127.0.0.1:8080/ords/f?p=810503:LOGIN'
 for i in range(90):
  try:
   response=urllib.request.urlopen(url,timeout=10);body=response.read().decode()
   if response.status==200 and ('password' in body.lower()) and 'APEX Delivery Laboratory' in body:
    (OUT/'application.html').write_text(body)
    (OUT/'application-access.json').write_text(json.dumps(dict(url=url,status=response.status,title='APEX Delivery Laboratory',login=True)))
    print('PASS actual ORDS APEX application login page');return
  except Exception:pass
  time.sleep(4)
 raise RuntimeError('Application login page not available through ORDS')

mode=sys.argv[1]
a=os.environ.get('ORACLE_CONTAINER');t=os.environ.get('TARGET_CONTAINER')
pw=os.environ.get('NATIVE_PASSWORD');admin=os.environ.get('APEX_ADMIN_PASSWORD')
if mode=='inputs':
 PRIVATE.mkdir(mode=0o700)
 pw='Aa1_'+secrets.token_hex(20);admin='Aa1_'+secrets.token_hex(20);passwords.extend([pw,admin])
 for value in passwords:print('::add-mask::'+value)
 with open(os.environ['GITHUB_ENV'],'a') as f:f.write('NATIVE_PASSWORD='+pw+'\nAPEX_ADMIN_PASSWORD='+admin+'\n')
 a=os.environ['ORACLE_CONTAINER'];t=os.environ['TARGET_CONTAINER']
 for container,label in [(a,'author'),(t,'target')]:
  sql(container,f'create user AUTHOR16 identified by "{pw}" quota unlimited on users;\ngrant connect,resource,create view to AUTHOR16;',label+'-schema')
 (OUT/'host.json').write_text(json.dumps(dict(run=os.environ['GITHUB_RUN_ID'],source=os.environ['GITHUB_SHA'],host=run(['hostname']).strip(),identity=run(['id']).strip(),fresh_inputs='new random per-run values; masked; no retained lab inputs',database_containers=[a,t]),indent=2))
if mode=='apex-download':
 archive=TMP/'apex.zip'
 run(['curl','--fail','--location','--retry','3','https://download.oracle.com/otn_software/apex/apex_24.2.zip','-o',str(archive)],label='download-apex')
 assert hashlib.sha256(archive.read_bytes()).hexdigest()==APEX_SHA,'APEX checksum mismatch'
 with zipfile.ZipFile(archive) as z:z.extractall(TMP/'apex-install')
 run(['docker','cp',str(TMP/'apex-install/apex'),t+':/tmp/apex'],label='copy-apex')
 run(['docker','exec','--user','root',t,'chown','-R','oracle:oinstall','/tmp/apex'])
if mode=='apex-install':
 run(['docker','exec','-i','--workdir','/tmp/apex',t,'sqlplus','-s','/ as sysdba'], 'whenever sqlerror exit failure\nalter session set container=FREEPDB1;\n@apexins.sql SYSAUX SYSAUX TEMP /i/\nexit\n','apex-install')
if mode=='apex-configure':
 sql(t,f"alter user APEX_PUBLIC_USER account unlock;\nbegin apex_instance_admin.add_workspace(p_workspace=>'E17',p_primary_schema=>'AUTHOR16'); apex_util.set_security_group_id(apex_util.find_security_group_id('E17')); apex_util.create_user(p_user_name=>'LAB_USER',p_email_address=>'e17@example.invalid',p_web_password=>'{admin}',p_change_password_on_first_use=>'N'); commit; end;\n/",'apex-configure')
if mode=='application-import':
 app=Path('application.sql').read_text()
 sql(t,"begin apex_application_install.set_workspace('E17'); apex_application_install.set_schema('AUTHOR16'); apex_application_install.set_application_id(810503); apex_application_install.generate_offset; end;\n/\n"+app,'application-import')
if mode=='ords-install':
 run(['docker','pull',ORDS],label='ords-pull')
 # ORDS administrator uses a newly supplied private password, never a retained profile.
 sql(t,f'create user E17_ADMIN identified by "{admin}";\ngrant dba to E17_ADMIN;','ords-admin-input')
 run(['docker','run','--user',str(os.getuid())+':'+str(os.getgid()),'--env','HOME=/tmp','--rm','--network','host','-i','-v',str(PRIVATE)+':/etc/ords/config',ORDS,'install','--admin-user','E17_ADMIN','--proxy-user','--db-hostname','127.0.0.1','--db-port','1522','--db-servicename','FREEPDB1','--gateway-mode','proxied','--gateway-user','APEX_PUBLIC_USER','--password-stdin'],admin+'\n'+pw+'\n','ords-install')
if mode=='ords-start':
 run(['docker','run','--user',str(os.getuid())+':'+str(os.getgid()),'--env','HOME=/tmp','-d','--name','e17-ords','--network','host','-v',str(PRIVATE)+':/etc/ords/config','-v',str(TMP/'apex-install/apex/images')+':/opt/oracle/apex/images:ro',ORDS,'serve','--port','8080','--apex-images','/opt/oracle/apex/images'],'','ords-start')
if mode=='verify':
 verify()
if mode not in ['inputs', 'apex-download', 'apex-install', 'apex-configure', 'application-import', 'ords-install', 'ords-start', 'verify']:raise ValueError('Unknown platform operation')
