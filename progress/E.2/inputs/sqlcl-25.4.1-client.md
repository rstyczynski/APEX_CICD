# SQLcl 25.4.1 verification client

This installs a separate client for the corrected G verification exercise.
It does not replace SQLcl 25.3, alter the F archives, or migrate a database.
The existing pinned Java 21 installation and saved-connection store are inputs.

Oracle publishes build **25.4.1.022.0618** and ZIP SHA1
**1ce64ff5778c0fb739f7d9724eebfcc9c1aacfeb** on its
[previous downloads page](https://www.oracle.com/tools/sqlcl/sqlcl-downloads.html).

In a regular shell, download the exact build:

```bash
cd /Users/rstyczynski/projects/APEX_CICD
curl -fL --connect-timeout 15 --max-time 180 \
  -o .local-apex/tools/sqlcl-25.4.1.022.0618.zip \
  https://download.oracle.com/otn_software/java/sqldeveloper/sqlcl-25.4.1.022.0618.zip
```

Verify the download, extract it only if absent, and copy the connection store
only if its separate destination is absent. No password is printed:

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib, shutil, zipfile
root = Path('/Users/rstyczynski/projects/APEX_CICD')
archive = root / '.local-apex/tools/sqlcl-25.4.1.022.0618.zip'
assert hashlib.sha1(archive.read_bytes()).hexdigest() == '1ce64ff5778c0fb739f7d9724eebfcc9c1aacfeb', 'Wrong client download'
destination = root / '.local-apex/tools/sqlcl-25.4.1.022.0618'
if not destination.exists():
    with zipfile.ZipFile(archive) as z:
        assert all((destination / n).resolve().is_relative_to(destination.resolve()) for n in z.namelist())
        z.extractall(destination)
client = destination / 'sqlcl/bin/sql'
assert client.is_file(), 'Incomplete client installation'
client.chmod(0o755)
home = root / '.local-apex/tools/sqlcl-home-25.4.1-qualification'
if not home.exists():
    shutil.copytree(root / '.local-apex/tools/sqlcl-home', home)
home.chmod(0o700)
print('PASS pinned client integrity and separate installation/store')
PY
JAVA_HOME="$PWD/.local-apex/tools/jdk-21.0.12.1+1/Contents/Home" \
  .local-apex/tools/sqlcl-25.4.1.022.0618/sqlcl/bin/sql -version
```

Require **Release 25.4.1.0 / Build 25.4.1.022.0618**. Continue at G.2 in the
[walkthrough](../cicd-walkthrough.md). This procedure has already supplied the
client for the current laboratory; reinstalling it is not part of G execution.
