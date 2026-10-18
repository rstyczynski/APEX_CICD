#!/usr/bin/env python3
"""Environment boundary: legacy aliases cannot select a different target."""
from pathlib import Path
import json,sys,unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from cicd_environments import canonical
import apex_sql

class EnvironmentNames(unittest.TestCase):
    def test_aliases_resolve_to_declared_physical_identity(self):
        config=json.loads((apex_sql.ROOT/'config/areas.json').read_text())
        for alias,new,schema,app in [('lab-qualify','integration_test','E1_INTEGRATION',810004),('lab-test','user_acceptance_test','E1_UAT',810005)]:
            self.assertEqual(canonical(alias),new)
            self.assertEqual(canonical(new),new)
            self.assertEqual(config['areas'][new]['schema'],schema)
            self.assertEqual(config['areas'][new]['workspace'],schema)
            self.assertEqual(config['areas'][new]['application_id'],app)
    def test_unknown_target_stops_before_credentials_or_sql(self):
        with patch.object(apex_sql,'secrets') as credentials,patch.object(apex_sql.subprocess,'run') as sql:
            with self.assertRaises(ValueError):apex_sql.run('select user from dual;',connection='not_a_target')
            credentials.assert_not_called();sql.assert_not_called()

if __name__=='__main__':unittest.main()
