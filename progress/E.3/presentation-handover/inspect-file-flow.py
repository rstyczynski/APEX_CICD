"""Inspect retained native source and ZIP; never export, stage or deploy."""
from pathlib import Path
import hashlib
import json
import subprocess
import tempfile
import zipfile

root = Path.cwd()
out = root / 'progress/E.3/tests/file-flow'
out.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix='e3-file-flow-source-') as tmp:
    repo = Path(tmp) / 'application'
    subprocess.run(['git', 'clone', str(root / 'examples/git-pipeline/baseline.bundle'), str(repo)], check=True, capture_output=True)
    def git(*args):
        return subprocess.check_output(['git', '-C', str(repo), *args])
    (out / 'heading-files.txt').write_bytes(git('show', '--format=', '--name-status', '568a06d'))
    (out / 'release-renames.txt').write_bytes(git('diff', '--name-status', '--find-renames', 'ed732c2^', 'ed732c2'))
    (out / 'heading-source.diff').write_bytes(git('diff', '568a06d^', '568a06d', '--', 'src/database/e1_dev_c/apex_apps/f810003/readable/application/pages/p00001.yaml'))
    for side, ref in [('before', 'ed732c2^'), ('after', 'ed732c2')]:
        (out / f'main-changelog-{side}.xml').write_bytes(git('show', ref + ':dist/releases/main.changelog.xml'))
        cfg = json.loads(git('show', ref + ':.dbtools/project.config.json'))
        (out / f'project-version-{side}.json').write_text(json.dumps({key: cfg[key] for key in ['project', 'sqlcl', 'lastReleaseVersion']}, indent=2) + '\n')
    archive = root / 'progress/E.3/tests/release-correction/e3-1.0.5.zip'
    with zipfile.ZipFile(archive) as z:
        members = [name for name in z.namelist() if not name.endswith('/')]
        for name in members:
            assert z.read(name) == git('show', 'ed732c2:dist/' + name), name
    (out / 'archive-files.txt').write_text('\n'.join(members) + '\n')
    (out / 'provenance.json').write_text(json.dumps({
        'heading_commit': git('rev-parse', '568a06d').decode().strip(),
        'native_freeze_commit': git('rev-parse', 'ed732c2').decode().strip(),
        'artifact_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
        'archive_files': len(members),
        'all_archive_files_match_committed_dist': True,
        'observation': 'Inspected retained source/history/archive; no fresh export, staging, release or deployment claimed',
    }, indent=2) + '\n')
print(f'PASS {len(members)} ZIP files exactly match the committed native distribution')
