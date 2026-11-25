"""Bounded local laboratory controller. Never expose this object to candidates."""
import json
import secrets
import subprocess
import threading

class Registry:
    def __init__(self):
        self.lock = threading.RLock()
        self.events, self.current, self.results = {}, {}, {}

    def admit(self, stream, revision, event):
        with self.lock:
            key = (stream, revision, event)
            if key in self.events:
                return self.events[key], None
            previous = self.current.get(stream)
            run = secrets.token_hex(12)
            self.events[key] = run
            self.current[stream] = run
            return run, previous

    def complete(self, stream, run, result):
        with self.lock:
            if self.current.get(stream) != run or run in self.results:
                raise ValueError('stale or duplicate completion')
            self.results[run] = result


def bounded(action, attempts=3):
    """Only transport timeouts are transient; assertion/command errors propagate."""
    if not 1 <= attempts <= 3:
        raise ValueError('retry bound')
    for attempt in range(attempts):
        try:
            return action()
        except (TimeoutError, subprocess.TimeoutExpired):
            if attempt + 1 == attempts:
                raise


def review(text):
    return json.dumps({'review': text})


class Containers:
    def __init__(self, image, session=None):
        self.image = image
        self.session = session or secrets.token_hex(12)
        self.prefix = ['podman', '--connection', 'apex-cicd']

    def cli(self, *args, timeout=30, check=True):
        return subprocess.run(self.prefix + list(args), text=True,
                              capture_output=True, timeout=timeout, check=check)

    def start(self, script, credential='synthetic-candidate'):
        name = 'e10-' + secrets.token_hex(10)
        self.cli('run', '-d', '--log-driver=k8s-file', '--name', name, '--label', 'e10.session=' + self.session,
                 '--network=none', '--read-only', '--cap-drop=ALL',
                 '--security-opt=no-new-privileges', '--user=65534:65534',
                 '--pids-limit=32', '--memory=32m', '--cpus=0.25',
                 '--tmpfs=/work:rw,noexec,nosuid,size=1m,mode=1777',
                 '--env', 'CANDIDATE_CREDENTIAL=' + credential,
                 self.image, '/bin/sh', '-c', script)
        return name

    def owned(self, name):
        info = json.loads(self.cli('inspect', name).stdout)[0]
        if info['Config']['Labels'].get('e10.session') != self.session:
            raise PermissionError('foreign resource')

    def cleanup(self, name):
        self.owned(name)
        self.cli('rm', '-f', name)
        if self.cli('container', 'exists', name, check=False).returncode != 1:
            raise RuntimeError('cleanup not verified')

    def reap(self):
        names = self.cli('ps', '-a', '--filter', 'label=e10.session=' + self.session,
                         '--format', '{{.Names}}').stdout.split()
        for name in names:
            self.cleanup(name)
        return names

    def wait(self, name, timeout=3):
        try:
            return int(self.cli('wait', name, timeout=timeout).stdout.strip())
        finally:
            self.cleanup(name)
