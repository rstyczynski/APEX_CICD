"""One-time E.5 framework bootstrap on the prepared lab; refuse existing owners."""
from pathlib import Path
import hashlib,subprocess,urllib.request,zipfile,re,sys
from backend_admin import sql,ROOT
PIN='6e650fc497bce02ae611e185e66c72204f0b984a024a41733b5452e7fb6db47a'
URL='https://github.com/utPLSQL/utPLSQL/releases/download/v.3.2.3/utPLSQL.zip'
probe=sql("select 'E5_EXISTING:'||count(*) from dba_users where username in ('E5_UT','E5_TEST');",'bootstrap-preflight.log')
if 'E5_EXISTING:0' not in probe:raise SystemExit('Refusing bootstrap: E5_UT or E5_TEST already exists; use the existing fixtures, never reset them implicitly.')
cache=ROOT/'.local-apex/e5/download';cache.mkdir(parents=True,exist_ok=True)
archive=cache/'utPLSQL.zip'
if not archive.exists():urllib.request.urlretrieve(URL,archive)
assert hashlib.sha256(archive.read_bytes()).hexdigest()==PIN, 'utPLSQL checksum mismatch'
with zipfile.ZipFile(archive) as z:
 for n in z.namelist():assert not Path(n).is_absolute() and '..' not in Path(n).parts
 z.extractall(cache)
subprocess.run(['podman','--connection','apex-cicd','cp',str(cache/'utPLSQL'),'apex-db:/tmp/e5-utplsql'],check=True)
body="""whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
set sqlblanklines on
alter session set container=FREEPDB1;
create user E5_UT no authentication default tablespace users quota unlimited on users;
grant create session, create sequence, create procedure, create type, create table, create view, create synonym, alter session to E5_UT;
grant execute on dbms_lock to E5_UT;
grant execute on dbms_crypto to E5_UT;
grant execute on dbms_lob to E5_UT;
grant execute on dbms_xmlgen to E5_UT;
grant execute on dbms_sql to E5_UT;
grant execute on dbms_random to E5_UT;
@install.sql E5_UT
"""+(ROOT/'tests/sql/backend/bootstrap.sql').read_text()+"\n@create_grants.sql E5_UT E5_TEST\n@create_synonyms.sql E5_UT E5_TEST\nprompt E5_BOOTSTRAP_COMPLETE\nexit\n"
r=subprocess.run(['podman','--connection','apex-cicd','exec','-i','--user','oracle','apex-db','bash','-lc','cd /tmp/e5-utplsql/source && sqlplus -s / as sysdba'],input=body,capture_output=True,text=True,timeout=240)
out=r.stdout+r.stderr;(ROOT/'progress/E.5/tests/bootstrap.log').write_text(out)
assert r.returncode==0 and 'E5_BOOTSTRAP_COMPLETE' in out and not re.search(r'(?m)^\s*(ORA-|PLS-|SP2-)',out),out[-2000:]
import backend_runner as b
b.sql((ROOT/'examples/testable-backend/sql/hello_entry_api.sql').read_text()+'\n'+(ROOT/'tests/sql/backend/test_hello_entry_api.sql').read_text(),'backend-install.log')
print('Installed pinned E5_UT framework, isolated E5_TEST API and tests; no public grants or retained passwords.')
