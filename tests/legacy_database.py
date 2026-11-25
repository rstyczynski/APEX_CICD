"""Prepare the owned separate FREEPDB1 database for historical regression."""
import subprocess,secrets,time,json,os,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
os.chdir(ROOT)
B=['podman','--connection','apex-cicd'];name='e12-regression-db';pwd='Ee12_'+secrets.token_hex(20)
def c(*a,**kw):return subprocess.run(B+list(a),check=True,**kw)
existing=subprocess.run(B+['inspect',name],capture_output=True,text=True)
if existing.returncode==0:
 info=json.loads(existing.stdout)[0]
 if info['Config']['Labels'].get('apex.cicd.fixture')!='E12':raise RuntimeError('Unowned regression database name')
 c('exec',name,'healthcheck.sh',capture_output=True)
 print('Reusing owned regression database; private inputs will be replaced')
 raise SystemExit(0)
assert hashlib.sha256((ROOT/'.local-apex/apex_24.2.zip').read_bytes()).hexdigest()=='a7ad0ba94f70b2d581f7dde97fe27cd07afc98c32ecc146d89fd70cce9b76456'
if subprocess.run(B+['volume','exists','e12-regression-data']).returncode==0:raise RuntimeError('Unattached regression volume requires ownership inspection')
c('volume','create','--label','apex.cicd.fixture=E12','e12-regression-data')
c('secret','create','e12-regression-db-password','-',input=pwd,text=True,capture_output=True)
c('run','-d','--name',name,'--label','apex.cicd.fixture=E12','--network','apex-net','-p','127.0.0.1:1551:1521','--secret','e12-regression-db-password','-e','ORACLE_PASSWORD_FILE=/run/secrets/e12-regression-db-password','-v','e12-regression-data:/opt/oracle/oradata','docker.io/gvenzl/oracle-free@sha256:c8a729fd791c17f34f7b2e5cd4673946f2503d8cbf10c394c1d4c11d52d02f48')
for i in range(120):
 if subprocess.run(B+['exec',name,'healthcheck.sh'],capture_output=True).returncode==0:break
 time.sleep(2)
else:raise RuntimeError('New database did not become ready')
sql='''whenever sqlerror exit failure rollback
alter system set sga_target=768M scope=spfile;
alter system set sga_max_size=768M scope=spfile;
alter system set pga_aggregate_target=256M scope=spfile;
shutdown immediate;
startup;
exit
'''
r=c('exec','-i','--user','oracle',name,'bash','-lc','sqlplus -s / as sysdba',input=sql,text=True,capture_output=True)
Path('progress/E.12/tests/isolated-db-memory.log').write_text(r.stdout+r.stderr)
c('cp','.local-apex/apex_24.2.zip',name+':/tmp/apex_24.2.zip')
c('exec','--user','root',name,'bash','-lc','cd /tmp && unzip -q apex_24.2.zip && chown -R oracle:oinstall /tmp/apex')
sql='''whenever sqlerror exit failure rollback
alter session set container=FREEPDB1;
@apexins.sql SYSAUX SYSAUX TEMP /i/
create user E12_ADMIN no authentication;
grant dba,apex_administrator_role to E12_ADMIN;
create table E12_ADMIN.E12_FIXTURE_OWNER(marker varchar2(40));
insert into E12_ADMIN.E12_FIXTURE_OWNER values('APEX_CICD_E12_REGRESSION');
commit;
prompt E12_DB_READY
exit
'''
r=c('exec','-i','--user','oracle','--workdir','/tmp/apex',name,'bash','-lc','sqlplus -s / as sysdba',input=sql,text=True,capture_output=True)
Path('progress/E.12/tests/isolated-db-apex-install.log').write_text(r.stdout+r.stderr)
assert 'E12_DB_READY' in r.stdout
print('Separate FREEPDB1 regression database ready')
