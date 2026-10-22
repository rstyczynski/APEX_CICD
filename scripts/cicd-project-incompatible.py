#!/usr/bin/env python3
"""Bounded G assessment: reuse compatibility rules; bind evidence before dispatch.

Native SQLcl PROJECT verification remains visible in the walkthrough. This helper
is project-authored orchestration, not an Oracle semantic-versioning feature.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import subprocess
import sys
import zipfile
from apex_sql import ROOT, run

BASE = ROOT / '.local-apex/e2/project-walkthrough'
SOURCE = BASE / 'component-repo-f2'
PROBE = BASE / 'component-repo-g'
EVIDENCE = BASE / 'g-evidence'
ARTIFACT = SOURCE / 'artifact/e2-1.0.1-execution-r2.zip'
SNAPSHOT = ROOT / 'progress/E.2/inputs/g-target-snapshot.sql'


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git(*args, repo=SOURCE):
    return subprocess.check_output(['git', '-C', str(repo), *args], text=True).strip()


def worktree_digest():
    if git('ls-files','--others','--exclude-standard','--','.dbtools','src','dist'):
        raise ValueError('Untracked source/distribution inputs; review before G')
    return hashlib.sha256(git('diff','HEAD','--','.dbtools','src','dist').encode()).hexdigest()


def validator():
    spec = importlib.util.spec_from_file_location('e1_compatibility', ROOT / 'scripts/cicd-compatibility.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.validate


def snapshot():
    return run(SNAPSHOT.read_text(), connection='user_acceptance_test').strip()


def save(name, value):
    p = EVIDENCE / name
    p.write_text(json.dumps(value, indent=2)+'\n')
    p.chmod(0o600)


def prepare():
    if EVIDENCE.exists() and PROBE.exists():
        bound()
        print('PASS existing G preparation retained; exact artifact/source/target baseline still matches')
        print('NEXT native PROJECT comparison; UAT baseline has not been recaptured')
        return
    if EVIDENCE.exists() or PROBE.exists():
        raise ValueError('Partial G preparation; inspect it before continuing')
    if not ARTIFACT.is_file():
        raise ValueError('Complete F with execution-r2 before G')
    expected = ARTIFACT.with_suffix('.sha256').read_text().strip()
    if digest(ARTIFACT) != expected:
        raise ValueError('F artifact differs from its recorded hash')
    with zipfile.ZipFile(ARTIFACT) as z:
        manifest = json.loads(z.read('component-contract.json'))
    validator()(manifest)
    if manifest['components'] != {'Foundation':'1.0.0','Hello':'1.0.1','World':'1.0.0'}:
        raise ValueError('Unexpected F component declaration')
    EVIDENCE.mkdir(mode=0o700)
    save('allowed.json', manifest)
    bad = json.loads(json.dumps(manifest))
    bad['components']['Foundation'] = '2.0.0'
    save('incompatible.json', bad)
    subprocess.run(['git','clone','--quiet','--no-hardlinks','--branch','e2-hello-patch',str(SOURCE),str(PROBE)],check=True)
    subprocess.run(['git','-C',str(PROBE),'branch','e2-world',git('rev-parse','e2-world')],check=True)
    before = snapshot()
    if 'STATUS|Available' not in before:
        raise ValueError('UAT must be Available after F')
    # Inspect installed versions independently of the candidate declaration.
    state = run("select component||'|'||version value from lab_components where installed=1 order by component;", connection='user_acceptance_test')
    for token in ('Foundation|1.0.0','Hello|1.0.1','World|1.0.0'):
        if token not in state:
            raise ValueError('UAT has not completed F: '+token)
    (EVIDENCE/'before.txt').write_text(before)
    (EVIDENCE/'before.txt').chmod(0o600)
    save('binding.json', {'source_commit':git('rev-parse','HEAD'),
         'source_worktree_sha256':worktree_digest(),
         'artifact_sha256':digest(ARTIFACT), 'allowed_sha256':digest(EVIDENCE/'allowed.json'),
         'incompatible_sha256':digest(EVIDENCE/'incompatible.json'),
         'target_snapshot_sha256':digest(EVIDENCE/'before.txt'),
         'snapshot_sql_sha256':digest(SNAPSHOT), 'validator_sha256':digest(ROOT/'scripts/cicd-compatibility.py'),
         'target':'user_acceptance_test / E1_UAT / 810005'})
    print('PASS supported Hello 1.0.1 declaration; existing compatibility validator reused')
    print('PASS immutable artifact, source revision, declarations, validator and UAT baseline bound')
    print('NEXT native PROJECT comparison in component-repo-g; no UAT deployment has run')


def bound():
    binding = json.loads((EVIDENCE/'binding.json').read_text())
    checks = {'source_commit':git('rev-parse','HEAD'),
        'source_worktree_sha256':worktree_digest(), 'artifact_sha256':digest(ARTIFACT),
        'allowed_sha256':digest(EVIDENCE/'allowed.json'),
        'incompatible_sha256':digest(EVIDENCE/'incompatible.json'),
        'target_snapshot_sha256':digest(EVIDENCE/'before.txt'),
        'snapshot_sql_sha256':digest(SNAPSHOT), 'validator_sha256':digest(ROOT/'scripts/cicd-compatibility.py')}
    for key,value in checks.items():
        if binding[key] != value:
            raise ValueError('STALE G binding: '+key+'; no deploy invoked')
    if snapshot() != (EVIDENCE/'before.txt').read_text():
        raise ValueError('Target changed since G baseline; no deploy invoked')
    return binding


def reject():
    binding = bound()
    calls = []
    def dispatch():
        # The real deploy is reachable only after the existing validator admits
        # the exact bound declaration. For the incompatible fixture it must not run.
        validator()(json.loads((EVIDENCE/'incompatible.json').read_text()))
        calls.append('project deploy')
        return run('cd "'+str(SOURCE)+'"\nset define on\ndefine DEFAULTS_FILE=utils/properties/uat.properties\nproject deploy -file artifact/e2-1.0.1-execution-r2.zip', connection='user_acceptance_test')
    reason = None
    try:
        dispatch()
    except ValueError as exc:
        reason = str(exc)
    if calls or reason != 'Hello requires Foundation 1.0.0; proposed Foundation 2.0.0':
        raise ValueError('Unexpected admission outcome; inspect G evidence')
    if snapshot() != (EVIDENCE/'before.txt').read_text():
        raise ValueError('Target changed during rejected proposal')
    save('rejection.json', {'binding':binding, 'result':'REJECTED', 'reason':reason,
        'deploy_invocations':len(calls), 'target_unchanged':True,
        'scope':'metadata-only proposal; project-authored gate reusing E.1 validator; no Foundation DDL'})
    print('REJECTED INCOMPATIBLE: '+reason)
    print('PASS PROJECT deploy invocations: 0')
    print('PASS UAT business rows, installed versions, migration history, schema DDL and APEX export unchanged')


def check():
    binding = bound()
    receipt = json.loads((EVIDENCE/'rejection.json').read_text())
    if receipt.get('binding') != binding:
        raise ValueError('Rejection receipt does not match the current binding')
    if receipt['deploy_invocations'] != 0 or receipt['result'] != 'REJECTED':
        raise ValueError('Missing expected rejection receipt')
    print('PASS retained rejection receipt; PROJECT deploy invocations: 0')
    print('PASS exact UAT baseline unchanged; application remains Available')


if __name__ == '__main__':
    try:
        actions = {'prepare':prepare, 'reject':reject, 'check':check}
        if len(sys.argv)!=2 or sys.argv[1] not in actions:
            raise ValueError('Usage: cicd-project-incompatible.py prepare|reject|check')
        actions[sys.argv[1]]()
    except (ValueError, KeyError, OSError, RuntimeError, subprocess.SubprocessError, zipfile.BadZipFile) as exc:
        print('BLOCKED: '+str(exc), file=sys.stderr)
        sys.exit(1)
