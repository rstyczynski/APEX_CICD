#!/usr/bin/env bash
# Source this file. It selects local tools/connections; it changes no target.
APEX_CICD_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export JAVA_HOME="$APEX_CICD_ROOT/.local-apex/tools/jdk-21.0.12.1+1/Contents/Home"
export PATH="$APEX_CICD_ROOT/.local-apex/tools/sqlcl/bin:$PATH"
export APEX_CICD_CONNECTIONS="$APEX_CICD_ROOT/.local-apex/tools/sqlcl-home"
unset APEX_CICD_ROOT
