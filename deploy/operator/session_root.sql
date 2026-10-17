-- Invoke from a shell already positioned by git rev-parse; argument is "$PWD".
set define on verify off
define REPO_ROOT = '&1'
cd "&REPO_ROOT"
