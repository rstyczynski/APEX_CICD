import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'scripts'))
from cicd_config import validate
import apex_sql


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


inputs = module('release_inputs', ROOT/'scripts/cicd-release-inputs.py')
artifact = module('review_artifact', ROOT/'scripts/cicd-artifact.py')


class ReviewFixTests(unittest.TestCase):
    def test_configuration_rejects_injection_invalid_ids_and_unknown_mappings(self):
        original = json.loads((ROOT/'config/areas.json').read_text())
        validate(original)
        variants = []
        for key, value in [('schema', "E1_X'; execute immediate 'drop user X'"),
                           ('workspace', 'BAD\nWORKSPACE'), ('application_id', '810004; drop user X'),
                           ('application_id', True), ('application_id', -1), ('schema', 'OTHER_VALID_NAME')]:
            c = copy.deepcopy(original); c['areas']['integration_test'][key] = value; variants.append(c)
        for service in ['localhost:1521/PDB\nexit', 'localhost:0/PDB', 'host:99999/PDB', 'host:1521/PDB;']:
            c = copy.deepcopy(original); c['service'] = service; variants.append(c)
        for c in variants:
            with self.subTest(c=c), self.assertRaises(ValueError): validate(c)

    def test_invalid_config_fails_before_secret_or_oracle_access(self):
        with patch.object(apex_sql, 'load', side_effect=ValueError('invalid mapping')), \
             patch.object(apex_sql, 'secrets') as secrets, patch.object(apex_sql.subprocess, 'run') as oracle:
            with self.assertRaises(ValueError): apex_sql.run('select 1 from dual', admin=True)
            secrets.assert_not_called(); oracle.assert_not_called()

    def test_platform_rejects_config_on_import_before_any_admin_call(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); (root/'config').mkdir(); (root/'config/areas.json').write_text('{"service":"bad"}')
            with patch.object(apex_sql, 'ROOT', root), patch.object(apex_sql, 'run') as oracle:
                with self.assertRaises(ValueError): module('unsafe_platform', ROOT/'scripts/cicd-platform.py')
                oracle.assert_not_called()

    def test_native_failure_policies_have_no_sqlcode_exit(self):
        for name in ['apex-configure.sh', 'apex-verify.sh', 'apex-db-install.sql', 'apex-db-verify.sql']:
            body = (ROOT/'scripts'/name).read_text().lower()
            self.assertNotIn('exit sql.sqlcode', body)
            self.assertIn('whenever sqlerror exit failure', body)
            self.assertIn('whenever oserror exit failure', body)

    def test_reconstruction_uses_clean_history_without_retained_archives(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)/'clone'
            subprocess.run(['git', 'clone', '--quiet', '--no-hardlinks', '--no-checkout', str(ROOT), str(root)], check=True)
            (root/'release').mkdir(); shutil.copytree(ROOT/'release/inputs', root/'release/inputs')
            self.assertFalse((root/'.local-apex').exists())
            inputs.prepare(root)
            for name in ['initial', 'patch']:
                recipe = json.loads((root/'release/inputs'/f'{name}.json').read_text())
                archive = root/(root/f'.local-apex/releases/{name}-selected.txt').read_text().strip()
                self.assertEqual(inputs.sha(archive.read_bytes()), recipe['archive_sha256'])
            inputs.prepare(root)  # exact existing inputs may be reused

    def test_tampered_evidence_and_missing_source_reject(self):
        recipe = json.loads((ROOT/'release/inputs/initial.json').read_text())
        recipe['evidence']['candidate.log'] += 'tampered'
        with self.assertRaisesRegex(ValueError, 'digest mismatch'): inputs.payload(recipe)
        recipe = json.loads((ROOT/'release/inputs/initial.json').read_text())
        info = json.loads(recipe['artifact_json']); info['source_commit'] = '0'*40
        recipe['artifact_json'] = json.dumps(info)
        with self.assertRaises(subprocess.CalledProcessError): inputs.payload(recipe)

    def test_conflicting_archive_never_overwritten_or_selected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); (root/'release/inputs').mkdir(parents=True)
            for name in ['initial', 'patch']:
                shutil.copyfile(ROOT/f'release/inputs/{name}.json', root/f'release/inputs/{name}.json')
            # Source lookup remains against real history; simulate reconstructed bytes only.
            dest = root/'.local-apex/releases'; dest.mkdir(parents=True)
            (dest/'lab-1.0.0-aaaaaaaaaaaa.tar').write_bytes(b'foreign')
            with patch.object(inputs, 'payload', return_value=('a'*40, b'expected')):
                with self.assertRaisesRegex(ValueError, 'Conflicting retained'): inputs.prepare(root)
            self.assertEqual((dest/'lab-1.0.0-aaaaaaaaaaaa.tar').read_bytes(), b'foreign')
            self.assertFalse((dest/'initial-selected.txt').exists())

    def test_dirty_test_harness_rejects_candidate_and_packaging_before_sql(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); (root/'scripts').mkdir(); (root/'tests/manifests').mkdir(parents=True)
            shutil.copyfile(ROOT/'scripts/cicd-candidate-check.sh', root/'scripts/cicd-candidate-check.sh')
            for name in ['tests/run.sh', 'tests/manifests/test.manifest', 'tests/test.py', 'tests/test.sh']:
                (root/name).write_text('original\n')
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            subprocess.run(['git', '-C', str(root), 'add', '.'], check=True)
            subprocess.run(['git', '-C', str(root), '-c', 'user.name=Fixture', '-c', 'user.email=fixture@localhost', 'commit', '-qm', 'fixture'], check=True)
            for name in ['tests/run.sh', 'tests/manifests/test.manifest', 'tests/test.py', 'tests/test.sh']:
                with self.subTest(name=name):
                    (root/name).write_text('unreviewed\n')
                    result = subprocess.run(['bash', str(root/'scripts/cicd-candidate-check.sh')], capture_output=True, text=True)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn('commit the reviewed candidate', result.stderr)
                    with patch.object(artifact, 'ROOT', root):
                        with self.assertRaisesRegex(ValueError, 'Dirty release source'): artifact.build()
                    (root/name).write_text('original\n')


if __name__ == '__main__': unittest.main()
