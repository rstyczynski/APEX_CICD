"""Trusted E.15 operator. Never execute candidate code or expose this identity to it."""
import argparse, hashlib, json, re, secrets, subprocess, time
from pathlib import Path
TRUSTED='rstyczynski/APEX_CICD_E.15'
SOURCE='rstyczynski/APEX_CICD_E.15-candidates'

def gh(*args):
    return subprocess.check_output(['gh',*args],text=True,timeout=45)
def api(path):
    return json.loads(gh('api',path))
def current(pr):
    assert not api(f'repos/{SOURCE}/actions/permissions')['enabled'], 'candidate Actions must be disabled'
    p=api(f'repos/{SOURCE}/pulls/{pr}')
    assert p['state']=='open', 'PR must be open'
    return p

def status(head,state,url=''):
    gh('api','--method','POST',f'repos/{SOURCE}/statuses/{head}',
       '-f','context=TrustedOracle','-f','state='+state,
       '-f','description=E.15 trusted Oracle and Review validation', '-f','target_url='+url)

def plan(pr):
    p=current(pr);head=p['head']['sha'];base=p['base']['sha']
    assert base==api(f'repos/{SOURCE}/commits/main')['sha'], 'stale source base'
    files=api(f'repos/{SOURCE}/compare/{base}...{head}')['files']
    assert [f['filename'] for f in files]==['candidate.sql'], 'unreviewed paths'
    trusted=api(f'repos/{TRUSTED}/commits/main')['sha']
    report=gh('api',f'repos/{TRUSTED}/contents/review.json?ref={trusted}',
              '-H','Accept: application/vnd.github.raw+json')
    sql=gh('api',f'repos/{SOURCE}/contents/candidate.sql?ref={head}',
           '-H','Accept: application/vnd.github.raw+json')
    review=json.loads(report)
    assert review['decision']=='accept' and review['sql_sha256']==hashlib.sha256(sql.encode()).hexdigest(), 'stale Review'
    return dict(pr=pr,head=head,base=base,trusted=trusted,
                report_sha256=hashlib.sha256(report.encode()).hexdigest())

def validate_receipt(receipt):
    assert plan(receipt['pr'])=={k:receipt[k] for k in ('pr','head','base','trusted','report_sha256')}, 'stale provenance'
    run=api(f'repos/{TRUSTED}/actions/runs/{receipt["run_id"]}')
    assert run['event']=='workflow_dispatch' and run['head_sha']==receipt['trusted'], 'wrong trusted source'
    assert run['status']=='completed' and run['conclusion']=='success', 'mandatory run not successful'
    assert run['display_title']=='Oracle '+receipt['correlation'], 'wrong correlated run'
    jobs=api(run['jobs_url'])['jobs']
    oracle=[j for j in jobs if j['name']=='Oracle candidate']
    assert len(oracle)==1 and oracle[0]['conclusion']=='success'
    log=gh('api',f'repos/{TRUSTED}/actions/jobs/{oracle[0]["id"]}/logs')
    for marker in [receipt['head'], 'PASS trusted Review matches candidate bytes',
                   'PASS real Oracle greeting', 'HTTP 403', 'Table created.']:
        assert marker in log, 'missing actual execution evidence: '+marker
    return log

def validate(pr,path,pause=False):
    head=current(pr)['head']['sha'];status(head,'pending')
    try:
        receipt=plan(pr);receipt['correlation']='companion-'+secrets.token_hex(12)
        gh('workflow','run','testing.yml','--repo',TRUSTED,'--ref','main',
           '-f','correlation='+receipt['correlation'],'-f','candidate_pr='+str(pr),
           '-f','inspection_pause='+str(pause).lower())
        deadline=time.monotonic()+700
        while time.monotonic()<deadline:
            runs=api(f'repos/{TRUSTED}/actions/runs?event=workflow_dispatch&per_page=30')['workflow_runs']
            matches=[r for r in runs if r['display_title']=='Oracle '+receipt['correlation']]
            if matches:
                run=matches[0];receipt['run_id']=run['id'];receipt['run_url']=run['html_url']
                path.write_text(json.dumps(receipt,indent=2)+'\n')
                if run['status']=='completed':break
            time.sleep(8)
        else:raise TimeoutError('hosted Oracle deadline exceeded')
        log=validate_receipt(receipt)
        log=re.sub(r'(ORACLE PASSWORD FOR SYS AND SYSTEM:) .*',r'\1 [REDACTED disposable password]',log)
        path.with_suffix('.log').write_text('\n'.join(line.rstrip() for line in log.splitlines()).rstrip()+'\n')
        status(head,'success',receipt['run_url'])
        print('PASS real Oracle, exact Review and current provenance:',receipt['run_url'],flush=True)
    except Exception:
        status(head,'failure')
        raise

def main():
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['validate','publish','merge'])
    parser.add_argument('pr',type=int);parser.add_argument('receipt',type=Path);parser.add_argument('--pause',action='store_true')
    args=parser.parse_args()
    assert args.pr>0
    if args.action=='validate':validate(args.pr,args.receipt,args.pause);return
    receipt=json.loads(args.receipt.read_text());assert receipt['pr']==args.pr
    validate_receipt(receipt)
    if args.action=='publish':status(receipt['head'],'success',receipt['run_url']);print('PASS current evidence publication')
    else:
        gh('pr','merge',str(args.pr),'--repo',SOURCE,'--merge','--match-head-commit',receipt['head'])
        print('PASS ordinary protected merge for verified head',receipt['head'])
if __name__=='__main__':main()
