"""Execute archived E.1 release operations against the isolated real regression PDB."""
import sys,os,json,re,subprocess,hashlib,tempfile,importlib.util,urllib.request,urllib.parse,http.cookiejar,html,tarfile,io,zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from apex_sql import ROOT,run,secrets
if os.environ.get('APEX_CICD_ISOLATED_E1')!='1':raise RuntimeError('Owned isolated regression environment required')
OUT=Path(os.environ['APEX_CICD_REGRESSION_EVIDENCE'])
INITIAL=Path((ROOT/'.local-apex/releases/initial-selected.txt').read_text().strip())
PATCH=Path(Path(os.environ.get('APEX_CICD_PATCH_SELECTION',str(ROOT/'.local-apex/releases/patch-selected.txt'))).read_text().strip())
for k in ['INITIAL','PATCH']:
 if not globals()[k].is_absolute():globals()[k]=ROOT/globals()[k]
def command(*args,expected=0):
 r=subprocess.run(args,cwd=ROOT,capture_output=True,text=True,timeout=300)
 out=r.stdout+r.stderr
 for value in secrets().values():
  if isinstance(value,str) and value:out=out.replace(value,'[REDACTED]')
 with (OUT/'operations.log').open('a') as f:f.write('COMMAND '+repr(args)+'\n'+out+'\nEXIT '+str(r.returncode)+'\n')
 if (r.returncode==0)!=(expected==0):raise RuntimeError(out[-2200:])
 return out

def state(target):
 text=run('set serveroutput on\nbegin E1_CTRL.e1_release.show_status; end;\n/',connection=target)
 return int(re.search(r'EPOCH=(\d+)',text)[1])
def sql(target,source):
 result=run(source,connection=target)
 with (OUT/'runtime.log').open('a') as f:f.write(target+'\n'+result)
 return result

def post(op,page,request,items=()):
 def byname(k):return html.unescape(re.search(r'name="'+k+r'" value="([^"]*)"',page)[1])
 def byid(k):
  m=re.search(r'id="'+k+r'" value="([^"]*)"',page)
  if not m:m=re.search(r'value="([^"]*)" id="'+k+r'"',page)
  return html.unescape(m[1]) if m else ''
 fields={k:byname(k) for k in ['p_flow_id','p_flow_step_id','p_instance','p_page_submission_id']}
 fields.update(p_request=request,p_reload_on_submit='S',p_json=json.dumps({'pageItems':{'itemsToSubmit':[{'n':n,'v':v} for n,v in items],'protected':byid('pPageItemsProtected'),'rowVersion':byid('pPageItemsRowVersion')},'salt':byid('pSalt')}))
 return op.open(os.environ['APEX_CICD_HTTP_BASE']+'wwv_flow.accept',urllib.parse.urlencode(fields).encode(),timeout=30).read().decode()
def browser(app,user='VERIFIER',request=None):
 base=os.environ['APEX_CICD_HTTP_BASE'];op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
 page=op.open(base+f'f?p={app}:1',timeout=30).read().decode()
 response=post(op,page,'LOGIN',[('P9999_USERNAME',user),('P9999_PASSWORD',secrets()[user]),('P9999_REMEMBER','N')])
 data=json.loads(response)
 assert 'redirectURL' in data,response[:200]
 page=op.open(urllib.parse.urljoin(base,data['redirectURL']),timeout=30).read().decode()
 assert f'APP_USER: "{user}"' in page,'Native login did not authenticate'
 if request:
  response=post(op,page,request)
  if response.lstrip().startswith('{'):
   data=json.loads(response)
   if 'redirectURL' in data:response=op.open(urllib.parse.urljoin(base,data['redirectURL']),timeout=30).read().decode()
  return response
 return page

def verify_runtime(target,app):
 sql(target,f'@"{ROOT}/deploy/operator/walkthrough_runtime.sql" '+('E1_INTEGRATION' if target=='integration_test' else 'E1_UAT')+f' {app}')
 before=sql(target,"set heading off pagesize 0\nselect count(*) from greeting_history;")
 page=browser(app,request='CREATE_GREETING')
 # Actual HTTP page-process submission must create exactly one additional snapshot.
 after=sql(target,"set heading off pagesize 0\nselect count(*) from greeting_history;")
 def count(s):return int(re.search(r'(?m)^\s*(\d+)\s*$',s)[1])
 assert count(after)==count(before)+1,'HTTP greeting submission did not create a snapshot'
 sql(target,"declare n number; begin select count(*) into n from greeting_history where actor='VERIFIER' and greeting_text='Hello World'; if n<2 then raise_application_error(-20001,'HTTP greeting missing'); end if; end;\n/")
 (OUT/f'http-{target}-{state(target)}.html').write_text(re.sub(r'\b\d{10,}\b','[SESSION]',re.sub(r'<input\b[^>]*>','',re.sub(r'(?s)<script.*?</script>','',page))))
 print('PASS actual authenticated HTTP greeting '+target,flush=True)

