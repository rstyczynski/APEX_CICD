#!/usr/bin/env python3
"""Read-only UAT source review against the exact published patch archive."""
import difflib
import importlib.util
import json
import re
import sys
import tempfile
from pathlib import Path
from apex_sql import ROOT, run

spec = importlib.util.spec_from_file_location('release_artifact', ROOT/'scripts/cicd-artifact.py')
artifact = importlib.util.module_from_spec(spec)
spec.loader.exec_module(artifact)
TARGET = 'user_acceptance_test'
APP = 810005


def receipt():
    output = run('set serveroutput on\nbegin E1_CTRL.e1_release.show_status; end;\n/', connection=TARGET)
    if not re.search(r'^TARGET=E1_UAT APP=810005 EPOCH=\d+ PHASE=ready\r?$', output, re.M):
        raise ValueError('Review requires the retained ready UAT release; inspect an active deployment first')
    status = {}
    for name in ('ARTIFACT', 'SOURCE', 'CONFIG', 'FINGERPRINT'):
        match = re.search(r'^'+name+r'=(.*)$', output, re.M)
        if not match:
            raise ValueError('Incomplete UAT receipt: '+name)
        status[name] = match.group(1).strip()
    return status


def check_receipt(status, digest, info):
    if (status['ARTIFACT'] != digest or status['SOURCE'] != info['source_commit'] or
            status['CONFIG'] != info['configuration_sha256'] or not re.fullmatch(r'SH256:[A-Za-z0-9+/]{43}=', status['FINGERPRINT'])):
        raise ValueError('Selected archive does not match the successful UAT receipt; refusing an unrelated comparison')


def fingerprint():
    output = run(f'@"{ROOT}/deploy/operator/fingerprint.sql" {APP}\n', connection=TARGET)
    found = re.findall(r'^SH256:[^\r\n]+', output, re.M)
    if len(found) != 1:
        raise ValueError('Single live APEX fingerprint required')
    return found[0]


def comparison_text(text):
    # Target import offset is an expected environment mapping, not a page edit.
    # Keep the original bytes in raw.diff; do not normalize application behavior.
    text = re.sub(r'(?m)^,p_default_id_offset=>\d+\r?\n', '', text)
    return re.sub(r'(?m)^--   Manifest\r?\n(?:--[^\n]*\n)*?--   Manifest End\r?\n', '', text)


def differences(published, live, normalize=False):
    chunks = []
    changed = []
    for name in sorted(set(published) | set(live)):
        before, after = published.get(name, ''), live.get(name, '')
        if normalize:
            before, after = comparison_text(before), comparison_text(after)
        if before == after:
            continue
        changed.append(name)
        chunks.append(''.join(difflib.unified_diff(
            before.splitlines(True), after.splitlines(True),
            fromfile='published/'+name, tofile='live/'+name)))
    return changed, ''.join(chunks)


def values(text, parameter):
    return [v.replace("''", "'") for v in re.findall(
        r"(?m)^\s*,?"+re.escape(parameter)+r"=>'((?:[^']|'')*)'", text)]


def main():
    if len(sys.argv) != 1:
        raise ValueError('Usage: python3 scripts/cicd-drift-diff.py (read-only; no restoration)')
    archive = Path((ROOT/'.local-apex/releases/patch-selected.txt').read_text().strip())
    if not archive.is_absolute():
        archive = ROOT/archive
    digest, info, files = artifact.inspect(archive)
    status = receipt()
    check_receipt(status, digest, info)
    before = fingerprint()
    work = Path(tempfile.mkdtemp(prefix='drift-review.', dir=ROOT/'.local-apex/releases'))
    work.chmod(0o700)
    published = {}
    for name, data in files.items():
        prefix = 'apex/f810001/'
        if name.startswith(prefix):
            relative = name[len(prefix):]
            destination = work/'published'/relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            published[relative] = data.decode('utf-8')
    live_dir = work/'live'
    live_dir.mkdir()
    (work/'capture.log').write_text(run(
        f'apex export -applicationid {APP} -split -skipExportDate -expOriginalIds '
        f'-expSupportingObjects N -dir "{live_dir}"\n', connection=TARGET))
    tree = live_dir/f'f{APP}'
    if not (tree/'application/pages/page_00001.sql').is_file():
        raise ValueError('Native split export is incomplete; no comparison result claimed')
    live = {p.relative_to(tree).as_posix(): p.read_bytes().decode('utf-8') for p in tree.rglob('*') if p.is_file()}
    if fingerprint() != before or receipt() != status:
        raise ValueError('UAT changed during capture; stop other editing/deployment and repeat the review')
    changed, review = differences(published, live, normalize=True)
    _, raw = differences(published, live)
    (work/'review.diff').write_text(review)
    (work/'raw.diff').write_text(raw)
    (work/'review.json').write_text(json.dumps({
        'target': TARGET, 'application': APP, 'archive_sha256': digest,
        'source_commit': info['source_commit'], 'receipt': status,
        'live_fingerprint': before, 'changed_files': changed,
        'comparison_rule': 'remove import-offset lines and generated Manifest comment blocks; raw.diff retains every exported difference'
    }, indent=2)+'\n')
    print(f'PUBLISHED SOURCE: {info["source_commit"]}\nARCHIVE SHA256: {digest}')
    print('PAGE CHANGES (- published value, + live value):')
    page_names = [name for name in changed if name.startswith('application/pages/')]
    for name in page_names:
        print(f'\n{name}')
        for parameter, label in [('p_step_title', 'Page title'), ('p_plug_name', 'Region name(s)')]:
            old, new = values(published.get(name, ''), parameter), values(live.get(name, ''), parameter)
            if old != new:
                print(f'  {label}: {old!r} -> {new!r}')
        _, diff = differences({name: published[name]} if name in published else {},
                              {name: live[name]} if name in live else {}, normalize=True)
        print(diff)
    if not page_names:
        print('No page-export differences after excluding target import-offset lines and generated Manifest comments.')
    other = [name for name in changed if name not in page_names]
    if other:
        print('OTHER EXPORT DIFFERENCES (review these too): '+', '.join(other))
        print('Target alias, runtime availability and generated metadata can differ from packaged source; they are retained in the report.')
    print(f'REVIEW: {work.relative_to(ROOT)}/review.diff')
    print(f'COMPLETE RAW DIFF: {work.relative_to(ROOT)}/raw.diff')
    print('READ-ONLY REVIEW COMPLETE: live edit and Git source are unchanged. No restoration performed.')
    print('Decision: restore the published page/region values in Page Designer, or retain the edit for reviewed Git reconciliation. Deployment stays blocked while drift remains.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, RuntimeError, KeyError) as exc:
        sys.exit('ERROR: '+str(exc))
