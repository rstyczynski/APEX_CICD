#!/usr/bin/env python3
"""Verify live E.3 evidence; never pass merely because a receipt exists."""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent.parent
LOCAL=ROOT/'.local-apex/e3'
os.environ['E3_LAB_CONFIG']=str(LOCAL/'lab.json')
REPOSITORY='rstyczynski/APEX_CICD_E3'


def gh(*args):
    return json.loads(subprocess.check_output(['gh',*args],text=True))


def lab(path):
    spec=importlib.util.spec_from_file_location('e3_lab',path/'scripts/lab.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod


def journey():
    e=json.loads((ROOT/'progress/E.3/tests/journey.json').read_text())
    for number in [e['change_pr'],e['release_pr']]:
        pr=gh('api',f'repos/{REPOSITORY}/pulls/{number}')
        assert pr['merged'] and pr['base']['ref']=='main'
    pr=gh('api',f'repos/{REPOSITORY}/pulls/{e["change_pr"]}')
    assert 'patch' in {x['name'] for x in pr['labels']} and pr['title'].startswith('fix:')
    ref=gh('api',f'repos/{REPOSITORY}/git/ref/tags/{e["version_tag"]}')['object']
    if ref['type']=='tag': ref=gh('api',f'repos/{REPOSITORY}/git/tags/{ref["sha"]}')['object']
    receipt=json.loads((LOCAL/'download/receipt.json').read_text())
    assert ref['sha']==receipt['source_sha']==e['release_sha']
    archives=list((LOCAL/'download').rglob('*.zip'))
    assert len(archives)==1
    assert hashlib.sha256(archives[0].read_bytes()).hexdigest()==receipt['artifact_sha256']
    r=gh('api',f'repos/{REPOSITORY}/actions/runs/{e["deploy_run"]}')
    assert r['event']=='workflow_dispatch' and r['conclusion']=='success'
    release=gh('api',f'repos/{REPOSITORY}/releases/tags/{e["version_tag"]}')
    assert not release['draft'] and 'heading' in release['body'].lower()
    repo=LOCAL/'repo'
    notes=subprocess.check_output(['git','-C',str(repo),'show',e['version_tag']+':CHANGELOG.md'],text=True)
    assert e['version_tag'][1:] in notes and release['body'].strip() in notes
    browser=json.loads((ROOT/'progress/E.3/tests/browser.json').read_text())
    assert browser['observed_heading']==receipt['heading'] and browser['history_greeting']=='Hello World'
    assert lab(repo).snapshot()==(LOCAL/'preservation-before.txt').read_text()
    assert e['no_deploy_before_dispatch'] is True and receipt['history_configuration_preserved'] is True
    assert (ROOT/'progress/E.3/tests/working-copy-diff.png').is_file()
    print('PASS live merged PRs, patch tag, both changelogs, manual successful run and current preservation')


def rejection():
    e=json.loads((ROOT/'progress/E.3/tests/journey.json').read_text())
    before=lab(LOCAL/'repo').snapshot()
    with tempfile.TemporaryDirectory(prefix='e3-rejection-',dir=LOCAL) as d:
        subprocess.run(['git','clone','--quiet','--no-hardlinks',str(LOCAL/'repo'),d],check=True)
        repo=Path(d)
        subprocess.run(['git','-C',d,'checkout','--quiet','-b','e3-rejection',e['version_tag']],check=True)
        files=list((repo/'dist/releases/next/changes').rglob('*.sql'))
        assert files,'Need an included native changeset to remove'
        missing=files[0];missing.unlink()
        r=subprocess.run([sys.executable,str(repo/'scripts/lab.py'),'verify'],env=os.environ,text=True,capture_output=True)
        out=r.stdout+r.stderr
        (ROOT/'progress/E.3/tests/native-verification-rejection.log').write_text(out)
        assert r.returncode!=0 and 'Errors:' in out and ('stagechangelogfilesvalid' in out or 'stagechangelogcomplete' in out),out
    after=lab(LOCAL/'repo').snapshot()
    assert before==after
    (ROOT/'progress/E.3/tests/rejection.json').write_text(json.dumps({'native_verification_failed':True,'target_unchanged':True,'deployment_called':False},indent=2)+'\n')
    print('PASS missing native changeset rejected before deployment; target unchanged')


if __name__=='__main__':
    {'journey':journey,'rejection':rejection}[sys.argv[1]]()
