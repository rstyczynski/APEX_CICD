import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('drift_diff', ROOT/'scripts/cicd-drift-diff.py')
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


class DriftReviewTests(unittest.TestCase):
    def test_only_environment_offset_and_manifest_comments_are_omitted(self):
        before = "--   Manifest\n--     FLOW: 1\n--   Manifest End\n,p_default_id_offset=>12\n,p_step_title=>'Old'\n"
        after = "--   Manifest\n--     FLOW: 2\n--   Manifest End\n,p_default_id_offset=>34\n,p_step_title=>'New'\n"
        _, diff = review.differences({'page.sql': before}, {'page.sql': after}, normalize=True)
        self.assertIn("-,p_step_title=>'Old'", diff)
        self.assertIn("New", diff)
        self.assertNotIn('offset', diff)
        self.assertNotIn('FLOW:', diff)
        _, raw = review.differences({'page.sql': before}, {'page.sql': after})
        self.assertIn('offset', raw)
        self.assertIn('FLOW:', raw)

    def test_additions_and_deletions_are_reported(self):
        names, diff = review.differences({'removed.sql': 'old\n'}, {'added.sql': 'new\n'})
        self.assertEqual(names, ['added.sql', 'removed.sql'])
        self.assertIn('+new', diff)
        self.assertIn('-old', diff)

    def test_region_name_and_escaped_quotes_are_preserved(self):
        self.assertEqual(review.values(",p_plug_name=>'Developer''s region'\n", 'p_plug_name'), ["Developer's region"])

    def test_matching_receipt_is_required(self):
        info = {'source_commit': 'c', 'configuration_sha256': 'config'}
        status = {'ARTIFACT': 'hash', 'SOURCE': 'c', 'CONFIG': 'config', 'FINGERPRINT': 'SH256:'+'A'*43+'='}
        review.check_receipt(status, 'hash', info)
        with self.assertRaises(ValueError):
            review.check_receipt(status, 'unrelated-hash', info)
        with self.assertRaises(ValueError):
            review.check_receipt(dict(status, SOURCE='other'), 'hash', info)

    def test_no_page_change_is_not_invented(self):
        names, diff = review.differences({'page.sql': 'same\n'}, {'page.sql': 'same\n'}, normalize=True)
        self.assertEqual(names, [])
        self.assertEqual(diff, '')


if __name__ == '__main__':
    unittest.main()
