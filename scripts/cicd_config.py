"""Validate the bounded lab mapping before it can enter SQL or connection text."""
import json
import re
from pathlib import Path

EXPECTED = {
    'lab-dev': ('E1_DEV_A', 810001),
    'lab-dev-b': ('E1_DEV_B', 810002),
    'lab-dev-c': ('E1_DEV_C', 810003),
    'integration_test': ('E1_INTEGRATION', 810004),
    'user_acceptance_test': ('E1_UAT', 810005),
}


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Z][A-Z0-9_]{0,29}', value):
        raise ValueError('Unsafe or unsupported Oracle identifier in area configuration')
    return value


def validate(config):
    if not isinstance(config, dict) or set(config) != {'service', 'control_schema', 'areas'}:
        raise ValueError('Unexpected area configuration structure')
    service = config['service']
    if not isinstance(service, str) or not re.fullmatch(r'[A-Za-z0-9.-]+:[0-9]{1,5}/[A-Za-z][A-Za-z0-9_]{0,29}', service):
        raise ValueError('Unsafe Oracle service descriptor')
    if not 1 <= int(service.split(':')[1].split('/')[0]) <= 65535:
        raise ValueError('Invalid Oracle service port')
    if identifier(config['control_schema']) != 'E1_CTRL':
        raise ValueError('Unsupported control schema for this bounded lab')
    areas = config['areas']
    if not isinstance(areas, dict) or set(areas) != set(EXPECTED):
        raise ValueError('Expected the five declared lab targets')
    schemas, workspaces, applications = set(), set(), set()
    for name, area in areas.items():
        if not isinstance(area, dict) or set(area) != {'schema', 'workspace', 'application_id'}:
            raise ValueError('Unexpected area fields')
        schema, workspace = identifier(area['schema']), identifier(area['workspace'])
        app = area['application_id']
        if type(app) is not int or not 1 <= app <= 999999999:
            raise ValueError('Application ID must be a positive bounded integer')
        if schema in schemas or workspace in workspaces or app in applications or schema == config['control_schema']:
            raise ValueError('Duplicate or control-colliding area mapping')
        schemas.add(schema); workspaces.add(workspace); applications.add(app)
        expected_schema, expected_app = EXPECTED[name]
        if (schema, workspace, app) != (expected_schema, expected_schema, expected_app):
            raise ValueError('Mapping differs from the bounded controller contract: ' + name)
    return config


def load(path):
    return validate(json.loads(Path(path).read_text()))