def initial(target):
 epoch=state(target)
 command('bash','scripts/cicd-release-step.sh',str(INITIAL),target,'admit',str(epoch));epoch+=1
 for operation in ['migrate','import','units','verify']:
  command('bash','scripts/cicd-release-step.sh',str(INITIAL),target,operation,str(epoch))
  if operation=='migrate':sql(target,'begin dbms_utility.compile_schema(user,false); end;\n/')
 verify_runtime(target,810004 if target=='integration_test' else 810005)
 command('bash','scripts/cicd-release-step.sh',str(INITIAL),target,'publish',str(epoch))
 command('bash','scripts/cicd-release-result.sh',str(INITIAL),target)

def patch(target,start):
 epoch=state(target)
 for operation in ['preflight','admit','migrate','import','units','verify']:
  command('bash','scripts/cicd-patch-step.sh',str(PATCH),target,operation,str(epoch),start)
  if operation=='admit':epoch+=1
  if operation=='migrate':sql(target,'begin dbms_utility.compile_schema(user,false); end;\n/')
 verify_runtime(target,810004 if target=='integration_test' else 810005)
 command('bash','scripts/cicd-patch-step.sh',str(PATCH),target,'publish',str(epoch),start)
 command('bash','scripts/cicd-patch-step.sh',str(PATCH),target,'result',str(epoch),'1.0.0')

def capture(target,name):command(sys.executable,'scripts/cicd-preservation.py','capture',target,str(OUT/name))
def compare(target,name):command(sys.executable,'scripts/cicd-preservation.py','compare',target,str(OUT/name))
def reset():
 if (OUT/'uat-before.json').exists():compare('user_acceptance_test','uat-before.json')
 command(sys.executable,'scripts/cicd-platform.py','reset-integration-test')
 if (OUT/'uat-before.json').exists():compare('user_acceptance_test','uat-before.json')

