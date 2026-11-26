"""Validate measured SQLcl identity and native metadata without invoking tools."""
import json,sys
from pathlib import Path
text=Path(sys.argv[1]).read_text()
if 'Release 25.4.1.0 Production Build: 25.4.1.022.0618' not in text:
    raise SystemExit('tool mismatch')
config=Path('.dbtools/project.config.json')
if config.exists() and json.loads(config.read_text())['sqlcl']['version']!='25.4.1.0':
    raise SystemExit('metadata version mismatch')
