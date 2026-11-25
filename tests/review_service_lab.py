"""Live loopback API and native local Git receive experiment, no remote publication."""
import concurrent.futures
import copy
import gzip
import json
import os
import subprocess
import sys
import tempfile
import threading
import urllib.error
import urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from review_service import Service, git

OUT = ROOT / 'progress/E.9/tests/service'
OUT.mkdir(parents=True, exist_ok=True)
observations = []
with tempfile.TemporaryDirectory(prefix='e9-authenticated-') as temp:
    home = Path(temp)
    service = Service(home)
    work = home / 'work'
    work.mkdir()
    git(work, 'init', '-b', 'main')
    git(work, 'config', 'user.name', 'E9 developer')
    git(work, 'config', 'user.email', 'developer@example.invalid')
    (work / 'greeting.py').write_text('def greet(name):\n    return "Hello " + name\n')
    git(work, 'add', '.')
    git(work, 'commit', '-m', 'Greeting baseline')
    base = git(work, 'rev-parse', 'HEAD')
    git(work, 'checkout', '-b', 'feature')
    (work / 'greeting.py').write_text('def greet(name):\n    return "Hello " + name.strip()\n')
    git(work, 'commit', '-am', 'Normalize outer whitespace')
    head1 = git(work, 'rev-parse', 'HEAD')
    initial_diff = git(work, 'diff', base, head1)
    (work / 'test_greeting.py').write_text('from greeting import greet\nassert greet(" World ")=="Hello World"\n')
    git(work, 'add', '.')
    git(work, 'commit', '-m', 'Add greeting assertion')
    head = git(work, 'rev-parse', 'HEAD')
    diff = git(work, 'diff', base, head)
    subprocess.run([sys.executable, 'test_greeting.py'], cwd=work, check=True)
    # Trusted fixture bootstrap imports objects before API clients receive access.
    git(service.repo, 'fetch', str(work), 'main:refs/heads/main', 'feature:refs/heads/feature')
    url = service.start()

    def call(role, action, data=None, expected=200, label=None):
        token = service.tokens.get(role, 'invalid-token')
        request = urllib.request.Request(url + '/' + action,
                    data=json.dumps(data or {}).encode(),
                    headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                status, value = response.status, json.load(response)
        except urllib.error.HTTPError as error:
            status, value = error.code, json.load(error)
        assert status == expected, (label or action, expected, status, value)
        observations.append({'case': label or action, 'http': status, 'result': copy.deepcopy(value)})
        return value

    def report():
        c = call('developer', 'state')['candidate']
        template = json.loads((ROOT / 'progress/E.9/tests/agent-review-template.json').read_text())
        return {**template, **c}

    def ready():
        r = report()
        key = call('developer', 'submit', {'report': r})['hash']
        accepted = call('review', 'publish')
        c = call('developer', 'state')['candidate']
        call('testing', 'testing', {'candidate': c, 'state': 'success'})
        call('approver', 'approve')
        return r, key, accepted

    try:
        call('intruder', 'state', expected=403, label='invalid credential')
        r = report()
        for role, action, data in [('testing', 'submit', {'report': r}),
                                   ('developer', 'publish', {'role': 'review'}),
                                   ('developer', 'testing', {'publisher': 'testing'}),
                                   ('developer', 'approve', {}),
                                   ('developer', 'merge', {}),
                                   ('developer', 'bypass', {'reason': 'spoof'})]:
            call(role, action, data, 403, 'unauthorized ' + action)
        for kind in ('missing assessment', 'unknown severity', 'unresolved blocker', 'ack-only dismissal'):
            bad = copy.deepcopy(r)
            if kind == 'missing assessment':
                del bad['assessments']['testing']
            elif kind == 'unknown severity':
                bad['findings'] = [{'severity': 'unknown', 'state': 'open'}]
            elif kind == 'unresolved blocker':
                bad['findings'] = [{'severity': 'blocker', 'state': 'open'}]
            else:
                bad['findings'] = [{'severity': 'blocker', 'state': 'dismissed', 'reason': 'acknowledged'}]
            call('developer', 'submit', {'report': bad}, 409, kind)
        assert git(service.repo, 'rev-parse', 'feature') == head
        call('integrator', 'merge', expected=409, label='missing evidence')
        r, key, accepted = ready()
        for state in ('failure', 'neutral', 'cancelled', 'skipped'):
            call('testing', 'testing', {'candidate': service.candidate(), 'state': state})
            call('integrator', 'merge', expected=409, label='nonpassing Testing ' + state)
        r, key, accepted = ready()
        call('developer', 'conversation', {'count': 1})
        call('integrator', 'merge', expected=409, label='unresolved conversation')
        call('developer', 'conversation', {'count': 0})
        # Accepted report is immutable history even after current report edit/delete.
        for action in ('edit', 'withdraw', 'delete'):
            r, key, accepted = ready()
            data = {}
            if action == 'edit':
                r['assessments']['testing'] += ' Additional limitation.'
                data = {'report': r}
            call('developer', action, data)
            call('integrator', 'merge', expected=409, label=action + ' invalidates')
            old = call('developer', 'report', {'hash': key})
            assert old == json.loads((service.store / (key + '.json')).read_text())
            assert 'Review' not in call('developer', 'state')['checks']
        for action, role, sha in [('head', 'developer', head1), ('base', 'administrator', head1)]:
            ready()
            call(role, action, {'sha': sha})
            call('integrator', 'merge', expected=409, label=action + ' invalidates')
            call(role, action, {'sha': head if action == 'head' else base})
        ready()
        call('administrator', 'policy', {'version': 2, 'independent_approval': True})
        call('integrator', 'merge', expected=409, label='policy invalidates')
        # Real concurrent HTTP event during report publication.
        for mutation in ('head', 'edit', 'withdraw', 'delete'):
            ready()
            entered, release = threading.Event(), threading.Event()
            def pause():
                entered.set()
                assert release.wait(10), 'race release timed out'
            service.pause_publication = pause
            with concurrent.futures.ThreadPoolExecutor() as pool:
                pending = pool.submit(call, 'review', 'publish', {}, 409, 'publication race ' + mutation)
                assert entered.wait(10)
                if mutation == 'head':
                    call('developer', 'head', {'sha': head1})
                elif mutation == 'edit':
                    changed = report(); changed['assessments']['security'] += ' Refreshed.'
                    call('developer', 'edit', {'report': changed})
                else:
                    call('developer', mutation)
                release.set()
                pending.result(timeout=10)
            service.pause_publication = None
            call('integrator', 'merge', expected=409, label='no stale success after race ' + mutation)
            if mutation == 'head':
                call('developer', 'head', {'sha': head})
        ready()
        # A change serialized before the merge lock must cause rejection.
        call('developer', 'head', {'sha': head1})
        call('integrator', 'merge', expected=409, label='change before integration')
        call('developer', 'head', {'sha': head})
        # Native receive-pack, not a mocked direct-write verdict. Local filesystem only.
        direct = subprocess.run(['git', '-C', str(work), 'send-pack', str(service.repo),
                                 'feature:refs/heads/main'], text=True, capture_output=True)
        raw_receive = direct.stdout + direct.stderr
        (OUT / 'direct-write.raw.gz').write_bytes(gzip.compress(raw_receive.encode(), mtime=0))
        (OUT / 'direct-write.log').write_text('\n'.join(line.rstrip() for line in raw_receive.splitlines()) + '\n')
        assert direct.returncode != 0 and 'pre-receive hook declined' in direct.stderr
        assert git(service.repo, 'rev-parse', 'main') == base
        observations.append({'case': 'native unauthorized direct write', 'exit': direct.returncode, 'ref_unchanged': True})
        ready()
        service.approval = None  # server-side loss of approval must fail closed
        call('integrator', 'merge', expected=409, label='missing independent approval')
        call('approver', 'approve')
        # Fault-inject corrupt stored evidence to test defense beyond API role checks.
        service.checks['Review']['publisher'] = 'developer'
        call('integrator', 'merge', expected=409, label='wrong persisted Review publisher')
        ready()
        service.checks['Testing']['publisher'] = 'developer'
        call('integrator', 'merge', expected=409, label='wrong persisted Testing publisher')
        ready()
        service.checks['Testing']['candidate'] = {'head': 'stale'}
        call('integrator', 'merge', expected=409, label='stale persisted Testing')
        r, key, accepted = ready()
        # Hold the actual merge critical section while a competing report edit arrives.
        merge_entered, merge_release = threading.Event(), threading.Event()
        def hold_merge():
            merge_entered.set()
            assert merge_release.wait(10)
        service.before_merge = hold_merge
        changed = copy.deepcopy(r); changed['assessments']['security'] += ' Concurrent edit.'
        with concurrent.futures.ThreadPoolExecutor() as pool:
            pending_merge = pool.submit(call, 'integrator', 'merge', {}, 200, 'ordinary controlled merge')
            assert merge_entered.wait(10)
            pending_edit = pool.submit(call, 'developer', 'edit', {'report': changed}, 409, 'concurrent edit serialized after merge')
            merge_release.set()
            merged = pending_merge.result(timeout=10)
            pending_edit.result(timeout=10)
        service.before_merge = None
        assert git(service.repo, 'rev-parse', 'main') == merged['commit']
        assert git(service.repo, 'rev-list', '--parents', '-n', '1', merged['commit']).split()[1:] == [base, head]
        # Inspect and run code from actual integrated source.
        (home / 'merged.py').write_text(git(service.repo, 'show', 'main:greeting.py') + '\nassert greet(" World ")=="Hello World"\n')
        subprocess.run([sys.executable, str(home / 'merged.py')], check=True)
        call('integrator', 'merge', expected=409, label='old success cannot authorize new base')
        call('administrator', 'bypass', {}, 409, 'unexplained bypass')
        bypass = call('administrator', 'bypass', {'reason': 'E9 authorized exception experiment'}, label='recorded administrator bypass')
        assert bypass['reason'] and bypass['actor'] == 'administrator'
        for file in service.store.glob('*.json'):
            (OUT / file.name).write_bytes(file.read_bytes())
        git(service.repo, 'bundle', 'create', str(OUT / 'candidate.bundle'), '--all')
        (OUT / 'initial.diff').write_text(initial_diff + '\n')
        (OUT / 'refreshed.diff').write_text(diff + '\n')
        (OUT / 'receipt.json').write_text(json.dumps(accepted, indent=2) + '\n')
        (OUT / 'events.json').write_text(json.dumps(service.events, indent=2) + '\n')
        (OUT / 'results.json').write_text(json.dumps(observations, indent=2) + '\n')
        print(json.dumps({'status': 'PASS', 'observations': len(observations),
                          'ordinary_merge': merged, 'bypass': bypass,
                          'scope': 'real loopback capabilities, serialized service, native local Git receive hook; trusted host'}, indent=2))
    finally:
        service.close()
