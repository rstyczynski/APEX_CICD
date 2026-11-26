"""Real native SQLcl PROJECT experiment; no credentials retained in source."""
import hashlib,json,os,re,subprocess
from pathlib import Path
ROOT=Path.cwd(); OUT=ROOT/'result';OUT.mkdir(exist_ok=True)
SQL=os.environ['SQL_EXE']; BUILD='25.4.1.022.0618'
version=subprocess.check_output([SQL,'-version'],text=True,stderr=subprocess.STDOUT)
assert BUILD in version,version
(OUT/'tool.txt').write_text(version)
P=Path(os.environ['RUNNER_TEMP'])/'native';P.mkdir(exist_ok=True)

def sql(body,label,user='AUTHOR16',cwd=P):
    prefix='whenever sqlerror exit failure rollback\nwhenever oserror exit failure rollback\n'
    if user:prefix+=f'connect {user}/Disposable_Native_16@//127.0.0.1:1521/FREEPDB1\n'
    r=subprocess.run([SQL,'-nohistory','-noupdates','-S','-L','/nolog'],input=prefix+body+'\nexit\n',text=True,capture_output=True,cwd=cwd,timeout=240)
    out=r.stdout+r.stderr;(OUT/(label+'.log')).write_text(out)
    assert r.returncode==0 and not re.search(r'(?im)^\s*(ORA-|PLS-|SP2-|ERROR\b|Error starting|Unknown Command)|Expected a subcommand',out),out[-6000:]
    return out

def git(*args):return subprocess.check_output(['git',*args],cwd=P,text=True).strip()
from provenance import guard

def package(v):
    sql('project gen-artifact -name native16 -version '+v,'package-'+v)
    archives=list(P.rglob('*.zip'));a=max(archives,key=lambda x:x.stat().st_mtime)
    data=a.read_bytes();target=OUT/a.name;target.write_bytes(data)
    receipt=dict(source=git('rev-parse','HEAD'),build=BUILD,sha256=hashlib.sha256(data).hexdigest(),version=v)
    (OUT/('receipt-'+v+'.json')).write_text(json.dumps(receipt,indent=2))
    return target,receipt

def deploy(a,r,label):
    config=json.loads((P/'.dbtools/project.config.json').read_text());assert config['sqlcl']['version']=='25.4.1.0'
    guard(a,r,git('rev-parse','HEAD'),BUILD)
    sql('project deploy -file '+str(a),label,'TARGET16')

sql('create table preserved (id number primary key, message varchar2(80));','author-initial')
sql('project init -name native16 -schemas AUTHOR16','init')
assert json.loads((P/'.dbtools/project.config.json').read_text())['sqlcl']['version']=='25.4.1.0'
git('init','-b','baseline');git('config','user.email','native16@example.invalid');git('config','user.name','E16 experiment');git('add','.');git('commit','-m','chore: initialize native project');git('switch','-c','release')
sql('project export -schemas AUTHOR16','export-1');git('add','.');git('commit','-m','feat: initial reviewed table')
sql('project stage -branch-name baseline\nproject verify -compared-branch-name baseline -verbose','stage-1')
sql('project release -version 1.0.0','release-1');git('add','.');git('commit','-m','chore: prepare native release 1.0.0')
a,r=package('1.0.0');deploy(a,r,'install')
sql("insert into preserved values (1,'retained across upgrade');\ncommit;",'seed','TARGET16')
git('branch','-f','baseline','HEAD')
sql('alter table preserved add (extra varchar2(80));','author-upgrade')
sql('project export -schemas AUTHOR16','export-2');git('add','.');git('commit','-m','feat: additive column upgrade')
sql('project stage -branch-name baseline\nproject verify -compared-branch-name baseline -verbose','stage-2')
sql('project release -version 1.1.0','release-2');git('add','.');git('commit','-m','chore: prepare native release 1.1.0')
a,r=package('1.1.0')
check="""select id,message,extra from preserved;
begin
 declare n number; begin select count(*) into n from preserved where id=1 and message='retained across upgrade'; if n<>1 then raise_application_error(-20016,'lost data');end if;end;
end;
/
"""
deploy(a,r,'upgrade');sql(check,'assert-upgrade','TARGET16');deploy(a,r,'repeat');sql(check,'assert-repeat','TARGET16')
before=sql('select id,message,extra from preserved;','negative-before','TARGET16')
for case in ['artifact','source','tool']:
    changed=dict(r);tool=BUILD;source=git('rev-parse','HEAD')
    if case=='artifact':changed['sha256']='0'*64
    if case=='source':source='0'*40
    if case=='tool':tool='26.3.0.260.1620'
    try:guard(a,changed,source,tool)
    except AssertionError as e:(OUT/('reject-'+case+'.txt')).write_text(str(e))
    else:raise AssertionError('negative accepted '+case)
after=sql('select id,message,extra from preserved;','negative-after','TARGET16');assert before==after
subprocess.run(['git','bundle','create',str(OUT/'native-history.bundle'),'--all'],cwd=P,check=True)
(OUT/'success.json').write_text(json.dumps(dict(native_install=True,native_upgrade=True,native_repeat=True,preserved=True,negatives=['artifact','source','tool'],source=git('rev-parse','HEAD')),indent=2))
print('PASS real native lifecycle and provenance preflight')
