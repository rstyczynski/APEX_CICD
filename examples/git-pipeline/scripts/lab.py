#!/usr/bin/env python3
"""Thin SQLcl boundary for the E.3 native PROJECT example. No migration engine."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
ANSI = re.compile(r'\x1b\[[0-9;]*m')
ERROR = re.compile(r'(?im)^\s*(ORA-\d+:|PLS-\d+:|SP2-\d+:|ERROR\b|Errors:\s*[1-9]\d*|Unknown Command|SEVERE:)|Option not recognized|Option not found|No database connection|java\.[\w.]+Exception')


def config():
    p = Path(os.environ['E3_LAB_CONFIG']).resolve()
    if p.stat().st_mode & 0o077:
        raise ValueError('E3_LAB_CONFIG must be readable only by its owner')
    return json.loads(p.read_text())


def sql(body, role='author', offline=False):
    c = config()
    connection = '' if offline else ('connect -name ' + c['author_connection'] if role == 'author'
        else f'connect {c["target_schema"]}/"{c["target_password"]}"@//{c["service"]}')
    prefix = 'set echo off verify off define off serveroutput on\nwhenever sqlerror exit failure rollback\nwhenever oserror exit failure rollback\n'
    env = dict(os.environ, JAVA_HOME=c['java_home'])
    env.pop('JAVA_TOOL_OPTIONS', None)
    r = subprocess.run([c['sqlcl'], '-nohistory', '-noupdates', '-home', c['sqlcl_home'], '-S', '-L', '/nolog'],
        input=prefix + connection + '\n' + body + '\nprompt E3_CLIENT_COMPLETE\nexit success\n',
        text=True, capture_output=True, cwd=ROOT, env=env, timeout=300)
    output = ANSI.sub('', r.stdout + r.stderr)
    output = output.replace(c['target_password'], '[REDACTED]')
    if r.returncode or ERROR.search(output) or 'E3_CLIENT_COMPLETE' not in output:
        raise RuntimeError('SQLcl operation failed:\n' + output)
    return output


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], text=True).strip()


def verify():
    base = json.loads((ROOT / 'pipeline.json').read_text())['baseline_sha']
    if not re.fullmatch('[0-9a-f]{40}', base):
        raise ValueError('Invalid pinned baseline')
    git('branch', '-f', 'e3-base', base)
    output = sql('project verify -cbn e3-base -verbose')
    if not re.search(r'Errors:\s*0\b', output):
        raise RuntimeError('Native verification did not report zero errors:\n' + output)
    print(output)


def snapshot():
    # JSON lines stay private; do not upload business data in workflow artifacts.
    tables = [('greeting_history','greeting_id'), ('hello_entries','entry_id'),
              ('world_entries','entry_id'), ('hello_config','config_id'),
              ('world_config','config_id'), ('lab_components','component'),
              ('lab_state','state_key')]
    body='set heading off pagesize 0 feedback off linesize 32767 long 1000000 longchunksize 32767\n'
    for table, key in tables:
        body += f"select '{table}|'||json_object(*) from {table} order by {key};\n"
    return sql(body, 'target')



def build(version):
    if not re.fullmatch(r'\d+\.\d+\.\d+(?:-[a-z0-9.-]+)?', version):
        raise ValueError('Invalid artifact version')
    print(sql(f'project gen-artifact -name e3 -version {version} -format zip', offline=True))
    archive = ROOT / f'artifact/e3-{version}.zip'
    if not archive.is_file():
        raise ValueError('Native artifact missing')
    return archive


def deploy(archive):
    c = config()
    # Exact fixed disposable target; never choose UAT via a dispatch input.
    if (c['target_schema'], c['target_app']) != ('E3_TARGET', 810203):
        raise ValueError('Unexpected E.3 target')
    print(sql(f'set define on\ndefine DEFAULTS_FILE="{ROOT / "utils/properties/e3.properties"}"\n'
              + f'project deploy -file "{archive}"', 'target'))


def release(tag):
    if not re.fullmatch(r'v\d+\.\d+\.\d+', tag):
        raise ValueError('Select an exact vMAJOR.MINOR.PATCH tag')
    sha = git('rev-parse', '--verify', f'refs/tags/{tag}^{{commit}}')
    subprocess.run(['git', '-C', str(ROOT), 'merge-base', '--is-ancestor', sha, 'origin/main'], check=True)
    if git('rev-parse', 'HEAD') != sha:
        raise ValueError('Checkout must match the resolved version tag')
    if (ROOT / 'version.txt').read_text().strip() != tag[1:]:
        raise ValueError('Tag and version.txt disagree')
    release_info = json.loads(subprocess.check_output(['gh', 'release', 'view', tag, '--json', 'tagName,isDraft,body'], cwd=ROOT, text=True))
    if release_info['isDraft'] or release_info['tagName'] != tag:
        raise ValueError('Select a published release')
    verify()  # all required checks precede target writes
    archive = build(tag[1:])
    before = snapshot()
    deploy(archive)
    after = snapshot()
    if before != after:
        raise ValueError('Prior history/configuration changed; inspect failed run')
    heading = sql("set heading off pagesize 0\nselect region_name from apex_application_page_regions where application_id=810203 and page_id=1;", 'target')
    expected = json.loads((ROOT / 'pipeline.json').read_text())['expected_heading']
    if expected not in heading:
        raise ValueError('Expected Home heading missing')
    receipt = {'version_tag': tag, 'source_sha': sha, 'artifact_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
        'target_schema': 'E3_TARGET', 'target_application': 810203, 'history_configuration_preserved': True,
        'heading': expected, 'run_id': os.environ.get('GITHUB_RUN_ID', 'local'), 'sqlcl': '25.4.1.022.0618'}
    (ROOT / 'result').mkdir(exist_ok=True)
    (ROOT / 'result/receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    try:
        action, *args = sys.argv[1:]
        if action == 'sql':
            print(sql(sys.stdin.read(), args[0] if args else 'author'))
        elif action == 'capture':
            print(sql('project export -list\nproject export'))
        elif action == 'adapt-runtime':
            changed=[]
            for source in (ROOT/'src').rglob('*'):
                if source.suffix not in ('.sql','.yaml'):
                    continue
                text=source.read_text()
                old='begin E1_CTRL.e1_release.assert_runtime; end;'
                if old in text:
                    source.write_text(text.replace(old,'begin lab_runtime.assert_ready; end;'))
                    changed.append(str(source.relative_to(ROOT)))
            print('REVIEW explicit E3 runtime adapter before stage: '+', '.join(changed))
        elif action == 'stage':
            print(sql('project stage -branch-name e3-base'))
        elif action == 'verify':
            verify()
        elif action == 'build':
            print(build(args[0]))
        elif action == 'deploy':
            deploy(Path(args[0]).resolve())
        elif action == 'snapshot':
            print(snapshot(), end='')
        elif action == 'release':
            release(args[0])
        else:
            raise ValueError('Unknown operation')
    except (ValueError, RuntimeError, KeyError, subprocess.SubprocessError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
