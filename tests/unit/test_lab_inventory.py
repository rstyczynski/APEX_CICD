#!/usr/bin/env python3
"""Destructive cleanup must reject shared or unexpected resource ownership."""
import contextlib
import copy
import importlib.util
import io
from pathlib import Path
import unittest

path = Path(__file__).resolve().parents[2] / 'scripts/cicd-lab-inventory.py'
spec = importlib.util.spec_from_file_location('lab_inventory', path)
inventory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inventory)


class OwnershipBoundary(unittest.TestCase):
    def setUp(self):
        self.rows = [{'Id': 'db', 'Names': ['apex-db']}]
        self.details = {'db': {
            'ImageName': 'docker.io/gvenzl/oracle-free@sha256:reviewed',
            'Mounts': [{'Name': 'apex-data'}, {'Name': 'apex-images'}],
            'NetworkSettings': {'Networks': {'apex-net': {}}}}}

    def check(self):
        with contextlib.redirect_stdout(io.StringIO()):
            inventory.check(self.rows, self.details)

    def test_owned_and_unrelated_resources_allowed(self):
        self.rows.append({'Id': 'other', 'Names': ['unrelated']})
        self.details['other'] = {'Mounts': [{'Name': 'other-data'}]}
        self.check()

    def test_shared_lab_resources_refused_before_mutation(self):
        for resource in [
            {'Mounts': [{'Name': 'apex-data'}]},
            {'NetworkSettings': {'Networks': {'apex-net': {}}}},
            {'Config': {'Secrets': [{'Name': 'apex-db-password'}]}}
        ]:
            with self.subTest(resource=resource):
                self.rows = [{'Id': 'other', 'Names': ['unrelated']}]
                self.details = {'other': resource}
                with self.assertRaisesRegex(SystemExit, 'unrelated container shares'):
                    self.check()

    def test_unexpected_owned_mount_or_image_refused(self):
        original = copy.deepcopy(self.details)
        self.details['db']['Mounts'].append({'Name': 'unknown-data'})
        with self.assertRaisesRegex(SystemExit, 'unexpected mount'):
            self.check()
        self.details = original
        self.details['db']['ImageName'] = 'unrelated/image'
        with self.assertRaisesRegex(SystemExit, 'unexpected database image'):
            self.check()

    def test_empty_installation_allowed(self):
        inventory.check([], {})


if __name__ == '__main__':
    unittest.main()
