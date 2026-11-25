"""E.9 loopback capability service; trusted host, untrusted API callers/source.

Not a multi-tenant sandbox or GitHub adapter. No external network is used.
"""
import copy
import hashlib
import http.server
import json
import secrets
import subprocess
import threading
from pathlib import Path
from review_control import digest, receipt, current


def git(repo, *args, input=None):
    return subprocess.check_output(['git', '-C', str(repo), *args], input=input,
                                   text=True, stderr=subprocess.STDOUT).strip()


class Service:
    def __init__(self, home):
        self.home = Path(home)
        self.repo = self.home / 'source.git'
        self.store = self.home / 'reports'
        self.store.mkdir()
        self.tokens = {role: secrets.token_urlsafe(32) for role in
                       ('developer', 'testing', 'review', 'integrator', 'approver', 'administrator')}
        self.lock = threading.RLock()
        self.events = []
        self.reports = {}
        self.accepted = None
        self.checks = {}
        self.conversations = 0
        self.approval = None
        self.withdrawn = False
        self.generation = 0
        self.policy = digest({'version': 1, 'independent_approval': True})
        self.pause_publication = None  # deterministic test synchronization, never an HTTP option
        self.before_merge = None
        git(self.home, 'init', '--bare', str(self.repo))
        git(self.repo, 'config', 'user.name', 'Trusted E9 integrator')
        git(self.repo, 'config', 'user.email', 'e9@example.invalid')
        hook = self.repo / 'hooks/pre-receive'
        hook.write_text('#!/bin/sh\necho "DENIED: protected refs require authenticated service integration" >&2\nexit 1\n')
        hook.chmod(0o700)
        self.server = None

    def role(self, token):
        for role, expected in self.tokens.items():
            if secrets.compare_digest(token, expected):
                return role
        raise PermissionError('invalid credential')

    def candidate(self):
        return {'base': git(self.repo, 'rev-parse', 'refs/heads/main'),
                'head': git(self.repo, 'rev-parse', 'refs/heads/feature'), 'policy': self.policy}

    def invalidate(self, kind):
        self.generation += 1
        self.checks.pop('Review', None)
        self.approval = None
        self.events.append({'event': kind, 'generation': self.generation})

    def live_report(self):
        return self.reports.get('live') if not self.withdrawn else None

    def evidence(self):
        c = self.candidate()
        return bool(self.accepted and current(self.accepted, c, self.live_report()))

    def handle(self, token, action, data):
        role = self.role(token)
        allowed = {'submit': {'developer'}, 'publish': {'review'}, 'testing': {'testing'},
                   'edit': {'developer'}, 'withdraw': {'developer'}, 'delete': {'developer'},
                   'head': {'developer'}, 'base': {'administrator'}, 'policy': {'administrator'},
                   'conversation': {'developer'}, 'approve': {'approver'},
                   'merge': {'integrator'}, 'bypass': {'administrator'},
                   'state': set(self.tokens), 'report': set(self.tokens)}
        if action not in allowed or role not in allowed[action]:
            raise PermissionError('role cannot perform action')
        if action == 'publish':
            with self.lock:
                generation = self.generation
                report = copy.deepcopy(self.live_report())
                if not report:
                    raise ValueError('missing report')
                accepted = receipt(report, 'developer')
                if not current(accepted, self.candidate(), report):
                    raise ValueError('report is stale')
            if self.pause_publication:
                self.pause_publication()
            with self.lock:
                if self.generation != generation or not current(accepted, self.candidate(), self.live_report()):
                    raise ValueError('candidate changed during publication')
                self.accepted = accepted
                self.checks['Review'] = {'publisher': role, 'candidate': self.candidate(), 'state': 'success',
                                         'report': accepted['report']}
                self.events.append({'event': 'published', 'receipt': accepted})
                return accepted
        with self.lock:
            if action == 'state':
                return {'candidate': self.candidate(), 'checks': self.checks,
                        'generation': self.generation, 'events': self.events}
            if action == 'report':
                key = data['hash']
                if len(key) != 64 or any(c not in '0123456789abcdef' for c in key):
                    raise ValueError('invalid hash')
                report = json.loads((self.store / (key + '.json')).read_text())
                if digest(report) != key:
                    raise ValueError('retained report integrity failure')
                return report
            if action in ('submit', 'edit'):
                report = data['report']
                # validate before changing any current state
                accepted = receipt(report, 'developer')
                if not current(accepted, self.candidate(), report):
                    raise ValueError('submission revision mismatch')
                key = digest(report)
                path = self.store / (key + '.json')
                if not path.exists():
                    with path.open('x') as stream:
                        json.dump(report, stream, sort_keys=True)
                    path.chmod(0o400)
                elif digest(json.loads(path.read_text())) != key:
                    raise ValueError('stored report corrupted')
                self.reports['live'] = copy.deepcopy(report)
                self.withdrawn = False
                self.invalidate(action)
                return {'hash': key}
            if action in ('withdraw', 'delete'):
                self.withdrawn = True
                if action == 'delete':
                    self.reports.pop('live', None)
                self.invalidate(action)
                return {'retained': True}
            if action in ('head', 'base'):
                sha = data['sha']
                if len(sha) != 40 or any(c not in '0123456789abcdef' for c in sha):
                    raise ValueError('invalid commit')
                git(self.repo, 'cat-file', '-e', sha + '^{commit}')
                ref = 'feature' if action == 'head' else 'main'
                git(self.repo, 'update-ref', 'refs/heads/' + ref, sha)
                self.invalidate(action)
                return self.candidate()
            if action == 'policy':
                self.policy = digest(data)
                self.invalidate(action)
                return self.candidate()
            if action == 'testing':
                if data['candidate'] != self.candidate():
                    raise ValueError('stale Testing candidate')
                self.checks['Testing'] = {'publisher': role, 'candidate': data['candidate'], 'state': data['state']}
                return self.checks['Testing']
            if action == 'conversation':
                if type(data['count']) is not int or data['count'] < 0:
                    raise ValueError('invalid conversation count')
                self.conversations = data['count']
                return {'count': self.conversations}
            if action == 'approve':
                self.approval = self.candidate()
                return {'approver': role, 'candidate': self.approval}
            if action in ('merge', 'bypass'):
                if self.before_merge:
                    self.before_merge()
                c = self.candidate()
                bypass = action == 'bypass'
                if bypass:
                    if not data.get('reason', '').strip():
                        raise ValueError('bypass requires reason')
                else:
                    if not self.evidence() or self.conversations or self.approval != c:
                        raise ValueError('review, conversations or independent approval blocks merge')
                    for name, publisher in [('Testing', 'testing'), ('Review', 'review')]:
                        check = self.checks.get(name, {})
                        if check.get('publisher') != publisher or check.get('state') != 'success' or check.get('candidate') != c:
                            raise ValueError('missing, stale, nonpassing or wrong publisher ' + name)
                    if self.checks['Review'].get('report') != self.accepted['report']:
                        raise ValueError('report revision mismatch')
                tree = git(self.repo, 'merge-tree', '--write-tree', c['base'], c['head']).splitlines()[0]
                commit = git(self.repo, 'commit-tree', tree, '-p', c['base'], '-p', c['head'],
                             input='E9 controlled integration\n')
                git(self.repo, 'update-ref', 'refs/heads/main', commit, c['base'])
                event = {'event': action, 'actor': role, 'candidate': c, 'commit': commit,
                         'reason': data.get('reason') if bypass else None}
                self.events.append(event)
                self.invalidate('integrated')
                return event
        raise ValueError('unsupported operation')

    def start(self):
        service = self
        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass  # never log authorization headers
            def do_POST(self):
                try:
                    length = int(self.headers.get('Content-Length', '0'))
                    if not 0 < length <= 100000:
                        raise ValueError('invalid body size')
                    data = json.loads(self.rfile.read(length))
                    token = self.headers.get('Authorization', '').removeprefix('Bearer ')
                    value = service.handle(token, self.path.lstrip('/'), data)
                    status = 200
                except PermissionError as exc:
                    status, value = 403, {'error': str(exc)}
                except (ValueError, KeyError, TypeError, FileNotFoundError, subprocess.CalledProcessError) as exc:
                    status, value = 409, {'error': str(exc)}
                payload = json.dumps(value).encode()
                self.send_response(status)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        thread.start()
        return 'http://127.0.0.1:' + str(self.server.server_port)

    def close(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
