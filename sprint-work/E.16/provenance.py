"""Fail-closed archive/source/tool identity check before native deployment."""
import hashlib
BUILD='25.4.1.022.0618'
def guard(archive,receipt,source,tool):
    assert receipt['source']==source,'source mismatch'
    assert receipt['build']==tool==BUILD,'tool mismatch'
    assert receipt['sha256']==hashlib.sha256(archive.read_bytes()).hexdigest(),'artifact mismatch'

if __name__=='__main__':
    import json,sys
    from pathlib import Path
    try:guard(Path(sys.argv[1]),json.loads(Path(sys.argv[2]).read_text()),sys.argv[3],sys.argv[4])
    except AssertionError as error:raise SystemExit(str(error))
