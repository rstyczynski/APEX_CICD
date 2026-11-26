"""Read real E.19 Actions evidence; synthetic unit contracts are separate."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
REPO='rstyczynski/APEX_CICD_E.19'; OUT=Path('progress/E.19/tests/qualified');OUT.mkdir(parents=True,exist_ok=True)
def need(value,message):
 if not value:raise RuntimeError(message)
def gh(*args):return subprocess.check_output(['gh',*args],text=True)
def run(runid):
 r=json.loads(gh('run','view',runid,'-R',REPO,'--json','status,conclusion,headSha,jobs,createdAt,updatedAt'))
 need(r['status']=='completed' and r['conclusion']=='success','run not successful: '+runid)
 (OUT/(runid+'.json')).write_text(json.dumps(r,indent=2));return r
def main():
 matrix=run(os.environ['E19_MATRIX_RUN']); steps={s['name']:s['conclusion'] for j in matrix['jobs'] for s in j['steps']}
 for kind in ['tool','output','provenance','candidate','review']:
  need(steps.get('Action '+kind+'_valid')=='success','missing valid '+kind)
  for v in ['missing','malformed']:need(steps.get('Assert refused '+kind+'_'+v)=='success','missing refusal '+kind+' '+v)
 for name,result in steps.items():
  if name.startswith('Mutation forbidden '):need(result=='skipped','unexpected mutation '+name)
 nativeid=os.environ['E19_NATIVE_RUN'];native=run(nativeid)
 required=['Export source 1.0.0','Stage changes 1.0.0','Verify changes 1.0.0','Package release 1.0.0','Install verified release 1.0.0','Upgrade with verified release 1.1.0','Repeat identical verified release 1.1.0','Assert refusal cases preserved target','Catalogued actual tool and native project metadata','Catalogued actual repeat output','Clean job-private connection material']
 steps={s['name']:s['conclusion'] for j in native['jobs'] for s in j['steps']}
 for name in required:need(steps.get(name)=='success','native step not successful '+name)
 dest=OUT/('native-'+nativeid)
 if not dest.exists():gh('run','download',nativeid,'-R',REPO,'-n','native-'+nativeid+'-1','-D',str(dest))
 for version in ['1.0.0','1.1.0']:
  rec=json.loads((dest/f'receipt-{version}.json').read_text());need(rec['workflow_source']==native['headSha'],'native workflow source mismatch');need(rec['workflow_run']==nativeid,'run mismatch');need(hashlib.sha256((dest/f'native16-{version}.zip').read_bytes()).hexdigest()==rec['sha256'],'artifact mismatch')
 need((dest/'negative-before.log').read_bytes()==(dest/'negative-after.log').read_bytes(),'target changed on refusal')
 need(json.loads((dest/'success.json').read_text())['preserved'],'preservation absent')
 timing=run(os.environ['E19_TIMING_RUN']);td=OUT/('timings-'+os.environ['E19_TIMING_RUN'])
 if not td.exists():gh('run','download',os.environ['E19_TIMING_RUN'],'-R',REPO,'-D',str(td))
 records=[json.loads(p.read_text()) for p in td.glob('*/result.json')];need(len(records)==4,'four timing replicas required')
 need({r['source'] for r in records}=={timing['headSha']},'timing source mismatch')
 for r in records:need(len(r['samples'])==11 and all(s['milliseconds']>0 for s in r['samples']),'incomplete timings')
 print('PASS real action matrix, actual SQLcl lifecycle/provenance/refusal preservation and equivalent timing receipts')
if __name__=='__main__':main()
