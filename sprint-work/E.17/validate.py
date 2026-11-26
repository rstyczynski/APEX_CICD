"""Trusted candidate validator; candidate input is SQL data, never host code."""
import os
from pathlib import Path

def load(path):
    p = Path(path)
    if p.name != 'candidate.sql' or p.is_symlink():
        raise ValueError('only candidate.sql regular input accepted')
    source = p.read_text()
    if len(source) > 8192 or not source.strip():
        raise ValueError('empty or oversized SQL')
    return source

def main():
    import oracledb
    source = load('candidate.sql')
    with oracledb.connect(user='candidate', password=os.environ['CANDIDATE_PASSWORD'],
                         dsn='localhost:1521/FREEPDB1') as conn:
        conn.call_timeout = 30000
        with conn.cursor() as cur:
            cur.execute(source)
            rows = cur.fetchall()
            assert rows == [('Hello World',)], rows
            cur.execute("select sys_context('USERENV','SESSION_USER') from dual")
            assert cur.fetchone() == ('CANDIDATE',)
            try:
                cur.execute('select * from system.e15_private')
            except oracledb.DatabaseError as exc:
                assert exc.args[0].code == 942, exc
            else:
                raise AssertionError('private table readable')
            print('PASS real Oracle greeting, schema identity and private-table refusal')

if __name__ == '__main__':
    main()
