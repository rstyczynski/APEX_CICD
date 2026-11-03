#!/usr/bin/env python3
"""Configure/run only the dedicated private-repository E.3 lab runner."""
import hashlib
import tarfile
import urllib.request
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent.parent
RUNNER=ROOT/'.local-apex/e3/runner'
env=dict(os.environ,E3_LAB_CONFIG=str(ROOT/'.local-apex/e3/lab.json'))
if sys.argv[1:] == ['install']:
    archive=ROOT/'.local-apex/e3/actions-runner.tar.gz'
    if not archive.exists():
        urllib.request.urlretrieve('https://github.com/actions/runner/releases/download/v2.338.2/actions-runner-osx-arm64-2.338.2.tar.gz',archive)
    if hashlib.sha256(archive.read_bytes()).hexdigest()!='25a065af409ffa317ab4d5a3b614dd15fc9c40f2172bc1b35a1b1258e919a388':
        sys.exit('Runner checksum mismatch')
    if RUNNER.exists():
        sys.exit('Runner directory exists; retained registration must not be overwritten')
    RUNNER.mkdir()
    with tarfile.open(archive) as package:
        package.extractall(RUNNER,filter='data')
    print('PASS verified official runner installation')
elif sys.argv[1:] == ['configure']:
    token=json.loads(subprocess.check_output(['gh','api','-X','POST','repos/rstyczynski/APEX_CICD_E3/actions/runners/registration-token'],text=True))['token']
    r=subprocess.run([str(RUNNER/'config.sh'),'--url','https://github.com/rstyczynski/APEX_CICD_E3','--token',token,'--name','e3-lab-mac','--labels','e3-lab','--work','_work','--unattended'],cwd=RUNNER,env=env,text=True,capture_output=True)
    print((r.stdout+r.stderr).replace(token,'[REDACTED]'))
    sys.exit(r.returncode)
elif sys.argv[1:] == ['run']:
    os.chdir(RUNNER)
    os.execve(str(RUNNER/'run.sh'),[str(RUNNER/'run.sh')],env)
else:
    sys.exit('Usage: e3-runner.py install | configure | run')
