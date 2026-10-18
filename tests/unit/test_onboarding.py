#!/usr/bin/env python3
"""Responsibility boundaries: infrastructure, one-area provisioning and developer profile."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))

def load(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

platform = load('onboarding_platform', 'scripts/cicd-platform.py')
developer = load('developer_configure', 'scripts/cicd-developer-configure.py')

class Boundaries(unittest.TestCase):
    def test_infrastructure_has_no_project_provisioning(self):
        script = (ROOT / 'scripts/cicd-walkthrough-apex-init.sh').read_text()
        for forbidden in ['cicd-platform.py', 'cicd-control-init.sh', 'cicd-area-provision.sh', 'deploy/control.sql', 'deploy/release_control.sql']:
            self.assertNotIn(forbidden, script)
        self.assertNotIn('deploy/operator/', script)
        self.assertNotIn('E1_', script)

    def test_control_creates_only_control_identity(self):
        with patch.object(platform, 'owned_inventory'), patch.object(platform, 'credentials', return_value={}), patch.object(platform, 'create_schema') as create, patch.object(platform, 'run'), contextlib.redirect_stdout(io.StringIO()):
            platform.control_identity()
            self.assertEqual(create.call_args.args[0], 'E1_CTRL')
            self.assertEqual(create.call_count, 1)
        for file in ['deploy/control.sql', 'deploy/release_control.sql']:
            self.assertNotIn('grant execute on ', (ROOT / file).read_text())

    def test_provision_touches_only_named_area(self):
        for name, area in platform.CONFIG['areas'].items():
            with self.subTest(name=name), patch.object(platform, 'owned_inventory'), patch.object(platform, 'credentials', return_value={area['schema']: 'Assigned_1', 'DEV_A':'Assigned_1', 'DEV_B':'Assigned_1', 'DEV_C':'Assigned_1','LAB_USER':'Assigned_1','VERIFIER':'Assigned_1'}), patch.object(platform, 'create_schema') as create, patch.object(platform, 'run') as sql, contextlib.redirect_stdout(io.StringIO()):
                platform.provision(name)
                self.assertEqual(create.call_count, 1)
                self.assertEqual(create.call_args.args[0], area['schema'])
                statements = '\n'.join(c.args[0] for c in sql.call_args_list)
                for other in platform.CONFIG['areas'].values():
                    if other != area:
                        self.assertNotIn(other['schema'], statements)

    def test_reset_reprovisions_only_qualification(self):
        with tempfile.TemporaryDirectory() as folder:
            Path(folder, 'e1-owned.json').write_text(json.dumps(platform.CONFIG))
            with patch.object(platform, 'LOCAL', Path(folder)), patch.object(platform, 'run'), patch.object(platform, 'provision') as provision, contextlib.redirect_stdout(io.StringIO()):
                platform.reset_qualification()
                provision.assert_called_once_with('lab-qualify')

    def test_developer_uses_only_assigned_password_and_private_home(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'config').mkdir()
            (root / 'config/areas.json').write_text(json.dumps(platform.CONFIG))
            def sql(command, **kwargs):
                body = Path(command[-1][1:]).read_text()
                self.assertIn('E1_DEV_A/"Assigned_1"', body)
                self.assertNotIn('SYS/', body)
                self.assertNotIn('create user', body.lower())
                self.assertIn(str(root / '.local-apex/developers/A/sqlcl-home'), command)
                return types.SimpleNamespace(returncode=0, stdout='DEVELOPER_PROFILE_COMPLETE\n', stderr='')
            with patch.object(developer, 'ROOT', root), patch.object(sys, 'argv', ['configure','A','--password-stdin']), patch.object(sys, 'stdin', io.StringIO('Assigned_1\n')), patch.object(developer.subprocess, 'run', side_effect=sql), contextlib.redirect_stdout(io.StringIO()):
                developer.main()
            self.assertTrue((root / '.local-apex/developers/A/environment.sh').exists())
            self.assertFalse((root / '.local-apex/developers/B').exists())
            self.assertFalse(list((root / '.local-apex/developers/A').glob('*.sql')))

if __name__ == '__main__':
    unittest.main()
