#!/usr/bin/env python3
"""E.2 prototype: visible SQLcl promotion steps, with separate browser gates.

This is local orchestration, not native PROJECT qualification enforcement or a
production release controller. It never rebuilds an archive or provisions a lab.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
from zipfile import ZipFile

from apex_sql import ROOT, run

REPO = ROOT / '.local-apex/e2/project-walkthrough/component-repo'
EVIDENCE = ROOT / 'progress/E.2/tests/project-integration-mapped-validation.json'
STATE = ROOT / '.local-apex/e2/project-walkthrough/uat-promotion'
BUSINESS = {
    'history': 'GREETING_ID', 'hello_entries': 'ENTRY_ID',
    'world_entries': 'ENTRY_ID', 'hello_config': 'CONFIG_ID',
    'world_config': 'CONFIG_ID',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def execute(connection, body, display=True):
    print(f'\nSQLcl [{connection}]\nconnect -name {connection}\n{body}', flush=True)
    output = run(body, connection=connection)
    if display:
        print(output, flush=True)
    require(not any(term in output for term in
                    ('Option not recognized', 'Syntax Error', 'Unexpected token')),
            'SQLcl rejected the displayed command')
    return output


def query(connection, expression):
    # SQLcl JSON has no trailing newline. A prompt separates its end from the
    # existing SQLcl boundary's server-side completion marker.
    body = (f'set long 1000000 longchunksize 1000000\nset sqlformat json\n'
            f'select {expression} as "payload" from dual;\n'
            'prompt E2_JSON_END\nset sqlformat ansiconsole')
    output = execute(connection, body, display=False)
    result, _ = json.JSONDecoder().raw_decode(output[output.index('{'):])
    payload = result['results'][0]['items'][0]['payload']
    return json.loads(payload) if isinstance(payload, str) else payload


def metadata(connection, app):
    return query(connection, f"""json_object(
      'schema' value user,
      'business_tables' value (select count(*) from user_tables where table_name in
        ('LAB_COMPONENTS','LAB_STATE','HELLO_ENTRIES','WORLD_ENTRIES',
         'HELLO_CONFIG','WORLD_CONFIG','GREETING_HISTORY')),
      'invalid_business' value (select count(*) from user_objects where
        status='INVALID' and object_type in ('PACKAGE','PACKAGE BODY','TRIGGER')),
      'application' value (select json_object('id' value application_id,
        'schema' value owner, 'status' value availability_status)
        from apex_applications where application_id={app}) format json)""")


def snapshot(connection):
    tables = {'history': ('greeting_history', 'greeting_id'),
              'hello_entries': ('hello_entries', 'entry_id'),
              'world_entries': ('world_entries', 'entry_id'),
              'hello_config': ('hello_config', 'config_id'),
              'world_config': ('world_config', 'config_id'),
              'components': ('lab_components', 'component')}
    parts = [f"'{name}' value (select coalesce(json_arrayagg(json_object(*) "
              f"order by {key} returning clob),to_clob('[]')) from {table}) format json"
             for name, (table, key) in tables.items()]
    return query(connection, 'json_object(' + ',\n'.join(parts) + ' returning clob)')


def initial_versions(data):
    actual = {r['COMPONENT']: (r['INSTALLED'], r['VERSION'])
              for r in data['components']}
    require(actual == {name: (1, '1.0.0') for name in
                       ('Foundation', 'Hello', 'World')}, 'Initial component mismatch')
    print('PASS initial component versions ' + json.dumps(actual), flush=True)


def record(name, value):
    STATE.mkdir(parents=True, exist_ok=True)
    path = STATE / name
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    path.chmod(0o600)
    return path


def candidate():
    evidence = json.loads(EVIDENCE.read_text())
    archive = ROOT / evidence['artifact']
    require(archive.resolve().parent == (REPO / 'artifact').resolve(),
            'Qualification archive is outside this application repository')
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    require(digest == evidence['sha256'], 'Archive differs from the D-tested bytes')
    require(evidence.get('mapped_deployment', '').startswith('passed'),
            'D mapped deployment evidence is missing')
    with ZipFile(archive) as z:
        require('-defaults-file &DEFAULTS_FILE' in z.read('install.sql').decode(),
                'Archive lacks the reviewed mapping hook')
        expected = ('apex.810003.workspace:E1_UAT\napex.810003.appId:810005\n'
                    'apex.810003.schema:E1_UAT\napex.810003.alias:E2-UAT\n')
        require(z.read('utils/properties/uat.properties').decode() == expected,
                'Packaged UAT mapping differs from the reviewed target')
        apex = z.read('releases/apex/f810003/f810003.sql').decode()
        require('E1_CTRL.e1_release.assert_runtime' not in apex and
                "p_flow_status=>'RESTRICTED_ACCESS'" in apex,
                'Candidate does not use the reviewed native runtime controls')
    print(f'ARCHIVE {archive.relative_to(ROOT)}\nSHA256 {digest}', flush=True)
    print('ASSESSMENT ONLY: native verify retains its documented APEX error.', flush=True)
    return archive, digest, evidence


def inspect():
    archive, digest, evidence = candidate()
    integration = metadata('integration_test', 810004)
    require(integration['schema'] == 'E1_INTEGRATION' and
            integration['application'] is not None and
            integration['application']['schema'] == 'E1_INTEGRATION' and
            integration['application']['status'] == 'Available',
            'D integration target is not the published mapped application')
    initial_versions(snapshot('integration_test'))
    print('PASS published integration 810004 / E1_INTEGRATION', flush=True)
    target = metadata('user_acceptance_test', 810005)
    require(target['schema'] == 'E1_UAT', 'Wrong effective UAT schema')
    print('TARGET ' + json.dumps(target), flush=True)
    return archive, digest, evidence, target


def mapped_target(target):
    require(target['business_tables'] == 7 and target['application'] is not None
            and target['application']['schema'] == 'E1_UAT'
            and target['invalid_business'] == 0,
            'UAT is not a complete mapped application; inspect partial state')


def saved_receipt(digest):
    path = STATE / 'deployment.json'
    require(path.exists(), 'No prototype deployment receipt; inspect existing UAT state')
    receipt = json.loads(path.read_text())
    require(receipt['sha256'] == digest and receipt['application_id'] == 810005,
            'UAT receipt does not match this artifact/target')
    return receipt


def assert_preserved(before, after):
    for table, key in BUSINESS.items():
        current = {r[key]: r for r in after[table]}
        for row in before[table]:
            live = current.get(row[key])
            require(live is not None and all(field in live and live[field] == value
                                            for field, value in row.items()),
                    f'Preservation mismatch: {table} {key}={row[key]}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('inspect', 'deploy', 'publish',
                                          'baseline', 'check-baseline'))
    parser.add_argument('--assessment', action='store_true',
                        help='Allow this explicitly non-formal runtime assessment')
    args = parser.parse_args()
    if args.action == 'check-baseline':
        baseline = json.loads((STATE / 'baseline.json').read_text())
        target = metadata('user_acceptance_test', 810005)
        require(target['schema'] == 'E1_UAT', 'Wrong UAT schema')
        mapped_target(target)
        assert_preserved(baseline['business'], snapshot('user_acceptance_test'))
        print('PASS every prior business field preserved; new rows/columns are permitted')
        return

    archive, digest, evidence, target = inspect()
    if args.action == 'inspect':
        print('PASS inspected D-tested archive, mapping and actual target identity')
        return
    if args.action in ('deploy', 'publish'):
        require(args.assessment, 'Native verification is not clean; use --assessment '
                'only for this documented prototype, not a formal release')

    if args.action == 'deploy':
        fresh = target['business_tables'] == 0 and target['application'] is None
        before = None
        if not fresh:
            mapped_target(target)
            saved_receipt(digest)
            before = snapshot('user_acceptance_test')
            initial_versions(before)
        body = (f'cd "{REPO}"\nset define on\n'
                'define DEFAULTS_FILE=utils/properties/uat.properties\n'
                f'project deploy -file artifact/{archive.name}\n')
        output = execute('user_acceptance_test', body)
        require('Operation completed successfully.' in output,
                'PROJECT did not report a successful deployment')
        require(hashlib.sha256(archive.read_bytes()).hexdigest() == digest,
                'Archive changed during deployment')
        target = metadata('user_acceptance_test', 810005)
        mapped_target(target)
        after = snapshot('user_acceptance_test')
        initial_versions(after)
        print('TARGET AFTER ' + json.dumps(target), flush=True)
        if before is not None:
            require(before == after, 'Identical-artifact repeat changed application data')
        previous = json.loads((STATE / 'deployment.json').read_text()) if not fresh else {}
        receipt = dict(previous, sha256=digest, application_id=810005,
                       schema='E1_UAT', source_commit=evidence['source_commit'],
                       scope='runtime assessment; formal native verification remains blocked',
                       status=target['application']['status'])
        record('deployment.json', receipt)
        print('PASS same-byte UAT deployment; inspect the printed native changeset results')
        print('NEXT browser: VERIFIER greeting/history; LAB_USER must be blocked '
              'while Restricted Access. If already Available, this was a preserved repeat.')
    elif args.action == 'publish':
        mapped_target(target)
        receipt = saved_receipt(digest)
        data = snapshot('user_acceptance_test')
        initial_versions(data)
        require(any(r['ACTOR'] == 'VERIFIER' and r['GREETING_TEXT'] == 'Hello World'
                    for r in data['history']), 'Create the VERIFIER Hello World greeting first')
        if target['application']['status'] != 'Available':
            execute('user_acceptance_test', """begin
  if user<>'E1_UAT' then raise_application_error(-20870,'Wrong target'); end if;
  apex_util.set_workspace('E1_UAT');
  apex_application_admin.set_application_status(810005,apex_application_admin.c_app_available);
  commit;