def rebuild_candidate():
 global PATCH
 spec=importlib.util.spec_from_file_location('e12_artifact',ROOT/'scripts/cicd-artifact.py');artifact=importlib.util.module_from_spec(spec);spec.loader.exec_module(artifact)
 _,old,files=artifact.inspect(PATCH);revision=old['source_commit']
 assert hashlib.sha256(INITIAL.read_bytes()).hexdigest()==json.loads(files['release/manifest.json'])['base_artifact'],'Initial dependency differs from accepted manifest'
 pr=json.loads(command('gh','api','repos/rstyczynski/APEX_CICD/pulls/1','--jq','{number,merged,merged_at,merge_commit_sha,html_url}'))
 assert pr['merged'] is True
 command('git','merge-base','--is-ancestor',revision,pr['merge_commit_sha'])
 (OUT/'accepted-pr.json').write_text(json.dumps({k:pr[k] for k in ['number','merged','merged_at','merge_commit_sha','html_url']},indent=2))
 payload=Path(os.environ['APEX_CICD_STATE'])/'candidate-source';payload.mkdir()
 for name in files:
  if name in ['artifact.json','candidate.json','candidate.log']:continue
  actual=subprocess.check_output(['git','show',revision+':'+name],cwd=ROOT)
  assert hashlib.sha256(actual).hexdigest()==old['files'][name],name
  p=payload/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(actual)
 candidate_log=sql('lab-dev-c',f'cd "{payload}"\nlb update -changelog-file db/changelog.xml\n@"{ROOT}/deploy/operator/import.sql" E1_DEV_C 810003 E1_DEV_C E12-CANDIDATE "{payload}/apex/f810001"\nbegin apex_util.set_workspace(user); apex_application_admin.set_application_status(810003,apex_application_admin.c_app_available); update lab_state set state=\'ready\' where state_key=\'Application\'; commit; end;\n/\nbegin dbms_utility.compile_schema(user,false); end;\n/\n@"{ROOT}/deploy/checks/patch_development.sql"\n@"{ROOT}/tests/sql/composition.sql"\n@"{ROOT}/tests/sql/history.sql"\n@"{ROOT}/tests/sql/hello_patch.sql"')
 files={name:(payload/name).read_bytes() for name in files if name not in ['artifact.json','candidate.json','candidate.log']}
 files['candidate.log']=candidate_log.encode()
 files['candidate.json']=(json.dumps({'source_commit':revision,'status':'passed','accepted_pr':pr['html_url'],'accepted_merge_commit':pr['merge_commit_sha'],'scope':'fresh native candidate validation in isolated DEV_C; existing merged PR 1 context, no new remote event','log_sha256':artifact.sha(files['candidate.log'])},indent=2)+'\n').encode()
 info={'format':1,'source_commit':revision,'files':{n:artifact.sha(v) for n,v in files.items()},'configuration_sha256':artifact.sha(files['config/areas.json'])}
 files['artifact.json']=(json.dumps(info,sort_keys=True,indent=2)+'\n').encode()
 PATCH=OUT/('lab-1.0.1-'+revision[:12]+'.tar')
 with tarfile.open(PATCH,mode='w',format=tarfile.USTAR_FORMAT) as tar:
  for name in sorted(files):
   member=tarfile.TarInfo(name);member.size=len(files[name]);member.mode=0o644;member.mtime=0
   tar.addfile(member,io.BytesIO(files[name]))
 PATCH.with_suffix('.tar.sha256').write_text(artifact.sha(PATCH.read_bytes())+'\n');artifact.inspect(PATCH)
 stale=dict(files);proof=json.loads(stale['candidate.json']);proof['source_commit']='0'*40;stale['candidate.json']=json.dumps(proof).encode()
 stale_info=json.loads(stale['artifact.json']);stale_info['files']['candidate.json']=artifact.sha(stale['candidate.json']);stale['artifact.json']=json.dumps(stale_info).encode()
 bad=OUT/'rejected-stale-candidate.tar'
 with tarfile.open(bad,'w',format=tarfile.USTAR_FORMAT) as tar:
  for name in sorted(stale):
   member=tarfile.TarInfo(name);member.size=len(stale[name]);member.mode=0o644;tar.addfile(member,io.BytesIO(stale[name]))
 bad.with_suffix('.tar.sha256').write_text(artifact.sha(bad.read_bytes())+'\n')
 rejection=command(sys.executable,'scripts/cicd-artifact.py','inspect',str(bad),expected=1)
 assert 'Candidate validation does not match release source' in rejection
 (OUT/'patch-selected.txt').write_text(str(PATCH)+'\n')
 print('BUILT accepted-PR source archive '+str(PATCH)+' SHA256 '+artifact.sha(PATCH.read_bytes()),flush=True)

