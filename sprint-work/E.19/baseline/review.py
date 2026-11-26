import hashlib,json,sys
from pathlib import Path
assert json.loads(Path(sys.argv[1]).read_text())==['candidate.sql'],'unreviewed files'
report=json.loads(Path(sys.argv[2]).read_text())
assert report['decision']=='accept'
assert hashlib.sha256(Path(sys.argv[3]).read_bytes()).hexdigest()==report['sql_sha256'],'stale Review'