end;
/""")
        after = snapshot('user_acceptance_test')
        require(data == after, 'Publication changed business data')
        require(metadata('user_acceptance_test', 810005)['application']['status']
                == 'Available', 'Native publication did not enable the application')
        record('deployment.json', dict(receipt, status='Available'))
        print('PASS native UAT publication; business data unchanged')
        print('NEXT browser: sign out of VERIFIER; sign in as LAB_USER; create a greeting.')
    elif args.action == 'baseline':
        mapped_target(target)
        saved_receipt(digest)
        require(target['application']['status'] == 'Available', 'Publish UAT first')
        data = snapshot('user_acceptance_test')
        initial_versions(data)
        require(len(data['hello_config']) == 1 and
                data['hello_config'][0]['PREFIX'] == 'UAT:',
                'Set Hello prefix to "UAT:" first')
        require(any(r['ACTOR'] == 'LAB_USER' and r['GREETING_TEXT'] == 'UAT:Hello World'
                    for r in data['history']), 'Create a LAB_USER greeting with the UAT prefix first')
        path = STATE / 'baseline.json'
        if path.exists():
            baseline = json.loads(path.read_text())
            require(baseline['sha256'] == digest and baseline['application_id'] == 810005,
                    'Existing baseline belongs to another initial artifact/target')
            assert_preserved(baseline['business'], data)
            print('PASS existing immutable baseline retained; prior fields match')
        else:
            record('baseline.json', {'sha256': digest, 'application_id': 810005,
                                     'business': data})
            print('PASS saved immutable baseline ' + str(path.relative_to(ROOT)))
        print('BASELINE counts ' + json.dumps({t: len(data[t]) for t in BUSINESS}))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, RuntimeError, KeyError, json.JSONDecodeError) as exc:
        print('BLOCKED: ' + str(exc), file=sys.stderr)
        sys.exit(1)