def release():
 rebuild_candidate()
 accepted_hash=hashlib.sha256(PATCH.read_bytes()).hexdigest()
 # Compare actual native exports, without dates, from the same unchanged developer state.
 for label in ['export-a','export-b']:
  sql('lab-dev',f'apex export -applicationid 810001 -split -skipExportDate -expOriginalIds -expSupportingObjects N -dir "{Path(os.environ['APEX_CICD_STATE'])/label}"')
 a={str(p.relative_to(Path(os.environ['APEX_CICD_STATE'])/'export-a')):p.read_bytes() for p in (Path(os.environ['APEX_CICD_STATE'])/'export-a').rglob('*') if p.is_file()}
 b={str(p.relative_to(Path(os.environ['APEX_CICD_STATE'])/'export-b')):p.read_bytes() for p in (Path(os.environ['APEX_CICD_STATE'])/'export-b').rglob('*') if p.is_file()}
 assert a and a==b,'Unchanged native exports differ'
 with zipfile.ZipFile(OUT/'stable-native-exports.zip','w',zipfile.ZIP_DEFLATED) as z:
  for label,fileset in [('export-a',a),('export-b',b)]:
   for name,data in fileset.items():z.writestr(label+'/'+name,data)
 (OUT/'native-export-stability.json').write_text(json.dumps({n:hashlib.sha256(v).hexdigest() for n,v in a.items()},indent=2))
 for archive in [INITIAL,PATCH]:command(sys.executable,'scripts/cicd-artifact.py','inspect',str(archive))
 # Changed bytes must fail archive identity before any target operation.
 with tempfile.TemporaryDirectory() as td:
  tampered=Path(td)/'changed.tar.gz';tampered.write_bytes(PATCH.read_bytes()+b'changed')
  tampered.with_suffix(tampered.suffix+'.sha256').write_text(hashlib.sha256(PATCH.read_bytes()).hexdigest())
  rejected=command(sys.executable,'scripts/cicd-artifact.py','inspect',str(tampered),expected=1)
  assert 'Artifact SHA-256 mismatch' in rejected
 # Reject promotion without qualification and leave the target generation untouched.
 uat_epoch=state('user_acceptance_test')
 rejected=command('bash','scripts/cicd-release-step.sh',str(INITIAL),'user_acceptance_test','admit',str(uat_epoch),expected=1)
 assert 'ORA-20614' in rejected,'Missing qualification did not cause its specific rejection'
 assert state('user_acceptance_test')==uat_epoch
 initial('integration_test');initial('user_acceptance_test')
 sql('user_acceptance_test',f'@"{ROOT}/tests/sql/prepare_history_sentinels.sql"')
 capture('user_acceptance_test','uat-before.json')
 # Fresh patch qualification, followed by a separately reconstructed baseline upgrade.
 reset();patch('integration_test','empty')
 reset();initial('integration_test')
 # Twenty snapshots in this upgrade fixture, then compare every saved field.
 sql('integration_test',"begin for i in 1..20 loop declare s varchar2(32767); begin s:=lab_runtime.record_greeting; end; end loop; commit; end;\n/")
 capture('integration_test','q-before.json')
 epoch=state('integration_test')
 sql('integration_test',"update lab_components set version='9.0.0' where component='Hello'; commit;")
 try:
  rejected=command('bash','scripts/cicd-patch-step.sh',str(PATCH),'integration_test','admit',str(epoch),'1.0.0',expected=1)
  assert 'ORA-20605' in rejected,'Unsupported start did not reach version rejection'
  assert state('integration_test')==epoch
 finally:sql('integration_test',"update lab_components set version='1.0.0' where component='Hello'; commit;")
 patch('integration_test','1.0.0');compare('integration_test','q-before.json')
 patch('user_acceptance_test','1.0.0');compare('user_acceptance_test','uat-before.json')
 assert hashlib.sha256(PATCH.read_bytes()).hexdigest()==accepted_hash,'Archive changed during promotion'
 print('PASS native export stability, archive identity, fresh reconstruction, both patch starts, HTTP greetings and preserved UAT upgrade',flush=True)

def result():
 for target in ['integration_test','user_acceptance_test']:
  before=sql(target,'set serveroutput on\nbegin E1_CTRL.e1_release.show_status; end;\n/')
  capture(target,target+'-repeat-before.json')
  repeat=command('bash','scripts/cicd-patch-step.sh',str(PATCH),target,'admit',str(state(target)),'1.0.0')
  assert 'ALREADY DELIVERED:' in repeat,'Repeat admission did not stop before migration/import'
  command('bash','scripts/cicd-patch-result.sh',target)
  capture(target,target+'-repeat-after.json')
  assert json.loads((OUT/(target+'-repeat-before.json')).read_text())==json.loads((OUT/(target+'-repeat-after.json')).read_text()),'Repeat changed business fields or appended rows'
  assert before==sql(target,'set serveroutput on\nbegin E1_CTRL.e1_release.show_status; end;\n/'),'Repeat changed the release generation or receipt'

 compare('integration_test','q-before.json');compare('user_acceptance_test','uat-before.json')
 sql('user_acceptance_test',f'@"{ROOT}/tests/sql/hello_patch.sql"');sql('lab-control',f'@"{ROOT}/tests/sql/patch_receipts.sql"')
 print('PASS identical patch receipts, repeat no-op and complete preserved fields',flush=True)

def assembly():
 sql('lab-dev',f'@"{ROOT}/deploy/operator/foundation_verify.sql"\n@"{ROOT}/deploy/checks/foundation_contract.sql"')
 opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
 page=opener.open(os.environ['APEX_CICD_HTTP_BASE']+'f?p=810001:1',timeout=30).read().decode()
 assert 'Foundation assembly: Hello and World are not installed.' in page,'Native unavailable-page message missing'
 (OUT/'assembly-rejection.html').write_text(re.sub(r'\b\d{10,}\b','[SESSION]',re.sub(r'<input\b[^>]*>','',re.sub(r'(?s)<script.*?</script>','',page))))
 print('PASS incomplete assembly metadata, native contract rejection and native HTTP unavailability',flush=True)
if __name__=='__main__':{'release':release,'result':result,'assembly':assembly}[sys.argv[1]]()
